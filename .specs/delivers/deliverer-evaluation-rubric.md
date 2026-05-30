# Deliverer — Evaluation Rubric

Objetivo: critérios objetivos para avaliar entregas em Sprints.

Scoring (0-5) por critério — total máximo 25

- **Core functionality (5)**: endpoints essenciais (register, assign, accept, pickup, deliver) implementados e funcionando.
- **Correctness & Edge cases (5)**: transições de estado válidas/invalidas tratadas, idempotência, race conditions evitadas.
- **Contracts & Decoupling (5)**: não há alterações em domínios externos; contratos respeitados.
- **Tests (5)**: cobertura unit + integração para regras de negócio >= 80% e cenários BDD automatizados.
- **Observability & Resilience (5)**: logs estruturados, métricas básicas e tratamento de falha/timeout.

Definições de pronto (DoD):
- API documentada (contract examples), testes passam, migrations adicionadas apenas para tabelas Deliverer, PR com changelog.
