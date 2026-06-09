import Button from '../../../shared/components/Button'
import Card from '../../../shared/components/Card'
import EmptyState from '../../../shared/components/EmptyState'
import type { Delivery, DelivererSession } from '../types'
import ActionButtons from '../components/ActionButtons'
import { useAdvanceDelivery } from '../hooks/useAdvanceDelivery'

type ActiveDeliveryPageProps = {
  session: DelivererSession
  delivery: Delivery | null
  onAccept: (deliveryId: string) => void
  onPickup: (deliveryId: string) => void
  onDeliver: (deliveryId: string) => void
  onAdvanced?: (completed: boolean) => void | Promise<void>
}

function ActiveDeliveryPage({
  session,
  delivery,
  onAccept,
  onPickup,
  onDeliver,
  onAdvanced,
}: ActiveDeliveryPageProps) {
  const { advance, label, canAdvance, nextLabel } = useAdvanceDelivery(delivery, session.id)

  const handleAdvance = async () => {
    if (!delivery || !canAdvance) return
    const completed = delivery.status === 'PICKED_UP'
    await advance()
    if (onAdvanced) {
      await onAdvanced(completed)
      return
    }
    if (completed) {
      await onDeliver(delivery.orderId)
      return
    }
    if (delivery.status === 'ASSIGNED') {
      await onAccept(delivery.orderId)
      return
    }
    await onPickup(delivery.orderId)
  }

  return (
    <section className="grid">
      <Card>
        <div className="section-head">
          <div>
            <h2>Entrega ativa</h2>
            <p>O próximo passo aparece aqui com prioridade máxima.</p>
          </div>
        </div>
        {delivery ? (
          <div className="stack">
            <div className="status-strip">
              <span className="status-chip status-chip--soft">Aceitar</span>
              <span className="status-chip status-chip--soft">Coletar</span>
              <span className="status-chip status-chip--soft">Entregar</span>
            </div>
            <p><strong>Entregador:</strong> {session.name}</p>
            <p><strong>Pedido:</strong> {delivery.orderId}</p>
            <p><strong>Status:</strong> {delivery.status}</p>
            {canAdvance && (
              <Button onClick={() => void handleAdvance()}>
                {label}
                {nextLabel ? ` — ${nextLabel}` : ''}
              </Button>
            )}
            <ActionButtons
              onAccept={() => onAccept(delivery.orderId)}
              onPickup={() => onPickup(delivery.orderId)}
              onDeliver={() => onDeliver(delivery.orderId)}
              acceptDisabled={delivery.status !== 'ASSIGNED'}
              pickupDisabled={delivery.status !== 'IN_DELIVERY'}
              deliverDisabled={delivery.status !== 'PICKED_UP'}
            />
          </div>
        ) : (
          <EmptyState message="Nenhuma entrega ativa no momento." />
        )}
      </Card>
    </section>
  )
}

export default ActiveDeliveryPage
