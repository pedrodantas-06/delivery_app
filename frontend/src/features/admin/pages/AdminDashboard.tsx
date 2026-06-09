import { useEffect, useState } from 'react'
import { useAuth } from '../../../app/providers/AuthProvider'
import Card from '../../../shared/components/Card'
import EmptyState from '../../../shared/components/EmptyState'
import LoadingState from '../../../shared/components/LoadingState'
import MetricCard from '../../../shared/components/MetricCard'
import StatusChip from '../../../shared/components/StatusChip'
import type { Order } from '../../customer/types'
import { getMetrics, getPedidos, type AdminMetrics } from '../api/adminApi'

const METRIC_LABELS: { key: keyof AdminMetrics; label: string }[] = [
  { key: 'total_clientes', label: 'Total Clientes' },
  { key: 'total_restaurantes', label: 'Total Restaurantes' },
  { key: 'total_pedidos', label: 'Total Pedidos' },
  { key: 'total_entregadores', label: 'Total Entregadores' },
]

function AdminDashboard() {
  const { token } = useAuth()
  const [metrics, setMetrics] = useState<AdminMetrics | null>(null)
  const [orders, setOrders] = useState<Order[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!token) {
      setError('Sessão não encontrada.')
      setLoading(false)
      return
    }

    let active = true

    Promise.all([getMetrics(token), getPedidos(token)])
      .then(([metricsData, ordersData]) => {
        if (!active) return
        setMetrics(metricsData)
        setOrders(ordersData)
      })
      .catch(() => {
        if (active) setError('Não foi possível carregar o painel admin.')
      })
      .finally(() => {
        if (active) setLoading(false)
      })

    return () => {
      active = false
    }
  }, [token])

  if (loading) {
    return <LoadingState label="Carregando painel admin..." />
  }

  if (error || !metrics) {
    return <p className="status-message status-message--error">{error ?? 'Dados indisponíveis.'}</p>
  }

  return (
    <section className="grid">
      <header className="section-head">
        <div>
          <h1 className="title">Painel Admin</h1>
          <p>Visão geral read-only da plataforma.</p>
        </div>
      </header>

      <div className="metric-grid">
        {METRIC_LABELS.map(({ key, label }) => (
          <MetricCard key={key} label={label} value={metrics[key]} />
        ))}
      </div>

      <header className="section-head">
        <div>
          <h2 className="title">Pedidos</h2>
          <p>Lista read-only de todos os pedidos.</p>
        </div>
      </header>

      {orders.length === 0 && <EmptyState message="Nenhum pedido registrado." />}

      <div className="stack">
        {orders.map((order) => (
          <Card key={order.id}>
            <div className="delivery-card__head">
              <strong>Pedido #{order.id}</strong>
              <StatusChip status={order.status} />
            </div>
            <p>Restaurante: {order.id_restaurante}</p>
            <p>Cliente: {order.cliente_id}</p>
            <p>R$ {Number(order.valor_total).toFixed(2)}</p>
          </Card>
        ))}
      </div>
    </section>
  )
}

export default AdminDashboard
