# MVP Delivery — Plano de Fechamento Universitário (Demo-Ready)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Entregar um **MVP demonstrável** — após `make up`, qualquer pessoa acessa Cliente, Restaurante, Entregador e Admin **sem cadastro manual**, com fluxo E2E completo em menos de 5 minutos.

**Architecture:** Monólito modular FastAPI + React/Vite. **Autenticação unificada** (`POST /api/v1/auth/login`) com `role` determinando a experiência. React Router com guards por role. Seeds demo completas. Pagamento via `MockPaymentGateway` (sem Stripe/MercadoPago). Reutilizar módulos backend existentes; adicionar `auth`, `pedido`, features `customer`, `restaurant`, `admin`; refatorar `deliverer` para auth unificada.

**Tech Stack:** FastAPI, MySQL, SQLite (delivery), React 19, Vite 7, React Router 7, TypeScript, pytest, Jest, Cypress, Docker Compose.

---

## Princípio Arquitetural (obrigatório para agentes)

> O sistema deve possuir **uma única autenticação** para todos os tipos de usuário. O papel (`role`) determina automaticamente a experiência carregada após o login. **É proibido** criar múltiplas telas de login ou mecanismos artificiais de troca de perfil para demonstração. A seed serve apenas para fornecer contas prontas durante testes E2E e apresentação. Isso aproxima o MVP do comportamento real de plataformas como iFood e Uber Eats, mantendo a implementação simples.

**Proibido:**
- `useState('customer' | 'deliverer')` ou botões "Entrar como Cliente/Restaurante"
- Múltiplas telas de login por role
- Integração real com gateway de pagamento

**Obrigatório:**
- Login único → redirect automático por `user.role`
- Route guards bloqueando cross-access
- Seed completa para demo imediata

---

## 0. Demo Readiness — Objetivo Central

Após `make up`, abrir `http://127.0.0.1:4173` e:

1. Fazer login com conta demo
2. Ser redirecionado automaticamente para a experiência correta
3. Navegar fluxo completo sem criar usuários manualmente

### Contas Demo (seed)

| Role | Email | Senha |
|------|-------|-------|
| CLIENTE | `cliente@yummicious.com` | `123456` |
| RESTAURANTE | `burger@burgerhouse.com` | `123456` |
| ENTREGADOR | `entregador@yummicious.com` | `123456` |
| ADMIN | `admin@yummicious.com` | `123456` |

### Restaurantes Demo (seed)

| Nome | Email operador | Itens |
|------|----------------|-------|
| Burger House | `burger@burgerhouse.com` | X-Burguer, X-Salada, Batata, Coca-Cola, Milkshake |
| Pizza Campus | — | Margherita, Calabresa, 4 Queijos, Guaraná, Brownie |
| Açaí Federal | — | Açaí 300ml, Açaí 500ml, Granola, Banana, Água |

### Pedidos Demo (seed — histórico/tracking antes de criar novos)

| Status | Propósito |
|--------|-----------|
| `Finalizado` | Histórico cliente + demo entregue |
| `Em preparo` | Tracking + painel restaurante |
| `Pago` | Aguardando aceite restaurante |
| `Cancelado` | Estado terminal visível |

---

## 0.1 Git Workflow — Branch e PR

**Branch única de fechamento:**

```bash
git checkout main
git pull origin main
git checkout -b feat/mvp-final-integration
```

**Convenção:** todos os commits seguem [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `test:`, `chore:`).

**Ao final:**

```bash
git push origin feat/mvp-final-integration
gh pr create --title "MVP Final Integration" --body "$(cat <<'EOF'
## Summary
- Finaliza fluxo completo Cliente → Pedido → Pagamento mock → Entrega
- Autenticação unificada com redirect por role
- Seeds demo para apresentação E2E imediata
- Frontend: customer, restaurant, deliverer, admin
- MockPaymentGateway (sem gateway externo)
- Testes E2E verdes

## Test plan
- [ ] `make up` sobe sem erros
- [ ] Login demo cliente → pedido → pagamento → tracking
- [ ] Login demo restaurante → aceitar/rejeitar pedido
- [ ] Login demo entregador → avançar status → entregar
- [ ] Login demo admin → métricas visíveis
- [ ] `make test` verde
- [ ] Fluxo demonstrável em < 5 minutos
EOF
)"
```

---

## 1. Resumo Executivo — Estado Atual

| Dimensão | Status |
|----------|--------|
| Entregadores | ✅ Backend + frontend (integração quebrada) |
| Cardápio | 🟡 Backend CRUD; sem frontend |
| Cliente | 🟡 Backend parcial; schema desalinhado; sem frontend |
| Restaurante | 🟡 Backend CRUD; **sem frontend** |
| Admin | ❌ Inexistente |
| Pagamento | 🟡 Código existe; router off; sem mock gateway |
| Pedido | ❌ Sem módulo/API |
| Auth unificada | ❌ Login só em `/clientes/login` |
| Seed demo | 🟡 Mínima (1 restaurante, 1 pedido) |
| Integração E2E | ❌ |

**Transformação deste plano:** de "MVP funcional" para **"MVP demonstrável"** — critério de banca universitária.

---

## 2. Fase 1 — Descoberta Arquitetural (atualizada)

### 2.1 Backend — Lanes

*(Mantém mapa original — ver seções Entregadores, Cliente, Restaurante, Cardápio, Pagamento, Pedido no commit anterior.)*

**Novos gaps identificados:**

