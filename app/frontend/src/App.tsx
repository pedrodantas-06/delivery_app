import { useCallback, useEffect, useMemo, useState } from 'react'
import Badge from './components/Badge'
import Button from './components/Button'
import Card from './components/Card'

type DelivererStatus = 'AVAILABLE' | 'OCCUPIED' | 'OFFLINE'

type Deliverer = {
  id: string
  name: string
  phone: string
  region: string
  status: DelivererStatus
}

type DeliverersResponse = {
  items: Deliverer[]
}

function App() {
  const [items, setItems] = useState<Deliverer[]>([])
  const [filter, setFilter] = useState<'ALL' | DelivererStatus>('ALL')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const fetchDeliverers = useCallback(async () => {
    setLoading(true)
    setError('')

    try {
      const query = filter === 'ALL' ? '' : `?status=${filter}`
      const response = await fetch(`/api/deliverers/${query}`)
      if (!response.ok) {
        throw new Error('Falha ao carregar entregadores')
      }
      const data: DeliverersResponse = await response.json()
      setItems(data.items)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Erro inesperado'
      setError(message)
    } finally {
      setLoading(false)
    }
  }, [filter])

  useEffect(() => {
    void fetchDeliverers()
  }, [fetchDeliverers])

  const title = useMemo(() => {
    if (filter === 'ALL') {
      return 'Todos os entregadores'
    }
    return `Entregadores ${filter}`
  }, [filter])

  const markAsOccupied = useCallback(async (delivererId: string) => {
    setError('')
    try {
      const response = await fetch(`/api/deliverers/${delivererId}/status/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: 'OCCUPIED' }),
      })
      if (!response.ok) {
        throw new Error('Nao foi possivel atualizar o status')
      }
      await fetchDeliverers()
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Erro inesperado'
      setError(message)
    }
  }, [fetchDeliverers])

  return (
    <main className="page">
      <section className="header">
        <h1 className="title">Gestao de Entregadores</h1>
        <p className="subtitle">Acompanhe disponibilidade e acione entregadores rapidamente.</p>
      </section>

      <section className="toolbar">
        <Button variant={filter === 'ALL' ? 'primary' : 'secondary'} onClick={() => setFilter('ALL')}>
          Todos
        </Button>
        <Button variant={filter === 'AVAILABLE' ? 'primary' : 'secondary'} onClick={() => setFilter('AVAILABLE')}>
          Disponiveis
        </Button>
        <Button variant={filter === 'OCCUPIED' ? 'primary' : 'secondary'} onClick={() => setFilter('OCCUPIED')}>
          Ocupados
        </Button>
        <Button variant={filter === 'OFFLINE' ? 'primary' : 'secondary'} onClick={() => setFilter('OFFLINE')}>
          Offline
        </Button>
      </section>

      <section className="content">
        <div className="content-header">
          <h2>{title}</h2>
          <Button variant="ghost" onClick={() => void fetchDeliverers()}>
            Atualizar
          </Button>
        </div>

        {loading && <p className="status-message">Carregando entregadores...</p>}

        {error && <p className="status-message status-message--error">{error}</p>}

        {!loading && !error && items.length === 0 && (
          <Card>
            <p className="empty">Nenhum entregador encontrado para este filtro.</p>
          </Card>
        )}

        <div className="cards">
          {items.map((deliverer) => (
            <Card key={deliverer.id}>
              <div className="card-header">
                <div>
                  <h3>{deliverer.name}</h3>
                  <p>{deliverer.phone}</p>
                </div>
                <Badge status={deliverer.status} />
              </div>

              <p className="region">Regiao: {deliverer.region}</p>

              <Button
                fullWidth
                disabled={deliverer.status !== 'AVAILABLE'}
                onClick={() => void markAsOccupied(deliverer.id)}
              >
                {deliverer.status === 'AVAILABLE' ? 'Marcar como ocupado' : 'Sem acao disponivel'}
              </Button>
            </Card>
          ))}
        </div>
      </section>
    </main>
  )
}

export default App
