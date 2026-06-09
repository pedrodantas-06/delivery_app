import { Route, Routes, useNavigate } from 'react-router-dom'
import { useAuth } from '../../../app/providers/AuthProvider'
import AppShell from '../../../shared/components/AppShell'
import TopBar from '../../../shared/components/TopBar'
import AdminDashboard from '../pages/AdminDashboard'

function AdminLayout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <AppShell>
      <TopBar
        title={user?.nome ?? 'Admin'}
        subtitle="Painel administrativo"
        onLogout={handleLogout}
      />

      <Routes>
        <Route index element={<AdminDashboard />} />
      </Routes>
    </AppShell>
  )
}

export function AdminRoutes() {
  return <AdminLayout />
}

export default AdminRoutes
