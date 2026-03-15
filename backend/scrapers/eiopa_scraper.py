"""
EIOPA DORA Hub Web Scraper

Scrapes DORA-related content from EIOPA website including:
- Main DORA regulations and directives
- Technical standards (RTS/ITS)
- Guidelines
- Q&As
- Supporting materials
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from datetime import datetime
import time
import logging
from urllib.parse import urljoin, urlparse
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EIOPAScraper:
    """Scraper for EIOPA DORA content"""
    
    BASE_URL = "https://www.eiopa.europa.eu"
    DORA_HUB_URL = f"{BASE_URL}/browse/regulation-and-policy/digital-operational-resilience-act-dora_en"
    
    def __init__(self, delay: float = 1.0):
        """
        Initialize scraper
        
        Args:
            delay: Delay between requests in seconds (be respectful)
        """
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'DORA-Compliance-Tool/1.0 (Educational/Research Purpose)'
        })
        self.scraped_urls = set()
    
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch and parse a webpage
        
        Args:
            url: URL to fetch
            
        Returns:
            BeautifulSoup object or None if failed
        """
        try:
            logger.info(f"Fetching: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            time.sleep(self.delay)  # Be respectful
            return BeautifulSoup(response.content, 'html5lib')
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def extract_document_metadata(self, soup: BeautifulSoup, url: str) -> Dict:
        """
        Extract metadata from a document page
        
        Args:
            soup: BeautifulSoup object of the page
            url: URL of the page
            
        Returns:
            Dictionary with document metadata
        """
        metadata = {
            'url': url,
            'title': '',
            'summary': '',
            'full_text': '',
            'publication_date': None,
            'last_updated': None,
            'document_type': 'OTHER',
            'legal_level': 'SUPPORTING',
            'binding_status': 'INFORMATIONAL',
            'source_body': 'EIOPA',
            'topics': [],
            'is_qa': False,
            'is_oversight_only': False
        }
        
        # Extract title
        title_elem = soup.find('h1') or soup.find('title')
        if title_elem:
            metadata['title'] = title_elem.get_text(strip=True)
        
        # Extract main content
        content_elem = soup.find('div', class_='content') or soup.find('article')
        if content_elem:
            metadata['full_text'] = content_elem.get_text(separator='\n', strip=True)
            # Generate summary (first 500 chars)
            metadata['summary'] = metadata['full_text'][:500] + '...' if len(metadata['full_text']) > 500 else metadata['full_text']
        
        # Classify document type based on title and URL
        title_lower = metadata['title'].lower()
        url_lower = url.lower()
        
        if 'regulation (eu)' in title_lower or 'directive (eu)' in title_lower:
            metadata['legal_level'] = 'LEVEL_1'
            metadata['binding_status'] = 'BINDING'
            if 'regulation' in title_lower:
                metadata['document_type'] = 'REGULATION'
            else:
                metadata['document_type'] = 'DIRECTIVE'
        
        elif 'rts' in title_lower or 'regulatory technical standard' in title_lower:
            metadata['legal_level'] = 'LEVEL_2'
            metadata['binding_status'] = 'TECHNICAL_STANDARD'
            metadata['document_type'] = 'RTS'
        
        elif 'its' in title_lower or 'implementing technical standard' in title_lower:
            metadata['legal_level'] = 'LEVEL_2'
            metadata['binding_status'] = 'TECHNICAL_STANDARD'
            metadata['document_type'] = 'ITS'
        
        elif 'delegated regulation' in title_lower:
            metadata['legal_level'] = 'LEVEL_2'
            metadata['binding_status'] = 'TECHNICAL_STANDARD'
            metadata['document_type'] = 'DELEGATED_REGULATION'
        
        elif 'guideline' in title_lower:
            metadata['legal_level'] = 'LEVEL_3'
            metadata['binding_status'] = 'GUIDANCE'
            metadata['document_type'] = 'GUIDELINE'
        
        elif 'q&a' in title_lower or 'question' in title_lower:
            metadata['is_qa'] = True
            metadata['binding_status'] = 'INTERPRETIVE'
            metadata['document_type'] = 'QA'
        
        elif 'opinion' in title_lower:
            metadata['document_type'] = 'OPINION'
            metadata['binding_status'] = 'GUIDANCE'
        
        elif 'statement' in title_lower:
            metadata['document_type'] = 'STATEMENT'
            metadata['binding_status'] = 'INFORMATIONAL'
        
        elif 'report' in title_lower:
            metadata['document_type'] = 'REPORT'
            metadata['binding_status'] = 'INFORMATIONAL'
        
        # Detect oversight-only content
        if 'oversight' in title_lower or 'ctpp' in title_lower or 'critical third-party' in title_lower:
            metadata['is_oversight_only'] = True
        
        # Extract topics
        if 'ict risk' in title_lower or 'ict risk management' in title_lower:
            metadata['topics'].append('ICT Risk Management')
        if 'third-party' in title_lower or 'third party' in title_lower:
            metadata['topics'].append('ICT Third-Party Risk Management')
        if 'testing' in title_lower or 'tlpt' in title_lower or 'penetration' in title_lower:
            metadata['topics'].append('Digital Operational Resilience Testing')
        if 'incident' in title_lower:
            metadata['topics'].append('ICT-Related Incidents')
        if 'information sharing' in title_lower or 'threat intelligence' in title_lower:
            metadata['topics'].append('Information Sharing')
        if 'oversight' in title_lower or 'ctpp' in title_lower:
            metadata['topics'].append('Oversight of Critical Third-Party Providers')
        
        # Extract dates
        date_pattern = r'\d{1,2}[/-]\d{1,2}[/-]\d{4}|\d{4}[/-]\d{1,2}[/-]\d{1,2}'
        dates = re.findall(date_pattern, metadata['full_text'][:1000])
        if dates:
            try:
                metadata['publication_date'] = datetime.strptime(dates[0], '%Y-%m-%d')
            except:
                pass
        
        return metadata
    
    def scrape_dora_hub(self) -> List[Dict]:
        """
        Scrape the main DORA hub page and extract all document links
        
        Returns:
            List of document metadata dictionaries
        """
        documents = []
        
        logger.info("Starting DORA hub scrape...")
        soup = self.fetch_page(self.DORA_HUB_URL)
        
        if not soup:
            logger.error("Failed to fetch DORA hub page")
            return documents
        
        # Find all links on the page
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link['href']
            full_url = urljoin(self.BASE_URL, href)
            
            # Skip if already scraped or not relevant
            if full_url in self.scraped_urls:
                continue
            
            # Filter for DORA-related content
            if not self._is_dora_related(full_url, link.get_text()):
                continue
            
            self.scraped_urls.add(full_url)
            
            # Fetch and parse document page
            doc_soup = self.fetch_page(full_url)
            if doc_soup:
                metadata = self.extract_document_metadata(doc_soup, full_url)
                documents.append(metadata)
                logger.info(f"Scraped: {metadata['title'][:50]}...")
        
        logger.info(f"Scraping complete. Found {len(documents)} documents.")
        return documents
    
    def _is_dora_related(self, url: str, text: str) -> bool:
        """
        Check if a URL/link is DORA-related
        
        Args:
            url: URL to check
            text: Link text
            
        Returns:
            True if DORA-related
        """
        dora_keywords = [
            'dora', 'digital operational resilience',
            'ict risk', 'ict incident', 'ict third-party',
            'operational resilience', 'tlpt', 'penetration testing',
            'ctpp', 'critical third-party'
        ]
        
        url_lower = url.lower()
        text_lower = text.lower()
        
        return any(keyword in url_lower or keyword in text_lower for keyword in dora_keywords)
    
    def scrape_specific_sections(self) -> Dict[str, List[Dict]]:
        """
        Scrape specific DORA sections
        
        Returns:
            Dictionary with section names as keys and document lists as values
        """
        sections = {
            'regulations': [],
            'technical_standards': [],
            'guidelines': [],
            'qas': [],
            'supporting_materials': []
        }
        
        # This would be expanded with specific URLs for each section
        # For now, it's a placeholder structure
        
        return sections


def main():
    """Main function to run the scraper"""
    scraper = EIOPAScraper(delay=2.0)  # 2 second delay between requests
    
    # Scrape DORA hub
    documents = scraper.scrape_dora_hub()
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"Scraping Summary")
    print(f"{'='*60}")
    print(f"Total documents found: {len(documents)}")
    
    # Group by document type
    by_type = {}
    for doc in documents:
        doc_type = doc['document_type']
        by_type[doc_type] = by_type.get(doc_type, 0) + 1
    
    print("\nDocuments by type:")
    for doc_type, count in sorted(by_type.items()):
        print(f"  {doc_type}: {count}")
    
    print(f"\n{'='*60}\n")
    
    return documents


if __name__ == "__main__":
    main()

# Made with Bob
