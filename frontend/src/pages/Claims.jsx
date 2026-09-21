import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getClaims } from '../services/claimService'
export default function Claims() { const [claims, setClaims] = useState([]); useEffect(() => { getClaims().then(setClaims) }, []); return <main className="container page"><div className="d-flex justify-content-between mb-4"><h1>Warranty claims</h1><Link className="btn btn-dark" to="/claims/create">New claim</Link></div>{claims.length === 0 ? <div className="empty-state">No claims submitted.</div> : claims.map(claim => <article className="claim-row" key={claim.id}><strong>{claim.status}</strong><span>{claim.issue_description}</span><small>{claim.claim_date}</small></article>)}</main> }
