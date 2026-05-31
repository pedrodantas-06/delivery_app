import { renderHook } from '@testing-library/react'
import { useDeliveryHistory } from '../hooks/useDeliveryHistory'
import type { Delivery } from '../types'

const deliveries: Delivery[] = [
  {
    orderId: 'order-1',
    region: 'Zona Sul',
    status: 'WAITING',
    delivererId: null,
  },
  {
    orderId: 'order-2',
    region: 'Zona Sul',
    status: 'DELIVERED',
    delivererId: 'deliverer-1',
    assignedDelivererId: 'deliverer-1',
  },
]

describe('useDeliveryHistory', () => {
  it('returns only deliveries related to the session', () => {
    const { result } = renderHook(() => useDeliveryHistory(deliveries, 'deliverer-1'))

    expect(result.current).toHaveLength(1)
    expect(result.current[0]?.orderId).toBe('order-2')
  })
})
