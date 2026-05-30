# Deliverer — Spec Document

Última atualização: 2026-05-30

## Executive Summary

Este documento define a especificação do bounded context `Deliverer` (Entregador) e do ciclo de vida `Delivery` dentro do monólito Delivery Universitário. O objetivo é permitir desenvolvimento, QA e avaliação independentemente dos demais domínios; o `Deliverer` só consome contratos e publica eventos, nunca altera a responsabilidade de `Orders`, `Payments`, `Restaurants` ou `Customers`.

## Scope

### In Scope
- Deliverer (registro, perfil mínimo, disponibilidade)
- Delivery (representação do trabalho ligado a um `Order`)
- Assignment (atribuição automática e manual)
- Pickup (coleta do pedido pelo entregador)
- Delivery Completion (entrega confirmada)
- Deliverer Availability (OFFLINE / AVAILABLE / BUSY)

### Out of Scope
- Criação/alteração de `Order`, processamento de `Payment`, gestão de `Restaurant`, gestão de `Menu`, gestão de `Customer`.
- Roteirização, navegação GPS, pagamentos ao entregador, notificações push (implementar só se houver contrato existente).

## Domain Model

### Entidades e campos (mínimos)

- `Deliverer`
  - `id` (UUID)
  - `user_id` (UUID | nullable)
  - `name` (string)
  - `phone` (string)
  - `region` (string)
  - `status` (DelivererStatus)
  - `created_at`, `updated_at`

- `Delivery`
  - `id` (UUID)
  - `order_id` (UUID) — referência lógica (owner: Orders)
  - `restaurant_id` (UUID)
  - `customer_id` (UUID)
  - `deliverer_id` (UUID | null)
  - `status` (DeliveryStatus)
  - `assigned_at`, `picked_up_at`, `delivered_at`
  - `region` (string)
  - `metadata` (jsonb | opcional)

- `DeliveryAssignment` (audit)
  - `id`, `delivery_id`, `deliverer_id`, `assigned_by`, `reason`, `created_at`

### Enums
- `DelivererStatus`: `OFFLINE`, `AVAILABLE`, `BUSY`
- `DeliveryStatus`: `ASSIGNED`, `PICKED_UP`, `DELIVERED`, `CANCELLED`, `WAITING`

## Functional Requirements (Deliverer-only)

RF-001 — Registrar entregador
- `POST /api/v1/deliverers` cria `Deliverer`. Retorna 201 com payload do recurso.

RF-002 — Atualizar status do entregador
- `PATCH /api/v1/deliverers/{deliverer_id}/status`.

RF-003 — Listar entregadores
- `GET /api/v1/deliverers?status=&region=` paginado.

RF-004 — Assign automático/manual
- `POST /api/v1/deliveries/assign` com `{order_id, region, deliverer_id?}`.

RF-005 — Reatribuir
- `POST /api/v1/deliveries/{delivery_id}/reassign` com `{reason}`.

RF-006 — Accept (opcional, para broadcast simulada)
- `POST /api/v1/deliveries/{delivery_id}/accept` com `{deliverer_id}`.

RF-007 — Pickup
- `PATCH /api/v1/deliveries/{delivery_id}/pickup` grava `picked_up_at`.

RF-008 — Deliver
- `PATCH /api/v1/deliveries/{delivery_id}/deliver` grava `delivered_at` e publica evento `DeliveryCompleted`.

RF-009 — Idempotência e auditoria
- Todas as transições devem ser idempotentes e auditadas.

RF-010 — Consultas read-only
- Somente leitura sobre Orders/Payments/Restaurants via contratos externos.

## State Machines

Deliverer:
- OFFLINE → AVAILABLE → BUSY → AVAILABLE → OFFLINE

Delivery:
- ASSIGNED → PICKED_UP → DELIVERED
- ASSIGNED → CANCELLED
- ASSIGNED → WAITING

Transições válidas são checadas no serviço; transições inválidas retornam 400 com código `invalid_transition`.

## API Contracts (resumo)

Base: `/api/v1`
Auth: `Authorization: Bearer <jwt>` com `role` e `sub`.

Principais endpoints (contratos simplificados):
- `POST /api/v1/deliverers` (create)
- `PATCH /api/v1/deliverers/{id}/status` (update status)
- `GET /api/v1/deliverers` (list)
- `POST /api/v1/deliveries/assign` (assign)
- `POST /api/v1/deliveries/{id}/reassign` (reassign)
- `POST /api/v1/deliveries/{id}/accept` (accept)
- `PATCH /api/v1/deliveries/{id}/pickup`
- `PATCH /api/v1/deliveries/{id}/deliver`

Erros padronizados:
```json
{ "error": { "code": "<code>", "message": "...", "details": {} } }
```

## Security Rules

- JWT obrigatório para todos endpoints de escrita.
- Roles: `DELIVERYMAN`, `ADMIN`.
- `DELIVERYMAN` age apenas sobre entregas atribuídas a si.
- Rate limiting: endpoints `accept`, `pickup`, `deliver`.
- Auditoria: registrar usuário, ação, ip, timestamp.

## Database Impact (Deliverer-only)

Somente tabelas abaixo: `deliverers`, `deliveries`, `delivery_assignments`.
Observação: não adicionar FK restritivos para `orders` para evitar acoplamento; usar índices e conventions.

## Frontend Impact

Telasmínimas: Login, Dashboard, Delivery Card, Perfil, Histórico.
UI: polling para simular broadcast; botões desabilitados durante operações pendentes.

## Acceptance Matrix (exemplo)

| RF | Gherkin | Endpoint | Teste |
|---|---|---|---|
| RF-001 | cadastrar entregador | POST /api/v1/deliverers | 201 + GET |
| RF-004 | atribuir automático | POST /api/v1/deliveries/assign | IN_DELIVERY + deliverer BUSY |

## Non-functional Requirements
- Idempotência, atomicidade de assignment, logs estruturados, cobertura de testes >= 80%.

## Conformance

Deliverer não deve modificar outros domínios; integrações via contratos em `deliverer-dependencies-contracts.md`.
