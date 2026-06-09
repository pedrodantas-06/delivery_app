import { act, renderHook } from '@testing-library/react'
import { useAdvanceDelivery } from '../hooks/useAdvanceDelivery'
import { acceptDelivery, deliverDelivery, pickupDelivery } from '../api/deliveryApi'
import type { Delivery } from '../types'

jest.mock('../api/deliveryApi', () => ({
  acceptDelivery: jest.fn(),
  pickupDelivery: jest.fn(),
  deliverDelivery: jest.fn(),
}))

const delivererId = 'deliverer-1'

function makeDelivery(status: Delivery['status']): Delivery {
  return {
    orderId: 'order-1',
    region: 'Zona Sul',
    status,
    delivererId,
  }
}

describe('useAdvanceDelivery', () => {
  beforeEach(() => {
    jest.clearAllMocks()
    ;(acceptDelivery as jest.Mock).mockResolvedValue(makeDelivery('IN_DELIVERY'))
    ;(pickupDelivery as jest.Mock).mockResolvedValue(makeDelivery('PICKED_UP'))
    ;(deliverDelivery as jest.Mock).mockResolvedValue(makeDelivery('DELIVERED'))
  })

  it('exposes the demo label and next step labels', () => {
    const { result: assigned } = renderHook(() => useAdvanceDelivery(makeDelivery('ASSIGNED'), delivererId))
    const { result: inDelivery } = renderHook(() => useAdvanceDelivery(makeDelivery('IN_DELIVERY'), delivererId))
    const { result: pickedUp } = renderHook(() => useAdvanceDelivery(makeDelivery('PICKED_UP'), delivererId))

    expect(assigned.current.label).toBe('Avançar status')
    expect(assigned.current.canAdvance).toBe(true)
    expect(assigned.current.nextLabel).toBe('Aceitar')
    expect(inDelivery.current.nextLabel).toBe('Coletar')
    expect(pickedUp.current.nextLabel).toBe('Entregar')
  })

  it('disables advance for deliveries without a next transition', () => {
    const { result } = renderHook(() => useAdvanceDelivery(makeDelivery('WAITING'), delivererId))

    expect(result.current.canAdvance).toBe(false)
    expect(result.current.nextLabel).toBeNull()
  })

  it('calls accept when advancing from ASSIGNED', async () => {
    const delivery = makeDelivery('ASSIGNED')
    const { result } = renderHook(() => useAdvanceDelivery(delivery, delivererId))

    await act(async () => {
      await result.current.advance()
    })

    expect(acceptDelivery).toHaveBeenCalledWith('order-1', delivererId)
    expect(pickupDelivery).not.toHaveBeenCalled()
    expect(deliverDelivery).not.toHaveBeenCalled()
  })

  it('calls pickup when advancing from IN_DELIVERY', async () => {
    const delivery = makeDelivery('IN_DELIVERY')
    const { result } = renderHook(() => useAdvanceDelivery(delivery, delivererId))

    await act(async () => {
      await result.current.advance()
    })

    expect(pickupDelivery).toHaveBeenCalledWith('order-1', delivererId)
    expect(acceptDelivery).not.toHaveBeenCalled()
    expect(deliverDelivery).not.toHaveBeenCalled()
  })

  it('calls deliver when advancing from PICKED_UP', async () => {
    const delivery = makeDelivery('PICKED_UP')
    const { result } = renderHook(() => useAdvanceDelivery(delivery, delivererId))

    await act(async () => {
      await result.current.advance()
    })

    expect(deliverDelivery).toHaveBeenCalledWith('order-1', delivererId)
    expect(acceptDelivery).not.toHaveBeenCalled()
    expect(pickupDelivery).not.toHaveBeenCalled()
  })

  it('does nothing when delivery is null', async () => {
    const { result } = renderHook(() => useAdvanceDelivery(null, delivererId))

    await act(async () => {
      await result.current.advance()
    })

    expect(acceptDelivery).not.toHaveBeenCalled()
    expect(pickupDelivery).not.toHaveBeenCalled()
    expect(deliverDelivery).not.toHaveBeenCalled()
  })
})
