type StatusChipProps = {
  status: string
}

function statusClass(status: string) {
  const normalized = status.toLowerCase()
  if (['pago', 'em preparo', 'em entrega', 'finalizado'].includes(normalized)) {
    return 'status-chip status-chip--live'
  }
  return 'status-chip status-chip--soft'
}

function StatusChip({ status }: StatusChipProps) {
  return <span className={statusClass(status)}>{status}</span>
}

export default StatusChip
