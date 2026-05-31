import Button from '../../../shared/components/Button'
import Card from '../../../shared/components/Card'
import Input from '../../../shared/components/Input'
import type { DelivererLoginForm } from '../types'

type LoginPageProps = {
  form: DelivererLoginForm
  loading?: boolean
  error?: string
  onChange: (form: DelivererLoginForm) => void
  onSubmit: () => void
}

function LoginPage({ form, loading = false, error, onChange, onSubmit }: LoginPageProps) {
  return (
    <main className="page page--login">
      <section className="hero">
        <p className="eyebrow">Deliverer</p>
        <h1 className="title">Acesse seu painel de entregas</h1>
        <p className="subtitle">Entre com seus dados para gerenciar disponibilidade, aceitar entregas e finalizar pedidos.</p>
      </section>

      <Card className="panel panel--login">
        <form
          className="stack"
          onSubmit={(event) => {
            event.preventDefault()
            onSubmit()
          }}
        >
          <label className="field">
            <span>Nome</span>
            <Input value={form.name} onChange={(event) => onChange({ ...form, name: event.target.value })} placeholder="Ana" />
          </label>
          <label className="field">
            <span>Telefone</span>
            <Input value={form.phone} onChange={(event) => onChange({ ...form, phone: event.target.value })} placeholder="11999999999" />
          </label>
          <label className="field">
            <span>Região</span>
            <Input value={form.region} onChange={(event) => onChange({ ...form, region: event.target.value })} placeholder="Zona Sul" />
          </label>
          <Button type="submit" fullWidth disabled={loading}>
            Entrar no painel
          </Button>
        </form>
        {error && <p className="status-message status-message--error">{error}</p>}
      </Card>
    </main>
  )
}

export default LoginPage
