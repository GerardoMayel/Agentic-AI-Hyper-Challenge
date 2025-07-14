#!/usr/bin/env python3
"""
Test Login Fix
"""

import requests
import json
import os
from datetime import datetime

# Configuration
BACKEND_URL = "http://localhost:8000"
DEMO_EMAIL = "analyst@zurich-demo.com"
DEMO_PASSWORD = "ZurichDemo2024!"

def test_login_fix():
    """Test the fixed login system"""
    print("🔐 Testing Fixed Login System")
    print("=" * 50)
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test 1: Check if backend is running
    print("\n1. Testing backend connectivity")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running and accessible")
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("💡 Make sure the backend is running with: cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
        return False
    
    # Test 2: Test login with correct credentials
    print("\n2. Testing login with correct credentials")
    try:
        form_data = {
            'email': DEMO_EMAIL,
            'password': DEMO_PASSWORD
        }
        response = requests.post(f"{BACKEND_URL}/api/analyst/auth/login", data=form_data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Login successful:")
            print(f"   User: {result.get('user', {}).get('email')}")
            print(f"   Role: {result.get('user', {}).get('role')}")
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error during login: {e}")
        return False
    
    # Test 3: Test login with incorrect password
    print("\n3. Testing login with incorrect password")
    try:
        form_data = {
            'email': DEMO_EMAIL,
            'password': 'wrongpassword'
        }
        response = requests.post(f"{BACKEND_URL}/api/analyst/auth/login", data=form_data, timeout=10)
        if response.status_code == 401:
            print("✅ Correctly rejected invalid password")
        else:
            print(f"❌ Should have rejected invalid password: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing invalid login: {e}")
        return False
    
    # Test 4: Test analyst dashboard access
    print("\n4. Testing analyst dashboard access")
    try:
        response = requests.get(f"{BACKEND_URL}/analyst", timeout=10)
        if response.status_code == 200:
            print("✅ Analyst dashboard is accessible")
        else:
            print(f"❌ Analyst dashboard failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error accessing analyst dashboard: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All login tests passed!")
    print("✅ Login system is working correctly")
    print("\n📋 Next steps:")
    print("1. Test the frontend login at: http://localhost:3000/login")
    print("2. Use credentials: analyst@zurich-demo.com / ZurichDemo2024!")
    print("3. Deploy to production when ready")
    
    return True

def main():
    """Main test function"""
    success = test_login_fix()
    
    if not success:
        print("\n❌ Some tests failed!")
        print("Please fix the issues before continuing")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 