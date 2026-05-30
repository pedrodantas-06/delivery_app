# Deliverer Research Report

Last updated: 2026-05-30

Resumo executivo
----------------
- Objetivo: entender como a funcionalidade de `Deliverer` (Entregador) foi concebida na base atual e propor integração com mínima complexidade.
- Conclusão curta: a base já possui uma implementação focalizada em entregadores (módulo `modulos.delivery`) com rotas HTTP, serviços e repositórios em memória e protótipos de persistência. Há vestígios de código legado (Django/DRF, MySQL) e uma mistura de abordagens que devem ser saneadas antes da produção. O entregador deve ser mantido como domínio leve no monólito, com APIs REST específicas e sem introduzir filas ou realtime obrigatório para MVP.

1. Estado atual do projeto (sumário técnico)
-----------------------------------------
- Backend: FastAPI app em `backend/main.py`. Módulos principais já criados, especialmente `modulos/delivery` (deliverers + pagamento). Alguns arquivos usam patterns Django/DRF (views/rotas) e há um `core/conexao_banco.py` que abre conexões MySQL diretamente — divergência técnica.
- Persistência: duas abordagens coexistem: repositórios em memória (`InMemoryDelivererRepository`) usados em testes e em `wires.py` para ambiente de desenvolvimento; também existe `repositories.py` que usa modelos (aparentemente Django ORM) — inconsistente com objetivo SQLAlchemy+Postgres.
- Frontend: SPA React + Vite com protótipo de gestão de entregadores em `frontend/App.tsx` e componentes simples em `frontend/src/componentes`.
- BDD: muitos cenários Gherkin existentes (backend e frontend) cobrindo entregadores, restaurantes, pagamentos, clientes e carrinho.

Observações críticas
- Há dependências técnicas inconsistentes: MySQL connector + Django views + FastAPI coexistindo. Antes de expandir, padronizar stack (FastAPI + SQLAlchemy + Postgres) evita dívida.
- O domínio de entregadores já está implementado de forma funcional (registro, listagem, atualização de status, atribuição/reatribuição), o que reduz risco de implementação.

2. Inventário de cenários Gherkin (resumo)
-----------------------------------------
Tabela resumida (cenários relevantes para entregador)

| Cenário | Usuário | Objetivo | Dependências |
|---|---:|---|---|
| cadastrar entregador com sucesso | Admin/Operador / UI | Criar entregador com status AVAILABLE | API `POST /api/deliverers/` |
| atualizar status do entregador | Entregador / API | Atualizar disponibilidade (AVAILABLE/OCCUPIED/OFFLINE) | API `PATCH /api/deliverers/{id}/status/` |
| listar entregadores por status | Admin/Operador / UI | Filtrar lista por status/region | API `GET /api/deliverers/?status=...` |
| atribuir entregador automaticamente | Sistema (Orders -> Deliverers) | Atribuir entregador disponível por região | Order service + deliverer repo |
| atribuir entregador manualmente | Restaurante/Dispatcher | Designar entregador específico | deliverer lookup + validation |
| nao atribuir quando nao ha entregador disponivel | Sistema | Gerar erro quando não há entregadores | Repo find_available_by_region |
| impedir atribuicao para entregador ocupado | Sistema | Validar estado do entregador | Deliverer.status check |
| reatribuir pedido apos recusa | Sistema | Reatribuir quando entregador recusa | Order + deliverer repo |
| distribuir/aceite/concorrencia (frontend) | Entregador (app) | Distribuir para múltiplos entregadores e aceitar por concorrência | Notificações (simuladas), contratos de aceitação |

Status dos cenários
- Cobertos e automatizados (backend): principais cenários de gestão e atribuição (vários testes e integração via `tests/test_deliverers_integration.py` e `tests/test_deliverers_service.py`).
- Cobertos UI: protótipos de testes E2E/Cypress e cenários frontend BDD que exercitam cadastro e aceitação/recusa em nível de interface.
- Incompletos/implicitamente esperados: fluxos de distribuição em broadcast (notificações/concorrência) são escritos em Gherkin, mas a infra de notificações/realtime não existe — são simulados no MVP.

