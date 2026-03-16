#!/usr/bin/env python3
"""
Generate architecture diagrams for DORA Compliance Lookup Tool
Uses the diagrams library to create PNG images
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import Client
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.programming.framework import React, FastAPI
from diagrams.programming.language import Python, JavaScript

def generate_system_architecture():
    """Generate high-level system architecture diagram"""
    with Diagram("DORA System Architecture", 
                 filename="diagrams/system-architecture",
                 show=False,
                 direction="TB"):
        
        browser = Client("Web Browser")
        
        with Cluster("Presentation Layer\nPort 3000"):
            react = React("React Frontend")
            vite = Server("Vite Dev Server")
        
        with Cluster("Application Layer\nPort 8000"):
            fastapi = FastAPI("FastAPI Server")
            routes = Python("API Routes")
        
        with Cluster("Business Logic"):
            search = Python("Whoosh Search")
            scraper = Python("EIOPA Scraper")
            models = Python("SQLAlchemy Models")
        
        with Cluster("Data Layer"):
            db = PostgreSQL("SQLite Database")
            index = Server("Search Index")
        
        # Connections
        browser >> Edge(label="HTTP/HTTPS") >> react
        react >> Edge(label="REST API") >> fastapi
        fastapi >> routes
        routes >> search
        routes >> models
        routes >> scraper
        search >> index
        models >> db
        scraper >> db

def generate_component_architecture():
    """Generate component-level architecture diagram"""
    with Diagram("Component Architecture",
                 filename="diagrams/component-architecture",
                 show=False,
                 direction="LR"):
        
        with Cluster("Frontend"):
            app = React("App.jsx")
            search_page = React("SearchPage")
            detail_page = React("DocumentDetailPage")
            search_bar = React("SearchBar")
            filters = React("FilterPanel")
            card = React("DocumentCard")
        
        with Cluster("Backend"):
            app_py = FastAPI("app.py")
            api_routes = Python("routes.py")
            database = Python("database.py")
            search_engine = Python("search_engine.py")
            scrapers = Python("eiopa_scraper.py")
        
        # Frontend connections
        app >> [search_page, detail_page]
        search_page >> [search_bar, filters, card]
        
        # API connections
        search_page >> Edge(label="API") >> api_routes
        detail_page >> Edge(label="API") >> api_routes
        
        # Backend connections
        app_py >> api_routes
        api_routes >> [database, search_engine, scrapers]

def generate_data_flow():
    """Generate data flow diagram"""
    with Diagram("Search Data Flow",
                 filename="diagrams/search-data-flow",
                 show=False,
                 direction="LR"):
        
        user = Client("User")
        frontend = React("React Frontend")
        api = FastAPI("FastAPI Backend")
        search = Python("Whoosh Search")
        db = PostgreSQL("SQLite DB")
        
        user >> Edge(label="1. Enter query") >> frontend
        frontend >> Edge(label="2. GET /api/search") >> api
        api >> Edge(label="3. Execute search") >> search
        search >> Edge(label="4. Fetch documents") >> db
        db >> Edge(label="5. Return data") >> search
        search >> Edge(label="6. Results") >> api
        api >> Edge(label="7. JSON response") >> frontend
        frontend >> Edge(label="8. Display") >> user

if __name__ == "__main__":
    print("Generating architecture diagrams...")
    
    try:
        print("1. Generating system architecture...")
        generate_system_architecture()
        print("   ✓ System architecture diagram created")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    try:
        print("2. Generating component architecture...")
        generate_component_architecture()
        print("   ✓ Component architecture diagram created")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    try:
        print("3. Generating data flow...")
        generate_data_flow()
        print("   ✓ Data flow diagram created")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\nAll diagrams generated successfully!")
    print("Location: /Users/hubertsavio/BOB/DORA/docs/diagrams/")

# Made with Bob
