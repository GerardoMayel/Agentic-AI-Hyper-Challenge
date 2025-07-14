#!/usr/bin/env python3
"""
Test Render Production Environment
"""

import requests
import time
import json
import hashlib
from datetime import datetime

# Production URLs
BACKEND_URL = "https://zurich-claims-api.onrender.com"
FRONTEND_URL = "https://zurich-claims-frontend.onrender.com"

def test_health_endpoint():
    """Test if backend is responding"""
    print("🔍 Testing backend health...")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Backend is responding")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend health check error: {e}")
        return False

def test_database_connection():
    """Test database connection through API"""
    print("\n🔍 Testing database connection...")
    try:
        # Test dashboard stats endpoint (requires DB)
        response = requests.get(f"{BACKEND_URL}/api/analyst/dashboard/stats", timeout=15)
        if response.status_code == 200:
            print("✅ Database connection successful")
            data = response.json()
            print(f"📊 Dashboard stats: {data}")
            return True
        else:
            print(f"❌ Database connection failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def test_login_with_retries(max_retries=5, delay=3):
    """Test login with multiple retries"""
    print(f"\n🔍 Testing login with {max_retries} retries...")
    
    login_data = {
        "email": "analyst@zurich-demo.com",
        "password": "demo123"
    }
    
    for attempt in range(max_retries):
        print(f"📋 Attempt {attempt + 1}/{max_retries}")
        try:
            response = requests.post(
                f"{BACKEND_URL}/api/analyst/auth/login",
                data=login_data,
                timeout=15
            )
            
            print(f"📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Login successful!")
                data = response.json()
                print(f"📋 Response: {data}")
                return True
            elif response.status_code == 401:
                print("❌ Invalid credentials")
                return False
            elif response.status_code == 500:
                print("❌ Server error - database might be unavailable")
                if attempt < max_retries - 1:
                    print(f"⏳ Waiting {delay} seconds before retry...")
                    time.sleep(delay)
                    continue
                else:
                    print("❌ Max retries reached")
                    return False
            else:
                print(f"❌ Unexpected status: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except requests.exceptions.Timeout:
            print("⏰ Request timeout")
            if attempt < max_retries - 1:
                print(f"⏳ Waiting {delay} seconds before retry...")
                time.sleep(delay)
                continue
            else:
                print("❌ Max retries reached")
                return False
        except Exception as e:
            print(f"❌ Request error: {e}")
            if attempt < max_retries - 1:
                print(f"⏳ Waiting {delay} seconds before retry...")
                time.sleep(delay)
                continue
            else:
                print("❌ Max retries reached")
                return False
    
    return False

def test_claims_endpoint():
    """Test claims endpoint"""
    print("\n🔍 Testing claims endpoint...")
    try:
        response = requests.get(f"{BACKEND_URL}/api/analyst/claims", timeout=15)
        if response.status_code == 200:
            print("✅ Claims endpoint working")
            data = response.json()
            print(f"📊 Claims count: {len(data)}")
            return True
        else:
            print(f"❌ Claims endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Claims endpoint error: {e}")
        return False

def check_auth_credentials():
    """Check if auth credentials exist in database"""
    print("\n🔍 Checking auth credentials in database...")
    try:
        # This would require a direct database connection
        # For now, we'll test through the login endpoint
        login_data = {
            "email": "analyst@zurich-demo.com",
            "password": "demo123"
        }
        
        response = requests.post(
            f"{BACKEND_URL}/api/analyst/auth/login",
            data=login_data,
            timeout=10
        )
        
        if response.status_code == 401:
            print("❌ User not found - credentials might not exist")
            return False
        elif response.status_code == 200:
            print("✅ User exists in database")
            return True
        else:
            print(f"⚠️  Could not determine user status: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error checking credentials: {e}")
        return None

def main():
    """Main test function"""
    print("🚀 RENDER PRODUCTION TEST")
    print("=" * 50)
    print(f"⏰ Test time: {datetime.now()}")
    print(f"🌐 Backend URL: {BACKEND_URL}")
    print(f"🌐 Frontend URL: {FRONTEND_URL}")
    print("=" * 50)
    
    # Test sequence
    tests = [
        ("Backend Health", test_health_endpoint),
        ("Database Connection", test_database_connection),
        ("Claims Endpoint", test_claims_endpoint),
        ("Auth Credentials", check_auth_credentials),
        ("Login with Retries", test_login_with_retries)
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS")
    print("=" * 50)
    
    if not results.get("Backend Health", False):
        print("❌ Backend is not responding - check Render dashboard")
    elif not results.get("Database Connection", False):
        print("❌ Database connection failed - database might be restarting")
        print("💡 Wait 2-3 minutes and try again")
    elif not results.get("Auth Credentials", False):
        print("❌ Auth credentials not found - need to recreate user")
        print("💡 Run database initialization script")
    elif not results.get("Login with Retries", False):
        print("❌ Login failing despite database working")
        print("💡 Check login endpoint implementation")
    else:
        print("✅ All tests passed! System is working correctly")

if __name__ == "__main__":
    main() 