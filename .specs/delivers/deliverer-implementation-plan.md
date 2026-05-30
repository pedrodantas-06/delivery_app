# Deliverer — Implementation Plan (4 Sprints)

Objetivo: entregar o módulo Deliverer em 4 sprints, maximizando velocidade e manutenção.

Sprint 1 — MVP (core APIs e infra mínima)
- Criar modelos DB: `deliverers`, `deliveries`, `delivery_assignments` (sem FK rígidos para orders).
- Implementar `POST /deliverers`, `PATCH /deliverers/{id}/status`, `GET /deliverers`.
- Implementar lógica de `assign` simples (first-available por região).
- Tests unitários para serviços e repositórios in-memory.

Sprint 2 — Fluxo de entrega e UI mínima
- Endpoints `accept`, `pickup`, `deliver` com checagem de permissão.
- Implementar publish de evento `DeliveryCompleted` (interface simples). 
- Implementar front-end mínimo/SPA para entregadores (toggle disponibilidade, aceitar, coletar, entregar).
- BDD scenarios automated.

Sprint 3 — Robustez e concorrência
- Garantir atomicidade de assignment (DB-level or optimistic locking).
- Implementar reassign e edge-cases (no_available_deliverer handling).
- Testes de concorrência (integration tests que simulam race accept).

Sprint 4 — Hardening e observability
- Logs estruturados e métricas básicas (assignments/sec, failures).
- Revisão de segurança e rate-limits.
- Documentação final e migração para SQLAlchemy/Postgres se necessário.

Notas de priorização: focar em endpoints que tornam o entregador útil no app (assign, accept, pickup, deliver). Postergar features analíticas.
