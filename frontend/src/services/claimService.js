import api from './api'
export const getClaims = () => api.get('/claims/my').then(({ data }) => data.data)
export const createClaim = (payload) => api.post('/claims', payload).then(({ data }) => data.data)
