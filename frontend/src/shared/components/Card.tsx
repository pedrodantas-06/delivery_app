import type { PropsWithChildren } from 'react'

type CardProps = PropsWithChildren<{
  className?: string
}>

function Card({ className = '', children }: CardProps) {
  return <article className={`card ${className}`.trim()}>{children}</article>
}

export default Card
