"""
Database connection and table creation test script
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import text

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_database_connection():
    """Test database connection with better error handling"""
    try:
        print("🔍 Testing database connection...")
        
        # Load environment variables
        load_dotenv()
        
        # Check if DATABASE_URL exists
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            print("❌ DATABASE_URL not found in environment variables")
            return False
        
        print(f"✅ DATABASE_URL found: {database_url[:50]}...")
        
        # Try to import and test connection
        from app.core.database import engine
        
        # Test connection with SSL mode
        try:
            with engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                result.fetchone()
                print("✅ Database connection successful!")
                return True
        except Exception as e:
            print(f"❌ Direct connection failed: {str(e)}")
            
            # Try with SSL mode disabled for local development
            print("🔄 Trying with SSL mode disabled...")
            try:
                # Modify DATABASE_URL to disable SSL
                if "?" in database_url:
                    database_url_no_ssl = database_url + "&sslmode=disable"
                else:
                    database_url_no_ssl = database_url + "?sslmode=disable"
                
                from sqlalchemy import create_engine
                test_engine = create_engine(database_url_no_ssl)
                
                with test_engine.connect() as connection:
                    result = connection.execute(text("SELECT 1"))
                    result.fetchone()
                    print("✅ Database connection successful with SSL disabled!")
                    return True
                    
            except Exception as e2:
                print(f"❌ Connection with SSL disabled also failed: {str(e2)}")
                return False
        
    except Exception as e:
        print(f"❌ Error in database test: {str(e)}")
        return False

def test_table_creation():
    """Test table creation"""
    try:
        print("\n🔧 Testing table creation...")
        
        from app.core.database import engine, Base
        from app.models.claim_models import ClaimForm, Document
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully!")
        
        # List created tables
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print("📋 Available tables:")
        for table in tables:
            print(f"   - {table}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {str(e)}")
        return False

def test_basic_operations():
    """Test basic database operations"""
    try:
        print("\n🧪 Testing basic database operations...")
        
        from app.core.database import SessionLocal
        from app.models.claim_models import ClaimForm
        
        db = SessionLocal()
        
        # Test insert
        test_claim = ClaimForm(
            coverage_type="TEST_COVERAGE",
            full_name="Test User",
            email="test@example.com",
            status="PENDING"
        )
        
        db.add(test_claim)
        db.commit()
        db.refresh(test_claim)
        
        print(f"✅ Insert test successful - Claim ID: {test_claim.claim_id}")
        
        # Test select
        retrieved_claim = db.query(ClaimForm).filter(ClaimForm.claim_id == test_claim.claim_id).first()
        if retrieved_claim:
            print(f"✅ Select test successful - Found claim: {retrieved_claim.full_name}")
        else:
            print("❌ Select test failed")
        
        # Clean up
        db.delete(test_claim)
        db.commit()
        print("✅ Cleanup successful")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Error in basic operations test: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Zurich Claims Database Test Suite")
    print("=" * 50)
    
    # Test 1: Connection
    if test_database_connection():
        # Test 2: Table creation
        if test_table_creation():
            # Test 3: Basic operations
            test_basic_operations()
        else:
            print("❌ Cannot proceed without table creation")
    else:
        print("❌ Cannot proceed without database connection")
        sys.exit(1) 