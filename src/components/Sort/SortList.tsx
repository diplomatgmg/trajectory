import { type ReactElement } from 'react'
import SortItem from './SortItem'

const SortList = (): ReactElement => {

  return (
    <ul className="cart__sort sort">
      Сортировать по:
      <SortItem text={'году'} orderType={'asc'}/>
      <SortItem text={'году'} orderType={'desc'}/>
      <SortItem text={'цене'} orderType={'asc'}/>
      <SortItem text={'цене'} orderType={'desc'}/>
    </ul>
  )
}

export default SortList
