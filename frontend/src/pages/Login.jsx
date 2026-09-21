import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
export default function Login() {
  const { login } = useAuth(); const navigate = useNavigate(); const [form, setForm] = useState({ email: '', password: '' }); const [error, setError] = useState('')
  const submit = async (event) => { event.preventDefault(); setError(''); try { await login(form.email, form.password); navigate('/dashboard') } catch (err) { setError(err.response?.data?.detail || 'Unable to sign in') } }
  return <main className="auth-shell"><form className="auth-panel" onSubmit={submit}><p className="eyebrow">WARRANTY REGISTRATION PORTAL</p><h1>Keep every purchase protected.</h1><p className="text-secondary">Sign in to manage registered products and active coverage.</p>{error && <div className="alert alert-danger">{error}</div>}<input className="form-control" type="email" placeholder="Email" required onChange={e => setForm({ ...form, email: e.target.value })} /><input className="form-control" type="password" placeholder="Password" required onChange={e => setForm({ ...form, password: e.target.value })} /><button className="btn btn-dark w-100">Sign in</button><p className="small text-center">New here? <Link to="/register">Create an account</Link></p></form></main>
}
