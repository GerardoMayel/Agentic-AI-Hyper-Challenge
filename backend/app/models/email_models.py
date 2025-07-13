"""
Database models for email processing and OCR documents
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid

def generate_claim_number():
    """Generate a unique claim number"""
    return f"CLM-{uuid.uuid4().hex[:8].upper()}"

class Email(Base):
    """Model for received emails"""
    __tablename__ = "EMAILS"
    
    id = Column(Integer, primary_key=True, index=True)
    gmail_id = Column(String(255), unique=True, nullable=False)  # Gmail message ID
    thread_id = Column(String(255), nullable=False)  # Gmail thread ID for conversation tracking
    
    # Email metadata
    from_email = Column(String(255), nullable=False)
    to_email = Column(String(255), nullable=False)
    subject = Column(String(500), nullable=False)
    body_text = Column(Text, nullable=True)
    body_html = Column(Text, nullable=True)
    
    # Timestamps
    received_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Status
    is_processed = Column(Boolean, default=False)
    is_first_notification = Column(Boolean, nullable=True)  # Determined by LLM
    
    # Relationships
    claim_submission = relationship("ClaimSubmission", back_populates="initial_email")
    documents = relationship("DocumentAgentOCR", back_populates="email")

class ClaimSubmission(Base):
    """Model for claim submissions from emails"""
    __tablename__ = "CLAIM_SUBMISSIONS"
    
    id = Column(Integer, primary_key=True, index=True)
    claim_number = Column(String(50), unique=True, index=True, default=generate_claim_number)
    
    # Email relationship
    email_id = Column(Integer, ForeignKey("EMAILS.id"), nullable=False)
    initial_email = relationship("Email", back_populates="claim_submission")
    
    # Claim details (extracted from email by LLM)
    customer_name = Column(String(200), nullable=False)
    customer_email = Column(String(200), nullable=False)
    policy_number = Column(String(100), nullable=True)
    claim_type = Column(String(100), nullable=False)
    incident_date = Column(DateTime, nullable=True)
    incident_description = Column(Text, nullable=True)
    estimated_amount = Column(Float, nullable=True)
    
    # Status and processing
    status = Column(String(50), default="PENDING")  # PENDING, UNDER_REVIEW, APPROVED, REJECTED, CLOSED
    priority = Column(String(20), default="NORMAL")  # LOW, NORMAL, HIGH, URGENT
    
    # LLM analysis
    llm_summary = Column(Text, nullable=True)
    llm_recommendation = Column(String(100), nullable=True)  # CLOSE_CASE, REQUEST_MORE_DOCS, APPROVE, REJECT
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    closed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    documents = relationship("DocumentAgentOCR", back_populates="claim_submission")
    status_updates = relationship("ClaimStatusUpdate", back_populates="claim_submission")

class DocumentAgentOCR(Base):
    """Model for documents processed with OCR"""
    __tablename__ = "DOCUMENTS_AGENT_OCR"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Relationships
    claim_submission_id = Column(Integer, ForeignKey("CLAIM_SUBMISSIONS.id"), nullable=False)
    claim_submission = relationship("ClaimSubmission", back_populates="documents")
    
    email_id = Column(Integer, ForeignKey("EMAILS.id"), nullable=True)
    email = relationship("Email", back_populates="documents")
    
    # Document metadata
    original_filename = Column(String(255), nullable=False)
    file_type = Column(String(100), nullable=False)  # MIME type
    file_size = Column(Integer, nullable=False)
    
    # Storage
    storage_url = Column(String(500), nullable=False)
    storage_path = Column(String(500), nullable=False)
    
    # OCR Results
    ocr_text = Column(Text, nullable=True)  # Raw OCR text
    structured_data = Column(JSON, nullable=True)  # Key-value pairs from OCR
    image_description = Column(JSON, nullable=True)  # Image analysis results
    
    # Document classification
    document_type = Column(String(100), nullable=True)  # FLIGHT_TICKET, HOTEL_RECEIPT, RESTAURANT_BILL, etc.
    inferred_costs = Column(JSON, nullable=True)  # Extracted costs from document
    
    # Processing status
    is_processed = Column(Boolean, default=False)
    processing_errors = Column(Text, nullable=True)
    
    # Timestamps
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)

class ClaimStatusUpdate(Base):
    """Model for tracking claim status changes"""
    __tablename__ = "CLAIM_STATUS_UPDATES"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Relationship
    claim_submission_id = Column(Integer, ForeignKey("CLAIM_SUBMISSIONS.id"), nullable=False)
    claim_submission = relationship("ClaimSubmission", back_populates="status_updates")
    
    # Status change
    old_status = Column(String(50), nullable=True)
    new_status = Column(String(50), nullable=False)
    reason = Column(Text, nullable=True)
    
    # Analyst info
    analyst_name = Column(String(200), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class DashboardStats(Base):
    """Model for dashboard statistics"""
    __tablename__ = "DASHBOARD_STATS"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Statistics
    total_claims = Column(Integer, default=0)
    pending_claims = Column(Integer, default=0)
    approved_claims = Column(Integer, default=0)
    rejected_claims = Column(Integer, default=0)
    closed_claims = Column(Integer, default=0)
    
    # Financial
    total_amount_requested = Column(Float, default=0.0)
    total_amount_approved = Column(Float, default=0.0)
    
    # Timestamps
    last_updated = Column(DateTime(timezone=True), server_default=func.now()) 