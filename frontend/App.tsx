import { useEffect, useMemo, useState, type FormEvent } from 'react'
import Badge from './src/componentes/Badge'
import Button from './src/componentes/Button'
import Card from './src/componentes/Card'

type DelivererStatus = 'AVAILABLE' | 'BUSY' | 'OCCUPIED' | 'OFFLINE'
type DeliveryStatus = 'WAITING' | 'ASSIGNED' | 'IN_DELIVERY' | 'PICKED_UP' | 'DELIVERED' | 'CANCELLED'

type Deliverer = {
  id: string
  name: string
  phone: string
  region: string
  status: DelivererStatus
}

type Delivery = {
  order_id: string
  region: string
  status: DeliveryStatus
  deliverer_id: string | null
  assigned_deliverer_id?: string | null
  picked_up_at?: string | null
  delivered_at?: string | null
}

type DeliverersResponse = {
  items: Deliverer[]
}

type DeliveriesResponse = {
  items: Delivery[]
}

type TabKey = 'dashboard' | 'active' | 'history' | 'profile'

type Session = {
  id: string
  name: string
  phone: string
  region: string
}

const STORAGE_KEY = 'deliverer-session'

function App() {
  const [session, setSession] = useState<Session | null>(() => {
    const raw = window.localStorage.getItem(STORAGE_KEY)
    return raw ? (JSON.parse(raw) as Session) : null
  })
  const [tab, setTab] = useState<TabKey>('dashboard')
  const [loginName, setLoginName] = useState('Ana')
  const [loginPhone, setLoginPhone] = useState('11999999999')
  const [loginRegion, setLoginRegion] = useState('Zona Sul')
  const [deliverers, setDeliverers] = useState<Deliverer[]>([])
  const [deliveries, setDeliveries] = useState<Delivery[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [filterRegion, setFilterRegion] = useState('Zona Sul')

  useEffect(() => {
    if (session) {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(session))
    } else {
      window.localStorage.removeItem(STORAGE_KEY)
    }
  }, [session])

  useEffect(() => {
    let active = true

    const load = async () => {
      setLoading(true)
      setError('')
      try {
        const [deliverersResponse, deliveriesResponse] = await Promise.all([
          fetch(`/api/v1/deliverers/?region=${encodeURIComponent(filterRegion)}`),
          fetch(`/api/v1/orders/?region=${encodeURIComponent(filterRegion)}`),
        ])

        if (!deliverersResponse.ok || !deliveriesResponse.ok) {
          throw new Error('Falha ao carregar dados do entregador')
        }

        const deliverersJson: DeliverersResponse = await deliverersResponse.json()
        const deliveriesJson: DeliveriesResponse = await deliveriesResponse.json()

        if (active) {
          setDeliverers(deliverersJson.items)
          setDeliveries(deliveriesJson.items)
        }
      } catch (cause) {
        if (active) {
          setError(cause instanceof Error ? cause.message : 'Erro inesperado')
        }
      } finally {
        if (active) {
          setLoading(false)
        }
      }
    }

    void load()
    const timer = window.setInterval(() => void load(), 15000)
    return () => {
      active = false
      window.clearInterval(timer)
    }
  }, [filterRegion])

  const activeDelivery = useMemo(
    () => deliveries.find((delivery) => delivery.deliverer_id === session?.id || delivery.assigned_deliverer_id === session?.id),
    [deliveries, session?.id],
  )

  const availableDeliveries = useMemo(
    () => deliveries.filter((delivery) => delivery.status === 'WAITING' || delivery.status === 'ASSIGNED'),
    [deliveries],
  )

  const myHistory = useMemo(
    () => deliveries.filter((delivery) => delivery.deliverer_id === session?.id || delivery.assigned_deliverer_id === session?.id),
    [deliveries, session?.id],
  )

  async function refresh() {
    const [deliverersResponse, deliveriesResponse] = await Promise.all([
      fetch(`/api/v1/deliverers/?region=${encodeURIComponent(filterRegion)}`),
      fetch(`/api/v1/orders/?region=${encodeURIComponent(filterRegion)}`),
    ])
    if (deliverersResponse.ok) {
      const deliverersJson: DeliverersResponse = await deliverersResponse.json()
      setDeliverers(deliverersJson.items)
    }
    if (deliveriesResponse.ok) {
      const deliveriesJson: DeliveriesResponse = await deliveriesResponse.json()
      setDeliveries(deliveriesJson.items)
    }
  }

  async function login(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')
    try {
      const response = await fetch('/api/v1/deliverers/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: loginName, phone: loginPhone, region: loginRegion }),
      })
      if (!response.ok) {
        throw new Error('Nao foi possivel efetuar login')
      }
      const data: Deliverer = await response.json()
      setSession({ id: data.id, name: data.name, phone: data.phone, region: data.region })
      setFilterRegion(data.region)
      setTab('dashboard')
      await refresh()
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : 'Erro inesperado')
    }
  }

  async function updateStatus(status: DelivererStatus) {
    if (!session) return
    const response = await fetch(`/api/v1/deliverers/${session.id}/status/`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status }),
    })
    if (response.ok) {
      await refresh()
    }
  }

  async function assign(deliveryId: string, delivererId?: string) {
    const response = await fetch('/api/v1/orders/assign/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ order_id: deliveryId, region: filterRegion, deliverer_id: delivererId ?? null }),
    })
    if (response.ok) {
      await refresh()
      setTab('active')
    }
  }

  async function accept(deliveryId: string) {
    if (!session) return
    const response = await fetch(`/api/v1/orders/${deliveryId}/accept/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ deliverer_id: session.id }),
    })
    if (response.ok) {
      await refresh()
      setTab('active')
    }
  }

  async function pickup(deliveryId: string) {
    if (!session) return
    const response = await fetch(`/api/v1/orders/${deliveryId}/pickup/`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ deliverer_id: session.id }),
    })
    if (response.ok) {
      await refresh()
    }
  }

  async function deliver(deliveryId: string) {
    if (!session) return
    const response = await fetch(`/api/v1/orders/${deliveryId}/deliver/`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ deliverer_id: session.id }),
    })
    if (response.ok) {
      await refresh()
      setTab('history')
    }
  }

  if (!session) {
    return (
      <main className="page page--login">
        <section className="hero">
          <p className="eyebrow">Deliverer</p>
          <h1 className="title">Acesse seu painel de entregas</h1>
          <p className="subtitle">Entre com seus dados para gerenciar disponibilidade, aceitar entregas e finalizar pedidos.</p>
        </section>

        <Card className="panel panel--login">
          <form className="stack" onSubmit={login}>
            <label className="field">
              <span>Nome</span>
              <input value={loginName} onChange={(event) => setLoginName(event.target.value)} placeholder="Ana" />
            </label>
            <label className="field">
              <span>Telefone</span>
              <input value={loginPhone} onChange={(event) => setLoginPhone(event.target.value)} placeholder="11999999999" />
            </label>
            <label className="field">
              <span>Região</span>
              <input value={loginRegion} onChange={(event) => setLoginRegion(event.target.value)} placeholder="Zona Sul" />
            </label>
            <Button type="submit" fullWidth>
              Entrar no painel
            </Button>
          </form>
          {error && <p className="status-message status-message--error">{error}</p>}
        </Card>
      </main>
    )
  }

  return (
    <main className="page">
      <section className="hero hero--compact">
        <div>
          <p className="eyebrow">Painel do entregador</p>
          <h1 className="title">{session.name}</h1>
          <p className="subtitle">Região atual: {filterRegion}</p>
        </div>
        <div className="hero__actions">
          <Button variant={tab === 'dashboard' ? 'primary' : 'secondary'} onClick={() => setTab('dashboard')}>Dashboard</Button>
          <Button variant={tab === 'active' ? 'primary' : 'secondary'} onClick={() => setTab('active')}>Active Delivery</Button>
          <Button variant={tab === 'history' ? 'primary' : 'secondary'} onClick={() => setTab('history')}>History</Button>
          <Button variant={tab === 'profile' ? 'primary' : 'secondary'} onClick={() => setTab('profile')}>Profile</Button>
        </div>
      </section>

      {error && <p className="status-message status-message--error">{error}</p>}

      {tab === 'dashboard' && (
        <section className="grid">
          <Card>
            <div className="section-head">
              <div>
                <h2>Disponíveis</h2>
                <p>Entregas prontas para atribuição ou aceitação.</p>
              </div>
              <Button variant="ghost" onClick={() => void refresh()}>Atualizar</Button>
            </div>
            {loading && <p>Carregando...</p>}
            <div className="stack">
              {availableDeliveries.map((delivery) => (
                <Card key={delivery.order_id} className="card--subtle">
                  <div className="row row--space">
                    <div>
                      <strong>{delivery.order_id}</strong>
                      <p>{delivery.region}</p>
                    </div>
                    <Badge status={mapBadgeStatus(delivery.status)} />
                  </div>
                  <div className="actions">
                    <Button variant="secondary" onClick={() => void accept(delivery.order_id)}>
                      Aceitar
                    </Button>
                    <Button variant="secondary" onClick={() => void assign(delivery.order_id, session.id)}>
                      Atribuir a mim
                    </Button>
                  </div>
                </Card>
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
              <Button onClick={() => void updateStatus('AVAILABLE')}>AVAILABLE</Button>
              <Button variant="secondary" onClick={() => void updateStatus('BUSY')}>BUSY</Button>
              <Button variant="ghost" onClick={() => void updateStatus('OFFLINE')}>OFFLINE</Button>
            </div>
          </Card>
        </section>
      )}

      {tab === 'active' && (
        <section className="grid">
          <Card>
            <div className="section-head">
              <div>
                <h2>Active Delivery</h2>
                <p>Entrega em andamento para o entregador logado.</p>
              </div>
            </div>
            {activeDelivery ? (
              <div className="stack">
                <p><strong>Pedido:</strong> {activeDelivery.order_id}</p>
                <p><strong>Status:</strong> {activeDelivery.status}</p>
                <div className="actions">
                  <Button variant="secondary" disabled={activeDelivery.status !== 'ASSIGNED'} onClick={() => void accept(activeDelivery.order_id)}>Accept</Button>
                  <Button variant="secondary" disabled={activeDelivery.status !== 'IN_DELIVERY'} onClick={() => void pickup(activeDelivery.order_id)}>Pickup</Button>
                  <Button disabled={activeDelivery.status !== 'PICKED_UP'} onClick={() => void deliver(activeDelivery.order_id)}>Deliver</Button>
                </div>
              </div>
            ) : (
              <p>Nenhuma entrega ativa no momento.</p>
            )}
          </Card>
        </section>
      )}

      {tab === 'history' && (
        <section className="grid">
          <Card>
            <div className="section-head">
              <div>
                <h2>Delivery History</h2>
                <p>Últimas entregas concluídas ou em andamento.</p>
              </div>
            </div>
            <div className="stack">
              {myHistory.map((delivery) => (
                <Card key={delivery.order_id} className="card--subtle">
                  <div className="row row--space">
                    <div>
                      <strong>{delivery.order_id}</strong>
                      <p>{delivery.region}</p>
                    </div>
                    <Badge status={mapBadgeStatus(delivery.status)} />
                  </div>
                  <p>Entregador: {delivery.deliverer_id ?? delivery.assigned_deliverer_id ?? '—'}</p>
                  <p>Pickup: {delivery.picked_up_at ?? '—'}</p>
                  <p>Delivered: {delivery.delivered_at ?? '—'}</p>
                </Card>
              ))}
            </div>
          </Card>
        </section>
      )}

      {tab === 'profile' && (
        <section className="grid">
          <Card>
            <div className="section-head">
              <div>
                <h2>Deliverer Profile</h2>
                <p>Dados básicos da conta e região ativa.</p>
              </div>
            </div>
            <div className="stack">
              <p><strong>ID:</strong> {session.id}</p>
              <p><strong>Nome:</strong> {session.name}</p>
              <p><strong>Telefone:</strong> {session.phone}</p>
              <p><strong>Região:</strong> {session.region}</p>
              <div className="actions">
                <Button variant="secondary" onClick={() => setSession(null)}>Sair</Button>
                <Button variant="ghost" onClick={() => setFilterRegion(session.region)}>Usar região do perfil</Button>
              </div>
            </div>
          </Card>
        </section>
      )}
    </main>
  )
}

function mapBadgeStatus(status: DeliveryStatus) {
  if (status === 'ASSIGNED' || status === 'IN_DELIVERY') {
    return 'BUSY'
  }
  if (status === 'PICKED_UP') {
    return 'AVAILABLE'
  }
  if (status === 'DELIVERED') {
    return 'AVAILABLE'
  }
  if (status === 'CANCELLED') {
    return 'OFFLINE'
  }
  return 'AVAILABLE'
}

export default App
