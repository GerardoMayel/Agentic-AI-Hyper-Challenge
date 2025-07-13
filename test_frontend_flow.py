#!/usr/bin/env python3
"""
Test script that simulates the exact frontend flow
"""

import requests
import json
from datetime import datetime

# Production API URL
API_URL = "https://agentic-ai-hyper-challenge-backend.onrender.com"

def test_frontend_claim_submission():
    """Test the exact flow that the frontend uses"""
    
    print("🧪 Testing Frontend Claim Submission Flow")
    print("=" * 50)
    
    # Simulate the exact data structure that frontend sends
    frontend_data = {
        "coverage_type": "Trip Cancellation",
        "full_name": "Test User",
        "email": "test@example.com",
        "phone": "+1-555-123-4567",
        "policy_number": "POL-123456",
        "incident_date": datetime.now().isoformat(),
        "incident_location": "123 Test Street, Test City, TX 12345",
        "description": "Test incident description for QA testing",
        "estimated_amount": 1500.00
    }
    
    print("📤 Sending claim data to /api/claims (frontend endpoint):")
    print(f"Data: {json.dumps(frontend_data, indent=2)}")
    
    try:
        # Test the original endpoint that frontend uses
        response = requests.post(
            f"{API_URL}/api/claims",
            json=frontend_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Original endpoint works!")
            return True
        else:
            print("❌ Original endpoint failed")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_new_frontend_endpoint():
    """Test the new frontend endpoint we created"""
    
    print("\n🧪 Testing New Frontend Endpoint (/api/claims/frontend)")
    print("=" * 50)
    
    # Simulate the exact data structure that frontend sends to new endpoint
    frontend_data = {
        "claimType": "Trip Cancellation",
        "fullName": "Test User",
        "email": "test@example.com",
        "address": "123 Test Street",
        "city": "Test City",
        "state": "TX",
        "zipCode": "12345",
        "mobilePhone": "+1-555-123-4567",
        "otherPhone": "",
        "allClaimants": "Test User",
        "policyNumber": "POL-123456",
        "insuranceAgency": "Zurich Insurance",
        "initialDepositDate": "2024-01-15",
        "incidentDescription": "Test incident description for QA testing",
        "lossDate": "2024-01-10",
        "authorization": True,
        "signature": "Test User",
        "signatureDate": datetime.now().strftime("%Y-%m-%d"),
        "expenses": [
            {
                "description": "Flight cancellation",
                "date": "2024-01-10",
                "amount": 1000.00
            },
            {
                "description": "Hotel cancellation",
                "date": "2024-01-10",
                "amount": 500.00
            }
        ]
    }
    
    print("📤 Sending claim data to /api/claims/frontend:")
    print(f"Data: {json.dumps(frontend_data, indent=2)}")
    
    try:
        response = requests.post(
            f"{API_URL}/api/claims/frontend",
            json=frontend_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ New frontend endpoint works!")
            return True
        else:
            print("❌ New frontend endpoint failed")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run both tests"""
    print("🚀 Frontend Flow Testing")
    print("=" * 50)
    
    # Test 1: Original endpoint
    test1_result = test_frontend_claim_submission()
    
    # Test 2: New endpoint
    test2_result = test_new_frontend_endpoint()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"Original endpoint (/api/claims): {'✅ PASS' if test1_result else '❌ FAIL'}")
    print(f"New endpoint (/api/claims/frontend): {'✅ PASS' if test2_result else '❌ FAIL'}")
    
    if test1_result and test2_result:
        print("\n🎉 Both endpoints work!")
    elif test2_result:
        print("\n⚠️  Only new endpoint works. Frontend needs to be updated.")
    else:
        print("\n❌ Both endpoints failed. Check backend deployment.")

if __name__ == "__main__":
    main() 