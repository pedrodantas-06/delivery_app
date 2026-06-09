import { useState, type FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../../app/providers/AuthProvider'
import { createOrder, processPayment } from '../api/customerApi'
import { useCart } from '../context/CartContext'
import Button from '../../../shared/components/Button'
import Input from '../../../shared/components/Input'
import LoadingState from '../../../shared/components/LoadingState'

function CheckoutPage() {
  const navigate = useNavigate()
  const { user } = useAuth()
  const { items, total, restaurantId, clear } = useCart()
  const [campus, setCampus] = useState('Campus Central')
  const [bloco, setBloco] = useState('')
  const [sala, setSala] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const clienteId = user?.referencia_id

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault()

    if (!clienteId || !restaurantId || items.length === 0) {
      setError('Carrinho inválido. Volte e adicione itens antes de pagar.')
      return
    }

    if (!bloco.trim() || !sala.trim()) {
      setError('Informe bloco e sala para entrega.')
      return
    }

    setSubmitting(true)
    setError(null)

    try {
      const order = await createOrder({
        id_restaurante: restaurantId,
        cliente_id: clienteId,
        itens: items.map((item) => ({
          nome: item.nome,
          preco: item.preco,
          quantidade: item.quantidade,
        })),
        endereco_entrega: `${campus.trim()} / ${bloco.trim()} / ${sala.trim()}`,
      })

      await processPayment(order.id)
      clear()
      navigate(`/customer/tracking/${order.id}`)
    } catch {
      setError('Não foi possível concluir o pagamento. Tente novamente.')
      setSubmitting(false)
    }
  }

  if (submitting) {
    return <LoadingState label="Processando pagamento..." />
  }

  return (
    <section className="customer-section">
      <header className="section-head">
        <h1 className="title">Checkout</h1>
        <p>Total do pedido: R$ {total.toFixed(2)}</p>
      </header>

      <form className="checkout-form" onSubmit={handleSubmit}>
        <label className="field">
          Campus
          <Input value={campus} onChange={(event) => setCampus(event.target.value)} required />
        </label>

        <label className="field">
          Bloco
          <Input value={bloco} onChange={(event) => setBloco(event.target.value)} required />
        </label>

        <label className="field">
          Sala
          <Input value={sala} onChange={(event) => setSala(event.target.value)} required />
        </label>

        {error && <p className="status-message status-message--error">{error}</p>}

        <Button type="submit" variant="primary" fullWidth>
          Pagar pedido
        </Button>
      </form>
    </section>
  )
}

export default CheckoutPage
