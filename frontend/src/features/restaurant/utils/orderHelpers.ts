import type { Order } from '../../customer/types'

export const RESTAURANT_METRIC_STATUSES = ['Pendente', 'Em preparo', 'Finalizado', 'Pago'] as const

export const ORDER_FILTER_STATUSES = ['Todos', ...RESTAURANT_METRIC_STATUSES] as const

export type OrderFilterStatus = (typeof ORDER_FILTER_STATUSES)[number]

export function countByStatus(orders: Order[], status: string) {
  const normalized = status.toLowerCase()
  return orders.filter((order) => order.status.toLowerCase() === normalized).length
}

export function filterOrdersByStatus(orders: Order[], filter: OrderFilterStatus) {
  if (filter === 'Todos') return orders
  return orders.filter((order) => order.status.toLowerCase() === filter.toLowerCase())
}

export function canDecideOrder(status: string) {
  const normalized = status.toLowerCase()
  return normalized === 'pendente' || normalized === 'pago'
}

export function parseOrderDetalhes(detalhes: Order['detalhes']) {
  if (typeof detalhes === 'string') {
    try {
      return JSON.parse(detalhes) as Record<string, unknown>
    } catch {
      return null
    }
  }
  return detalhes
}
