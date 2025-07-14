#!/usr/bin/env python3
"""
Test Login Simulado
"""

import requests
import json
from datetime import datetime

# Configuration
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

def test_login_simulado():
    """Test the simulated login system"""
    print("🔓 Testing Simulated Login System")
    print("=" * 50)
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Frontend URL: {FRONTEND_URL}")
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
    
    # Test 2: Test login with any credentials
    print("\n2. Testing login with any credentials")
    test_credentials = [
        {"email": "test@example.com", "password": "anypassword"},
        {"email": "demo@zurich.com", "password": "demo123"},
        {"email": "admin@test.com", "password": "admin123"},
        {"email": "", "password": ""}
    ]
    
    for i, creds in enumerate(test_credentials, 1):
        try:
            print(f"   Testing credentials {i}: {creds['email']} / {creds['password']}")
            response = requests.post(f"{BACKEND_URL}/api/analyst/auth/login", data=creds, timeout=10)
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Login successful:")
                print(f"      User: {result.get('user', {}).get('email')}")
                print(f"      Role: {result.get('user', {}).get('role')}")
                print(f"      Message: {result.get('message')}")
            else:
                print(f"   ❌ Login failed: {response.status_code}")
                print(f"      Response: {response.text}")
                return False
        except Exception as e:
            print(f"   ❌ Error during login: {e}")
            return False
    
    # Test 3: Test analyst dashboard access
    print("\n3. Testing analyst dashboard access")
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
    
    # Test 4: Test dashboard stats API
    print("\n4. Testing dashboard stats API")
    try:
        response = requests.get(f"{BACKEND_URL}/api/analyst/dashboard/stats", timeout=10)
        if response.status_code == 200:
            stats = response.json()
            print("✅ Dashboard stats API is working")
            print(f"   Total claims: {stats.get('claims_summary', {}).get('total_claims', 0)}")
            print(f"   Total emails: {stats.get('processing_summary', {}).get('total_emails', 0)}")
        else:
            print(f"❌ Dashboard stats API failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error accessing dashboard stats: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All simulated login tests passed!")
    print("✅ Login system is working correctly in development mode")
    print("\n📋 Next steps:")
    print("1. Test the frontend login at: http://localhost:3000/login")
    print("2. Enter any email and password to access the system")
    print("3. Navigate to the dashboard and analyst interface")
    print("4. The system will accept any credentials for testing")
    
    return True

if __name__ == "__main__":
    test_login_simulado() 