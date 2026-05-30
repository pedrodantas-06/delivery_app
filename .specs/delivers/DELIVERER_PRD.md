# Deliverer PRD — Delivery Universitário

Last updated: 2026-05-30

1. Visão do Produto
-------------------
Pequeno conjunto de funcionalidades para permitir que entregadores (alunos/colaboradores) recebam e concluam entregas no campus com a menor complexidade possível. O foco é permitir que um cliente faça um pedido, que o restaurante aceite, e que um entregador execute a entrega até a confirmação.

2. Problema resolvido
---------------------
- Restaurantes precisam de entregadores disponíveis e um fluxo simples de atribuição/aceitação para operar dentro do campus.
- Entregadores precisam de interface clara para aceitar, confirmar coleta e confirmar entrega.

3. Personas
-----------
- Entregador: aluno voluntário/freelancer que quer aceitar entregas no campus. Requisitos: simplicidade, baixa latência, controle de disponibilidade.
- Restaurante: parceiro que prepara alimentos e precisa confirmar prontidão.
- Cliente: estudante que cria pedido e acompanha status.

4. Objetivos
-----------
- Implementar registro, disponibilidade e ciclo de entrega (aceitar → buscar → entregar) em 2-3 sprints.
- Minimizar dependências técnicas adicionais (sem WebSockets, sem filas).

5. User Stories (exemplos)
--------------------------
- US-1 (P0): Como entregador, quero me registrar e indicar disponibilidade para receber entregas.
- US-2 (P0): Como sistema, quero atribuir automaticamente um entregador disponível por região quando houver um pedido pronto.
- US-3 (P0): Como entregador, quero aceitar um pedido atribuído para passar ao status `IN_DELIVERY`.
- US-4 (P0): Como entregador, quero marcar `PICKED_UP` e `DELIVERED` para cada entrega.
- US-5 (P1): Como entregador, quero ver histórico de entregas.

6. Requisitos Funcionais (mínimos)
---------------------------------
- RF-1: Registrar entregador (`POST /api/v1/deliverers`).
- RF-2: Atualizar status (`PATCH /api/v1/deliverers/{id}/status`).
- RF-3: Listar entregadores por status/região (`GET /api/v1/deliverers`).
- RF-4: Assign order (`POST /api/v1/deliveries/assign`).
- RF-5: Accept delivery (if broadcasted) or confirm assignment success (`POST /api/v1/deliveries/{id}/accept` or implicit by assignment). 
- RF-6: Pickup/Deliver transitions (`PATCH /api/v1/deliveries/{id}/pickup`, `/deliver`).

7. Requisitos Não Funcionais
---------------------------
- Persistência PostgreSQL via SQLAlchemy + Alembic migrations.
- JWT auth for deliverer endpoints.
- Logs: criar eventos para `delivery_assigned`, `delivery_picked_up`, `delivery_delivered`.
- Tests: unit + integration + BDD for all RFs.

8. Fluxos Principais (resumidos)
--------------------------------
Aceitar Entrega (assign simple flow)
1. Pedido criado e pago → Restaurante marca READY
2. Sistema chama `DeliveryAssignmentService.assign(order_id, region)`
3. Service encontra `Deliverer` AVAILABLE na mesma região e atomically marca deliverer OCCUPIED e cria Delivery with status `IN_DELIVERY`
4. Response returns assigned deliverer id

Coletar Pedido
1. Deliverer marca `pickup` via API
2. System records `picked_up_at`

Entregar Pedido
1. Deliverer marca `deliver` via API
2. System records `delivered_at` and sets order status `DELIVERED`

9. Critérios de Aceite
---------------------
- Registro: `POST /api/v1/deliverers` cria entregador e retorna 201 com `id`.
- Assignment: `POST /api/v1/deliveries/assign` com `order_id` e `region` retorna `IN_DELIVERY` e `assigned_deliverer_id` quando há deliverer disponível.
- Transições: `pickup` e `deliver` endpoints mudam status corretamente e persistem timestamps.
- Segurança: apenas token JWT válido com role `DELIVERYMAN` permite endpoints de ação.
- Testes: cada fluxo principal tem BDD feature e CI passa testes.

10. Escopo MVP (o que está incluído)
----------------------------------
- Registro / disponibilidade
- Assignment (automático / manual)
- Pickup / Deliver transitions
- Basic UI in deliverer SPA (dashboard, active delivery)
- Persistence + migrations
- Tests + BDD

11. Fora de Escopo (MVP)
-----------------------
- Roteirização, otimização de rotas
- Notificações push reais / WebSockets (simular com polling)
- Pagamentos ao entregador
- Relatórios avançados

12. Roadmap Técnico (3 sprints sugeridos)
---------------------------------------
- Sprint A (1): Modelos SQLAlchemy + migrations; APIs: register, list, update status; frontend basic register/list.
- Sprint B (2): Assignment service + endpoints assign/reassign; pickup/deliver endpoints; integration tests + BDD.
- Sprint C (3): UI polish, history, auth hardening, performance and observability logs.

13. Medidas de Sucesso
---------------------
- Entregador consegue aceitar e completar uma entrega em menos de 3 minutos após implementação.
- 90% dos fluxos principais cobertos por testes automatizados.

14. Dependências e riscos
------------------------
- Risco: dívida técnica por coexistência de MySQL/Django; mitigação: encapsular e migrar incrementalmente.

15. Recomendações operacionais
-----------------------------
- Não introduzir WebSockets neste PRD — simular broadcast com polling UI.
- Priorizar confiabilidade das transições de status (atomicidade no banco) — use transactions.
- Mantenha a UX do entregador minimalista e com feedbacks claros.
