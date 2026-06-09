import { Route, Routes, useLocation } from 'react-router-dom'
import { CartProvider } from '../context/CartContext'
import AppShell from '../../../shared/components/AppShell'
import BottomNavigation from '../../../shared/components/BottomNavigation'
import HomePage from '../pages/HomePage'
import MenuPage from '../pages/MenuPage'
import CartPage from '../pages/CartPage'
import CheckoutPage from '../pages/CheckoutPage'
import OrderTrackingPage from '../pages/OrderTrackingPage'
import OrderHistoryPage from '../pages/OrderHistoryPage'
import ProfilePage from '../pages/ProfilePage'

const NAV_HIDDEN_PREFIXES = ['/customer/menu/', '/customer/checkout', '/customer/tracking/']

function CustomerLayout() {
  const location = useLocation()
  const showBottomNav = !NAV_HIDDEN_PREFIXES.some((prefix) => location.pathname.startsWith(prefix))

  return (
    <div className="customer-layout">
      <AppShell className="customer-page">
        <Routes>
          <Route index element={<HomePage />} />
          <Route path="menu/:restaurantId" element={<MenuPage />} />
          <Route path="cart" element={<CartPage />} />
          <Route path="checkout" element={<CheckoutPage />} />
          <Route path="tracking/:orderId" element={<OrderTrackingPage />} />
          <Route path="orders" element={<OrderHistoryPage />} />
          <Route path="profile" element={<ProfilePage />} />
        </Routes>
      </AppShell>
      {showBottomNav && <BottomNavigation />}
    </div>
  )
}

export function CustomerRoutes() {
  return (
    <CartProvider>
      <CustomerLayout />
    </CartProvider>
  )
}
