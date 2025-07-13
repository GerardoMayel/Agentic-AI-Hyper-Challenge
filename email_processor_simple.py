#!/usr/bin/env python3
"""
Simple Email Processor for testing
"""

import os
import json
import time
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Import our models
import sys
sys.path.append('backend')
from app.models.email_models import Email, ClaimSubmission, DocumentAgentOCR, Base
from app.core.database import get_db

class SimpleEmailProcessor:
    """Simple email processor for testing"""
    
    def __init__(self):
        self.db = next(get_db())
        
        # Keywords for claim notification subjects
        self.claim_keywords = [
            "claim notification",
            "claim submission", 
            "claim report",
            "insurance claim",
            "trip cancellation",
            "trip delay",
            "trip interruption",
            "travel claim",
            "flight cancellation",
            "hotel cancellation",
            "travel insurance claim"
        ]
    
    def is_claim_notification(self, subject: str, body: str) -> bool:
        """Check if email is a claim notification"""
        subject_lower = subject.lower()
        body_lower = body.lower()
        
        # Check subject keywords
        for keyword in self.claim_keywords:
            if keyword in subject_lower:
                return True
        
        # Check body keywords
        for keyword in self.claim_keywords:
            if keyword in body_lower:
                return True
        
        return False
    
    def simulate_email_check(self):
        """Simulate checking for new emails"""
        print("📧 Simulating email check...")
        
        # Simulate some test emails
        test_emails = [
            {
                'gmail_id': f'test_{int(time.time())}_1',
                'thread_id': f'thread_{int(time.time())}_1',
                'from_email': 'john.doe@example.com',
                'to_email': 'claims@zurich.com',
                'subject': 'Claim Notification - Trip Cancellation',
                'body_text': 'Hello, I need to submit a claim for my cancelled trip to Paris. My flight was cancelled due to weather conditions.',
                'received_at': datetime.now()
            },
            {
                'gmail_id': f'test_{int(time.time())}_2',
                'thread_id': f'thread_{int(time.time())}_2',
                'from_email': 'jane.smith@example.com',
                'to_email': 'claims@zurich.com',
                'subject': 'Insurance Claim Report',
                'body_text': 'I had to cancel my hotel reservation due to a medical emergency. Please process my claim.',
                'received_at': datetime.now()
            },
            {
                'gmail_id': f'test_{int(time.time())}_3',
                'thread_id': f'thread_{int(time.time())}_3',
                'from_email': 'spam@example.com',
                'to_email': 'claims@zurich.com',
                'subject': 'Weekly Newsletter',
                'body_text': 'Check out our latest offers and promotions!',
                'received_at': datetime.now()
            }
        ]
        
        processed_count = 0
        
        for email_data in test_emails:
            # Check if it's a claim notification
            if self.is_claim_notification(email_data['subject'], email_data['body_text']):
                print(f"📋 Found claim notification: {email_data['subject']}")
                
                # Check if email already processed
                existing_email = self.db.query(Email).filter(
                    Email.gmail_id == email_data['gmail_id']
                ).first()
                
                if existing_email:
                    print(f"⚠️  Email already processed: {email_data['gmail_id']}")
                    continue
                
                # Save email to database
                email_record = Email(
                    gmail_id=email_data['gmail_id'],
                    thread_id=email_data['thread_id'],
                    from_email=email_data['from_email'],
                    to_email=email_data['to_email'],
                    subject=email_data['subject'],
                    body_text=email_data['body_text'],
                    body_html=email_data['body_text'],
                    received_at=email_data['received_at'],
                    is_first_notification=True,
                    is_processed=True,
                    processed_at=datetime.now()
                )
                
                self.db.add(email_record)
                self.db.commit()
                self.db.refresh(email_record)
                
                # Create claim submission
                self.create_claim_submission(email_record)
                
                processed_count += 1
                print(f"✅ Processed email: {email_data['subject']}")
            else:
                print(f"❌ Not a claim notification: {email_data['subject']}")
        
        print(f"✅ Processed {processed_count} claim notifications")
        return processed_count
    
    def create_claim_submission(self, email_record: Email):
        """Create a new claim submission from email"""
        try:
            # Extract basic claim details
            customer_name = email_record.from_email.split('@')[0].replace('.', ' ').title()
            
            # Determine claim type from subject/body
            claim_type = "General"
            if "trip cancellation" in email_record.subject.lower():
                claim_type = "Trip Cancellation"
            elif "trip delay" in email_record.subject.lower():
                claim_type = "Trip Delay"
            elif "hotel" in email_record.body_text.lower():
                claim_type = "Hotel Cancellation"
            
            # Create claim submission
            claim_submission = ClaimSubmission(
                email_id=email_record.id,
                customer_name=customer_name,
                customer_email=email_record.from_email,
                policy_number=None,  # Will be extracted by LLM later
                claim_type=claim_type,
                incident_date=datetime.now(),
                incident_description=email_record.body_text[:500],
                estimated_amount=0.0,  # Will be calculated later
                status='PENDING',
                priority='NORMAL',
                llm_summary="Claim requires review",
                llm_recommendation="REQUEST_MORE_DOCS"
            )
            
            self.db.add(claim_submission)
            self.db.commit()
            self.db.refresh(claim_submission)
            
            print(f"✅ Created claim submission: {claim_submission.claim_number}")
            
        except Exception as e:
            print(f"❌ Error creating claim submission: {e}")
    
    def run_continuous_check(self, interval_minutes: int = 1):
        """Run continuous email checking"""
        print(f"🚀 Starting email processor (checking every {interval_minutes} minute(s))")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                print(f"\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Checking emails...")
                self.simulate_email_check()
                
                # Wait for next check
                time.sleep(interval_minutes * 60)
                
        except KeyboardInterrupt:
            print("\n🛑 Email processor stopped")

def main():
    """Main function"""
    processor = SimpleEmailProcessor()
    
    # Run one check
    print("🧪 Running single email check...")
    processor.simulate_email_check()
    
    # Ask if user wants continuous checking
    response = input("\nDo you want to run continuous checking? (y/n): ")
    if response.lower() == 'y':
        interval = int(input("Check interval in minutes (default 1): ") or "1")
        processor.run_continuous_check(interval)

if __name__ == "__main__":
    main() 