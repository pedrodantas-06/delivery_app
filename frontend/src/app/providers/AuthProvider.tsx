import { createContext, useContext, useState, useCallback, type ReactNode } from 'react'

export type UserRole = 'CLIENTE' | 'RESTAURANTE' | 'ENTREGADOR' | 'ADMIN'

export interface AuthUser {
  id: number
  nome: string
  email: string
  role: UserRole
  referencia_id: string | null
}

interface AuthContextValue {
  user: AuthUser | null
  token: string | null
  login: (email: string, senha: string) => Promise<UserRole>
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | null>(null)
const STORAGE_KEY = 'yummicious_auth'

export function AuthProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState(() => {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : { user: null, token: null }
  })

  const login = useCallback(async (email: string, senha: string) => {
    const res = await fetch('/api/v1/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, senha }),
    })
    if (!res.ok) throw new Error('Credenciais inválidas')
    const data = await res.json()
    const next = { user: data.user, token: data.access_token }
    localStorage.setItem(STORAGE_KEY, JSON.stringify(next))
    setState(next)
    return data.user.role as UserRole
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem(STORAGE_KEY)
    setState({ user: null, token: null })
  }, [])

  return (
    <AuthContext.Provider value={{ ...state, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth outside AuthProvider')
  return ctx
}
