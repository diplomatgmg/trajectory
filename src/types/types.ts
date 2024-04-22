interface TCar {
  id: number
  name: string
  model: string
  year: number
  color: string
  price: number
  latitude: number
  longitude: number
}

interface Ordering {
  field: keyof TCar
  direction: 'asc' | 'desc'
}

export type { TCar, Ordering }
