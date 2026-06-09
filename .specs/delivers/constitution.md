# Delivery App Constitution

Last updated: 2026-06-09

## Principles

- Monolith first.
- REST only for integration boundaries.
- Mobile-first for deliverer and customer-facing UI.
- Simple over complex.
- Functional over perfect.
- Testability is mandatory.
- Every feature must ship with BDD coverage and automated tests.
- Keep the deliverer bounded context isolated from Orders, Payments, Restaurants, Customers, and Menu ownership.

## Frontend Rules

- Design for 390x844 first.
- Keep touch targets large and actions obvious.
- Prefer one primary action per screen.
- Use floating navigation and glass surfaces for the deliverer shell.
- Preserve polling until the backend exposes a stronger live-update strategy.

## Backend Rules

- Use stable `/api/v1` contracts.
- Keep read-only contracts read-only.
- Do not add unnecessary service layers or abstractions.
- Prefer explicit status transitions and idempotent state changes.

## Delivery Rules

- Phase 1 must be behavior-neutral where possible.
- Phase 2 and later can improve data richness and operational context.
- No realtime infrastructure is required for the MVP.
- No route optimization, push, or earnings features in the deliverer redesign.
