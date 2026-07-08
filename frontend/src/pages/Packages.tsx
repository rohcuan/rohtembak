import { useState, useEffect } from 'react'
import { packagesApi, purchaseApi } from '../api/client'
import './Packages.css'

function Packages() {
  const [families, setFamilies] = useState<any[]>([])
  const [selectedFamily, setSelectedFamily] = useState<string>('')
  const [packages, setPackages] = useState<any[]>([])
  const [myPackages, setMyPackages] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  useEffect(() => {
    loadFamilies()
    loadMyPackages()
  }, [])

  const loadFamilies = async () => {
    try {
      const res = await packagesApi.getFamilies()
      setFamilies(res.data.data || [])
    } catch (err) {
      console.error('Error loading families:', err)
    }
  }

  const loadMyPackages = async () => {
    try {
      const res = await packagesApi.getMyPackages()
      setMyPackages(Array.isArray(res.data.data) ? res.data.data : [])
    } catch (err) {
      console.error('Error loading my packages:', err)
    }
  }

  const handleSelectFamily = async (code: string) => {
    setSelectedFamily(code)
    setLoading(true)
    try {
      const res = await packagesApi.getFamily(code)
      setPackages(res.data.data || [])
    } catch (err) {
      setError('Gagal memuat paket')
    } finally {
      setLoading(false)
    }
  }

  const handlePurchase = async (optionCode: string) => {
    if (!confirm('Beli paket ini dengan pulsa?')) return
    setLoading(true)
    setError('')
    setSuccess('')
    try {
      const res = await purchaseApi.buyWithBalance(optionCode)
      setSuccess('Pembelian berhasil!')
      loadMyPackages()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Pembelian gagal')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="packages-page">
      <h2>Paket Data</h2>

      <div className="my-packages-section">
        <h3>Paket Aktif</h3>
        {myPackages.length === 0 ? (
          <p className="empty-message">Belum ada paket aktif</p>
        ) : (
          <div className="my-packages-grid">
            {myPackages.map((pkg, idx) => (
              <div key={idx} className="my-package-card">
                <h4>{pkg.name || 'Paket'}</h4>
                <p>{pkg.quota || pkg.volume || '-'}</p>
                {pkg.expired && <span className="expiry">s/d {pkg.expired}</span>}
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="browse-section">
        <h3>Beli Paket Baru</h3>
        <div className="family-list">
          {families.map((fam) => (
            <button
              key={fam.code}
              className={`family-btn ${selectedFamily === fam.code ? 'active' : ''}`}
              onClick={() => handleSelectFamily(fam.code)}
            >
              {fam.name}
            </button>
          ))}
        </div>

        {loading && <p>Memuat...</p>}
        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}

        {packages.length > 0 && (
          <div className="packages-grid">
            {packages.map((pkg, idx) => (
              <div key={idx} className="package-card">
                <h4>{pkg.name}</h4>
                <p className="price">{pkg.price || '-'}</p>
                <p className="validity">{pkg.validity || '-'}</p>
                <button onClick={() => handlePurchase(pkg.option_code)} disabled={loading}>
                  Beli
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default Packages
