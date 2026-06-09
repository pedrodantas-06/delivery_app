import { useCallback, useMemo } from 'react'
import { acceptDelivery, deliverDelivery, pickupDelivery } from '../api/deliveryApi'
import type { Delivery, DeliveryStatus } from '../types'

const ADVANCEABLE_STATUSES: DeliveryStatus[] = ['ASSIGNED', 'IN_DELIVERY', 'PICKED_UP']

const NEXT_LABELS: Partial<Record<DeliveryStatus, string>> = {
  ASSIGNED: 'Aceitar',
  IN_DELIVERY: 'Coletar',
  PICKED_UP: 'Entregar',
}

export function useAdvanceDelivery(delivery: Delivery | null, delivererId: string) {
  const canAdvance = useMemo(
    () => delivery !== null && ADVANCEABLE_STATUSES.includes(delivery.status),
    [delivery],
  )

  const nextLabel = useMemo(() => {
    if (!delivery) return null
    return NEXT_LABELS[delivery.status] ?? null
  }, [delivery])

  const advance = useCallback(async () => {
    if (!delivery || !canAdvance) return

    switch (delivery.status) {
      case 'ASSIGNED':
        await acceptDelivery(delivery.orderId, delivererId)
        break
      case 'IN_DELIVERY':
        await pickupDelivery(delivery.orderId, delivererId)
        break
      case 'PICKED_UP':
        await deliverDelivery(delivery.orderId, delivererId)
        break
    }
  }, [delivery, delivererId, canAdvance])

  return {
    advance,
    label: 'Avançar status',
    canAdvance,
    nextLabel,
  }
}
