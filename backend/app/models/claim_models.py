"""
Database models for claims and documents
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid

def generate_claim_id():
    """Generate a unique claim ID"""
    return f"CLM-{uuid.uuid4().hex[:8].upper()}"

class ClaimForm(Base):
    """Model for claim form data"""
    __tablename__ = "CLAIM_FORM"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Unique claim identifier
    claim_id = Column(String(50), unique=True, index=True, default=generate_claim_id)
    
    # Form data fields
    coverage_type = Column(String(100), nullable=False)
    full_name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    phone = Column(String(50), nullable=True)
    policy_number = Column(String(100), nullable=True)
    incident_date = Column(DateTime, nullable=True)
    incident_location = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    estimated_amount = Column(Float, nullable=True)
    
    # Status and metadata
    status = Column(String(50), default="PENDING")
    is_active = Column(Boolean, default=True)
    
    # Customer information
    customer_email = Column(String(200), nullable=True)
    
    # Analysis fields
    sentiment_analysis = Column(String(50), nullable=True)  # positive, negative, neutral
    risk_score = Column(Float, nullable=True)  # 0.0 to 1.0
    priority_level = Column(String(50), nullable=True)  # low, medium, high, urgent
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship to documents
    documents = relationship("Document", back_populates="claim_form", cascade="all, delete-orphan")

class Document(Base):
    """Model for uploaded documents"""
    __tablename__ = "DOCUMENTS"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign key to claim form
    claim_form_id = Column(Integer, ForeignKey("CLAIM_FORM.id"), nullable=False)
    
    # Document metadata
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_type = Column(String(100), nullable=False)  # MIME type
    file_size = Column(Integer, nullable=False)  # Size in bytes
    document_type = Column(String(100), nullable=False)  # e.g., "POLICE_REPORT", "RECEIPT", etc.
    
    # Storage information
    storage_url = Column(String(500), nullable=False)
    storage_path = Column(String(500), nullable=False)
    
    # Upload metadata
    uploaded_by = Column(String(200), nullable=True)  # User who uploaded
    upload_notes = Column(Text, nullable=True)
    
    # Status
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship to claim form
    claim_form = relationship("ClaimForm", back_populates="documents")