import { requestJson } from '../../../shared/services/http'
import type {
  Deliverer,
  DelivererApiDeliverer,
  DelivererApiListResponse,
  DelivererLoginForm,
  DelivererStatus,
} from '../types'

const API_BASE = '/api/v1'

function mapDeliverer(payload: DelivererApiDeliverer): Deliverer {
  return {
    id: payload.id,
    name: payload.name,
    phone: payload.phone,
    region: payload.region,
    status: payload.status,
  }
}

export async function getDeliverers(region: string) {
  const response = await requestJson<DelivererApiListResponse<DelivererApiDeliverer>>(
    `${API_BASE}/deliverers/?region=${encodeURIComponent(region)}`,
  )
  return response.items.map(mapDeliverer)
}

export async function createDeliverer(form: DelivererLoginForm) {
  const response = await requestJson<DelivererApiDeliverer>(`${API_BASE}/deliverers/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(form),
  })
  return mapDeliverer(response)
}

export async function updateDelivererStatus(delivererId: string, status: DelivererStatus) {
  const response = await requestJson<DelivererApiDeliverer>(`${API_BASE}/deliverers/${delivererId}/status/`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status }),
  })
  return mapDeliverer(response)
}
