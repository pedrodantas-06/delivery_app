import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { useAuth } from '../../../app/providers/AuthProvider'
import Card from '../../../shared/components/Card'
import Button from '../../../shared/components/Button'
import LoadingState from '../../../shared/components/LoadingState'
import StatusChip from '../../../shared/components/StatusChip'
import { decideOrder, getOrders } from '../api/restaurantApi'
import type { Order } from '../../customer/types'
import { canDecideOrder, parseOrderDetalhes } from '../utils/orderHelpers'

function RestaurantDecisionPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { user } = useAuth()
  const [order, setOrder] = useState<Order | null>(null)
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [message, setMessage] = useState<string | null>(null)

  const restauranteId = user?.referencia_id
  const pedidoId = Number(id)

  useEffect(() => {
    if (!restauranteId || !pedidoId) {
      setError('Pedido ou restaurante não identificado.')
      setLoading(false)
      return
    }

    let active = true

    getOrders(restauranteId)
      .then((orders) => {
        if (!active) return
        const match = orders.find((item) => item.id === pedidoId)
        if (!match) {
          setError('Pedido não encontrado para este restaurante.')
          return
        }
        setOrder(match)
      })
      .catch(() => {
        if (active) setError('Não foi possível carregar o pedido.')
      })
      .finally(() => {
        if (active) setLoading(false)
      })

    return () => {
      active = false
    }
  }, [restauranteId, pedidoId])

  const handleDecision = async (aceitacao: 'aceito' | 'rejeitado') => {
    if (!order || !restauranteId) return

    setSubmitting(true)
    setError(null)
    setMessage(null)

    try {
      const response = await decideOrder(order.id, Number(restauranteId), aceitacao)
      setMessage(response.mensagem)
      setOrder({ ...order, status: aceitacao === 'aceito' ? 'Em preparo' : 'Rejeitado' })
    } catch {
      setError('Não foi possível registrar a decisão.')
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) {
    return <LoadingState label="Carregando pedido..." />
  }

  if (error && !order) {
    return (
      <section className="grid">
        <p className="status-message status-message--error">{error}</p>
        <Link to="/restaurant/orders" className="btn btn--ghost">
          Voltar aos pedidos
        </Link>
      </section>
    )
  }

  if (!order) {
    return null
  }

  const detalhes = parseOrderDetalhes(order.detalhes)
  const itens = Array.isArray(detalhes?.itens) ? detalhes.itens : []
  const endereco = typeof detalhes?.endereco_entrega === 'string' ? detalhes.endereco_entrega : null
  const showDecision = canDecideOrder(order.status)

  return (
    <section className="grid">
      <header className="section-head">
        <div>
          <h1 className="title">Pedido #{order.id}</h1>
          <p>Detalhes e decisão do restaurante.</p>
        </div>
        <Link to="/restaurant/orders" className="btn btn--ghost">
          Voltar aos pedidos
        </Link>
      </header>

      <Card>
        <div className="delivery-card__head">
          <strong>Status atual</strong>
          <StatusChip status={order.status} />
        </div>
        <p>Cliente: {order.cliente_id}</p>
        <p>Total: R$ {Number(order.valor_total).toFixed(2)}</p>
        {endereco && <p>Entrega: {endereco}</p>}

        {itens.length > 0 && (
          <div className="stack">
            <strong>Itens</strong>
            {itens.map((item, index) => {
              const entry = item as { nome?: string; quantidade?: number; preco?: number }
              return (
                <p key={`${entry.nome ?? 'item'}-${index}`}>
                  {entry.quantidade ?? 1}x {entry.nome ?? 'Item'} — R$ {Number(entry.preco ?? 0).toFixed(2)}
                </p>
              )
            })}
          </div>
        )}
      </Card>

      {message && <p className="status-message status-message--success">{message}</p>}
      {error && <p className="status-message status-message--error">{error}</p>}

      {showDecision && (
        <div className="actions actions--stacked">
          <Button disabled={submitting} onClick={() => handleDecision('aceito')}>
            Aceitar
          </Button>
          <Button variant="secondary" disabled={submitting} onClick={() => handleDecision('rejeitado')}>
            Rejeitar
          </Button>
        </div>
      )}

      {!showDecision && (
        <Button variant="ghost" onClick={() => navigate('/restaurant/orders')}>
          Voltar para lista
        </Button>
      )}
    </section>
  )
}

export default RestaurantDecisionPage
