import { useEffect, useMemo, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { getMenu } from '../api/customerApi'
import { useCart } from '../context/CartContext'
import type { MenuItem } from '../types'
import Card from '../../../shared/components/Card'
import Button from '../../../shared/components/Button'
import Loading from '../../../shared/components/Loading'
import EmptyState from '../../../shared/components/EmptyState'

function formatPrice(value: number) {
  return `R$ ${value.toFixed(2)}`
}

function MenuPage() {
  const { restaurantId } = useParams()
  const navigate = useNavigate()
  const { addItem } = useCart()
  const [items, setItems] = useState<MenuItem[]>([])
  const [restaurantName, setRestaurantName] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const parsedRestaurantId = Number(restaurantId)

  useEffect(() => {
    if (!parsedRestaurantId) {
      setError('Restaurante inválido.')
      setLoading(false)
      return
    }

    let active = true

    getMenu(parsedRestaurantId)
      .then((data) => {
        if (!active) return
        setRestaurantName(data.restaurante)
        setItems(data.itens)
      })
      .catch(() => {
        if (active) setError('Não foi possível carregar o cardápio.')
      })
      .finally(() => {
        if (active) setLoading(false)
      })

    return () => {
      active = false
    }
  }, [parsedRestaurantId])

  const groupedItems = useMemo(() => {
    return items.reduce<Record<string, MenuItem[]>>((groups, item) => {
      const category = item.categoria
      if (!groups[category]) groups[category] = []
      groups[category].push(item)
      return groups
    }, {})
  }, [items])

  if (loading) {
    return <Loading label="Carregando cardápio..." />
  }

  if (error) {
    return <p className="status-message status-message--error">{error}</p>
  }

  if (items.length === 0) {
    return <EmptyState message="Este restaurante ainda não possui itens no cardápio." />
  }

  return (
    <section className="customer-section">
      <header className="section-head">
        <h1 className="title">{restaurantName}</h1>
        <p>Adicione itens ao carrinho por categoria.</p>
      </header>

      {Object.entries(groupedItems).map(([category, categoryItems]) => (
        <section key={category} className="customer-menu-group">
          <h2>{category}</h2>
          <div className="grid">
            {categoryItems.map((item) => (
              <Card key={item.id}>
                <strong>{item.nome}</strong>
                <p>{item.descricao}</p>
                <p>{formatPrice(Number(item.preco))}</p>
                <Button
                  variant="primary"
                  fullWidth
                  onClick={() =>
                    addItem(
                      { id: item.id, nome: item.nome, preco: Number(item.preco) },
                      parsedRestaurantId,
                      restaurantName,
                    )
                  }
                >
                  Adicionar
                </Button>
              </Card>
            ))}
          </div>
        </section>
      ))}

      <div className="actions actions--stacked">
        <Button variant="secondary" fullWidth onClick={() => navigate('/customer/cart')}>
          Ir para o carrinho
        </Button>
      </div>
    </section>
  )
}

export default MenuPage
