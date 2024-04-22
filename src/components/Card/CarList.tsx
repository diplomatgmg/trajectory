import { type FC, type ReactElement, useEffect, useMemo, useState } from 'react'
import CarItem from './CarItem'
import { useGetVehiclesQuery } from '../../redux/api'
import { type Ordering, type TCar } from '../../types/types'
import _ from 'lodash'

interface CarListProps {
  ordering: Ordering | null
}

const CarList: FC<CarListProps> = ({ ordering }): ReactElement => {
  const {
    data = [],
    isLoading
  } = useGetVehiclesQuery({})

  // Говнокод ON
  const [cars, setCars] = useState<TCar[]>([])

  useEffect(() => {
    if (data.length > 0) {
      setCars([...data])
    }
  }, [data])

  const sortedCars = useMemo(() => {
    if (ordering === null) return cars

    const { field, direction } = ordering
    return _.orderBy(cars, [field], [direction])
  }, [cars, ordering])

  const handleDelete = (id: TCar['id']): void => {
    const filteredCars = _.filter(cars, car => car.id !== id)
    setCars(filteredCars)
  }

  // Говнокод OFF
  /*
    Надеюсь, кровь из глаз не пошла после выше увиденного.
    В идеале, должен быть эндпоинт для удаления, в таком случае можно было использовать useMutation
    из rtk-query, но в тз нужного эндпоинта нет, поэтому пришлось придумать такую "прелесть".
    Также, можно было использовать store и localStorage (redux-persist)
    для сохранения удаленных автомобилей при перезагрузке странице, но в рамках этого тз это явно лишнее.
  */

  if (isLoading) {
    return <h1 style={{ textAlign: 'center' }}>Loading...</h1>
  }

  return (
    <ul className="cars__list">
      {sortedCars.map(car => <CarItem car={car} key={car.id} onDelete={handleDelete}/>)}
    </ul>
  )
}

export default CarList
