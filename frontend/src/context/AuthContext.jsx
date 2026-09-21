import { createContext, useContext, useEffect, useState } from 'react'
import api from '../services/api'
import { login as loginRequest, logout as logoutRequest } from '../services/authService'

const AuthContext = createContext(null)
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  useEffect(() => {
    if (!localStorage.getItem('access_token')) return setLoading(false)
    api.get('/auth/me').then(({ data }) => setUser(data)).catch(logoutRequest).finally(() => setLoading(false))
  }, [])
  const login = async (email, password) => { await loginRequest(email, password); const { data } = await api.get('/auth/me'); setUser(data) }
  const logout = () => { logoutRequest(); setUser(null) }
  return <AuthContext.Provider value={{ user, loading, login, logout }}>{children}</AuthContext.Provider>
}
export const useAuth = () => useContext(AuthContext)
