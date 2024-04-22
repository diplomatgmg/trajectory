import { type ReactElement } from 'react'
import './style.scss'
import CarList from './components/Card/CarList'
import SortList from './components/Sort/SortList'

const App = (): ReactElement => {

  return (
    <div className="cars container">
      <h1 className="cars__title">Список автомобилей</h1>
      <SortList/>
      <CarList/>
    </div>
  )
}

export default App
