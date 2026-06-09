# Deliverer Redesign Spec

Last updated: 2026-06-09

## Product Vision

Create a deliverer experience that feels fast, confident, and operationally clear on a phone in one hand. The product should let a courier understand availability, see what is waiting, open the active delivery, and finish pickup and delivery with very few taps.

This is not a dispatch control tower. It is an execution cockpit for one person on the move.

## UX Vision

- One screen should answer three questions immediately: what is waiting, what is active, and what should I do next.
- The shell should prioritize the current operational state, not a long navigation menu.
- All primary actions must be reachable by thumb without demanding precise taps.
- The system should show freshness, not just data. If content is coming from polling, the user must feel that it is alive.

## Design Principles

### Mobile First

- Target 390x844 as the primary design frame.
- Design for thumb reach, short scan paths, and large touch targets.
- Keep critical actions in the lower half of the screen whenever possible.

### One Hand Usage

- Use a single dominant action per screen.
- Secondary actions should collapse into overflow or contextual rows.
- Avoid horizontal complexity that requires precision gestures.

### Low Cognitive Load

- Show only the operational facts needed to act.
- Prefer status chips, short labels, and a small number of consistent card types.
- Avoid forcing the user to infer state from subtle color changes alone.

### Fast Feedback

- Every action needs immediate visual confirmation.
- Loading, success, and error states must be visible and distinct.
- Prevent double submissions with disabled controls and optimistic UI where safe.

### Liquid Design

- Use translucent cards, soft borders, blur layers, and gentle depth.
- Prefer soft gradients and atmospheric backgrounds over flat panels.
- Use motion as state change language, not decoration.

## User Flows

### 1. Login

1. Deliverer opens the app.
2. The login surface asks for identity and region context with minimal friction.
3. On success, the app lands on the operational dashboard.

### 2. Dashboard Review

1. The deliverer sees current status, available deliveries, and active work.
2. The app highlights one next action.
3. The user can toggle availability or open an available delivery card.

### 3. Accept / Assign

1. The deliverer opens an available delivery.
2. The app shows customer, restaurant, region, notes, and payment readiness.
3. The deliverer accepts or assigns to self when eligible.

### 4. Pickup

1. The active delivery card shows the next step clearly.
2. The deliverer confirms pickup once the order is collected.
3. The UI moves the delivery into the next state and surfaces the next action.

### 5. Deliver

1. The app presents the final confirmation step.
2. The deliverer confirms successful delivery.
3. The app returns to the dashboard or history with a visible completion state.

### 6. History

1. The user opens history from the shell.
2. The app shows recent completed deliveries with compact summaries.
3. The user can scan by day and see completion metadata.

### 7. Profile

1. The user opens profile.
2. The app shows identity, region, status, and logout.
3. The user can quickly return the region to the profile default.

## Navigation

### Recommended Shell

- Keep the feature as a dedicated deliverer area with four top-level views: Dashboard, Active, History, Profile.
- Use a floating bottom navigation or segmented floating dock rather than a desktop-style tab strip.
- The active delivery should remain one tap away from every other screen.

### Navigation Rules

- The current operational state should be visible at all times.
- The active delivery should not require repeated drill-downs.
- The dashboard should default to the current region and availability context.

## Screen Architecture

### Login Screen

- Purpose: authenticate or initialize the deliverer session.
- Key elements: identity form, region context, submit action, error area.
- Behavior: the screen should be sparse, fast, and focused on first access.

### Dashboard Screen

- Purpose: show availability, nearby work, and current operational summary.
- Key elements: status summary, available deliveries, nearby deliverers, quick status actions, refresh state.
- Behavior: this is the default landing screen after login.

### Active Delivery Screen

- Purpose: focus on the currently assigned or in-progress delivery.
- Key elements: order summary, restaurant, customer, address, step indicator, accept/pickup/deliver actions.
- Behavior: only the next valid action should appear as primary.

### History Screen

- Purpose: show completed and recent delivery history.
- Key elements: grouped list, completion timestamps, compact metadata, filters by period if needed later.
- Behavior: read-only and scan-friendly.

### Profile Screen

- Purpose: show identity and availability configuration.
- Key elements: name, phone, region, current status, logout, region reset.
- Behavior: should be stable and simple.

## Components

### Reuse

