"""
Database models for DORA Compliance Lookup Tool
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Table, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import enum

Base = declarative_base()

# Association table for document relationships (many-to-many)
document_relationships = Table(
    'document_relationships',
    Base.metadata,
    Column('source_id', Integer, ForeignKey('documents.id'), primary_key=True),
    Column('related_id', Integer, ForeignKey('documents.id'), primary_key=True)
)

# Association table for document topics (many-to-many)
document_topics = Table(
    'document_topics',
    Base.metadata,
    Column('document_id', Integer, ForeignKey('documents.id'), primary_key=True),
    Column('topic_id', Integer, ForeignKey('topics.id'), primary_key=True)
)


class LegalLevel(enum.Enum):
    """Legal hierarchy levels"""
    LEVEL_1 = "Level 1 - Primary Legislation"
    LEVEL_2 = "Level 2 - Technical Standards"
    LEVEL_3 = "Level 3 - Guidelines"
    SUPPORTING = "Supporting Material"


class DocumentType(enum.Enum):
    """Types of DORA documents"""
    REGULATION = "Regulation"
    DIRECTIVE = "Directive"
    RTS = "Regulatory Technical Standard"
    ITS = "Implementing Technical Standard"
    DELEGATED_REGULATION = "Delegated Regulation"
    GUIDELINE = "Guideline"
    DECISION = "Decision"
    OPINION = "Opinion"
    STATEMENT = "Public Statement"
    REPORT = "Report"
    QA = "Q&A"
    TOOL = "Reporting Tool"
    ROADMAP = "Roadmap"
    GUIDE = "Guide"
    MOU = "Memorandum of Understanding"
    OTHER = "Other"


class BindingStatus(enum.Enum):
    """Binding status of documents"""
    BINDING = "Binding Law"
    TECHNICAL_STANDARD = "Technical Standard (Binding)"
    GUIDANCE = "Guidance (Non-binding)"
    INTERPRETIVE = "Interpretive Material"
    INFORMATIONAL = "Informational"


class SourceBody(enum.Enum):
    """EU regulatory bodies"""
    EIOPA = "EIOPA"
    EBA = "EBA"
    ESMA = "ESMA"
    ESA_JOINT = "ESAs (Joint)"
    EU_COMMISSION = "European Commission"
    EU_PARLIAMENT = "European Parliament"
    EU_COUNCIL = "Council of the EU"


class QAStatus(enum.Enum):
    """Status of Q&A documents"""
    UNDER_REVIEW = "Under Review"
    FINAL = "Final"
    REVISED = "Revised"
    SUPERSEDED = "Superseded"


class Topic(Base):
    """Main topic categories for DORA"""
    __tablename__ = 'topics'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, unique=True)
    description = Column(Text)
    parent_id = Column(Integer, ForeignKey('topics.id'), nullable=True)
    
    # Relationships
    parent = relationship('Topic', remote_side=[id], backref='subcategories')
    documents = relationship('Document', secondary=document_topics, back_populates='topics')
    
    def __repr__(self):
        return f"<Topic(name='{self.name}')>"


class Document(Base):
    """Core document model for all DORA materials"""
    __tablename__ = 'documents'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    summary = Column(Text, nullable=False)
    full_text = Column(Text)
    
    # Classification
    legal_level = Column(Enum(LegalLevel), nullable=False)
    document_type = Column(Enum(DocumentType), nullable=False)
    binding_status = Column(Enum(BindingStatus), nullable=False)
    source_body = Column(Enum(SourceBody), nullable=False)
    
    # Metadata
    url = Column(String(1000), nullable=False)
    publication_date = Column(DateTime, nullable=True)
    last_updated = Column(DateTime, nullable=True)
    applicability = Column(Text)  # Who/what this applies to
    
    # Q&A specific
    is_qa = Column(Boolean, default=False)
    qa_status = Column(Enum(QAStatus), nullable=True)
    
    # Oversight specific
    is_oversight_only = Column(Boolean, default=False)
    
    # System metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    scraped_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    topics = relationship('Topic', secondary=document_topics, back_populates='documents')
    related_documents = relationship(
        'Document',
        secondary=document_relationships,
        primaryjoin=id == document_relationships.c.source_id,
        secondaryjoin=id == document_relationships.c.related_id,
        backref='referenced_by'
    )
    
    def __repr__(self):
        return f"<Document(title='{self.title[:50]}...', type='{self.document_type.value}')>"
    
    def to_dict(self):
        """Convert document to dictionary for API responses"""
        return {
            'id': self.id,
            'title': self.title,
            'summary': self.summary,
            'legal_level': self.legal_level.value,
            'document_type': self.document_type.value,
            'binding_status': self.binding_status.value,
            'source_body': self.source_body.value,
            'url': self.url,
            'publication_date': self.publication_date.isoformat() if self.publication_date else None,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'applicability': self.applicability,
            'is_qa': self.is_qa,
            'qa_status': self.qa_status.value if self.qa_status else None,
            'is_oversight_only': self.is_oversight_only,
            'topics': [{'id': t.id, 'name': t.name} for t in self.topics],
            'related_documents': [{'id': d.id, 'title': d.title} for d in self.related_documents]
        }


class SearchLog(Base):
    """Log of user searches for analytics"""
    __tablename__ = 'search_logs'
    
    id = Column(Integer, primary_key=True)
    query = Column(String(500), nullable=False)
    filters = Column(Text)  # JSON string of applied filters
    results_count = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<SearchLog(query='{self.query}', results={self.results_count})>"


# Database initialization
def init_db(database_url: str = "sqlite:///dora_compliance.db"):
    """Initialize database and create all tables"""
    engine = create_engine(database_url, echo=True)
    Base.metadata.create_all(engine)
    return engine


def get_session(engine):
    """Get database session"""
    Session = sessionmaker(bind=engine)
    return Session()


def seed_topics(session):
    """Seed initial topic categories"""
    topics_data = [
        {
            'name': 'ICT Risk Management',
            'description': 'Requirements for managing ICT risks in financial entities'
        },
        {
            'name': 'ICT Third-Party Risk Management',
            'description': 'Managing risks from ICT third-party service providers'
        },
        {
            'name': 'Digital Operational Resilience Testing',
            'description': 'Testing requirements including TLPT'
        },
        {
            'name': 'ICT-Related Incidents',
            'description': 'Incident classification, reporting, and management'
        },
        {
            'name': 'Information Sharing',
            'description': 'Sharing of cyber threat information and intelligence'
        },
        {
            'name': 'Oversight of Critical Third-Party Providers',
            'description': 'CTPP designation and oversight framework'
        }
    ]
    
    for topic_data in topics_data:
        topic = Topic(**topic_data)
        session.add(topic)
    
    session.commit()
    print("Topics seeded successfully")


if __name__ == "__main__":
    # Initialize database
    engine = init_db()
    session = get_session(engine)
    
    # Seed topics
    seed_topics(session)
    
    print("Database initialized successfully")

# Made with Bob
