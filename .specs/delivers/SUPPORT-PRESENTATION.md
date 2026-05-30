# 1. Resumo Executivo

A feature Deliverer foi concluída para resolver o fluxo operacional de entrega dentro do MVP. O objetivo era sair de uma implementação híbrida e pouco organizada para uma solução legível, testável e fácil de apresentar.

O problema resolvido foi a falta de uma cadeia completa e coerente para cadastro de entregador, atribuição de pedido, aceitação, pickup e conclusão da entrega. O resultado final cobre backend, BDD, frontend modular e documentação de apoio.

# 2. Visão do Produto

Fluxo principal:

Cliente → Pedido → Restaurante → Deliverer → Entrega

Explicação:

- O cliente cria o pedido.
- O pedido segue para o restaurante.
- O restaurante prepara e libera a operação.
- O Deliverer recebe ou aceita a entrega.
- O status evolui até a conclusão da entrega.

A feature Deliverer existe para fechar o trecho operacional entre a preparação do pedido e a finalização da entrega, sem introduzir complexidade desnecessária no restante do produto.

# 3. Arquitetura Geral

Diagrama textual:

```text
Frontend React + Vite
↓
FastAPI
↓
Services
↓
Repositories
↓
PostgreSQL
```

Responsabilidades:

- O frontend apresenta a experiência do entregador e consome a API.
- A API FastAPI expõe o contrato HTTP e valida os payloads.
- Os services concentram as regras de negócio.
- Os repositories encapsulam a persistência.
- O PostgreSQL mantém os dados do domínio.

# 4. Arquitetura Backend

## Domain

O domínio foi separado para manter o núcleo de negócio previsível.

### Entities

- Deliverer
- Delivery

As entidades representam o estado operacional do entregador e do pedido em entrega.

### Enums

- DelivererStatus
- DeliveryStatus

Os enums controlam os estados válidos e evitam transições implícitas fora do fluxo esperado.

## Services

Na prática, a feature concentra sua lógica principal no serviço do módulo de Deliverer, que cobre três responsabilidades conceituais:

- DelivererService: cadastro, status e visão do entregador.
- DeliveryAssignmentService: atribuição e reatribuição de pedidos.
- DeliveryService: accept, pickup e deliver.

Essa separação é útil para explicar o domínio, mesmo quando a implementação está concentrada em um serviço orquestrador.

## Repositories

- InMemory: usado nos testes unitários e no raciocínio rápido do domínio.
- SQLAlchemy: usado na persistência real com PostgreSQL.

A escolha dos dois estilos facilita teste isolado sem perder o caminho real de produção.

## APIs

Endpoints principais:

- GET /api/v1/deliverers/
- POST /api/v1/deliverers/
- PATCH /api/v1/deliverers/{deliverer_id}/status/
- POST /api/v1/orders/assign/
- GET /api/v1/orders/
- POST /api/v1/orders/{order_id}/reassign/
- POST /api/v1/orders/{order_id}/accept/
- PATCH /api/v1/orders/{order_id}/pickup/
- PATCH /api/v1/orders/{order_id}/deliver/

Exemplos de uso:

- Registrar um entregador para iniciar o ciclo operacional.
- Atribuir um pedido automaticamente pela região.
- Reatribuir um pedido quando a primeira tentativa falhar.
- Confirmar acceptance, pickup e finalização do pedido.

# 5. Arquitetura Frontend

A interface foi reorganizada em Feature Driven Architecture para isolar a feature Deliverer.

Estrutura principal:

```text
src/
  app/
  features/
    deliverer/
  shared/
```

Explicação:

- app contém o ponto de composição da aplicação.
- features/deliverer contém a feature isolada, com API, services, hooks, components, pages e routes.
- shared contém os componentes e helpers reutilizáveis.

Benefício principal:

- a feature passa a evoluir sem depender de um arquivo único gigante ou de efeitos colaterais espalhados.

# 6. Exemplo de Fluxo Completo

Passo a passo:

1. Pedido pronto.
2. O sistema faz assign para um entregador compatível.
3. O entregador aceita a entrega.
4. O entregador executa pickup.
5. O entregador conclui a entrega com deliver.

O valor desse fluxo é mostrar a progressão do estado de forma linear e verificável.

# 7. Exemplo de Cenário BDD

Cenário escolhido:

```gherkin
Feature: Deliverer BDD

  Scenario Outline: cadastrar entregador com sucesso
    Given nenhum entregador existe
    When eu cadastro um entregador com nome "<name>" telefone "<phone>" regiao "<region>"
    Then o entregador "<name>" deve ficar com status "<status>"
```

Por que ele existe:

- Ele valida a entrada principal da feature.
- Ele mostra que o contrato do sistema começa com um cadastro consistente.
- Ele evita regressões no estado inicial do entregador.

# 8. Exemplo de Teste Backend

Teste escolhido: `test_assigns_deliverer_automatically_in_same_region`

```python
from uuid import uuid4

from modulos.delivery.application.services.deliverers_service import DelivererService
from modulos.delivery.infrastructure.memory_repositories import (
    InMemoryDelivererRepository,
    InMemoryOrderRepository,
)


def test_assigns_deliverer_automatically_in_same_region():
    service = DelivererService(
        InMemoryDelivererRepository(), InMemoryOrderRepository())
    deliverer = service.register_deliverer('Ana', '11999999999', 'Zona Sul')

    order = service.assign_deliverer(uuid4(), 'Zona Sul')

    assert order.status.value == 'ASSIGNED'
    assert order.deliverer_id == deliverer.id
```

