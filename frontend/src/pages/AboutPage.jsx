import { AlertTriangle, BookOpen, Scale, Shield, Search } from 'lucide-react'

function AboutPage() {
  return (
    <div className="container">
      <div style={styles.content}>
        <h1 style={styles.title}>About DORA Compliance Lookup Tool</h1>

        {/* Main Disclaimer */}
        <div className="alert alert-warning">
          <AlertTriangle size={24} />
          <div>
            <strong>IMPORTANT LEGAL DISCLAIMER</strong>
            <p style={styles.disclaimerText}>
              This tool is for regulatory research and navigation purposes ONLY. 
              It does NOT provide legal advice, does NOT certify compliance, and 
              does NOT create any attorney-client relationship. Always consult 
              qualified legal counsel for compliance decisions and legal interpretations.
            </p>
          </div>
        </div>

        {/* Purpose Section */}
        <div className="card">
          <h2 style={styles.sectionTitle}>
            <BookOpen size={24} style={styles.icon} />
            Purpose
          </h2>
          <p style={styles.text}>
            The DORA Compliance Lookup Tool is a structured regulatory research interface 
            designed to help users search, navigate, summarize, and cross-reference 
            requirements and supporting materials related to the EU Digital Operational 
            Resilience Act (DORA).
          </p>
          <p style={styles.text}>
            This tool aggregates content from the EIOPA DORA hub and related EU regulatory 
            sources to provide a centralized search and reference system for financial 
            sector entities researching DORA requirements.
          </p>
        </div>

        {/* What This Tool Does */}
        <div className="card">
          <h2 style={styles.sectionTitle}>
            <Search size={24} style={styles.icon} />
            What This Tool Does
          </h2>
          <ul style={styles.list}>
            <li>Provides full-text search across DORA regulations, technical standards, and guidance</li>
            <li>Filters documents by legal level, document type, binding status, and topic</li>
            <li>Displays plain-language summaries of complex regulatory text</li>
            <li>Shows cross-references between related documents</li>
            <li>Clearly labels whether content is binding law, technical standard, guidance, or interpretive material</li>
            <li>Links to official source documents</li>
            <li>Distinguishes between hard requirements and supervisory guidance</li>
          </ul>
        </div>

        {/* Legal Hierarchy */}
        <div className="card">
          <h2 style={styles.sectionTitle}>
            <Scale size={24} style={styles.icon} />
            DORA Legal Hierarchy
          </h2>
          
          <div style={styles.hierarchySection}>
            <h3 style={styles.hierarchyTitle}>
              <span className="badge badge-danger">Level 1</span> Primary Legislation
            </h3>
            <ul style={styles.list}>
              <li>Regulation (EU) 2022/2554 - Main DORA Regulation</li>
              <li>Directive (EU) 2022/2556 - DORA Directive</li>
            </ul>
            <p style={styles.hierarchyNote}>
              <strong>Binding:</strong> Directly applicable law across all EU member states
            </p>
          </div>

          <div style={styles.hierarchySection}>
            <h3 style={styles.hierarchyTitle}>
              <span className="badge badge-warning">Level 2</span> Technical Standards
            </h3>
            <ul style={styles.list}>
              <li>Regulatory Technical Standards (RTS)</li>
              <li>Implementing Technical Standards (ITS)</li>
              <li>Delegated Regulations</li>
            </ul>
            <p style={styles.hierarchyNote}>
              <strong>Binding:</strong> Detailed technical requirements with legal force
            </p>
          </div>

          <div style={styles.hierarchySection}>
            <h3 style={styles.hierarchyTitle}>
              <span className="badge badge-info">Level 3</span> Guidelines & Guidance
            </h3>
            <ul style={styles.list}>
              <li>ESA Guidelines</li>
              <li>Supervisory guidance</li>
              <li>Best practice recommendations</li>
            </ul>
            <p style={styles.hierarchyNote}>
              <strong>Non-binding:</strong> Interpretive guidance and recommendations
            </p>
          </div>

          <div style={styles.hierarchySection}>
            <h3 style={styles.hierarchyTitle}>
              <span className="badge badge-primary">Supporting</span> Additional Materials
            </h3>
            <ul style={styles.list}>
              <li>Q&As and interpretive materials</li>
              <li>Reports and opinions</li>
              <li>Oversight materials</li>
              <li>Public statements</li>
            </ul>
            <p style={styles.hierarchyNote}>
              <strong>Informational:</strong> Context and clarification, not legally binding
            </p>
          </div>
        </div>

        {/* Main Topic Areas */}
        <div className="card">
          <h2 style={styles.sectionTitle}>
            <Shield size={24} style={styles.icon} />
            Main DORA Topic Areas
          </h2>
          <div style={styles.topicsGrid}>
            <div style={styles.topicCard}>
              <h3 style={styles.topicTitle}>ICT Risk Management</h3>
              <p style={styles.topicText}>
                Requirements for managing ICT risks in financial entities
              </p>
            </div>
            <div style={styles.topicCard}>
              <h3 style={styles.topicTitle}>ICT Third-Party Risk Management</h3>
              <p style={styles.topicText}>
                Managing risks from ICT third-party service providers
              </p>
            </div>
            <div style={styles.topicCard}>
              <h3 style={styles.topicTitle}>Digital Operational Resilience Testing</h3>
              <p style={styles.topicText}>
                Testing requirements including TLPT (Threat-Led Penetration Testing)
              </p>
            </div>
            <div style={styles.topicCard}>
              <h3 style={styles.topicTitle}>ICT-Related Incidents</h3>
              <p style={styles.topicText}>
                Incident classification, reporting, and management
              </p>
            </div>
            <div style={styles.topicCard}>
              <h3 style={styles.topicTitle}>Information Sharing</h3>
              <p style={styles.topicText}>
                Sharing of cyber threat information and intelligence
              </p>
            </div>
            <div style={styles.topicCard}>
              <h3 style={styles.topicTitle}>Oversight of Critical Third-Party Providers</h3>
              <p style={styles.topicText}>
                CTPP designation and oversight framework
              </p>
            </div>
          </div>
        </div>

        {/* Guardrails */}
        <div className="card">
          <h2 style={styles.sectionTitle}>Tool Guardrails</h2>
          <ul style={styles.list}>
            <li><strong>No compliance certification:</strong> This tool does not claim any organization is compliant or non-compliant</li>
            <li><strong>Source accuracy:</strong> Content is derived from official sources but may not reflect the most recent updates</li>
            <li><strong>Explicit ambiguity:</strong> When regulatory text is ambiguous, this is clearly stated</li>
            <li><strong>Authority hierarchy:</strong> Legal text is prioritized over technical standards, then guidelines, then Q&As</li>
            <li><strong>No legal advice:</strong> Outputs are for research support only, not legal counsel</li>
          </ul>
        </div>

        {/* Data Sources */}
        <div className="card">
          <h2 style={styles.sectionTitle}>Data Sources</h2>
          <p style={styles.text}>
            This tool aggregates content from:
          </p>
          <ul style={styles.list}>
            <li>EIOPA (European Insurance and Occupational Pensions Authority) DORA hub</li>
            <li>EBA (European Banking Authority) DORA materials</li>
            <li>ESMA (European Securities and Markets Authority) DORA materials</li>
            <li>European Commission official publications</li>
            <li>Joint ESA Q&A registers</li>
          </ul>
          <p style={styles.text}>
            All content links back to official source documents for verification.
          </p>
        </div>

        {/* Contact */}
        <div className="card">
          <h2 style={styles.sectionTitle}>Version & Updates</h2>
          <p style={styles.text}>
            <strong>Version:</strong> 1.0.0<br />
            <strong>Last Updated:</strong> {new Date().toLocaleDateString()}<br />
            <strong>Status:</strong> Active Development
          </p>
          <p style={styles.text}>
            This tool is continuously updated as new DORA materials are published by EU authorities.
          </p>
        </div>
      </div>
    </div>
  )
}

