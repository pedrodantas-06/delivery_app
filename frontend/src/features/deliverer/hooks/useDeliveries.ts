import { useCallback, useEffect, useMemo, useState } from 'react'
import { getDeliverers } from '../api/delivererApi'
import { assignDelivery, acceptDelivery, deliverDelivery, getDeliveries, pickupDelivery } from '../api/deliveryApi'
import { getAvailableDeliveries } from '../services/deliveryService'
import { POLLING_INTERVAL_MS } from '../constants'
import type { Delivery, Deliverer } from '../types'

export function useDeliveries(region: string) {
  const [deliverers, setDeliverers] = useState<Deliverer[]>([])
  const [deliveries, setDeliveries] = useState<Delivery[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [refreshedAt, setRefreshedAt] = useState<string | null>(null)

  const refresh = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const [nextDeliverers, nextDeliveries] = await Promise.all([
        getDeliverers(region),
        getDeliveries(region),
      ])
      setDeliverers(nextDeliverers)
      setDeliveries(nextDeliveries)
      setRefreshedAt(new Date().toISOString())
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : 'Erro inesperado')
    } finally {
      setLoading(false)
    }
  }, [region])

  useEffect(() => {
    void refresh()
    const timer = window.setInterval(() => void refresh(), POLLING_INTERVAL_MS)
    return () => window.clearInterval(timer)
  }, [refresh])

  const availableDeliveries = useMemo(() => getAvailableDeliveries(deliveries), [deliveries])

  return {
    deliverers,
    deliveries,
    availableDeliveries,
    loading,
    error,
    refreshedAt,
    refresh,
    assign: assignDelivery,
    accept: acceptDelivery,
    pickup: pickupDelivery,
    deliver: deliverDelivery,
  }
}