Gaps identificados nos cenários
- Fluxo de aceite concorrente assume broadcast/notifications; necessidades de infra (WebSockets, push) não devem entrar no MVP — simular via polling ou chamadas polled por UI.
- Falta de cenários de segurança/autorizações específicas para entregador (login, perfil, segurança do token/rotas).

3. Inventário das implementações existentes (backend)
--------------------------------------------------
Tabela resumida

| Módulo | Status | Observações |
|---|---|---|
| `modulos/delivery` | Implementado (parcial) | Serviços de `Deliverer` com `DelivererService`, repositórios em memória e implementação de rotas em `http/api.py`. Testes unitários e integração existem. |
| `modulos/delivery/infrastructure/repositories.py` | Implementado (Django ORM style) | Usa modelos `DelivererModel`, `OrderModel` (Django ORM style). Incompatível com objetivo SQLAlchemy/Postgres. |
| `modulos/delivery/infrastructure/memory_repositories.py` | Implementado | InMemory repos usados por `wires.py` e testes — ótimo para TDD e prototipagem. |
| `modulos/delivery/http/views/*` | Implementado | Há views em estilo Django e rotas FastAPI coexistindo — precisa unificar. |
| `modulos/pagamento/controle.py` | Implementado (procedural) | Acesso direto ao banco via `ConexaoBanco` (MySQL). Lógica de estorno e métodos de pagamento existe. Precisa ser migrada para service/repository padrão e Postgres. |
| `core/conexao_banco.py` | Implementado (MySQL) | Usa mysql.connector pooling — contradiz o objetivo Postgres/SQLAlchemy. |
| `core/config.py` | Implementado | Usa Pydantic settings; API base path configured. Bom. |
| Auth / Users | Parcial/placeholder | Existem módulos `modulos/cliente` e `modulos/cliente/placeholder` — autenticação detalhada não encontrada consistentemente; PRD exige JWT. |

APIs já implementadas
- `/api/deliverers/` GET/POST
- `/api/deliverers/{id}/status/` PATCH
- `/api/orders/assign/` POST
- `/api/orders/{order_id}/reassign/` POST
- Payment endpoints exist but implemented em estilo Django views (`/api/pagamento/...`) e usam DB direto.

4. Fluxo de negócio (entrega) — mapa de interação
------------------------------------------------
Fluxo principal

Client -> Frontend -> POST /api/v1/orders -> Order created (PENDING) -> Payment processing -> Restaurant accepts -> System assigns deliverer -> Delivery status transitions -> Delivered

Onde o Deliverer entra
- Assignment: After order is PAID (or after accepted), the system assigns a deliverer available in the order's region.
- Acceptance: Deliverer accepts assignment (in current base, assignment is immediate: the system finds an available deliverer and marks order IN_DELIVERY).
- Status updates: deliverer updates status to PICKED_UP, DELIVERED.

Quem inicia a interação
- System (assignment) triggered by order events; deliverer updates are initiated by the deliverer via UI or API.

Quem atualiza status
- Restaurant updates PREPARING/READY
- Deliverer updates PICKED_UP/DELIVERED
- System records transitions and audits

5. UX e Design — o que existe e recomendações
-------------------------------------------
Arquivos: `FRONTEND-RULE.md` e componentes simples em `frontend/src/componentes`.

Como o Deliverer deve navegar (MVP)
- Tela principal: Lista de entregas disponíveis / Aceitar
- Tela de atividade: Entregas ativas (um cartão por entrega) com passos: aceitar -> buscar -> entregue
- Perfil: Estado online/offline
- Histórico: lista simples de entregas anteriores

Telas mínimas para MVP
- Login (JWT)
- Dashboard: Filtrar por região, ver disponibilidade
- Delivery Card: Ação `Aceitar` / `Recusar` / `Confirmar entrega`
- Perfil: Toggle `Disponível` / `Indisponível`

O que pode ser removido no MVP
- Roteirização, mapa em tempo real, notificações push reais, complexa tela de analytics

