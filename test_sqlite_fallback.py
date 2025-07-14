#!/usr/bin/env python3
"""
Test SQLite Fallback System
"""

import requests
import json
import time
from datetime import datetime

def test_health_endpoint():
    """Test the health endpoint to see database info"""
    print("🔍 Testing health endpoint...")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Health endpoint working")
            print(f"Database type: {data.get('database', {}).get('info', {}).get('type', 'unknown')}")
            print(f"Database fallback: {data.get('database', {}).get('info', {}).get('fallback', False)}")
            return data
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error testing health endpoint: {e}")
        return None

def test_dashboard_stats():
    """Test dashboard stats endpoint"""
    print("\n🔍 Testing dashboard stats...")
    
    try:
        response = requests.get("http://localhost:8000/api/analyst/dashboard/stats", timeout=15)
        if response.status_code == 200:
            data = response.json()
            print("✅ Dashboard stats working")
            print(f"Total claims: {data.get('claims_summary', {}).get('total_claims', 0)}")
            print(f"Total emails: {data.get('processing_summary', {}).get('total_emails', 0)}")
            return data
        else:
            print(f"❌ Dashboard stats failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error testing dashboard stats: {e}")
        return None

def test_claims_endpoint():
    """Test claims endpoint"""
    print("\n🔍 Testing claims endpoint...")
    
    try:
        response = requests.get("http://localhost:8000/api/analyst/claims", timeout=15)
        if response.status_code == 200:
            data = response.json()
            print("✅ Claims endpoint working")
            print(f"Total claims returned: {len(data.get('claims', []))}")
            return data
        else:
            print(f"❌ Claims endpoint failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error testing claims endpoint: {e}")
        return None

def main():
    """Main test function"""
    print("🧪 TESTING SQLITE FALLBACK SYSTEM")
    print("=" * 50)
    print(f"Test time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(5)
    
    # Test endpoints
    health_data = test_health_endpoint()
    stats_data = test_dashboard_stats()
    claims_data = test_claims_endpoint()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS")
    
    if health_data:
        db_info = health_data.get('database', {}).get('info', {})
        print(f"✅ Database: {db_info.get('type', 'unknown')}")
        print(f"✅ Fallback mode: {db_info.get('fallback', False)}")
    else:
        print("❌ Health check failed")
    
    if stats_data:
        print(f"✅ Stats endpoint: Working")
        print(f"   - Claims: {stats_data.get('claims_summary', {}).get('total_claims', 0)}")
        print(f"   - Emails: {stats_data.get('processing_summary', {}).get('total_emails', 0)}")
    else:
        print("❌ Stats endpoint: Failed")
    
    if claims_data:
        print(f"✅ Claims endpoint: Working")
        print(f"   - Claims returned: {len(claims_data.get('claims', []))}")
    else:
        print("❌ Claims endpoint: Failed")
    
    print("\n🎯 System is ready for testing!")

if __name__ == "__main__":
    main() 