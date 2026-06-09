import Button from '../../../shared/components/Button'

type DelivererHeaderProps = {
  title: string
  subtitle: string
  actions?: Array<{
    label: string
    active: boolean
    onClick: () => void
  }>
}

function DelivererHeader({ title, subtitle, actions = [] }: DelivererHeaderProps) {
  return (
    <section className="hero hero--compact shell-header">
      <div className="shell-header__copy">
        <p className="eyebrow">Painel do entregador</p>
        <h1 className="title">{title}</h1>
        <p className="subtitle">{subtitle}</p>
      </div>
      <div className="shell-header__meta">
        <span className="status-chip status-chip--live">Ao vivo</span>
        <span className="status-chip status-chip--soft">Mobile first</span>
      </div>
      <div className="hero__actions shell-header__actions">
        {actions.map((action) => (
          <Button key={action.label} variant={action.active ? 'primary' : 'secondary'} onClick={action.onClick}>
            {action.label}
          </Button>
        ))}
      </div>
    </section>
  )
}

export default DelivererHeader
