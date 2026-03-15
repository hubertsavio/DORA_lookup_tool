"""
Index all documents in the database for search
"""
from models import init_db, get_session, Document
from utils import DORASearchEngine

def index_all_documents():
    """Index all documents from database into search engine"""
    engine = init_db()
    session = get_session(engine)
    search_engine = DORASearchEngine()
    
    # Get all documents
    documents = session.query(Document).all()
    
    if not documents:
        print("No documents found in database")
        return
    
    print(f"Indexing {len(documents)} documents...")
    
    # Convert to dict format for indexing
    docs_to_index = []
    for doc in documents:
        doc_dict = {
            'id': doc.id,
            'title': doc.title,
            'summary': doc.summary,
            'full_text': doc.full_text or '',
            'legal_level': doc.legal_level.value,
            'document_type': doc.document_type.value,
            'binding_status': doc.binding_status.value,
            'source_body': doc.source_body.value,
            'topics': [t.name for t in doc.topics],
            'url': doc.url,
            'publication_date': doc.publication_date,
            'is_qa': doc.is_qa,
            'is_oversight_only': doc.is_oversight_only
        }
        docs_to_index.append(doc_dict)
    
    # Index all documents
    search_engine.index_documents_bulk(docs_to_index)
    
    print(f"✅ Successfully indexed {len(documents)} documents")
    
    # Test search
    print("\nTesting search...")
    results = search_engine.search("ICT incident", limit=3)
    print(f"Found {len(results)} results for 'ICT incident'")
    for result in results:
        print(f"  - {result['title']}")
    
    session.close()

if __name__ == "__main__":
    index_all_documents()

# Made with Bob
