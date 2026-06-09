import Button from '../../../shared/components/Button'
import Card from '../../../shared/components/Card'
import EmptyState from '../../../shared/components/EmptyState'
import Loading from '../../../shared/components/Loading'
import MetricCard from '../../../shared/components/MetricCard'
import type { Delivery, Deliverer, DelivererSession } from '../types'
import DeliveryCard from '../components/DeliveryCard'
import StatusBadge from '../components/StatusBadge'
import { useAdvanceDelivery } from '../hooks/useAdvanceDelivery'

type DashboardPageProps = {
  session: DelivererSession
  region: string
  loading: boolean
  refreshedAt?: string | null
  deliveries: Delivery[]
  deliverers: Deliverer[]
  onRefresh: () => void
  onAccept: (deliveryId: string) => void
  onAssign: (deliveryId: string, delivererId?: string) => void
  onStatusChange: (status: Deliverer['status']) => void
  onAdvanceStatus?: (delivery: Delivery) => void | Promise<void>
}

type AdvanceStatusShortcutProps = {
  delivery: Delivery
  delivererId: string
  onDone: () => void | Promise<void>
}

function AdvanceStatusShortcut({ delivery, delivererId, onDone }: AdvanceStatusShortcutProps) {
  const { advance, label, canAdvance, nextLabel } = useAdvanceDelivery(delivery, delivererId)

  if (!canAdvance) {
    return null
  }

  return (
    <Button onClick={() => void (async () => {
      await advance()
      await onDone()
    })()}>
      {label}
      {nextLabel ? ` — ${nextLabel}` : ''}
    </Button>
  )
}

function DashboardPage({
  session,
  region,
  loading,
  refreshedAt,
  deliveries,
  deliverers,
  onRefresh,
  onAccept,
  onAssign,
  onStatusChange,
  onAdvanceStatus,
}: DashboardPageProps) {
  const availableDeliveries = deliveries.filter((delivery) => delivery.status === 'WAITING' || delivery.status === 'ASSIGNED')
  const activeDeliveries = deliveries.filter((delivery) => delivery.status === 'IN_DELIVERY' || delivery.status === 'PICKED_UP')
  const availableDeliverers = deliverers.filter((deliverer) => deliverer.status === 'AVAILABLE')
  const busyDeliverers = deliverers.filter((deliverer) => deliverer.status === 'BUSY' || deliverer.status === 'OCCUPIED')
  const completedDeliveries = deliveries.filter((delivery) => delivery.status === 'DELIVERED')
  const freshnessLabel = refreshedAt ? `Atualizado às ${new Date(refreshedAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}` : 'Aguardando atualização'

  return (
    <section className="grid">
      <div className="metric-grid">
        <MetricCard label="Sessão ativa" value={session.name} detail={session.region} />
        <MetricCard label="Disponíveis" value={availableDeliveries.length} detail="Entregas prontas para agir" />
        <MetricCard
          label="Em rota"
          value={activeDeliveries.length}
          detail={`${completedDeliveries.length} concluídas na lista`}
        />
        <MetricCard
          label="Entregadores livres"
          value={availableDeliverers.length}
          detail={`${busyDeliverers.length} ocupados`}
        />
      </div>

      <Card>
        <div className="section-head">
          <div>
            <h2>Disponíveis agora</h2>
            <p>Entregas prontas para atribuição ou aceitação.</p>
          </div>
          <div className="section-head__meta">
            <span className="status-chip status-chip--soft">{freshnessLabel}</span>
            <Button variant="ghost" onClick={onRefresh}>Atualizar</Button>
          </div>
        </div>
        {loading && <Loading />}
        {!loading && availableDeliveries.length === 0 && <EmptyState message="Nenhuma entrega disponível para esta região." />}
        <div className="stack">
          {availableDeliveries.map((delivery) => (
            <div key={delivery.orderId} className="stack">
              <DeliveryCard
                delivery={delivery}
                actions={{
                  onAccept: () => onAccept(delivery.orderId),
                  onAssign: () => onAssign(delivery.orderId, session.id),
                }}
              />
              {delivery.status === 'ASSIGNED' && onAdvanceStatus && (
                <AdvanceStatusShortcut
                  delivery={delivery}
                  delivererId={session.id}
                  onDone={() => onAdvanceStatus(delivery)}
                />
              )}
            </div>
          ))}
        </div>
      </Card>

      <Card>
        <div className="section-head">
          <div>
            <h2>Disponibilidade</h2>
            <p>Controle simples de presença e carga operacional.</p>
          </div>
        </div>
        <div className="actions actions--stacked">
          <Button onClick={() => onStatusChange('AVAILABLE')}>AVAILABLE</Button>
          <Button variant="secondary" onClick={() => onStatusChange('BUSY')}>BUSY</Button>
          <Button variant="ghost" onClick={() => onStatusChange('OFFLINE')}>OFFLINE</Button>
        </div>
        <div className="section-head section-head--spaced">
          <div>
            <h2>Entregadores na região</h2>
            <p>{region}</p>
          </div>
        </div>
        <div className="stack">
          {deliverers.map((deliverer) => (
            <Card key={deliverer.id} className="card--subtle">
              <div className="row row--space">
                <div>
                  <strong>{deliverer.name}</strong>
                  <p>{deliverer.phone}</p>
                </div>
                <StatusBadge status={deliverer.status} />
              </div>
            </Card>
          ))}
        </div>
      </Card>
    </section>
  )
}

export default DashboardPage
