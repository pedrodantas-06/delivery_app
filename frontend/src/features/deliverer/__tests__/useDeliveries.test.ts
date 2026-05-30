import { act, renderHook, waitFor } from '@testing-library/react'
import { useDeliveries } from '../hooks/useDeliveries'
import { getDeliverers } from '../api/delivererApi'
import { assignDelivery, getDeliveries } from '../api/deliveryApi'

jest.mock('../api/delivererApi', () => ({
  getDeliverers: jest.fn(),
  createDeliverer: jest.fn(),
  updateDelivererStatus: jest.fn(),
}))

jest.mock('../api/deliveryApi', () => ({
  getDeliveries: jest.fn(),
  assignDelivery: jest.fn(),
  acceptDelivery: jest.fn(),
  pickupDelivery: jest.fn(),
  deliverDelivery: jest.fn(),
}))

describe('useDeliveries', () => {
  beforeEach(() => {
    jest.clearAllMocks()
    ;(getDeliverers as jest.Mock).mockResolvedValue([
      { id: 'deliverer-1', name: 'Ana', phone: '11999999999', region: 'Zona Sul', status: 'AVAILABLE' },
    ])
    ;(getDeliveries as jest.Mock).mockResolvedValue([
      { orderId: 'order-1', region: 'Zona Sul', status: 'WAITING', delivererId: null },
      { orderId: 'order-2', region: 'Zona Sul', status: 'DELIVERED', delivererId: 'deliverer-1' },
    ])
  })

  it('loads deliveries and exposes available deliveries', async () => {
    const { result } = renderHook(() => useDeliveries('Zona Sul'))

    await waitFor(() => {
      expect(result.current.deliverers).toHaveLength(1)
    })

    expect(getDeliverers).toHaveBeenCalledWith('Zona Sul')
    expect(getDeliveries).toHaveBeenCalledWith('Zona Sul')
    expect(result.current.availableDeliveries).toHaveLength(1)
    expect(result.current.availableDeliveries[0]?.orderId).toBe('order-1')
  })

  it('forwards action calls to the delivery api', async () => {
    const { result } = renderHook(() => useDeliveries('Zona Sul'))

    await waitFor(() => {
      expect(result.current.deliveries).toHaveLength(2)
    })

    await act(async () => {
      await result.current.assign('order-3', 'Zona Sul', 'deliverer-1')
    })

    expect(assignDelivery).toHaveBeenCalledWith('order-3', 'Zona Sul', 'deliverer-1')
  })
})
