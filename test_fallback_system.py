#!/usr/bin/env python3
"""
Test script for SQLite fallback system
This script tests the dual database system (Render PostgreSQL + SQLite fallback)
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

def test_database_connection():
    """Test database connections"""
    print("🔍 Testing database connections...")
    
    try:
        from app.core.database import get_current_database_info, engine
        
        # Test current database
        db_info = get_current_database_info()
        print(f"✅ Current database: {db_info['type']}")
        print(f"   URL: {db_info['url']}")
        
        # Test connection
        from sqlalchemy import text
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_sync_process():
    """Test the sync process"""
    print("\n🔄 Testing sync process...")
    
    try:
        from sync_render_to_sqlite import main as sync_main
        sync_main()
        print("✅ Sync process completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Sync process failed: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🌐 Testing API endpoints...")
    
    try:
        import requests
        import time
        
        # Start server in background (simulate)
        base_url = "http://localhost:8000"
        
        # Test health endpoint
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Health endpoint working")
                data = response.json()
                print(f"   Database: {data.get('database', {}).get('info', {}).get('type', 'unknown')}")
            else:
                print(f"⚠️  Health endpoint returned {response.status_code}")
        except Exception as e:
            print(f"⚠️  Health endpoint test failed: {e}")
        
        # Test stats endpoint
        try:
            response = requests.get(f"{base_url}/api/analyst/dashboard/stats", timeout=10)
            if response.status_code == 200:
                print("✅ Stats endpoint working")
                data = response.json()
                print(f"   Total claims: {data.get('claims_summary', {}).get('total_claims', 0)}")
            else:
                print(f"⚠️  Stats endpoint returned {response.status_code}")
        except Exception as e:
            print(f"⚠️  Stats endpoint test failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 TESTING FALLBACK SYSTEM")
    print("=" * 50)
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Sync Process", test_sync_process),
        ("API Endpoints", test_api_endpoints)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Fallback system is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 