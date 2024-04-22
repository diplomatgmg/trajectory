import { type ReactElement, useState } from 'react'
import './style.scss'
import CarList from './components/Card/CarList'
import SortList from './components/Sort/SortList'
import { type Ordering } from './types/types'

const App = (): ReactElement => {
  const [ordering, setOrdering] = useState<Ordering | null>(null)

  /*
  Сортировка должна приходить с бекенда.
  Приходится использовать такой костыль
  */

  return (
    <div className="cars container">
      <h1 className="cars__title">Список автомобилей</h1>
      <SortList changeOrdering={setOrdering}/>
      <CarList ordering={ordering}/>
    </div>
  )
}

export default App
