import { X } from 'lucide-react'

function FilterPanel({ 
  filters, 
  setFilters, 
  includeQA, 
  setIncludeQA, 
  includeOversight, 
  setIncludeOversight,
  filterOptions,
  onClear 
}) {
  return (
    <div className="card" style={styles.panel}>
      <div style={styles.header}>
        <h3 style={styles.title}>Filter Options</h3>
        <button className="btn btn-secondary" onClick={onClear}>
          Clear All
        </button>
      </div>

      <div style={styles.grid}>
        {/* Legal Level */}
        <div style={styles.filterGroup}>
          <label style={styles.label}>Legal Level</label>
          <select
            className="input"
            value={filters.legal_level}
            onChange={(e) => setFilters({...filters, legal_level: e.target.value})}
          >
            <option value="">All Levels</option>
            {filterOptions.legal_levels.map(level => (
              <option key={level} value={level}>{level}</option>
            ))}
          </select>
        </div>

        {/* Document Type */}
        <div style={styles.filterGroup}>
          <label style={styles.label}>Document Type</label>
          <select
            className="input"
            value={filters.document_type}
            onChange={(e) => setFilters({...filters, document_type: e.target.value})}
          >
            <option value="">All Types</option>
            {filterOptions.document_types.map(type => (
              <option key={type} value={type}>{type}</option>
            ))}
          </select>
        </div>

        {/* Binding Status */}
        <div style={styles.filterGroup}>
          <label style={styles.label}>Binding Status</label>
          <select
            className="input"
            value={filters.binding_status}
            onChange={(e) => setFilters({...filters, binding_status: e.target.value})}
          >
            <option value="">All Statuses</option>
            {filterOptions.binding_statuses.map(status => (
              <option key={status} value={status}>{status}</option>
            ))}
          </select>
        </div>

        {/* Source Body */}
        <div style={styles.filterGroup}>
          <label style={styles.label}>Source Body</label>
          <select
            className="input"
            value={filters.source_body}
            onChange={(e) => setFilters({...filters, source_body: e.target.value})}
          >
            <option value="">All Sources</option>
            {filterOptions.source_bodies.map(body => (
              <option key={body} value={body}>{body}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Topics */}
      <div style={styles.filterGroup}>
        <label style={styles.label}>Topics</label>
        <div style={styles.topicsGrid}>
          {filterOptions.topics.map(topic => (
            <label key={topic} style={styles.checkboxLabel}>
              <input
                type="checkbox"
                checked={filters.topics.includes(topic)}
                onChange={(e) => {
                  if (e.target.checked) {
                    setFilters({...filters, topics: [...filters.topics, topic]})
                  } else {
                    setFilters({...filters, topics: filters.topics.filter(t => t !== topic)})
                  }
                }}
                style={styles.checkbox}
              />
              {topic}
            </label>
          ))}
        </div>
      </div>

      {/* Toggle Options */}
      <div style={styles.toggles}>
        <label style={styles.checkboxLabel}>
          <input
            type="checkbox"
            checked={includeQA}
            onChange={(e) => setIncludeQA(e.target.checked)}
            style={styles.checkbox}
          />
          Include Q&A Documents
        </label>
        <label style={styles.checkboxLabel}>
          <input
            type="checkbox"
            checked={includeOversight}
            onChange={(e) => setIncludeOversight(e.target.checked)}
            style={styles.checkbox}
          />
          Include Oversight-Only Materials
        </label>
      </div>
    </div>
  )
}

const styles = {
  panel: {
    marginBottom: '1.5rem',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '1.5rem',
  },
  title: {
    fontSize: '1.125rem',
    fontWeight: '600',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '1rem',
    marginBottom: '1.5rem',
  },
  filterGroup: {
    marginBottom: '1rem',
  },
  label: {
    display: 'block',
    fontWeight: '500',
    marginBottom: '0.5rem',
    color: 'var(--text-primary)',
  },
  topicsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '0.5rem',
  },
  checkboxLabel: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
    cursor: 'pointer',
  },
  checkbox: {
    width: '1rem',
    height: '1rem',
    cursor: 'pointer',
  },
  toggles: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.75rem',
    paddingTop: '1rem',
    borderTop: '1px solid var(--border-color)',
  },
}

export default FilterPanel

// Made with Bob
