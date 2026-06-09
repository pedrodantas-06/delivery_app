import { Link, Route, Routes, useNavigate } from 'react-router-dom'
import { useAuth } from '../../../app/providers/AuthProvider'
import AppShell from '../../../shared/components/AppShell'
import TopBar from '../../../shared/components/TopBar'
import RestaurantDashboardPage from '../pages/RestaurantDashboardPage'
import RestaurantDecisionPage from '../pages/RestaurantDecisionPage'
import RestaurantOrdersPage from '../pages/RestaurantOrdersPage'

function RestaurantLayout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <AppShell>
      <TopBar
        title={user?.nome ?? 'Restaurante'}
        subtitle="Painel operacional"
        onLogout={handleLogout}
        actions={
          <>
            <Link to="/restaurant" className="btn btn--ghost">
              Dashboard
            </Link>
            <Link to="/restaurant/orders" className="btn btn--ghost">
              Pedidos
            </Link>
          </>
        }
      />

      <Routes>
        <Route index element={<RestaurantDashboardPage />} />
        <Route path="orders" element={<RestaurantOrdersPage />} />
        <Route path="orders/:id" element={<RestaurantDecisionPage />} />
      </Routes>
    </AppShell>
  )
}

export function RestaurantRoutes() {
  return <RestaurantLayout />
}

export default RestaurantRoutes