| Gap | Solução mínima |
|-----|----------------|
| Auth fragmentada (`/clientes/login` only) | Novo `modulos/auth/` com `/auth/login` unificado |
| `role` inconsistente (`admin`/`cliente` lowercase) | ENUM `CLIENTE\|RESTAURANTE\|ENTREGADOR\|ADMIN` |
| Restaurante sem credencial | Tabela `usuarios` + FK `restaurantes.usuario_id` |
| Entregador login separado (POST deliverer) | Login via auth; session guarda `deliverer_id` do seed |
| Admin sem endpoints | `GET /api/v1/admin/metrics` read-only |

### 2.2 Frontend — Arquitetura Alvo

```
frontend/src/
├── app/
│   ├── App.tsx                    # AuthProvider + RouterProvider
│   ├── routes/index.tsx           # rotas centralizadas
│   ├── guards/RoleGuard.tsx       # proteção por role
│   └── providers/AuthProvider.tsx # JWT + user context
├── features/
│   ├── auth/                      # LoginPage, RegisterPage (único login)
│   ├── customer/                  # Home, Menu, Cart, Checkout, Tracking, History
│   ├── restaurant/                # Dashboard, Orders, Decision (aceitar/rejeitar)
│   ├── deliverer/                 # Dashboard, Active, History (+ Avançar status)
│   └── admin/                     # AdminDashboard (métricas read-only)
└── shared/
    ├── components/                # AppShell, TopBar, BottomNavigation, MetricCard, ...
    └── services/http.ts
```

**Rotas:**

| Path | Role | Layout |
|------|------|--------|
| `/login` | público | AuthLayout |
| `/customer/*` | CLIENTE | CustomerLayout + BottomNavigation |
| `/restaurant/*` | RESTAURANTE | RestaurantLayout |
| `/deliverer/*` | ENTREGADOR | DelivererLayout |
| `/admin/*` | ADMIN | AdminLayout |

**Redirect pós-login:**

```typescript
function redirectByRole(role: UserRole, navigate: NavigateFunction) {
  switch (role) {
    case 'CLIENTE':    navigate('/customer'); break
    case 'RESTAURANTE': navigate('/restaurant'); break
    case 'ENTREGADOR': navigate('/deliverer'); break
    case 'ADMIN':      navigate('/admin'); break
  }
}
```

**Route guard:**

```tsx
<Route
  path="/restaurant/*"
  element={
    <RoleGuard allowed={['RESTAURANTE', 'ADMIN']}>
      <RestaurantLayout />
    </RoleGuard>
  }
/>
```

- CLIENTE nunca acessa `/deliverer` ou `/restaurant`
- ENTREGADOR nunca acessa `/customer` ou `/restaurant`
- ADMIN acessa todas as rotas (guard permite ADMIN em qualquer área)

---

## 3. Autenticação Unificada — Spec

### Modelo de Usuário

**Arquivo:** `database/esquemas/03_alteracoes_mvp.sql`

```sql
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    role ENUM('CLIENTE', 'RESTAURANTE', 'ENTREGADOR', 'ADMIN') NOT NULL,
    referencia_id VARCHAR(50) NULL COMMENT 'cliente_id, restaurante_id ou deliverer_uuid',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### API

```
POST /api/v1/auth/login
Body: { "email": "cliente@yummicious.com", "senha": "123456" }

Response 200:
{
  "access_token": "eyJ...",
  "user": {
    "id": 1,
    "nome": "João Demo",
    "email": "cliente@yummicious.com",
    "role": "CLIENTE",
    "referencia_id": "cli_demo_001"
  }
}

POST /api/v1/auth/register  (opcional MVP — seed cobre demo)
POST /api/v1/auth/logout    (client-side token clear)
GET  /api/v1/auth/me        (JWT required)
```

**Implementação:** `backend/modulos/auth/rotas.py` reutiliza `core/jwt.py` e `core/seguranca.py`. Login consulta `usuarios`; endpoints legados `/clientes/login` permanecem como alias deprecated (não remover — evitar quebra).

---

## 4. Pagamento — MockPaymentGateway

**Sem Stripe. Sem MercadoPago. Sem webhook.**

```python
# backend/modulos/pagamento/mock_gateway.py
import asyncio

class MockPaymentGateway:
    @staticmethod
    async def processar(valor: float) -> dict:
        await asyncio.sleep(1)  # simula latência
        return {"status": "APROVADO", "transaction_id": f"mock_{int(valor * 100)}"}
```

**Fluxo:**

```
Cliente clica "Pagar"
  → POST /api/v1/pagamento/processar/{pedido_id}
  → MockPaymentGateway.processar (1s delay)
  → pedidos.status = 'Pago'
  → transacao registrada
  → bridge assign delivery
  → Response { status: "Pago" }
```

Frontend exibe `LoadingState` durante o 1 segundo.

---

## 5. Entregador — Botão "Avançar Status" (demo)

Manter state machine existente (WAITING → ASSIGNED → IN_DELIVERY → PICKED_UP → DELIVERED).

Adicionar na `ActiveDeliveryPage` botão único **"Avançar status"** que chama a próxima transição válida:

| Status atual | Próxima ação | Endpoint |
|--------------|--------------|----------|
| ASSIGNED | accept | `POST /orders/{id}/accept/` |
| IN_DELIVERY | pickup | `PATCH /orders/{id}/pickup/` |
| PICKED_UP | deliver | `PATCH /orders/{id}/deliver/` |

Permite demonstrar entrega completa em **< 1 minuto** na banca.

---

## 6. Liquid Design — Tokens Obrigatórios

Adicionar em `frontend/styles.css`:

```css
:root {
  /* Radius */
  --radius-sm: 6px;
  --radius-md: 12px;
  --radius-lg: 20px;

  /* Spacing */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;

  /* Surfaces */
  --surface: #ffffff;
  --surface-secondary: #f5f5f7;

  /* Semantic */
  --primary: #e85d04;
  --success: #2a9d8f;
  --danger: #e63946;
}

