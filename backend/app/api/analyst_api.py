"""
API endpoints para la interfaz de analistas
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Form
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel

from app.core.database import get_db
from app.models.email_models import Email, ClaimSubmission, DocumentAgentOCR, ClaimStatusUpdate, DashboardStats
from app.services.llm_service import LLMService

router = APIRouter(prefix="/api/analyst", tags=["Analyst Interface"])

@router.get("/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics - only unique claims"""
    try:
        stats = db.query(DashboardStats).first()
        if not stats:
            stats = DashboardStats()
            db.add(stats)
            db.commit()
            db.refresh(stats)
        
        # Calculate additional statistics
        total_emails = db.query(Email).count()
        total_documents = db.query(DocumentAgentOCR).count()
        processed_emails = db.query(Email).filter(Email.is_processed == True).count()
        unprocessed_emails = db.query(Email).filter(Email.is_processed == False).count()
        
        # Calculate claims by status
        claims_by_status = db.query(ClaimSubmission.status, func.count(ClaimSubmission.id)).group_by(ClaimSubmission.status).all()
        status_breakdown = {status: count for status, count in claims_by_status}
        
        # Handle None values safely
        total_amount_requested = float(stats.total_amount_requested or 0)
        total_amount_approved = float(stats.total_amount_approved or 0)
        approval_rate = (total_amount_approved / total_amount_requested * 100) if total_amount_requested > 0 else 0
        
        return {
            "claims_summary": {
                "total_claims": stats.total_claims or 0,
                "pending_claims": stats.pending_claims or 0,
                "approved_claims": stats.approved_claims or 0,
                "rejected_claims": stats.rejected_claims or 0,
                "closed_claims": stats.closed_claims or 0,
                "status_breakdown": status_breakdown
            },
            "financial_summary": {
                "total_amount_requested": total_amount_requested,
                "total_amount_approved": total_amount_approved,
                "approval_rate": approval_rate
            },
            "processing_summary": {
                "total_emails": total_emails,
                "processed_emails": processed_emails,
                "unprocessed_emails": unprocessed_emails,
                "total_documents": total_documents
            },
            "last_updated": stats.last_updated.isoformat() if stats.last_updated else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting statistics: {str(e)}")

@router.get("/claims")
def get_claims(
    status: Optional[str] = Query(None, description="Filtrar por status"),
    priority: Optional[str] = Query(None, description="Filtrar por prioridad"),
    limit: int = Query(50, description="Número máximo de claims"),
    offset: int = Query(0, description="Offset para paginación"),
    db: Session = Depends(get_db)
):
    """Obtener lista de claims con filtros"""
    try:
        query = db.query(ClaimSubmission)
        
        if status:
            query = query.filter(ClaimSubmission.status == status)
        if priority:
            query = query.filter(ClaimSubmission.priority == priority)
        
        total = query.count()
        claims = query.order_by(ClaimSubmission.created_at.desc()).offset(offset).limit(limit).all()
        
        return {
            "claims": [
                {
                    "id": claim.id,
                    "claim_number": claim.claim_number,
                    "customer_name": claim.customer_name,
                    "customer_email": claim.customer_email,
                    "claim_type": claim.claim_type,
                    "status": claim.status,
                    "priority": claim.priority,
                    "estimated_amount": float(claim.estimated_amount) if claim.estimated_amount else None,
                    "created_at": claim.created_at.isoformat(),
                    "updated_at": claim.updated_at.isoformat() if claim.updated_at else None,
                    "llm_summary": claim.llm_summary,
                    "llm_recommendation": claim.llm_recommendation
                }
                for claim in claims
            ],
            "total": total,
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo claims: {str(e)}")

@router.get("/claims/{claim_id}")
def get_claim_details(claim_id: int, db: Session = Depends(get_db)):
    """Obtener detalles completos de un claim"""
    try:
        claim = db.query(ClaimSubmission).filter(ClaimSubmission.id == claim_id).first()
        if not claim:
            raise HTTPException(status_code=404, detail="Claim no encontrado")
        
        # Obtener email asociado
        email = db.query(Email).filter(Email.id == claim.email_id).first()
        
        # Obtener documentos
        documents = db.query(DocumentAgentOCR).filter(
            DocumentAgentOCR.claim_submission_id == claim_id
        ).all()
        
        # Obtener historial de cambios de estado
        status_updates = db.query(ClaimStatusUpdate).filter(
            ClaimStatusUpdate.claim_submission_id == claim_id
        ).order_by(ClaimStatusUpdate.created_at.desc()).all()
        
        return {
            "claim": {
                "id": claim.id,
                "claim_number": claim.claim_number,
                "customer_name": claim.customer_name,
                "customer_email": claim.customer_email,
                "policy_number": claim.policy_number,
                "claim_type": claim.claim_type,
                "incident_date": claim.incident_date.isoformat() if claim.incident_date else None,
                "incident_description": claim.incident_description,
                "estimated_amount": float(claim.estimated_amount) if claim.estimated_amount else None,
                "status": claim.status,
                "priority": claim.priority,
                "llm_summary": claim.llm_summary,
                "llm_recommendation": claim.llm_recommendation,
                "created_at": claim.created_at.isoformat(),
                "updated_at": claim.updated_at.isoformat() if claim.updated_at else None,
                "closed_at": claim.closed_at.isoformat() if claim.closed_at else None
            },
            "email": {
                "id": email.id if email else None,
                "subject": email.subject if email else None,
                "from_email": email.from_email if email else None,
                "body_text": email.body_text if email else None,
                "received_at": email.received_at.isoformat() if email and email.received_at else None
            } if email else None,
            "documents": [
                {
                    "id": doc.id,
                    "original_filename": doc.original_filename,
                    "file_type": doc.file_type,
                    "file_size": doc.file_size,
                    "document_type": doc.document_type,
                    "storage_url": doc.storage_url,
                    "is_processed": doc.is_processed,
                    "uploaded_at": doc.uploaded_at.isoformat(),
                    "ocr_text": doc.ocr_text[:500] + "..." if doc.ocr_text and len(doc.ocr_text) > 500 else doc.ocr_text
                }
                for doc in documents
            ],
            "status_updates": [
                {
                    "id": update.id,
                    "old_status": update.old_status,
                    "new_status": update.new_status,
                    "reason": update.reason,
                    "analyst_name": update.analyst_name,
                    "created_at": update.created_at.isoformat()
                }
                for update in status_updates
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo detalles del claim: {str(e)}")

@router.put("/claims/{claim_id}/status")
def update_claim_status(
    claim_id: int,
    status: str,
    reason: Optional[str] = None,
    analyst_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Actualizar el status de un claim"""
    try:
        claim = db.query(ClaimSubmission).filter(ClaimSubmission.id == claim_id).first()
        if not claim:
            raise HTTPException(status_code=404, detail="Claim no encontrado")
        
        old_status = claim.status
        claim.status = status
        claim.updated_at = datetime.now()
        
        # Crear registro de cambio de estado
        status_update = ClaimStatusUpdate(
            claim_submission_id=claim_id,
            old_status=old_status,
            new_status=status,
            reason=reason,
            analyst_name=analyst_name
        )
        
        db.add(status_update)
        db.commit()
        
        return {"message": f"Status actualizado de {old_status} a {status}"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error actualizando status: {str(e)}")

@router.get("/emails")
def get_emails(
    is_processed: Optional[bool] = Query(None, description="Filtrar por estado de procesamiento"),
    limit: int = Query(50, description="Número máximo de emails"),
    offset: int = Query(0, description="Offset para paginación"),
    db: Session = Depends(get_db)
):
    """Obtener lista de emails"""
    try:
        query = db.query(Email)
        
        if is_processed is not None:
            query = query.filter(Email.is_processed == is_processed)
        
        total = query.count()
        emails = query.order_by(Email.received_at.desc()).offset(offset).limit(limit).all()
        
        return {
            "emails": [
                {
                    "id": email.id,
                    "gmail_id": email.gmail_id,
                    "thread_id": email.thread_id,
                    "from_email": email.from_email,
                    "to_email": email.to_email,
                    "subject": email.subject,
                    "body_text": email.body_text[:200] + "..." if email.body_text and len(email.body_text) > 200 else email.body_text,
                    "is_processed": email.is_processed,
                    "is_first_notification": email.is_first_notification,
                    "received_at": email.received_at.isoformat(),
                    "processed_at": email.processed_at.isoformat() if email.processed_at else None
                }
                for email in emails
            ],
            "total": total,
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo emails: {str(e)}")

@router.get("/documents")
def get_documents(
    claim_id: Optional[int] = Query(None, description="Filtrar por claim ID"),
    document_type: Optional[str] = Query(None, description="Filtrar por tipo de documento"),
    is_processed: Optional[bool] = Query(None, description="Filtrar por estado de procesamiento"),
    limit: int = Query(50, description="Número máximo de documentos"),
    offset: int = Query(0, description="Offset para paginación"),
    db: Session = Depends(get_db)
):
    """Obtener lista de documentos"""
    try:
        query = db.query(DocumentAgentOCR)
        
        if claim_id:
            query = query.filter(DocumentAgentOCR.claim_submission_id == claim_id)
        if document_type:
            query = query.filter(DocumentAgentOCR.document_type == document_type)
        if is_processed is not None:
            query = query.filter(DocumentAgentOCR.is_processed == is_processed)
        
        total = query.count()
        documents = query.order_by(DocumentAgentOCR.uploaded_at.desc()).offset(offset).limit(limit).all()
        
        return {
            "documents": [
                {
                    "id": doc.id,
                    "claim_submission_id": doc.claim_submission_id,
                    "original_filename": doc.original_filename,
                    "file_type": doc.file_type,
                    "file_size": doc.file_size,
                    "document_type": doc.document_type,
                    "storage_url": doc.storage_url,
                    "is_processed": doc.is_processed,
                    "uploaded_at": doc.uploaded_at.isoformat(),
                    "processed_at": doc.processed_at.isoformat() if doc.processed_at else None,
                    "ocr_text": doc.ocr_text[:300] + "..." if doc.ocr_text and len(doc.ocr_text) > 300 else doc.ocr_text
                }
                for doc in documents
            ],
            "total": total,
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo documentos: {str(e)}")

@router.post("/claims/{claim_id}/analyze")
def analyze_claim_with_llm(claim_id: int, db: Session = Depends(get_db)):
    """Analyze a claim with LLM for comprehensive recommendations and closure suggestions"""
    try:
        claim = db.query(ClaimSubmission).filter(ClaimSubmission.id == claim_id).first()
        if not claim:
            raise HTTPException(status_code=404, detail="Claim not found")
        
        # Get associated email
        email = db.query(Email).filter(Email.id == claim.email_id).first()
        
        # Get documents
        documents = db.query(DocumentAgentOCR).filter(
            DocumentAgentOCR.claim_submission_id == claim_id
        ).all()
        
        # Get status updates history
        status_updates = db.query(ClaimStatusUpdate).filter(
            ClaimStatusUpdate.claim_submission_id == claim_id
        ).order_by(ClaimStatusUpdate.created_at.desc()).all()
        
        # Prepare comprehensive data for analysis
        analysis_data = {
            "claim": {
                "claim_number": claim.claim_number,
                "customer_name": claim.customer_name,
                "customer_email": claim.customer_email,
                "policy_number": claim.policy_number,
                "claim_type": claim.claim_type,
                "incident_description": claim.incident_description,
                "estimated_amount": claim.estimated_amount,
                "status": claim.status,
                "priority": claim.priority,
                "llm_summary": claim.llm_summary,
                "llm_recommendation": claim.llm_recommendation,
                "created_at": claim.created_at.isoformat(),
                "updated_at": claim.updated_at.isoformat() if claim.updated_at else None
            },
            "email": {
                "subject": email.subject if email else None,
                "body_text": email.body_text if email else None,
                "received_at": email.received_at.isoformat() if email and email.received_at else None
            },
            "documents": [
                {
                    "filename": doc.original_filename,
                    "document_type": doc.document_type,
                    "ocr_text": doc.ocr_text,
                    "structured_data": doc.structured_data,
                    "inferred_costs": doc.inferred_costs,
                    "is_processed": doc.is_processed
                }
                for doc in documents
            ],
            "status_history": [
                {
                    "old_status": update.old_status,
                    "new_status": update.new_status,
                    "reason": update.reason,
                    "analyst_name": update.analyst_name,
                    "created_at": update.created_at.isoformat()
                }
                for update in status_updates
            ]
        }
        
        # Create comprehensive analysis prompt
        prompt = f"""
        You are an expert insurance claims analyst. Analyze this claim comprehensively and provide detailed recommendations for closure.

        CLAIM INFORMATION:
        - Claim Number: {claim.claim_number}
        - Customer: {claim.customer_name} ({claim.customer_email})
        - Policy Number: {claim.policy_number or 'Not provided'}
        - Claim Type: {claim.claim_type}
        - Current Status: {claim.status}
        - Priority: {claim.priority}
        - Estimated Amount: ${claim.estimated_amount or 'Not specified'}
        - Created: {claim.created_at.strftime('%Y-%m-%d %H:%M')}
        
        INCIDENT DESCRIPTION:
        {claim.incident_description or 'No description provided'}
        
        ORIGINAL EMAIL:
        Subject: {email.subject if email else 'No subject'}
        Body: {email.body_text[:2000] if email and email.body_text else 'No email content'}
        Received: {email.received_at.strftime('%Y-%m-%d %H:%M') if email and email.received_at else 'Unknown'}
        
        DOCUMENTS ({len(documents)} total):
        {chr(10).join([f"- {doc.document_type}: {doc.original_filename} ({'Processed' if doc.is_processed else 'Pending'})" for doc in documents])}
        
        STATUS HISTORY:
        {chr(10).join([f"- {update.created_at.strftime('%Y-%m-%d %H:%M')}: {update.old_status} → {update.new_status} (by {update.analyst_name or 'System'})" for update in status_updates])}
        
        Please provide a comprehensive analysis in the following JSON format:
        {{
            "case_summary": "Detailed summary of the claim case",
            "risk_assessment": "Assessment of claim validity and potential risks",
            "documentation_analysis": "Analysis of provided documents and missing items",
            "recommended_action": "APPROVE/REJECT/REQUEST_MORE_DOCS/CLOSE_CASE",
            "recommended_status": "FINAL_STATUS_TO_SET",
            "closure_reason": "Detailed reason for the recommended closure",
            "suggested_amount": "Recommended approval amount (if applicable)",
            "priority_recommendation": "LOW/NORMAL/HIGH/URGENT",
            "additional_documents_needed": ["List of additional documents if any"],
            "closure_email_template": {{
                "subject": "Suggested email subject",
                "body": "Complete email body template for closure"
            }},
            "key_points": ["List of key points for the analyst"],
            "compliance_check": "Compliance and regulatory considerations"
        }}
        
        Focus on providing actionable insights and a clear path to closure.
        """
        
        # Analyze with LLM
        llm_service = LLMService()
        analysis_result = llm_service.analyze_text(prompt)
        
        # Try to parse JSON response
        try:
            import json
            import re
            
            # Try to extract JSON from markdown code blocks
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', analysis_result, re.DOTALL)
            if json_match:
                parsed_analysis = json.loads(json_match.group(1))
            else:
                # Try direct JSON parsing
                parsed_analysis = json.loads(analysis_result)
                
        except Exception as parse_error:
            print(f"JSON parsing failed: {parse_error}")
            # If JSON parsing fails, create a structured response
            parsed_analysis = {
                "case_summary": analysis_result,
                "risk_assessment": "Analysis provided in summary",
                "documentation_analysis": "Documents reviewed",
                "recommended_action": "ANALYZED",
                "recommended_status": claim.status,
                "closure_reason": "See case summary",
                "suggested_amount": claim.estimated_amount,
                "priority_recommendation": claim.priority,
                "additional_documents_needed": [],
                "closure_email_template": {
                    "subject": f"Claim Resolution - {claim.claim_number}",
                    "body": "Please review the analysis for closure details."
                },
                "key_points": ["Analysis completed"],
                "compliance_check": "Standard compliance review"
            }
        
        # Update claim with analysis
        claim.llm_summary = analysis_result
        claim.llm_recommendation = parsed_analysis.get("recommended_action", "ANALYZED")
        db.commit()
        
        return {
            "claim_id": claim_id,
            "analysis": parsed_analysis,
            "raw_analysis": analysis_result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error analyzing claim: {str(e)}")

@router.post("/auth/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    """Authenticate analyst with credentials from database"""
    try:
        # Query credentials from database with retry logic
        from sqlalchemy import text
        from sqlalchemy.exc import OperationalError
        import time
        import hashlib
        
        max_retries = 3
        retry_delay = 1  # seconds
        
        for attempt in range(max_retries):
            try:
                result = db.execute(
                    text("SELECT email, password_hash, role FROM auth_credentials WHERE email = :email AND is_active = true"),
                    {"email": email}
                ).fetchone()
                
                if result:
                    break  # Success, exit retry loop
                else:
                    raise HTTPException(status_code=401, detail="Invalid credentials")
                    
            except OperationalError as db_error:
                if "SSL connection has been closed" in str(db_error) and attempt < max_retries - 1:
                    print(f"SSL connection error, retrying in {retry_delay} seconds... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                    continue
                else:
                    # If it's the last attempt or a different error, raise it
                    raise HTTPException(status_code=503, detail="Database temporarily unavailable. Please try again in a few moments.")
        
        if not result:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        stored_email, stored_password_hash, role = result
        
        # Hash the provided password and compare
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        if password_hash == stored_password_hash:
            return {
                "success": True,
                "user": {
                    "email": stored_email,
                    "role": role
                },
                "message": "Authentication successful"
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail="Authentication service temporarily unavailable. Please try again.")

@router.get("/auth/credentials")
def get_demo_credentials(db: Session = Depends(get_db)):
    """Get demo credentials for display (without password)"""
    try:
        from sqlalchemy import text
        result = db.execute(
            text("SELECT email, role FROM auth_credentials WHERE is_active = true LIMIT 1"),
        ).fetchone()
        
        if result:
            return {
                "demo_email": result[0],
                "demo_password": "ZurichDemo2024!"  # Hardcoded for demo display
            }
        else:
            return {
                "demo_email": "analyst@zurich-demo.com",
                "demo_password": "ZurichDemo2024!"
            }
            
    except Exception as e:
        return {
            "demo_email": "analyst@zurich-demo.com",
            "demo_password": "ZurichDemo2024!"
        } 