import Button from '../../../shared/components/Button'
import Card from '../../../shared/components/Card'
import MetricCard from '../../../shared/components/MetricCard'
import type { DelivererSession } from '../types'

function ProfileCard({
  session,
  onLogout,
  onUseProfileRegion,
}: {
  session: DelivererSession
  onLogout: () => void
  onUseProfileRegion: () => void
}) {
  return (
    <Card>
      <div className="section-head">
        <div>
          <h2>Perfil</h2>
          <p>Dados básicos da conta e região ativa.</p>
        </div>
      </div>
      <div className="metric-grid metric-grid--compact">
        <MetricCard compact label="Nome" value={session.name} />
        <MetricCard compact label="Região" value={session.region} />
      </div>
      <div className="stack">
        <p><strong>ID:</strong> {session.id}</p>
        <p><strong>Nome:</strong> {session.name}</p>
        <p><strong>Telefone:</strong> {session.phone}</p>
        <p><strong>Região:</strong> {session.region}</p>
        <div className="actions">
          <Button variant="secondary" onClick={onLogout}>Sair</Button>
          <Button variant="ghost" onClick={onUseProfileRegion}>Usar região do perfil</Button>
        </div>
      </div>
    </Card>
  )
}

export default ProfileCard
