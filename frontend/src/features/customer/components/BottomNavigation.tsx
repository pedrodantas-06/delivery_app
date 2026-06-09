import { NavLink } from 'react-router-dom'

const tabs = [
  { to: '/customer', label: 'Home', end: true },
  { to: '/customer/orders', label: 'Pedidos', end: false },
  { to: '/customer/cart', label: 'Carrinho', end: false },
  { to: '/customer/profile', label: 'Perfil', end: false },
]

function BottomNavigation() {
  return (
    <nav className="bottom-nav" aria-label="Navegação do cliente">
      {tabs.map((tab) => (
        <NavLink
          key={tab.to}
          to={tab.to}
          end={tab.end}
          className={({ isActive }) => `bottom-nav__item ${isActive ? 'bottom-nav__item--active' : ''}`}
        >
          {tab.label}
        </NavLink>
      ))}
    </nav>
  )
}

export default BottomNavigation
