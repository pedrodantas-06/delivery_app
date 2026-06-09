import { render, screen } from '@testing-library/react'
import DelivererHeader from '../components/DelivererHeader'

describe('DelivererHeader', () => {
  it('renders the mobile shell affordances', () => {
    render(
      <DelivererHeader
        title="Ana"
        subtitle="Região atual: Zona Sul"
        actions={[{ label: 'Dashboard', active: true, onClick: () => {} }]}
      />,
    )

    expect(screen.getByText('Painel do entregador')).toBeInTheDocument()
    expect(screen.getByText('Ao vivo')).toBeInTheDocument()
    expect(screen.getByText('Mobile first')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Dashboard' })).toBeInTheDocument()
  })
})
