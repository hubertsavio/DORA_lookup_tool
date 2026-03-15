import { useState } from 'react'
import { Link } from 'react-router-dom'
import { ExternalLink, ChevronDown, ChevronUp, AlertCircle, Info } from 'lucide-react'

function DocumentCard({ document }) {
  const [expanded, setExpanded] = useState(false)

  const getBadgeClass = (bindingStatus) => {
    switch (bindingStatus) {
      case 'Binding Law':
        return 'badge-danger'
      case 'Technical Standard (Binding)':
        return 'badge-warning'
      case 'Guidance (Non-binding)':
        return 'badge-info'
      case 'Interpretive Material':
        return 'badge-info'
      default:
        return 'badge-primary'
    }
  }

  const getLevelBadgeClass = (level) => {
    if (level.includes('Level 1')) return 'badge-danger'
    if (level.includes('Level 2')) return 'badge-warning'
    if (level.includes('Level 3')) return 'badge-info'
    return 'badge-primary'
  }

  return (
    <div className="card" style={styles.card}>
      <div style={styles.header}>
        <div style={styles.titleSection}>
          <h3 style={styles.title}>
            <Link to={`/document/${document.id}`} style={styles.titleLink}>
              {document.title}
            </Link>
          </h3>
          <div style={styles.badges}>
            <span className={`badge ${getLevelBadgeClass(document.legal_level)}`}>
              {document.legal_level}
            </span>
            <span className={`badge ${getBadgeClass(document.binding_status)}`}>
              {document.binding_status}
            </span>
            <span className="badge badge-primary">
              {document.document_type}
            </span>
            {document.is_qa && (
              <span className="badge badge-info">Q&A</span>
            )}
            {document.is_oversight_only && (
              <span className="badge badge-warning">Oversight Only</span>
            )}
          </div>
        </div>
      </div>

      <p style={styles.summary}>{document.summary}</p>

      {/* Metadata */}
      <div style={styles.metadata}>
        <div style={styles.metadataItem}>
          <strong>Source:</strong> {document.source_body}
        </div>
        {document.publication_date && (
          <div style={styles.metadataItem}>
            <strong>Published:</strong> {new Date(document.publication_date).toLocaleDateString()}
          </div>
        )}
        {document.topics && document.topics.length > 0 && (
          <div style={styles.metadataItem}>
            <strong>Topics:</strong>
            <div style={styles.topicTags}>
              {document.topics.map((topic, idx) => (
                <span key={idx} className="badge badge-primary">
                  {topic.name}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Warning for non-binding documents */}
      {document.binding_status !== 'Binding Law' && document.binding_status !== 'Technical Standard (Binding)' && (
        <div className="alert alert-info" style={styles.alert}>
          <Info size={16} />
          <span>
            This is {document.binding_status.toLowerCase()} and should not be treated as legally binding.
          </span>
        </div>
      )}

      {/* Expandable section */}
      {document.related_documents && document.related_documents.length > 0 && (
        <div style={styles.expandable}>
          <button
            onClick={() => setExpanded(!expanded)}
            style={styles.expandButton}
            className="btn btn-secondary"
          >
            {expanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
            {expanded ? 'Hide' : 'Show'} Related Documents ({document.related_documents.length})
          </button>
          
          {expanded && (
            <div style={styles.relatedDocs}>
              {document.related_documents.map((related) => (
                <div key={related.id} style={styles.relatedDoc}>
                  <Link to={`/document/${related.id}`} style={styles.relatedLink}>
                    {related.title}
                  </Link>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Actions */}
      <div style={styles.actions}>
        <Link to={`/document/${document.id}`} className="btn btn-primary">
          View Details
        </Link>
        <a
          href={document.url}
          target="_blank"
          rel="noopener noreferrer"
          className="btn btn-secondary"
        >
          <ExternalLink size={16} />
          Official Source
        </a>
      </div>
    </div>
  )
}

const styles = {
  card: {
    transition: 'box-shadow 0.2s',
  },
  header: {
    marginBottom: '1rem',
  },
  titleSection: {
    marginBottom: '0.75rem',
  },
  title: {
    fontSize: '1.25rem',
    fontWeight: '600',
    marginBottom: '0.5rem',
  },
  titleLink: {
    color: 'var(--primary-color)',
    textDecoration: 'none',
  },
  badges: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '0.5rem',
  },
  summary: {
    color: 'var(--text-secondary)',
    lineHeight: '1.6',
    marginBottom: '1rem',
  },
  metadata: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.5rem',
    marginBottom: '1rem',
    padding: '1rem',
    backgroundColor: 'var(--bg-secondary)',
    borderRadius: '0.375rem',
  },
  metadataItem: {
    fontSize: '0.875rem',
  },
  topicTags: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '0.25rem',
    marginTop: '0.25rem',
  },
  alert: {
    marginBottom: '1rem',
  },
  expandable: {
    marginBottom: '1rem',
  },
  expandButton: {
    width: '100%',
    justifyContent: 'center',
  },
  relatedDocs: {
    marginTop: '1rem',
    padding: '1rem',
    backgroundColor: 'var(--bg-secondary)',
    borderRadius: '0.375rem',
  },
  relatedDoc: {
    padding: '0.5rem 0',
    borderBottom: '1px solid var(--border-color)',
  },
  relatedLink: {
    color: 'var(--primary-color)',
    textDecoration: 'none',
    fontSize: '0.875rem',
  },
  actions: {
    display: 'flex',
    gap: '1rem',
    paddingTop: '1rem',
    borderTop: '1px solid var(--border-color)',
  },
}

export default DocumentCard

// Made with Bob
