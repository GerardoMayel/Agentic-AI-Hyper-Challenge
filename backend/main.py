"""
Main FastAPI application for Claims Management System
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import uvicorn
import threading
import time
import os

from app.core.database import engine, Base
from app.models.email_models import Email, ClaimSubmission, DocumentAgentOCR, ClaimStatusUpdate, DashboardStats
from app.services.email_scheduler import email_scheduler
from app.api.analyst_api import router as analyst_router

# Create tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for the application"""
    # Startup
    print("🚀 Starting Claims Management System...")
    
    # Start email scheduler in separate thread
    def start_scheduler():
        time.sleep(5)  # Wait for app to be ready
        email_scheduler.start_scheduler()
    
    scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
    scheduler_thread.start()
    
    print("✅ System started successfully")
    
    yield
    
    # Shutdown
    print("🛑 Stopping Claims Management System...")
    email_scheduler.stop_scheduler()
    print("✅ System stopped")

# Create FastAPI application
app = FastAPI(
    title="Claims Management System",
    description="Automated insurance claims processing system",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analyst_router)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Basic endpoints
@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Claims Management System API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "analyst_dashboard": "/analyst",
            "api_docs": "/docs",
            "health": "/health"
        }
    }

@app.get("/analyst")
def analyst_dashboard():
    """Analyst dashboard interface"""
    return FileResponse("app/static/analyst_dashboard.html")

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "services": {
            "database": "connected",
            "email_scheduler": "running" if email_scheduler.is_running else "stopped",
            "gmail_service": "available",
            "llm_service": "available"
        }
    }

@app.get("/api/status")
def get_system_status():
    """Get system status"""
    return {
        "system": "Claims Management System",
        "version": "1.0.0",
        "email_scheduler": {
            "running": email_scheduler.is_running,
            "keywords": email_scheduler.claim_keywords
        },
        "endpoints": {
            "analyst": "/api/analyst",
            "health": "/health",
            "status": "/api/status"
        }
    }

# Scheduler control endpoints
@app.post("/api/scheduler/start")
def start_email_scheduler():
    """Start automatic email processing"""
    try:
        email_scheduler.start_scheduler()
        return {"message": "Email scheduler started", "status": "running"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting scheduler: {str(e)}")

@app.post("/api/scheduler/stop")
def stop_email_scheduler():
    """Stop automatic email processing"""
    try:
        email_scheduler.stop_scheduler()
        return {"message": "Email scheduler stopped", "status": "stopped"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error stopping scheduler: {str(e)}")

@app.get("/api/scheduler/status")
def get_scheduler_status():
    """Get email scheduler status"""
    return {
        "running": email_scheduler.is_running,
        "keywords": email_scheduler.claim_keywords,
        "last_check": "N/A"  # Can implement tracking of last check
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 