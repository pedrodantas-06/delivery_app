import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { AuthProvider } from '../../../app/providers/AuthProvider'
import LoginPage from '../pages/LoginPage'

function renderLoginPage() {
  return render(
    <AuthProvider>
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    </AuthProvider>,
  )
}

describe('LoginPage', () => {
  beforeEach(() => {
    localStorage.clear()
    global.fetch = jest.fn()
  })

  it('renders email and password form', () => {
    const { container } = renderLoginPage()

    expect(screen.getByText('Entre na plataforma')).toBeInTheDocument()
    expect(container.querySelector('[data-cy="email"]')).toBeInTheDocument()
    expect(container.querySelector('[data-cy="password"]')).toBeInTheDocument()
    expect(container.querySelector('[data-cy="login-submit"]')).toBeInTheDocument()
  })

  it('submits credentials to auth login endpoint', async () => {
    ;(global.fetch as jest.Mock).mockResolvedValue({
      ok: true,
      json: async () => ({
        access_token: 'token-demo',
        user: {
          id: 1,
          nome: 'Cliente Demo',
          email: 'cliente@yummicious.com',
          role: 'CLIENTE',
          referencia_id: 'cli_demo_001',
        },
      }),
    })

    const { container } = renderLoginPage()

    fireEvent.change(container.querySelector('[data-cy="email"]')!, {
      target: { value: 'cliente@yummicious.com' },
    })
    fireEvent.change(container.querySelector('[data-cy="password"]')!, {
      target: { value: '123456' },
    })
    fireEvent.click(container.querySelector('[data-cy="login-submit"]')!)

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith('/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: 'cliente@yummicious.com', senha: '123456' }),
      })
    })
  })
})
