import { FormEvent, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import Button from '../../../shared/components/Button'
import Card from '../../../shared/components/Card'
import Input from '../../../shared/components/Input'
import { registerCliente } from '../api/authApi'

function RegisterPage() {
  const navigate = useNavigate()
  const [form, setForm] = useState({
    nome: '',
    email: '',
    cpf: '',
    telefone: '',
    senha: '',
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  function update(field: keyof typeof form) {
    return (event: React.ChangeEvent<HTMLInputElement>) =>
      setForm((prev) => ({ ...prev, [field]: event.target.value }))
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')
    setLoading(true)
    try {
      await registerCliente(form)
      navigate('/login', {
        state: { message: 'Conta criada com sucesso. Faça login para continuar.' },
      })
    } catch {
      setError('Não foi possível criar a conta. Verifique os dados (e-mail/CPF podem já existir).')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="page page--login">
      <section className="hero hero--login">
        <p className="eyebrow">Yummicious</p>
        <h1 className="title">Criar conta</h1>
        <p className="subtitle">Cadastre-se para fazer pedidos no campus.</p>
      </section>

      <Card className="panel panel--login">
        <form className="stack" onSubmit={handleSubmit}>
          <label className="field">
            <span>Nome</span>
            <Input value={form.nome} onChange={update('nome')} required data-cy="nome" />
          </label>
          <label className="field">
            <span>E-mail</span>
            <Input type="email" value={form.email} onChange={update('email')} required data-cy="email" />
          </label>
          <label className="field">
            <span>CPF</span>
            <Input value={form.cpf} onChange={update('cpf')} required data-cy="cpf" />
          </label>
          <label className="field">
            <span>Telefone</span>
            <Input value={form.telefone} onChange={update('telefone')} required data-cy="telefone" />
          </label>
          <label className="field">
            <span>Senha</span>
            <Input
              type="password"
              value={form.senha}
              onChange={update('senha')}
              placeholder="••••••"
              required
              data-cy="password"
            />
          </label>
          <Button type="submit" fullWidth disabled={loading} data-cy="register-submit">
            Criar conta
          </Button>
        </form>
        {error && <p className="status-message status-message--error">{error}</p>}
        <p className="status-message">
          Já tem conta? <Link to="/login">Entrar</Link>
        </p>
      </Card>
    </main>
  )
}

export default RegisterPage
