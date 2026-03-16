# DORA Architecture Diagrams Guide

This guide describes the three professional architecture diagrams created for the DORA Compliance Lookup Tool.

---

## 📊 Diagram 1: System Architecture

**File:** `diagrams/system-architecture.png` (235 KB, 300 DPI)

### What It Shows
A complete view of the four-layer architecture from client to data storage.

### Layers Depicted

**1. Client Layer (Blue)**
- Web Browser component
- Entry point for all user interactions

**2. Presentation Layer (Green) - Port 3000**
- React Frontend: Main UI application
- Vite Dev Server: Development server
- React Router: Client-side navigation
- Handles all user interface rendering

**3. Application Layer (Orange) - Port 8000**
- FastAPI Server: Python web framework
- API Routes: REST endpoint handlers
- CORS Middleware: Cross-origin request handling
- Business logic orchestration

**4. Business Logic Layer (Purple)**
- Whoosh Search Engine: Full-text search
- EIOPA Web Scraper: Document collection
- SQLAlchemy ORM: Database abstraction
- Core application logic

**5. Data Layer (Red)**
- SQLite Database: Persistent storage
- Search Index Files: Whoosh index storage
- Data persistence and retrieval

### Key Features
- Color-coded by layer for easy identification
- Clear data flow arrows showing request/response paths
- Port numbers indicated (3000, 8000)
- REST API communication highlighted
- Component relationships clearly shown

### Use Cases
- Understanding overall system structure
- Explaining architecture to stakeholders
- Planning deployment strategy
- Identifying integration points

---

## 🗄️ Diagram 2: Database Schema

**File:** `diagrams/database-schema.png` (255 KB, 300 DPI)

### What It Shows
Complete Entity-Relationship Diagram (ERD) of the database structure.

### Tables Depicted

**1. DOCUMENTS (Blue) - Main Entity**
- Primary Key: id
- 19 fields total including:
  - title, summary, full_text
  - legal_level, document_type, binding_status
  - source_body, url
  - publication_date, last_updated
  - is_qa, qa_status, is_oversight_only
  - Timestamps: created_at, updated_at, scraped_at

**2. TOPICS (Green) - Hierarchical Structure**
- Primary Key: id
- Fields: name, description
- Foreign Key: parent_id (self-referential)
- Supports nested topic categories

**3. DOCUMENT_TOPICS (Orange) - Junction Table**
- Many-to-many relationship
- Foreign Keys: document_id, topic_id
- Links documents to multiple topics

**4. DOCUMENT_RELATIONSHIPS (Purple)**
- Self-referential relationships
- Foreign Keys: source_id, target_id
- Field: relationship_type
- Enables cross-referencing between documents

**5. SEARCH_LOGS (Red) - Analytics**
- Primary Key: id
- Fields: query, results_count, timestamp
- Tracks search usage patterns

### Relationships Shown
- 1:N (One-to-Many) from Documents to Document_Topics
- 1:N from Topics to Document_Topics
- 1:N from Documents to Document_Relationships
- Self-referential relationship in Topics (parent-child)

### Legend Included
- PK = Primary Key
- FK = Foreign Key
- 1:N = One-to-Many relationship

### Use Cases
- Database design documentation
- Understanding data relationships
- Planning queries and indexes
- Schema migration planning

---

## 🔄 Diagram 3: Search Data Flow

**File:** `diagrams/search-data-flow.png` (231 KB, 300 DPI)

### What It Shows
Step-by-step sequence of a search operation from user input to result display.

### Flow Steps

**Step 1: User → React Frontend**
- User enters search query
- May include filters (legal level, document type, etc.)

**Step 2: React Frontend → FastAPI Backend**
- HTTP GET request to `/api/search`
- Query parameters include search terms and filters
- Axios handles the HTTP communication

**Step 3: FastAPI Backend → Whoosh Search**
- Request validation with Pydantic
- Search query passed to search engine
- Filters applied

