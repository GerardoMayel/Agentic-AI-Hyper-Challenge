"""
Backend FastAPI para el Claims Management System
Extraído de la aplicación Reflex existente
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Importar servicios existentes
from app.services.claims_processor import ClaimsProcessor
from app.services.email_service import EmailService
from app.services.gcs_storage import GCSStorage
from app.services.llm_service import LLMService
from app.core.models import Claim

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

# Modelos Pydantic para la API
class ClaimRequest(BaseModel):
    coverage_type: str
    full_name: str
    email: str
    description: Optional[str] = None
    amount: Optional[float] = None

class ClaimResponse(BaseModel):
    id: str
    status: str
    message: str
    claim_number: Optional[str] = None

# Inicializar servicios
claims_processor = ClaimsProcessor()
email_service = EmailService()
storage_service = GCSStorage()
llm_service = LLMService()

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
            "email": "configured" if os.getenv("GMAIL_CREDENTIALS_FILE") else "not_configured",
            "storage": "configured" if os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET") else "not_configured"
        }
        
        return {
            "status": "healthy",
            "services": services_status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.post("/api/claims", response_model=ClaimResponse)
async def create_claim(claim_data: ClaimRequest):
    """Crear un nuevo siniestro"""
    try:
        # Procesar el siniestro
        claim = Claim(
            coverage_type=claim_data.coverage_type,
            full_name=claim_data.full_name,
            email=claim_data.email,
            description=claim_data.description,
            amount=claim_data.amount,
            status="pending"
        )
        
        # Procesar con el servicio existente
        result = await claims_processor.process_claim(claim)
        
        return ClaimResponse(
            id=str(result.get("id", "generated_id")),
            status="submitted",
            message="Claim submitted successfully",
            claim_number=result.get("claim_number")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing claim: {str(e)}")

@app.post("/api/claims/upload")
async def upload_claim_document(
    file: UploadFile = File(...),
    claim_id: str = Form(...),
    document_type: str = Form(...)
):
    """Subir documento relacionado con un siniestro"""
    try:
        # Validar tipo de archivo
        if not file.content_type.startswith('image/') and not file.content_type.startswith('application/pdf'):
            raise HTTPException(status_code=400, detail="Only images and PDF files are allowed")
        
        # Subir a Google Cloud Storage
        file_url = await storage_service.upload_file(
            file.file,
            f"claims/{claim_id}/{document_type}_{file.filename}"
        )
        
        return {
            "message": "Document uploaded successfully",
            "file_url": file_url,
            "claim_id": claim_id,
            "document_type": document_type
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading document: {str(e)}")

@app.get("/api/claims/{claim_id}")
async def get_claim(claim_id: str):
    """Obtener detalles de un siniestro específico"""
    try:
        # Aquí implementarías la lógica para obtener el siniestro de la base de datos
        # Por ahora, retornamos un mock
        return {
            "id": claim_id,
            "status": "pending",
            "coverage_type": "Trip Cancellation",
            "full_name": "John Doe",
            "email": "john@example.com",
            "created_at": "2024-01-01T00:00:00Z"
        }
        
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Claim not found: {str(e)}")

@app.get("/api/claims")
async def list_claims(limit: int = 10, offset: int = 0):
    """Listar siniestros (para el dashboard)"""
    try:
        # Aquí implementarías la lógica para obtener siniestros de la base de datos
        # Por ahora, retornamos datos mock
        claims = [
            {
                "id": f"claim_{i}",
                "status": "pending" if i % 3 == 0 else "approved" if i % 3 == 1 else "rejected",
                "coverage_type": "Trip Cancellation",
                "full_name": f"User {i}",
                "email": f"user{i}@example.com",
                "created_at": "2024-01-01T00:00:00Z"
            }
            for i in range(1, limit + 1)
        ]
        
        return {
            "claims": claims,
            "total": 100,  # Mock total
            "limit": limit,
            "offset": offset
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving claims: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 