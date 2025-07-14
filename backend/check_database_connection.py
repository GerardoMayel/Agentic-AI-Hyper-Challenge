#!/usr/bin/env python3
"""
Database connection test and table creation script
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.core.database import engine, Base
from app.models.email_models import Email, DashboardStats
from sqlalchemy import text
import time

def test_database_connection():
    """Test database connection"""
    print("🔍 Testing database connection...")
    
    try:
        # Test basic connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as test"))
            print("✅ Basic connection successful")
            
            # Test database info
            result = conn.execute(text("SELECT version()"))
            version_result = result.fetchone()
            if version_result:
                version = version_result[0]
                print(f"✅ Database version: {version}")
            
            # Test current database
            result = conn.execute(text("SELECT current_database()"))
            db_result = result.fetchone()
            if db_result:
                db_name = db_result[0]
                print(f"✅ Connected to database: {db_name}")
            
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def create_tables():
    """Create all tables"""
    print("\n🔨 Creating database tables...")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully")
        
        # Verify tables exist
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            
            tables = [row[0] for row in result.fetchall()]
            print(f"✅ Tables in database: {', '.join(tables)}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def test_table_operations():
    """Test basic table operations"""
    print("\n🧪 Testing table operations...")
    
    try:
        from sqlalchemy.orm import Session
        
        with Session(engine) as session:
            # Test DashboardStats table
            stats = DashboardStats(
                total_emails=0,
                total_claims=0,
                pending_claims=0,
                processed_claims=0,
                total_amount=0.0,
                avg_processing_time=0.0
            )
            session.add(stats)
            session.commit()
            print("✅ DashboardStats table test successful")
            
            # Clean up test data
            session.delete(stats)
            session.commit()
            
        return True
        
    except Exception as e:
        print(f"❌ Error testing table operations: {e}")
        return False

def main():
    """Main function"""
    print("🚀 DATABASE CONNECTION TEST")
    print("=" * 50)
    
    # Test connection
    if not test_database_connection():
        print("\n❌ Database connection failed. Check your DATABASE_URL configuration.")
        sys.exit(1)
    
    # Create tables
    if not create_tables():
        print("\n❌ Table creation failed.")
        sys.exit(1)
    
    # Test operations
    if not test_table_operations():
        print("\n❌ Table operations failed.")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 ALL DATABASE TESTS PASSED!")
    print("✅ Database is ready for the application")
    print("\n📋 Database configuration:")
    print(f"   - Engine: {engine.url}")
    print(f"   - Pool recycle: {getattr(engine.pool, '_recycle', 'Not set')}")

if __name__ == "__main__":
    main() 