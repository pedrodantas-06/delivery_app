import type { ReactNode } from 'react'
import Button from './Button'

type TopBarProps = {
  title: string
  subtitle?: string
  actions?: ReactNode
  onLogout?: () => void
}

function TopBar({ title, subtitle, actions, onLogout }: TopBarProps) {
  return (
    <header className="section-head section-head--spaced">
      <div>
        <h2>{title}</h2>
        {subtitle && <p>{subtitle}</p>}
      </div>
      {(actions || onLogout) && (
        <div className="actions">
          {actions}
          {onLogout && (
            <Button variant="secondary" onClick={onLogout}>
              Sair
            </Button>
          )}
        </div>
      )}
    </header>
  )
}

export default TopBar