const styles = {
  content: {
    maxWidth: '900px',
    margin: '0 auto',
  },
  title: {
    fontSize: '2.5rem',
    fontWeight: '700',
    marginBottom: '2rem',
    color: 'var(--text-primary)',
  },
  disclaimerText: {
    marginTop: '0.5rem',
    marginBottom: 0,
  },
  sectionTitle: {
    fontSize: '1.5rem',
    fontWeight: '600',
    marginBottom: '1rem',
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
  },
  icon: {
    color: 'var(--primary-color)',
  },
  text: {
    lineHeight: '1.8',
    marginBottom: '1rem',
    color: 'var(--text-secondary)',
  },
  list: {
    lineHeight: '1.8',
    paddingLeft: '1.5rem',
    color: 'var(--text-secondary)',
  },
  hierarchySection: {
    marginBottom: '1.5rem',
    paddingBottom: '1.5rem',
    borderBottom: '1px solid var(--border-color)',
  },
  hierarchyTitle: {
    fontSize: '1.125rem',
    fontWeight: '600',
    marginBottom: '0.75rem',
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
  },
  hierarchyNote: {
    marginTop: '0.5rem',
    fontSize: '0.875rem',
    color: 'var(--text-secondary)',
  },
  topicsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '1rem',
  },
  topicCard: {
    padding: '1rem',
    backgroundColor: 'var(--bg-secondary)',
    borderRadius: '0.375rem',
  },
  topicTitle: {
    fontSize: '1rem',
    fontWeight: '600',
    marginBottom: '0.5rem',
    color: 'var(--primary-color)',
  },
  topicText: {
    fontSize: '0.875rem',
    color: 'var(--text-secondary)',
    marginBottom: 0,
  },
}

export default AboutPage

// Made with Bob
