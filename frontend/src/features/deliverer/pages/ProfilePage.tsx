import { useMemo } from 'react'
import type { DelivererSession } from '../types'
import ProfileCard from '../components/ProfileCard'

type ProfilePageProps = {
  session: DelivererSession
  onLogout: () => void
  onUseProfileRegion: () => void
}

function ProfilePage({ session, onLogout, onUseProfileRegion }: ProfilePageProps) {
  const currentSession = useMemo(() => session, [session])
  return <ProfileCard session={currentSession} onLogout={onLogout} onUseProfileRegion={onUseProfileRegion} />
}

export default ProfilePage
