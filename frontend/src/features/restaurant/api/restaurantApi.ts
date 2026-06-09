import { requestJson } from '../../../shared/services/http'
import type { Order } from '../../customer/types'

const API_BASE = '/api/v1'

export type OrderDecision = 'aceito' | 'rejeitado'

export async function getOrders(restauranteId: string) {
  return requestJson<Order[]>(`${API_BASE}/pedidos?restaurante_id=${encodeURIComponent(restauranteId)}`)
}

export async function decideOrder(pedidoId: number, idRestaurante: number, aceitacao: OrderDecision) {
  return requestJson<{ mensagem: string }>(`${API_BASE}/pedidos/${pedidoId}/decisao`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      id_pedido: pedidoId,
      id_restaurante: idRestaurante,
      aceitacao,
    }),
  })
}
