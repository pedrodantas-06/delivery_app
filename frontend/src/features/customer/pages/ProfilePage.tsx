import { FormEvent, useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../../app/providers/AuthProvider'
import Card from '../../../shared/components/Card'
import Button from '../../../shared/components/Button'
import Input from '../../../shared/components/Input'
import Loading from '../../../shared/components/Loading'
import { deleteAccount, getProfile, updateProfile } from '../api/customerApi'
import type { CustomerProfile } from '../types'

function ProfilePage() {
  const navigate = useNavigate()
  const { user, token, logout, updateUser } = useAuth()

  const [profile, setProfile] = useState<CustomerProfile | null>(null)
  const [loading, setLoading] = useState(true)
  const [editing, setEditing] = useState(false)
  const [form, setForm] = useState({ nome: '', telefone: '', senha: '' })
  const [saving, setSaving] = useState(false)
  const [feedback, setFeedback] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let active = true
    getProfile(token)
      .then((data) => {
        if (!active) return
        setProfile(data)
        setForm({ nome: data.nome ?? '', telefone: data.telefone ?? '', senha: '' })
      })
      .catch(() => {
        if (active) setError('Não foi possível carregar o perfil.')
      })
      .finally(() => {
        if (active) setLoading(false)
      })
    return () => {
      active = false
    }
  }, [token])

  if (!user) {
    return null
  }

  if (loading) {
    return <Loading label="Carregando perfil..." />
  }

  async function handleSave(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!user) return
    setError(null)
    setFeedback(null)
    setSaving(true)
    try {
      const payload: { nome: string; telefone: string; senha?: string } = {
        nome: form.nome,
        telefone: form.telefone,
      }
      if (form.senha) payload.senha = form.senha

      await updateProfile(user.id, payload, token)
      updateUser({ nome: form.nome })
      setProfile((prev) => (prev ? { ...prev, nome: form.nome, telefone: form.telefone } : prev))
      setForm((prev) => ({ ...prev, senha: '' }))
      setEditing(false)
      setFeedback('Dados atualizados com sucesso.')
    } catch {
      setError('Não foi possível salvar as alterações.')
    } finally {
      setSaving(false)
    }
  }

  async function handleDelete() {
    if (!user) return
    const confirmar = window.confirm(
      'Tem certeza que deseja excluir sua conta? Esta ação não pode ser desfeita.',
    )
    if (!confirmar) return

    try {
      await deleteAccount(user.id, token)
      logout()
      navigate('/login', { state: { message: 'Conta excluída.' } })
    } catch {
      setError('Não foi possível excluir a conta.')
    }
  }

  return (
    <section className="customer-section">
      <header className="section-head">
        <h1 className="title">Perfil</h1>
        <p>Dados da sua conta no campus.</p>
      </header>

      {feedback && <p className="status-message status-message--success">{feedback}</p>}
      {error && <p className="status-message status-message--error">{error}</p>}

      {!editing ? (
        <Card>
          <p>
            <strong>Nome:</strong> {profile?.nome ?? user.nome}
          </p>
          <p>
            <strong>Email:</strong> {profile?.email ?? user.email}
          </p>
          <p>
            <strong>Telefone:</strong> {profile?.telefone ?? '—'}
          </p>
          <p>
            <strong>CPF:</strong> {profile?.cpf ?? '—'}
          </p>
          <p>
            <strong>Cliente:</strong> {profile?.referencia_id ?? user.referencia_id ?? '—'}
          </p>
        </Card>
      ) : (
        <Card>
          <form className="stack" onSubmit={handleSave}>
            <label className="field">
              <span>Nome</span>
              <Input
                value={form.nome}
                onChange={(e) => setForm((p) => ({ ...p, nome: e.target.value }))}
                required
                data-cy="profile-nome"
              />
            </label>
            <label className="field">
              <span>Telefone</span>
              <Input
                value={form.telefone}
                onChange={(e) => setForm((p) => ({ ...p, telefone: e.target.value }))}
                data-cy="profile-telefone"
              />
            </label>
            <label className="field">
              <span>Nova senha (opcional)</span>
              <Input
                type="password"
                value={form.senha}
                onChange={(e) => setForm((p) => ({ ...p, senha: e.target.value }))}
                placeholder="••••••"
                data-cy="profile-senha"
              />
            </label>
            <Button type="submit" fullWidth disabled={saving} data-cy="profile-save">
              Salvar
            </Button>
          </form>
        </Card>
      )}

      <div className="actions actions--stacked">
        {!editing ? (
          <Button variant="primary" fullWidth onClick={() => setEditing(true)} data-cy="profile-edit">
            Editar dados
          </Button>
        ) : (
          <Button variant="ghost" fullWidth onClick={() => setEditing(false)}>
            Cancelar
          </Button>
        )}
        <Button variant="secondary" fullWidth onClick={() => { logout(); navigate('/login') }}>
          Sair
        </Button>
        <Button variant="ghost" fullWidth className="btn--danger" onClick={handleDelete} data-cy="profile-delete">
          Excluir conta
        </Button>
      </div>
    </section>
  )
}

export default ProfilePage
