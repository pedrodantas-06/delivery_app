# PRD — Delivery Universitário (MVP)

**Versão:** 1.0  
**Status:** Draft  
**Autor:** Product Management  
**Data:** 2026-05-30

---

# 1. Visão do Produto (Product Vision)

## Resumo Executivo

O Delivery Universitário é uma plataforma de delivery hiperlocal focada em ambientes acadêmicos, conectando estudantes, restaurantes do campus e entregadores em um único ecossistema.

O produto busca resolver problemas específicos que plataformas tradicionais não atendem adequadamente, como entregas em blocos, salas e laboratórios, filas em horários de pico e dependência de canais informais (WhatsApp).

## Problema

### Para estudantes

- Filas longas em horários de almoço
- Pouco tempo entre aulas
- Dificuldade para receber pedidos em locais internos do campus

### Para restaurantes

- Gestão manual de pedidos
- Dependência de WhatsApp
- Falta de previsibilidade operacional

### Para entregadores

- Rotas ineficientes
- Baixa organização dos pedidos
- Falta de visibilidade operacional

## Proposta de Valor

"Receba seu pedido dentro do campus de forma rápida, organizada e previsível."

---

# 2. Público-Alvo e Personas

## Persona 1 — Estudante

### Perfil

- 18 a 30 anos
- Frequenta campus universitário diariamente
- Usuário frequente de aplicativos mobile

### Necessidades

- Rapidez
- Conveniência
- Pagamento simples

---

## Persona 2 — Restaurante

### Perfil

- Pequenos restaurantes
- Lanchonetes
- Cafeterias

### Necessidades

- Organização operacional
- Redução de erros
- Recebimento estruturado de pedidos

---

## Persona 3 — Entregador

### Perfil

- Alunos
- Freelancers
- Entregadores locais

### Necessidades

- Fluxo simples de entregas
- Rotas organizadas
- Ganhos previsíveis

---

# 3. Objetivos e Métricas (OKRs)

## Objetivo 1

Validar adoção dentro de um campus universitário.

### Key Results

- 500 usuários cadastrados
- 100 pedidos semanais
- 5 restaurantes ativos

---

## Objetivo 2

Garantir boa experiência de entrega.

### Key Results

- Tempo médio de entrega < 20 minutos
- Taxa de sucesso das entregas > 95%
- Taxa de cancelamento < 5%

---

## Objetivo 3

Validar retenção inicial.

### Key Results

- 30% dos usuários realizando novo pedido em até 30 dias
- NPS > 50

---

# 4. Requisitos Funcionais (RFs)

## Prioridade P0 (Must Have)

### RF-001 Cadastro e Login

Usuários podem:

- Criar conta
- Fazer login
- Recuperar senha

---

### RF-002 Gestão de Restaurantes

Restaurante pode:

- Cadastrar perfil
- Atualizar informações
- Definir status aberto/fechado

---

### RF-003 Gestão de Cardápio

Restaurante pode:

- Criar item
- Editar item
- Remover item
- Informar preço

---

### RF-004 Catálogo para Cliente

Cliente pode:

- Visualizar restaurantes
- Visualizar cardápio
- Buscar itens

---

### RF-005 Carrinho

Cliente pode:

- Adicionar itens
- Alterar quantidades
- Remover itens

---

### RF-006 Criação de Pedido

Cliente pode:

- Confirmar pedido
- Informar localização acadêmica

Campos obrigatórios:

- Campus
- Bloco
- Sala

---

### RF-007 Pagamento

Integração com gateway externo.

Métodos:

- PIX
- Cartão

---

### RF-008 Painel Restaurante

Restaurante pode:

- Receber pedidos
- Atualizar status

Status:

- CREATED
- PREPARING
- READY

---

### RF-009 Gestão de Entregas

Sistema pode:

- Atribuir entregador disponível
- Atualizar status

Status:

- ASSIGNED
- PICKED_UP
- DELIVERED

---

### RF-010 Histórico de Pedidos

Cliente pode visualizar:

- Pedidos anteriores
- Status final
- Valor

---

## Prioridade P1 (Should Have)

### RF-011 Rastreamento em Tempo Real

Visualização do status atual do pedido.

---

### RF-012 Notificações

Push notifications para:

- Pedido aceito
- Pedido pronto
- Pedido entregue

---

### RF-013 Avaliação

Cliente avalia:

- Restaurante
- Entrega

---

## Prioridade P2 (Nice to Have)

### RF-014 Cupons

Sistema promocional.

---

### RF-015 Programa de Fidelidade

Acúmulo de pontos.

---

### RF-016 Pedidos Recorrentes

Repetir pedido anterior.

---

# 5. Requisitos Não Funcionais (RNFs)

## RNF-001 Segurança

- Autenticação JWT
- Senhas criptografadas
- HTTPS obrigatório

---

## RNF-002 Performance

- Tempo médio de resposta < 500ms
- APIs críticas < 1s

---

## RNF-003 Disponibilidade

- Disponibilidade mínima 99,5%

---

## RNF-004 Escalabilidade

Arquitetura preparada para:

- Múltiplos campi
- Múltiplas universidades

---

## RNF-005 Observabilidade

- Logs estruturados
- Tracing distribuído
- Métricas de negócio

---

## RNF-006 LGPD

- Consentimento de dados
- Exclusão de conta
- Exportação de dados pessoais

---

# 6. Jornada do Usuário (User Stories)

## Cliente

### US-001

Como estudante,
quero visualizar restaurantes,
para escolher onde pedir.

### US-002

Como estudante,
quero realizar um pedido,
para receber comida sem sair da sala.

### US-003

Como estudante,
quero acompanhar meu pedido,
para saber quando chegará.

---

## Restaurante

### US-004

Como restaurante,
quero receber pedidos digitalmente,
para evitar erros operacionais.

### US-005

Como restaurante,
quero atualizar o status do pedido,
para informar o cliente.

---

## Entregador

### US-006

Como entregador,
quero receber pedidos disponíveis,
para realizar entregas.

### US-007

Como entregador,
quero atualizar o status da entrega,
para informar progresso.

---

# 7. Critérios de Aceite

## Cadastro

Dado que o usuário preenche os campos obrigatórios

Quando enviar o formulário

Então sua conta deve ser criada com sucesso

---

## Pedido

Dado que existem itens no carrinho

Quando o cliente confirmar o pedido

Então um pedido deve ser criado com status CREATED

---

## Pagamento

Dado que o pagamento foi aprovado

Quando o gateway retornar sucesso

Então o pedido deve ser atualizado para PAID

---

## Entrega

Dado que existe entregador disponível

Quando o pedido estiver READY

Então o sistema deve atribuir um entregador automaticamente

---

# 8. Roadmap Pós-Lançamento

## Fase 1 — MVP

- Cadastro
- Cardápio
- Pedido
- Pagamento
- Entrega

---

## Fase 2 — Operação

- Rastreamento em tempo real
- Notificações push
- Avaliações

---

## Fase 3 — Crescimento

- Cupons
- Fidelidade
- Indicação de amigos
- Analytics operacional

---

## Fase 4 — Escala

- Multi-campus
- Multi-universidade
- Entregas agrupadas
- Otimização de rotas

---

# Fora de Escopo do MVP

- Inteligência artificial
- Chat interno
- Entrega por drones
- Assinaturas mensais
- Programa avançado de fidelidade
