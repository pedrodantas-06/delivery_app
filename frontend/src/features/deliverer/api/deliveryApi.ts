import { requestJson } from '../../../shared/services/http'
import type {
  Delivery,
  DelivererApiDelivery,
  DelivererApiListResponse,
  DeliveryStatus,
} from '../types'

const API_BASE = '/api/v1'

function mapDelivery(payload: DelivererApiDelivery): Delivery {
  return {
    orderId: payload.order_id,
    region: payload.region,
    status: payload.status,
    delivererId: payload.deliverer_id,
    assignedDelivererId: payload.assigned_deliverer_id ?? payload.deliverer_id,
    assignedAt: payload.assigned_at ?? null,
    pickedUpAt: payload.picked_up_at ?? null,
    deliveredAt: payload.delivered_at ?? null,
  }
}

export async function getDeliveries(region: string) {
  const response = await requestJson<DelivererApiListResponse<DelivererApiDelivery>>(
    `${API_BASE}/orders/?region=${encodeURIComponent(region)}`,
  )
  return response.items.map(mapDelivery)
}

export async function assignDelivery(orderId: string, region: string, delivererId?: string | null) {
  const response = await requestJson<DelivererApiDelivery>(`${API_BASE}/orders/assign/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ order_id: orderId, region, deliverer_id: delivererId ?? null }),
  })
  return mapDelivery(response)
}

export async function acceptDelivery(orderId: string, delivererId: string) {
  const response = await requestJson<DelivererApiDelivery>(`${API_BASE}/orders/${orderId}/accept/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ deliverer_id: delivererId }),
  })
  return mapDelivery(response)
}

export async function pickupDelivery(orderId: string, delivererId: string) {
  const response = await requestJson<DelivererApiDelivery>(`${API_BASE}/orders/${orderId}/pickup/`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ deliverer_id: delivererId }),
  })
  return mapDelivery(response)
}

export async function deliverDelivery(orderId: string, delivererId: string) {
  const response = await requestJson<DelivererApiDelivery>(`${API_BASE}/orders/${orderId}/deliver/`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ deliverer_id: delivererId }),
  })
  return mapDelivery(response)
}

export function isDelivering(status: DeliveryStatus) {
  return status === 'ASSIGNED' || status === 'IN_DELIVERY' || status === 'PICKED_UP'
}
