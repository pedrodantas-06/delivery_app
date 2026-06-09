import { decideOrder, getOrders } from '../api/restaurantApi'
import { requestJson } from '../../../shared/services/http'

jest.mock('../../../shared/services/http', () => ({
  requestJson: jest.fn(),
}))

describe('restaurantApi', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('loads orders for a restaurant', async () => {
    ;(requestJson as jest.Mock).mockResolvedValue([
      { id: 1, id_restaurante: 1, status: 'Pendente', cliente_id: 'c1', valor_total: 25, detalhes: '{}' },
    ])

    const orders = await getOrders('1')

    expect(requestJson).toHaveBeenCalledWith('/api/v1/pedidos?restaurante_id=1')
    expect(orders).toHaveLength(1)
    expect(orders[0]?.status).toBe('Pendente')
  })

  it('posts accept/reject decision to the pedidos endpoint', async () => {
    ;(requestJson as jest.Mock).mockResolvedValue({ mensagem: 'Pedido em preparo com sucesso' })

    await decideOrder(42, 1, 'aceito')

    expect(requestJson).toHaveBeenCalledWith('/api/v1/pedidos/42/decisao', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        id_pedido: 42,
        id_restaurante: 1,
        aceitacao: 'aceito',
      }),
    })
  })
})
