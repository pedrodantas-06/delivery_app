import { act, renderHook } from '@testing-library/react'
import type { ReactNode } from 'react'
import { CartProvider, useCart } from '../context/CartContext'

function wrapper({ children }: { children: ReactNode }) {
  return <CartProvider>{children}</CartProvider>
}

describe('CartContext', () => {
  it('adds items and calculates total', () => {
    const { result } = renderHook(() => useCart(), { wrapper })

    act(() => {
      result.current.addItem({ id: 1, nome: 'X-Burguer', preco: 25 }, 1, 'Burger House')
    })

    expect(result.current.items).toHaveLength(1)
    expect(result.current.items[0].quantidade).toBe(1)
    expect(result.current.total).toBe(25)
    expect(result.current.restaurantId).toBe(1)
    expect(result.current.restaurantName).toBe('Burger House')
  })

  it('increments quantity for repeated items', () => {
    const { result } = renderHook(() => useCart(), { wrapper })

    act(() => {
      result.current.addItem({ id: 1, nome: 'X-Burguer', preco: 25 }, 1, 'Burger House')
      result.current.addItem({ id: 1, nome: 'X-Burguer', preco: 25 }, 1, 'Burger House')
    })

    expect(result.current.items).toHaveLength(1)
    expect(result.current.items[0].quantidade).toBe(2)
    expect(result.current.total).toBe(50)
  })

  it('removes items and clears restaurant metadata when empty', () => {
    const { result } = renderHook(() => useCart(), { wrapper })

    act(() => {
      result.current.addItem({ id: 1, nome: 'X-Burguer', preco: 25 }, 1, 'Burger House')
      result.current.removeItem(1)
    })

    expect(result.current.items).toHaveLength(0)
    expect(result.current.total).toBe(0)
    expect(result.current.restaurantId).toBeNull()
    expect(result.current.restaurantName).toBeNull()
  })

  it('clears the cart', () => {
    const { result } = renderHook(() => useCart(), { wrapper })

    act(() => {
      result.current.addItem({ id: 1, nome: 'X-Burguer', preco: 25 }, 1, 'Burger House')
      result.current.addItem({ id: 2, nome: 'Coca-Cola', preco: 8 }, 1, 'Burger House')
      result.current.clear()
    })

    expect(result.current.items).toHaveLength(0)
    expect(result.current.total).toBe(0)
    expect(result.current.restaurantId).toBeNull()
  })

  it('resets cart when switching restaurants', () => {
    const { result } = renderHook(() => useCart(), { wrapper })

    act(() => {
      result.current.addItem({ id: 1, nome: 'X-Burguer', preco: 25 }, 1, 'Burger House')
      result.current.addItem({ id: 10, nome: 'Margherita', preco: 45 }, 2, 'Pizza Campus')
    })

    expect(result.current.items).toHaveLength(1)
    expect(result.current.items[0].nome).toBe('Margherita')
    expect(result.current.restaurantId).toBe(2)
    expect(result.current.restaurantName).toBe('Pizza Campus')
    expect(result.current.total).toBe(45)
  })
})
