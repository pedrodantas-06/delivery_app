export type DelivererStatus = 'AVAILABLE' | 'BUSY' | 'OCCUPIED' | 'OFFLINE'
export type DeliveryStatus = 'WAITING' | 'ASSIGNED' | 'IN_DELIVERY' | 'PICKED_UP' | 'DELIVERED' | 'CANCELLED'

export type Deliverer = {
  id: string
  name: string
  phone: string
  region: string
  status: DelivererStatus
}

export type Delivery = {
  orderId: string
  region: string
  status: DeliveryStatus
  delivererId: string | null
  assignedDelivererId?: string | null
  assignedAt?: string | null
  pickedUpAt?: string | null
  deliveredAt?: string | null
}

export type DelivererSession = {
  id: string
  name: string
  phone: string
  region: string
}

export type DelivererTab = 'dashboard' | 'active' | 'history' | 'profile'

export type DelivererFilters = {
  region: string
}

export type DelivererLoginForm = {
  name: string
  phone: string
  region: string
}

export type DelivererApiListResponse<T> = {
  items: T[]
}

export type DelivererApiDeliverer = {
  id: string
  name: string
  phone: string
  region: string
  status: DelivererStatus
}

export type DelivererApiDelivery = {
  order_id: string
  region: string
  status: DeliveryStatus
  deliverer_id: string | null
  assigned_deliverer_id?: string | null
  assigned_at?: string | null
  picked_up_at?: string | null
  delivered_at?: string | null
}
