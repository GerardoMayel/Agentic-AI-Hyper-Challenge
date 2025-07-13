#!/usr/bin/env python3
"""
Test Authentication System
"""

import requests
import json
import os
from datetime import datetime

# Configuration
BACKEND_URL = "http://localhost:8000"
DEMO_EMAIL = "analyst@zurich-demo.com"
DEMO_PASSWORD = "ZurichDemo2024!"

def test_auth_endpoints():
    """Test authentication endpoints"""
    print("🔐 Testing Authentication System")
    print("=" * 50)
    
    # Test 1: Get demo credentials
    print("\n1. Testing GET /api/analyst/auth/credentials")
    try:
        response = requests.get(f"{BACKEND_URL}/api/analyst/auth/credentials")
        if response.status_code == 200:
            credentials = response.json()
            print(f"✅ Demo credentials retrieved:")
            print(f"   Email: {credentials.get('demo_email')}")
            print(f"   Password: {credentials.get('demo_password')}")
        else:
            print(f"❌ Failed to get credentials: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error getting credentials: {e}")
        return False
    
    # Test 2: Test login with correct credentials
    print("\n2. Testing POST /api/analyst/auth/login with correct credentials")
    try:
        form_data = {
            'email': DEMO_EMAIL,
            'password': DEMO_PASSWORD
        }
        response = requests.post(f"{BACKEND_URL}/api/analyst/auth/login", data=form_data)
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
    
    # Test 3: Test login with incorrect credentials
    print("\n3. Testing POST /api/analyst/auth/login with incorrect credentials")
    try:
        form_data = {
            'email': DEMO_EMAIL,
            'password': 'wrongpassword'
        }
        response = requests.post(f"{BACKEND_URL}/api/analyst/auth/login", data=form_data)
        if response.status_code == 401:
            print("✅ Correctly rejected invalid credentials")
        else:
            print(f"❌ Should have rejected invalid credentials: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing invalid login: {e}")
        return False
    
    # Test 4: Test login with non-existent email
    print("\n4. Testing POST /api/analyst/auth/login with non-existent email")
    try:
        form_data = {
            'email': 'nonexistent@example.com',
            'password': DEMO_PASSWORD
        }
        response = requests.post(f"{BACKEND_URL}/api/analyst/auth/login", data=form_data)
        if response.status_code == 401:
            print("✅ Correctly rejected non-existent email")
        else:
            print(f"❌ Should have rejected non-existent email: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing non-existent email: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All authentication tests passed!")
    return True

def test_frontend_integration():
    """Test frontend integration with backend"""
    print("\n🌐 Testing Frontend Integration")
    print("=" * 50)
    
    # Test if frontend can reach backend
    print("\n1. Testing frontend-backend connectivity")
    try:
        response = requests.get(f"{BACKEND_URL}/health")
        if response.status_code == 200:
            print("✅ Backend is reachable from frontend")
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot reach backend: {e}")
        return False
    
    # Test analyst dashboard endpoint
    print("\n2. Testing analyst dashboard endpoint")
    try:
        response = requests.get(f"{BACKEND_URL}/analyst")
        if response.status_code == 200:
            print("✅ Analyst dashboard is accessible")
        else:
            print(f"❌ Analyst dashboard failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error accessing analyst dashboard: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Frontend integration tests passed!")
    return True

def main():
    """Main test function"""
    print("🚀 AUTHENTICATION SYSTEM TEST")
    print("=" * 50)
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run tests
    auth_success = test_auth_endpoints()
    frontend_success = test_frontend_integration()
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    print(f"Authentication Tests: {'✅ PASSED' if auth_success else '❌ FAILED'}")
    print(f"Frontend Integration: {'✅ PASSED' if frontend_success else '❌ FAILED'}")
    
    if auth_success and frontend_success:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Authentication system is ready for deployment")
        print("\n📋 Next steps:")
        print("1. Execute the SQL script to create auth_credentials table")
        print("2. Deploy to Render")
        print("3. Configure environment variables in Render")
    else:
        print("\n❌ SOME TESTS FAILED!")
        print("Please fix the issues before deployment")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 