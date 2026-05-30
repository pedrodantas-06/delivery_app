import { renderHook } from '@testing-library/react'
import { useActiveDelivery } from '../hooks/useActiveDelivery'
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
    status: 'ASSIGNED',
    delivererId: 'deliverer-1',
    assignedDelivererId: 'deliverer-1',
  },
]

describe('useActiveDelivery', () => {
  it('returns the active delivery for the current session', () => {
    const { result } = renderHook(() => useActiveDelivery(deliveries, 'deliverer-1'))

    expect(result.current?.orderId).toBe('order-2')
  })
})
