import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../../../app/providers/AuthProvider'
import EmptyState from '../../../shared/components/EmptyState'
import LoadingState from '../../../shared/components/LoadingState'
import MetricCard from '../../../shared/components/MetricCard'
import { getOrders } from '../api/restaurantApi'
import type { Order } from '../../customer/types'
import { countByStatus, RESTAURANT_METRIC_STATUSES } from '../utils/orderHelpers'

function RestaurantDashboardPage() {
  const { user } = useAuth()
  const [orders, setOrders] = useState<Order[]>([])
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

  if (loading) {
    return <LoadingState label="Carregando painel..." />
  }

  if (error) {
    return <p className="status-message status-message--error">{error}</p>
  }

  return (
    <section className="grid">
      <header className="section-head">
        <div>
          <h1 className="title">Painel do restaurante</h1>
          <p>Resumo dos pedidos de {user?.nome ?? 'seu restaurante'}.</p>
        </div>
        <Link to="/restaurant/orders" className="btn btn--ghost">
          Ver pedidos
        </Link>
      </header>

      <div className="metric-grid">
        {RESTAURANT_METRIC_STATUSES.map((status) => (
          <MetricCard
            key={status}
            label={status}
            value={countByStatus(orders, status)}
            detail="pedidos neste status"
          />
        ))}
      </div>

      {orders.length === 0 && <EmptyState message="Nenhum pedido recebido ainda." />}
    </section>
  )
}

export default RestaurantDashboardPage
