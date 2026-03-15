import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, ExternalLink, AlertCircle } from 'lucide-react'
import axios from 'axios'

function DocumentDetailPage() {
  const { id } = useParams()
  const [document, setDocument] = useState(null)
  const [relatedDocs, setRelatedDocs] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchDocument()
    fetchRelatedDocuments()
  }, [id])

  const fetchDocument = async () => {
    try {
      const response = await axios.get(`/api/documents/${id}`)
      setDocument(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load document')
    } finally {
      setLoading(false)
    }
  }

  const fetchRelatedDocuments = async () => {
    try {
      const response = await axios.get(`/api/documents/${id}/related`)
      setRelatedDocs(response.data.related_documents)
    } catch (err) {
      console.error('Error fetching related documents:', err)
    }
  }

  if (loading) {
    return (
      <div className="container">
        <div className="spinner"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="container">
        <div className="alert alert-danger">
          <AlertCircle size={20} />
          {error}
        </div>
        <Link to="/" className="btn btn-primary">
          <ArrowLeft size={16} />
          Back to Search
        </Link>
      </div>
    )
  }

  if (!document) return null

  return (
    <div className="container">
      <Link to="/" className="btn btn-secondary mb-3">
        <ArrowLeft size={16} />
        Back to Search
      </Link>

      <div className="card">
        <h1 style={styles.title}>{document.title}</h1>

        {/* Badges */}
        <div style={styles.badges}>
          <span className={`badge ${getLevelBadgeClass(document.legal_level)}`}>
            {document.legal_level}
          </span>
          <span className={`badge ${getBindingBadgeClass(document.binding_status)}`}>
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

        {/* Warning for non-binding */}
        {document.binding_status !== 'Binding Law' && 
         document.binding_status !== 'Technical Standard (Binding)' && (
          <div className="alert alert-warning">
            <AlertCircle size={20} />
            <div>
              <strong>Note:</strong> This is {document.binding_status.toLowerCase()} 
              and should not be treated as legally binding law. 
              It provides guidance or interpretation but does not create legal obligations.
            </div>
          </div>
        )}

        {/* Summary */}
        <div style={styles.section}>
          <h2 style={styles.sectionTitle}>Summary</h2>
          <p style={styles.text}>{document.summary}</p>
        </div>

        {/* Metadata Grid */}
        <div style={styles.metadataGrid}>
          <div style={styles.metadataItem}>
            <strong>Source Body:</strong>
            <span>{document.source_body}</span>
          </div>
          <div style={styles.metadataItem}>
            <strong>Legal Level:</strong>
            <span>{document.legal_level}</span>
          </div>
          <div style={styles.metadataItem}>
            <strong>Document Type:</strong>
            <span>{document.document_type}</span>
          </div>
          <div style={styles.metadataItem}>
            <strong>Binding Status:</strong>
            <span>{document.binding_status}</span>
          </div>
          {document.publication_date && (
            <div style={styles.metadataItem}>
              <strong>Publication Date:</strong>
              <span>{new Date(document.publication_date).toLocaleDateString()}</span>
            </div>
          )}
          {document.last_updated && (
            <div style={styles.metadataItem}>
              <strong>Last Updated:</strong>
              <span>{new Date(document.last_updated).toLocaleDateString()}</span>
            </div>
          )}
          {document.qa_status && (
            <div style={styles.metadataItem}>
              <strong>Q&A Status:</strong>
              <span>{document.qa_status}</span>
            </div>
          )}
        </div>

        {/* Topics */}
        {document.topics && document.topics.length > 0 && (
          <div style={styles.section}>
            <h2 style={styles.sectionTitle}>Topics</h2>
            <div style={styles.topicTags}>
              {document.topics.map((topic, idx) => (
                <span key={idx} className="badge badge-primary">
                  {topic.name}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Applicability */}
        {document.applicability && (
          <div style={styles.section}>
            <h2 style={styles.sectionTitle}>Applicability</h2>
            <p style={styles.text}>{document.applicability}</p>
          </div>
        )}

        {/* Related Documents */}
        {relatedDocs.length > 0 && (
          <div style={styles.section}>
            <h2 style={styles.sectionTitle}>Related Documents ({relatedDocs.length})</h2>
            <div style={styles.relatedList}>
              {relatedDocs.map((related) => (
                <div key={related.id} style={styles.relatedItem}>
                  <Link to={`/document/${related.id}`} style={styles.relatedLink}>
                    {related.title}
                  </Link>
                  <div style={styles.relatedMeta}>
                    <span className="badge badge-primary">{related.document_type}</span>
                    <span className="badge badge-info">{related.legal_level}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Actions */}
        <div style={styles.actions}>
          <a
            href={document.url}
            target="_blank"
            rel="noopener noreferrer"
            className="btn btn-primary"
          >
            <ExternalLink size={16} />
            View Official Source
          </a>
        </div>
      </div>

      {/* Disclaimer */}
      <div className="alert alert-info">
        <AlertCircle size={20} />
        <div>
          <strong>Research Tool Disclaimer:</strong> This information is provided for 
          regulatory research purposes only. It does not constitute legal advice or 
          certification of compliance. Always consult qualified legal counsel for 
          compliance decisions.
        </div>
      </div>
    </div>
  )
}

const getLevelBadgeClass = (level) => {
  if (level.includes('Level 1')) return 'badge-danger'
  if (level.includes('Level 2')) return 'badge-warning'
  if (level.includes('Level 3')) return 'badge-info'
  return 'badge-primary'
}

const getBindingBadgeClass = (status) => {
  if (status === 'Binding Law') return 'badge-danger'
  if (status === 'Technical Standard (Binding)') return 'badge-warning'
  return 'badge-info'
}

const styles = {
  title: {
    fontSize: '2rem',
    fontWeight: '700',
    marginBottom: '1rem',
    color: 'var(--text-primary)',
  },
  badges: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '0.5rem',
    marginBottom: '1.5rem',
  },
  section: {
    marginTop: '2rem',
    paddingTop: '1.5rem',
    borderTop: '1px solid var(--border-color)',
  },
  sectionTitle: {
    fontSize: '1.5rem',
    fontWeight: '600',
    marginBottom: '1rem',
  },
  text: {
    lineHeight: '1.8',
    color: 'var(--text-secondary)',
  },
  metadataGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '1rem',
    padding: '1.5rem',
    backgroundColor: 'var(--bg-secondary)',
    borderRadius: '0.375rem',
    marginTop: '1.5rem',
  },
  metadataItem: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.25rem',
  },
  topicTags: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '0.5rem',
  },
  relatedList: {
    display: 'flex',
    flexDirection: 'column',
    gap: '1rem',
  },
  relatedItem: {
    padding: '1rem',
    backgroundColor: 'var(--bg-secondary)',
    borderRadius: '0.375rem',
  },
  relatedLink: {
    color: 'var(--primary-color)',
    textDecoration: 'none',
    fontWeight: '500',
    display: 'block',
    marginBottom: '0.5rem',
  },
  relatedMeta: {
    display: 'flex',
    gap: '0.5rem',
  },
  actions: {
    marginTop: '2rem',
    paddingTop: '1.5rem',
    borderTop: '1px solid var(--border-color)',
  },
}

export default DocumentDetailPage

// Made with Bob
