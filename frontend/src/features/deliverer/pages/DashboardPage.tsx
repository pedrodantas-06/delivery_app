import Button from '../../../shared/components/Button'
import Card from '../../../shared/components/Card'
import EmptyState from '../../../shared/components/EmptyState'
import Loading from '../../../shared/components/Loading'
import type { Delivery, Deliverer, DelivererSession } from '../types'
import ActionButtons from '../components/ActionButtons'
import DeliveryCard from '../components/DeliveryCard'
import StatusBadge from '../components/StatusBadge'

type DashboardPageProps = {
  session: DelivererSession
  region: string
  loading: boolean
  deliveries: Delivery[]
  deliverers: Deliverer[]
  onRefresh: () => void
  onAccept: (deliveryId: string) => void
  onAssign: (deliveryId: string, delivererId?: string) => void
  onStatusChange: (status: Deliverer['status']) => void
}

function DashboardPage({
  session,
  region,
  loading,
  deliveries,
  deliverers,
  onRefresh,
  onAccept,
  onAssign,
  onStatusChange,
}: DashboardPageProps) {
  const availableDeliveries = deliveries.filter((delivery) => delivery.status === 'WAITING' || delivery.status === 'ASSIGNED')

  return (
    <section className="grid">
      <Card>
        <div className="section-head">
          <div>
            <h2>Disponíveis</h2>
            <p>Entregas prontas para atribuição ou aceitação.</p>
          </div>
          <Button variant="ghost" onClick={onRefresh}>Atualizar</Button>
        </div>
        {loading && <Loading />}
        {!loading && availableDeliveries.length === 0 && <EmptyState message="Nenhuma entrega disponível para esta região." />}
        <div className="stack">
          {availableDeliveries.map((delivery) => (
            <DeliveryCard
              key={delivery.orderId}
              delivery={delivery}
              actions={{
                onAccept: () => onAccept(delivery.orderId),
                onAssign: () => onAssign(delivery.orderId, session.id),
              }}
            />
          ))}
        </div>
      </Card>

      <Card>
        <div className="section-head">
          <div>
            <h2>Disponibilidade</h2>
            <p>Controle simples de presença e carga.</p>
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
