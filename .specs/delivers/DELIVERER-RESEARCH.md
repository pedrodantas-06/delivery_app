# Deliverer Research Report

Last updated: 2026-06-09

## Executive Summary

The Deliverer feature already exists as a usable vertical slice, but the current surface is split across a modern FastAPI/React implementation and older compatibility paths. The new deliverer vision should keep the existing delivery domain, strengthen the mobile-first UI, and normalize contracts so the frontend can depend on stable `/api/v1` endpoints, explicit delivery state transitions, and read-only data from the other business domains.

The practical conclusion is simple: the new experience can be built incrementally on top of the current module structure, but the current integration seams are not clean enough for a polished iFood-style driver experience without a redesign of the frontend shell and a contract cleanup on the backend.

## Current State

### Frontend

- The deliverer experience lives in `frontend/src/features/deliverer` and is already split into pages, hooks, services, API clients, and shared components.
- The root app is only a thin wrapper: `frontend/App.tsx` forwards to `frontend/src/app/App.tsx`, which renders the deliverer route shell.
- The current shell is tab-based, not router-based. `DelivererRoutes` keeps state for `dashboard`, `active`, `history`, and `profile` inside one component.
- The login flow is lightweight and stores a local session in `localStorage`; there is no real JWT/auth integration in the UI yet.
- Polling is already used to refresh deliveries and deliverers every 15 seconds.

### Backend

- Deliverer is implemented under `backend/modulos/delivery` with domain entities, application services, in-memory repositories, SQLAlchemy repositories, HTTP routes, and tests.
- The delivery domain already supports registration, status updates, assignment, accept, pickup, deliver, and reassign flows.
- SQLAlchemy models exist for deliverers, deliveries, and delivery assignments.
- The app mount is inconsistent: `backend/main.py` exposes the delivery router under `/api`, while the frontend and tests expect `/api/v1` style contracts.
- There is still legacy baggage in the repository, especially Django-style views and older payment code paths.

### BDD

- The repository contains Gherkin coverage for deliverer behavior in `tests/deliverer.feature`, `bdd/backend/features/deliverers/deliverers.feature`, and `bdd/frontend/features/deliveres/deliverers.feature`.
- The existing BDD set covers registration, update status, list by status, distribution/broadcast, accept race, refusal, and reassignment after failure/cancel.
- The BDD coverage is good on operational transitions but weak on login, dashboard composition, profile, metrics, and error/loading states.

## Benchmark

### iFood Entregador

- Strong “what do I do next” hierarchy.
- Bottom navigation / tab orientation with very low cognitive load.
- High use of cards, status chips, clear next action, and dense but readable operational summaries.

### Uber Eats Driver

- Map and trip context are more prominent.
- Availability and trip state are usually visible in a persistent shell.
- Actions are large, obvious, and timed for one-hand use.

### DoorDash Dasher

- Very task-oriented, with strong focus on offer/assignment clarity.
- Uses a single primary CTA pattern aggressively.
- Gives a sense of urgency through timers and state labels.

### Rappi Entregador

- Tends to present more operational density and service breadth.
- More likely to combine multi-service context with strong card-based grouping.
- Good inspiration for flexible status surfaces and quick switches.

### What to Reproduce

- iFood-style clarity in the dashboard shell.
- DoorDash-style clarity in primary CTA hierarchy.
- Uber-style persistent operational context.
- Rappi-style quick access to status and context blocks.

### What to Simplify

- Do not copy map-heavy workflows if the backend cannot support them.
- Do not add multi-step flows that increase taps for common actions.
- Do not introduce realtime infrastructure just to imitate the biggest players.

## Problems

| Area | Problem | Impact |
|---|---|---|
| API mount | Frontend expects `/api/v1`, backend deliverer router is mounted differently | Integration gap and brittle assumptions |
| Navigation | Current deliverer shell uses internal tabs instead of a route-aware mobile shell | Harder to deep link and harder to evolve |
| Auth | Session is stored locally without real JWT lifecycle handling | Weak security model and poor production readiness |
| Status model | UI maps several operational states into a small generic badge set | Oversimplifies business meaning |
| Realtime | UX relies on polling, but the UI does not make refresh freshness explicit | Users may not trust state recency |
| Domain coupling | Order, restaurant, customer, and payment data are not yet exposed through one clear read-only layer for deliverer | Limits contextual delivery cards |
| Visual system | Existing styles are functional but generic, not liquid or premium | Brand and product differentiation are weak |

## Opportunities

- Reuse the current feature-driven frontend split and replace the shell, not the whole module.
- Keep `shared` primitives, but add deliverer-specific screen composition and status surfaces.
- Reuse the backend service and repository split, but normalize the route contract and align the delivery state machine with the future spec.
- Pull richer order, restaurant, and customer context into delivery cards instead of showing only order IDs and regions.
- Use the existing polling approach as a transitional mechanism for the broadcast/assignment experience.

## Available Integrations

### Deliverer Domain

- `GET /api/v1/deliverers`
- `POST /api/v1/deliverers`
- `PATCH /api/v1/deliverers/{id}/status`
- `POST /api/v1/orders/assign`
- `GET /api/v1/orders`
- `POST /api/v1/orders/{order_id}/reassign`
- `POST /api/v1/orders/{order_id}/accept`
- `PATCH /api/v1/orders/{order_id}/pickup`
- `PATCH /api/v1/orders/{order_id}/deliver`

### Customer Domain

- Customer auth and CRUD exist in `backend/modulos/cliente/rotas.py`.
- Available data includes name, email, cpf, telefone, and token info for the authenticated user.

### Restaurant Domain

- Restaurant registration, listing, update, and operational status exist in `backend/modulos/restaurante/rotas.py`.
- Available data includes name, address, CNPJ, operating hours, type, and status.

### Menu Domain

- Menu CRUD and restaurant menu listing exist in `backend/modulos/cardapio/rotas.py`.
- Available data includes item name, description, price, category, restaurant ID, and availability.

### Payment Domain

- Payment methods and refund flows exist in `backend/modulos/pagamento/rotas.py`.
- The current payment surface is not yet a clean read-only order payment status contract for the deliverer view.

### Missing but Needed

- A clear read-only order details contract with restaurant, customer, delivery address, notes, and payment state.
- A clean `/api/v1/deliveries` read model for the frontend, even if the current backend keeps using `/orders` internally.
- A stable auth contract for deliveryman login and role validation.

## Technical Debt

- Mixed route conventions between `/api`, `/api/v1`, and legacy route shapes.
- Legacy Django-oriented artifacts remain in the codebase and should not be extended for the deliverer redesign.
- The current UI has too little visual hierarchy for mobile delivery work.
- Some route names still expose order-centric behavior even when the product concept is delivery-centric.
- The frontend currently pulls a list of deliveries and deliverers, but not enough contextual order data to make a strong operational dashboard.

## Recommended Improvements

1. Normalize deliverer-facing APIs under a stable `/api/v1` contract.
2. Introduce a richer read model for delivery cards with customer, restaurant, address, payment, and notes.
3. Replace the tab shell with a mobile-first shell that supports dashboard, active delivery, history, and profile as distinct surfaces.
4. Keep polling for now, but expose freshness cues and loading states so the user trusts the screen.
5. Rebuild the visual language around liquid glass surfaces, soft elevation, and a stronger primary action hierarchy.
6. Preserve the current modular code organization so implementation can proceed in small steps without a rewrite.

## Current Conclusion

The feature is already far enough along to support a redesign rather than a rewrite. The frontend should be re-authored around better mobile workflows and richer delivery context, while the backend should be treated as the source of truth for transitions and contracts after a small normalization pass.
