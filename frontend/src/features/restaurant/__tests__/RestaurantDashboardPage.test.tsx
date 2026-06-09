import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import RestaurantDashboardPage from '../pages/RestaurantDashboardPage'
import type { Order } from '../../customer/types'

jest.mock('../../../app/providers/AuthProvider', () => ({
  useAuth: () => ({
    user: { id: 2, nome: 'Burger House', email: 'burger@burgerhouse.com', role: 'RESTAURANTE', referencia_id: '1' },
    token: 'token',
    login: jest.fn(),
    logout: jest.fn(),
  }),
}))

jest.mock('../api/restaurantApi', () => ({
  getOrders: jest.fn(),
}))

import { getOrders } from '../api/restaurantApi'

describe('RestaurantDashboardPage', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('renders metric cards grouped by order status', async () => {
    const orders: Order[] = [
      { id: 1, id_restaurante: 1, status: 'Pendente', cliente_id: 'c1', valor_total: 10, detalhes: '{}' },
      { id: 2, id_restaurante: 1, status: 'Pago', cliente_id: 'c2', valor_total: 20, detalhes: '{}' },
      { id: 3, id_restaurante: 1, status: 'Em preparo', cliente_id: 'c3', valor_total: 30, detalhes: '{}' },
      { id: 4, id_restaurante: 1, status: 'Finalizado', cliente_id: 'c4', valor_total: 40, detalhes: '{}' },
    ]
    ;(getOrders as jest.Mock).mockResolvedValue(orders)

    render(
      <MemoryRouter>
        <RestaurantDashboardPage />
      </MemoryRouter>,
    )

    expect(await screen.findByText('Pendente', { selector: '.metric-card__label' })).toBeInTheDocument()
    expect(screen.getByText('Em preparo', { selector: '.metric-card__label' })).toBeInTheDocument()
    expect(screen.getByText('Finalizado', { selector: '.metric-card__label' })).toBeInTheDocument()
    expect(screen.getByText('Pago', { selector: '.metric-card__label' })).toBeInTheDocument()
    expect(screen.getAllByText('1').length).toBeGreaterThanOrEqual(4)
  })
})
