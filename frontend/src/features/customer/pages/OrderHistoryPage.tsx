import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../../app/providers/AuthProvider'
import { getOrders } from '../api/customerApi'
import type { Order } from '../types'
import StatusChip from '../components/StatusChip'
import Card from '../../../shared/components/Card'
import Button from '../../../shared/components/Button'
import Loading from '../../../shared/components/Loading'
import EmptyState from '../../../shared/components/EmptyState'

function OrderHistoryPage() {
  const navigate = useNavigate()
  const { user } = useAuth()
  const [orders, setOrders] = useState<Order[]>([])
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

    getOrders(clienteId)
      .then((data) => {
        if (active) setOrders(data)
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
  }, [clienteId])

  if (loading) {
    return <Loading label="Carregando pedidos..." />
  }

  if (error) {
    return <p className="status-message status-message--error">{error}</p>
  }

  if (orders.length === 0) {
    return <EmptyState message="Você ainda não fez pedidos." />
  }

  return (
    <section className="customer-section">
      <header className="section-head">
        <h1 className="title">Meus pedidos</h1>
        <p>Histórico completo de pedidos no campus.</p>
      </header>

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
    </section>
  )
}

export default OrderHistoryPage
