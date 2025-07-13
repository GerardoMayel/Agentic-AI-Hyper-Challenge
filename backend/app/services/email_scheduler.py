"""
Email Scheduler Service - Automatically processes emails every minute
"""

import asyncio
import schedule
import time
import threading
from datetime import datetime, timedelta
from typing import List, Dict
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.services.email_processor import EmailProcessor
from app.services.gmail_service import GmailService
from app.models.email_models import Email, ClaimSubmission, DashboardStats

class EmailScheduler:
    """Service to automatically process emails every minute"""
    
    def __init__(self):
        self.is_running = False
        self.thread = None
        self.gmail_service = GmailService()
        
        # Keywords to detect claim emails
        self.claim_keywords = [
            "claim", "insurance", "trip cancellation", "flight delay", "hotel problem",
            "travel insurance", "medical claim", "accident", "cancellation", "delay", 
            "interruption", "loss", "damage", "injury", "illness", "emergency",
            "compensation", "reimbursement", "coverage", "policy"
        ]
    
    def start_scheduler(self):
        """Start automatic email processing"""
        if self.is_running:
            print("⚠️ Scheduler is already running")
            return
        
        print("🚀 Starting Email Scheduler...")
        self.is_running = True
        
        # Schedule task every minute
        schedule.every(1).minutes.do(self.process_new_emails)
        
        # Run in separate thread
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
        
        print("✅ Email Scheduler started - processing emails every minute")
    
    def stop_scheduler(self):
        """Stop automatic processing"""
        if not self.is_running:
            return
        
        print("🛑 Stopping Email Scheduler...")
        self.is_running = False
        schedule.clear()
        
        if self.thread:
            self.thread.join(timeout=5)
        
        print("✅ Email Scheduler stopped")
    
    def _run_scheduler(self):
        """Run the scheduler in loop"""
        while self.is_running:
            schedule.run_pending()
            time.sleep(30)  # Check every 30 seconds
    
    def process_new_emails(self):
        """Process new claim emails"""
        try:
            print(f"📧 [{datetime.now().strftime('%H:%M:%S')}] Checking for new emails...")
            
            db = SessionLocal()
            processor = EmailProcessor(db)
            
            # Get recent emails from Gmail
            recent_emails = self.gmail_service.get_recent_emails(max_results=10)
            
            processed_count = 0
            claims_created = 0
            
            for email_data in recent_emails:
                gmail_id = email_data['id']
                subject = email_data.get('subject', '').lower()
                body = email_data.get('body_text', '').lower()
                
                # Check if already processed - CRITICAL: Prevent duplicate processing
                existing_email = db.query(Email).filter(Email.gmail_id == gmail_id).first()
                if existing_email:
                    print(f"⏭️ Skipping already processed email: {gmail_id} - {email_data.get('subject', 'No subject')}")
                    continue
                
                # Check if it's a claim email
                if self._is_claim_email(subject, body):
                    print(f"📋 Claim email detected: {email_data.get('subject', 'No subject')}")
                    
                    try:
                        # Process the email
                        result = self._process_claim_email(email_data, db, processor)
                        if result:
                            processed_count += 1
                            if result.get('claim_created'):
                                claims_created += 1
                    except Exception as e:
                        print(f"❌ Error processing email {gmail_id}: {e}")
            
            # Update statistics
            if processed_count > 0:
                self._update_dashboard_stats(db, processed_count, claims_created)
                print(f"✅ Processed {processed_count} emails, {claims_created} claims created")
            
            db.close()
            
        except Exception as e:
            print(f"❌ Error in automatic processing: {e}")
    
    def _is_claim_email(self, subject: str, body: str) -> bool:
        """Determine if an email is a claim based on keywords"""
        text = f"{subject} {body}".lower()
        
        # Check keywords
        for keyword in self.claim_keywords:
            if keyword in text:
                return True
        
        return False
    
    def _process_claim_email(self, email_data: Dict, db: Session, processor: EmailProcessor) -> Dict:
        """Process a specific claim email"""
        try:
            # Create email record and mark as processed immediately to prevent duplicates
            email_record = Email(
                gmail_id=email_data['id'],
                thread_id=email_data['threadId'],
                from_email=email_data.get('from', ''),
                to_email=email_data.get('to', ''),
                subject=email_data.get('subject', ''),
                body_text=email_data.get('body_text', ''),
                body_html=email_data.get('body_html', ''),
                received_at=datetime.now(),
                is_processed=True,  # Mark as processed immediately
                processed_at=datetime.now()
            )
            
            db.add(email_record)
            db.commit()
            db.refresh(email_record)
            
            print(f"📝 Email marked as processed: {email_data['id']}")
            
            # Process with the processor
            processor.process_claim_email(email_record)
            
            # Check if a claim was created
            claim_created = db.query(ClaimSubmission).filter(
                ClaimSubmission.email_id == email_record.id
            ).first() is not None
            
            return {
                'email_id': email_record.id,
                'claim_created': claim_created
            }
            
        except Exception as e:
            print(f"❌ Error processing email: {e}")
            db.rollback()
            return None
    
    def _update_dashboard_stats(self, db: Session, emails_processed: int, claims_created: int):
        """Update dashboard statistics - only unique claims"""
        try:
            stats = db.query(DashboardStats).first()
            if not stats:
                stats = DashboardStats(
                    total_claims=0,
                    pending_claims=0,
                    approved_claims=0,
                    rejected_claims=0,
                    closed_claims=0,
                    total_amount_requested=0.0,
                    total_amount_approved=0.0,
                    last_updated=datetime.now()
                )
                db.add(stats)
            
            # Only update if new claims were created (not just emails processed)
            if claims_created > 0:
                # Handle None values safely
                current_total = stats.total_claims or 0
                current_pending = stats.pending_claims or 0
                
                stats.total_claims = current_total + claims_created
                stats.pending_claims = current_pending + claims_created
                stats.last_updated = datetime.now()
                
                print(f"📊 Updated dashboard stats: {claims_created} new unique claims")
            
            db.commit()
            
        except Exception as e:
            print(f"❌ Error updating statistics: {e}")
            db.rollback()

# Global scheduler instance
email_scheduler = EmailScheduler() 