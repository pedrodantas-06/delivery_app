import { useMemo, useState } from 'react'
import DelivererHeader from '../components/DelivererHeader'
import ActiveDeliveryPage from '../pages/ActiveDeliveryPage'
import DashboardPage from '../pages/DashboardPage'
import HistoryPage from '../pages/HistoryPage'
import LoginPage from '../pages/LoginPage'
import ProfilePage from '../pages/ProfilePage'
import { useActiveDelivery } from '../hooks/useActiveDelivery'
import { useDeliverer } from '../hooks/useDeliverer'
import { useDeliveries } from '../hooks/useDeliveries'
import { useDeliveryHistory } from '../hooks/useDeliveryHistory'
import { DEFAULT_REGION } from '../constants'
import type { DelivererTab } from '../types'


function DelivererRoutes() {
  const { session, error, login, logout, changeStatus } = useDeliverer()
  const [tab, setTab] = useState<DelivererTab>('dashboard')
  const [region, setRegion] = useState(DEFAULT_REGION)
  const [loginForm, setLoginForm] = useState({ name: 'Ana', phone: '11999999999', region: DEFAULT_REGION })
  const { deliverers, deliveries, loading, refresh, assign, accept, pickup, deliver } = useDeliveries(region)
  const activeDelivery = useActiveDelivery(deliveries, session?.id)
  const history = useDeliveryHistory(deliveries, session?.id)

  const header = useMemo(() => {
    if (!session) {
      return null
    }
    return (
      <DelivererHeader
        title={session.name}
        subtitle={`Região atual: ${region}`}
        actions={[
          { label: 'Dashboard', active: tab === 'dashboard', onClick: () => setTab('dashboard') },
          { label: 'Active Delivery', active: tab === 'active', onClick: () => setTab('active') },
          { label: 'History', active: tab === 'history', onClick: () => setTab('history') },
          { label: 'Profile', active: tab === 'profile', onClick: () => setTab('profile') },
        ]}
      />
    )
  }, [region, session, tab])

  if (!session) {
    return (
      <LoginPage
        form={loginForm}
        error={error}
        onChange={setLoginForm}
        onSubmit={async () => {
          const nextSession = await login(loginForm)
          setRegion(nextSession.region)
          setTab('dashboard')
          await refresh()
        }}
      />
    )
  }

  return (
    <main className="page">
      {header}

      {tab === 'dashboard' && (
        <DashboardPage
          session={session}
          region={region}
          loading={loading}
          deliveries={deliveries}
          deliverers={deliverers}
          onRefresh={refresh}
          onAccept={async (deliveryId) => {
            await accept(deliveryId, session.id)
            await refresh()
            setTab('active')
          }}
          onAssign={async (deliveryId, delivererId) => {
            await assign(deliveryId, region, delivererId)
            await refresh()
            setTab('active')
          }}
          onStatusChange={async (status) => {
            await changeStatus(status)
            await refresh()
          }}
        />
      )}

      {tab === 'active' && (
        <ActiveDeliveryPage
          session={session}
          delivery={activeDelivery}
          onAccept={async (deliveryId) => {
            await accept(deliveryId, session.id)
            await refresh()
          }}
          onPickup={async (deliveryId) => {
            await pickup(deliveryId, session.id)
            await refresh()
          }}
          onDeliver={async (deliveryId) => {
            await deliver(deliveryId, session.id)
            await refresh()
            setTab('history')
          }}
        />
      )}

      {tab === 'history' && <HistoryPage deliveries={history} />}

      {tab === 'profile' && (
        <ProfilePage
          session={session}
          onLogout={logout}
          onUseProfileRegion={() => setRegion(session.region)}
        />
      )}
    </main>
  )
}

export default DelivererRoutes
