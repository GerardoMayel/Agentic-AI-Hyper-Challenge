"""
Database initialization script
Creates tables and tests connection
"""

import os
import sys
from dotenv import load_dotenv

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine, Base
from app.models.claim_models import ClaimForm, Document
from sqlalchemy import text

def init_database():
    """Initialize database tables"""
    try:
        print("🔧 Initializing database...")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        print("✅ Database tables created successfully!")
        print("📋 Created tables:")
        print("   - CLAIM_FORM")
        print("   - DOCUMENTS")
        
        return True
        
    except Exception as e:
        print(f"❌ Error initializing database: {str(e)}")
        return False

def test_connection():
    """Test database connection"""
    try:
        print("🔍 Testing database connection...")
        
        # Try to connect
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            result.fetchone()
            print("✅ Database connection successful!")
            return True
            
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    load_dotenv()
    
    print("🚀 Zurich Claims Database Initialization")
    print("=" * 50)
    
    # Test connection first
    if test_connection():
        # Initialize tables
        init_database()
    else:
        print("❌ Cannot proceed without database connection")
        sys.exit(1) 