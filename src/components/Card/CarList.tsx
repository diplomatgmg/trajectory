import { type ReactElement } from 'react'
import CarItem from './CarItem'
import { useGetVehiclesQuery } from '../../redux/api'

const CarList = (): ReactElement => {
  const {
    data = [],
    isLoading
  } = useGetVehiclesQuery({})

  if (isLoading) {
    return <h1 style={{ textAlign: 'center' }}>Loading...</h1>
  }

  return (
    <ul className="cars__list">
      {data.map(car => <CarItem car={car} key={car.id}/>)}
    </ul>
  )
}

export default CarList
