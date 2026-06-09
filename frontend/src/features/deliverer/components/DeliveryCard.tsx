import Card from '../../../shared/components/Card'
import StatusBadge from './StatusBadge'
import ActionButtons, { type ActionButtonsProps } from './ActionButtons'
import type { Delivery } from '../types'

type DeliveryCardProps = {
  delivery: Delivery
  actions?: ActionButtonsProps
}

function DeliveryCard({ delivery, actions }: DeliveryCardProps) {
  const timelineLabel = delivery.deliveredAt
    ? 'Concluída'
    : delivery.pickedUpAt
      ? 'Em rota'
      : delivery.assignedAt
        ? 'Atribuída'
        : 'Aguardando'

  return (
    <Card className="card--subtle">
      <div className="delivery-card__head">
        <div className="delivery-card__title">
          <strong>{delivery.orderId}</strong>
          <p>{delivery.region}</p>
        </div>
        <StatusBadge status={delivery.status} />
      </div>

      <div className="status-strip delivery-card__chips">
        <span className="status-chip status-chip--soft">{timelineLabel}</span>
        <span className="status-chip status-chip--soft">Região {delivery.region}</span>
      </div>

      <div className="delivery-card__details">
        <p><strong>Entregador:</strong> {delivery.delivererId ?? delivery.assignedDelivererId ?? '—'}</p>
        <p><strong>Atribuído:</strong> {delivery.assignedAt ?? '—'}</p>
        <p><strong>Pickup:</strong> {delivery.pickedUpAt ?? '—'}</p>
        <p><strong>Entrega:</strong> {delivery.deliveredAt ?? '—'}</p>
      </div>

      {actions && <ActionButtons {...actions} />}
    </Card>
  )
}

export default DeliveryCard
