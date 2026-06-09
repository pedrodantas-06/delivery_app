import { render, screen } from '@testing-library/react'
import DashboardPage from '../pages/DashboardPage'
import type { Deliverer, DelivererSession } from '../types'

describe('DashboardPage', () => {
  it('renders the operational summary cards', () => {
    const session: DelivererSession = {
      id: 'deliverer-1',
      name: 'Ana',
      phone: '11999999999',
      region: 'Zona Sul',
    }

    const deliverers: Deliverer[] = []

    render(
      <DashboardPage
        session={session}
        region="Zona Sul"
        loading={false}
        deliveries={[]}
        deliverers={deliverers}
        onRefresh={() => {}}
        onAccept={() => {}}
        onAssign={() => {}}
        onStatusChange={() => {}}
      />,
    )

    expect(screen.getByText('Sessão ativa')).toBeInTheDocument()
    expect(screen.getByText('Disponíveis', { selector: '.metric-card__label' })).toBeInTheDocument()
    expect(screen.getByText('Entregadores livres')).toBeInTheDocument()
    expect(screen.getByText('Aguardando atualização')).toBeInTheDocument()
  })
})