6. Benchmark rápido de entregadores (resumo)
------------------------------------------
MVP funcionalidades mínimas (benchmark: iFood/Uber/Rappi)
- Disponibilidade online/offline (P0)
- Receber tarefas/entregas e aceitar (P0)
- Marcar coleta e entrega (P0)
- Histórico de entregas (P1)

Funcionalidades opcionais (P1)
- Notificações em tempo real (WebSocket ou push)
- Aceitação concorrente/broadcast (simulação via polling para MVP)

Funcionalidades avançadas (P2)
- Navegação integrada, otimização de rota, pagamentos ao entregador, escalonamento automático, ranking

7. Modelagem de domínio mínima proposta
-------------------------------------
Entidades essenciais
- `Deliverer` (id, user_id, name, phone, region, status, created_at)
- `Delivery` (id, order_id, deliverer_id nullable, status, assigned_at, picked_up_at, delivered_at)

Relações e regras essenciais
- Um `Delivery` pertence a um `Order`.
- O `Deliverer` tem `status` (AVAILABLE, OCCUPIED, OFFLINE).
- Assignment: somente `Deliverer.status == AVAILABLE` e `Deliverer.region == Order.region`.
- Snapshot: manter dados críticos no `Delivery`/`Order` para histórico.

8. APIs propostas (mínimas) — alinhadas ao que existe
---------------------------------------------------
Notas: aproveitar e unificar as rotas já existentes em `modulos/delivery/http/api.py` para `/api/v1` e padronizar respostas de erro.

Endpoints mínimos (P0)
- `GET /api/v1/deliverers?status=&region=` — listar
- `POST /api/v1/deliverers` — registrar entregador
- `PATCH /api/v1/deliverers/{id}/status` — alterar status
- `POST /api/v1/deliveries/assign` — assignar entregador (order_id, region, optional deliverer_id)
- `POST /api/v1/deliveries/{id}/reassign` — reatribuir
- `POST /api/v1/deliveries/{id}/accept` — accept delivery (if using broadcast simulated)
- `PATCH /api/v1/deliveries/{id}/pickup` — mark pickup
- `PATCH /api/v1/deliveries/{id}/deliver` — mark delivered

9. Serviços necessários (backend)
--------------------------------
- `DelivererService` — registro, listagem, update_status, find_available_by_region
- `DeliveryAssignmentService` — lógica de seleção e atribuição (wrap around DelivererService)
- `DeliveryLifecycleService` — pickup/deliver transitions and validations

10. Banco de dados
------------------
- Recomendação imediata: padronizar para PostgreSQL + SQLAlchemy (Alembic migrations). Migrar scripts/daos que usam MySQL/Django.
- Migrations obrigatórias para criar `deliverers`, `deliveries` e relações com `orders`.

11. Critérios de aceite (exemplos)
--------------------------------
- Entregador se registra e aparece na lista (API + UI).
- Sistema atribui entregador disponível e marca `Order.status` como `IN_DELIVERY`.
- Entregador pode marcar como `PICKED_UP` e `DELIVERED` e o pedido reflete mudanças (persistência).
- Cenários BDD para os fluxos críticos passarem no pipeline.

12. Riscos e dívida técnica
---------------------------
- Mistura de frameworks (FastAPI + Django/DRF) e DB drivers (MySQL connector) cria dívida técnica.
- Recomendação: antes da large-surface refactor, encapsular entregadores em uma camada que use SQLAlchemy e manter InMemory para testes.

Conclusão e próximo passo recomendado
------------------------------------
- Priorizar: padronizar persistência (Postgres+SQLAlchemy) e unificar rotas em `/api/v1` no FastAPI. Em seguida, mover a lógica existente de `Deliverer` para usar repositórios SQLAlchemy (facilitando disponibilidade de dados) e manter InMemory para testes.
- Implementação incremental: 1) API e modelos SQLAlchemy para `deliverers` e `deliveries`; 2) migrar testes de integração; 3) ajustar frontend para `/api/v1` e garantir BDD.
