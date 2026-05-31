import { render, screen } from '@testing-library/react'
import HistoryList from '../components/HistoryList'
import type { Delivery } from '../types'

const deliveries: Delivery[] = [
  {
    orderId: 'order-1',
    region: 'Zona Sul',
    status: 'DELIVERED',
    delivererId: 'deliverer-1',
    assignedDelivererId: 'deliverer-1',
    pickedUpAt: '2024-01-01T10:00:00.000Z',
    deliveredAt: '2024-01-01T11:00:00.000Z',
  },
]

describe('HistoryList', () => {
  it('renders an empty state when there are no deliveries', () => {
    render(<HistoryList deliveries={[]} />)

    expect(screen.getByText('Nenhuma entrega encontrada.')).toBeInTheDocument()
  })

  it('renders delivery history cards', () => {
    render(<HistoryList deliveries={deliveries} />)

    expect(screen.getByText('order-1')).toBeInTheDocument()
    expect(screen.getByText('AVAILABLE')).toBeInTheDocument()
  })
})
