import Card from '../../../shared/components/Card'
import EmptyState from '../../../shared/components/EmptyState'
import type { Delivery } from '../types'
import HistoryList from '../components/HistoryList'

type HistoryPageProps = {
  deliveries: Delivery[]
}

function HistoryPage({ deliveries }: HistoryPageProps) {
  const deliveredCount = deliveries.filter((delivery) => delivery.status === 'DELIVERED').length
  const inProgressCount = deliveries.filter((delivery) => delivery.status === 'IN_DELIVERY' || delivery.status === 'PICKED_UP').length

  return (
    <section className="grid">
      <Card>
        <div className="section-head">
          <div>
            <h2>Histórico</h2>
            <p>Últimas entregas concluídas ou em andamento.</p>
          </div>
        </div>
        <div className="status-strip">
          <span className="status-chip status-chip--soft">Concluídas {deliveredCount}</span>
          <span className="status-chip status-chip--soft">Em rota {inProgressCount}</span>
          <span className="status-chip status-chip--soft">Total {deliveries.length}</span>
        </div>
        {deliveries.length === 0 ? <EmptyState message="Nenhuma entrega registrada." /> : <HistoryList deliveries={deliveries} />}
      </Card>
    </section>
  )
}

export default HistoryPage
