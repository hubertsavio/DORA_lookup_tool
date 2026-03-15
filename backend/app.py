"""
Main FastAPI application for DORA Compliance Lookup Tool
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from api.routes import router
from models import init_db, seed_topics, get_session

# Initialize FastAPI app
app = FastAPI(
    title="DORA Compliance Lookup Tool",
    description=(
        "Regulatory research assistant for EU DORA (Digital Operational Resilience Act) compliance. "
        "⚠️ DISCLAIMER: This tool is for regulatory research purposes only. "
        "It does NOT provide legal advice or certify compliance."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    """Initialize database and search index on startup"""
    print("Initializing DORA Compliance Lookup Tool...")
    
    # Initialize database
    engine = init_db()
    session = get_session(engine)
    
    # Check if topics exist, if not seed them
    from models import Topic
    if session.query(Topic).count() == 0:
        print("Seeding initial topics...")
        seed_topics(session)
    
    session.close()
    print("Startup complete!")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "disclaimer": (
                "This tool is for regulatory research purposes only. "
                "It does NOT provide legal advice or certify compliance."
            )
        }
    )


@app.get("/")
async def root():
    """Root endpoint with welcome message"""
    return {
        "message": "Welcome to DORA Compliance Lookup Tool API",
        "version": "1.0.0",
        "documentation": "/docs",
        "disclaimer": (
            "⚠️ IMPORTANT: This tool is for regulatory research purposes only. "
            "It does NOT provide legal advice or certify compliance. "
            "Always consult qualified legal counsel for compliance decisions."
        ),
        "endpoints": {
            "search": "/api/search",
            "documents": "/api/documents/{id}",
            "related": "/api/documents/{id}/related",
            "topics": "/api/topics",
            "filters": "/api/filters",
            "suggestions": "/api/search/suggestions",
            "stats": "/api/stats",
            "health": "/api/health"
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

# Made with Bob
