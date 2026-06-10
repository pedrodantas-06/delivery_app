import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../../app/providers/AuthProvider'
import { getOrders, getOrderStats } from '../api/customerApi'
import type { Order, OrderStats } from '../types'
import StatusChip from '../../../shared/components/StatusChip'
import Card from '../../../shared/components/Card'
import Button from '../../../shared/components/Button'
import Loading from '../../../shared/components/Loading'
import EmptyState from '../../../shared/components/EmptyState'
import MetricCard from '../../../shared/components/MetricCard'

function OrderHistoryPage() {
  const navigate = useNavigate()
  const { user, token } = useAuth()
  const [orders, setOrders] = useState<Order[]>([])
  const [stats, setStats] = useState<OrderStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const clienteId = user?.referencia_id

  useEffect(() => {
    if (!clienteId) {
      setError('Cliente não identificado.')
      setLoading(false)
      return
    }

    let active = true

    Promise.all([getOrders(clienteId), getOrderStats(token).catch(() => null)])
      .then(([pedidos, estatisticas]) => {
        if (!active) return
        setOrders(pedidos)
        setStats(estatisticas)
      })
      .catch(() => {
        if (active) setError('Não foi possível carregar o histórico.')
      })
      .finally(() => {
        if (active) setLoading(false)
      })

    return () => {
      active = false
    }
  }, [clienteId, token])

  if (loading) {
    return <Loading label="Carregando pedidos..." />
  }

  if (error) {
    return <p className="status-message status-message--error">{error}</p>
  }

  return (
    <section className="customer-section">
      <header className="section-head">
        <h1 className="title">Meus pedidos</h1>
        <p>Histórico completo de pedidos no campus.</p>
      </header>

      {stats && (
        <div className="metric-grid metric-grid--compact">
          <MetricCard label="Total de pedidos" value={stats.total} compact />
          <MetricCard label="Pedidos no mês" value={stats.no_mes} compact />
          <MetricCard
            label="Preço médio"
            value={`R$ ${Number(stats.preco_medio).toFixed(2)}`}
            compact
          />
        </div>
      )}

      {orders.length === 0 ? (
        <EmptyState message="Você ainda não fez pedidos." />
      ) : (
        <div className="grid">
          {orders.map((order) => (
            <Card key={order.id}>
              <div className="delivery-card__head">
                <strong>Pedido #{order.id}</strong>
                <StatusChip status={order.status} />
              </div>
              <p>Restaurante #{order.id_restaurante}</p>
              <p>R$ {Number(order.valor_total).toFixed(2)}</p>
              <Button variant="ghost" onClick={() => navigate(`/customer/tracking/${order.id}`)}>
                Acompanhar
              </Button>
            </Card>
          ))}
        </div>
      )}
    </section>
  )
}

export default OrderHistoryPage
