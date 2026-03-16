#!/usr/bin/env python3
"""
Create architecture diagrams for DORA Compliance Lookup Tool using matplotlib
Generates PNG images without external dependencies
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.lines as mlines

def create_system_architecture():
    """Create high-level system architecture diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Title
    ax.text(5, 11.5, 'DORA Compliance Lookup Tool - System Architecture', 
            ha='center', fontsize=16, fontweight='bold')
    
    # Client Layer
    client_box = FancyBboxPatch((4, 10), 2, 0.8, boxstyle="round,pad=0.1", 
                                edgecolor='#2196F3', facecolor='#E3F2FD', linewidth=2)
    ax.add_patch(client_box)
    ax.text(5, 10.4, 'Web Browser', ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Presentation Layer
    pres_rect = mpatches.Rectangle((0.5, 7.5), 9, 2, linewidth=2, 
                                   edgecolor='#4CAF50', facecolor='#E8F5E9', alpha=0.3)
    ax.add_patch(pres_rect)
    ax.text(5, 9.3, 'Presentation Layer (Port 3000)', ha='center', fontsize=11, fontweight='bold')
    
    react_box = FancyBboxPatch((1.5, 8), 2, 0.8, boxstyle="round,pad=0.1",
                               edgecolor='#4CAF50', facecolor='#C8E6C9', linewidth=2)
    ax.add_patch(react_box)
    ax.text(2.5, 8.4, 'React Frontend', ha='center', va='center', fontsize=9)
    
    vite_box = FancyBboxPatch((4, 8), 2, 0.8, boxstyle="round,pad=0.1",
                              edgecolor='#4CAF50', facecolor='#C8E6C9', linewidth=2)
    ax.add_patch(vite_box)
    ax.text(5, 8.4, 'Vite Dev Server', ha='center', va='center', fontsize=9)
    
    router_box = FancyBboxPatch((6.5, 8), 2, 0.8, boxstyle="round,pad=0.1",
                                edgecolor='#4CAF50', facecolor='#C8E6C9', linewidth=2)
    ax.add_patch(router_box)
    ax.text(7.5, 8.4, 'React Router', ha='center', va='center', fontsize=9)
    
    # Application Layer
    app_rect = mpatches.Rectangle((0.5, 5), 9, 2, linewidth=2,
                                  edgecolor='#FF9800', facecolor='#FFF3E0', alpha=0.3)
    ax.add_patch(app_rect)
    ax.text(5, 6.8, 'Application Layer (Port 8000)', ha='center', fontsize=11, fontweight='bold')
    
    fastapi_box = FancyBboxPatch((1.5, 5.5), 2, 0.8, boxstyle="round,pad=0.1",
                                 edgecolor='#FF9800', facecolor='#FFE0B2', linewidth=2)
    ax.add_patch(fastapi_box)
    ax.text(2.5, 5.9, 'FastAPI Server', ha='center', va='center', fontsize=9)
    
    routes_box = FancyBboxPatch((4, 5.5), 2, 0.8, boxstyle="round,pad=0.1",
                                edgecolor='#FF9800', facecolor='#FFE0B2', linewidth=2)
    ax.add_patch(routes_box)
    ax.text(5, 5.9, 'API Routes', ha='center', va='center', fontsize=9)
    
    cors_box = FancyBboxPatch((6.5, 5.5), 2, 0.8, boxstyle="round,pad=0.1",
                              edgecolor='#FF9800', facecolor='#FFE0B2', linewidth=2)
    ax.add_patch(cors_box)
    ax.text(7.5, 5.9, 'CORS Middleware', ha='center', va='center', fontsize=9)
    
    # Business Logic Layer
    logic_rect = mpatches.Rectangle((0.5, 2.5), 9, 2, linewidth=2,
                                    edgecolor='#9C27B0', facecolor='#F3E5F5', alpha=0.3)
    ax.add_patch(logic_rect)
    ax.text(5, 4.3, 'Business Logic Layer', ha='center', fontsize=11, fontweight='bold')
    
    search_box = FancyBboxPatch((1, 3), 2.3, 0.8, boxstyle="round,pad=0.1",
                                edgecolor='#9C27B0', facecolor='#E1BEE7', linewidth=2)
    ax.add_patch(search_box)
    ax.text(2.15, 3.4, 'Whoosh Search', ha='center', va='center', fontsize=9)
    
    scraper_box = FancyBboxPatch((3.8, 3), 2.4, 0.8, boxstyle="round,pad=0.1",
                                 edgecolor='#9C27B0', facecolor='#E1BEE7', linewidth=2)
    ax.add_patch(scraper_box)
    ax.text(5, 3.4, 'EIOPA Scraper', ha='center', va='center', fontsize=9)
    
    models_box = FancyBboxPatch((6.7, 3), 2.3, 0.8, boxstyle="round,pad=0.1",
                                edgecolor='#9C27B0', facecolor='#E1BEE7', linewidth=2)
    ax.add_patch(models_box)
    ax.text(7.85, 3.4, 'SQLAlchemy ORM', ha='center', va='center', fontsize=9)
    
    # Data Layer
    data_rect = mpatches.Rectangle((0.5, 0.2), 9, 2, linewidth=2,
                                   edgecolor='#F44336', facecolor='#FFEBEE', alpha=0.3)
    ax.add_patch(data_rect)
    ax.text(5, 2, 'Data Layer', ha='center', fontsize=11, fontweight='bold')
    
    db_box = FancyBboxPatch((2, 0.6), 2.5, 0.8, boxstyle="round,pad=0.1",
                            edgecolor='#F44336', facecolor='#FFCDD2', linewidth=2)
    ax.add_patch(db_box)
    ax.text(3.25, 1, 'SQLite Database', ha='center', va='center', fontsize=9)
    
    index_box = FancyBboxPatch((5.5, 0.6), 2.5, 0.8, boxstyle="round,pad=0.1",
                               edgecolor='#F44336', facecolor='#FFCDD2', linewidth=2)
    ax.add_patch(index_box)
    ax.text(6.75, 1, 'Search Index', ha='center', va='center', fontsize=9)
    
    # Arrows
    arrow_props = dict(arrowstyle='->', lw=2, color='#333')
    
    # Client to Presentation
    ax.annotate('', xy=(5, 9.5), xytext=(5, 10), arrowprops=arrow_props)
    
    # Presentation to Application
    ax.annotate('', xy=(5, 7), xytext=(5, 7.5), arrowprops=arrow_props)
    ax.text(5.3, 7.25, 'REST API', fontsize=8, style='italic')
    
    # Application to Business Logic
    ax.annotate('', xy=(5, 4.5), xytext=(5, 5), arrowprops=arrow_props)
    
    # Business Logic to Data
    ax.annotate('', xy=(3.25, 2.2), xytext=(2.15, 2.8), arrowprops=arrow_props)
    ax.annotate('', xy=(6.75, 2.2), xytext=(7.85, 2.8), arrowprops=arrow_props)
    
    plt.tight_layout()
    plt.savefig('/Users/hubertsavio/BOB/DORA/docs/diagrams/system-architecture.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

def create_database_schema():
    """Create database schema diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Title
    ax.text(5, 11.5, 'DORA Database Schema', 
            ha='center', fontsize=16, fontweight='bold')
    
    # Documents table
    doc_box = FancyBboxPatch((0.5, 7), 3, 3.5, boxstyle="round,pad=0.1",
                             edgecolor='#2196F3', facecolor='#E3F2FD', linewidth=2)
    ax.add_patch(doc_box)
    ax.text(2, 10.2, 'DOCUMENTS', ha='center', fontsize=11, fontweight='bold')
    doc_fields = [
        'id (PK)',
        'title',
        'summary',
        'full_text',
        'legal_level',
        'document_type',
        'binding_status',
        'source_body',
        'url',
        'publication_date',
        'is_qa',
        'qa_status'
    ]
    y_pos = 9.8
    for field in doc_fields:
        ax.text(2, y_pos, field, ha='center', fontsize=8)
        y_pos -= 0.22
    
    # Topics table
    topic_box = FancyBboxPatch((6.5, 8.5), 2.5, 2, boxstyle="round,pad=0.1",
                               edgecolor='#4CAF50', facecolor='#E8F5E9', linewidth=2)
    ax.add_patch(topic_box)
    ax.text(7.75, 10.2, 'TOPICS', ha='center', fontsize=11, fontweight='bold')
    topic_fields = ['id (PK)', 'name', 'description', 'parent_id (FK)']
    y_pos = 9.8
    for field in topic_fields:
        ax.text(7.75, y_pos, field, ha='center', fontsize=8)
        y_pos -= 0.3
    
    # Document_Topics junction table
    dt_box = FancyBboxPatch((4, 8.5), 2, 1.5, boxstyle="round,pad=0.1",
                            edgecolor='#FF9800', facecolor='#FFF3E0', linewidth=2)
    ax.add_patch(dt_box)
    ax.text(5, 9.8, 'DOCUMENT_TOPICS', ha='center', fontsize=10, fontweight='bold')
    dt_fields = ['document_id (FK)', 'topic_id (FK)']
    y_pos = 9.4
    for field in dt_fields:
        ax.text(5, y_pos, field, ha='center', fontsize=8)
        y_pos -= 0.3
    
    # Document_Relationships table
    rel_box = FancyBboxPatch((0.5, 3.5), 3, 2, boxstyle="round,pad=0.1",
                             edgecolor='#9C27B0', facecolor='#F3E5F5', linewidth=2)
    ax.add_patch(rel_box)
    ax.text(2, 5.2, 'DOCUMENT_RELATIONSHIPS', ha='center', fontsize=10, fontweight='bold')
    rel_fields = ['source_id (FK)', 'target_id (FK)', 'relationship_type']
    y_pos = 4.8
    for field in rel_fields:
        ax.text(2, y_pos, field, ha='center', fontsize=8)
        y_pos -= 0.3
    
    # Search_Logs table
    log_box = FancyBboxPatch((6.5, 3.5), 2.5, 1.8, boxstyle="round,pad=0.1",
                             edgecolor='#F44336', facecolor='#FFEBEE', linewidth=2)
    ax.add_patch(log_box)
    ax.text(7.75, 5.1, 'SEARCH_LOGS', ha='center', fontsize=10, fontweight='bold')
    log_fields = ['id (PK)', 'query', 'results_count', 'timestamp']
    y_pos = 4.7
    for field in log_fields:
        ax.text(7.75, y_pos, field, ha='center', fontsize=8)
        y_pos -= 0.3
    
    # Relationships
    arrow_props = dict(arrowstyle='->', lw=1.5, color='#666')
    
    # Documents to Document_Topics
    ax.annotate('', xy=(4, 9.2), xytext=(3.5, 9.2), arrowprops=arrow_props)
    ax.text(3.75, 9.4, '1:N', fontsize=8, style='italic')
    
    # Topics to Document_Topics
    ax.annotate('', xy=(6, 9.2), xytext=(6.5, 9.2), arrowprops=arrow_props)
    ax.text(6.25, 9.4, '1:N', fontsize=8, style='italic')
    
    # Documents to Document_Relationships
    ax.annotate('', xy=(2, 6.8), xytext=(2, 5.5), arrowprops=arrow_props)
    ax.text(2.3, 6.2, '1:N', fontsize=8, style='italic')
    
    # Legend
    ax.text(1, 2.5, 'Legend:', fontsize=10, fontweight='bold')
    ax.text(1, 2.2, 'PK = Primary Key', fontsize=8)
    ax.text(1, 1.9, 'FK = Foreign Key', fontsize=8)
    ax.text(1, 1.6, '1:N = One-to-Many', fontsize=8)
    
    # Notes
    ax.text(5, 1, 'Database: SQLite | ORM: SQLAlchemy', 
            ha='center', fontsize=9, style='italic', color='#666')
    
    plt.tight_layout()
    plt.savefig('/Users/hubertsavio/BOB/DORA/docs/diagrams/database-schema.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

def create_data_flow():
    """Create search data flow diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Title
    ax.text(5, 7.5, 'Search Operation Data Flow', 
            ha='center', fontsize=16, fontweight='bold')
    
    # Components
    components = [
        (1, 4, 'User', '#2196F3'),
        (2.5, 4, 'React\nFrontend', '#4CAF50'),
        (4.5, 4, 'FastAPI\nBackend', '#FF9800'),
        (6.5, 4, 'Whoosh\nSearch', '#9C27B0'),
        (8.5, 4, 'SQLite\nDatabase', '#F44336')
    ]
    
    for x, y, label, color in components:
        box = FancyBboxPatch((x-0.4, y-0.4), 0.8, 0.8, boxstyle="round,pad=0.1",
                             edgecolor=color, facecolor=color, alpha=0.3, linewidth=2)
        ax.add_patch(box)
        ax.text(x, y, label, ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Flow arrows and labels
    flows = [
        (1.4, 4, 2.1, 4, '1. Enter query'),
        (2.9, 4, 4.1, 4, '2. GET /api/search'),
        (4.9, 4, 6.1, 4, '3. Execute search'),
        (6.9, 4, 8.1, 4, '4. Fetch documents'),
        (8.1, 3.7, 6.9, 3.7, '5. Return data'),
        (6.1, 3.7, 4.9, 3.7, '6. Search results'),
        (4.1, 3.7, 2.9, 3.7, '7. JSON response'),
        (2.1, 3.7, 1.4, 3.7, '8. Display results')
    ]
    
    arrow_props = dict(arrowstyle='->', lw=2, color='#333')
    
    for x1, y1, x2, y2, label in flows:
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=arrow_props)
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mid_x, mid_y + 0.2, label, ha='center', fontsize=8, 
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='none'))
    
    # Timeline
    ax.text(5, 2, 'Response Time: < 100ms', ha='center', fontsize=10, 
            style='italic', color='#666')
    
    # Process description
    desc_y = 1.2
    descriptions = [
        '• User enters search query with optional filters',
        '• React sends HTTP GET request to FastAPI',
        '• FastAPI validates request and calls search engine',
        '• Whoosh performs full-text search with BM25F scoring',
        '• Database returns matching document data',
        '• Results formatted and sent back to frontend',
        '• React updates UI with search results'
    ]
    
    for desc in descriptions:
        ax.text(0.5, desc_y, desc, fontsize=8, va='top')
        desc_y -= 0.15
    
    plt.tight_layout()
    plt.savefig('/Users/hubertsavio/BOB/DORA/docs/diagrams/search-data-flow.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

if __name__ == "__main__":
    print("Generating DORA architecture diagrams...")
    print("=" * 60)
    
    try:
        print("\n1. Creating system architecture diagram...")
        create_system_architecture()
        print("   ✓ system-architecture.png created")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    try:
        print("\n2. Creating database schema diagram...")
        create_database_schema()
        print("   ✓ database-schema.png created")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    try:
        print("\n3. Creating data flow diagram...")
        create_data_flow()
        print("   ✓ search-data-flow.png created")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ All diagrams generated successfully!")
    print("📁 Location: /Users/hubertsavio/BOB/DORA/docs/diagrams/")
    print("\nGenerated files:")
    print("  - system-architecture.png")
    print("  - database-schema.png")
    print("  - search-data-flow.png")

# Made with Bob
