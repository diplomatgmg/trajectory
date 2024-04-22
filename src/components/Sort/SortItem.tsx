import React, { type FC, type ReactElement } from 'react'

interface SortItemProps {
  text: string
  orderType: 'asc' | 'desc'
}

const SortItem: FC<SortItemProps> = ({ text, orderType }): ReactElement => {
  const orderSymbol = orderType === 'asc' ? '↓' : '↑'

  return <li className="sort__item">{text} {orderSymbol}</li>
}

export default SortItem
