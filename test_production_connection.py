#!/usr/bin/env python3
"""
Test script to verify production API connection and data loading
"""

import requests
import json
import time

def test_production_api():
    """Test the production API endpoints"""
    base_url = "https://zurich-claims-api.onrender.com"
    
    print("🔍 Testing Production API Connection")
    print("=" * 50)
    
    # Test health endpoint
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test dashboard stats
    print("\n2. Testing dashboard stats...")
    try:
        start_time = time.time()
        response = requests.get(f"{base_url}/api/analyst/dashboard/stats", timeout=15)
        end_time = time.time()
        
        print(f"   Status: {response.status_code}")
        print(f"   Response time: {end_time - start_time:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Data: {json.dumps(data, indent=2)}")
        else:
            print(f"   Error response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test claims endpoint
    print("\n3. Testing claims endpoint...")
    try:
        start_time = time.time()
        response = requests.get(f"{base_url}/api/analyst/claims", timeout=15)
        end_time = time.time()
        
        print(f"   Status: {response.status_code}")
        print(f"   Response time: {end_time - start_time:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Claims count: {len(data) if isinstance(data, list) else 'N/A'}")
            print(f"   First claim: {json.dumps(data[0] if isinstance(data, list) and len(data) > 0 else data, indent=2)}")
        else:
            print(f"   Error response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test emails endpoint
    print("\n4. Testing emails endpoint...")
    try:
        start_time = time.time()
        response = requests.get(f"{base_url}/api/analyst/emails?limit=5", timeout=15)
        end_time = time.time()
        
        print(f"   Status: {response.status_code}")
        print(f"   Response time: {end_time - start_time:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Emails count: {len(data) if isinstance(data, list) else 'N/A'}")
        else:
            print(f"   Error response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_production_api() 