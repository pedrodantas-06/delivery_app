# Deliverer Redesign Plan

Last updated: 2026-06-09

## Summary

This plan turns the current deliverer prototype into a mobile-first, iFood-inspired operational experience. The first phase focuses on the frontend shell, visual language, and screen hierarchy. Later phases expand the dashboard, active delivery flow, contextual integrations, and polish.

## Technical Context

- Frontend stack: React + Vite + TypeScript.
- Current deliverer implementation already exists under `frontend/src/features/deliverer`.
- Shared primitives exist under `frontend/src/shared/components`.
- The backend deliverer domain already exposes registration, status, assignment, accept, pickup, deliver, and reassign flows.
- Polling is currently used for refresh.
- The design direction is liquid glass, mobile-first, and thumb-friendly.

## Constitution Check

- Monolith first: preserved.
- REST only: preserved.
- Mobile-first: required by the new shell.
- Testability: preserved by keeping the feature modular.
- Simplicity: phase 1 limits behavior changes.
- BDD coverage: later implementation tasks must remain aligned with existing scenarios.

## Applied Guidelines

- Deliverer UI should prioritize one primary action per screen.
- Cards should stay compact and actionable.
- Navigation should be floating and always reachable.
- Loading and error states must be explicit.
- Visual language should use glass surfaces, soft elevation, and gentle motion.

## Implementation Steps

### Phase 1: Foundation and visual shell

#### Step 1.1: [Cross-cutting] Establish the liquid-glass visual tokens and responsive base

- Replace the current generic page styling with a tokenized mobile-first visual foundation.
- Introduce glass surfaces, softer elevation, better spacing, and explicit motion variables.
- Update shared primitives to inherit the new system where needed.

#### Step 1.2: [Cross-cutting] Rework the deliverer shell and navigation model

- Convert the current tab-heavy shell into a clearer mobile operational shell.
- Add a floating navigation pattern and a stronger status header.
- Keep the same logical views: Dashboard, Active, History, Profile.

#### Step 1.3: [Cross-cutting] Recompose login and dashboard surfaces

- Refresh the login entry point to feel like a product screen, not a plain form.
- Improve the dashboard hierarchy so availability and available deliveries are obvious.
- Add stronger loading and empty states.

### Phase 2: Operational dashboard

#### Step 2.1: [Cross-cutting] Add richer delivery summaries and status affordances

- Expand delivery cards to show more context and clearer status semantics.
- Make the action hierarchy more explicit.
- Prepare room for metrics and freshness indicators.

#### Step 2.2: [Cross-cutting] Surface metrics and freshness indicators

- Add today/week/month summary blocks.
- Show polling freshness and refresh feedback.

### Phase 3: Active delivery flow

#### Step 3.1: [Cross-cutting] Tighten the active delivery state machine UI

- Make accept, pickup, and deliver state transitions visually obvious.
- Keep only the next valid action primary.

#### Step 3.2: [Cross-cutting] Add localized success and error feedback

- Show action-level success and error feedback in the active delivery surface.
- Prevent double-submits through disabled and pending states.

### Phase 4: Full integrations

#### Step 4.1: [Cross-cutting] Add contextual order, restaurant, customer, and payment data

- Consume read-only context where available.
- Enrich the delivery card with job-ticket details.

#### Step 4.2: [Cross-cutting] Normalize API usage and auth assumptions

- Align frontend calls to stable `/api/v1` contracts.
- Prepare for a real token-based session model.

### Phase 5: Polish and hardening

#### Step 5.1: [Cross-cutting] Polish motion, accessibility, and empty states

- Refine spacing, transitions, and focus states.
- Ensure touch targets and contrast meet mobile accessibility needs.

#### Step 5.2: [Cross-cutting] Validate the redesign against the deliverer scenarios

- Ensure the final UI still supports registration, status, list, assign, accept, pickup, deliver, reassign, and history.

## Project Structure

- `frontend/src/features/deliverer/routes/DelivererRoutes.tsx`
- `frontend/src/features/deliverer/pages/*.tsx`
- `frontend/src/features/deliverer/components/*.tsx`
- `frontend/src/features/deliverer/hooks/*.ts`
- `frontend/src/features/deliverer/api/*.ts`
- `frontend/src/features/deliverer/services/*.ts`
- `frontend/src/features/deliverer/types/index.ts`
- `frontend/styles.css`
- `frontend/src/shared/components/*.tsx`

## Requirement Mapping

