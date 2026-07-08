import { Link, useLocation } from 'react-router-dom'
import './Layout.css'

interface LayoutProps {
  children: React.ReactNode
  onLogout: () => void
  subscriptionData: any
}

function Layout({ children, onLogout, subscriptionData }: LayoutProps) {
  const location = useLocation()

  const navItems = [
    { path: '/', label: 'Dashboard', icon: '📊' },
    { path: '/packages', label: 'Paket', icon: '📦' },
    { path: '/circle', label: 'Circle', icon: '👥' },
    { path: '/family', label: 'Family', icon: '👨‍👩‍👧‍👦' },
    { path: '/notifications', label: 'Notifikasi', icon: '🔔' },
  ]

  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="sidebar-header">
          <h1>RohTembak</h1>
          <p>XL Axiata Client</p>
        </div>

        <nav className="sidebar-nav">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`nav-item ${location.pathname === item.path ? 'active' : ''}`}
            >
              <span className="icon">{item.icon}</span>
              <span className="label">{item.label}</span>
            </Link>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="user-info">
            <div className="user-details">
              <span className="username">{subscriptionData?.username || 'User'}</span>
              <span className="expiry">Exp: {subscriptionData?.expiry || '-'}</span>
            </div>
          </div>
          <button onClick={onLogout} className="logout-button">
            Logout
          </button>
        </div>
      </aside>

      <main className="main-content">
        {children}
      </main>
    </div>
  )
}

export default Layout
