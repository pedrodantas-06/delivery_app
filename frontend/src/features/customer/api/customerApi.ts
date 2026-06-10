import { requestJson } from '../../../shared/services/http'
import type {
  CreateOrderPayload,
  CreateOrderResponse,
  CustomerProfile,
  MenuResponse,
  Order,
  OrderStats,
  Restaurant,
  UpdateProfilePayload,
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

export async function getProfile(token: string | null) {
  return requestJson<CustomerProfile>(`${API_BASE}/clientes/me`, undefined, token)
}

export async function getOrderStats(token: string | null) {
  return requestJson<OrderStats>(`${API_BASE}/clientes/me/estatisticas`, undefined, token)
}

export async function updateProfile(
  usuarioId: number,
  payload: UpdateProfilePayload,
  token: string | null,
) {
  return requestJson<{ mensagem: string }>(
    `${API_BASE}/clientes/${usuarioId}`,
    {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    },
    token,
  )
}

export async function deleteAccount(usuarioId: number, token: string | null) {
  return requestJson<{ mensagem: string }>(
    `${API_BASE}/clientes/${usuarioId}`,
    { method: 'DELETE' },
    token,
  )
}
