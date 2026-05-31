import Button from '../../../shared/components/Button'

export type ActionButtonsProps = {
  onAccept?: () => void
  onAssign?: () => void
  onPickup?: () => void
  onDeliver?: () => void
  acceptDisabled?: boolean
  assignDisabled?: boolean
  pickupDisabled?: boolean
  deliverDisabled?: boolean
}

function ActionButtons({
  onAccept,
  onAssign,
  onPickup,
  onDeliver,
  acceptDisabled = false,
  assignDisabled = false,
  pickupDisabled = false,
  deliverDisabled = false,
}: ActionButtonsProps) {
  return (
    <div className="actions">
      {onAccept && (
        <Button variant="secondary" disabled={acceptDisabled} onClick={onAccept}>
          Aceitar
        </Button>
      )}
      {onAssign && (
        <Button variant="secondary" disabled={assignDisabled} onClick={onAssign}>
          Atribuir a mim
        </Button>
      )}
      {onPickup && (
        <Button variant="secondary" disabled={pickupDisabled} onClick={onPickup}>
          Pickup
        </Button>
      )}
      {onDeliver && (
        <Button disabled={deliverDisabled} onClick={onDeliver}>
          Deliver
        </Button>
      )}
    </div>
  )
}

export default ActionButtons