| REQ ID | Description | Plan Items | Implementation Evidence |
|--------|-------------|------------|------------------------|
| REQ-001 | Registrar entregador | 1.3, 4.2 | LoginPage.tsx, useDeliverer.ts, delivererApi.ts |
| REQ-002 | Atualizar disponibilidade do entregador | 1.2, 1.3, 2.1, 4.2 | DashboardPage.tsx, ProfilePage.tsx, useDeliverer.ts |
| REQ-003 | Listar entregadores por região/status | 1.2, 2.1, 2.2 | DashboardPage.tsx, useDeliveries.ts, delivererApi.ts |
| REQ-004 | Atribuição automática de delivery por região | 2.1, 4.1 | deliveryApi.ts, useDeliveries.ts, DeliveryCard.tsx |
| REQ-005 | Reatribuir entrega | 3.1, 4.1 | ActionButtons.tsx, deliveryApi.ts, DashboardPage.tsx |
| REQ-006 | Aceitar entrega / accept endpoint | 1.2, 3.1, 3.2 | ActiveDeliveryPage.tsx, ActionButtons.tsx, deliveryApi.ts |
| REQ-007 | Coletar pedido / pickup | 3.1, 3.2 | ActiveDeliveryPage.tsx, ActionButtons.tsx, deliveryApi.ts |
| REQ-008 | Confirmar entrega / deliver | 3.1, 3.2 | ActiveDeliveryPage.tsx, ActionButtons.tsx, deliveryApi.ts |
| REQ-009 | Histórico de entregas do entregador | 1.2, 1.3, 5.1, 5.2 | HistoryPage.tsx, HistoryList.tsx, useDeliveryHistory.ts |
| REQ-010 | Consultas read-only sobre outros domínios | 4.1, 4.2 | delivererApi.ts, deliveryApi.ts, future order/restaurant/customer/payment adapters |

## Phase 1 Task Breakdown

### Foundation

- [ ] T001 [Plan:1.1] Rebuild `frontend/styles.css` with liquid-glass tokens, mobile-first spacing, status chips, and motion variables.
- [ ] T002 [P] [Plan:1.1] Refresh shared primitives in `frontend/src/shared/components/Button.tsx`, `frontend/src/shared/components/Card.tsx`, `frontend/src/shared/components/Badge.tsx`, `frontend/src/shared/components/Input.tsx`, `frontend/src/shared/components/EmptyState.tsx`, and `frontend/src/shared/components/Loading.tsx` to inherit the new design language.

### Shell

- [ ] T003 [P] [Plan:1.2] Recompose `frontend/src/features/deliverer/routes/DelivererRoutes.tsx` and `frontend/src/features/deliverer/components/DelivererHeader.tsx` into a clearer mobile shell with stronger navigation hierarchy.
- [ ] T004 [P] [Plan:1.2] Update `frontend/src/features/deliverer/components/ActionButtons.tsx` and `frontend/src/features/deliverer/components/StatusBadge.tsx` so the primary actions and states match the new shell language.

### Screens

- [ ] T005 [P] [Plan:1.3] Redesign `frontend/src/features/deliverer/pages/LoginPage.tsx` for the liquid-glass entry experience and stronger mobile-first hierarchy.
- [ ] T006 [P] [Plan:1.3] Redesign `frontend/src/features/deliverer/pages/DashboardPage.tsx` to prioritize availability, available work, and one-hand actions.
- [ ] T007 [P] [Plan:1.3] Rework `frontend/src/features/deliverer/pages/ActiveDeliveryPage.tsx`, `HistoryPage.tsx`, and `ProfilePage.tsx` to match the new screen architecture and responsive rules.

### Baseline Validation

- [ ] T008 [Plan:1.3,1.2] Update or extend `frontend/src/features/deliverer/__tests__/*.test.*` to confirm the shell, login, and dashboard still render after the visual refactor.

### Phase 2: Operational dashboard

#### Metrics and freshness

- [ ] T009 [P] [Plan:2.1] Extend `frontend/src/features/deliverer/hooks/useDeliveries.ts` to expose refresh freshness and operational counts for the dashboard.
- [ ] T010 [P] [Plan:2.1] Enrich `frontend/src/features/deliverer/components/DeliveryCard.tsx` with richer status affordances and timeline details.
- [ ] T011 [Plan:2.2] Update `frontend/src/features/deliverer/routes/DelivererRoutes.tsx`, `frontend/src/features/deliverer/pages/DashboardPage.tsx`, and `frontend/src/features/deliverer/pages/HistoryPage.tsx` to surface freshness, summary metrics, and the updated delivery summary experience.
