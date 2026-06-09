import type { ElementType, PropsWithChildren } from 'react'

type AppShellProps = PropsWithChildren<{
  as?: ElementType
  className?: string
}>

function AppShell({ as: Component = 'main', className = '', children }: AppShellProps) {
  return <Component className={`page ${className}`.trim()}>{children}</Component>
}

export default AppShell
