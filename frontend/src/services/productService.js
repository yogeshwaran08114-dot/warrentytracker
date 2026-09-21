import api from './api'

export const getProducts = () => api.get('/products').then(({ data }) => data.data)
