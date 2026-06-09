import { requestJson } from '../../../shared/services/http'
import type {
  CreateOrderPayload,
  CreateOrderResponse,
  MenuResponse,
  Order,
  Restaurant,
} from '../types'

const API_BASE = '/api/v1'

export async function getRestaurants() {
  return requestJson<Restaurant[]>(`${API_BASE}/restaurantes`)
}

export async function getMenu(restaurantId: number) {
  return requestJson<MenuResponse>(`${API_BASE}/restaurantes/${restaurantId}/cardapio`)
}

export async function createOrder(payload: CreateOrderPayload) {
  return requestJson<CreateOrderResponse>(`${API_BASE}/pedidos`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
}

export async function processPayment(pedidoId: number) {
  return requestJson<{ pedido_id: number; status: string; transaction_id: string }>(
    `${API_BASE}/pagamento/processar/${pedidoId}`,
    { method: 'POST' },
  )
}

export async function getOrders(clienteId: string) {
  return requestJson<Order[]>(`${API_BASE}/pedidos?cliente_id=${encodeURIComponent(clienteId)}`)
}
