"""
Google Cloud Storage service for document management
"""

import os
import uuid
from datetime import datetime
from typing import Optional, BinaryIO
from google.cloud import storage
from google.cloud.exceptions import GoogleCloudError
import json
from dotenv import load_dotenv

load_dotenv()

class StorageService:
    """Service for Google Cloud Storage operations"""
    
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        self.bucket_name = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")
        self.folder = os.getenv("GOOGLE_CLOUD_STORAGE_FOLDER", "documents")
        self.client = None
        self.bucket = None
        
        # Initialize Google Cloud Storage client (optional)
        try:
            # Check if credentials are provided as JSON string or file path
            credentials_value = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
            
            if credentials_value:
                # Check if it's a valid JSON string
                try:
                    credentials_info = json.loads(credentials_value)
                    self.client = storage.Client.from_service_account_info(credentials_info)
                    print("✅ Google Cloud Storage initialized with service account credentials (JSON)")
                except json.JSONDecodeError:
                    # If not JSON, treat as file path
                    if os.path.exists(credentials_value):
                        self.client = storage.Client.from_service_account_json(credentials_value)
                        print(f"✅ Google Cloud Storage initialized with service account credentials (file: {credentials_value})")
                    else:
                        print(f"⚠️  Credentials file not found: {credentials_value}")
                        raise Exception(f"Credentials file not found: {credentials_value}")
            else:
                # Try to use default credentials (only works in development)
                print("⚠️  No GOOGLE_APPLICATION_CREDENTIALS_JSON found")
                print("📝 Please configure service account credentials in production")
                raise Exception("Service account credentials required")
            
            self.bucket = self.client.bucket(self.bucket_name)
            print("✅ Google Cloud Storage bucket connected successfully")
        except Exception as e:
            print(f"⚠️  Google Cloud Storage not available: {str(e)}")
            print("📝 File upload functionality will be disabled")
            self.client = None
            self.bucket = None
    
    def generate_file_path(self, claim_id: str, document_type: str, original_filename: str) -> str:
        """Generate a unique file path for storage"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = os.path.splitext(original_filename)[1]
        unique_id = str(uuid.uuid4())[:8]
        
        filename = f"{document_type}_{timestamp}_{unique_id}{file_extension}"
        return f"{self.folder}/{claim_id}/{filename}"
    
    async def upload_file(
        self, 
        file_content: BinaryIO, 
        claim_id: str, 
        document_type: str, 
        original_filename: str
    ) -> dict:
        """
        Upload a file to Google Cloud Storage
        
        Returns:
            dict: {
                "storage_url": str,
                "storage_path": str,
                "filename": str,
                "file_size": int
            }
        """
        if not self.client or not self.bucket:
            raise Exception("Google Cloud Storage is not configured. Please set GOOGLE_APPLICATION_CREDENTIALS_JSON environment variable.")
        
        try:
            # Generate storage path
            storage_path = self.generate_file_path(claim_id, document_type, original_filename)
            
            # Create blob
            blob = self.bucket.blob(storage_path)
            
            # Upload file content
            blob.upload_from_file(file_content, content_type=self._get_content_type(original_filename))
            
            # Make blob publicly readable (optional, depending on your security requirements)
            # blob.make_public()
            
            # Get file size
            blob.reload()
            file_size = blob.size
            
            # Generate public URL (if needed)
            storage_url = blob.self_link
            
            return {
                "storage_url": storage_url,
                "storage_path": storage_path,
                "filename": os.path.basename(storage_path),
                "file_size": file_size
            }
            
        except GoogleCloudError as e:
            raise Exception(f"Google Cloud Storage error: {str(e)}")
        except Exception as e:
            raise Exception(f"File upload failed: {str(e)}")
    
    def delete_file(self, storage_path: str) -> bool:
        """Delete a file from Google Cloud Storage"""
        if not self.client or not self.bucket:
            raise Exception("Google Cloud Storage is not configured. Please set GOOGLE_APPLICATION_CREDENTIALS_JSON environment variable.")
        
        try:
            blob = self.bucket.blob(storage_path)
            blob.delete()
            return True
        except GoogleCloudError as e:
            raise Exception(f"Failed to delete file: {str(e)}")
    
    def get_file_url(self, storage_path: str, signed: bool = False, expiration: int = 3600) -> str:
        """Get file URL (public or signed)"""
        if not self.client or not self.bucket:
            raise Exception("Google Cloud Storage is not configured. Please set GOOGLE_APPLICATION_CREDENTIALS_JSON environment variable.")
        
        try:
            blob = self.bucket.blob(storage_path)
            
            if signed:
                url = blob.generate_signed_url(expiration=expiration)
            else:
                url = blob.self_link
            
            if url is None:
                raise Exception("Failed to generate file URL")
            return url
                
        except GoogleCloudError as e:
            raise Exception(f"Failed to generate file URL: {str(e)}")
    
    def _get_content_type(self, filename: str) -> str:
        """Get MIME content type based on file extension"""
        extension = os.path.splitext(filename)[1].lower()
        
        content_types = {
            '.pdf': 'application/pdf',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.xls': 'application/vnd.ms-excel',
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        }
        
        return content_types.get(extension, 'application/octet-stream')
    
    def list_files_by_claim(self, claim_id: str) -> list:
        """List all files for a specific claim"""
        if not self.client or not self.bucket:
            raise Exception("Google Cloud Storage is not configured. Please set GOOGLE_APPLICATION_CREDENTIALS_JSON environment variable.")
        
        try:
            prefix = f"{self.folder}/{claim_id}/"
            blobs = self.client.list_blobs(self.bucket_name, prefix=prefix)
            
            files = []
            for blob in blobs:
                files.append({
                    "name": blob.name,
                    "size": blob.size,
                    "created": blob.time_created,
                    "url": blob.public_url if blob.is_public else blob.self_link
                })
            
            return files
            
        except GoogleCloudError as e:
            raise Exception(f"Failed to list files: {str(e)}") 