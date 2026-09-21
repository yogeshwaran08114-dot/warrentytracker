import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
export default function Navbar() {
  const { user, logout } = useAuth()
  return <nav className="navbar navbar-expand-lg border-bottom bg-white"><div className="container"><Link className="navbar-brand fw-bold" to="/dashboard">WarrantyHub</Link><div className="d-flex align-items-center gap-3">{user && <><Link to="/catalog">Catalog</Link><Link to="/products">My Products</Link><Link to="/claims">Claims</Link>{user.role === 'admin' && <Link to="/admin">Admin</Link>}<button className="btn btn-outline-dark btn-sm" onClick={logout}>Sign out</button></>}</div></div></nav>
}
