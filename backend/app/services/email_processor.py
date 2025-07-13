"""
Email processing service for claim notifications
"""

import os
import json
import base64
import email
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

from app.models.email_models import Email, ClaimSubmission, DocumentAgentOCR
from app.services.llm_service import LLMService
from app.services.gmail_service import GmailService
from app.services.storage_service import StorageService

class EmailProcessor:
    """Service for processing claim notification emails"""
    
    def __init__(self, db: Session):
        self.db = db
        self.llm_service = LLMService()
        self.gmail_service = GmailService()
        self.storage_service = StorageService()
        
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
    
    def check_new_emails(self) -> List[Dict]:
        """Check for new emails and process claim notifications"""
        try:
            print("📧 Checking for new emails...")
            
            # Get recent emails from Gmail
            emails = self.gmail_service.get_recent_emails(max_results=20)
            processed_emails = []
            
            for email_data in emails:
                gmail_id = email_data['id']
                thread_id = email_data['threadId']
                
                # Check if email already processed
                existing_email = self.db.query(Email).filter(Email.gmail_id == gmail_id).first()
                if existing_email:
                    continue
                
                # Extract email content
                subject = email_data.get('subject', '')
                from_email = email_data.get('from', '')
                to_email = email_data.get('to', '')
                body_text = email_data.get('body_text', '')
                body_html = email_data.get('body_html', '')
                
                # Check if it's a claim notification
                if self.is_claim_notification(subject, body_text):
                    print(f"📋 Found claim notification: {subject}")
                    
                    # Save email to database
                    email_record = Email(
                        gmail_id=gmail_id,
                        thread_id=thread_id,
                        from_email=from_email,
                        to_email=to_email,
                        subject=subject,
                        body_text=body_text,
                        body_html=body_html,
                        received_at=datetime.now()
                    )
                    
                    self.db.add(email_record)
                    self.db.commit()
                    self.db.refresh(email_record)
                    
                    # Process the email
                    self.process_claim_email(email_record)
                    
                    processed_emails.append({
                        'id': email_record.id,
                        'subject': subject,
                        'from': from_email,
                        'processed': True
                    })
            
            print(f"✅ Processed {len(processed_emails)} claim notifications")
            return processed_emails
            
        except Exception as e:
            print(f"❌ Error checking emails: {e}")
            return []
    
    def process_claim_email(self, email_record: Email):
        """Process a claim notification email"""
        try:
            print(f"🔍 Processing email ID: {email_record.id}")
            
            # Check if this is the first notification in the thread
            is_first = self.check_if_first_notification(email_record)
            email_record.is_first_notification = is_first
            
            if is_first:
                print("🆕 First notification detected - creating new claim")
                self.create_claim_submission(email_record)
                self.send_initial_response(email_record)
            else:
                print("📝 Follow-up email - updating existing claim")
                self.process_follow_up_email(email_record)
            
            # Process attachments
            self.process_email_attachments(email_record)
            
            # Mark as processed
            email_record.is_processed = True
            email_record.processed_at = datetime.now()
            self.db.commit()
            
        except Exception as e:
            print(f"❌ Error processing email {email_record.id}: {e}")
    
    def check_if_first_notification(self, email_record: Email) -> bool:
        """Use LLM to determine if this is the first notification"""
        try:
            # Check if there are previous emails in the same thread
            previous_emails = self.db.query(Email).filter(
                Email.thread_id == email_record.thread_id,
                Email.received_at < email_record.received_at
            ).count()
            
            if previous_emails == 0:
                return True
            
            # Use LLM to analyze the email content
            prompt = f"""
            Analyze this email and determine if it's the FIRST notification of a new insurance claim or a follow-up to an existing claim.
            
            Email Subject: {email_record.subject}
            Email Body: {email_record.body_text[:1000]}
            
            Consider:
            1. Does this email introduce a new incident/claim?
            2. Does it reference a previous claim number or conversation?
            3. Is it responding to a previous email?
            4. Does it contain initial claim details or additional information?
            
            Respond with ONLY: "FIRST" or "FOLLOW_UP"
            """
            
            response = self.llm_service.analyze_text(prompt)
            return "FIRST" in response.upper()
            
        except Exception as e:
            print(f"❌ Error checking if first notification: {e}")
            return True  # Default to first notification
    
    def create_claim_submission(self, email_record: Email):
        """Create a new claim submission from email"""
        try:
            # Extract claim details using LLM
            claim_data = self.extract_claim_details(email_record)
            
            # Create claim submission
            claim_submission = ClaimSubmission(
                email_id=email_record.id,
                customer_name=claim_data.get('customer_name', 'Unknown'),
                customer_email=email_record.from_email,
                policy_number=claim_data.get('policy_number'),
                claim_type=claim_data.get('claim_type', 'General'),
                incident_date=claim_data.get('incident_date'),
                incident_description=claim_data.get('incident_description'),
                estimated_amount=claim_data.get('estimated_amount'),
                status='PENDING',
                priority=claim_data.get('priority', 'NORMAL'),
                sentiment_analysis=claim_data.get('sentiment_analysis', 'NEUTRAL'),
                risk_score=claim_data.get('risk_score', 0.5),
                priority_level=claim_data.get('priority', 'NORMAL').lower()
            )
            
            self.db.add(claim_submission)
            self.db.commit()
            self.db.refresh(claim_submission)
            
            print(f"✅ Created claim submission: {claim_submission.claim_number}")
            
            # Generate LLM summary
            self.generate_claim_summary(claim_submission)
            
        except Exception as e:
            print(f"❌ Error creating claim submission: {e}")
    
    def extract_claim_details(self, email_record: Email) -> Dict:
        """Extract claim details from email using LLM"""
        try:
            prompt = f"""
            Extract insurance claim details from this email. Return a JSON object with the following fields:
            
            Email Subject: {email_record.subject}
            Email Body: {email_record.body_text}
            
            Extract and return JSON with these fields:
            - customer_name: Full name of the claimant
            - policy_number: Insurance policy number (if mentioned)
            - claim_type: Type of claim (Trip Cancellation, Trip Delay, Trip Interruption, etc.)
            - incident_date: Date of the incident (YYYY-MM-DD format)
            - incident_description: Description of what happened
            - estimated_amount: Estimated claim amount (number only)
            - priority: LOW, NORMAL, HIGH, or URGENT based on content
            - sentiment_analysis: POSITIVE, NEGATIVE, or NEUTRAL based on customer tone
            - risk_score: Number between 0.0 and 1.0 indicating claim risk (0=low risk, 1=high risk)
            
            Return ONLY valid JSON, no additional text.
            """
            
            response = self.llm_service.analyze_text(prompt)
            
            # Try to parse JSON response
            try:
                return json.loads(response)
            except:
                # Fallback to default values
                return {
                    'customer_name': 'Unknown',
                    'claim_type': 'General',
                    'incident_description': email_record.body_text[:500],
                    'priority': 'NORMAL'
                }
                
        except Exception as e:
            print(f"❌ Error extracting claim details: {e}")
            return {
                'customer_name': 'Unknown',
                'claim_type': 'General',
                'incident_description': email_record.body_text[:500],
                'priority': 'NORMAL'
            }
    
    def generate_claim_summary(self, claim_submission: ClaimSubmission):
        """Generate LLM summary and recommendation for claim"""
        try:
            prompt = f"""
            Analyze this insurance claim and provide a summary and recommendation.
            
            Claim Details:
            - Customer: {claim_submission.customer_name}
            - Type: {claim_submission.claim_type}
            - Description: {claim_submission.incident_description}
            - Amount: ${claim_submission.estimated_amount}
            
            Provide:
            1. A brief summary of the claim
            2. Recommendation: CLOSE_CASE, REQUEST_MORE_DOCS, APPROVE, or REJECT
            
            Return as JSON:
            {{"summary": "brief summary", "recommendation": "RECOMMENDATION"}}
            """
            
            response = self.llm_service.analyze_text(prompt)
            
            try:
                result = json.loads(response)
                claim_submission.llm_summary = result.get('summary', '')
                claim_submission.llm_recommendation = result.get('recommendation', 'REQUEST_MORE_DOCS')
                self.db.commit()
            except:
                claim_submission.llm_summary = "Claim requires review"
                claim_submission.llm_recommendation = "REQUEST_MORE_DOCS"
                self.db.commit()
                
        except Exception as e:
            print(f"❌ Error generating claim summary: {e}")
    
    def send_initial_response(self, email_record: Email):
        """Send initial response email with form options"""
        try:
            claim_submission = self.db.query(ClaimSubmission).filter(
                ClaimSubmission.email_id == email_record.id
            ).first()
            
            if not claim_submission:
                return
            
            subject = f"Claim Received - {claim_submission.claim_number}"
            
            body = f"""
            Dear {claim_submission.customer_name},
            
            Thank you for submitting your insurance claim. We have received your notification and assigned claim number: {claim_submission.claim_number}
            
            To complete your claim, you have two options:
            
            1. **Online Form**: Visit our secure claim form at:
               https://agentic-ai-hyper-challenge-front-end.onrender.com/claim-form/
               
            2. **Email Response**: Reply to this email with the following information:
               - Policy Number: {claim_submission.policy_number or 'Please provide'}
               - Detailed incident description
               - Supporting documents (attachments)
               - Estimated claim amount
               - Contact information
               
            Please include any relevant documents such as:
            - Flight tickets
            - Hotel receipts
            - Restaurant bills
            - Medical documents
            - Police reports (if applicable)
            
            We will process your claim within 24-48 hours.
            
            Best regards,
            Zurich Insurance Claims Team
            """
            
            # Send email
            self.gmail_service.send_email(
                to_email=email_record.from_email,
                subject=subject,
                body=body
            )
            
            print(f"✅ Sent initial response for claim {claim_submission.claim_number}")
            
        except Exception as e:
            print(f"❌ Error sending initial response: {e}")
    
    def process_follow_up_email(self, email_record: Email):
        """Process follow-up email in existing claim thread"""
        try:
            # Find the original claim submission
            original_email = self.db.query(Email).filter(
                Email.thread_id == email_record.thread_id,
                Email.is_first_notification == True
            ).first()
            
            if original_email and original_email.claim_submission:
                claim_submission = original_email.claim_submission
                print(f"📝 Processing follow-up for claim {claim_submission.claim_number}")
                
                # Process any new information or documents
                # This could include updating claim details, processing new documents, etc.
                
        except Exception as e:
            print(f"❌ Error processing follow-up email: {e}")
    
    def process_email_attachments(self, email_record: Email):
        """Process attachments from email"""
        try:
            # Get attachments from Gmail
            attachments = self.gmail_service.get_email_attachments(email_record.gmail_id)
            
            for attachment in attachments:
                # Upload to storage
                storage_url = self.storage_service.upload_file(
                    attachment['data'],
                    attachment['filename'],
                    f"email-{email_record.id}",
                    "email-attachments",
                    attachment['mime_type']
                )
                
                if storage_url:
                    # Create document record
                    doc_record = DocumentAgentOCR(
                        email_id=email_record.id,
                        original_filename=attachment['filename'],
                        file_type=attachment['mime_type'],
                        file_size=len(attachment['data']),
                        storage_url=storage_url,
                        storage_path=f"documentos/email-{email_record.id}/email-attachments/{attachment['filename']}"
                    )
                    
                    self.db.add(doc_record)
                    self.db.commit()
                    
                    print(f"✅ Processed attachment: {attachment['filename']}")
                    
        except Exception as e:
            print(f"❌ Error processing attachments: {e}") 