/* Breakpoints (mobile-first) */
/* 480px  — mobile large */
/* 768px  — tablet */
/* 1024px — desktop */
/* 1440px — wide */
```

### Componentes Compartilhados Obrigatórios

| Componente | Path | Usado em |
|------------|------|----------|
| AppShell | `shared/components/AppShell.tsx` | Todas lanes |
| TopBar | `shared/components/TopBar.tsx` | Todas lanes |
| BottomNavigation | `shared/components/BottomNavigation.tsx` | Customer, Deliverer |
| Card | `shared/components/Card.tsx` | ✅ existe |
| Badge | `shared/components/Badge.tsx` | ✅ existe |
| Button | `shared/components/Button.tsx` | ✅ existe |
| Input | `shared/components/Input.tsx` | ✅ existe |
| StatusChip | `shared/components/StatusChip.tsx` | Pedidos, entregas |
| MetricCard | `shared/components/MetricCard.tsx` | Admin, dashboards |
| EmptyState | `shared/components/EmptyState.tsx` | ✅ existe |
| LoadingState | `shared/components/LoadingState.tsx` | Renomear/alias Loading |

**Regra:** nenhum componente duplicado entre lanes — importar de `shared/`.

---

## 7. Lanes Frontend — Escopo Mínimo

### Customer (`features/customer/`)

| Page | Função |
|------|--------|
| HomePage | Lista restaurantes (Card + Badge Aberto/Fechado) |
| MenuPage | Cardápio por categoria |
| CartPage | Carrinho + total |
| CheckoutPage | Endereço campus + pagar |
| OrderTrackingPage | Polling status 10s |
| OrderHistoryPage | Lista pedidos (inclui seed) |
| ProfilePage | Dados do user |

BottomNavigation: Home | Pedidos | Carrinho | Perfil

### Restaurant (`features/restaurant/`)

| Page | Função |
|------|--------|
| RestaurantDashboard | Métricas: pendentes, em preparo, finalizados |
| RestaurantOrdersPage | Lista pedidos filtrados por status |
| RestaurantDecisionPage | Botões Aceitar / Rejeitar |

Consome APIs existentes:
- `GET /api/v1/pedidos?restaurante_id=` (novo filtro no módulo pedido)
- `POST /api/v1/pedidos/{id}/decisao` (fix path)

**Sem CRUD. Sem edição de cardápio.**

### Deliverer (`features/deliverer/` — refatorar)

| Page | Função |
|------|--------|
| DashboardPage | Entregas disponíveis |
| ActiveDeliveryPage | Entrega ativa + **Avançar status** |
| HistoryPage | Histórico |
| ProfilePage | Perfil |

Remover `LoginPage` própria — usar auth unificada.

### Admin (`features/admin/`)

| Page | Função |
|------|--------|
| AdminDashboard | MetricCards: Total Clientes, Restaurantes, Pedidos, Entregadores |

Consome `GET /api/v1/admin/metrics` (read-only).

**Sem CRUD.**

---

## 8. Integrações Quebradas (mantidas + novas)

```
#1  Prefixo API deliverer /api vs /api/v1     → FIX Task 4
#2  Vite sem proxy                             → FIX Task 4
#3  Pagamento router off                       → FIX Task 5
#4  cardapio table missing                     → FIX Task 1
#5  Auth schema mismatch                       → FIX Task 1 + Task 3
#6  pedidos ↔ deliveries bridge               → FIX Task 7
#7  list_orders assigned_deliverer_id bug     → FIX Task 4
#8  Restaurante decisão path inválido          → FIX Task 6
#9  Login entregador separado do auth          → FIX Task 8 (remover LoginPage deliverer)
#10 Seed insuficiente para demo                → FIX Task 2
```

---

## 9. Definição de Pronto (atualizada)

### Autenticação e Navegação

- [ ] Login único funcional em `/login`
- [ ] JWT funcional
- [ ] Role persistida no banco (`usuarios.role`)
- [ ] Redirect automático baseado em role
- [ ] Route guards por role
- [ ] Cliente vê apenas experiência cliente
- [ ] Restaurante vê apenas experiência restaurante
- [ ] Entregador vê apenas experiência entregador
- [ ] Admin vê dashboard administrativo
- [ ] **Proibido** troca manual de perfil na UI

### Cliente

- [ ] Login demo `cliente@yummicious.com`
- [ ] Ver 3 restaurantes
- [ ] Ver cardápio (5 itens cada)
- [ ] Adicionar ao carrinho
- [ ] Criar pedido
- [ ] Pagar pedido (mock 1s)
- [ ] Acompanhar pedido (tracking)
- [ ] Ver histórico (inclui pedidos seed)

### Restaurante

- [ ] Login demo `burger@burgerhouse.com`
- [ ] Ver pedidos (Pendente / Em preparo / Finalizado)
- [ ] Aceitar pedido
- [ ] Rejeitar pedido

### Entregador

- [ ] Login demo `entregador@yummicious.com`
- [ ] Ver entregas disponíveis
- [ ] Aceitar entrega
- [ ] Avançar status (botão único demo)
- [ ] Finalizar entrega

### Admin

- [ ] Login demo `admin@yummicious.com`
- [ ] Ver métricas (clientes, restaurantes, pedidos, entregadores)
- [ ] Ver lista de pedidos

### Sistema

- [ ] Seed completa (`04_seed_demo.sql`)
- [ ] Sem dependências externas (pagamento)
- [ ] `make up` funcional
- [ ] `make test` verde
- [ ] Fluxo E2E demonstrável em **< 5 minutos**

---

## 10. Ordem de Execução

1. Branch `feat/mvp-final-integration`
2. DDL + tabela `usuarios`
3. **Seed demo completa** (`04_seed_demo.sql`)
4. Auth unificada backend
5. Integrações críticas (proxy, prefix, bugs)
6. Módulo pedido + pagamento mock + bridge entrega
7. Auth frontend (AuthProvider, Router, Guards)
8. Features: customer → restaurant → deliverer refactor → admin
9. Liquid design tokens + shared components
10. Testes E2E + PR

---

## 11. File Structure — Mudanças Planejadas

```
backend/
├── modulos/auth/                    # CREATE — login unificado
│   ├── rotas.py
│   └── auth_service.py
├── modulos/admin/                   # CREATE — metrics read-only
│   └── rotas.py
├── modulos/pedido/                  # CREATE
├── modulos/pagamento/
│   ├── mock_gateway.py              # CREATE
│   ├── controle.py                  # MODIFY — usa mock + delay
│   └── rotas.py
└── main.py                          # MODIFY — mount all routers

