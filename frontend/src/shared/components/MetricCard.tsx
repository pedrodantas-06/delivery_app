import type { ReactNode } from 'react'
import Card from './Card'

type MetricCardProps = {
  label: string
  value: ReactNode
  detail?: string
  compact?: boolean
}

function MetricCard({ label, value, detail, compact = false }: MetricCardProps) {
  return (
    <Card className={`metric-card ${compact ? 'metric-card--compact' : ''}`.trim()}>
      <p className="metric-card__label">{label}</p>
      <strong>{value}</strong>
      {detail && <p>{detail}</p>}
    </Card>
  )
}

export default MetricCard
