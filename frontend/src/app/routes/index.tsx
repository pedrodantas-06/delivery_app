import { createBrowserRouter, Navigate } from 'react-router-dom'
import { RoleGuard } from '../guards/RoleGuard'
import LoginPage from '../../features/auth/pages/LoginPage'
import { CustomerRoutes } from '../../features/customer/routes/CustomerRoutes'
import { RestaurantRoutes } from '../../features/restaurant/routes/RestaurantRoutes'
import DelivererRoutes from '../../features/deliverer/routes/DelivererRoutes'
import { AdminRoutes } from '../../features/admin/routes/AdminRoutes'

export const router = createBrowserRouter([
  { path: '/login', element: <LoginPage /> },
  {
    path: '/customer/*',
    element: (
      <RoleGuard allowed={['CLIENTE']}>
        <CustomerRoutes />
      </RoleGuard>
    ),
  },
  {
    path: '/restaurant/*',
    element: (
      <RoleGuard allowed={['RESTAURANTE']}>
        <RestaurantRoutes />
      </RoleGuard>
    ),
  },
  {
    path: '/deliverer/*',
    element: (
      <RoleGuard allowed={['ENTREGADOR']}>
        <DelivererRoutes />
      </RoleGuard>
    ),
  },
  {
    path: '/admin/*',
    element: (
      <RoleGuard allowed={['ADMIN']}>
        <AdminRoutes />
      </RoleGuard>
    ),
  },
  { path: '/', element: <Navigate to="/login" replace /> },
  { path: '*', element: <Navigate to="/login" replace /> },
])
