import { useState, useEffect } from 'react'
import { notificationsApi } from '../api/client'
import './Notifications.css'

function Notifications() {
  const [notifications, setNotifications] = useState<any[]>([])
  const [selectedNotification, setSelectedNotification] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    loadNotifications()
  }, [])

  const loadNotifications = async () => {
    setLoading(true)
    try {
      const res = await notificationsApi.getAll()
      setNotifications(res.data.data || [])
    } catch (err) {
      setError('Gagal memuat notifikasi')
    } finally {
      setLoading(false)
    }
  }

  const handleViewDetail = async (id: string) => {
    try {
      const res = await notificationsApi.getDetail(id)
      setSelectedNotification(res.data.data)
    } catch (err) {
      setError('Gagal memuat detail notifikasi')
    }
  }

  return (
    <div className="notifications-page">
      <h2>Notifikasi</h2>

      {loading ? (
        <p>Memuat...</p>
      ) : notifications.length === 0 ? (
        <div className="empty-state">
          <p>Tidak ada notifikasi</p>
        </div>
      ) : (
        <div className="notifications-layout">
          <div className="notifications-list">
            {notifications.map((notif, idx) => (
              <div
                key={idx}
                className={`notification-item ${selectedNotification?.id === notif.id ? 'active' : ''}`}
                onClick={() => handleViewDetail(notif.id)}
              >
                <div className="notification-header">
                  <h4>{notif.title || 'Notifikasi'}</h4>
                  <span className="date">{notif.date || notif.created_at || '-'}</span>
                </div>
                <p className="preview">{notif.preview || notif.message?.substring(0, 100) || '-'}</p>
              </div>
            ))}
          </div>

          {selectedNotification && (
            <div className="notification-detail">
              <h3>{selectedNotification.title}</h3>
              <div className="meta">
                <span>{selectedNotification.date || selectedNotification.created_at}</span>
              </div>
              <div className="content">
                {selectedNotification.message || selectedNotification.content}
              </div>
            </div>
          )}
        </div>
      )}

      {error && <div className="error-message">{error}</div>}
    </div>
  )
}

export default Notifications
