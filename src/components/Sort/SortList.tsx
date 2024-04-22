import React, { type FC } from 'react'
import SortItem from './SortItem'
import { type Ordering } from '../../types/types'

interface SortListProps {
  changeOrdering: (newOrdering: Ordering) => void
}

const SortList: FC<SortListProps> = ({ changeOrdering }) => {

  return (
    <ul className="cart__sort sort">
      Сортировать по:
      <SortItem text={'году'} orderType={'asc'} fieldName={'year'} changeOrdering={changeOrdering}/>
      <SortItem text={'году'} orderType={'desc'} fieldName={'year'} changeOrdering={changeOrdering}/>
      <SortItem text={'цене'} orderType={'asc'} fieldName={'price'} changeOrdering={changeOrdering}/>
      <SortItem text={'цене'} orderType={'desc'} fieldName={'price'} changeOrdering={changeOrdering}/>
    </ul>
  )
}

export default SortList
