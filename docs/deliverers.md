# Deliverers Feature Guide

## Escopo
Feature inicial para gerir entregadores e atribuicao de pedidos.

## Entidades
- Deliverer
  - `id`, `name`, `phone`, `region`, `status`
- Order
  - `id`, `region`, `status`, `assigned_deliverer_id`

## Status
- Deliverer: `AVAILABLE`, `OCCUPIED`, `OFFLINE`
- Order: `PENDING`, `IN_DELIVERY`, `WAITING`

## Regras de negocio
1. Cadastro cria entregador com status `AVAILABLE`.
2. Atualizacao de status altera apenas o entregador alvo.
3. Atribuicao automatica seleciona primeiro `AVAILABLE` da mesma regiao.
4. Atribuicao manual exige entregador `AVAILABLE` e da mesma regiao.
5. Nao atribuir quando entregador estiver `OCCUPIED` ou `OFFLINE`.
6. Reatribuicao por `refused` ou `timeout` libera entregador atual e tenta novo.
7. Sem entregador disponivel na reatribuicao, pedido vai para `WAITING`.

## Endpoints
- `GET /api/deliverers/?status=AVAILABLE&region=Zona Sul`
- `POST /api/deliverers/`
- `PATCH /api/deliverers/{deliverer_id}/status/`
- `POST /api/orders/assign/` (automatico ou manual com `deliverer_id`)
- `POST /api/orders/{order_id}/reassign/` (body com `reason`)

## Payloads
### Criar entregador
```json
{
  "name": "Ana",
  "phone": "11999999999",
  "region": "Zona Sul"
}
```

### Atribuicao manual
```json
{
  "order_id": "uuid",
  "region": "Zona Sul",
  "deliverer_id": "uuid"
}
```

### Reatribuicao
```json
{
  "reason": "refused"
}
```

## Como evoluir sem quebrar
- Adicionar nova regra primeiro em BDD
- Implementar no service
- Ajustar controller apenas para receber/retornar payload
- Manter repositorio sem regra de negocio
