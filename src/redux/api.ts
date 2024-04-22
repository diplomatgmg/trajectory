import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import { type TCar } from '../types/types'

const api = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({
    baseUrl: 'https://test.tspb.su/test-task'
  }),
  endpoints: (build) => ({
    getVehicles: build.query<TCar[], unknown>({
      query: () => 'vehicles'
    })
  })
})

export const {
  useGetVehiclesQuery
} = api

export default api
