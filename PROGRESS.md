# Progress — Deliverer Feature

## Visão Geral do Projeto

O MVP resolve o fluxo de entrega do pedido dentro do domínio de delivery da aplicação. A meta foi sair de um protótipo misto, com resquícios de Django e uma interface monolítica, para uma feature Deliverer fechada, testada e apresentável.

### Objetivo do MVP

Permitir cadastrar entregadores, atualizar status, atribuir pedidos, aceitar entregas, executar pickup e concluir a entrega final com rastreabilidade mínima do ciclo.

### Escopo

- Backend Deliverer completo.
- Persistência relacional com SQLAlchemy e migrações Alembic.
- BDD cobrindo o comportamento principal da feature.
- Frontend modular em React/Vite com a feature isolada.
- Testes de serviço, integração, BDD, hooks e componentes.

### Tecnologias

- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- React
- Vite
- TypeScript
- Jest
- Testing Library
- pytest
- pytest-bdd

### Arquitetura Escolhida

- Backend monólito modular por domínio.
- Frontend feature driven architecture.
- Camadas explícitas para domain, services, repositories, HTTP e UI.

### Motivos da Simplificação

- Evitar complexidade de microsserviços para um único fluxo operacional.
- Reduzir dependências de frameworks legados.
- Tornar o comportamento fácil de testar em cada camada.
- Facilitar demonstração técnica e evolução incremental.

## Linha do Tempo

### Investigação

- O deliverer já existia como protótipo, mas o backend ainda carregava peças de Django e o frontend concentrava toda a lógica em um único arquivo.
- Foram identificados pontos de acoplamento entre UI, estado local e chamadas HTTP.
- Também foi identificado que os cenários BDD usavam identificadores não estritamente UUID, exigindo normalização na borda HTTP.

### Problemas Encontrados

- Persistência inconsistente entre o código e a modelagem desejada.
- Estado de entrega sem uma máquina de estados clara.
- Interface frontend monolítica, difícil de testar e evoluir.
- Necessidade de compatibilizar fixtures BDD com IDs gerados fora do formato UUID.

### Decisões Tomadas

- Substituir a persistência legacy por SQLAlchemy.
- Centralizar regras de negócio no serviço do domínio Deliverer.
- Normalizar IDs na borda HTTP para preservar o contrato do BDD.
- Refatorar o frontend em módulos feature driven.
- Adotar testes por camada como critério de finalização.

## Backend

### Persistência

- Foram criadas entidades e repositórios para deliverers, deliveries e assignments.
- A persistência passou a usar SQLAlchemy com migração Alembic dedicada.
- Repositórios em memória foram mantidos apenas para testes unitários.

### Serviços

- A lógica de cadastro, atualização de status e transições da entrega foi concentrada em um serviço de domínio.
- O serviço passou a coordenar atribuição automática, reatribuição e transições de pickup/deliver.
- O fluxo ficou orientado por regras explícitas, não por efeitos colaterais espalhados.

### APIs

- A API expõe os endpoints do fluxo Deliverer sob `/api/v1`.
- A borda HTTP converte payloads em comandos de domínio.
- IDs de entrada são normalizados para manter compatibilidade com BDD e integração.

### State Machine

- O status do deliverer segue a trilha operacional da feature.
- O estado da entrega controla as transições entre espera, atribuição, coleta, conclusão e cancelamento.

### Auditoria

- As operações relevantes registram rastreio de atribuição e mudança de estado.
- O objetivo foi permitir inspeção do ciclo da entrega sem introduzir infraestrutura extra.

### BDD

- Foi mantido o contrato funcional descrito nos cenários da feature Deliverer.
- O comportamento principal foi validado com pytest-bdd e fixtures compatíveis com o fluxo esperado.

### Testes

- Cobertura de serviço para status, atribuição e transições.
- Cobertura de integração para endpoints principais.
- Cobertura BDD para o cenário de cadastro do entregador.
- Execução da suíte focada com resultado verde.

## Frontend

### Estrutura Original

- A UI do Deliverer começou concentrada em `frontend/App.tsx`.
- O arquivo continha login, dashboard, histórico, perfil, polling e chamadas HTTP.

### Problemas Identificados