Explicação em Arrange, Act, Assert:

- Arrange: cria o service e registra um entregador.
- Act: executa a atribuição de pedido na mesma região.
- Assert: confirma que o pedido foi marcado como ASSIGNED e associado ao entregador.

# 9. Exemplo de Teste Frontend

Componente escolhido: DeliveryCard

Teste relevante:

```tsx
render(
  <DeliveryCard
    delivery={delivery}
    actions={{
      onPickup: () => {},
      onDeliver: () => {},
    }}
  />,
)
```

O que ele valida:

- O cartão mostra o pedido.
- O cartão mostra a região.
- O cartão mostra o entregador associado.
- Os botões de ação aparecem quando o componente recebe ações.

Por que isso importa:

- Confirma a composição visual do módulo sem depender de toda a SPA.
- Garante que a interface de entrega continua legível e testável.

# 10. Exemplo de Service

Serviço escolhido: accept_delivery

Motivação:

- É uma transição crítica do estado do pedido.
- Representa uma regra central do fluxo operacional.

Leitura conceitual do fluxo:

1. Receber o ID do pedido e o ID do entregador.
2. Validar se o pedido pode ser aceito.
3. Vincular o entregador ao pedido.
4. Atualizar o status para indicar que a entrega foi assumida.
5. Persistir a transição.

Regras de negócio:

- Só entregadores válidos podem assumir o pedido.
- A transição precisa respeitar o estado atual da entrega.
- O retorno precisa refletir o estado final, não apenas o comando recebido.

# 11. State Machine

## Deliverer

| Estado | Significado |
|---|---|
| OFFLINE | Não disponível para novas tarefas. |
| AVAILABLE | Pronto para receber entregas. |
| BUSY | Com carga operacional ativa. |

Transições principais:

- OFFLINE → AVAILABLE
- AVAILABLE → BUSY
- BUSY → AVAILABLE

## Delivery

| Estado | Significado |
|---|---|
| WAITING | Pedido aguardando atribuição. |
| ASSIGNED | Pedido atribuído a um entregador. |
| PICKED_UP | Pedido coletado para transporte. |
| DELIVERED | Pedido finalizado. |
| CANCELLED | Pedido cancelado. |

Transições principais:

- WAITING → ASSIGNED
- ASSIGNED → PICKED_UP
- PICKED_UP → DELIVERED
- qualquer etapa operacional relevante → CANCELLED, quando aplicável

# 12. Decisões Arquiteturais

## FastAPI

- Rápido para expor contratos HTTP.
- Bom encaixe com Pydantic e validação explícita.
- Baixa fricção para uma feature orientada a API.

## SQLAlchemy

- Dá controle claro sobre persistência relacional.
- Suporta evolução de schema com migrações.
- Mantém o domínio desacoplado do banco.

## PostgreSQL

- Banco relacional consistente para estados e transições.
- Adequado para o histórico da entrega.
- Bom equilíbrio entre simplicidade e robustez.

## React

- Boa composição visual para o painel do entregador.
- Adequado para decompor páginas e componentes por responsabilidade.

## Vite

- Build rápido.
- Excelente experiência no desenvolvimento local.
- Integração direta com React e TypeScript.

## BDD

- Transforma a regra de negócio em contrato legível.
- Ajuda a validar o comportamento esperado do MVP.

## Monólito

- O fluxo ainda é pequeno o suficiente para não justificar microsserviços.
- Reduz custos de operação e observabilidade.
- Mantém a implementação mais fácil de testar e explicar.

# 13. Refatorações Relevantes

## Antes

- Backend com resquícios de Django.
- Frontend com lógica concentrada em um arquivo único.
- APIs, hooks e UI misturados.
- Pouca separação entre comportamento e apresentação.

## Depois

- Backend com SQLAlchemy e camada de domínio explícita.
- Frontend isolado em feature driven architecture.
- APIs, services, hooks, components, pages e routes separados.
- Wrappers legados mantidos apenas por compatibilidade.

## Benefícios

- Melhor testabilidade.
- Menor acoplamento.
- Fluxo de apresentação mais limpo.
- Base preparada para novas features sem recomeçar a arquitetura.

# 14. Métricas da Entrega

- Endpoints backend: 9
- Entidades de domínio: 2
- Serviços de negócio: 3 responsabilidades conceituais no módulo do Deliverer
- Testes backend: 4 arquivos
- BDD: 1 feature principal com cenário outline e exemplos
- Componentes frontend: 12 no total, sendo 6 do módulo e 6 compartilhados
- Hooks frontend: 4

# 15. Próximos Passos

- Customer
- Restaurant
- Admin
- Observability
- Autenticação real

# 16. Perguntas Frequentes

## Por que não usar microsserviços?

Porque o problema atual é pequeno e linear. Um monólito modular entrega mais rápido e com menos custo operacional.

## Por que não usar WebSocket?

Porque o fluxo foi resolvido com polling simples e a necessidade atual não exige comunicação em tempo real complexa.

## Por que SQLAlchemy?

Porque ele oferece controle explícito sobre persistência, migração e consulta sem prender o domínio ao banco.

## Por que Feature Driven Architecture?

Porque a feature Deliverer precisava de isolamento real. A separação por feature reduz acoplamento e facilita evolução.

## Por que manter BDD?

Porque os cenários funcionam como documentação executável do comportamento do MVP.
