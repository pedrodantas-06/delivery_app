import { render, screen } from '@testing-library/react'
import StatusBadge from '../components/StatusBadge'

describe('StatusBadge', () => {
  it('maps delivery and deliverer states to shared badge states', () => {
    render(<StatusBadge status="ASSIGNED" />)

    expect(screen.getByText('BUSY')).toBeInTheDocument()
  })
})
