import React, { type FC, type ReactElement, useState } from 'react'
import { type TCar } from '../../types/types'
import Button from '../Button'
import EditField from '../EditField'
import { MapContainer, Marker, Popup, TileLayer } from 'react-leaflet'
import Map from '../Map'

interface CardItemProps {
  car: TCar
  onDelete: (id: TCar['id']) => void
}

const CardItem: FC<CardItemProps> = ({ car, onDelete }): ReactElement => {
  const [editedCar, setEditedCar] = useState<TCar>({ ...car })
  const [isEditing, setIsEditing] = useState<boolean>(false)
  const [keyToEdit, setKeyToEdit] = useState<keyof TCar | null>(null)

  const handleEdit = (valueToEdit: keyof TCar) => () => {
    setKeyToEdit(valueToEdit)
    setIsEditing(true)
  }

  const handleApply = (valueToApply: keyof TCar) => (newValue: TCar[keyof TCar]) => {
    setEditedCar({ ...editedCar, [valueToApply]: newValue })
    setIsEditing(false)
    setKeyToEdit(null)
  }

  const handleDiscard = (): void => {
    setIsEditing(false)
    setKeyToEdit(null)
  }

  return (
    <li className="car">
      <p className="car__name">{editedCar.name}
        {keyToEdit !== 'name' && <Button onClick={handleEdit('name')} type={'rename'} text={'редактировать'}/>}
        {isEditing && keyToEdit === 'name' &&
          <EditField defaultValue={editedCar.name}
                     inputType={'text'}
                     onApply={handleApply('name')}
                     onDiscard={handleDiscard}/>}
      </p>
      <p className="car__model">{editedCar.model}
        {keyToEdit !== 'model' && <Button onClick={handleEdit('model')} type={'rename'} text={'редактировать'}/>}
        {isEditing && keyToEdit === 'model' &&
          <EditField defaultValue={editedCar.model}
                     inputType={'text'}
                     onApply={handleApply('model')}
                     onDiscard={handleDiscard}/>}
      </p>
      <p className="car__year">Год выпуска: {editedCar.year}</p>
      <p className="car__color">Цвет: {editedCar.color}</p>
      <p className="car__price">Цена: {editedCar.price}
        {keyToEdit !== 'price' && <Button onClick={handleEdit('price')} type={'rename'} text={'редактировать'}/>}
        {isEditing && keyToEdit === 'price' &&
          <EditField defaultValue={editedCar.price}
                     inputType={'number'}
                     onApply={handleApply('price')}
                     onDiscard={handleDiscard}/>}
      </p>
      <div className="car__coordinates">
        <p className="car__latitude">Широта: {editedCar.latitude}</p>
        <p className="car__longitude">Долгота: {editedCar.longitude}</p>
      </div>
      <Map car={car} />
      <Button onClick={() => onDelete(car.id)} type={'remove'} text={'Удалить'} />
    </li>
  )
}

export default CardItem
