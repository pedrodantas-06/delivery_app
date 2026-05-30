# Delivery Universitario MVP - Rules

## 1. Executive Summary

This project is a university delivery MVP. The goal is to let a client choose a restaurant, select items, create an order, pay, and receive the delivery with the simplest possible stack and the smallest possible code surface.

Core decision:

- One backend monolith
- One PostgreSQL database
- One frontend SPA
- REST only
- BDD and automated tests for every feature

Decision rule:

If removing a piece of code does not prevent the user from ordering food, that piece is probably not MVP.

What this project is not:

- Not a microservices platform
- Not a distributed system
- Not a queue-driven architecture
- Not an enterprise abstraction exercise

## 2. Recommended Architecture

### Product shape

- Backend: FastAPI monolith
- Frontend: React + Vite SPA
- Database: single PostgreSQL instance
- Integration: REST APIs only
- Testing: Pytest, React Testing Library, BDD with Gherkin, Playwright optional
- Infrastructure: Docker Compose only

### Architectural principles

- Simples > Complexo
- Funcional > Perfeito
- Monolith First
- Testabilidade obrigatoria
- Prefer one clear path over multiple optional paths
- Build only what is needed to complete the ordering flow

### Recommended backend structure

```text
backend/
  auth/
    domain/
    application/
    infrastructure/
    http/
  users/
    domain/
    application/
    infrastructure/
    http/
  restaurants/
    domain/
    application/
    infrastructure/
    http/
  menu/
    domain/
    application/
    infrastructure/
    http/
  orders/
    domain/
    application/
    infrastructure/
    http/
  deliveries/
    domain/
    application/
    infrastructure/
    http/
  payments/
    domain/
    application/
    infrastructure/
    http/
  core/
    config.py
    database.py
    security.py
    logging.py
    deps.py
  main.py
```

### Recommended frontend structure

```text
frontend/
  src/
    pages/
    components/
    services/
    hooks/
    types/
    styles/
    assets/
    App.tsx
    main.tsx
```

### Minimum responsibility split

- `domain`: business rules, entities, value objects, status enums
- `application`: use cases and orchestration
- `infrastructure`: SQLAlchemy models, repositories, external adapters
- `http`: FastAPI routers, request and response schemas

Rules for splitting code:

- Keep each module small and focused on one business area
- Do not create extra layers without a real need
- Do not create abstract base classes before there are at least two real implementations
- Prefer plain functions and services over heavy frameworks inside the domain

## 3. Initial Data Model

### Real MVP entities

Only these entities are required to make the user order food:

- `User`
- `Restaurant`
- `MenuItem`
- `Order`
- `OrderItem`
- `Payment`
- `Delivery`

Optional support fields:

- `Campus`
- `Block`
- `Room`
- `Phone`
- `Status`
- `CreatedAt`
- `UpdatedAt`

### What is not a first-class entity in the MVP

- Cart persisted in the database
- Review system
- Chat system
- Loyalty points
- Favorites
- Promotions engine
- Route optimization engine

### Suggested minimum fields

#### User

- id
- name
- email
- password_hash
- role: CLIENT, RESTAURANT, DELIVERYMAN, ADMIN
- is_active
- created_at

#### Restaurant

- id
- owner_user_id
- name
- description
- phone
- campus
- status: OPEN, CLOSED
- created_at
- updated_at

#### MenuItem

- id
- restaurant_id
- name
- description
- price
- is_available
- created_at
- updated_at

#### Order

- id
- client_user_id
- restaurant_id
- deliveryman_user_id nullable
- status: CREATED, PAID, PREPARING, READY, IN_DELIVERY, DELIVERED, CANCELED
- campus
- block
- room
- subtotal
- delivery_fee
- total
- created_at
- updated_at

#### OrderItem

- id
- order_id
- menu_item_id
- item_name_snapshot
- unit_price_snapshot
- quantity
- line_total

#### Payment

- id
- order_id
- provider
- status: PENDING, APPROVED, DECLINED, CANCELED
- amount
- transaction_code
- paid_at nullable
- created_at

#### Delivery

- id
- order_id
- deliveryman_user_id
- status: ASSIGNED, PICKED_UP, DELIVERED, FAILED
- assigned_at
- picked_up_at nullable
- delivered_at nullable

### Data rules

