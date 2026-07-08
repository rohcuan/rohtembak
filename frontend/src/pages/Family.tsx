import { useState, useEffect } from 'react'
import { familyApi } from '../api/client'
import './Family.css'

function Family() {
  const [familyData, setFamilyData] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  useEffect(() => {
    loadFamilyData()
  }, [])

  const loadFamilyData = async () => {
    setLoading(true)
    try {
      const res = await familyApi.getData()
      setFamilyData(res.data.data)
    } catch (err) {
      setError('Gagal memuat data family plan')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="family-page">
      <h2>Family Plan</h2>

      {loading ? (
        <p>Memuat...</p>
      ) : familyData ? (
        <div className="family-info">
          <div className="info-card">
            <h3>Informasi Family Plan</h3>
            <p><strong>Paket:</strong> {familyData.package_name || '-'}</p>
            <p><strong>Status:</strong> {familyData.status || '-'}</p>
            <p><strong>Quota:</strong> {familyData.quota || '-'}</p>
            <p><strong>Masa Aktif:</strong> {familyData.validity || '-'}</p>
          </div>

          <div className="members-card">
            <h3>Anggota Family ({familyData.members?.length || 0})</h3>
            {familyData.members && familyData.members.length > 0 ? (
              <div className="members-list">
                {familyData.members.map((member: any, idx: number) => (
                  <div key={idx} className="member-item">
                    <div className="member-info">
                      <span className="phone">{member.phone || member.msisdn}</span>
                      {member.is_owner && <span className="badge owner">Owner</span>}
                    </div>
                    <div className="member-quota">
                      <span>Kuota: {member.quota_used || 0} / {member.quota_total || '-'}</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="empty-message">Belum ada anggota</p>
            )}
          </div>
        </div>
      ) : (
        <div className="no-family">
          <p>Anda belum memiliki Family Plan</p>
          <p className="hint">Family Plan memungkinkan Anda berbagi kuota dengan keluarga</p>
        </div>
      )}

      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}
    </div>
  )
}

export default Family
