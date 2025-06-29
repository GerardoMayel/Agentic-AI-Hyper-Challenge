# Este archivo define los modelos de la base de datos usando SQLAlchemy.

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, BigInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class Siniestro(Base):
    """Modelo básico para siniestros reportados."""
    __tablename__ = 'siniestros'
    
    id = Column(Integer, primary_key=True, index=True)
    numero_siniestro = Column(String(100), unique=True, nullable=False, index=True)
    gmail_message_id = Column(String(255), unique=True, nullable=False, index=True)
    remitente_email = Column(String(255), nullable=False, index=True)
    remitente_nombre = Column(String(255))
    subject = Column(Text, nullable=False)
    contenido_texto = Column(Text)
    fecha_reporte = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relación 1 a muchos con documentos
    documentos = relationship("Documento", back_populates="siniestro", cascade="all, delete-orphan")

class Documento(Base):
    """Modelo para documentos adjuntos a siniestros."""
    __tablename__ = 'documentos'
    
    id = Column(Integer, primary_key=True, index=True)
    siniestro_id = Column(Integer, ForeignKey('siniestros.id', ondelete='CASCADE'), nullable=False, index=True)
    nombre_archivo = Column(String(255), nullable=False)
    tipo_mime = Column(String(100), nullable=False)
    tamaño_bytes = Column(BigInteger, nullable=False)
    url_storage = Column(String(500))
    ruta_storage = Column(String(500))
    created_at = Column(DateTime, default=func.now())
    
    # Relación muchos a uno con siniestro
    siniestro = relationship("Siniestro", back_populates="documentos")

# Función para generar número único de siniestro
def generar_numero_siniestro():
    """Genera un número único de siniestro con formato CLAIM-YYYYMMDD-XXXX."""
    from datetime import datetime
    import random
    
    fecha = datetime.now().strftime("%Y%m%d")
    numero_aleatorio = random.randint(1000, 9999)
    return f"CLAIM-{fecha}-{numero_aleatorio}"

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