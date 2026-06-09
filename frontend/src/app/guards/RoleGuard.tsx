import { Navigate } from 'react-router-dom'
import { useAuth, type UserRole } from '../providers/AuthProvider'

type RoleGuardProps = {
  allowed: UserRole[]
  children: React.ReactNode
}

export function RoleGuard({ allowed, children }: RoleGuardProps) {
  const { user } = useAuth()
  if (!user) return <Navigate to="/login" replace />
  if (!allowed.includes(user.role) && user.role !== 'ADMIN') return <Navigate to="/login" replace />
  return <>{children}</>
}