database/esquemas/
├── 03_alteracoes_mvp.sql            # CREATE — usuarios, cardapio, pedido enum
└── 04_seed_demo.sql                 # CREATE — contas, restaurantes, cardápio, pedidos

frontend/
├── package.json                     # MODIFY — add react-router-dom
├── src/app/
│   ├── providers/AuthProvider.tsx   # CREATE
│   ├── guards/RoleGuard.tsx         # CREATE
│   └── routes/index.tsx             # CREATE
├── src/features/auth/               # CREATE — LoginPage única
├── src/features/customer/           # CREATE
├── src/features/restaurant/         # CREATE
├── src/features/admin/              # CREATE
├── src/features/deliverer/          # MODIFY — remove LoginPage, add advance
└── src/shared/components/           # MODIFY — AppShell, TopBar, MetricCard, ...
```

---

## 12. Tasks de Implementação

### Task 0: Branch de Fechamento

- [ ] **Step 1: Criar branch**

```bash
git checkout main
git pull origin main
git checkout -b feat/mvp-final-integration
```

- [ ] **Step 2: Verificar baseline**

Run: `make test`
Expected: documentar estado atual (pass/fail)

---

### Task 1: Migration DDL — Schema MVP

**Files:**
- Create: `database/esquemas/03_alteracoes_mvp.sql`

- [ ] **Step 1: Criar migration**

```sql
USE yummicious_db;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    role ENUM('CLIENTE', 'RESTAURANTE', 'ENTREGADOR', 'ADMIN') NOT NULL,
    referencia_id VARCHAR(50) NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cardapio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10,2) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    id_restaurante INT NOT NULL,
    disponivel BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_restaurante) REFERENCES restaurantes(id),
    UNIQUE KEY uk_cardapio_nome_rest (nome, id_restaurante)
);

ALTER TABLE restaurantes
    ADD COLUMN IF NOT EXISTS usuario_id INT NULL;

ALTER TABLE pedidos
    MODIFY COLUMN status ENUM(
        'Pendente', 'Pago', 'Em preparo', 'Rejeitado',
        'Finalizado', 'Cancelado'
    ) DEFAULT 'Pendente';
```

- [ ] **Step 2: Aplicar**

Run: `make build-db`
Expected: tabelas `usuarios`, `cardapio` existem

- [ ] **Step 3: Commit**

```bash
git add database/esquemas/03_alteracoes_mvp.sql
git commit -m "fix: adicionar schema usuarios, cardapio e status pedido"
```

---

### Task 2: Seed Completa de Demonstração

**Files:**
- Create: `database/esquemas/04_seed_demo.sql`
- Modify: `docker-compose.yml` (garantir ordem init scripts 01→02→03→04)

- [ ] **Step 1: Criar seed demo**

```sql
-- database/esquemas/04_seed_demo.sql
USE yummicious_db;

-- Senha bcrypt de "123456" (gerar via passlib no script ou fixar hash conhecido)
-- Hash exemplo: $2b$12$... (substituir pelo hash real gerado em runtime ou script)

-- Usuarios demo
INSERT INTO usuarios (nome, email, senha, role, referencia_id) VALUES
('Cliente Demo', 'cliente@yummicious.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.G2oXjKjKjKjKjK', 'CLIENTE', 'cli_demo_001'),
('Burger House', 'burger@burgerhouse.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.G2oXjKjKjKjKjK', 'RESTAURANTE', '1'),
('Entregador Demo', 'entregador@yummicious.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.G2oXjKjKjKjKjK', 'ENTREGADOR', 'del_demo_001'),
('Admin Demo', 'admin@yummicious.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.G2oXjKjKjKjKjK', 'ADMIN', NULL)
ON DUPLICATE KEY UPDATE nome = VALUES(nome);

