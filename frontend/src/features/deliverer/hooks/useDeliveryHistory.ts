import { useMemo } from 'react'
import { getDeliveryHistory } from '../services/deliveryService'
import type { Delivery } from '../types'

export function useDeliveryHistory(deliveries: Delivery[], sessionId?: string | null) {
  return useMemo(() => getDeliveryHistory(deliveries, sessionId), [deliveries, sessionId])
}
