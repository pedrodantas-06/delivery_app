# 🚀 Cronograma de Desenvolvimento — Delivery App (4 Sprints)

## 📌 Contexto Geral

- Duração: **4 sprints (2 semanas cada)**
- Objetivo: Entregar um **MVP funcional incremental**, iniciando já na **Sprint 1**
- Estratégia:
  - Desenvolvimento por **lanes (domínios paralelos)**
  - Integração contínua ao final de cada semana
  - Uso de **APIs externas** para reduzir complexidade (pagamento, mapas, etc.)

---

## 🧩 Lanes / Épicos

- 🍽️ Restaurantes
- 🧑‍🍳 Cardápio
- 🛒 Fazer Pedido
- 🧍 Clientes
- 🚴 Entregadores
- 💳 Pagamento

---

# 🏁 Visão Geral dos Milestones

| Milestone | Descrição | Sprint |
|----------|----------|--------|
| M1 | Base funcional + primeiro fluxo simples | Sprint 1 |
| M2 | Fluxo completo de pedido (sem pagamento real) | Sprint 2 |
| M3 | Integração com pagamento + melhorias UX | Sprint 3 |
| M4 | MVP completo integrado e estável | Sprint 4 |

---

# 🧱 Sprint 1 — Fundação + MVP Inicial

## 🎯 Objetivo
Ter um **MVP mínimo funcional**, mesmo que simples.

---

## 📦 Entregas por Épico

### 🧍 Clientes
- Cadastro simples (nome, email)
- Autenticação básica (mock ou simples)

---

### 🍽️ Restaurantes
- Cadastro de restaurante
- Listagem básica

---

### 🧑‍🍳 Cardápio
- Cadastro de itens
- Listagem de itens por restaurante

---

### 🛒 Fazer Pedido
- Criar pedido simples (sem pagamento)
- Adicionar itens ao pedido

---

### 🚴 Entregadores
- Cadastro de entregador
- Status (AVAILABLE / OFFLINE)

---

### 💳 Pagamento
- ❌ Não implementado ainda (mock apenas)

---

## 🔗 Integrações da Sprint

- Cliente cria pedido
- Pedido contém itens do cardápio
- Pedido associado a restaurante

---

## 🏁 Marco semanal (Semana 2)

👉 Usuário consegue:
- Ver restaurantes
- Ver cardápio
- Criar pedido simples

---

## 🎯 Milestone

**M1 — MVP inicial funcional**

---

# ⚙️ Sprint 2 — Fluxo Completo de Pedido

## 🎯 Objetivo
Completar o fluxo de entrega **sem pagamento real**

---

## 📦 Entregas por Épico

### 🛒 Fazer Pedido
- Finalização de pedido
- Status do pedido (CREATED → ASSIGNED)

---

### 🚴 Entregadores
- Atribuição automática de entregador
- Reatribuição em caso de falha

---

### 🧍 Clientes
- Histórico de pedidos

---

### 🍽️ Restaurantes
- Associação pedido ↔ restaurante

---

### 🧑‍🍳 Cardápio
- Ajustes e validações

---

### 💳 Pagamento
- Mock de pagamento (status: PENDING / PAID)

---

## 🔗 Integrações da Sprint

- Pedido → atribuição de entregador
- Atualização de status
- Fluxo completo sem pagamento real

---

## 🏁 Marco semanal (Semana 4)

👉 Sistema permite:
- Criar pedido
- Atribuir entregador
- Simular fluxo de entrega

---

## 🎯 Milestone

**M2 — Fluxo completo sem pagamento real**

---

# 💳 Sprint 3 — Pagamento + Refinamento

## 🎯 Objetivo
Adicionar pagamento real e melhorar UX

---

## 📦 Entregas por Épico

### 💳 Pagamento
- Integração com API externa (ex: Stripe/Mercado Pago)
- Confirmação de pagamento

---

### 🛒 Fazer Pedido
- Bloquear fluxo sem pagamento confirmado
- Atualizar status: PAID → IN_DELIVERY

---

### 🚴 Entregadores
- Melhorar lógica de seleção (simples, mas robusta)

---

### 🧍 Clientes
- Visualização de status do pedido

---

### 🎨 Frontend (todos)
- Aplicar Design System
- Melhorar feedback visual

---

## 🔗 Integrações da Sprint

- Pedido depende de pagamento
- Fluxo completo realista

---

## 🏁 Marco semanal (Semana 6)

👉 Usuário consegue:
- Pagar pedido
- Acompanhar status
- Receber confirmação

---

## 🎯 Milestone

**M3 — Pagamento integrado + UX melhorada**

---

# 🧪 Sprint 4 — Estabilização + MVP Final

## 🎯 Objetivo
Garantir qualidade, integração total e estabilidade

---

## 📦 Entregas por Épico

### 🚴 Entregadores
- Ajustes finais
- Logs e rastreabilidade

---

### 🛒 Fazer Pedido
- Tratamento de erros
- Melhorias de fluxo

---

### 💳 Pagamento
- Tratamento de falhas
- Retry básico

---

### 🧍 Clientes
- Ajustes finais de UX

---

### 🧪 Qualidade (todos)
- Revisão de cenários BDD
- Testes integrados
- Correção de bugs

---

## 🔗 Integrações da Sprint

- Todos os fluxos integrados:
  - Cliente → Pedido → Pagamento → Entregador

---

## 🏁 Marco semanal (Semana 8)

👉 Sistema completo:

- Pedido real
- Pagamento real
- Entrega simulada funcional

---

## 🎯 Milestone

**M4 — MVP completo e estável**

---

# 🔄 Estratégia de Integração Contínua

## 📌 Regras obrigatórias

- Toda feature deve:
  - Ter cenários BDD
  - Passar nos testes antes de merge
- Integração mínima semanal
- PR obrigatória com review

---

## 🔗 Integração entre lanes

| Lane | Depende de |
|------|-----------|
| Pedido | Cardápio, Cliente |
| Entregadores | Pedido |
| Pagamento | Pedido |
| Cliente | Pedido |

---

# ⚠️ Decisões Arquiteturais

- Pagamento via API externa
- Sem otimizações complexas
- Foco em fluxo funcional

---

# 🎯 Resultado Esperado

Ao final:

- MVP funcional de delivery
- Fluxo completo:
  - Cliente → Pedido → Pagamento → Entrega
- Código organizado e testável
- Integração suave entre equipes

---

# 🚀 Diretriz Final

> Entregar valor incremental toda semana  
> > Integrar cedo, integrar sempre  
> > Simples > complexo  
> > Funcional > perfeito