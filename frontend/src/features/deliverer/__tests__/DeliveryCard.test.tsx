import { render, screen } from '@testing-library/react'
import DeliveryCard from '../components/DeliveryCard'
import type { Delivery } from '../types'

const delivery: Delivery = {
  orderId: 'order-123',
  region: 'Zona Sul',
  status: 'PICKED_UP',
  delivererId: 'deliverer-1',
  assignedDelivererId: 'deliverer-1',
  pickedUpAt: '2024-01-01T10:00:00.000Z',
  deliveredAt: null,
}

describe('DeliveryCard', () => {
  it('renders delivery details and actions', () => {
    render(
      <DeliveryCard
        delivery={delivery}
        actions={{
          onPickup: () => {},
          onDeliver: () => {},
        }}
      />,
    )

    expect(screen.getByText('order-123')).toBeInTheDocument()
    expect(screen.getByText('Zona Sul')).toBeInTheDocument()
    expect(screen.getByText('deliverer-1')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Pickup' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Deliver' })).toBeInTheDocument()
  })
})
