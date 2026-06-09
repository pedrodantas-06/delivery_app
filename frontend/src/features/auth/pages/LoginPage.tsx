import { FormEvent, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth, type UserRole } from '../../../app/providers/AuthProvider'
import Button from '../../../shared/components/Button'
import Card from '../../../shared/components/Card'
import Input from '../../../shared/components/Input'

function redirectByRole(role: UserRole, navigate: ReturnType<typeof useNavigate>) {
  switch (role) {
    case 'CLIENTE':
      navigate('/customer')
      break
    case 'RESTAURANTE':
      navigate('/restaurant')
      break
    case 'ENTREGADOR':
      navigate('/deliverer')
      break
    case 'ADMIN':
      navigate('/admin')
      break
  }
}

function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')
    setLoading(true)
    try {
      const role = await login(email, senha)
      redirectByRole(role, navigate)
    } catch {
      setError('Credenciais inválidas')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="page page--login">
      <section className="hero hero--login">
        <p className="eyebrow">Yummicious</p>
        <h1 className="title">Entre na plataforma</h1>
        <p className="subtitle">Use sua conta para acessar a experiência correta automaticamente.</p>
        <p className="subtitle">Use contas demo da documentação.</p>
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
              data-cy="email"
              required
            />
          </label>
          <label className="field">
            <span>Senha</span>
            <Input
              type="password"
              value={senha}
              onChange={(event) => setSenha(event.target.value)}
              placeholder="••••••"
              data-cy="password"
              required
            />
          </label>
          <Button type="submit" fullWidth disabled={loading} data-cy="login-submit">
            Entrar
          </Button>
        </form>
        {error && <p className="status-message status-message--error">{error}</p>}
      </Card>
    </main>
  )
}

export default LoginPage
