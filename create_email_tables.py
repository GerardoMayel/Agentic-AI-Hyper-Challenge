#!/usr/bin/env python3
"""
Script to create new email processing tables
"""

import sys
import os
sys.path.append('backend')

from sqlalchemy import create_engine, text
from app.core.database import engine, Base
from app.models.email_models import Email, ClaimSubmission, DocumentAgentOCR, ClaimStatusUpdate, DashboardStats

def create_email_tables():
    """Create the new email processing tables"""
    try:
        print("🔧 Creating email processing tables...")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        print("✅ Email processing tables created successfully!")
        
        # Verify tables exist
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name IN ('EMAILS', 'CLAIM_SUBMISSIONS', 'DOCUMENTS_AGENT_OCR', 'CLAIM_STATUS_UPDATES', 'DASHBOARD_STATS')
                ORDER BY table_name
            """))
            
            tables = [row[0] for row in result]
            print(f"📋 Created tables: {', '.join(tables)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def test_email_models():
    """Test the email models by creating sample data"""
    try:
        print("\n🧪 Testing email models...")
        
        from sqlalchemy.orm import sessionmaker
        from datetime import datetime
        
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Create a test email
        test_email = Email(
            gmail_id="test_123",
            thread_id="thread_123",
            from_email="test@example.com",
            to_email="claims@zurich.com",
            subject="Test Claim Notification",
            body_text="This is a test claim notification",
            body_html="<p>This is a test claim notification</p>",
            received_at=datetime.now(),
            is_first_notification=True,
            is_processed=True,
            processed_at=datetime.now()
        )
        
        db.add(test_email)
        db.commit()
        db.refresh(test_email)
        
        print(f"✅ Test email created with ID: {test_email.id}")
        
        # Create a test claim submission
        test_claim = ClaimSubmission(
            email_id=test_email.id,
            customer_name="Test User",
            customer_email="test@example.com",
            claim_type="Trip Cancellation",
            incident_date=datetime.now(),
            incident_description="Test incident",
            estimated_amount=1000.0,
            status="PENDING",
            priority="NORMAL",
            llm_summary="Test claim",
            llm_recommendation="REQUEST_MORE_DOCS"
        )
        
        db.add(test_claim)
        db.commit()
        db.refresh(test_claim)
        
        print(f"✅ Test claim created with number: {test_claim.claim_number}")
        
        # Clean up test data
        db.delete(test_claim)
        db.delete(test_email)
        db.commit()
        
        print("✅ Test data cleaned up")
        db.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing models: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Email Processing Tables Setup")
    print("=" * 50)
    
    # Create tables
    if create_email_tables():
        # Test models
        test_email_models()
        print("\n🎉 Email processing system setup complete!")
    else:
        print("\n❌ Setup failed!")

if __name__ == "__main__":
    main() 