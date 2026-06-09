import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../../app/providers/AuthProvider'
import Card from '../../../shared/components/Card'
import Button from '../../../shared/components/Button'

function ProfilePage() {
  const navigate = useNavigate()
  const { user, logout } = useAuth()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  if (!user) {
    return null
  }

  return (
    <section className="customer-section">
      <header className="section-head">
        <h1 className="title">Perfil</h1>
        <p>Dados da sua conta no campus.</p>
      </header>

      <Card>
        <p>
          <strong>Nome:</strong> {user.nome}
        </p>
        <p>
          <strong>Email:</strong> {user.email}
        </p>
        <p>
          <strong>Cliente:</strong> {user.referencia_id ?? '—'}
        </p>
      </Card>

      <div className="actions actions--stacked">
        <Button variant="secondary" fullWidth onClick={handleLogout}>
          Sair
        </Button>
      </div>
    </section>
  )
}

export default ProfilePage