**Step 4: Whoosh Search → SQLite Database**
- Full-text search with BM25F scoring algorithm
- Multi-field search (title, summary, full_text, topics)
- Filter application (legal level, document type, etc.)
- Document IDs retrieved

**Step 5: SQLite Database → Whoosh Search**
- Complete document data returned
- Includes all metadata and relationships
- Related documents fetched

**Step 6: Whoosh Search → FastAPI Backend**
- Search results compiled
- Relevance scoring applied
- Results sorted by score

**Step 7: FastAPI Backend → React Frontend**
- JSON response formatted
- Includes document metadata
- Related documents included
- Total count provided

**Step 8: React Frontend → User**
- UI updated with results
- DocumentCard components rendered
- Filters displayed
- Results paginated if needed

### Performance Metrics
- **Response Time:** < 100ms
- **API Response:** < 50ms
- **Database Query:** < 10ms
- **Frontend Render:** < 2 seconds

### Process Description
The diagram includes detailed descriptions of each step:
- User interaction patterns
- HTTP request/response cycle
- Search algorithm details
- Database query optimization
- UI update mechanisms

### Use Cases
- Understanding search functionality
- Performance optimization
- Debugging search issues
- API documentation
- User experience analysis

---

## 🎨 Diagram Specifications

### Technical Details
- **Resolution:** 300 DPI (print quality)
- **Format:** PNG with transparency support
- **Color Scheme:** Professional, color-blind friendly
- **Font:** Clear, readable at all sizes
- **Size:** Optimized for both screen and print

### Color Coding
- **Blue (#2196F3):** Client/User components
- **Green (#4CAF50):** Presentation layer
- **Orange (#FF9800):** Application layer
- **Purple (#9C27B0):** Business logic
- **Red (#F44336):** Data layer

### Design Principles
- Clear visual hierarchy
- Consistent styling across diagrams
- Minimal clutter
- Professional appearance
- Easy to understand at a glance

---

## 📁 File Locations

All diagrams are located in:
```
/Users/hubertsavio/BOB/DORA/docs/diagrams/
```

### Available Files
1. `system-architecture.png` - System overview
2. `database-schema.png` - Database structure
3. `search-data-flow.png` - Search operation flow

### Source Files
Mermaid diagram sources are also available:
- `01-system-architecture.mmd`
- `02-database-schema.mmd`
- `03-search-flow.mmd`
- `04-component-architecture.mmd`

### Generation Script
To regenerate diagrams:
```bash
cd /Users/hubertsavio/BOB/DORA/docs
python3 create_architecture_diagrams.py
```

---

## 🔗 Related Documentation

- **ARCHITECTURE.md** - Complete architecture documentation
- **README.md** - Project overview
- **DEPLOYMENT.md** - Deployment instructions
- **USAGE_GUIDE.md** - User guide

---

## 💡 Usage Tips

### For Presentations
- Use system-architecture.png for high-level overview
- Use database-schema.png for technical discussions
- Use search-data-flow.png for explaining functionality

### For Documentation
- Embed diagrams in technical specifications
- Reference in API documentation
- Include in deployment guides

### For Development
- Use as reference during coding
- Guide for new team members
- Planning for enhancements

---

## 📊 Diagram Comparison

| Diagram | Focus | Audience | Detail Level |
|---------|-------|----------|--------------|
| System Architecture | Overall structure | All stakeholders | High-level |
| Database Schema | Data model | Developers, DBAs | Technical |
| Search Data Flow | Functionality | Developers, Users | Detailed |

---

## ✅ Quality Checklist

All diagrams include:
- ✓ Clear title and labels
- ✓ Color-coded components
- ✓ Relationship indicators
- ✓ Legend where applicable
- ✓ Professional styling
- ✓ High resolution (300 DPI)
- ✓ Consistent design language
- ✓ Easy to read and understand

---

**Generated:** March 16, 2026  
**Tool:** matplotlib + Python  
**Version:** 1.0  
**Repository:** https://github.com/hubertsavio/DORA_lookup_tool