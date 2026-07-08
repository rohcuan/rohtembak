import { useState, useEffect } from 'react'
import { circleApi } from '../api/client'
import './Circle.css'

function Circle() {
  const [circleData, setCircleData] = useState<any>(null)
  const [members, setMembers] = useState<any[]>([])
  const [bonus, setBonus] = useState<any>(null)
  const [invitePhone, setInvitePhone] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  useEffect(() => {
    loadCircleData()
  }, [])

  const loadCircleData = async () => {
    setLoading(true)
    try {
      const [statusRes, membersRes, bonusRes] = await Promise.all([
        circleApi.getStatus(),
        circleApi.getMembers(),
        circleApi.getBonus()
      ])
      setCircleData(statusRes.data.data)
      setMembers(membersRes.data.data || [])
      setBonus(bonusRes.data.data)
    } catch (err) {
      setError('Gagal memuat data circle')
    } finally {
      setLoading(false)
    }
  }

  const handleInvite = async () => {
    if (!invitePhone) return
    setLoading(true)
    setError('')
    setSuccess('')
    try {
      await circleApi.inviteMember(invitePhone)
      setSuccess('Undangan berhasil dikirim!')
      setInvitePhone('')
      loadCircleData()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Gagal mengirim undangan')
    } finally {
      setLoading(false)
    }
  }

  const handleRemove = async (phone: string) => {
    if (!confirm(`Hapus ${phone} dari circle?`)) return
    setLoading(true)
    try {
      await circleApi.removeMember(phone)
      setSuccess('Member berhasil dihapus')
      loadCircleData()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Gagal menghapus member')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="circle-page">
      <h2>Circle</h2>

      {circleData && (
        <div className="circle-info">
          <div className="info-card">
            <h3>Status Circle</h3>
            <p><strong>Nama:</strong> {circleData.name || '-'}</p>
            <p><strong>Role:</strong> {circleData.role || '-'}</p>
            <p><strong>Members:</strong> {members.length}</p>
          </div>

          {bonus && (
            <div className="info-card">
              <h3>Bonus Circle</h3>
              <p><strong>Total Bonus:</strong> {bonus.total || '-'}</p>
              <p><strong>Terpakai:</strong> {bonus.used || '0'}</p>
              <p><strong>Sisa:</strong> {bonus.remaining || '-'}</p>
            </div>
          )}
        </div>
      )}

      <div className="invite-section">
        <h3>Invite Member</h3>
        <div className="invite-form">
          <input
            type="text"
            placeholder="Nomor HP (628xxx)"
            value={invitePhone}
            onChange={(e) => setInvitePhone(e.target.value)}
            disabled={loading}
          />
          <button onClick={handleInvite} disabled={loading}>
            {loading ? 'Mengirim...' : 'Invite'}
          </button>
        </div>
      </div>

      <div className="members-section">
        <h3>Members ({members.length})</h3>
        {loading ? (
          <p>Memuat...</p>
        ) : members.length === 0 ? (
          <p className="empty-message">Belum ada member</p>
        ) : (
          <div className="members-list">
            {members.map((member, idx) => (
              <div key={idx} className="member-item">
                <div className="member-info">
                  <span className="phone">{member.phone || member.msisdn}</span>
                  {member.role && <span className="role">{member.role}</span>}
                </div>
                {member.role !== 'leader' && (
                  <button className="danger" onClick={() => handleRemove(member.phone || member.msisdn)}>
                    Hapus
                  </button>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}
    </div>
  )
}

export default Circle
