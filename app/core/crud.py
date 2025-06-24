from sqlalchemy.orm import Session
from sqlalchemy import and_, desc, func
from typing import List, Optional, Dict, Any
from datetime import datetime
import random

from app.core.models import Conversation, User, EmailMessage, Policy, Coverage, Claim, Document, ClaimForm, Communication, StatusEnum
from app.core.database import Base

# ============================================================================
# OPERACIONES CRUD PARA CONVERSACIONES
# ============================================================================

def get_conversation_by_user(
    db: Session, 
    user_identifier: str, 
    channel: str = "email"
) -> Optional[Conversation]:
    """
    Obtiene una conversación activa para un usuario específico.
    
    Args:
        db: Sesión de la base de datos
        user_identifier: Identificador del usuario (email)
        channel: Canal de comunicación ('email' o 'chat')
        
    Returns:
        Conversation: Objeto de conversación si existe, None en caso contrario
    """
    return db.query(Conversation).filter(
        and_(
            Conversation.user_identifier == user_identifier,
            Conversation.channel == channel,
            Conversation.is_active == True
        )
    ).first()

def create_conversation(
    db: Session,
    user_identifier: str,
    channel: str = "email",
    initial_history: Optional[List[Dict[str, Any]]] = None
) -> Conversation:
    """
    Crea una nueva conversación para un usuario.
    
    Args:
        db: Sesión de la base de datos
        user_identifier: Identificador del usuario (email)
        channel: Canal de comunicación ('email' o 'chat')
        initial_history: Historial inicial de la conversación
        
    Returns:
        Conversation: Objeto de conversación creado
    """
    conversation = Conversation(
        user_identifier=user_identifier,
        channel=channel,
        history=initial_history or []
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

def update_conversation_history(
    db: Session,
    conversation_id: int,
    new_messages: List[Dict[str, Any]]
) -> Optional[Conversation]:
    """
    Actualiza el historial de una conversación existente.
    
    Args:
        db: Sesión de la base de datos
        conversation_id: ID de la conversación
        new_messages: Lista de nuevos mensajes a añadir
        
    Returns:
        Conversation: Objeto de conversación actualizado, None si no existe
    """
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id
    ).first()
    
    if conversation:
        # Añadir nuevos mensajes al historial existente
        conversation.history.extend(new_messages)
        conversation.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(conversation)
    
    return conversation

def get_or_create_conversation(
    db: Session,
    user_identifier: str,
    channel: str = "email"
) -> Conversation:
    """
    Obtiene una conversación existente o crea una nueva si no existe.
    
    Args:
        db: Sesión de la base de datos
        user_identifier: Identificador del usuario (email)
        channel: Canal de comunicación ('email' o 'chat')
        
    Returns:
        Conversation: Objeto de conversación
    """
    conversation = get_conversation_by_user(db, user_identifier, channel)
    if not conversation:
        conversation = create_conversation(db, user_identifier, channel)
    return conversation

def get_conversations_by_user(
    db: Session,
    user_identifier: str,
    limit: int = 10
) -> List[Conversation]:
    """
    Obtiene todas las conversaciones de un usuario.
    
    Args:
        db: Sesión de la base de datos
        user_identifier: Identificador del usuario (email)
        limit: Número máximo de conversaciones a retornar
        
    Returns:
        List[Conversation]: Lista de conversaciones
    """
    return db.query(Conversation).filter(
        Conversation.user_identifier == user_identifier
    ).order_by(desc(Conversation.updated_at)).limit(limit).all()

def deactivate_conversation(
    db: Session,
    conversation_id: int
) -> bool:
    """
    Desactiva una conversación (marca como inactiva).
    
    Args:
        db: Sesión de la base de datos
        conversation_id: ID de la conversación
        
    Returns:
        bool: True si se desactivó correctamente, False en caso contrario
    """
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id
    ).first()
    
    if conversation:
        conversation.is_active = False
        conversation.updated_at = datetime.utcnow()
        db.commit()
        return True
    return False

