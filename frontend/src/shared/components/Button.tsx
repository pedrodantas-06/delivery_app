import type { ButtonHTMLAttributes, PropsWithChildren } from 'react'

type Variant = 'primary' | 'secondary' | 'ghost'

type ButtonProps = PropsWithChildren<
  ButtonHTMLAttributes<HTMLButtonElement> & {
    variant?: Variant
    fullWidth?: boolean
  }
>

function Button({ variant = 'primary', fullWidth = false, className = '', children, ...props }: ButtonProps) {
  return (
    <button
      className={`btn btn--${variant} ${fullWidth ? 'btn--full' : ''} ${className}`.trim()}
      {...props}
    >
      {children}
    </button>
  )
}

export default Button
