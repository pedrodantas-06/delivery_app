import type { Delivery, DelivererSession } from '../types'

export function getActiveDelivery(deliveries: Delivery[], sessionId?: string | null) {
  return deliveries.find((delivery) => delivery.delivererId === sessionId || delivery.assignedDelivererId === sessionId) ?? null
}

export function getDeliveryHistory(deliveries: Delivery[], sessionId?: string | null) {
  return deliveries.filter((delivery) => delivery.delivererId === sessionId || delivery.assignedDelivererId === sessionId)
}

export function getAvailableDeliveries(deliveries: Delivery[]) {
  return deliveries.filter((delivery) => delivery.status === 'WAITING' || delivery.status === 'ASSIGNED')
}

export function isSessionActive(session: DelivererSession | null) {
  return session !== null
}
