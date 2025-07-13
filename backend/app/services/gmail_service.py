"""
Gmail Service for reading and sending emails
"""

import os
import base64
import email.message
from typing import List, Dict, Optional
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import json

class GmailService:
    """Service for Gmail operations"""
    
    def __init__(self):
        self.creds = None
        self.service = None
        self.setup_gmail_service()
    
    def setup_gmail_service(self):
        """Setup Gmail API service"""
        try:
            # Load token from environment variable
            token_json = os.getenv("GMAIL_TOKEN_JSON")
            if not token_json:
                raise ValueError("GMAIL_TOKEN_JSON environment variable is required")
            
            # Parse token
            token_data = json.loads(token_json)
            
            # Create credentials from token
            creds = Credentials(
                token=token_data.get('token'),
                refresh_token=token_data.get('refresh_token'),
                token_uri=token_data.get('token_uri', 'https://oauth2.googleapis.com/token'),
                client_id=token_data.get('client_id'),
                client_secret=token_data.get('client_secret'),
                scopes=token_data.get('scopes', [
                    'https://www.googleapis.com/auth/gmail.readonly',
                    'https://www.googleapis.com/auth/gmail.send',
                    'https://www.googleapis.com/auth/gmail.modify'
                ])
            )
            
            # Refresh if needed
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            
            self.creds = creds
            self.service = build('gmail', 'v1', credentials=creds)
            
        except Exception as e:
            print(f"❌ Error setting up Gmail service: {e}")
            raise
    
    def get_recent_emails(self, max_results: int = 20) -> List[Dict]:
        """Get recent emails from Gmail"""
        try:
            if not self.service:
                return []
            
            # Get recent messages
            results = self.service.users().messages().list(
                userId='me',
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            emails = []
            
            for message in messages:
                email_data = self.get_email_details(message['id'])
                if email_data:
                    emails.append(email_data)
            
            return emails
            
        except Exception as e:
            print(f"❌ Error getting recent emails: {e}")
            return []
    
    def get_email_details(self, message_id: str) -> Optional[Dict]:
        """Get detailed email information"""
        try:
            if not self.service:
                return None
            
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            
            headers = message['payload']['headers']
            
            # Extract headers
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
            from_email = next((h['value'] for h in headers if h['name'] == 'From'), '')
            to_email = next((h['value'] for h in headers if h['name'] == 'To'), '')
            
            # Extract body
            body_text = self.extract_email_body(message['payload'])
            
            return {
                'id': message_id,
                'threadId': message['threadId'],
                'subject': subject,
                'from': from_email,
                'to': to_email,
                'body_text': body_text,
                'body_html': body_text  # Simplified for now
            }
            
        except Exception as e:
            print(f"❌ Error getting email details: {e}")
            return None
    
    def extract_email_body(self, payload: Dict) -> str:
        """Extract email body text"""
        try:
            if 'body' in payload and payload['body'].get('data'):
                data = payload['body']['data']
                text = base64.urlsafe_b64decode(data).decode('utf-8')
                return text
            
            if 'parts' in payload:
                for part in payload['parts']:
                    if part['mimeType'] == 'text/plain':
                        if 'data' in part['body']:
                            data = part['body']['data']
                            text = base64.urlsafe_b64decode(data).decode('utf-8')
                            return text
            
            return ""
            
        except Exception as e:
            print(f"❌ Error extracting email body: {e}")
            return ""
    
    def get_email_attachments(self, message_id: str) -> List[Dict]:
        """Get attachments from email"""
        try:
            if not self.service:
                return []
            
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            
            attachments = []
            
            def process_parts(parts):
                for part in parts:
                    if part.get('filename'):
                        attachment_id = part['body'].get('attachmentId')
                        if attachment_id:
                            attachment = self.service.users().messages().attachments().get(
                                userId='me',
                                messageId=message_id,
                                id=attachment_id
                            ).execute()
                            
                            data = base64.urlsafe_b64decode(attachment['data'])
                            
                            attachments.append({
                                'filename': part['filename'],
                                'mime_type': part['mimeType'],
                                'data': data
                            })
                    
                    if 'parts' in part:
                        process_parts(part['parts'])
            
            if 'parts' in message['payload']:
                process_parts(message['payload']['parts'])
            
            return attachments
            
        except Exception as e:
            print(f"❌ Error getting attachments: {e}")
            return []
    
    def send_email(self, to_email: str, subject: str, body: str) -> bool:
        """Send email via Gmail"""
        try:
            if not self.service:
                print("❌ Gmail service not initialized")
                return False
            
            message = email.message.EmailMessage()
            message.set_content(body)
            message['To'] = to_email
            message['Subject'] = subject
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            # Send email
            self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            print(f"✅ Email sent to {to_email}")
            return True
            
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False 