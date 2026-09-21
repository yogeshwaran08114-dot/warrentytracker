import { Navigate, Outlet } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
export default function ProtectedRoute({ admin = false }) {
  const { user, loading } = useAuth()
  if (loading) return <main className="container py-5">Loading...</main>
  if (!user) return <Navigate to="/login" replace />
  if (admin && user.role !== 'admin') return <Navigate to="/dashboard" replace />
  return <Outlet />
}
