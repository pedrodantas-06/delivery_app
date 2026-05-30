# Deliverer — Test Plan

Test types and scope:

- Unit Tests
  - Services: DelivererService methods (register, update_status, assign, accept, pickup, deliver, reassign).
  - Repositories: in-memory repository behaviors and failure modes.
  - Mocks: contracts for Orders/Restaurants/Customers.

- Integration Tests
  - TestClient (FastAPI) coverage for all endpoints.
  - DB-backed tests for assignment atomicity (use test DB or SQLite in-memory configured appropriately).

- BDD / E2E
  - Gherkin scenarios in `deliverer-bdd.feature` automatizados via framework (behave/pytest-bdd/cypress as appropriate).

- Concurrency Tests
  - Simular múltiplos accept simultâneos e validar apenas um vencedor.

Test data guidelines:
- Use seeds: 3 deliverers por região, 2 restaurants, orders stubbed with minimal payload.

Coverage targets:
- Unit: 90% no serviço core.
- Integration: 80% das APIs.

CI:
- Adicionar job que executa testes fast (unit) e um job separado para integração/BDD que roda em runner com DB.
