"""
FastAPI routes for DORA Compliance Lookup Tool
"""
from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from datetime import datetime
from sqlalchemy.orm import Session

from models import Document, Topic, SearchLog, get_session, init_db
from utils import DORASearchEngine

# Initialize router
router = APIRouter()

# Initialize search engine
search_engine = DORASearchEngine()


# Pydantic models for request/response
class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    filters: Optional[Dict] = None
    limit: int = Field(50, ge=1, le=100)
    include_qa: bool = True
    include_oversight: bool = True


class DocumentResponse(BaseModel):
    id: int
    title: str
    summary: str
    legal_level: str
    document_type: str
    binding_status: str
    source_body: str
    url: str
    publication_date: Optional[datetime]
    last_updated: Optional[datetime]
    applicability: Optional[str]
    is_qa: bool
    qa_status: Optional[str]
    is_oversight_only: bool
    topics: List[Dict]
    related_documents: List[Dict]


class SearchResponse(BaseModel):
    query: str
    total_results: int
    documents: List[DocumentResponse]
    filters_applied: Optional[Dict]
    disclaimer: str = (
        "⚠️ DISCLAIMER: This tool is for regulatory research purposes only. "
        "It does NOT provide legal advice or certify compliance. "
        "Always consult qualified legal counsel for compliance decisions."
    )


class TopicResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    subcategories: List[Dict]


class FilterOptionsResponse(BaseModel):
    legal_levels: List[str]
    document_types: List[str]
    binding_statuses: List[str]
    source_bodies: List[str]
    topics: List[str]


# Dependency to get database session
def get_db():
    engine = init_db()
    session = get_session(engine)
    try:
        yield session
    finally:
        session.close()


# Routes
@router.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "DORA Compliance Lookup Tool API",
        "version": "1.0.0",
        "description": "Regulatory research assistant for EU DORA compliance",
        "disclaimer": (
            "This tool is for regulatory research purposes only. "
            "It does NOT provide legal advice or certify compliance."
        ),
        "endpoints": {
            "search": "/api/search",
            "documents": "/api/documents",
            "topics": "/api/topics",
            "filters": "/api/filters"
        }
    }


@router.post("/api/search", response_model=SearchResponse)
async def search_documents(
    request: SearchRequest,
    db: Session = Depends(get_db)
):
    """
    Search DORA documents with filters
    
    - **query**: Search query string
    - **filters**: Optional filters (legal_level, document_type, etc.)
    - **limit**: Maximum number of results (1-100)
    - **include_qa**: Include Q&A documents
    - **include_oversight**: Include oversight-only documents
    """
    try:
        # Perform search
        results = search_engine.search(
            query=request.query,
            filters=request.filters,
            limit=request.limit,
            include_qa=request.include_qa,
            include_oversight=request.include_oversight
        )
        
        # Log search
        search_log = SearchLog(
            query=request.query,
            filters=str(request.filters),
            results_count=len(results)
        )
        db.add(search_log)
        db.commit()
        
        # Get full document details from database
        document_ids = [int(r['id']) for r in results]
        documents = db.query(Document).filter(Document.id.in_(document_ids)).all()
        
        # Convert to response format
        doc_responses = [DocumentResponse(**doc.to_dict()) for doc in documents]
        
        return SearchResponse(
            query=request.query,
            total_results=len(doc_responses),
            documents=doc_responses,
            filters_applied=request.filters
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")


@router.get("/api/documents/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific document
    
    - **document_id**: Unique document identifier
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return DocumentResponse(**document.to_dict())


@router.get("/api/documents/{document_id}/related")
async def get_related_documents(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Get documents related to a specific document
    
    - **document_id**: Unique document identifier
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    related = [
        {
            'id': doc.id,
            'title': doc.title,
            'document_type': doc.document_type.value,
            'legal_level': doc.legal_level.value,
            'url': doc.url
        }
        for doc in document.related_documents
    ]
    
    return {
        'document_id': document_id,
        'document_title': document.title,
        'related_documents': related,
        'total_related': len(related)
    }


@router.get("/api/topics", response_model=List[TopicResponse])
async def get_topics(db: Session = Depends(get_db)):
    """
    Get all DORA topic categories
    """
    topics = db.query(Topic).filter(Topic.parent_id == None).all()
    
    topic_responses = []
    for topic in topics:
        subcats = [
            {'id': sub.id, 'name': sub.name}
            for sub in topic.subcategories
        ]
        topic_responses.append(
            TopicResponse(
                id=topic.id,
                name=topic.name,
                description=topic.description,
                subcategories=subcats
            )
        )
    
    return topic_responses


@router.get("/api/filters", response_model=FilterOptionsResponse)
async def get_filter_options(db: Session = Depends(get_db)):
    """
    Get available filter options for search
    """
    from models import LegalLevel, DocumentType, BindingStatus, SourceBody
    
    topics = db.query(Topic).all()
    
    return FilterOptionsResponse(
        legal_levels=[level.value for level in LegalLevel],
        document_types=[dtype.value for dtype in DocumentType],
        binding_statuses=[status.value for status in BindingStatus],
        source_bodies=[body.value for body in SourceBody],
        topics=[topic.name for topic in topics]
    )


@router.get("/api/search/suggestions")
async def get_search_suggestions(
    q: str = Query(..., min_length=2, max_length=100)
):
    """
    Get search suggestions based on partial query
    
    - **q**: Partial search query
    """
    suggestions = search_engine.get_suggestions(q)
    return {
        'query': q,
        'suggestions': suggestions
    }


@router.get("/api/stats")
async def get_statistics(db: Session = Depends(get_db)):
    """
    Get system statistics
    """
    from models import LegalLevel, DocumentType
    
    total_docs = db.query(Document).count()
    
    # Count by legal level
    by_level = {}
    for level in LegalLevel:
        count = db.query(Document).filter(Document.legal_level == level).count()
        by_level[level.value] = count
    
    # Count by document type
    by_type = {}
    for dtype in DocumentType:
        count = db.query(Document).filter(Document.document_type == dtype).count()
        by_type[dtype.value] = count
    
    # Search index stats
    search_stats = search_engine.get_stats()
    
    return {
        'total_documents': total_docs,
        'by_legal_level': by_level,
        'by_document_type': by_type,
        'search_index': search_stats,
        'last_updated': datetime.utcnow().isoformat()
    }


@router.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    }

# Made with Bob
