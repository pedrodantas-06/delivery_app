import { FormEvent, useState } from 'react'
import { Link } from 'react-router-dom'
import Button from '../../../shared/components/Button'
import Card from '../../../shared/components/Card'
import Input from '../../../shared/components/Input'
import { forgotPassword } from '../api/authApi'

function ForgotPasswordPage() {
  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(false)
  const [mensagem, setMensagem] = useState('')
  const [devToken, setDevToken] = useState<string | null>(null)

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setLoading(true)
    setMensagem('')
    setDevToken(null)
    try {
      const res = await forgotPassword(email)
      setMensagem(res.mensagem)
      if (res.token) setDevToken(res.token)
    } catch {
      setMensagem('Não foi possível processar a solicitação. Tente novamente.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="page page--login">
      <section className="hero hero--login">
        <p className="eyebrow">Yummicious</p>
        <h1 className="title">Esqueci minha senha</h1>
        <p className="subtitle">Informe seu e-mail para receber instruções de recuperação.</p>
      </section>

      <Card className="panel panel--login">
        <form className="stack" onSubmit={handleSubmit}>
          <label className="field">
            <span>E-mail</span>
            <Input
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              placeholder="cliente@yummicious.com"
              required
              data-cy="email"
            />
          </label>
          <Button type="submit" fullWidth disabled={loading} data-cy="forgot-submit">
            Enviar
          </Button>
        </form>

        {mensagem && <p className="status-message">{mensagem}</p>}

        {devToken && (
          <p className="status-message">
            Modo dev — use este token:{' '}
            <Link to={`/reset-password?token=${encodeURIComponent(devToken)}`} data-cy="dev-reset-link">
              redefinir senha agora
            </Link>
          </p>
        )}

        <p className="status-message">
          <Link to="/login">Voltar ao login</Link>
        </p>
      </Card>
    </main>
  )
}

export default ForgotPasswordPage
