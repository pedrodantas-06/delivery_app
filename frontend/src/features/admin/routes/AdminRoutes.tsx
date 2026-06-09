import { Route, Routes, useNavigate } from 'react-router-dom'
import { useAuth } from '../../../app/providers/AuthProvider'
import Button from '../../../shared/components/Button'
import AdminDashboard from '../pages/AdminDashboard'

function AdminLayout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <main className="page">
      <header className="section-head section-head--spaced">
        <div>
          <h2>{user?.nome ?? 'Admin'}</h2>
          <p>Painel administrativo</p>
        </div>
        <div className="actions">
          <Button variant="secondary" onClick={handleLogout}>
            Sair
          </Button>
        </div>
      </header>

      <Routes>
        <Route index element={<AdminDashboard />} />
      </Routes>
    </main>
  )
}

export function AdminRoutes() {
  return <AdminLayout />
}

export default AdminRoutes
