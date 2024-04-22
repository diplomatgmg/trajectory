import React, { type FC, type ReactElement } from 'react'
import type { Ordering, TCar } from '../../types/types'

interface SortItemProps {
  text: string
  fieldName: keyof TCar
  orderType: 'asc' | 'desc'
  changeOrdering: (newOrdering: Ordering) => void
}

const SortItem: FC<SortItemProps> = ({ text, fieldName, orderType, changeOrdering }): ReactElement => {
  const orderSymbol = orderType === 'asc' ? '↓' : '↑'

  const handleChangeOrdering = (): void => {
    changeOrdering({
      field: fieldName,
      direction: orderType
    })
  }

  return <li className="sort__item" onClick={handleChangeOrdering}>{text} {orderSymbol}</li>
}

export default SortItem
