import { createContext, useCallback, useContext, useMemo, useState, type ReactNode } from 'react'
import type { CartItem } from '../types'

interface CartState {
  items: CartItem[]
  restaurantId: number | null
  restaurantName: string | null
}

interface CartContextValue extends CartState {
  total: number
  addItem: (item: Omit<CartItem, 'quantidade'>, restaurantId: number, restaurantName: string) => void
  removeItem: (itemId: number) => void
  clear: () => void
}

const emptyCart: CartState = {
  items: [],
  restaurantId: null,
  restaurantName: null,
}

const CartContext = createContext<CartContextValue | null>(null)

export function CartProvider({ children }: { children: ReactNode }) {
  const [cart, setCart] = useState<CartState>(emptyCart)

  const addItem = useCallback(
    (item: Omit<CartItem, 'quantidade'>, nextRestaurantId: number, nextRestaurantName: string) => {
      setCart((current) => {
        const switching =
          current.restaurantId !== null && current.restaurantId !== nextRestaurantId
        const baseItems = switching ? [] : current.items
        const existing = baseItems.find((entry) => entry.id === item.id)
        const items = existing
          ? baseItems.map((entry) =>
              entry.id === item.id ? { ...entry, quantidade: entry.quantidade + 1 } : entry,
            )
          : [...baseItems, { ...item, quantidade: 1 }]

        return {
          items,
          restaurantId: nextRestaurantId,
          restaurantName: nextRestaurantName,
        }
      })
    },
    [],
  )

  const removeItem = useCallback((itemId: number) => {
    setCart((current) => {
      const items = current.items
        .map((entry) =>
          entry.id === itemId ? { ...entry, quantidade: entry.quantidade - 1 } : entry,
        )
        .filter((entry) => entry.quantidade > 0)

      if (items.length === 0) {
        return emptyCart
      }

      return { ...current, items }
    })
  }, [])

  const clear = useCallback(() => {
    setCart(emptyCart)
  }, [])

  const total = useMemo(
    () => cart.items.reduce((sum, item) => sum + item.preco * item.quantidade, 0),
    [cart.items],
  )

  const value = useMemo(
    () => ({
      ...cart,
      total,
      addItem,
      removeItem,
      clear,
    }),
    [cart, total, addItem, removeItem, clear],
  )

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>
}

export function useCart() {
  const ctx = useContext(CartContext)
  if (!ctx) throw new Error('useCart outside CartProvider')
  return ctx
}
