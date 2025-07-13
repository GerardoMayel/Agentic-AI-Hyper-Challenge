"""
Pydantic schemas for API validation
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Claim Form Schemas
class ClaimFormBase(BaseModel):
    coverage_type: str
    full_name: str
    email: str
    phone: Optional[str] = None
    policy_number: Optional[str] = None
    incident_date: Optional[datetime] = None
    incident_location: Optional[str] = None
    description: Optional[str] = None
    estimated_amount: Optional[float] = None

class ClaimFormCreate(ClaimFormBase):
    pass

# Extended schemas for frontend form
class FrontendClaimForm(BaseModel):
    # Claim type
    claimType: str
    
    # Claimant information
    fullName: str
    email: str
    address: str
    city: str
    state: str
    zipCode: str
    mobilePhone: str
    otherPhone: Optional[str] = None
    allClaimants: str
    policyNumber: str
    insuranceAgency: str
    initialDepositDate: str
    
    # Incident details
    incidentDescription: str
    lossDate: str
    
    # Authorization
    authorization: bool
    signature: str
    signatureDate: str
    
    # Expenses (will be stored as JSON in description field)
    expenses: Optional[List[dict]] = None

class ClaimFormResponse(ClaimFormBase):
    id: int
    claim_id: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Document Schemas
class DocumentBase(BaseModel):
    document_type: str
    upload_notes: Optional[str] = None

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: int
    claim_form_id: int
    filename: str
    original_filename: str
    file_type: str
    file_size: int
    storage_url: str
    storage_path: str
    uploaded_by: Optional[str] = None
    is_verified: bool
    uploaded_at: datetime
    
    class Config:
        from_attributes = True

# Combined Response Schemas
class ClaimFormWithDocuments(ClaimFormResponse):
    documents: List[DocumentResponse] = []

# API Response Schemas
class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

class ClaimFormAPIResponse(APIResponse):
    data: Optional[ClaimFormResponse] = None

class DocumentAPIResponse(APIResponse):
    data: Optional[DocumentResponse] = None 