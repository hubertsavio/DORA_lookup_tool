# DORA Compliance Lookup Tool

## Overview
A regulatory lookup assistant for EU financial-sector DORA (Digital Operational Resilience Act) compliance research. This tool helps users search, navigate, summarize, and cross-reference DORA requirements and supporting materials.

**⚠️ IMPORTANT DISCLAIMER**: This tool is for regulatory research and navigation purposes only. It does NOT provide definitive legal advice or certify compliance. Always consult qualified legal counsel for compliance decisions.

## Purpose
- Structured regulatory research interface
- Search and filter DORA documents by topic, legal level, and type
- Cross-reference related requirements
- Plain-language summaries of complex regulations
- Clear distinction between binding law, guidance, and interpretive materials

## Source Scope

### Main DORA Topic Areas
1. ICT risk management
2. ICT third-party risk management
3. Digital operational resilience testing
4. ICT-related incidents
5. Information sharing
6. Oversight of critical third-party providers (CTPP)

### Legal Hierarchy

#### Level 1 (Primary Legislation)
- Regulation (EU) 2022/2554
- Directive (EU) 2022/2556

#### Level 2 (Technical Standards)
- RTS on ICT risk management framework
- RTS on ICT incidents classification
- RTS on ICT incidents reporting process
- ITS on ICT incidents reporting
- RTS on Threat Led Penetration Testing (TLPT)
- RTS on ICT third-party policy
- RTS on subcontracting
- ITS on Register of Information
- Delegated Regulation on CTPP designation criteria
- Delegated Regulation on DORA oversight fees
- Oversight conditions acts
- Joint Examination Team acts

#### Level 3 (Guidelines & Guidance)
- Guidelines on oversight cooperation
- Guidelines on estimation of aggregated annual costs and losses caused by major ICT-related incidents

### Supporting Materials
- ESAs decisions
- Reporting tools
- Opinions
- Public statements
- Reports
- Roadmap for CTPP designation
- Oversight guide
- Opt-in process
- Oversight Forum material
- International cooperation and MoUs
- Equivalence assessments
- Declarations of interest

### Q&A Support
- Previously answered questions on DORA
- Joint Q&A Register
- Q&A statuses (under review, final, revised)
- Routing to EBA, EIOPA, and ESMA

## Architecture

### Backend (Python/FastAPI)
- **API Layer**: RESTful endpoints for search, filtering, and document retrieval
- **Scraper Module**: Web scraping from EIOPA DORA hub
- **Database**: SQLite/PostgreSQL for document storage and indexing
- **Search Engine**: Full-text search with filtering capabilities
- **Cross-Reference Engine**: Document relationship mapping

### Frontend (React)
- **Search Interface**: Natural language query input
- **Filter Panel**: Topic, legal level, document type, source body, binding status
- **Results Display**: Expandable cards with metadata
- **Cross-Reference Panel**: Related documents viewer
- **Disclaimer Banner**: Persistent legal notice

### Data Model
Each document contains:
- Title
- Summary (plain language)
- Topic category & subcategory
- Legal level (1, 2, 3, or supporting)
- Document type
- Binding status
- Applicability
- Date/last updated
- Source body (EBA, EIOPA, ESMA)
- URL
- Related documents (cross-references)

## Features

### Search Capabilities
- Natural language queries
- Full-text search across all documents
- Fuzzy matching for typos
- Synonym support

### Filtering Options
- Topic area
- Legal level
- Document type
- Source body
- Binding status
- Date range
- Include/exclude Q&As
- Include/exclude oversight-only materials

### Result Display
- Grouped by category
- Expandable details
- Clear labeling of document authority
- Source links
- Related documents panel

### Guardrails
- No compliance certification claims
- Explicit ambiguity warnings
- Source authority hierarchy respected
- Legal text prioritized over interpretive materials
- Clear distinction between requirements and guidance

## Installation

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 13+ (or SQLite for development)

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m scrapers.eiopa_scraper  # Initial data collection
python app.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## Usage Examples

### Search Queries
- "Show DORA rules for ICT incident reporting"
- "What are the DORA requirements for subcontracting?"
- "Find all DORA material related to CTPPs"
- "Show Level 2 measures for ICT risk management"
- "What guidance exists for oversight cooperation?"
- "Find DORA Q&As related to operational resilience testing"

### API Endpoints
- `GET /api/search?q={query}&filters={json}` - Search documents
- `GET /api/documents/{id}` - Get document details
- `GET /api/documents/{id}/related` - Get related documents
- `GET /api/topics` - List all topic categories
- `GET /api/filters` - Get available filter options

## Project Structure
```
DORA/
├── backend/
│   ├── api/              # FastAPI endpoints
│   ├── scrapers/         # EIOPA web scraper
│   ├── models/           # Database models
│   ├── utils/            # Helper functions
│   ├── app.py            # Main application
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   └── styles/       # CSS/styling
│   ├── public/
│   └── package.json
├── data/                 # Scraped data storage
├── docs/                 # Additional documentation
└── README.md
```

## Development Roadmap
1. ✅ Project structure setup
2. ⏳ Backend API implementation
3. ⏳ Web scraper development
4. ⏳ Database schema design
5. ⏳ Search engine implementation
6. ⏳ Frontend interface development
7. ⏳ Cross-reference system
8. ⏳ Testing and validation
9. ⏳ Deployment configuration

## Contributing
This is a regulatory research tool. Contributions should maintain:
- Accuracy of source material
- Clear distinction between legal levels
- Appropriate disclaimers
- No legal advice provision

## License
[To be determined]

## Contact
[To be determined]

## Acknowledgments
- EIOPA (European Insurance and Occupational Pensions Authority)
- EBA (European Banking Authority)
- ESMA (European Securities and Markets Authority)
- EU DORA Regulation (EU) 2022/2554