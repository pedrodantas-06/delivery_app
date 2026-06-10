import { FormEvent, useState } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'
import Button from '../../../shared/components/Button'
import Card from '../../../shared/components/Card'
import Input from '../../../shared/components/Input'
import { resetPassword } from '../api/authApi'

function ResetPasswordPage() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const [token, setToken] = useState(searchParams.get('token') ?? '')
  const [novaSenha, setNovaSenha] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')
    setLoading(true)
    try {
      await resetPassword(token, novaSenha)
      navigate('/login', {
        state: { message: 'Senha redefinida com sucesso. Faça login com a nova senha.' },
      })
    } catch {
      setError('Token inválido ou expirado. Solicite uma nova recuperação.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="page page--login">
      <section className="hero hero--login">
        <p className="eyebrow">Yummicious</p>
        <h1 className="title">Redefinir senha</h1>
        <p className="subtitle">Informe o token recebido e a nova senha.</p>
      </section>

      <Card className="panel panel--login">
        <form className="stack" onSubmit={handleSubmit}>
          <label className="field">
            <span>Token</span>
            <Input
              value={token}
              onChange={(event) => setToken(event.target.value)}
              required
              data-cy="token"
            />
          </label>
          <label className="field">
            <span>Nova senha</span>
            <Input
              type="password"
              value={novaSenha}
              onChange={(event) => setNovaSenha(event.target.value)}
              placeholder="••••••"
              required
              data-cy="nova-senha"
            />
          </label>
          <Button type="submit" fullWidth disabled={loading} data-cy="reset-submit">
            Redefinir
          </Button>
        </form>
        {error && <p className="status-message status-message--error">{error}</p>}
        <p className="status-message">
          <Link to="/login">Voltar ao login</Link>
        </p>
      </Card>
    </main>
  )
}

export default ResetPasswordPage