- Use a single PostgreSQL schema unless a real need appears later
- Use migrations for every change
- Use snapshots in `OrderItem` so historical orders do not change when menu prices change
- Keep soft delete out of the MVP unless there is a concrete business reason
- Prefer status columns over separate audit tables for the MVP

## 4. REST API Map

### API conventions

- Base path: `/api/v1`
- Use REST nouns, not action names when possible
- Use plural resource names
- Return JSON only
- Use standard HTTP status codes
- Keep request and response payloads small and explicit

### Auth

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`

### Users

- `GET /api/v1/users/me`
- `PATCH /api/v1/users/me`
- `GET /api/v1/users` only for admin

### Restaurants

- `GET /api/v1/restaurants`
- `POST /api/v1/restaurants` only for restaurant or admin
- `GET /api/v1/restaurants/{id}`
- `PATCH /api/v1/restaurants/{id}`
- `PATCH /api/v1/restaurants/{id}/status`

### Menu

- `GET /api/v1/restaurants/{restaurant_id}/menu-items`
- `POST /api/v1/restaurants/{restaurant_id}/menu-items`
- `GET /api/v1/menu-items/{id}`
- `PATCH /api/v1/menu-items/{id}`
- `PATCH /api/v1/menu-items/{id}/availability`

### Orders

- `POST /api/v1/orders`
- `GET /api/v1/orders/{id}`
- `GET /api/v1/orders?mine=true`
- `PATCH /api/v1/orders/{id}/status`
- `POST /api/v1/orders/{id}/cancel`

### Payments

- `POST /api/v1/orders/{order_id}/payments`
- `GET /api/v1/orders/{order_id}/payment`
- `POST /api/v1/payments/{id}/confirm`
- `POST /api/v1/payments/{id}/cancel`

### Deliveries

- `POST /api/v1/deliveries/assign`
- `GET /api/v1/deliveries/{id}`
- `PATCH /api/v1/deliveries/{id}/pickup`
- `PATCH /api/v1/deliveries/{id}/deliver`

### Error format

Use a consistent JSON error response:

```json
{
  "error": {
    "code": "order_not_found",
    "message": "Order not found",
    "details": {}
  }
}
```

Rules for errors:

- 400 for invalid input
- 401 for unauthenticated requests
- 403 for forbidden access
- 404 for missing resources
- 409 for business conflicts
- 422 for validation failures when the framework already provides it clearly
- 500 for unexpected failures

### API simplicity rules

- Prefer one endpoint per business action
- Do not create generic RPC style endpoints
- Do not add GraphQL
- Do not expose internal repository details in responses
- Keep payloads stable and versioned

## 5. Test Strategy

### Mandatory test layers

- Unit tests for business rules and services
- Integration tests for HTTP endpoints and database interaction
- BDD scenarios for every feature delivered to the user

### Rule for every feature

Every feature must have:

- At least one Gherkin scenario
- At least one automated test
- A passing integration check for the touched slice

### What to test where

#### Unit tests

- Status transitions
- Price calculations
- Permission checks
- Validation rules
- Order total calculation

#### Integration tests

- Endpoint contracts
- Authentication flow
- Database persistence
- Repository behavior

#### BDD tests

- Client chooses restaurant and creates order
- Restaurant updates order status
- Payment is approved
- Delivery is assigned and completed

### Testing rules

- No PR is accepted without tests
- No feature is considered done if only manual verification exists
- Keep tests close to the business flow, not to implementation details
- Prefer deterministic test data
- Use factories or helpers only when they reduce repetition

### Frontend tests

- Use React Testing Library for UI behavior
- Mock HTTP services at the boundary
- Test user-visible behavior, not internal state

### BDD convention

- Feature files live with the domain they describe
- Steps should read like business language
- Do not duplicate the whole HTTP contract in every scenario

## 6. Frontend Rules

### Frontend stack

- React
- Vite
- TypeScript
- React Testing Library

### Frontend structure rules

- `pages` own screen composition
- `components` are reusable UI pieces
- `services` isolate HTTP calls
- `hooks` contain reusable client-side state logic when needed
- Keep business rules out of components whenever possible

### UI rules

- Build for clarity first
- Keep forms short
- Keep actions obvious
- Show loading, error, and empty states
- Avoid overengineering design systems for the MVP

### Frontend data rules

- The frontend may keep cart state locally before checkout
- Do not persist cart in the backend unless it is necessary for the flow
- Do not duplicate backend business rules in the UI
- Use typed service functions for every API call

### Frontend anti-complexity rules

- Do not add global state libraries unless the app really needs them
- Do not add a component abstraction for every element
- Do not split a screen into many tiny files for no reason
- Do not add client-side architecture patterns that only help at large scale

## 7. Security Rules

### Minimum required security

- JWT authentication
- Password hashing with a strong one-way algorithm
- Input validation on every request
- Access control by role

### Roles

- `CLIENT`
- `RESTAURANT`
- `DELIVERYMAN`
- `ADMIN`

### Security rules

- Every protected endpoint must check authentication
- Every role-restricted endpoint must check authorization explicitly
- Never store plain-text passwords
- Never trust client-side role claims without server verification
- Never expose secrets in frontend code or logs

### Practical MVP rule

- Use the smallest auth model that supports the ordering flow and the three user profiles
- Do not add SSO, OAuth federation, or advanced identity workflows for the MVP

## 8. Observability Rules

### Minimum observability

- Structured logs
- Error logs with context
- Business logs for order creation and payment updates

### Required log events

- User login success and failure
- Order created
- Payment approved or rejected
- Delivery assigned
- Delivery completed
- Unexpected errors with stack trace

### Logging rules

- Use consistent JSON or key-value structured logs
- Include request id when available
- Include user id and order id when relevant
- Do not log secrets, passwords, or payment data

### What not to add

- No distributed tracing platform for the MVP
- No metrics stack unless there is a concrete need
- No log aggregation complexity beyond what Docker Compose can support later

## 9. MVP Scope

### In scope

- User registration and login
- Client browsing restaurants and menu items
- Order creation with items and delivery location
- Payment confirmation for the order
- Restaurant status updates for order preparation
- Deliverer assignment and delivery status
- Basic order history
- Role-based access control
- Tests and BDD for every delivered feature

### Out of scope

- Microservices
- Multiple databases
- Queues and asynchronous brokers
- Redis
- Kafka
- RabbitMQ
- GraphQL
- Event sourcing
- CQRS
- Service mesh
- Real-time GPS tracking
- Live chat
- Push notifications
- Ratings and reviews
- Loyalty points
- Coupons engine
- Recommendation engine
- Route optimization algorithms
- Multi-tenant enterprise abstractions

### Sprint guidance

- Sprint 1: authentication, restaurants, menu, basic order creation
- Sprint 2: order lifecycle, delivery assignment, history
- Sprint 3: payment integration and UI refinement
- Sprint 4: stabilization, tests, bug fixes, polish

## 10. Anti-Patterns

The following are explicitly forbidden for this MVP unless a real requirement appears and is approved:

- Microsservices
- Multiple databases
- Background processing infrastructure without a real use case
- Premature optimization
- Over-abstracted repository and service layers
- Deep inheritance trees
- Excessive interfaces with a single implementation
- Event buses for simple CRUD flows
- Domain events that only add ceremony
- Generated code that hides business rules
- Designing for hypothetical future scale instead of current delivery

### Specific code smells to avoid

- A module that only forwards calls without owning logic
- Duplicate status enums in multiple layers
- Generic `Utils` or `Helpers` folders with no clear owner
- Business rules inside UI components
- SQL scattered across the HTTP layer
- Adapters created before the core use case exists

## 11. Development Heuristics

Use these questions before adding anything:

1. Does this help the user place or complete an order?
2. Can this be implemented with one database and one backend?
3. Can this be tested quickly?
4. Can a student understand it in one reading session?
5. Will this still make sense at the end of Sprint 4?

If the answer to question 1 is no, defer it.

If the answer to questions 2 to 5 is unclear, simplify before building.

## 12. Project Rules for Contributors

- Keep changes small and focused
- Prefer the simplest design that works
- Update tests in the same change as the behavior
- Do not introduce a new library unless there is a clear payoff
- Do not add layers just because they exist in larger systems
- Keep the code readable for students who are learning backend and frontend together

## 13. Final Product Definition

The project is done when a client can:

- Sign in
- See restaurants
- See menu items
- Create an order
- Pay for it
- Track its status
- Receive delivery confirmation

And when the team can prove it with:

- Automated tests
- BDD scenarios
- A simple Docker Compose local environment
- Clear, readable code