- Alto acoplamento entre renderização e acesso à API.
- Dificuldade para testar estados isolados.
- Reuso mínimo de UI.
- Baixa escalabilidade para crescimento da feature.

### Refatoração

- O frontend foi dividido em `src/features/deliverer` e `src/shared`.
- Fetches foram movidos para API/services/hook layers.
- As páginas passaram a orquestrar os componentes sem carregar regras de acesso a dados.
- A configuração do Jest foi separada em backend-bdd e frontend-deliverer.

### Estrutura Final

- `frontend/src/app`
- `frontend/src/features/deliverer`
- `frontend/src/shared`
- Wrappers legados mantidos apenas para compatibilidade de import.

### Design Adotado

- Visual mais editorial e menos genérico.
- Cartões, hero e badges com contraste suave.
- Layout responsivo com espaço para apresentação técnica.

## Refatorações

### Remoção Django

- Eliminou o resíduo do stack legado.
- Reduziu ambiguidade de implementação.
- Facilitou manutenção e entendimento do módulo.

### SQLAlchemy

- Tornou a camada de persistência explícita e testável.
- Aproximeou o código do fluxo relacional real do domínio.
- Simplificou a integração com a API e os testes.

### Modularização Frontend

- Separou UI, estado, serviços e chamadas HTTP.
- Permitiu testes mais finos por responsabilidade.
- Preparou a base para evolução de outras features.

### Normalização de APIs

- Aceitou entradas não estritamente UUID nos cenários de teste.
- Manteve o contrato do domínio intacto.
- Melhorou a compatibilidade entre BDD e implementação.

## Evidências

### RFs Implementados

- Cadastro de entregador.
- Atualização de status.
- Atribuição de pedido.
- Reatribuição por regra operacional.
- Accept do pedido.
- Pickup.
- Deliver final.

### Cenários BDD

- Cadastro do entregador com sucesso.
- Fluxos de entrega validados por integração e serviço.

### Endpoints

- GET `/api/v1/deliverers/`
- POST `/api/v1/deliverers/`
- PATCH `/api/v1/deliverers/{deliverer_id}/status/`
- POST `/api/v1/orders/assign/`
- GET `/api/v1/orders/`
- POST `/api/v1/orders/{order_id}/reassign/`
- POST `/api/v1/orders/{order_id}/accept/`
- PATCH `/api/v1/orders/{order_id}/pickup/`
- PATCH `/api/v1/orders/{order_id}/deliver/`

### Cobertura

- 4 arquivos de teste backend.
- 1 feature BDD principal com cenário outline.
- 7 suites de teste frontend para hooks e componentes.

## Commits Importantes

| Commit | Objetivo |
|---|---|
| 8e38be7 | Substituir a persistência Django por SQLAlchemy e consolidar a base do backend Deliverer. |
| 98c94b4 | Adicionar endpoints de entrega e ampliar a cobertura de testes de integração e serviço. |
| 7e01be8 | Introduzir a SPA do Deliverer e fechar o ciclo de progresso/documentação da feature. |

## Branches

| Branch | Objetivo |
|---|---|
| main | Linha estável do repositório. |
| feature/deliverer-complete | Branch atual com a entrega completa da feature Deliverer. |
| test/deliverers-bdd-e2e | Branch histórica usada na validação BDD/e2e. |

## Pull Requests

| PR | Objetivo |
|---|---|
| #29 | Consolidar a implementação completa do módulo Deliverer com backend, BDD, frontend e testes. |

## Lições Aprendidas

### Técnicas

- Separar domínio, serviço e persistência reduz retrabalho em refatorações.
- Normalizar a borda HTTP é mais barato do que espalhar exceções pelo domínio.
- Um monólito modular é suficiente para uma feature com um fluxo bem definido.

### Produto

- O MVP ficou mais fácil de explicar depois que o fluxo foi enxuto e linear.
- A tela do entregador ganhou clareza ao mostrar apenas estados operacionais.

### Arquitetura

- A feature driven architecture funcionou bem no frontend porque o escopo era fechado.
- Wrappers legados evitaram quebra de import durante a migração.

### BDD

- O BDD funcionou como contrato do comportamento esperado.
- Fixtures consistentes e IDs normalizados evitam ruído desnecessário no passo a passo.

