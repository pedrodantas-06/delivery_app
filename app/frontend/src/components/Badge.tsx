type BadgeStatus = 'AVAILABLE' | 'OCCUPIED' | 'OFFLINE'

type BadgeProps = {
  status: BadgeStatus
}

function Badge({ status }: BadgeProps) {
  const className = `badge badge--${status.toLowerCase()}`
  return <span className={className}>{status}</span>
}

export default Badge
