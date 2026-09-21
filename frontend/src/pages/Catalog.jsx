import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { getProducts } from '../services/productService'

export default function Catalog() {
  const [products, setProducts] = useState([])
  const [query, setQuery] = useState('')
  const [brand, setBrand] = useState('all')
  const [error, setError] = useState('')

  useEffect(() => {
    getProducts().then(setProducts).catch(() => setError('Unable to load the product catalog'))
  }, [])

  const brands = useMemo(
    () => [...new Set(products.map(product => product.brand))].sort(),
    [products],
  )

  const filteredProducts = useMemo(() => {
    const normalizedQuery = query.trim().toLowerCase()
    return products.filter(product => {
      const matchesBrand = brand === 'all' || product.brand === brand
      const matchesQuery = !normalizedQuery || [
        product.product_name,
        product.brand,
        product.model_number,
      ].some(value => value.toLowerCase().includes(normalizedQuery))
      return matchesBrand && matchesQuery
    })
  }, [brand, products, query])

  return <main className="container page">
    <div className="catalog-heading">
      <div>
        <p className="eyebrow">PRODUCT CATALOG</p>
        <h1>Choose what you own</h1>
        <p className="catalog-intro">Browse the supported product range, then register a purchase to track its warranty.</p>
      </div>
      <Link className="btn btn-dark" to="/register-product">Register a product</Link>
    </div>

    {error && <div className="alert alert-danger">{error}</div>}

    <div className="catalog-filters" role="search">
      <input
        className="form-control"
        aria-label="Search products"
        placeholder="Search by product, brand, or model"
        value={query}
        onChange={event => setQuery(event.target.value)}
      />
      <select className="form-select" aria-label="Filter by brand" value={brand} onChange={event => setBrand(event.target.value)}>
        <option value="all">All brands</option>
        {brands.map(item => <option key={item} value={item}>{item}</option>)}
      </select>
    </div>

    {filteredProducts.length === 0
      ? <div className="empty-state">No products match your search.</div>
      : <div className="catalog-grid">{filteredProducts.map(product => <article className="catalog-card" key={product.id}>
        <div className="catalog-card-topline"><span className="catalog-brand">{product.brand}</span><span className="catalog-warranty">{product.default_warranty_months} months</span></div>
        <h2>{product.product_name}</h2>
        <p className="catalog-model">Model {product.model_number}</p>
        <p className="catalog-copy">Manufacturer coverage is calculated automatically when you register this product.</p>
      </article>)}</div>}
  </main>
}
