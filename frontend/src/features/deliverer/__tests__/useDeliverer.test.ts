import { act, renderHook, waitFor } from '@testing-library/react'
import { useDeliverer } from '../hooks/useDeliverer'
import { clearSession, loadSession, saveSession } from '../services/delivererService'
import { createDeliverer, updateDelivererStatus } from '../api/delivererApi'

jest.mock('../services/delivererService', () => ({
  loadSession: jest.fn(),
  saveSession: jest.fn(),
  clearSession: jest.fn(),
}))

jest.mock('../api/delivererApi', () => ({
  createDeliverer: jest.fn(),
  updateDelivererStatus: jest.fn(),
}))

describe('useDeliverer', () => {
  beforeEach(() => {
    jest.clearAllMocks()
    ;(loadSession as jest.Mock).mockReturnValue({
      id: 'deliverer-1',
      name: 'Ana',
      phone: '11999999999',
      region: 'Zona Sul',
    })
  })

  it('loads the session and supports login, status change and logout', async () => {
    ;(createDeliverer as jest.Mock).mockResolvedValue({
      id: 'deliverer-2',
      name: 'Bia',
      phone: '11888888888',
      region: 'Centro',
      status: 'AVAILABLE',
    })
    ;(updateDelivererStatus as jest.Mock).mockResolvedValue({
      id: 'deliverer-2',
      name: 'Bia',
      phone: '11888888888',
      region: 'Centro',
      status: 'BUSY',
    })

    const { result } = renderHook(() => useDeliverer())

    expect(result.current.session?.name).toBe('Ana')

    await act(async () => {
      await result.current.login({ name: 'Bia', phone: '11888888888', region: 'Centro' })
    })

    await waitFor(() => {
      expect(saveSession).toHaveBeenCalled()
    })
    expect(createDeliverer).toHaveBeenCalledWith({ name: 'Bia', phone: '11888888888', region: 'Centro' })
    expect(result.current.session?.region).toBe('Centro')

    await act(async () => {
      await result.current.changeStatus('BUSY')
    })

    expect(updateDelivererStatus).toHaveBeenCalledWith('deliverer-2', 'BUSY')
    expect(result.current.session?.name).toBe('Bia')

    act(() => {
      result.current.logout()
    })

    expect(clearSession).toHaveBeenCalled()
    expect(result.current.session).toBeNull()
  })
})
