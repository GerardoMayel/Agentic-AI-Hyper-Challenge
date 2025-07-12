# Este archivo define los modelos de la base de datos usando SQLAlchemy.

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, BigInteger, ForeignKey, Enum, Numeric, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

Base = declarative_base()

class ClaimStatus(enum.Enum):
    """Status of the claim process."""
    INITIAL_NOTIFICATION = "initial_notification"
    FORM_SENT = "form_sent"
    FORM_SUBMITTED = "form_submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"

class CoverageType(enum.Enum):
    """Types of travel insurance coverage."""
    TRIP_CANCELLATION = "trip_cancellation"
    TRIP_DELAY = "trip_delay"
    TRIP_INTERRUPTION = "trip_interruption"
    BAGGAGE_DELAY = "baggage_delay"

class Claim(Base):
    """Main claim record."""
    __tablename__ = 'claims'
    
    id = Column(Integer, primary_key=True, index=True)
    claim_number = Column(String(100), unique=True, nullable=False, index=True)
    gmail_message_id = Column(String(255), unique=True, nullable=False, index=True)
    
    # Email information
    sender_email = Column(String(255), nullable=False, index=True)
    sender_name = Column(String(255))
    subject = Column(Text, nullable=False)
    email_content = Column(Text)
    notification_date = Column(DateTime, nullable=False, index=True)
    
    # Claim status
    status = Column(Enum(ClaimStatus), default=ClaimStatus.INITIAL_NOTIFICATION, index=True)
    
    # Response tracking
    response_sent = Column(Boolean, default=False)
    response_sent_date = Column(DateTime)
    form_link_sent = Column(Boolean, default=False)
    form_link_sent_date = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    documents = relationship("ClaimDocument", back_populates="claim", cascade="all, delete-orphan")
    form_submissions = relationship("ClaimFormSubmission", back_populates="claim", cascade="all, delete-orphan")

