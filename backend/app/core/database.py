"""
Database configuration and connection setup with SQLite fallback
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import sqlite3
from pathlib import Path

# Load environment variables from project root
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))  # Go up 3 levels: core -> app -> backend -> project_root
env_path = os.path.join(project_root, '.env')
load_dotenv(env_path)

# Database URLs
RENDER_DATABASE_URL = os.getenv("DATABASE_URL")
SQLITE_DATABASE_PATH = os.path.join(os.path.dirname(current_dir), "data", "zurich_claims.db")

# Ensure SQLite data directory exists
sqlite_data_dir = os.path.dirname(SQLITE_DATABASE_PATH)
os.makedirs(sqlite_data_dir, exist_ok=True)

# SQLite fallback URL
SQLITE_DATABASE_URL = f"sqlite:///{SQLITE_DATABASE_PATH}"

def test_render_connection():
    """Test if Render database is available"""
    if not RENDER_DATABASE_URL:
        return False
    
    try:
        # Fix DATABASE_URL for Render PostgreSQL
        render_url = RENDER_DATABASE_URL
        if render_url.startswith("postgres://"):
            render_url = render_url.replace("postgres://", "postgresql://", 1)
        
        # Test connection with timeout
        test_engine = create_engine(
            render_url,
            pool_pre_ping=True,
            connect_args={"connect_timeout": 5}
        )
        
        with test_engine.connect() as conn:
            from sqlalchemy import text
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"⚠️ Render database not available: {e}")
        return False

def get_database_url():
    """Get the appropriate database URL based on availability"""
    if test_render_connection():
        print("✅ Using Render PostgreSQL database")
        # Fix DATABASE_URL for Render PostgreSQL
        url = RENDER_DATABASE_URL
        if url and url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        return url or SQLITE_DATABASE_URL
    else:
        print("🔄 Using SQLite fallback database")
        return SQLITE_DATABASE_URL

# Get the appropriate database URL
DATABASE_URL = get_database_url()

# Create SQLAlchemy engine with robust configuration
if DATABASE_URL.startswith("sqlite"):
    # SQLite configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        pool_pre_ping=True
    )
else:
    # PostgreSQL configuration
    engine = create_engine(
        DATABASE_URL, 
        pool_pre_ping=True,
        pool_recycle=300,  # Recycle connections every 5 minutes
        pool_timeout=20,   # Connection timeout
        max_overflow=10,   # Allow extra connections
        connect_args={
            "connect_timeout": 10,
            "application_name": "zurich-claims-api"
        }
    )

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_database_info():
    """Get information about which database is being used"""
    if DATABASE_URL and DATABASE_URL.startswith("sqlite"):
        return {
            "type": "sqlite",
            "path": SQLITE_DATABASE_PATH,
            "fallback": True
        }
    else:
        return {
            "type": "postgresql",
            "url": RENDER_DATABASE_URL[:50] + "..." if RENDER_DATABASE_URL else None,
            "fallback": False
        } 