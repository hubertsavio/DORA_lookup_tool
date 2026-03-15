import { useState, useEffect } from 'react'
import { Search, Filter, X } from 'lucide-react'
import axios from 'axios'
import SearchBar from '../components/SearchBar'
import FilterPanel from '../components/FilterPanel'
import DocumentCard from '../components/DocumentCard'

function SearchPage() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [showFilters, setShowFilters] = useState(false)
  const [filters, setFilters] = useState({
    legal_level: '',
    document_type: '',
    binding_status: '',
    source_body: '',
    topics: []
  })
  const [includeQA, setIncludeQA] = useState(true)
  const [includeOversight, setIncludeOversight] = useState(true)
  const [filterOptions, setFilterOptions] = useState(null)

  // Fetch filter options on mount
  useEffect(() => {
    fetchFilterOptions()
  }, [])

  const fetchFilterOptions = async () => {
    try {
      const response = await axios.get('/api/filters')
      setFilterOptions(response.data)
    } catch (err) {
      console.error('Error fetching filter options:', err)
    }
  }

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!query.trim()) return

    setLoading(true)
    setError(null)

    try {
      const response = await axios.post('/api/search', {
        query: query,
        filters: filters,
        limit: 50,
        include_qa: includeQA,
        include_oversight: includeOversight
      })

      setResults(response.data.documents)
    } catch (err) {
      setError(err.response?.data?.detail || 'Search failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const clearFilters = () => {
    setFilters({
      legal_level: '',
      document_type: '',
      binding_status: '',
      source_body: '',
      topics: []
    })
    setIncludeQA(true)
    setIncludeOversight(true)
  }

  const hasActiveFilters = () => {
    return filters.legal_level || filters.document_type || 
           filters.binding_status || filters.source_body || 
           filters.topics.length > 0 || !includeQA || !includeOversight
  }

  return (
    <div className="container">
      <div style={styles.searchContainer}>
        <h2 style={styles.heading}>Search DORA Regulations & Guidance</h2>
        
        <form onSubmit={handleSearch} style={styles.searchForm}>
          <div style={styles.searchInputWrapper}>
            <Search size={20} style={styles.searchIcon} />
            <input
              type="text"
              className="input"
              placeholder="Search DORA documents... (e.g., 'ICT incident reporting', 'CTPP oversight')"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              style={styles.searchInput}
            />
          </div>
          
          <div style={styles.searchActions}>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Searching...' : 'Search'}
            </button>
            <button
              type="button"
              className="btn btn-secondary"
              onClick={() => setShowFilters(!showFilters)}
            >
              <Filter size={16} />
              Filters {hasActiveFilters() && '(Active)'}
            </button>
          </div>
        </form>

        {/* Filter Panel */}
        {showFilters && filterOptions && (
          <FilterPanel
            filters={filters}
            setFilters={setFilters}
            includeQA={includeQA}
            setIncludeQA={setIncludeQA}
            includeOversight={includeOversight}
            setIncludeOversight={setIncludeOversight}
            filterOptions={filterOptions}
            onClear={clearFilters}
          />
        )}

        {/* Active Filters Display */}
        {hasActiveFilters() && (
          <div style={styles.activeFilters}>
            <span style={styles.activeFiltersLabel}>Active filters:</span>
            {filters.legal_level && (
              <span className="badge badge-primary">
                Level: {filters.legal_level}
                <X size={14} style={styles.removeIcon} onClick={() => setFilters({...filters, legal_level: ''})} />
              </span>
            )}
            {filters.document_type && (
              <span className="badge badge-primary">
                Type: {filters.document_type}
                <X size={14} style={styles.removeIcon} onClick={() => setFilters({...filters, document_type: ''})} />
              </span>
            )}
            {filters.binding_status && (
              <span className="badge badge-primary">
                Status: {filters.binding_status}
                <X size={14} style={styles.removeIcon} onClick={() => setFilters({...filters, binding_status: ''})} />
              </span>
            )}
            {!includeQA && <span className="badge badge-warning">Q&As excluded</span>}
            {!includeOversight && <span className="badge badge-warning">Oversight excluded</span>}
            <button className="btn btn-secondary" onClick={clearFilters} style={styles.clearAllBtn}>
              Clear All
            </button>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="alert alert-danger">
            {error}
          </div>
        )}

        {/* Results */}
        {loading && (
          <div className="spinner"></div>
        )}

        {!loading && results.length > 0 && (
          <div style={styles.results}>
            <h3 style={styles.resultsHeading}>
              Found {results.length} document{results.length !== 1 ? 's' : ''}
            </h3>
            {results.map((doc) => (
              <DocumentCard key={doc.id} document={doc} />
            ))}
          </div>
        )}

        {!loading && query && results.length === 0 && !error && (
          <div className="card text-center">
            <p>No documents found matching your search criteria.</p>
            <p style={styles.suggestion}>Try adjusting your search terms or filters.</p>
          </div>
        )}

        {!query && !loading && (
          <div className="card">
            <h3 style={styles.examplesHeading}>Example Searches:</h3>
            <ul style={styles.examplesList}>
              <li onClick={() => setQuery('ICT incident reporting')} style={styles.exampleItem}>
                "ICT incident reporting"
              </li>
              <li onClick={() => setQuery('DORA requirements for subcontracting')} style={styles.exampleItem}>
                "DORA requirements for subcontracting"
              </li>
              <li onClick={() => setQuery('CTPP oversight')} style={styles.exampleItem}>
                "CTPP oversight"
              </li>
              <li onClick={() => setQuery('Level 2 measures for ICT risk management')} style={styles.exampleItem}>
                "Level 2 measures for ICT risk management"
              </li>
              <li onClick={() => setQuery('operational resilience testing')} style={styles.exampleItem}>
                "operational resilience testing"
              </li>
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}

const styles = {
  searchContainer: {
    maxWidth: '1200px',
    margin: '0 auto',
  },
  heading: {
    fontSize: '2rem',
    fontWeight: '700',
    marginBottom: '2rem',
    color: 'var(--text-primary)',
  },
  searchForm: {
    marginBottom: '1.5rem',
  },
  searchInputWrapper: {
    position: 'relative',
    marginBottom: '1rem',
  },
  searchIcon: {
    position: 'absolute',
    left: '1rem',
    top: '50%',
    transform: 'translateY(-50%)',
    color: 'var(--text-secondary)',
  },
  searchInput: {
    paddingLeft: '3rem',
  },
  searchActions: {
    display: 'flex',
    gap: '1rem',
  },
  activeFilters: {
    display: 'flex',
    flexWrap: 'wrap',
    alignItems: 'center',
    gap: '0.5rem',
    padding: '1rem',
    backgroundColor: 'var(--bg-secondary)',
    borderRadius: '0.375rem',
    marginBottom: '1rem',
  },
  activeFiltersLabel: {
    fontWeight: '600',
    marginRight: '0.5rem',
  },
  removeIcon: {
    marginLeft: '0.25rem',
    cursor: 'pointer',
  },
  clearAllBtn: {
    marginLeft: 'auto',
  },
  results: {
    marginTop: '2rem',
  },
  resultsHeading: {
    fontSize: '1.25rem',
    fontWeight: '600',
    marginBottom: '1rem',
  },
  suggestion: {
    color: 'var(--text-secondary)',
    marginTop: '0.5rem',
  },
  examplesHeading: {
    fontSize: '1.125rem',
    fontWeight: '600',
    marginBottom: '1rem',
  },
  examplesList: {
    listStyle: 'none',
    padding: 0,
  },
  exampleItem: {
    padding: '0.75rem',
    marginBottom: '0.5rem',
    backgroundColor: 'var(--bg-secondary)',
    borderRadius: '0.375rem',
    cursor: 'pointer',
    transition: 'background-color 0.2s',
  },
}

export default SearchPage

// Made with Bob
