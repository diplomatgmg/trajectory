import React, { type FC, type ReactElement } from 'react'
import { type TCar } from '../../types/types'

interface CardItemProps {
  car: TCar
}

const CardItem: FC<CardItemProps> = ({ car }): ReactElement => {

  return (
    <li className="car">
      <p className="car__name">{car.name}
        <button className="btn btn__rename">редактировать</button>
      </p>
      <p className="car__model">{car.model}
        <label>
          <input type="text" value="CamryNew"/>
        </label>
        <button className="btn btn__apply">✓</button>
        <button className="btn btn__discard">×</button>
      </p>
      <p className="car__year">Год выпуска: {car.year}</p>
      <p className="car__color">Цвет: {car.color}</p>
      <p className="car__price">Цена: {car.price}
        <button className="btn btn__rename">редактировать</button>
      </p>
      <div className="car__coordinates">
        <p className="car__latitude">Широта: {car.latitude}</p>
        <p className="car_longitude">Долгота: {car.longitude}</p>
      </div>
      <button className="btn btn__remove">Удалить</button>
    </li>
  )
}

export default CardItem
