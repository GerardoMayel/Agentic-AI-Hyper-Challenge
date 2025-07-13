#!/usr/bin/env python3
"""
Script para probar el procesamiento de emails con datos simulados
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Agregar el directorio actual al path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from app.core.database import SessionLocal
from app.models.email_models import Email, ClaimSubmission, DocumentAgentOCR
from app.services.email_processor import EmailProcessor
from app.services.llm_service import LLMService

def test_email_processing():
    """Test email processing with simulated data"""
    print("🧪 EMAIL PROCESSING TEST")
    print("=" * 50)
    
    db = SessionLocal()
    processor = EmailProcessor(db)
    llm_service = LLMService()
    
    # Test data
    test_emails = [
        {
            "gmail_id": "test_claim_001",
            "thread_id": "thread_claim_001",
            "from_email": "customer1@example.com",
            "to_email": "claims@zurich.com",
            "subject": "Travel Insurance Claim - Flight Cancellation",
            "body_text": "Hello, I had a problem with my flight and need to file a claim. My name is John Smith and my policy number is POL-2024-001. The incident occurred on January 15, 2024. I'm attaching the necessary documents.",
            "is_first_notification": True
        },
        {
            "gmail_id": "test_claim_002",
            "thread_id": "thread_claim_002",
            "from_email": "customer2@example.com",
            "to_email": "claims@zurich.com",
            "subject": "Hotel Claim - Room Problems",
            "body_text": "Good morning, I had problems with my hotel room and want to file a claim. I'm Mary Johnson, policy POL-2024-002. The problem occurred on January 20, 2024. The room had cleanliness issues and excessive noise.",
            "is_first_notification": True
        },
        {
            "gmail_id": "test_followup_001",
            "thread_id": "thread_claim_001",
            "from_email": "customer1@example.com",
            "to_email": "claims@zurich.com",
            "subject": "Re: Travel Insurance Claim - Additional Documents",
            "body_text": "Here are the additional documents you requested for my claim.",
            "is_first_notification": False
        }
    ]
    
    try:
        print("📧 Processing test emails...")
        
        for i, email_data in enumerate(test_emails, 1):
            print(f"\n📋 Processing email {i}: {email_data['subject']}")
            
            # Create email record
            email_record = Email(
                gmail_id=email_data['gmail_id'],
                thread_id=email_data['thread_id'],
                from_email=email_data['from_email'],
                to_email=email_data['to_email'],
                subject=email_data['subject'],
                body_text=email_data['body_text'],
                body_html=email_data['body_text'],
                received_at=datetime.now(),
                is_first_notification=email_data['is_first_notification']
            )
            
            db.add(email_record)
            db.commit()
            db.refresh(email_record)
            
            print(f"✅ Email saved with ID: {email_record.id}")
            
            # Process the email
            if email_data['is_first_notification']:
                print("🆕 Processing as first notification...")
                
                # Analyze with LLM
                analysis_result = llm_service.analyze_email_content({
                    "subject": email_data['subject'],
                    "body": email_data['body_text']
                })
                
                print(f"🤖 LLM Analysis: {analysis_result.get('claim_type', 'N/A')}")
                
                # Create claim submission
                claim_submission = ClaimSubmission(
                    claim_number=f"CLM-TEST{i:03d}",
                    email_id=email_record.id,
                    customer_name=analysis_result.get('customer_name') or 'Test Customer',
                    customer_email=email_data['from_email'],
                    policy_number=analysis_result.get('policy_number'),
                    claim_type=analysis_result.get('claim_type', 'OTHER'),
                    incident_description=email_data['body_text'][:500],
                    estimated_amount=analysis_result.get('estimated_amount'),
                    status='PENDING',
                    priority=analysis_result.get('priority', 'NORMAL'),
                    llm_summary=analysis_result.get('summary'),
                    llm_recommendation=analysis_result.get('llm_recommendation')
                )
                
                db.add(claim_submission)
                db.commit()
                db.refresh(claim_submission)
                
                print(f"✅ Claim created: {claim_submission.claim_number}")
                
                # Simulate attached documents
                if i == 1:  # Only for the first email
                    test_documents = [
                        {
                            "filename": "flight_ticket.pdf",
                            "file_type": "application/pdf",
                            "file_size": 245760,
                            "document_type": "FLIGHT_TICKET"
                        },
                        {
                            "filename": "hotel_receipt.pdf",
                            "file_type": "application/pdf",
                            "file_size": 189440,
                            "document_type": "HOTEL_RECEIPT"
                        }
                    ]
                    
                    for doc_data in test_documents:
                        document = DocumentAgentOCR(
                            claim_submission_id=claim_submission.id,
                            email_id=email_record.id,
                            original_filename=doc_data['filename'],
                            file_type=doc_data['file_type'],
                            file_size=doc_data['file_size'],
                            storage_url=f"https://storage.googleapis.com/bucket/{doc_data['filename']}",
                            storage_path=f"claims/{claim_submission.claim_number}/{doc_data['filename']}",
                            document_type=doc_data['document_type'],
                            is_processed=True
                        )
                        
                        db.add(document)
                    
                    db.commit()
                    print(f"✅ {len(test_documents)} simulated documents added")
            else:
                print("📝 Processing as follow-up...")
            
            # Mark as processed
            email_record.is_processed = True
            email_record.processed_at = datetime.now()
            db.commit()
            
            print(f"✅ Email processed successfully")
        
        # Show results
        print("\n" + "=" * 50)
        print("📊 TEST RESULTS")
        print("=" * 50)
        
        total_emails = db.query(Email).count()
        total_claims = db.query(ClaimSubmission).count()
        total_documents = db.query(DocumentAgentOCR).count()
        
        print(f"📧 Emails processed: {total_emails}")
        print(f"📋 Claims created: {total_claims}")
        print(f"📄 Documents: {total_documents}")
        
        # Show created claims
        claims = db.query(ClaimSubmission).all()
        print(f"\n📋 Created claims:")
        for claim in claims:
            print(f"  - {claim.claim_number}: {claim.customer_name} ({claim.claim_type}) - {claim.status}")
        
        print("\n✅ Test completed successfully")
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        db.rollback()
    finally:
        db.close()

def cleanup_test_data():
    """Clean test data"""
    print("\n🧹 Cleaning test data...")
    
    db = SessionLocal()
    try:
        # Delete in order to respect foreign keys
        # First delete documents from test claims
        test_claims = db.query(ClaimSubmission).filter(ClaimSubmission.claim_number.like("CLM-TEST%")).all()
        for claim in test_claims:
            db.query(DocumentAgentOCR).filter(DocumentAgentOCR.claim_submission_id == claim.id).delete()
        
        # Then delete test claims
        db.query(ClaimSubmission).filter(ClaimSubmission.claim_number.like("CLM-TEST%")).delete()
        
        # Finally delete test emails
        db.query(Email).filter(Email.gmail_id.like("test_%")).delete()
        
        db.commit()
        print("✅ Test data cleaned")
        
    except Exception as e:
        print(f"❌ Error cleaning data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test email processing")
    parser.add_argument("--cleanup", action="store_true", help="Clean test data")
    
    args = parser.parse_args()
    
    if args.cleanup:
        cleanup_test_data()
    else:
        test_email_processing() 