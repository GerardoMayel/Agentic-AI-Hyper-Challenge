"""
Test script with correct database URL
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import text, create_engine

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_correct_connection():
    """Test connection with the correct database URL"""
    print("🔍 Testing connection with correct DATABASE_URL...")
    
    # Use the correct URL you provided
    correct_url = "postgresql://agent:QRp3aBO6eGFT2mXY6p1nTmAxd41QRFJc@dpg-d1k9hmer433s73c9g7mg-a.oregon-postgres.render.com/claims_ropj_z7d1"
    
    try:
        # Create engine
        engine = create_engine(correct_url)
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            result.fetchone()
            print("✅ Connection successful with correct URL!")
            
            # Test database name
            result = connection.execute(text("SELECT current_database()"))
            db_row = result.fetchone()
            if db_row:
                db_name = db_row[0]
                print(f"✅ Connected to database: {db_name}")
            else:
                print("✅ Connected to database (name not available)")
            
            # List tables
            result = connection.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            tables = [row[0] for row in result.fetchall()]
            
            if tables:
                print(f"✅ Found {len(tables)} table(s):")
                for table in tables:
                    print(f"   - {table}")
            else:
                print("📭 No tables found in database")
            
            return True
            
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Correct Database URL")
    print("=" * 50)
    
    if test_correct_connection():
        print("\n✅ Database connection test successful!")
        print("🎯 Ready to proceed with backend deployment")
    else:
        print("\n❌ Database connection test failed")
        sys.exit(1) 