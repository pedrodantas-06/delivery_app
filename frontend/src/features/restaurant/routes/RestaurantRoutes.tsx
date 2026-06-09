import { Link, Route, Routes, useNavigate } from 'react-router-dom'
import { useAuth } from '../../../app/providers/AuthProvider'
import Button from '../../../shared/components/Button'
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
    <main className="page">
      <header className="section-head section-head--spaced">
        <div>
          <h2>{user?.nome ?? 'Restaurante'}</h2>
          <p>Painel operacional</p>
        </div>
        <div className="actions">
          <Link to="/restaurant" className="btn btn--ghost">
            Dashboard
          </Link>
          <Link to="/restaurant/orders" className="btn btn--ghost">
            Pedidos
          </Link>
          <Button variant="secondary" onClick={handleLogout}>
            Sair
          </Button>
        </div>
      </header>

      <Routes>
        <Route index element={<RestaurantDashboardPage />} />
        <Route path="orders" element={<RestaurantOrdersPage />} />
        <Route path="orders/:id" element={<RestaurantDecisionPage />} />
      </Routes>
    </main>
  )
}

export function RestaurantRoutes() {
  return <RestaurantLayout />
}

export default RestaurantRoutes