INSERT INTO clientes (id, nome, email, saldo) VALUES
('cli_demo_001', 'Cliente Demo', 'cliente@yummicious.com', 0.00)
ON DUPLICATE KEY UPDATE nome = VALUES(nome);

-- Restaurantes (3)
INSERT INTO restaurantes (id, nome, endereco, cnpj, horario, tipo, status, usuario_id) VALUES
(1, 'Burger House', 'Bloco A, Campus Central', '11.111.111/0001-11', '08:00-22:00', 'Lanches', 'Aberto', 2),
(2, 'Pizza Campus', 'Bloco B, Campus Central', '22.222.222/0001-22', '10:00-23:00', 'Pizza', 'Aberto', NULL),
(3, 'Açaí Federal', 'Bloco C, Campus Central', '33.333.333/0001-33', '09:00-21:00', 'Açaí', 'Aberto', NULL)
ON DUPLICATE KEY UPDATE nome = VALUES(nome);

-- Cardápio Burger House (5 itens)
INSERT INTO cardapio (nome, descricao, preco, categoria, id_restaurante) VALUES
('X-Burguer', 'Hambúrguer clássico', 25.00, 'Lanches', 1),
('X-Salada', 'Hambúrguer vegetariano', 28.00, 'Lanches', 1),
('Batata Frita', 'Porção média', 12.00, 'Acompanhamentos', 1),
('Coca-Cola 350ml', 'Refrigerante', 8.00, 'Bebidas', 1),
('Milkshake', 'Morango', 18.00, 'Bebidas', 1)
ON DUPLICATE KEY UPDATE preco = VALUES(preco);

-- Cardápio Pizza Campus (5 itens)
INSERT INTO cardapio (nome, descricao, preco, categoria, id_restaurante) VALUES
('Margherita', 'Molho, mussarela, manjericão', 45.00, 'Pizzas', 2),
('Calabresa', 'Calabresa e cebola', 42.00, 'Pizzas', 2),
('4 Queijos', 'Mussarela, gorgonzola, parmesão, catupiry', 48.00, 'Pizzas', 2),
('Guaraná 350ml', 'Refrigerante', 7.00, 'Bebidas', 2),
('Brownie', 'Com sorvete', 15.00, 'Sobremesas', 2)
ON DUPLICATE KEY UPDATE preco = VALUES(preco);

-- Cardápio Açaí Federal (5 itens)
INSERT INTO cardapio (nome, descricao, preco, categoria, id_restaurante) VALUES
('Açaí 300ml', 'Com granola', 16.00, 'Açaí', 3),
('Açaí 500ml', 'Com banana', 22.00, 'Açaí', 3),
('Granola Extra', 'Porção', 3.00, 'Adicionais', 3),
('Banana Extra', 'Unidade', 2.00, 'Adicionais', 3),
('Água 500ml', 'Sem gás', 4.00, 'Bebidas', 3)
ON DUPLICATE KEY UPDATE preco = VALUES(preco);

-- Pedidos demo (4 estados)
INSERT INTO pedidos (id, id_restaurante, status, cliente_id, valor_total, detalhes) VALUES
(1001, 1, 'Finalizado', 'cli_demo_001', 33.00, '{"itens":[{"nome":"X-Burguer","preco":25,"quantidade":1},{"nome":"Coca-Cola 350ml","preco":8,"quantidade":1}]}'),
(1002, 1, 'Em preparo', 'cli_demo_001', 25.00, '{"itens":[{"nome":"X-Burguer","preco":25,"quantidade":1}]}'),
(1003, 2, 'Pago', 'cli_demo_001', 45.00, '{"itens":[{"nome":"Margherita","preco":45,"quantidade":1}]}'),
(1004, 3, 'Cancelado', 'cli_demo_001', 16.00, '{"itens":[{"nome":"Açaí 300ml","preco":16,"quantidade":1}]}')
ON DUPLICATE KEY UPDATE status = VALUES(status);
```

- [ ] **Step 2: Script helper para gerar bcrypt**

```python
# scripts/generate_seed_hash.py
from passlib.context import CryptContext
print(CryptContext(schemes=["bcrypt"]).hash("123456"))
```

Run: `cd backend && python ../scripts/generate_seed_hash.py`
Substituir hashes placeholder no SQL.

- [ ] **Step 3: Seed entregador SQLite** (via startup hook ou script)

Criar deliverer `del_demo_001` na região `Zona Sul` com status AVAILABLE.

- [ ] **Step 4: Validar seed**

Run: `make build-db && docker exec yummicious_db mysql -u delivery_user -pdelivery_pass yummicious_db -e "SELECT email, role FROM usuarios; SELECT COUNT(*) FROM cardapio; SELECT status, COUNT(*) FROM pedidos GROUP BY status;"`
Expected: 4 usuarios, 15 cardápio items, 4 pedidos

- [ ] **Step 5: Commit**

```bash
git add database/esquemas/04_seed_demo.sql scripts/generate_seed_hash.py
git commit -m "feat: seed demo completa para apresentação E2E"
```

---

### Task 3: Auth Unificada — Backend

**Files:**
- Create: `backend/modulos/auth/auth_service.py`
- Create: `backend/modulos/auth/rotas.py`
- Modify: `backend/main.py`
- Test: `backend/tests/test_auth_login.py`

- [ ] **Step 1: Teste falhando**

```python
def test_login_cliente_demo(client):
    r = client.post("/api/v1/auth/login", json={
        "email": "cliente@yummicious.com", "senha": "123456"
    })
    assert r.status_code == 200
    body = r.json()
    assert body["user"]["role"] == "CLIENTE"
    assert "access_token" in body

