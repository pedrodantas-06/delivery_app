import { DELIVERER_SESSION_STORAGE_KEY } from '../constants'
import type { DelivererSession } from '../types'

export function loadSession(): DelivererSession | null {
  const raw = window.localStorage.getItem(DELIVERER_SESSION_STORAGE_KEY)
  return raw ? (JSON.parse(raw) as DelivererSession) : null
}

export function saveSession(session: DelivererSession) {
  window.localStorage.setItem(DELIVERER_SESSION_STORAGE_KEY, JSON.stringify(session))
}

export function clearSession() {
  window.localStorage.removeItem(DELIVERER_SESSION_STORAGE_KEY)
}
