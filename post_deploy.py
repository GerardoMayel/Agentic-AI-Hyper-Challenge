#!/usr/bin/env python3
"""
Post-Deploy Script for Render
This script runs after deployment to initialize the database and verify the setup.
"""

import os
import sys
import time
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

def post_deploy_setup():
    """Run post-deployment setup tasks."""
    
    print("🚀 Post-Deploy Setup Started")
    print("=" * 50)
    
    # Wait a moment for database to be ready
    print("⏳ Waiting for database to be ready...")
    time.sleep(10)
    
    try:
        # Import our modules
        from app.core.database import create_tables, test_connection
        from app.core.models import Claim, ClaimDocument, Coverage
        
        # Test database connection
        print("🔍 Testing database connection...")
        if test_connection():
            print("✅ Database connection successful")
            
            # Create tables
            print("📋 Creating database tables...")
            create_tables()
            print("✅ Tables created successfully")
            
            # Verify tables exist
            print("🔍 Verifying database setup...")
            from app.core.database import SessionLocal
            
            session = SessionLocal()
            try:
                # Test basic queries
                claims_count = session.query(Claim).count()
                coverages_count = session.query(Coverage).count()
                documents_count = session.query(ClaimDocument).count()
                
                print(f"✅ Database verification successful:")
                print(f"   - Claims table: {claims_count} records")
                print(f"   - Coverages table: {coverages_count} records")
                print(f"   - Documents table: {documents_count} records")
                
            finally:
                session.close()
            
            print("\n🎉 Post-deploy setup completed successfully!")
            print("✅ Database is ready for production use")
            print("✅ Application is ready to receive requests")
            
        else:
            print("❌ Database connection failed")
            return False
            
    except Exception as e:
        print(f"❌ Error during post-deploy setup: {e}")
        return False
    
    return True

if __name__ == "__main__":
    post_deploy_setup() 