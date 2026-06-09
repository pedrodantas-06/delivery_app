import { requestJson } from '../../../shared/services/http'
import type { Order } from '../../customer/types'

const API_BASE = '/api/v1'

export interface AdminMetrics {
  total_clientes: number
  total_restaurantes: number
  total_pedidos: number
  total_entregadores: number
}

export async function getMetrics(token: string) {
  return requestJson<AdminMetrics>(`${API_BASE}/admin/metrics`, undefined, token)
}

export async function getPedidos(token: string) {
  return requestJson<Order[]>(`${API_BASE}/admin/pedidos`, undefined, token)
}
