# delivery_app

## Visão geral
Base de um projeto de delivery com arquitetura hexagonal / clean architecture, backend em Django e testes BDD com `pytest-bdd`.

O objetivo desta base é permitir que o time comece a desenvolver rapidamente com uma estrutura clara, separação de responsabilidades e o primeiro recurso de entregadores.

## Estrutura do projeto
- `service/backend/`: código do backend Django
- `app/frontend/`: frontend Vite + React (lista funcional de entregadores)
- `docker-compose.yml`: orquestra o backend Django e PostgreSQL
- `.env.example`: variáveis de ambiente para desenvolvimento
- `docs/`: source of truth de arquitetura, design system e BDD

## Documentação oficial
- `docs/architecture.md`
- `docs/design-system.md`
- `docs/bdd-guidelines.md`
- `docs/deliverers.md`

## Como rodar localmente
1. Copie as variáveis de ambiente:
   ```bash
   cp .env.example .env
   ```
2. Inicie os serviços:
   ```bash
   docker compose up --build
   ```
3. A API estará disponível em `http://localhost:8000`

### Endpoints de exemplo
- `GET /api/deliverers/?status=AVAILABLE&region=Zona Sul`
- `POST /api/deliverers/`
- `PATCH /api/deliverers/{deliverer_id}/status/`
- `POST /api/orders/assign/` (automática ou manual com `deliverer_id`)
- `POST /api/orders/{order_id}/reassign/` (com `reason`: `timeout` ou `refused`)

### Frontend local
O frontend inicial está em `app/frontend`.
```bash
cd app/frontend
npm install
npm run dev
```

## Como rodar os testes
Entre na pasta do backend e execute:
```bash
cd service/backend
pytest
```

## Como adicionar uma nova feature
1. Crie um novo domínio dentro de `service/backend/delivery/domain/` ou extraia um app para `service/backend/<feature>`.
2. Adicione portos (`ports.py`) e implementação de repositórios em `infrastructure/repositories.py`.
3. Crie regras de aplicação em `application/services.py`.
4. Exponha a API em `http/views.py` e registre as rotas em `http/urls.py`.
5. Adicione cenários BDD em `service/backend/tests/features/` e passos em `service/backend/tests/steps/`.

## Boas práticas de colaboração
- Use branches pequenas e focadas por feature: `feature/deliverers`, `feature/orders`, `fix/tests`
- Escreva commits claros: `feat(delivery): add assign order endpoint`
- Inclua no PR:
  - descrição da mudança
  - exemplos de uso e chamadas de API
  - notas de testes executados

## Observações
Esta base foi montada para ser simples, clara e facilmente extensível pelo time. A arquitetura deve ser replicada em novos domínios conforme o projeto crescer.
