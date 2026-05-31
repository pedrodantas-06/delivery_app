import { useCallback, useState } from 'react'
import { createDeliverer, updateDelivererStatus } from '../api/delivererApi'
import { clearSession, loadSession, saveSession } from '../services/delivererService'
import type { DelivererLoginForm, DelivererSession, DelivererStatus } from '../types'

export function useDeliverer() {
  const [session, setSession] = useState<DelivererSession | null>(() => loadSession())
  const [error, setError] = useState('')

  const login = useCallback(async (form: DelivererLoginForm) => {
    setError('')
    try {
      const deliverer = await createDeliverer(form)
      const nextSession = {
        id: deliverer.id,
        name: deliverer.name,
        phone: deliverer.phone,
        region: deliverer.region,
      }
      setSession(nextSession)
      saveSession(nextSession)
      return nextSession
    } catch (cause) {
      const message = cause instanceof Error ? cause.message : 'Erro inesperado'
      setError(message)
      throw cause instanceof Error ? cause : new Error(message)
    }
  }, [])

  const logout = useCallback(() => {
    clearSession()
    setSession(null)
  }, [])

  const changeStatus = useCallback(async (status: DelivererStatus) => {
    if (!session) {
      throw new Error('Session not found')
    }
    const deliverer = await updateDelivererStatus(session.id, status)
    const nextSession = {
      id: deliverer.id,
      name: deliverer.name,
      phone: deliverer.phone,
      region: deliverer.region,
    }
    setSession(nextSession)
    saveSession(nextSession)
    return nextSession
  }, [session])

  return {
    session,
    error,
    login,
    logout,
    changeStatus,
    setSession,
  }
}
