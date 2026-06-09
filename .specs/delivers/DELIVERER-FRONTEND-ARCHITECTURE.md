# Deliverer Frontend Architecture

Last updated: 2026-06-09

## Target Architecture

The deliverer frontend should remain a feature-driven module inside the React/Vite app, but the shell and data orchestration should be reorganized so the user journey feels like a dedicated mobile product.

## Current Structure

### Reusable Today

- `frontend/src/features/deliverer/pages`
- `frontend/src/features/deliverer/components`
- `frontend/src/features/deliverer/hooks`
- `frontend/src/features/deliverer/services`
- `frontend/src/features/deliverer/api`
- `frontend/src/shared/components`
- `frontend/src/shared/services/http.ts`

### Current Limitations

- The route shell is still a single stateful component.
- The login view is too close to a plain form and does not feel like a product entry point.
- Delivery cards show too little context for an operational workload.
- There is no explicit screen architecture for metrics or contextual order metadata.

## Recommended Folder Shape

```text
frontend/src/features/deliverer/
  api/
  components/
  constants/
  hooks/
  pages/
  routes/
  services/
  types/
  utils/
```

## What to Reuse

- Keep the current feature split by responsibility.
- Keep the shared primitive set for buttons, cards, inputs, badges, and loading states.
- Keep polling and local session persistence as transitional behavior.
- Keep the idea of a dedicated deliverer shell rather than scattering this experience through the app.

## What to Remove or Deprecate

- Remove desktop-like assumptions from the current header and action layout.
- Remove any dependence on the root `App` for business logic.
- Deprecate the current tab-only shell if a route-aware shell is introduced.
- Deprecate cards that only expose order ID and region without contextual data.

## What to Create

### Shell Layer

- A mobile-first shell with a strong header and floating navigation.
- A compact freshness indicator for polling-based refresh.
- A status summary bar showing current deliverer state and active region.

### Page Layer

- Dashboard page focused on availability, live work, and quick actions.
- Active delivery page focused on the currently assigned task.
- History page focused on completed work and period summaries.
- Profile page focused on identity and availability control.
- Login page with stronger brand and product framing.

### Component Layer

- Delivery summary card with rich context.
- Availability control module.
- Metrics strip for today, week, and month.
- Floating action group for accept, pickup, and deliver steps.
- Freshness badge for polling state.
- Context sections for restaurant, customer, address, payment, and notes.

### Hook Layer

- A dashboard orchestration hook that aggregates session, availability, deliveries, and metrics.
- A delivery lifecycle hook if the active flow needs local state management.
- A data freshness hook if the app should explicitly show refresh age.

### Service Layer

- Session service to persist and clear the deliverer session.
- Delivery service for list and lifecycle transformation logic.
- A metrics adapter if the backend later exposes today/week/month rollups.

### API Layer

- Keep the API client as the thin transport boundary.
- Separate deliverer identity calls from delivery lifecycle calls.
- Add read-only adapters for order, restaurant, customer, and payment context as soon as the backend contract is ready.

### Types Layer

- Keep explicit status unions.
- Extend delivery types to support rich read models and summary cards.
- Add screen-specific view models if needed so components do not own transformation logic.

## Proposed Data Flow

1. The shell loads the session.
2. The dashboard hook fetches deliverers and deliveries for the current region.
3. The UI derives available work, current task, history, and metrics from the same read model.
4. Delivery actions call thin API functions and then trigger a refresh.
5. The shell keeps context visible at every step.

## Screen Responsibilities

### Login

- Initialize the session.
- Set the default region.
- Bring the user into the operational shell.

### Dashboard

- Show availability and nearby work.
- Surface the next likely action.
- Show quick access to current region and current status.

### Active Delivery

- Show only the active delivery and its next step.
- Prevent accidental actions with clear state gating.

### History

- Present completed deliveries as a readable feed.
- Keep it compact and scan-friendly.

### Profile

- Show identity and region.
- Provide logout and region reset.

## Route Strategy

### Option A: Internal Shell State

- Keep the current no-router pattern, but rebuild the shell and page composition.
- Best for incremental implementation and minimal churn.

### Option B: Route-Aware Shell

- Introduce route-based views for dashboard, active, history, and profile.
- Best for deep links and future extensibility.

### Recommendation

- Use Option A if the goal is a low-risk redesign inside the current app.
- Use Option B only if the broader app is ready to adopt route-based navigation patterns.

## Contract Dependencies

### Must Exist

- Stable deliverer CRUD and status endpoints.
- Stable delivery list and lifecycle endpoints.
- A clear auth or session contract.

### Should Exist

- Order detail read model.
- Restaurant summary read model.
- Customer summary read model.
- Payment state read model.

## Migration Notes

- Do not force a rewrite of the entire feature module.
- The shell, cards, and data view models are the highest-value refactor points.
- Keep behavior identical in the initial refactor and improve visuals in later phases.
