# Este archivo define los modelos de la base de datos usando SQLAlchemy.

from sqlalchemy import (Column, Integer, String, DateTime, Float, Text,
                        ForeignKey, Enum)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base

class StatusEnum(str, enum.Enum):
    OPEN_NOTIFIED = "OPEN_NOTIFIED"
    PENDING_CUSTOMER_DOCUMENTS = "PENDING_CUSTOMER_DOCUMENTS"
    UNDER_AI_REVIEW = "UNDER_AI_REVIEW"
    PENDING_ANALYST_REVIEW = "PENDING_ANALYST_REVIEW"
    ADDITIONAL_INFO_REQUESTED = "ADDITIONAL_INFO_REQUESTED"
    DECISION_APPROVED = "DECISION_APPROVED"
    DECISION_REJECTED = "DECISION_REJECTED"
    CLOSED_PAID = "CLOSED_PAID"
    CLOSED_REJECTED = "CLOSED_REJECTED"
    IN_LITIGATION = "IN_LITIGATION"

class User(Base):
    """Modelo para analistas y administradores del sistema."""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="analyst")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    claims = relationship("Claim", back_populates="analyst")

class Policy(Base):
    """Modelo para las pólizas de seguro."""
    __tablename__ = 'policies'
    
    id = Column(Integer, primary_key=True)
    policy_number = Column(String(255), unique=True, index=True, nullable=False)
    customer_email = Column(String(255), index=True, nullable=False)
    customer_name = Column(String(255))
    status = Column(String(50), default="active")
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    coverages = relationship("Coverage", back_populates="policy", cascade="all, delete-orphan")
    claims = relationship("Claim", back_populates="policy", cascade="all, delete-orphan")

class Coverage(Base):
    """Modelo para las coberturas específicas de cada póliza."""
    __tablename__ = 'coverages'
    
    id = Column(Integer, primary_key=True)
    policy_id = Column(Integer, ForeignKey('policies.id'), nullable=False)
    coverage_type = Column(String(100), nullable=False)  # e.g., 'BAGGAGE_DELAY', 'MEDICAL', etc.
    limit_amount = Column(Float)
    deductible = Column(Float)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    policy = relationship("Policy", back_populates="coverages")

class Claim(Base):
    """Modelo central para los siniestros (claims)."""
    __tablename__ = 'claims'
    
    id = Column(Integer, primary_key=True)
    claim_number = Column(String(255), unique=True, index=True, nullable=False)
    policy_id = Column(Integer, ForeignKey('policies.id'), nullable=False)
    assigned_to_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    status = Column(Enum(StatusEnum), default=StatusEnum.OPEN_NOTIFIED, nullable=False)
    summary_ai = Column(Text)  # Resumen generado por IA
    incident_date = Column(DateTime(timezone=True))  # Fecha del incidente
    incident_description = Column(Text)  # Descripción del incidente
    estimated_amount = Column(Float)  # Monto estimado del siniestro
    opened_at = Column(DateTime(timezone=True), server_default=func.now())
    closed_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    policy = relationship("Policy", back_populates="claims")
    analyst = relationship("User", back_populates="claims")
    documents = relationship("Document", back_populates="claim", cascade="all, delete-orphan")
    claim_forms = relationship("ClaimForm", back_populates="claim", cascade="all, delete-orphan")
    communications = relationship("Communication", back_populates="claim", cascade="all, delete-orphan")

class Document(Base):
    """Modelo para los documentos adjuntos a los siniestros."""
    __tablename__ = 'documents'
    
    id = Column(Integer, primary_key=True)
    claim_id = Column(Integer, ForeignKey('claims.id'), nullable=False)
    file_name = Column(String(255), nullable=False)
    storage_url = Column(Text, nullable=False)  # URL de Cloudflare R2
    document_type = Column(String(100))  # e.g., 'RECEIPT', 'MEDICAL_REPORT', 'POLICE_REPORT'
    file_size = Column(Integer)  # Tamaño del archivo en bytes
    mime_type = Column(String(100))  # Tipo MIME del archivo
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    claim = relationship("Claim", back_populates="documents")

class ClaimForm(Base):
    """Modelo para los datos de los formularios (web o extraídos de PDF)."""
    __tablename__ = 'claim_forms'
    
    id = Column(Integer, primary_key=True)
    claim_id = Column(Integer, ForeignKey('claims.id'), nullable=False)
    submission_type = Column(String(50), nullable=False)  # 'WEB' o 'PDF_EXTRACTED'
    form_data = Column(JSONB, nullable=False)  # Todos los campos del formulario van aquí
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    claim = relationship("Claim", back_populates="claim_forms")

class Communication(Base):
    """Modelo para registrar todas las comunicaciones relacionadas con un siniestro."""
    __tablename__ = 'communications'
    
    id = Column(Integer, primary_key=True)
    claim_id = Column(Integer, ForeignKey('claims.id'), nullable=False)
    channel = Column(String(50), nullable=False)  # e.g., 'EMAIL_INBOUND', 'EMAIL_OUTBOUND', 'CHAT', 'PHONE'
    content = Column(JSONB, nullable=False)  # Cuerpo del email, transcripción del chat, etc.
    direction = Column(String(20), default="inbound")  # 'inbound' o 'outbound'
    sender = Column(String(255))  # Email o identificador del remitente
    recipient = Column(String(255))  # Email o identificador del destinatario
    subject = Column(String(500))  # Asunto (para emails)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    claim = relationship("Claim", back_populates="communications") 