"""
Search engine for DORA documents using Whoosh full-text search
"""
from whoosh.index import create_in, open_dir, exists_in
from whoosh.fields import Schema, TEXT, ID, KEYWORD, DATETIME, BOOLEAN
from whoosh.qparser import MultifieldParser, OrGroup
from whoosh.query import And, Or, Term
from whoosh import scoring
import os
from typing import List, Dict, Optional
from datetime import datetime


class DORASearchEngine:
    """Full-text search engine for DORA documents"""
    
    def __init__(self, index_dir: str = "search_index"):
        """
        Initialize search engine
        
        Args:
            index_dir: Directory to store search index
        """
        self.index_dir = index_dir
        self.schema = self._create_schema()
        self.index = self._get_or_create_index()
    
    def _create_schema(self) -> Schema:
        """Create Whoosh schema for DORA documents"""
        return Schema(
            id=ID(stored=True, unique=True),
            title=TEXT(stored=True, field_boost=2.0),
            summary=TEXT(stored=True, field_boost=1.5),
            full_text=TEXT(stored=True),
            legal_level=KEYWORD(stored=True, lowercase=True),
            document_type=KEYWORD(stored=True, lowercase=True),
            binding_status=KEYWORD(stored=True, lowercase=True),
            source_body=KEYWORD(stored=True, lowercase=True),
            topics=KEYWORD(stored=True, lowercase=True, commas=True),
            url=ID(stored=True),
            publication_date=DATETIME(stored=True),
            is_qa=BOOLEAN(stored=True),
            is_oversight_only=BOOLEAN(stored=True)
        )
    
    def _get_or_create_index(self):
        """Get existing index or create new one"""
        if not os.path.exists(self.index_dir):
            os.makedirs(self.index_dir)
        
        if exists_in(self.index_dir):
            return open_dir(self.index_dir)
        else:
            return create_in(self.index_dir, self.schema)
    
    def index_document(self, doc: Dict):
        """
        Add or update a document in the search index
        
        Args:
            doc: Document dictionary with metadata
        """
        writer = self.index.writer()
        
        # Convert topics list to comma-separated string
        topics_str = ','.join(doc.get('topics', []))
        
        writer.update_document(
            id=str(doc['id']),
            title=doc.get('title', ''),
            summary=doc.get('summary', ''),
            full_text=doc.get('full_text', ''),
            legal_level=doc.get('legal_level', ''),
            document_type=doc.get('document_type', ''),
            binding_status=doc.get('binding_status', ''),
            source_body=doc.get('source_body', ''),
            topics=topics_str,
            url=doc.get('url', ''),
            publication_date=doc.get('publication_date'),
            is_qa=doc.get('is_qa', False),
            is_oversight_only=doc.get('is_oversight_only', False)
        )
        
        writer.commit()
    
    def index_documents_bulk(self, documents: List[Dict]):
        """
        Index multiple documents at once
        
        Args:
            documents: List of document dictionaries
        """
        writer = self.index.writer()
        
        for doc in documents:
            topics_str = ','.join(doc.get('topics', []))
            
            writer.update_document(
                id=str(doc['id']),
                title=doc.get('title', ''),
                summary=doc.get('summary', ''),
                full_text=doc.get('full_text', ''),
                legal_level=doc.get('legal_level', ''),
                document_type=doc.get('document_type', ''),
                binding_status=doc.get('binding_status', ''),
                source_body=doc.get('source_body', ''),
                topics=topics_str,
                url=doc.get('url', ''),
                publication_date=doc.get('publication_date'),
                is_qa=doc.get('is_qa', False),
                is_oversight_only=doc.get('is_oversight_only', False)
            )
        
        writer.commit()
    
    def search(
        self,
        query: str,
        filters: Optional[Dict] = None,
        limit: int = 50,
        include_qa: bool = True,
        include_oversight: bool = True
    ) -> List[Dict]:
        """
        Search documents with optional filters
        
        Args:
            query: Search query string
            filters: Dictionary of filters (legal_level, document_type, etc.)
            limit: Maximum number of results
            include_qa: Include Q&A documents
            include_oversight: Include oversight-only documents
            
        Returns:
            List of matching documents
        """
        with self.index.searcher(weighting=scoring.BM25F()) as searcher:
            # Parse query across multiple fields
            parser = MultifieldParser(
                ['title', 'summary', 'full_text', 'topics'],
                schema=self.schema,
                group=OrGroup
            )
            
            parsed_query = parser.parse(query)
            
            # Build filter query
            filter_query = None
            if filters:
                filter_terms = []
                
                if 'legal_level' in filters and filters['legal_level']:
                    filter_terms.append(Term('legal_level', filters['legal_level'].lower()))
                
                if 'document_type' in filters and filters['document_type']:
                    filter_terms.append(Term('document_type', filters['document_type'].lower()))
                
                if 'binding_status' in filters and filters['binding_status']:
                    filter_terms.append(Term('binding_status', filters['binding_status'].lower()))
                
                if 'source_body' in filters and filters['source_body']:
                    filter_terms.append(Term('source_body', filters['source_body'].lower()))
                
                if 'topics' in filters and filters['topics']:
                    for topic in filters['topics']:
                        filter_terms.append(Term('topics', topic.lower()))
                
                if filter_terms:
                    filter_query = And(filter_terms)
            
            # Add Q&A and oversight filters
            additional_filters = []
            if not include_qa:
                additional_filters.append(Term('is_qa', False))
            if not include_oversight:
                additional_filters.append(Term('is_oversight_only', False))
            
            if additional_filters:
                if filter_query:
                    filter_query = And([filter_query] + additional_filters)
                else:
                    filter_query = And(additional_filters)
            
            # Execute search
            results = searcher.search(
                parsed_query,
                filter=filter_query,
                limit=limit
            )
            
            # Convert results to list of dicts
            documents = []
            for hit in results:
                doc = {
                    'id': hit['id'],
                    'title': hit['title'],
                    'summary': hit['summary'],
                    'legal_level': hit['legal_level'],
                    'document_type': hit['document_type'],
                    'binding_status': hit['binding_status'],
                    'source_body': hit['source_body'],
                    'topics': hit['topics'].split(',') if hit['topics'] else [],
                    'url': hit['url'],
                    'publication_date': hit['publication_date'],
                    'is_qa': hit['is_qa'],
                    'is_oversight_only': hit['is_oversight_only'],
                    'score': hit.score
                }
                documents.append(doc)
            
            return documents
    
    def get_suggestions(self, partial_query: str, field: str = 'title') -> List[str]:
        """
        Get search suggestions based on partial query
        
        Args:
            partial_query: Partial search term
            field: Field to search for suggestions
            
        Returns:
            List of suggested terms
        """
        suggestions = []
        with self.index.searcher() as searcher:
            # Get terms that start with the partial query
            for term in searcher.lexicon(field):
                if term.decode('utf-8').startswith(partial_query.lower()):
                    suggestions.append(term.decode('utf-8'))
                if len(suggestions) >= 10:
                    break
        
        return suggestions
    
    def clear_index(self):
        """Clear all documents from the index"""
        writer = self.index.writer()
        writer.commit(mergetype=3)  # Optimize and clear
    
    def get_stats(self) -> Dict:
        """Get index statistics"""
        with self.index.searcher() as searcher:
            return {
                'total_documents': searcher.doc_count_all(),
                'indexed_fields': list(self.schema.names())
            }


def main():
    """Test the search engine"""
    engine = DORASearchEngine()
    
    # Test document
    test_doc = {
        'id': 1,
        'title': 'Regulation (EU) 2022/2554 on Digital Operational Resilience',
        'summary': 'Main DORA regulation establishing requirements for ICT risk management',
        'full_text': 'This regulation establishes uniform requirements for the security of network and information systems...',
        'legal_level': 'LEVEL_1',
        'document_type': 'REGULATION',
        'binding_status': 'BINDING',
        'source_body': 'EU_COMMISSION',
        'topics': ['ICT Risk Management', 'Digital Operational Resilience Testing'],
        'url': 'https://example.com/regulation',
        'publication_date': datetime.now(),
        'is_qa': False,
        'is_oversight_only': False
    }
    
    # Index test document
    engine.index_document(test_doc)
    
    # Test search
    results = engine.search('ICT risk management')
    print(f"Found {len(results)} results")
    for result in results:
        print(f"- {result['title']} (score: {result['score']:.2f})")
    
    # Get stats
    stats = engine.get_stats()
    print(f"\nIndex stats: {stats}")


if __name__ == "__main__":
    main()

# Made with Bob