# ============================================================================
# OPERACIONES CRUD PARA USUARIOS
# ============================================================================

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Obtiene un usuario por su nombre de usuario."""
    return db.query(User).filter(User.username == username).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Obtiene un usuario por su ID."""
    return db.query(User).filter(User.id == user_id).first()

def create_user(
    db: Session,
    username: str,
    hashed_password: str,
    role: str = "analyst"
) -> User:
    """Crea un nuevo usuario."""
    user = User(
        username=username,
        hashed_password=hashed_password,
        role=role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(
    db: Session,
    user_id: int,
    **kwargs
) -> Optional[User]:
    """Actualiza la información de un usuario."""
    user = get_user_by_id(db, user_id)
    if user:
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
    return user

# ============================================================================
# OPERACIONES CRUD PARA PÓLIZAS
# ============================================================================

def get_policy_by_number(db: Session, policy_number: str) -> Optional[Policy]:
    """Obtiene una póliza por su número."""
    return db.query(Policy).filter(Policy.policy_number == policy_number).first()

def get_policy_by_id(db: Session, policy_id: int) -> Optional[Policy]:
    """Obtiene una póliza por su ID."""
    return db.query(Policy).filter(Policy.id == policy_id).first()

def get_policies_by_customer_email(db: Session, customer_email: str) -> List[Policy]:
    """Obtiene todas las pólizas de un cliente."""
    return db.query(Policy).filter(Policy.customer_email == customer_email).all()

def create_policy(
    db: Session,
    policy_number: str,
    customer_email: str,
    customer_name: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> Policy:
    """Crea una nueva póliza."""
    policy = Policy(
        policy_number=policy_number,
        customer_email=customer_email,
        customer_name=customer_name,
        start_date=start_date,
        end_date=end_date
    )
    db.add(policy)
    db.commit()
    db.refresh(policy)
    return policy

def update_policy(
    db: Session,
    policy_id: int,
    **kwargs
) -> Optional[Policy]:
    """Actualiza la información de una póliza."""
    policy = get_policy_by_id(db, policy_id)
    if policy:
        for key, value in kwargs.items():
            if hasattr(policy, key):
                setattr(policy, key, value)
        policy.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(policy)
    return policy

# ============================================================================
# OPERACIONES CRUD PARA COBERTURAS
# ============================================================================

def get_coverages_by_policy(db: Session, policy_id: int) -> List[Coverage]:
    """Obtiene todas las coberturas de una póliza."""
    return db.query(Coverage).filter(Coverage.policy_id == policy_id).all()

def create_coverage(
    db: Session,
    policy_id: int,
    coverage_type: str,
    limit_amount: Optional[float] = None,
    deductible: Optional[float] = None,
    description: Optional[str] = None
) -> Coverage:
    """Crea una nueva cobertura."""
    coverage = Coverage(
        policy_id=policy_id,
        coverage_type=coverage_type,
        limit_amount=limit_amount,
        deductible=deductible,
        description=description
    )
    db.add(coverage)
    db.commit()
    db.refresh(coverage)
    return coverage

# ============================================================================
# OPERACIONES CRUD PARA SINIESTROS (CLAIMS)
# ============================================================================

def get_claim_by_number(db: Session, claim_number: str) -> Optional[Claim]:
    """Obtiene un siniestro por su número."""
    return db.query(Claim).filter(Claim.claim_number == claim_number).first()

def get_claim_by_id(db: Session, claim_id: int) -> Optional[Claim]:
    """Obtiene un siniestro por su ID."""
    return db.query(Claim).filter(Claim.id == claim_id).first()

def get_claims_by_policy(db: Session, policy_id: int, limit: int = 50) -> List[Claim]:
    """Obtiene todos los siniestros de una póliza."""
    return db.query(Claim).filter(
        Claim.policy_id == policy_id
    ).order_by(desc(Claim.opened_at)).limit(limit).all()

def get_claims_by_status(db: Session, status: StatusEnum, limit: int = 50) -> List[Claim]:
    """Obtiene todos los siniestros con un estado específico."""
    return db.query(Claim).filter(
        Claim.status == status
    ).order_by(desc(Claim.opened_at)).limit(limit).all()

def get_claims_by_analyst(db: Session, analyst_id: int, limit: int = 50) -> List[Claim]:
    """Obtiene todos los siniestros asignados a un analista."""
    return db.query(Claim).filter(
        Claim.assigned_to_id == analyst_id
    ).order_by(desc(Claim.opened_at)).limit(limit).all()

def create_claim(db: Session, policy: Policy) -> Claim:
    """
    Crea un nuevo siniestro para una póliza.
    Genera automáticamente un número único de siniestro.
    """
    # Generar número único de siniestro
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_part = random.randint(100, 999)
    claim_number = f"CLAIM-{timestamp}-{random_part}"
    
    # Verificar que el número no exista (muy improbable, pero por seguridad)
    while get_claim_by_number(db, claim_number):
        random_part = random.randint(100, 999)
        claim_number = f"CLAIM-{timestamp}-{random_part}"
    
    new_claim = Claim(
        claim_number=claim_number,
        policy_id=policy.id,
        status=StatusEnum.OPEN_NOTIFIED
    )
    db.add(new_claim)
    db.commit()
    db.refresh(new_claim)
    return new_claim

def update_claim_status(
    db: Session,
    claim_id: int,
    status: StatusEnum,
    assigned_to_id: Optional[int] = None
) -> Optional[Claim]:
    """Actualiza el estado de un siniestro."""
    claim = get_claim_by_id(db, claim_id)
    if claim:
        claim.status = status
        if assigned_to_id:
            claim.assigned_to_id = assigned_to_id
        claim.updated_at = datetime.utcnow()
        
        # Si el estado es de cierre, establecer closed_at
        if status in [StatusEnum.CLOSED_PAID, StatusEnum.CLOSED_REJECTED]:
            claim.closed_at = datetime.utcnow()
        
        db.commit()
        db.refresh(claim)
    return claim

def update_claim_summary(
    db: Session,
    claim_id: int,
    summary_ai: str
) -> Optional[Claim]:
    """Actualiza el resumen de IA de un siniestro."""
    claim = get_claim_by_id(db, claim_id)
    if claim:
        claim.summary_ai = summary_ai
        claim.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(claim)
    return claim

def assign_claim_to_analyst(
    db: Session,
    claim_id: int,
    analyst_id: int
) -> Optional[Claim]:
    """Asigna un siniestro a un analista."""
    claim = get_claim_by_id(db, claim_id)
    if claim:
        claim.assigned_to_id = analyst_id
        claim.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(claim)
    return claim

# ============================================================================
# OPERACIONES CRUD PARA DOCUMENTOS
# ============================================================================

def get_documents_by_claim(db: Session, claim_id: int) -> List[Document]:
    """Obtiene todos los documentos de un siniestro."""
    return db.query(Document).filter(Document.claim_id == claim_id).all()

def create_document(
    db: Session,
    claim_id: int,
    file_name: str,
    storage_url: str,
    document_type: Optional[str] = None,
    file_size: Optional[int] = None,
    mime_type: Optional[str] = None
) -> Document:
    """Crea un nuevo documento."""
    document = Document(
        claim_id=claim_id,
        file_name=file_name,
        storage_url=storage_url,
        document_type=document_type,
        file_size=file_size,
        mime_type=mime_type
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document

# ============================================================================
# OPERACIONES CRUD PARA FORMULARIOS
# ============================================================================

def get_claim_forms_by_claim(db: Session, claim_id: int) -> List[ClaimForm]:
    """Obtiene todos los formularios de un siniestro."""
    return db.query(ClaimForm).filter(ClaimForm.claim_id == claim_id).all()

def create_claim_form(
    db: Session,
    claim_id: int,
    submission_type: str,
    form_data: Dict[str, Any]
) -> ClaimForm:
    """Crea un nuevo formulario de siniestro."""
    claim_form = ClaimForm(
        claim_id=claim_id,
        submission_type=submission_type,
        form_data=form_data
    )
    db.add(claim_form)
    db.commit()
    db.refresh(claim_form)
    return claim_form

# ============================================================================
# OPERACIONES CRUD PARA COMUNICACIONES
# ============================================================================

def get_communications_by_claim(db: Session, claim_id: int, limit: int = 100) -> List[Communication]:
    """Obtiene todas las comunicaciones de un siniestro."""
    return db.query(Communication).filter(
        Communication.claim_id == claim_id
    ).order_by(desc(Communication.timestamp)).limit(limit).all()

def log_communication(
    db: Session,
    claim_id: int,
    channel: str,
    content: Dict[str, Any],
    direction: str = "inbound",
    sender: Optional[str] = None,
    recipient: Optional[str] = None,
    subject: Optional[str] = None
) -> Communication:
    """Registra una nueva comunicación."""
    communication = Communication(
        claim_id=claim_id,
        channel=channel,
        content=content,
        direction=direction,
        sender=sender,
        recipient=recipient,
        subject=subject
    )
    db.add(communication)
    db.commit()
    db.refresh(communication)
    return communication

# ============================================================================
# FUNCIONES DE UTILIDAD Y ESTADÍSTICAS
# ============================================================================

def get_claim_stats(db: Session) -> Dict[str, int]:
    """Obtiene estadísticas generales de siniestros."""
    total_claims = db.query(Claim).count()
    open_claims = db.query(Claim).filter(
        Claim.status.in_([
            StatusEnum.OPEN_NOTIFIED,
            StatusEnum.PENDING_CUSTOMER_DOCUMENTS,
            StatusEnum.UNDER_AI_REVIEW,
            StatusEnum.PENDING_ANALYST_REVIEW,
            StatusEnum.ADDITIONAL_INFO_REQUESTED
        ])
    ).count()
    closed_claims = db.query(Claim).filter(
        Claim.status.in_([
            StatusEnum.CLOSED_PAID,
            StatusEnum.CLOSED_REJECTED
        ])
    ).count()
    
    return {
        "total_claims": total_claims,
        "open_claims": open_claims,
        "closed_claims": closed_claims
    }

def get_claims_by_date_range(
    db: Session,
    start_date: datetime,
    end_date: datetime
) -> List[Claim]:
    """Obtiene siniestros en un rango de fechas."""
    return db.query(Claim).filter(
        and_(
            Claim.opened_at >= start_date,
            Claim.opened_at <= end_date
        )
    ).order_by(desc(Claim.opened_at)).all()

def search_claims(
    db: Session,
    policy_number: Optional[str] = None,
    customer_email: Optional[str] = None,
    claim_number: Optional[str] = None,
    status: Optional[StatusEnum] = None,
    limit: int = 50
) -> List[Claim]:
    """Búsqueda avanzada de siniestros."""
    query = db.query(Claim).join(Policy)
    
    if policy_number:
        query = query.filter(Policy.policy_number.ilike(f"%{policy_number}%"))
    
    if customer_email:
        query = query.filter(Policy.customer_email.ilike(f"%{customer_email}%"))
    
    if claim_number:
        query = query.filter(Claim.claim_number.ilike(f"%{claim_number}%"))
    
    if status:
        query = query.filter(Claim.status == status)
    
    return query.order_by(desc(Claim.opened_at)).limit(limit).all()

def get_conversation_stats(db: Session, user_identifier: str) -> Dict[str, int]:
    """
    Obtiene estadísticas de conversaciones para un usuario.
    
    Args:
        db: Sesión de la base de datos
        user_identifier: Identificador del usuario
        
    Returns:
        Dict[str, int]: Estadísticas de conversaciones
    """
    total_conversations = db.query(Conversation).filter(
        Conversation.user_identifier == user_identifier
    ).count()
    
    active_conversations = db.query(Conversation).filter(
        and_(
            Conversation.user_identifier == user_identifier,
            Conversation.is_active == True
        )
    ).count()
    
    total_messages = db.query(EmailMessage).join(Conversation).filter(
        Conversation.user_identifier == user_identifier
    ).count()
    
    return {
        "total_conversations": total_conversations,
        "active_conversations": active_conversations,
        "total_messages": total_messages
    } 