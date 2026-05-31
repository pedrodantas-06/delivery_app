import Card from '../../../shared/components/Card'
import StatusBadge from './StatusBadge'
import ActionButtons, { type ActionButtonsProps } from './ActionButtons'
import type { Delivery } from '../types'

type DeliveryCardProps = {
  delivery: Delivery
  actions?: ActionButtonsProps
}

function DeliveryCard({ delivery, actions }: DeliveryCardProps) {
  return (
    <Card className="card--subtle">
      <div className="row row--space">
        <div>
          <strong>{delivery.orderId}</strong>
          <p>{delivery.region}</p>
        </div>
        <StatusBadge status={delivery.status} />
      </div>
      <p>Entregador: {delivery.delivererId ?? delivery.assignedDelivererId ?? '—'}</p>
      {delivery.pickedUpAt && <p>Pickup: {delivery.pickedUpAt}</p>}
      {delivery.deliveredAt && <p>Delivered: {delivery.deliveredAt}</p>}
      {actions && <ActionButtons {...actions} />}
    </Card>
  )
}

export default DeliveryCard
