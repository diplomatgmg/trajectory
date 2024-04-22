import { type ReactElement } from 'react'
import response from '../../response'
import CarItem from './CarItem'
const CarList = (): ReactElement => {

  return (
    <ul className="cars__list">
      {response.map(car => <CarItem car={car} key={car.id} />)}
    </ul>
  )
}

export default CarList
