import { useEffect, useState } from 'react'
import api from '../services/api'

export default function AdminDashboard() {
  const [data, setData] = useState({ registrations: [], warranties: [], claims: [] })
  const [error, setError] = useState('')

  useEffect(() => {
    Promise.all([
      api.get('/admin/registrations'),
      api.get('/admin/warranties'),
      api.get('/admin/claims'),
    ])
      .then(([registrations, warranties, claims]) => setData({
        registrations: registrations.data.data,
        warranties: warranties.data.data,
        claims: claims.data.data,
      }))
      .catch(() => setError('Unable to load admin data'))
  }, [])

  return <main className="container page">
    <p className="eyebrow">ADMIN OPERATIONS</p>
    <h1>Warranty overview</h1>
    {error && <div className="alert alert-danger">{error}</div>}
    <div className="row g-3 my-3">
      <div className="col-md-4"><article className="product-tile"><strong>{data.registrations.length}</strong><p className="mb-0">Registrations</p></article></div>
      <div className="col-md-4"><article className="product-tile"><strong>{data.warranties.length}</strong><p className="mb-0">Warranties</p></article></div>
      <div className="col-md-4"><article className="product-tile"><strong>{data.claims.length}</strong><p className="mb-0">Claims</p></article></div>
    </div>
    <h2>Claims</h2>
    {data.claims.map(claim => <article className="claim-row" key={claim.id}><strong>{claim.status}</strong><span>{claim.issue_description}</span><small>{claim.admin_remarks || 'No remarks'}</small></article>)}
  </main>
}