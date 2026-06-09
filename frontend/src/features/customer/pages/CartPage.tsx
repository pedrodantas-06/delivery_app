import { useNavigate } from 'react-router-dom'
import { useCart } from '../context/CartContext'
import Card from '../../../shared/components/Card'
import Button from '../../../shared/components/Button'
import EmptyState from '../../../shared/components/EmptyState'

function formatPrice(value: number) {
  return `R$ ${value.toFixed(2)}`
}

function CartPage() {
  const navigate = useNavigate()
  const { items, total, restaurantName, removeItem } = useCart()

  if (items.length === 0) {
    return (
      <section className="customer-section">
        <header className="section-head">
          <h1 className="title">Carrinho</h1>
        </header>
        <EmptyState message="Seu carrinho está vazio." />
        <div className="actions actions--stacked">
          <Button variant="primary" fullWidth onClick={() => navigate('/customer')}>
            Ver restaurantes
          </Button>
        </div>
      </section>
    )
  }

  return (
    <section className="customer-section">
      <header className="section-head">
        <h1 className="title">Carrinho</h1>
        {restaurantName && <p>{restaurantName}</p>}
      </header>

      <div className="grid">
        {items.map((item) => (
          <Card key={item.id}>
            <div className="delivery-card__head">
              <strong>{item.nome}</strong>
              <span>{item.quantidade}x</span>
            </div>
            <p>{formatPrice(item.preco * item.quantidade)}</p>
            <Button variant="ghost" onClick={() => removeItem(item.id)}>
              Remover
            </Button>
          </Card>
        ))}
      </div>

      <Card>
        <strong>Total: {formatPrice(total)}</strong>
      </Card>

      <div className="actions actions--stacked">
        <Button variant="primary" fullWidth onClick={() => navigate('/customer/checkout')}>
          Finalizar pedido
        </Button>
      </div>
    </section>
  )
}

export default CartPage
