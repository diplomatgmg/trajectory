import React, { type FC, type ReactElement } from 'react'

interface ButtonProps {
  onClick: () => void
  type: 'apply' | 'discard' | 'remove' | 'rename'
  text: string
}
const Button: FC<ButtonProps> = ({ onClick, type, text }): ReactElement => {
  const className = `btn btn__${type}`
  return <button className={className} onClick={onClick}>{text}</button>
}

export default Button