- Reuse base `Button`, `Card`, `Badge`, `Input`, `EmptyState`, and `Loading` primitives.
- Reuse the current fetch separation between API, services, and hooks.

### Replace or Reshape

- Replace the current generic `ActionButtons` as the main interaction pattern.
- Replace the current desktop-like header with a mobile shell header and compact status bar.
- Replace order-ID-only cards with richer delivery cards that carry context.

### Create

- Delivery summary card with contextual sections.
- Availability control block with explicit status states.
- Freshness indicator for polling-based updates.
- Metrics strip for today, week, and month.
- Floating primary action region for the active delivery.

## States

### Availability States

- ONLINE / AVAILABLE
- BUSY
- OFFLINE

### Delivery States

- WAITING
- ASSIGNED
- IN_DELIVERY
- PICKED_UP
- DELIVERED
- CANCELLED

### UI States

- Initial loading
- Polling refresh
- Empty list
- Error banner
- Disabled action
- Success confirmation

## Loading States

- Login loading should disable the form and keep the layout stable.
- Dashboard loading should preserve shell structure and show skeletons or lightweight placeholders.
- Action loading should be local to the affected card or button group.
- Refresh loading should be subtle and not block navigation.

## Error States

- Login errors should appear near the submit action.
- Delivery action failures should appear inside the card that triggered them.
- Global refresh failures should surface as a top banner with a retry action.
- Errors must explain whether the problem is validation, auth, unavailable data, or transient backend failure.

## Empty States

- No available deliveries: explain that the region has no active work right now.
- No active delivery: reassure the deliverer that nothing is assigned yet.
- No history: show a compact empty state with guidance rather than dead space.

## Accessibility

- Minimum touch target of 44x44.
- Strong contrast for text and chips.
- Clear focus rings for keyboard support.
- Status text must never rely on color alone.
- Motion must respect reduced-motion preferences.

## Motion Design

- Use short transitions for card elevation, status changes, and navigation changes.
- Animate only meaningful state transitions: login success, acceptance, pickup, deliver, and refresh.
- Keep motion durations in the 120-240ms range for UI transitions.
- Use gentle stagger only when revealing a delivery stack.

## Responsive Rules

- Mobile first at 390x844.
- At larger widths, keep the same information hierarchy and only expand density.
- Do not switch to a desktop dashboard layout that hides the mobile operational model.
- Use fluid spacing and clamp-based typography where helpful.

## API Dependencies

### Deliverer APIs

- `GET /api/v1/deliverers?status=&region=`
- `POST /api/v1/deliverers`
- `PATCH /api/v1/deliverers/{id}/status`
- `POST /api/v1/orders/assign`
- `GET /api/v1/orders?region=`
- `POST /api/v1/orders/{order_id}/reassign`
- `POST /api/v1/orders/{order_id}/accept`
- `PATCH /api/v1/orders/{order_id}/pickup`
- `PATCH /api/v1/orders/{order_id}/deliver`

### Read-Only Context APIs Needed for Rich UI

- Orders: `GET /api/v1/orders/{order_id}`
- Restaurants: `GET /api/v1/restaurants/{restaurant_id}`
- Customers: `GET /api/v1/customers/{customer_id}`
- Payments: `GET /api/v1/payments?order_id={order_id}`

### Auth

- JWT or token introspection with a `sub` and `role` claim.
- Deliveryman actions must be restricted to the logged-in deliverer.

## Contracts Consumed

The redesign should consume these fields whenever available:

- Deliverer: id, name, phone, region, status.
- Delivery: order id, region, status, deliverer id, assigned timestamp, picked up timestamp, delivered timestamp.
- Order context: restaurant, customer, address, notes, status, payment state.
- Restaurant context: name, region, address, phone, status.
- Customer context: name, phone, address, region.

## Integrations Necessary

1. Align deliverer frontend calls to the stable backend contract.
2. Add a read model for delivery cards so the dashboard is context-rich.
3. Confirm the auth strategy for login and role enforcement.
4. Preserve polling as a transitional mechanism while designing the next refresh strategy.
5. Expose metrics data for today, week, and month either from the backend or a lightweight derived layer.

## Out of Scope

- Map navigation.
- Route optimization.
- Push notifications.
- Earnings payout flows.
- Social or community features.

## Final UX Rule

If a screen does not help the deliverer understand the next operational step in under two seconds, the screen is too busy.
