"""
Backend FastAPI para el Claims Management System
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import os
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Importar componentes de la nueva estructura
from app.core.database import get_db, engine, Base
from app.models.claim_models import ClaimForm, Document
from app.models.schemas import (
    ClaimFormCreate, 
    ClaimFormResponse, 
    DocumentCreate, 
    DocumentResponse,
    APIResponse,
    FrontendClaimForm
)
from app.services.storage_service import StorageService

# Crear aplicación FastAPI
app = FastAPI(
    title="Zurich Insurance Claims API",
    description="API para gestión de siniestros de Zurich Insurance",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar servicios
storage_service = StorageService()

@app.on_event("startup")
async def startup_event():
    """Evento de inicio - verificar conexión a base de datos"""
    try:
        # Solo verificar conexión, no crear tablas
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1")).fetchone()
        print("✅ Database connection verified")
    except Exception as e:
        print(f"❌ Error connecting to database: {str(e)}")
        print("⚠️  Server will start but database operations may fail")

@app.get("/")
async def root():
    """Endpoint de salud de la API"""
    return {
        "message": "Zurich Insurance Claims API",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/api/health")
async def health_check():
    """Verificar estado de servicios"""
    try:
        # Verificar servicios críticos
        services_status = {
            "api": "healthy",
            "database": "connected" if os.getenv("DATABASE_URL") else "not_configured",
            "storage": "configured" if os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET") else "not_configured"
        }
        
        return {
            "status": "healthy",
            "services": services_status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.post("/api/claims", response_model=APIResponse)
async def create_claim(
    claim_data: ClaimFormCreate,
    db: Session = Depends(get_db)
):
    """Crear un nuevo siniestro"""
    try:
        print(f"Received claim data: {claim_data.dict()}")
        
        # Crear nuevo claim en la base de datos
        db_claim = ClaimForm(**claim_data.dict())
        db.add(db_claim)
        db.commit()
        db.refresh(db_claim)
        
        print(f"Claim created successfully: {db_claim.claim_id}")
        
        return APIResponse(
            success=True,
            message="Claim created successfully",
            data={
                "id": db_claim.id,
                "claim_id": db_claim.claim_id,
                "status": db_claim.status
            }
        )
        
    except Exception as e:
        db.rollback()
        print(f"Error creating claim: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating claim: {str(e)}")

@app.post("/api/claims/frontend", response_model=APIResponse)
async def create_claim_from_frontend(
    claim_data: FrontendClaimForm,
    db: Session = Depends(get_db)
):
    """Crear un nuevo siniestro desde el formulario del frontend"""
    try:
        print(f"Received frontend claim data: {claim_data.dict()}")
        
        # Preparar datos para la base de datos
        db_claim_data = {
            "coverage_type": claim_data.claimType,
            "full_name": claim_data.fullName,
            "email": claim_data.email,
            "phone": claim_data.mobilePhone,
            "policy_number": claim_data.policyNumber,
            "incident_date": datetime.fromisoformat(claim_data.lossDate) if claim_data.lossDate else None,
            "incident_location": f"{claim_data.address}, {claim_data.city}, {claim_data.state} {claim_data.zipCode}",
            "description": claim_data.incidentDescription,
            "estimated_amount": sum(expense.get('amount', 0) for expense in claim_data.expenses) if claim_data.expenses else 0
        }
        
        # Crear nuevo claim en la base de datos
        db_claim = ClaimForm(**db_claim_data)
        db.add(db_claim)
        db.commit()
        db.refresh(db_claim)
        
        print(f"Frontend claim created successfully: {db_claim.claim_id}")
        
        return APIResponse(
            success=True,
            message="Claim created successfully from frontend",
            data={
                "id": db_claim.id,
                "claim_id": db_claim.claim_id,
                "status": db_claim.status
            }
        )
        
    except Exception as e:
        db.rollback()
        print(f"Error creating frontend claim: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating claim: {str(e)}")

@app.post("/api/claims/{claim_id}/documents", response_model=APIResponse)
async def upload_claim_document(
    claim_id: str,
    file: UploadFile = File(...),
    document_type: str = Form(...),
    upload_notes: str = Form(None),
    db: Session = Depends(get_db)
):
    """Subir documento relacionado con un siniestro"""
    try:
        # Validar tipo de archivo
        if not file.content_type or (not file.content_type.startswith('image/') and not file.content_type.startswith('application/pdf')):
            raise HTTPException(status_code=400, detail="Only images and PDF files are allowed")
        
        # Buscar el claim
        claim = db.query(ClaimForm).filter(ClaimForm.claim_id == claim_id).first()
        if not claim:
            raise HTTPException(status_code=404, detail="Claim not found")
        
        # Leer contenido del archivo
        file_content = await file.read()
        
        # Validar que el archivo tenga nombre
        if not file.filename:
            raise HTTPException(status_code=400, detail="File must have a name")
        
        # Subir archivo a Google Cloud Storage
        storage_url = storage_service.upload_file(
            file_content,
            file.filename,
            claim_id,
            "web-form",  # email_id para la estructura de carpetas
            file.content_type
        )
        
        if not storage_url:
            raise HTTPException(status_code=500, detail="Failed to upload file to storage")
        
        # Generar ruta de storage
        storage_path = f"documentos/{claim_id}/web-form/{file.filename}"
        
        # Crear registro en la base de datos
        db_document = Document(
            claim_form_id=claim.id,
            filename=file.filename,
            original_filename=file.filename,
            file_type=file.content_type,
            file_size=len(file_content),
            document_type=document_type,
            storage_url=storage_url,
            storage_path=storage_path,
            upload_notes=upload_notes
        )
        
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
        
        return APIResponse(
            success=True,
            message="Document uploaded successfully",
            data={
                "id": db_document.id,
                "filename": db_document.filename,
                "storage_url": db_document.storage_url,
                "file_size": db_document.file_size
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error uploading document: {str(e)}")

@app.get("/api/claims/{claim_id}", response_model=APIResponse)
async def get_claim(claim_id: str, db: Session = Depends(get_db)):
    """Obtener detalles de un siniestro específico"""
    try:
        claim = db.query(ClaimForm).filter(ClaimForm.claim_id == claim_id).first()
        if not claim:
            raise HTTPException(status_code=404, detail="Claim not found")
        
        # Obtener documentos relacionados
        documents = db.query(Document).filter(Document.claim_form_id == claim.id).all()
        
        return APIResponse(
            success=True,
            message="Claim retrieved successfully",
            data={
                "claim": {
                    "id": claim.id,
                    "claim_id": claim.claim_id,
                    "coverage_type": claim.coverage_type,
                    "full_name": claim.full_name,
                    "email": claim.email,
                    "phone": claim.phone,
                    "policy_number": claim.policy_number,
                    "incident_date": claim.incident_date,
                    "incident_location": claim.incident_location,
                    "description": claim.description,
                    "estimated_amount": claim.estimated_amount,
                    "status": claim.status,
                    "created_at": claim.created_at
                },
                "documents": [
                    {
                        "id": doc.id,
                        "filename": doc.filename,
                        "document_type": doc.document_type,
                        "storage_url": doc.storage_url,
                        "uploaded_at": doc.uploaded_at
                    }
                    for doc in documents
                ]
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving claim: {str(e)}")

@app.get("/api/claims", response_model=APIResponse)
async def list_claims(
    limit: int = 10, 
    offset: int = 0, 
    db: Session = Depends(get_db)
):
    """Listar siniestros (para el dashboard)"""
    try:
        claims = db.query(ClaimForm).offset(offset).limit(limit).all()
        total = db.query(ClaimForm).count()
        
        return APIResponse(
            success=True,
            message="Claims retrieved successfully",
            data={
                "claims": [
                    {
                        "id": claim.id,
                        "claim_id": claim.claim_id,
                        "coverage_type": claim.coverage_type,
                        "full_name": claim.full_name,
                        "email": claim.email,
                        "status": claim.status,
                        "created_at": claim.created_at
                    }
                    for claim in claims
                ],
                "total": total,
                "limit": limit,
                "offset": offset
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving claims: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 