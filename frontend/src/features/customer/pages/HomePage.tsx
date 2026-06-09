import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getRestaurants } from '../api/customerApi'
import type { Restaurant } from '../types'
import Card from '../../../shared/components/Card'
import Loading from '../../../shared/components/Loading'
import EmptyState from '../../../shared/components/EmptyState'

function restaurantBadgeClass(status: string) {
  return status.toLowerCase() === 'aberto' ? 'badge badge--available' : 'badge badge--offline'
}

function HomePage() {
  const navigate = useNavigate()
  const [restaurants, setRestaurants] = useState<Restaurant[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let active = true

    getRestaurants()
      .then((data) => {
        if (active) setRestaurants(data)
      })
      .catch(() => {
        if (active) setError('Não foi possível carregar os restaurantes.')
      })
      .finally(() => {
        if (active) setLoading(false)
      })

    return () => {
      active = false
    }
  }, [])

  if (loading) {
    return <Loading label="Carregando restaurantes..." />
  }

  if (error) {
    return <p className="status-message status-message--error">{error}</p>
  }

  if (restaurants.length === 0) {
    return <EmptyState message="Nenhum restaurante disponível no momento." />
  }

  return (
    <section className="customer-section">
      <header className="section-head">
        <h1 className="title">Restaurantes</h1>
        <p>Escolha onde pedir hoje no campus.</p>
      </header>

      <div className="grid">
        {restaurants.map((restaurant) => (
          <Card key={restaurant.id}>
            <div className="delivery-card__head">
              <div className="delivery-card__title">
                <strong>{restaurant.nome}</strong>
                <p>{restaurant.tipo}</p>
              </div>
              <span className={restaurantBadgeClass(restaurant.status)}>{restaurant.status}</span>
            </div>
            <p>{restaurant.endereco}</p>
            <p>{restaurant.horario}</p>
            <div className="actions actions--stacked">
              <button
                type="button"
                className="btn btn--primary btn--full"
                disabled={restaurant.status.toLowerCase() !== 'aberto'}
                onClick={() => navigate(`/customer/menu/${restaurant.id}`)}
              >
                Ver cardápio
              </button>
            </div>
          </Card>
        ))}
      </div>
    </section>
  )
}

export default HomePage
