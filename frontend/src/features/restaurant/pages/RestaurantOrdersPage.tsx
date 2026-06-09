import { useEffect, useMemo, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../../../app/providers/AuthProvider'
import Card from '../../../shared/components/Card'
import Button from '../../../shared/components/Button'
import EmptyState from '../../../shared/components/EmptyState'
import LoadingState from '../../../shared/components/LoadingState'
import StatusChip from '../../../shared/components/StatusChip'
import { getOrders } from '../api/restaurantApi'
import type { Order } from '../../customer/types'
import { filterOrdersByStatus, ORDER_FILTER_STATUSES, type OrderFilterStatus } from '../utils/orderHelpers'

function RestaurantOrdersPage() {
  const navigate = useNavigate()
  const { user } = useAuth()
  const [orders, setOrders] = useState<Order[]>([])
  const [filter, setFilter] = useState<OrderFilterStatus>('Todos')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const restauranteId = user?.referencia_id

  useEffect(() => {
    if (!restauranteId) {
      setError('Restaurante não identificado.')
      setLoading(false)
      return
    }

    let active = true

    getOrders(restauranteId)
      .then((data) => {
        if (active) setOrders(data)
      })
      .catch(() => {
        if (active) setError('Não foi possível carregar os pedidos.')
      })
      .finally(() => {
        if (active) setLoading(false)
      })

    return () => {
      active = false
    }
  }, [restauranteId])

  const filteredOrders = useMemo(() => filterOrdersByStatus(orders, filter), [orders, filter])

  if (loading) {
    return <LoadingState label="Carregando pedidos..." />
  }

  if (error) {
    return <p className="status-message status-message--error">{error}</p>
  }

  return (
    <section className="grid">
      <header className="section-head">
        <div>
          <h1 className="title">Pedidos</h1>
          <p>Lista de pedidos recebidos pelo restaurante.</p>
        </div>
        <Link to="/restaurant" className="btn btn--ghost">
          Voltar ao painel
        </Link>
      </header>

      <div className="actions actions--stacked">
        {ORDER_FILTER_STATUSES.map((status) => (
          <Button
            key={status}
            variant={filter === status ? 'primary' : 'ghost'}
            onClick={() => setFilter(status)}
          >
            {status}
          </Button>
        ))}
      </div>

      {filteredOrders.length === 0 && (
        <EmptyState message={filter === 'Todos' ? 'Nenhum pedido encontrado.' : `Nenhum pedido com status ${filter}.`} />
      )}

      <div className="stack">
        {filteredOrders.map((order) => (
          <Card key={order.id}>
            <div className="delivery-card__head">
              <strong>Pedido #{order.id}</strong>
              <StatusChip status={order.status} />
            </div>
            <p>Cliente: {order.cliente_id}</p>
            <p>R$ {Number(order.valor_total).toFixed(2)}</p>
            <Button variant="ghost" onClick={() => navigate(`/restaurant/orders/${order.id}`)}>
              Ver detalhes
            </Button>
          </Card>
        ))}
      </div>
    </section>
  )
}

export default RestaurantOrdersPage
