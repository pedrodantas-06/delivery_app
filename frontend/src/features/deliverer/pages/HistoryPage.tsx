import Card from '../../../shared/components/Card'
import EmptyState from '../../../shared/components/EmptyState'
import type { Delivery } from '../types'
import HistoryList from '../components/HistoryList'

type HistoryPageProps = {
  deliveries: Delivery[]
}

function HistoryPage({ deliveries }: HistoryPageProps) {
  return (
    <section className="grid">
      <Card>
        <div className="section-head">
          <div>
            <h2>Delivery History</h2>
            <p>Últimas entregas concluídas ou em andamento.</p>
          </div>
        </div>
        {deliveries.length === 0 ? <EmptyState message="Nenhuma entrega registrada." /> : <HistoryList deliveries={deliveries} />}
      </Card>
    </section>
  )
}

export default HistoryPage
