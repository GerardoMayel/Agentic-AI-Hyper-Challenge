from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime

from app.core.models import Claim, ClaimDocument, ClaimFormSubmission, ClaimExpense, Coverage, ClaimStatus, CoverageType
from app.core.database import Base

# =========================================================================
# CRUD OPERATIONS FOR CLAIMS
# =========================================================================

def get_claim_by_number(db: Session, claim_number: str) -> Optional[Claim]:
    return db.query(Claim).filter(Claim.claim_number == claim_number).first()

def get_claim_by_id(db: Session, claim_id: int) -> Optional[Claim]:
    return db.query(Claim).filter(Claim.id == claim_id).first()

def get_claims_by_status(db: Session, status: ClaimStatus, limit: int = 50) -> List[Claim]:
    return db.query(Claim).filter(Claim.status == status).order_by(desc(Claim.created_at)).limit(limit).all()

def create_claim(db: Session, **kwargs) -> Claim:
    claim = Claim(**kwargs)
    db.add(claim)
    db.commit()
    db.refresh(claim)
    return claim

def update_claim_status(db: Session, claim_id: int, status: ClaimStatus) -> Optional[Claim]:
    claim = get_claim_by_id(db, claim_id)
    if claim:
        claim.status = status
        claim.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(claim)
    return claim

def get_documents_by_claim(db: Session, claim_id: int) -> List[ClaimDocument]:
    return db.query(ClaimDocument).filter(ClaimDocument.claim_id == claim_id).all()

def create_document(db: Session, **kwargs) -> ClaimDocument:
    document = ClaimDocument(**kwargs)
    db.add(document)
    db.commit()
    db.refresh(document)
    return document

def get_form_submissions_by_claim(db: Session, claim_id: int) -> List[ClaimFormSubmission]:
    return db.query(ClaimFormSubmission).filter(ClaimFormSubmission.claim_id == claim_id).all()

def create_form_submission(db: Session, **kwargs) -> ClaimFormSubmission:
    form = ClaimFormSubmission(**kwargs)
    db.add(form)
    db.commit()
    db.refresh(form)
    return form

def get_expenses_by_form_submission(db: Session, form_submission_id: int) -> List[ClaimExpense]:
    return db.query(ClaimExpense).filter(ClaimExpense.form_submission_id == form_submission_id).all()

def create_expense(db: Session, **kwargs) -> ClaimExpense:
    expense = ClaimExpense(**kwargs)
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense

def get_coverage_by_type(db: Session, coverage_type: CoverageType) -> Optional[Coverage]:
    return db.query(Coverage).filter(Coverage.coverage_type == coverage_type).first()

def get_all_coverages(db: Session) -> List[Coverage]:
    return db.query(Coverage).filter(Coverage.is_active == True).all() 