class ClaimDocument(Base):
    """Documents attached to claims."""
    __tablename__ = 'claim_documents'
    
    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(Integer, ForeignKey('claims.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Document information
    filename = Column(String(255), nullable=False)
    mime_type = Column(String(100), nullable=False)
    file_size_bytes = Column(BigInteger, nullable=False)
    
    # Storage information
    storage_url = Column(String(500))
    storage_path = Column(String(500))
    
    # Document source
    source_type = Column(String(50), nullable=False)  # 'email_attachment', 'web_form', 'manual_pdf'
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    claim = relationship("Claim", back_populates="documents")
    ocr_data = relationship("DocumentOCR", back_populates="document", uselist=False, cascade="all, delete-orphan")

class DocumentOCR(Base):
    """OCR processed data from documents."""
    __tablename__ = 'documents_ocr'
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey('DOCUMENTS.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # OCR processing information
    processed_at = Column(DateTime, default=func.now())
    processing_status = Column(String(50), default='pending')  # 'pending', 'processing', 'completed', 'failed'
    error_message = Column(Text, nullable=True)
    
    # Extracted text data
    raw_text = Column(Text, nullable=True)  # Texto extraído crudo
    structured_data = Column(JSON, nullable=True)  # Datos estructurados en formato key-value
    confidence_score = Column(Numeric(5, 4), nullable=True)  # Puntuación de confianza del OCR
    
    # Gemini processing metadata
    gemini_model_used = Column(String(100), nullable=True)
    processing_time_seconds = Column(Numeric(10, 3), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    document = relationship("Document", back_populates="ocr_data")

class ClaimFormSubmission(Base):
    """Form submissions for claims - ALINEADO CON EL FORMULARIO."""
    __tablename__ = 'claim_form_submissions'
    
    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(Integer, ForeignKey('claims.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Step 1: Claim Type
    coverage_type = Column(Enum(CoverageType), nullable=False)
    
    # Step 2: Claimant Information (About Me)
    claimant_name = Column(String(255), nullable=False)  # Name of person completing form
    email_address = Column(String(255), nullable=False)
    all_claimants_names = Column(Text)  # Full names of all persons claiming
    mailing_address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))  # State/Province
    postal_code = Column(String(20))
    mobile_phone = Column(String(50))
    other_phone = Column(String(50))  # Other Phone Number
    policy_number = Column(String(100))  # Policy/Confirmation Number
    travel_agency = Column(String(255))  # Name of agency/company you purchased from
    initial_deposit_date = Column(DateTime)  # Date initial deposit paid for trip
    
    # Step 3: Incident Details (About What Happened)
    loss_date = Column(DateTime, nullable=False)  # Date of Loss
    total_amount_requested = Column(Numeric(10, 2), nullable=False)  # Total Amount Requested (USD)
    incident_description = Column(Text, nullable=False)  # Detailed description of the incident
    
    # Step 5: Authorization & Signature
    declaration_accepted = Column(Boolean, default=False)  # I DECLARE checkbox
    signature_name = Column(String(255))  # Signature (Type your full name)
    signature_date = Column(DateTime)  # Signature Date
    
    # Submission information
    submitted_via = Column(String(50), nullable=False)  # 'web_form', 'manual_pdf'
    submitted_at = Column(DateTime, default=func.now())
    
    # Additional tracking
    ip_address = Column(String(45))  # IP address of submission
    user_agent = Column(Text)  # Browser/device info
    
    # Relationships
    claim = relationship("Claim", back_populates="form_submissions")
    expenses = relationship("ClaimExpense", back_populates="form_submission", cascade="all, delete-orphan")

class ClaimExpense(Base):
    """Individual expenses within a claim - Step 4: Breakdown of Expenses."""
    __tablename__ = 'claim_expenses'
    
    id = Column(Integer, primary_key=True, index=True)
    form_submission_id = Column(Integer, ForeignKey('claim_form_submissions.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Expense details
    description = Column(Text, nullable=False)  # Description of Expense
    expense_date = Column(DateTime, nullable=False)  # Date
    amount = Column(Numeric(10, 2), nullable=False)  # Amount (USD)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    form_submission = relationship("ClaimFormSubmission", back_populates="expenses")

class Coverage(Base):
    """Available coverage types."""
    __tablename__ = 'coverages'
    
    id = Column(Integer, primary_key=True, index=True)
    coverage_type = Column(Enum(CoverageType), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

# Function to generate unique claim number
def generate_claim_number():
    """Generates a unique claim number with format CLAIM-YYYYMMDD-XXXX."""
    from datetime import datetime
    import random
    
    date = datetime.now().strftime("%Y%m%d")
    number = random.randint(1000, 9999)
    return f"CLAIM-{date}-{number}"

# Función para extraer información del remitente
def extraer_info_remitente(from_header):
    """Extrae email y nombre del header 'From' de Gmail."""
    if not from_header:
        return None, None
    
    # Formato típico: "Nombre Apellido <email@dominio.com>"
    if '<' in from_header and '>' in from_header:
        nombre = from_header.split('<')[0].strip().strip('"')
        email = from_header.split('<')[1].split('>')[0].strip()
        return email, nombre if nombre else None
    else:
        # Solo email sin nombre
        return from_header.strip(), None

# Función para determinar si es nuevo siniestro
def es_nuevo_siniestro(remitente_email, subject, contenido):
    """Determina si un email corresponde a un nuevo siniestro."""
    # TODO: Implementar lógica más sofisticada con AI
    # Por ahora, lógica básica basada en palabras clave
    
    palabras_clave_nuevo = [
        'nuevo siniestro', 'reportar siniestro', 'declarar siniestro',
        'accidente', 'daño', 'pérdida', 'robo', 'incendio',
        'first time', 'new claim', 'report claim'
    ]
    
    texto_completo = f"{subject} {contenido}".lower()
    
    for palabra in palabras_clave_nuevo:
        if palabra in texto_completo:
            return True
    
    return False 