import { Search } from 'lucide-react'

function SearchBar({ query, setQuery, onSearch, loading }) {
  return (
    <form onSubmit={onSearch} style={styles.form}>
      <div style={styles.inputWrapper}>
        <Search size={20} style={styles.icon} />
        <input
          type="text"
          className="input"
          placeholder="Search DORA documents..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={styles.input}
        />
      </div>
      <button type="submit" className="btn btn-primary" disabled={loading}>
        {loading ? 'Searching...' : 'Search'}
      </button>
    </form>
  )
}

const styles = {
  form: {
    display: 'flex',
    gap: '1rem',
    marginBottom: '1.5rem',
  },
  inputWrapper: {
    position: 'relative',
    flex: 1,
  },
  icon: {
    position: 'absolute',
    left: '1rem',
    top: '50%',
    transform: 'translateY(-50%)',
    color: 'var(--text-secondary)',
  },
  input: {
    paddingLeft: '3rem',
  },
}

export default SearchBar

// Made with Bob
