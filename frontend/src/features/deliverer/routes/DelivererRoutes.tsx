import { useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../../app/providers/AuthProvider'
import AppShell from '../../../shared/components/AppShell'
import Loading from '../../../shared/components/Loading'
import DelivererHeader from '../components/DelivererHeader'
import ActiveDeliveryPage from '../pages/ActiveDeliveryPage'
import DashboardPage from '../pages/DashboardPage'
import HistoryPage from '../pages/HistoryPage'
import ProfilePage from '../pages/ProfilePage'
import { useActiveDelivery } from '../hooks/useActiveDelivery'
import { useDeliverer } from '../hooks/useDeliverer'
import { useDeliveries } from '../hooks/useDeliveries'
import { useDeliveryHistory } from '../hooks/useDeliveryHistory'
import { DEFAULT_REGION } from '../constants'
import { saveSession } from '../services/delivererService'
import type { DelivererTab } from '../types'

function DelivererRoutes() {
  const { user, logout: authLogout } = useAuth()
  const navigate = useNavigate()
  const { session, logout: delivererLogout, changeStatus, setSession } = useDeliverer()
  const [tab, setTab] = useState<DelivererTab>('dashboard')
  const [region, setRegion] = useState(DEFAULT_REGION)
  const { deliverers, deliveries, loading, refreshedAt, refresh, assign, accept, pickup, deliver } = useDeliveries(region)
  const activeDelivery = useActiveDelivery(deliveries, session?.id)
  const history = useDeliveryHistory(deliveries, session?.id)

  useEffect(() => {
    if (!user?.referencia_id) return
    const nextSession = {
      id: user.referencia_id,
      name: user.nome,
      phone: '',
      region: DEFAULT_REGION,
    }
    setSession(nextSession)
    saveSession(nextSession)
  }, [user, setSession])

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

  const handleLogout = () => {
    delivererLogout()
    authLogout()
    navigate('/login')
  }

  if (!session) {
    return <Loading label="Carregando painel do entregador..." />
  }

  return (
    <AppShell>
      {header}

      {tab === 'dashboard' && (
        <DashboardPage
          session={session}
          region={region}
          loading={loading}
          refreshedAt={refreshedAt}
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
          onAdvanceStatus={async () => {
            await refresh()
            setTab('active')
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
          onAdvanced={async (completed) => {
            await refresh()
            if (completed) {
              setTab('history')
            }
          }}
        />
      )}

      {tab === 'history' && <HistoryPage deliveries={history} />}

      {tab === 'profile' && (
        <ProfilePage
          session={session}
          onLogout={handleLogout}
          onUseProfileRegion={() => setRegion(session.region)}
        />
      )}
    </AppShell>
  )
}

export default DelivererRoutes
