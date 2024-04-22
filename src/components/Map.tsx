import React, { type FC, type ReactElement } from 'react'
import { type TCar } from '../types/types'
import { MapContainer, Marker, Popup, TileLayer } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'

interface MapProps {
  car: TCar
}

const Map: FC<MapProps> = ({ car }): ReactElement => {
  return (
    <MapContainer center={[car.latitude, car.longitude]} zoom={13} style={{ height: '200px' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <Marker position={[car.latitude, car.longitude]}>
        <Popup>
          {car.name}
        </Popup>
      </Marker>
    </MapContainer>
  )
}

export default Map