def test_login_restaurante_demo(client):
    r = client.post("/api/v1/auth/login", json={
        "email": "burger@burgerhouse.com", "senha": "123456"
    })
    assert r.json()["user"]["role"] == "RESTAURANTE"

def test_login_entregador_demo(client):
    r = client.post("/api/v1/auth/login", json={
        "email": "entregador@yummicious.com", "senha": "123456"
    })
    assert r.json()["user"]["role"] == "ENTREGADOR"

def test_login_admin_demo(client):
    r = client.post("/api/v1/auth/login", json={
        "email": "admin@yummicious.com", "senha": "123456"
    })
    assert r.json()["user"]["role"] == "ADMIN"
```

- [ ] **Step 2: Implementar AuthService**

```python
# backend/modulos/auth/auth_service.py
from core.seguranca import verificar_senha
from core.jwt import criar_token
from core.conexao_banco import ConexaoBanco

class AuthService:
    @staticmethod
    def login(email: str, senha: str):
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            user = cursor.fetchone()
            if not user or not verificar_senha(senha, user["senha"]):
                return {"erro": "Credenciais inválidas", "status_code": 401}
            token = criar_token({"sub": str(user["id"]), "role": user["role"]})
            return {
                "access_token": token,
                "user": {
                    "id": user["id"],
                    "nome": user["nome"],
                    "email": user["email"],
                    "role": user["role"],
                    "referencia_id": user["referencia_id"],
                },
                "status_code": 200,
            }
        finally:
            cursor.close()
            conn.close()
```

```python
# backend/modulos/auth/rotas.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from modulos.auth.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])

class LoginRequest(BaseModel):
    email: str
    senha: str

@router.post("/login")
async def login(body: LoginRequest):
    resultado = AuthService.login(body.email, body.senha)
    if "erro" in resultado:
        raise HTTPException(status_code=resultado["status_code"], detail=resultado["erro"])
    return {"access_token": resultado["access_token"], "user": resultado["user"]}
```

- [ ] **Step 3: Mount + rodar testes**

Run: `cd backend && pytest tests/test_auth_login.py -v`
Expected: PASS (4 roles)

- [ ] **Step 4: Commit**

```bash
git commit -m "feat: autenticação unificada com login por role"
```

---

### Task 4: Integrações Críticas (Proxy, Prefix, Bugs)

*(Mesmo conteúdo da Task 1 original — prefix `/api/v1`, vite proxy, list_orders fix, active delivery filter)*

- [ ] Corrigir `main.py` deliverer prefix → `settings.API_V1_STR`
- [ ] Adicionar proxy Vite `/api` → `:8000`
- [ ] Fix `list_orders` → `o.deliverer_id`
- [ ] Fix `getActiveDelivery` excluir DELIVERED/CANCELLED
- [ ] Commit: `fix: integrações API v1 e proxy dev`

---

### Task 5: MockPaymentGateway + Mount Pagamento

**Files:**
- Create: `backend/modulos/pagamento/mock_gateway.py`
- Modify: `backend/modulos/pagamento/controle.py`
- Test: `backend/tests/test_pagamento_mock.py`

- [ ] **Step 1: Teste com delay**

```python
import pytest

@pytest.mark.asyncio
async def test_mock_gateway_approves_after_delay():
    from modulos.pagamento.mock_gateway import MockPaymentGateway
    import time
    start = time.monotonic()
    result = await MockPaymentGateway.processar(50.0)
    elapsed = time.monotonic() - start
    assert result["status"] == "APROVADO"
    assert elapsed >= 0.9
```

- [ ] **Step 2: Implementar gateway + processar_pagamento async**

```python
# mock_gateway.py
import asyncio
import uuid

class MockPaymentGateway:
    @staticmethod
    async def processar(valor: float) -> dict:
        await asyncio.sleep(1)
        return {"status": "APROVADO", "transaction_id": f"mock_{uuid.uuid4().hex[:8]}"}
```

Integrar em `PagamentoControle.processar_pagamento` (async endpoint).

- [ ] **Step 3: Commit**

```bash
git commit -m "feat: MockPaymentGateway com delay de 1s"
```

---

### Task 6: Módulo Pedido + Fix Decisão Restaurante

**Files:**
- Create: `backend/modulos/pedido/`
- Modify: `backend/modulos/restaurante/rotas.py`
- Test: `backend/tests/test_pedido_criar.py`

Adicionar ao pedido:
- `GET /api/v1/pedidos?cliente_id=` 
- `GET /api/v1/pedidos?restaurante_id=` (para painel restaurante)
- Fix path: `POST /api/v1/pedidos/{id_pedido}/decisao`

- [ ] Implementar + testes + commit `feat: módulo pedido e decisão restaurante`

---

### Task 7: Bridge Pagamento → Entrega

*(Mesmo da Task 4 original — uuid5 bridge após pagamento)*

- [ ] Commit: `feat: bridge pagamento para atribuição de entrega`

---

### Task 8: Auth Frontend — AuthProvider + Router + Guards

**Files:**
- Modify: `package.json` — add `react-router-dom`
- Create: `frontend/src/app/providers/AuthProvider.tsx`
- Create: `frontend/src/app/guards/RoleGuard.tsx`
- Create: `frontend/src/app/routes/index.tsx`
- Create: `frontend/src/features/auth/pages/LoginPage.tsx`
- Modify: `frontend/src/app/App.tsx`
- Test: `frontend/src/features/auth/__tests__/LoginPage.test.tsx`

- [ ] **Step 1: Instalar react-router-dom**

```bash
npm install react-router-dom
npm install -D @types/react-router-dom
```

- [ ] **Step 2: AuthProvider**

```typescript
// frontend/src/app/providers/AuthProvider.tsx
import { createContext, useContext, useState, useCallback, ReactNode } from 'react'

