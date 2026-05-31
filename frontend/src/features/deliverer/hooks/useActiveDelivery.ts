import { useMemo } from 'react'
import { getActiveDelivery } from '../services/deliveryService'
import type { Delivery } from '../types'

export function useActiveDelivery(deliveries: Delivery[], sessionId?: string | null) {
  return useMemo(() => getActiveDelivery(deliveries, sessionId), [deliveries, sessionId])
}
