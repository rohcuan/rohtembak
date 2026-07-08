import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Packages from './pages/Packages'
import Circle from './pages/Circle'
import Family from './pages/Family'
import Notifications from './pages/Notifications'
import Layout from './components/Layout'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [subscriptionData, setSubscriptionData] = useState<any>(null)

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('subscription_token')
    const data = localStorage.getItem('subscription_data')
    if (token && data) {
      setIsAuthenticated(true)
      setSubscriptionData(JSON.parse(data))
    }
  }, [])

  const handleLogin = (data: any) => {
    setIsAuthenticated(true)
    setSubscriptionData(data)
  }

  const handleLogout = () => {
    localStorage.removeItem('subscription_token')
    localStorage.removeItem('subscription_data')
    setIsAuthenticated(false)
    setSubscriptionData(null)
  }

  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} />
  }

  return (
    <BrowserRouter>
      <Layout onLogout={handleLogout} subscriptionData={subscriptionData}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/packages" element={<Packages />} />
          <Route path="/circle" element={<Circle />} />
          <Route path="/family" element={<Family />} />
          <Route path="/notifications" element={<Notifications />} />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}

export default App
