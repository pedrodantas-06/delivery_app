import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { useAuth } from '../../../app/providers/AuthProvider'
import { getOrders } from '../api/customerApi'
import type { Order } from '../types'
import StatusChip from '../components/StatusChip'
import Card from '../../../shared/components/Card'
import Loading from '../../../shared/components/Loading'
import EmptyState from '../../../shared/components/EmptyState'

const POLL_INTERVAL_MS = 10_000

function OrderTrackingPage() {
  const { orderId } = useParams()
  const { user } = useAuth()
  const [order, setOrder] = useState<Order | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const clienteId = user?.referencia_id
  const parsedOrderId = Number(orderId)

  useEffect(() => {
    if (!clienteId || !parsedOrderId) {
      setError('Pedido inválido.')
      setLoading(false)
      return
    }

    let active = true

    const loadOrder = async () => {
      try {
        const orders = await getOrders(clienteId)
        if (!active) return
        const current = orders.find((entry) => entry.id === parsedOrderId) ?? null
        setOrder(current)
        setError(current ? null : 'Pedido não encontrado.')
      } catch {
        if (active) setError('Não foi possível atualizar o status do pedido.')
      } finally {
        if (active) setLoading(false)
      }
    }

    loadOrder()
    const intervalId = window.setInterval(loadOrder, POLL_INTERVAL_MS)

    return () => {
      active = false
      window.clearInterval(intervalId)
    }
  }, [clienteId, parsedOrderId])

  if (loading) {
    return <Loading label="Carregando acompanhamento..." />
  }

  if (error || !order) {
    return <EmptyState message={error ?? 'Pedido não encontrado.'} />
  }

  return (
    <section className="customer-section">
      <header className="section-head">
        <h1 className="title">Acompanhar pedido</h1>
        <p>Pedido #{order.id}</p>
      </header>

      <Card>
        <div className="delivery-card__head">
          <strong>Status atual</strong>
          <StatusChip status={order.status} />
        </div>
        <p>Valor total: R$ {Number(order.valor_total).toFixed(2)}</p>
        <p className="status-message">Atualização automática a cada 10 segundos.</p>
      </Card>
    </section>
  )
}

export default OrderTrackingPage
