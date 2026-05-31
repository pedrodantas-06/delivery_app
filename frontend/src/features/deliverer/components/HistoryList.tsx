import EmptyState from '../../../shared/components/EmptyState'
import type { Delivery } from '../types'
import DeliveryCard from './DeliveryCard'

function HistoryList({ deliveries }: { deliveries: Delivery[] }) {
  if (deliveries.length === 0) {
    return <EmptyState message="Nenhuma entrega encontrada." />
  }

  return (
    <div className="stack">
      {deliveries.map((delivery) => (
        <DeliveryCard key={delivery.orderId} delivery={delivery} />
      ))}
    </div>
  )
}

export default HistoryList
