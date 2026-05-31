import Badge from '../../../shared/components/Badge'
import type { DelivererStatus, DeliveryStatus } from '../types'

function mapBadgeStatus(status: DelivererStatus | DeliveryStatus) {
  if (status === 'ASSIGNED' || status === 'IN_DELIVERY' || status === 'PICKED_UP') {
    return 'BUSY'
  }
  if (status === 'DELIVERED') {
    return 'AVAILABLE'
  }
  if (status === 'CANCELLED') {
    return 'OFFLINE'
  }
  return status === 'BUSY' ? 'BUSY' : status === 'OCCUPIED' ? 'OCCUPIED' : 'AVAILABLE'
}

function StatusBadge({ status }: { status: DelivererStatus | DeliveryStatus }) {
  return <Badge status={mapBadgeStatus(status)} />
}

export default StatusBadge
export { mapBadgeStatus }
