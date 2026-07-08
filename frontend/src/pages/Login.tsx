import { useState } from 'react'
import { subscriptionApi } from '../api/client'
import './Login.css'

interface LoginProps {
  onLogin: (data: any) => void
}

function Login({ onLogin }: LoginProps) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const response = await subscriptionApi.login(username, password)
      const { access_token, username: user, subscription_expiry, is_expired } = response.data

      if (is_expired) {
        setError('Subscription Anda sudah expired. Silakan hubungi admin.')
        setLoading(false)
        return
      }

      // Store token and data
      localStorage.setItem('subscription_token', access_token)
      localStorage.setItem('subscription_data', JSON.stringify({
        username: user,
        expiry: subscription_expiry
      }))

      onLogin({ username: user, expiry: subscription_expiry })
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login gagal. Periksa username dan password.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-container">
      <div className="login-box">
        <div className="login-header">
          <h1>RohTembak</h1>
          <p>XL Axiata Client</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Masukkan username"
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Masukkan password"
              required
              disabled={loading}
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <button type="submit" className="login-button" disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <div className="login-footer">
          <p>Belum punya akun? Hubungi admin untuk mendapatkan akses.</p>
        </div>
      </div>
    </div>
  )
}

export default Login