export type UserRole = 'CLIENTE' | 'RESTAURANTE' | 'ENTREGADOR' | 'ADMIN'

export interface AuthUser {
  id: number
  nome: string
  email: string
  role: UserRole
  referencia_id: string | null
}

interface AuthContextValue {
  user: AuthUser | null
  token: string | null
  login: (email: string, senha: string) => Promise<UserRole>
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | null>(null)
const STORAGE_KEY = 'yummicious_auth'

export function AuthProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState(() => {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : { user: null, token: null }
  })

  const login = useCallback(async (email: string, senha: string) => {
    const res = await fetch('/api/v1/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, senha }),
    })
    if (!res.ok) throw new Error('Credenciais inválidas')
    const data = await res.json()
    const next = { user: data.user, token: data.access_token }
    localStorage.setItem(STORAGE_KEY, JSON.stringify(next))
    setState(next)
    return data.user.role as UserRole
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem(STORAGE_KEY)
    setState({ user: null, token: null })
  }, [])

  return (
    <AuthContext.Provider value={{ ...state, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth outside AuthProvider')
  return ctx
}
```

- [ ] **Step 3: RoleGuard + Routes**

```typescript
// frontend/src/app/guards/RoleGuard.tsx
import { Navigate } from 'react-router-dom'
import { useAuth, UserRole } from '../providers/AuthProvider'

export function RoleGuard({ allowed, children }: { allowed: UserRole[]; children: React.ReactNode }) {
  const { user } = useAuth()
  if (!user) return <Navigate to="/login" replace />
  if (!allowed.includes(user.role) && user.role !== 'ADMIN') return <Navigate to="/login" replace />
  return <>{children}</>
}
```

```typescript
// frontend/src/app/routes/index.tsx
import { createBrowserRouter, Navigate } from 'react-router-dom'
import { RoleGuard } from '../guards/RoleGuard'
import LoginPage from '../../features/auth/pages/LoginPage'
import { CustomerRoutes } from '../../features/customer/routes/CustomerRoutes'
import { RestaurantRoutes } from '../../features/restaurant/routes/RestaurantRoutes'
import { DelivererRoutes } from '../../features/deliverer/routes/DelivererRoutes'
import { AdminRoutes } from '../../features/admin/routes/AdminRoutes'

export const router = createBrowserRouter([
  { path: '/login', element: <LoginPage /> },
  {
    path: '/customer/*',
    element: <RoleGuard allowed={['CLIENTE']}><CustomerRoutes /></RoleGuard>,
  },
  {
    path: '/restaurant/*',
    element: <RoleGuard allowed={['RESTAURANTE']}><RestaurantRoutes /></RoleGuard>,
  },
  {
    path: '/deliverer/*',
    element: <RoleGuard allowed={['ENTREGADOR']}><DelivererRoutes /></RoleGuard>,
  },
  {
    path: '/admin/*',
    element: <RoleGuard allowed={['ADMIN']}><AdminRoutes /></RoleGuard>,
  },
  { path: '/', element: <Navigate to="/login" replace /> },
  { path: '*', element: <Navigate to="/login" replace /> },
])
```

- [ ] **Step 4: LoginPage única (sem botões demo por role)**

```typescript
// frontend/src/features/auth/pages/LoginPage.tsx
// Form: email + senha
// On success: redirectByRole(role, navigate)
// Hint discreto: "Use contas demo da documentação" — NÃO botões "Entrar como X"
```

- [ ] **Step 5: App.tsx**

```typescript
import { RouterProvider } from 'react-router-dom'
import { AuthProvider } from './providers/AuthProvider'
import { router } from './routes'

export default function App() {
  return (
    <AuthProvider>
      <RouterProvider router={router} />
    </AuthProvider>
  )
}
```

- [ ] **Step 6: Teste + commit**

Run: `npm run test -- --testPathPattern=LoginPage`
```bash
git commit -m "feat: auth frontend com AuthProvider, Router e RoleGuard"
```

---

### Task 9: Feature Customer

**Files:** `frontend/src/features/customer/` (Home, Menu, Cart, Checkout, Tracking, History, Profile)

- [ ] CartContext + pages consumindo APIs existentes
- [ ] CheckoutPage chama pagamento mock (LoadingState 1s)
- [ ] BottomNavigation: Home | Pedidos | Carrinho | Perfil
- [ ] Commit: `feat: feature customer completa`

---

### Task 10: Feature Restaurant

**Files:** `frontend/src/features/restaurant/`

- [ ] RestaurantDashboard — MetricCards por status
- [ ] RestaurantOrdersPage — lista filtrada
- [ ] RestaurantDecisionPage — Aceitar / Rejeitar
- [ ] Commit: `feat: painel restaurante read-only com decisão de pedidos`

---

### Task 11: Feature Admin

**Files:**
- Create: `backend/modulos/admin/rotas.py` — `GET /admin/metrics`
- Create: `frontend/src/features/admin/pages/AdminDashboard.tsx`

```python
# backend/modulos/admin/rotas.py
@router.get("/admin/metrics")
async def metrics(user=Depends(require_admin)):
    return {
        "total_clientes": ...,
        "total_restaurantes": ...,
        "total_pedidos": ...,
        "total_entregadores": ...,
    }
```

- [ ] AdminDashboard com 4 MetricCards
- [ ] Lista read-only de pedidos
- [ ] Commit: `feat: dashboard admin read-only`

---

### Task 12: Refatorar Deliverer + Avançar Status

**Files:**
- Delete/deprecate: `frontend/src/features/deliverer/pages/LoginPage.tsx`
- Modify: `DelivererRoutes.tsx` — remover auth local, usar `useAuth()`
- Modify: `ActiveDeliveryPage.tsx` — botão "Avançar status"
- Create: `frontend/src/features/deliverer/hooks/useAdvanceDelivery.ts`

```typescript
// useAdvanceDelivery.ts
export function useAdvanceDelivery(delivery: Delivery | null) {
  const advance = async () => {
    if (!delivery) return
    switch (delivery.status) {
      case 'ASSIGNED':
        await acceptDelivery(delivery.orderId, delivererId)
        break
      case 'IN_DELIVERY':
        await pickupDelivery(delivery.orderId, delivererId)
        break
      case 'PICKED_UP':
        await deliverDelivery(delivery.orderId, delivererId)
        break
    }
  }
  return { advance, label: 'Avançar status' }
}
```

- [ ] Commit: `feat: deliverer integrado ao auth unificado com avanço de status demo`

---

### Task 13: Liquid Design + Shared Components

**Files:**
- Modify: `frontend/styles.css` — tokens completos
- Create: `AppShell.tsx`, `TopBar.tsx`, `BottomNavigation.tsx`, `MetricCard.tsx`, `StatusChip.tsx`, `LoadingState.tsx`

- [ ] Aplicar tokens em todas as features
- [ ] Remover CSS corrompido `.btn` / `.badge`
- [ ] Commit: `feat: design tokens liquid e componentes compartilhados`

---

### Task 14: Admin Metrics Backend + E2E

**Files:**
- Create: `cypress/e2e/demo-flow.cy.ts`
- Create: `bdd/backend/features/pedido/fluxo_completo.feature`

- [ ] **Step 1: Cypress E2E demo (< 5 min script)**

```typescript
// cypress/e2e/demo-flow.cy.ts
describe('Demo MVP', () => {
  it('fluxo cliente completo', () => {
    cy.visit('/login')
    cy.get('[data-cy=email]').type('cliente@yummicious.com')
    cy.get('[data-cy=password]').type('123456')
    cy.get('[data-cy=login-submit]').click()
    cy.url().should('include', '/customer')
    // ... adicionar item, checkout, pagar, tracking
  })
})
```

- [ ] **Step 2: Rodar suite**

Run: `make test && npm run cypress:run`
Expected: PASS

- [ ] **Step 3: Push + PR**

```bash
git push origin feat/mvp-final-integration
gh pr create --title "MVP Final Integration" ...
```

---

## 13. Roteiro de Demonstração (< 5 minutos)

| Min | Ação | Conta |
|-----|------|-------|
| 0:00 | `make up` → abrir app | — |
| 0:30 | Login cliente → ver restaurantes → pedir X-Burguer | cliente@yummicious.com |
| 1:30 | Checkout → pagar (loading 1s) → tracking | — |
| 2:00 | Logout → login restaurante → aceitar pedido | burger@burgerhouse.com |
| 2:30 | Logout → login entregador → aceitar → avançar status ×3 | entregador@yummicious.com |
| 3:30 | Logout → login cliente → histórico mostra Finalizado | cliente@yummicious.com |
| 4:00 | Logout → login admin → métricas | admin@yummicious.com |
| 4:30 | Mostrar pedidos seed (Em preparo, Cancelado) | — |

---

## 14. Self-Review

### Spec coverage

| Requisito | Task |
|-----------|------|
| Login único + redirect | Task 3, 8 |
| Guards por role | Task 8 |
| Seed demo E2E | Task 2 |
| Customer flow | Task 9 |
| Restaurant panel | Task 10 |
| Admin dashboard | Task 11 |
| Deliverer + advance | Task 12 |
| MockPaymentGateway | Task 5 |
| RF-001 a RF-010 | Tasks 3–12 |

**Removido do escopo:** gateway real, email comprovante, cupons, CRUD admin/restaurant.

### Placeholder scan

Hashes bcrypt na seed devem ser gerados via script (Task 2 Step 2) — não deixar placeholder em produção.

### Type consistency

- `UserRole` frontend = `ENUM` backend (`CLIENTE`, `RESTAURANTE`, `ENTREGADOR`, `ADMIN`)
- JWT payload: `{ sub: user_id, role: UserRole }`

---

## 15. Estimativa Total (atualizada)

| Área | Esforço |
|------|---------|
| DDL + Seed demo | ~6h |
| Auth unificada (BE + FE) | ~10h |
| Pedido + Pagamento + Bridge | ~12h |
| Customer frontend | ~14h |
| Restaurant frontend | ~8h |
| Admin frontend + metrics | ~6h |
| Deliverer refactor | ~4h |
| Design tokens + shared | ~4h |
| E2E + PR | ~6h |
| **Total** | **~70h (~9 dias úteis)** |

---

Plan complete and saved to `docs/superpowers/plans/2026-06-09-mvp-delivery-fechamento.md`. Two execution options:

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
