"""
Database Diagnosis Script
Tests connection and shows current schema before backend deployment
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import text, inspect

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def load_environment():
    """Load and validate environment variables"""
    print("🔧 Loading environment variables...")
    load_dotenv()
    
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
        return None
    
    print(f"✅ DATABASE_URL found: {database_url[:50]}...")
    return database_url

def test_database_connection(database_url):
    """Test database connection with multiple SSL modes"""
    print("\n🔍 Testing database connection...")
    
    # Try different SSL configurations
    ssl_configs = [
        ("Default SSL", database_url),
        ("SSL Disabled", database_url + "?sslmode=disable" if "?" not in database_url else database_url + "&sslmode=disable"),
        ("SSL Required", database_url + "?sslmode=require" if "?" not in database_url else database_url + "&sslmode=require"),
        ("SSL Prefer", database_url + "?sslmode=prefer" if "?" not in database_url else database_url + "&sslmode=prefer")
    ]
    
    working_config = None
    
    for config_name, config_url in ssl_configs:
        try:
            print(f"  🔄 Trying {config_name}...")
            from sqlalchemy import create_engine
            test_engine = create_engine(config_url)
            
            with test_engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                result.fetchone()
                print(f"  ✅ {config_name} - Connection successful!")
                working_config = config_url
                break
                
        except Exception as e:
            print(f"  ❌ {config_name} - Failed: {str(e)[:100]}...")
    
    if working_config:
        print(f"\n✅ Database connection successful with: {working_config[:50]}...")
        return working_config
    else:
        print("\n❌ All connection attempts failed")
        return None

def show_current_schema(database_url):
    """Show current database schema and tables"""
    print("\n📋 Analyzing current database schema...")
    
    try:
        from sqlalchemy import create_engine
        engine = create_engine(database_url)
        
        # Get inspector
        inspector = inspect(engine)
        
        # Get all tables
        tables = inspector.get_table_names()
        
        if not tables:
            print("  📭 No tables found in database")
            return True
        
        print(f"  📊 Found {len(tables)} table(s):")
        
        for table_name in tables:
            print(f"\n  📋 Table: {table_name}")
            
            # Get columns
            columns = inspector.get_columns(table_name)
            print(f"    Columns ({len(columns)}):")
            for column in columns:
                nullable = "NULL" if column['nullable'] else "NOT NULL"
                default = f" DEFAULT {column['default']}" if column.get('default') else ""
                print(f"      - {column['name']}: {column['type']} {nullable}{default}")
            
            # Get indexes
            indexes = inspector.get_indexes(table_name)
            if indexes:
                print(f"    Indexes ({len(indexes)}):")
                for index in indexes:
                    unique = "UNIQUE" if index['unique'] else ""
                    column_names = [name for name in index['column_names'] if name is not None]
                    print(f"      - {index['name']}: {', '.join(column_names)} {unique}")
            
            # Get foreign keys
            foreign_keys = inspector.get_foreign_keys(table_name)
            if foreign_keys:
                print(f"    Foreign Keys ({len(foreign_keys)}):")
                for fk in foreign_keys:
                    print(f"      - {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error analyzing schema: {str(e)}")
        return False

def test_table_creation(database_url):
    """Test if we can create our required tables"""
    print("\n🔧 Testing table creation...")
    
    try:
        from app.core.database import Base
        from app.models.claim_models import ClaimForm, Document
        from sqlalchemy import create_engine
        
        # Create engine with working URL
        engine = create_engine(database_url)
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        print("  ✅ Tables created successfully!")
        
        # Verify tables were created
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print(f"  📋 Current tables in database: {tables}")
        
        if tables:
            print("  ✅ Database has existing tables")
            return True
        else:
            print("  📭 Database is empty (no tables)")
            return True
            
    except Exception as e:
        print(f"  ❌ Error creating tables: {str(e)}")
        return False

def test_basic_operations(database_url):
    """Test basic database operations"""
    print("\n🧪 Testing basic database operations...")
    
    try:
        from sqlalchemy import create_engine
        from app.core.database import SessionLocal
        from app.models.claim_models import ClaimForm
        
        # Create engine
        engine = create_engine(database_url)
        SessionLocal.configure(bind=engine)
        
        db = SessionLocal()
        
        # Test insert
        test_claim = ClaimForm(
            coverage_type="DIAGNOSTIC_TEST",
            full_name="Diagnostic Test User",
            email="diagnostic@test.com",
            status="PENDING"
        )
        
        db.add(test_claim)
        db.commit()
        db.refresh(test_claim)
        
        print(f"  ✅ Insert test successful - Claim ID: {test_claim.claim_id}")
        
        # Test select
        retrieved_claim = db.query(ClaimForm).filter(ClaimForm.claim_id == test_claim.claim_id).first()
        if retrieved_claim:
            print(f"  ✅ Select test successful - Found claim: {retrieved_claim.full_name}")
        else:
            print("  ❌ Select test failed")
        
        # Test update
        if retrieved_claim:
            retrieved_claim.status = "TESTED"
            db.commit()
            print("  ✅ Update test successful")
        else:
            print("  ❌ Update test failed - no claim to update")
        
        # Clean up
        db.delete(retrieved_claim)
        db.commit()
        print("  ✅ Cleanup successful")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"  ❌ Error in basic operations test: {str(e)}")
        return False

def main():
    """Main diagnosis function"""
    print("🚀 Zurich Claims Database Diagnosis")
    print("=" * 60)
    
    # Step 1: Load environment
    database_url = load_environment()
    if not database_url:
        print("\n❌ Cannot proceed without DATABASE_URL")
        sys.exit(1)
    
    # Step 2: Test connection
    working_url = test_database_connection(database_url)
    if not working_url:
        print("\n❌ Cannot proceed without database connection")
        sys.exit(1)
    
    # Step 3: Show current schema
    if not show_current_schema(working_url):
        print("\n❌ Cannot analyze current schema")
        sys.exit(1)
    
    # Step 4: Test table creation
    if not test_table_creation(working_url):
        print("\n❌ Cannot create required tables")
        sys.exit(1)
    
    # Step 5: Test basic operations
    if not test_basic_operations(working_url):
        print("\n❌ Basic operations failed")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ Database diagnosis completed successfully!")
    print("🎯 Ready to deploy backend")
    print("=" * 60)

if __name__ == "__main__":
    main() 