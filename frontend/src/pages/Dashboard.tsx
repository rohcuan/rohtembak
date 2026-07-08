import { useState, useEffect } from 'react'
import { profileApi, xlAuthApi } from '../api/client'
import './Dashboard.css'

function Dashboard() {
  const [profile, setProfile] = useState<any>(null)
  const [balance, setBalance] = useState<any>(null)
  const [xlAccounts, setXlAccounts] = useState<any[]>([])
  const [activeMsisdn, setActiveMsisdn] = useState<string>('')
  const [xlLoggedIn, setXlLoggedIn] = useState(false)
  const [otpMsisdn, setOtpMsisdn] = useState('')
  const [otpCode, setOtpCode] = useState('')
  const [otpSent, setOtpSent] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    checkXLStatus()
  }, [])

  const checkXLStatus = async () => {
    try {
      const statusRes = await xlAuthApi.getStatus()
      const { logged_in, active_msisdn } = statusRes.data
      setXlLoggedIn(logged_in)
      setActiveMsisdn(active_msisdn || '')

      const accountsRes = await xlAuthApi.getAccounts()
      setXlAccounts(accountsRes.data.accounts || [])

      if (logged_in && active_msisdn) {
        loadProfile(active_msisdn)
      }
    } catch (err) {
      console.error('Error checking XL status:', err)
    }
  }

  const loadProfile = async (msisdn: string) => {
    try {
      const [profileRes, balanceRes] = await Promise.all([
        profileApi.getProfile(),
        profileApi.getBalance()
      ])
      setProfile(profileRes.data.data)
      setBalance(balanceRes.data.data)
    } catch (err) {
      console.error('Error loading profile:', err)
    }
  }

  const handleRequestOTP = async () => {
    if (!otpMsisdn) return
    setLoading(true)
    setError('')
    try {
      await xlAuthApi.requestOTP(otpMsisdn)
      setOtpSent(true)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Gagal mengirim OTP')
    } finally {
      setLoading(false)
    }
  }

  const handleVerifyOTP = async () => {
    if (!otpMsisdn || !otpCode) return
    setLoading(true)
    setError('')
    try {
      await xlAuthApi.verifyOTP(otpMsisdn, otpCode)
      setOtpSent(false)
      setOtpCode('')
      checkXLStatus()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'OTP tidak valid')
    } finally {
      setLoading(false)
    }
  }

  const handleSwitchAccount = async (msisdn: string) => {
    try {
      await xlAuthApi.switchAccount(msisdn)
      checkXLStatus()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Gagal switch account')
    }
  }

  const handleRemoveAccount = async (msisdn: string) => {
    if (!confirm(`Hapus akun ${msisdn}?`)) return
    try {
      await xlAuthApi.removeAccount(msisdn)
      checkXLStatus()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Gagal menghapus akun')
    }
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h2>Dashboard</h2>
        {activeMsisdn && <span className="active-number">{activeMsisdn}</span>}
      </div>

      {!xlLoggedIn ? (
        <div className="xl-login-section">
          <h3>Login XL Axiata</h3>
          <div className="xl-login-form">
            <input
              type="text"
              placeholder="Nomor HP (628xxx)"
              value={otpMsisdn}
              onChange={(e) => setOtpMsisdn(e.target.value)}
              disabled={loading}
            />
            {!otpSent ? (
              <button onClick={handleRequestOTP} disabled={loading}>
                {loading ? 'Mengirim...' : 'Kirim OTP'}
              </button>
            ) : (
              <div className="otp-verify">
                <input
                  type="text"
                  placeholder="Kode OTP"
                  value={otpCode}
                  onChange={(e) => setOtpCode(e.target.value)}
                  disabled={loading}
                />
                <button onClick={handleVerifyOTP} disabled={loading}>
                  {loading ? 'Memverifikasi...' : 'Verifikasi'}
                </button>
              </div>
            )}
            {error && <div className="error-message">{error}</div>}
          </div>
        </div>
      ) : (
        <>
          <div className="profile-section">
            <div className="profile-card">
              <h3>Profil</h3>
              {profile ? (
                <div className="profile-info">
                  <p><strong>Nama:</strong> {profile.name || '-'}</p>
                  <p><strong>Nomor:</strong> {profile.msisdn || activeMsisdn}</p>
                </div>
              ) : (
                <p>Memuat profil...</p>
              )}
            </div>

            <div className="balance-card">
              <h3>Saldo & Kuota</h3>
              {balance ? (
                <div className="balance-info">
                  <div className="balance-item">
                    <span className="label">Pulsa</span>
                    <span className="value">{balance.pulsa || '-'}</span>
                  </div>
                  <div className="balance-item">
                    <span className="label">Kuota Utama</span>
                    <span className="value">{balance.kuota || '-'}</span>
                  </div>
                </div>
              ) : (
                <p>Memuat saldo...</p>
              )}
            </div>
          </div>

          <div className="accounts-section">
            <h3>Akun Tersimpan</h3>
            <div className="accounts-list">
              {xlAccounts.map((acc) => (
                <div key={acc.msisdn} className={`account-item ${acc.is_active ? 'active' : ''}`}>
                  <span>{acc.msisdn}</span>
                  <div className="account-actions">
                    {!acc.is_active && (
                      <button onClick={() => handleSwitchAccount(acc.msisdn)}>Switch</button>
                    )}
                    <button className="danger" onClick={() => handleRemoveAccount(acc.msisdn)}>Hapus</button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  )
}

export default Dashboard
