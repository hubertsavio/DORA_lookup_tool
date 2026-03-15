import { Link } from 'react-router-dom'
import { AlertTriangle } from 'lucide-react'

function Header() {
  return (
    <header style={styles.header}>
      <div className="container">
        <div style={styles.headerContent}>
          <Link to="/" style={styles.logo}>
            <h1 style={styles.title}>DORA Compliance Lookup Tool</h1>
          </Link>
          <nav style={styles.nav}>
            <Link to="/" style={styles.navLink}>Search</Link>
            <Link to="/about" style={styles.navLink}>About</Link>
          </nav>
        </div>
        
        {/* Disclaimer Banner */}
        <div className="alert alert-warning" style={styles.disclaimer}>
          <AlertTriangle size={20} />
          <div>
            <strong>DISCLAIMER:</strong> This tool is for regulatory research purposes only. 
            It does NOT provide legal advice or certify compliance. 
            Always consult qualified legal counsel for compliance decisions.
          </div>
        </div>
      </div>
    </header>
  )
}

const styles = {
  header: {
    backgroundColor: 'var(--bg-primary)',
    borderBottom: '1px solid var(--border-color)',
    padding: '1rem 0',
    marginBottom: '2rem',
    boxShadow: 'var(--shadow)',
  },
  headerContent: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '1rem',
  },
  logo: {
    textDecoration: 'none',
    color: 'var(--text-primary)',
  },
  title: {
    fontSize: '1.5rem',
    fontWeight: '700',
    color: 'var(--primary-color)',
  },
  nav: {
    display: 'flex',
    gap: '1.5rem',
  },
  navLink: {
    textDecoration: 'none',
    color: 'var(--text-secondary)',
    fontWeight: '500',
    transition: 'color 0.2s',
  },
  disclaimer: {
    marginBottom: 0,
  },
}

export default Header

// Made with Bob
