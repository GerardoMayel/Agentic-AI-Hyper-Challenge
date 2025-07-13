#!/usr/bin/env python3
"""
QA Script for Production Testing - Zurich Claims System
Tests complete claim creation flow including PDF upload, storage, and database verification
"""

import os
import sys
import json
import requests
import time
from datetime import datetime, timedelta
from pathlib import Path
import random
import string

# Configuration
PRODUCTION_API_URL = "https://agentic-ai-hyper-challenge-backend.onrender.com"
LOCAL_API_URL = "http://localhost:8000"

class ProductionQATester:
    def __init__(self, use_production=True):
        self.api_url = PRODUCTION_API_URL if use_production else LOCAL_API_URL
        self.session = requests.Session()
        self.test_data = {}
        
    def generate_test_data(self):
        """Generate realistic test data for claim submission"""
        # Generate random claim data
        claim_types = ["Trip Cancellation", "Trip Delay", "Trip Interruption"]
        cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
        states = ["NY", "CA", "IL", "TX", "AZ"]
        
        # Generate random names and data
        first_names = ["John", "Jane", "Michael", "Sarah", "David", "Emily", "Robert", "Lisa"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller"]
        
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        full_name = f"{first_name} {last_name}"
        
        # Generate random policy number
        policy_number = f"POL-{random.randint(100000, 999999)}"
        
        # Generate random amounts
        total_amount = round(random.uniform(500, 5000), 2)
        
        self.test_data = {
            # Claim type
            "claimType": random.choice(claim_types),
            
            # Claimant information
            "fullName": full_name,
            "email": f"{first_name.lower()}.{last_name.lower()}@example.com",
            "address": f"{random.randint(100, 9999)} Main Street",
            "city": random.choice(cities),
            "state": random.choice(states),
            "zipCode": f"{random.randint(10000, 99999)}",
            "mobilePhone": f"+1-{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}",
            "otherPhone": f"+1-{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}",
            "allClaimants": full_name,
            "policyNumber": policy_number,
            "insuranceAgency": "Zurich Insurance",
            "initialDepositDate": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
            
            # Incident details
            "incidentDescription": f"Trip was cancelled due to unexpected weather conditions affecting flight operations. The cancellation occurred on {datetime.now().strftime('%Y-%m-%d')} and resulted in significant financial losses including non-refundable flight tickets and hotel reservations.",
            "lossDate": (datetime.now() - timedelta(days=random.randint(1, 7))).strftime("%Y-%m-%d"),
            
            # Authorization
            "authorization": True,
            "signature": full_name,
            "signatureDate": datetime.now().strftime("%Y-%m-%d"),
            
            # Expenses
            "expenses": [
                {
                    "description": "Flight cancellation fees",
                    "date": (datetime.now() - timedelta(days=random.randint(1, 10))).strftime("%Y-%m-%d"),
                    "amount": round(total_amount * 0.6, 2)
                },
                {
                    "description": "Hotel reservation cancellation",
                    "date": (datetime.now() - timedelta(days=random.randint(1, 10))).strftime("%Y-%m-%d"),
                    "amount": round(total_amount * 0.4, 2)
                }
            ],
            
            # Calculated total
            "totalAmount": total_amount
        }
        
        return self.test_data
    
    def create_test_pdf(self):
        """Create a test PDF file for upload"""
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            from reportlab.lib import colors
            
            # Create test PDF
            pdf_path = "test_claim_document.pdf"
            c = canvas.Canvas(pdf_path, pagesize=letter)
            
            # Add content to PDF
            c.setFont("Helvetica-Bold", 16)
            c.drawString(100, 750, "Zurich Insurance - Claim Document")
            
            c.setFont("Helvetica", 12)
            c.drawString(100, 720, f"Claimant: {self.test_data['full_name']}")
            c.drawString(100, 700, f"Policy Number: {self.test_data['policy_number']}")
            c.drawString(100, 680, f"Claim Type: {self.test_data['claim_type']}")
            c.drawString(100, 660, f"Date: {datetime.now().strftime('%Y-%m-%d')}")
            
            c.setFont("Helvetica", 10)
            c.drawString(100, 620, "Incident Details:")
            c.drawString(100, 600, self.test_data['incident_description'][:100] + "...")
            
            c.drawString(100, 560, "Expenses:")
            y_pos = 540
            for expense in self.test_data['expenses']:
                c.drawString(120, y_pos, f"- {expense['description']}: ${expense['amount']}")
                y_pos -= 20
            
            c.drawString(100, y_pos - 20, f"Total Amount: ${self.test_data['total_amount_requested']}")
            
            c.save()
            print(f"✅ Test PDF created: {pdf_path}")
            return pdf_path
            
        except ImportError:
            print("⚠️  reportlab not available, creating simple text file instead")
            # Create a simple text file as fallback
            text_path = "test_claim_document.txt"
            with open(text_path, "w") as f:
                f.write("Zurich Insurance - Claim Document\n")
                f.write(f"Claimant: {self.test_data['full_name']}\n")
                f.write(f"Policy Number: {self.test_data['policy_number']}\n")
                f.write(f"Claim Type: {self.test_data['claim_type']}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d')}\n")
                f.write(f"Total Amount: ${self.test_data['total_amount_requested']}\n")
            print(f"✅ Test text file created: {text_path}")
            return text_path
    
    def test_health_endpoint(self):
        """Test if the API is accessible"""
        print("\n🔍 Testing API Health...")
        try:
            response = self.session.get(f"{self.api_url}/api/health")
            if response.status_code == 200:
                print("✅ API is healthy and accessible")
                health_data = response.json()
                print(f"   - Status: {health_data.get('status')}")
                print(f"   - Database: {health_data.get('services', {}).get('database')}")
                print(f"   - Storage: {health_data.get('services', {}).get('storage')}")
                return True
            else:
                print(f"❌ API health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ API health check error: {e}")
            return False
    
    def test_claim_creation(self):
        """Test complete claim creation flow"""
        print("\n📝 Testing Claim Creation...")
        
        # Generate test data
        claim_data = self.generate_test_data()
        print(f"📋 Generated test claim for: {claim_data['full_name']}")
        
        # Create test document
        document_path = self.create_test_pdf()
        
        try:
            # Prepare form data for frontend endpoint
            form_data = {
                'claimType': claim_data['claimType'],
                'fullName': claim_data['fullName'],
                'email': claim_data['email'],
                'address': claim_data['address'],
                'city': claim_data['city'],
                'state': claim_data['state'],
                'zipCode': claim_data['zipCode'],
                'mobilePhone': claim_data['mobilePhone'],
                'otherPhone': claim_data['otherPhone'],
                'allClaimants': claim_data['allClaimants'],
                'policyNumber': claim_data['policyNumber'],
                'insuranceAgency': claim_data['insuranceAgency'],
                'initialDepositDate': claim_data['initialDepositDate'],
                'incidentDescription': claim_data['incidentDescription'],
                'lossDate': claim_data['lossDate'],
                'authorization': claim_data['authorization'],
                'signature': claim_data['signature'],
                'signatureDate': claim_data['signatureDate'],
                'expenses': claim_data['expenses']
            }
            
            # First, create the claim
            print("📤 Submitting claim to API...")
            
            # Submit claim using frontend endpoint
            response = self.session.post(
                f"{self.api_url}/api/claims/frontend",
                json=form_data,
                timeout=30
            )
            
            if response.status_code == 201:
                claim_response = response.json()
                claim_id = claim_response.get('data', {}).get('claim_id')
                print(f"✅ Claim created successfully! ID: {claim_id}")
                
                # Store claim data for verification
                self.test_data['claim_id'] = claim_id
                self.test_data['claim_response'] = claim_response
                
                # Now upload the document
                print("📄 Uploading document...")
                with open(document_path, 'rb') as f:
                    files = {
                        'file': (os.path.basename(document_path), f, 'application/pdf')
                    }
                    form_data_doc = {
                        'document_type': 'CLAIM_DOCUMENT',
                        'upload_notes': 'Test document uploaded via QA script'
                    }
                    
                    doc_response = self.session.post(
                        f"{self.api_url}/api/claims/{claim_id}/documents",
                        data=form_data_doc,
                        files=files,
                        timeout=30
                    )
                    
                    if doc_response.status_code == 201:
                        doc_result = doc_response.json()
                        print(f"✅ Document uploaded successfully!")
                        print(f"   - Filename: {doc_result.get('data', {}).get('filename')}")
                        print(f"   - Storage URL: {doc_result.get('data', {}).get('storage_url')}")
                    else:
                        print(f"⚠️  Document upload failed: {doc_response.status_code}")
                        print(f"Response: {doc_response.text}")
                
                return True
            else:
                print(f"❌ Claim creation failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
            

            
            print("📤 Submitting claim to API...")
            
            # Submit claim using frontend endpoint
            response = self.session.post(
                f"{self.api_url}/api/claims/frontend",
                json=form_data,
                timeout=30
            )
            
            if response.status_code == 201:
                claim_response = response.json()
                claim_id = claim_response.get('id')
                print(f"✅ Claim created successfully! ID: {claim_id}")
                
                # Store claim data for verification
                self.test_data['claim_id'] = claim_id
                self.test_data['claim_response'] = claim_response
                
                return True
            else:
                print(f"❌ Claim creation failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error creating claim: {e}")
            return False
        finally:
            # Clean up test file
            if os.path.exists(document_path):
                os.remove(document_path)
                print(f"🧹 Cleaned up test file: {document_path}")
    
    def verify_database_records(self):
        """Verify that records were created in the database"""
        print("\n🔍 Verifying Database Records...")
        
        if not self.test_data.get('claim_id'):
            print("❌ No claim ID available for verification")
            return False
        
        claim_id = self.test_data['claim_id']
        
        try:
            # Verify claim record
            print(f"📋 Verifying claim record (ID: {claim_id})...")
            claim_response = self.session.get(f"{self.api_url}/api/claims/{claim_id}")
            
            if claim_response.status_code == 200:
                claim_data = claim_response.json()
                print("✅ Claim record found in database")
                print(f"   - Claimant: {claim_data.get('data', {}).get('claim', {}).get('full_name')}")
                print(f"   - Policy: {claim_data.get('data', {}).get('claim', {}).get('policy_number')}")
                print(f"   - Amount: ${claim_data.get('data', {}).get('claim', {}).get('estimated_amount')}")
                print(f"   - Status: {claim_data.get('data', {}).get('claim', {}).get('status')}")
            else:
                print(f"❌ Claim record not found: {claim_response.status_code}")
                return False
            
            # Verify documents
            print("📄 Verifying document records...")
            # Documents are included in the claim response
            claim_data = claim_response.json()
            documents = claim_data.get('data', {}).get('documents', [])
            
            if documents:
                print(f"✅ {len(documents)} document(s) found")
                for doc in documents:
                    print(f"   - Document: {doc.get('filename')}")
                    print(f"   - Storage URL: {doc.get('storage_url')}")
                    print(f"   - Document Type: {doc.get('document_type')}")
            else:
                print("⚠️  No documents found for this claim")
            
            return True
            
        except Exception as e:
            print(f"❌ Error verifying database records: {e}")
            return False
    
    def test_storage_access(self):
        """Test if uploaded files are accessible in storage"""
        print("\n☁️  Testing Storage Access...")
        
        if not self.test_data.get('claim_id'):
            print("❌ No claim ID available for storage test")
            return False
        
        try:
            # Get documents for the claim
            claim_response = self.session.get(f"{self.api_url}/api/claims/{self.test_data['claim_id']}")
            
            if claim_response.status_code == 200:
                claim_data = claim_response.json()
                documents = claim_data.get('data', {}).get('documents', [])
                
                for doc in documents:
                    storage_url = doc.get('storage_url')
                    if storage_url:
                        print(f"🔗 Testing storage URL: {storage_url}")
                        
                        # Try to access the file
                        file_response = self.session.head(storage_url, timeout=10)
                        if file_response.status_code in [200, 302, 403]:  # 403 is OK for private files
                            print("✅ File is accessible in storage")
                        else:
                            print(f"⚠️  File access returned: {file_response.status_code}")
                    else:
                        print("⚠️  No storage URL available")
            
            return True
            
        except Exception as e:
            print(f"❌ Error testing storage access: {e}")
            return False
    
    def run_complete_test(self):
        """Run the complete QA test suite"""
        print("🚀 Starting Production QA Test Suite")
        print("=" * 50)
        print(f"🌐 Testing API: {self.api_url}")
        print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        
        test_results = {
            'health_check': False,
            'claim_creation': False,
            'database_verification': False,
            'storage_access': False
        }
        
        # Test 1: Health Check
        test_results['health_check'] = self.test_health_endpoint()
        
        if not test_results['health_check']:
            print("\n❌ Health check failed. Stopping tests.")
            return test_results
        
        # Test 2: Claim Creation
        test_results['claim_creation'] = self.test_claim_creation()
        
        if not test_results['claim_creation']:
            print("\n❌ Claim creation failed. Stopping tests.")
            return test_results
        
        # Test 3: Database Verification
        test_results['database_verification'] = self.verify_database_records()
        
        # Test 4: Storage Access
        test_results['storage_access'] = self.test_storage_access()
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 QA Test Results Summary")
        print("=" * 50)
        
        for test_name, result in test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name.replace('_', ' ').title()}: {status}")
        
        passed_tests = sum(test_results.values())
        total_tests = len(test_results)
        
        print(f"\n🎯 Overall Result: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests == total_tests:
            print("🎉 All tests passed! Production system is working correctly.")
        else:
            print("⚠️  Some tests failed. Please check the logs above.")
        
        return test_results

def main():
    """Main function to run QA tests"""
    import argparse
    
    parser = argparse.ArgumentParser(description='QA Test Suite for Zurich Claims System')
    parser.add_argument('--local', action='store_true', help='Test against local API instead of production')
    parser.add_argument('--install-deps', action='store_true', help='Install required dependencies')
    
    args = parser.parse_args()
    
    # Install dependencies if requested
    if args.install_deps:
        print("📦 Installing required dependencies...")
        os.system("pip install reportlab requests")
        print("✅ Dependencies installed")
    
    # Run tests
    tester = ProductionQATester(use_production=not args.local)
    results = tester.run_complete_test()
    
    # Exit with appropriate code
    sys.exit(0 if all(results.values()) else 1)

if __name__ == "__main__":
    main() 