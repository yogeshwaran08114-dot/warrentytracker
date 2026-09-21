import api from './api'
export const getRegistrations = () => api.get('/registrations/my').then(({ data }) => data.data)
export const registerProduct = (payload) => api.post('/registrations', payload).then(({ data }) => data.data)
export const getWarrantyStatus = (id) => api.get(`/warranties/${id}/status`).then(({ data }) => data.data)
