import api from './api'

export async function login(email, password) {
  const body = new URLSearchParams({ username: email, password })
  const { data } = await api.post('/auth/login', body, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } })
  localStorage.setItem('access_token', data.access_token)
  return data
}

export async function register(payload) {
  return (await api.post('/auth/register', payload)).data
}

export function logout() { localStorage.removeItem('access_token') }
