from fastapi import Request, Response, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
import json
import os
import re
from datetime import datetime

# Importar servicios
from app.services.email_service import email_service
from app.services.llm_service import llm_service

# Importar funciones de base de datos
from app.core.database import get_db
from app.core import crud
from app.core.models import StatusEnum

async def email_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Endpoint para recibir webhooks de SendGrid sobre correos entrantes.
    
    Este endpoint procesa los emails recibidos y crea siniestros automáticamente
    basándose en el contenido del email.
    
    Args:
        request: Objeto de petición de FastAPI
        db: Sesión de base de datos inyectada por FastAPI
    """
    print("📧 Webhook de email recibido - Procesando siniestro...")
    
    try:
        # 1. Verificar la firma del webhook de SendGrid (muy importante para seguridad)
        signature = request.headers.get("X-Twilio-Email-Event-Webhook-Signature")
        timestamp = request.headers.get("X-Twilio-Email-Event-Webhook-Timestamp")
        
        # Obtener el cuerpo de la petición
        body = await request.body()
        payload = body.decode('utf-8')
        
        # Verificar firma (implementar según documentación de SendGrid)
        if not email_service.verify_webhook_signature(payload, signature or "", timestamp or ""):
            print("❌ Firma del webhook inválida")
            raise HTTPException(status_code=401, detail="Invalid signature")
        
        # 2. Parsear el cuerpo de la petición
        # SendGrid envía los datos como multipart/form-data
        form_data = await request.form()
        
        # Extraer información del email
        sender = form_data.get('from', '')
        recipient = form_data.get('to', '')
        subject = form_data.get('subject', '')
        body_text = form_data.get('text', '')
        body_html = form_data.get('html', '')
        
        print(f"📨 Email recibido de: {sender}")
        print(f"📋 Asunto: {subject}")
        print(f"📝 Contenido: {body_text[:200]}...")
        
        # 3. Extraer número de póliza del email usando IA
        policy_number = await extract_policy_number_from_email(subject, body_text)
        
        if not policy_number:
            print("❌ No se pudo extraer el número de póliza del email")
            # Registrar comunicación de error
            await log_error_communication(db, sender, subject, body_text, "No se pudo extraer número de póliza")
            return Response(
                content=json.dumps({
                    "status": "error",
                    "message": "No se pudo extraer el número de póliza del email"
                }),
                status_code=200,
                media_type="application/json"
            )
        
        print(f"🔍 Número de póliza extraído: {policy_number}")
        
        # 4. Buscar la póliza en la base de datos
        policy = crud.get_policy_by_number(db, policy_number)
        
        if not policy:
            print(f"❌ Póliza no encontrada: {policy_number}")
            # Registrar comunicación de error
            await log_error_communication(db, sender, subject, body_text, f"Póliza no encontrada: {policy_number}")
            return Response(
                content=json.dumps({
                    "status": "error",
                    "message": f"Póliza no encontrada: {policy_number}"
                }),
                status_code=200,
                media_type="application/json"
            )
        
        print(f"✅ Póliza encontrada: {policy.policy_number} - Cliente: {policy.customer_email}")
        
        # 5. Crear el siniestro
        claim = crud.create_claim(db, policy)
        print(f"✅ Siniestro creado: {claim.claim_number}")
        
        # 6. Generar resumen de IA del siniestro
        ai_summary = await generate_claim_summary(subject, body_text)
        if ai_summary:
            crud.update_claim_summary(db, claim.id, ai_summary)
            print(f"✅ Resumen de IA generado")
        
        # 7. Registrar la comunicación original
        communication = crud.log_communication(
            db=db,
            claim_id=claim.id,
            channel="EMAIL_INBOUND",
            content={
                "subject": subject,
                "body": body_text,
                "html_body": body_html,
                "original_sender": sender,
                "original_recipient": recipient
            },
            direction="inbound",
            sender=sender,
            recipient=recipient,
            subject=subject
        )
        print(f"✅ Comunicación registrada: ID {communication.id}")
        
        # 8. Enviar acuse de recibo al cliente
        email_sent = email_service.send_acknowledgement(
            to_email=sender,
            claim_number=claim.claim_number,
            customer_name=policy.customer_name
        )
        
        if email_sent:
            print(f"✅ Acuse de recibo enviado a {sender}")
            
            # Registrar la comunicación de salida
            crud.log_communication(
                db=db,
                claim_id=claim.id,
                channel="EMAIL_OUTBOUND",
                content={
                    "type": "acknowledgement",
                    "claim_number": claim.claim_number
                },
                direction="outbound",
                sender=email_service.from_email,
                recipient=sender,
                subject=f"Acuse de Recibo - Siniestro {claim.claim_number}"
            )
        else:
            print(f"❌ Error enviando acuse de recibo a {sender}")
        
        # 9. Respuesta exitosa
        return Response(
            content=json.dumps({
                "status": "success",
                "message": "Siniestro procesado exitosamente",
                "claim_number": claim.claim_number,
                "policy_number": policy.policy_number,
                "acknowledgement_sent": email_sent
            }),
            status_code=200,
            media_type="application/json"
        )
        
    except Exception as e:
        print(f"❌ Error procesando webhook de email: {str(e)}")
        # Aún devolvemos 200 para evitar que SendGrid reintente
        return Response(
            content=json.dumps({"status": "error", "message": str(e)}),
            status_code=200,
            media_type="application/json"
        )

async def extract_policy_number_from_email(subject: str, body: str) -> Optional[str]:
    """
    Extrae el número de póliza del email usando IA y regex.
    
    Args:
        subject: Asunto del email
        body: Cuerpo del email
        
        Returns:
            str: Número de póliza extraído, None si no se encuentra
    """
    # Primero intentar con regex para patrones comunes
    combined_text = f"{subject} {body}"
    
    # Patrones comunes de números de póliza
    patterns = [
        r'POL[IÍ]ZA[:\s]*([A-Z0-9\-]+)',  # PÓLIZA: ABC123
        r'POLICY[:\s]*([A-Z0-9\-]+)',     # POLICY: ABC123
        r'P[OÓ]L[:\s]*([A-Z0-9\-]+)',    # PÓL: ABC123
        r'([A-Z]{2,3}\d{3,8})',          # ABC123456
        r'(\d{3,8}[A-Z]{2,3})',          # 123456ABC
    ]
    
    for pattern in patterns:
        match = re.search(pattern, combined_text, re.IGNORECASE)
        if match:
            policy_number = match.group(1) if len(match.groups()) > 0 else match.group(0)
            print(f"🔍 Número de póliza encontrado con regex: {policy_number}")
            return policy_number.upper()
    
    # Si no se encuentra con regex, usar IA
    try:
        prompt = f"""
        Analiza el siguiente email y extrae el número de póliza de seguro.
        
        Asunto: {subject}
        Contenido: {body}
        
        Busca patrones como:
        - Números de póliza (ej: ABC123, 123456, POL-2024-001)
        - Referencias a pólizas de seguro
        - Cualquier identificador que parezca ser un número de póliza
        
        Responde SOLO con el número de póliza encontrado, sin texto adicional.
        Si no encuentras un número de póliza, responde con "NO_ENCONTRADO".
        """
        
        response = llm_service.get_response(prompt)
        
        if response and response.strip() != "NO_ENCONTRADO":
            policy_number = response.strip()
            print(f"🔍 Número de póliza encontrado con IA: {policy_number}")
            return policy_number.upper()
        
    except Exception as e:
        print(f"⚠️ Error usando IA para extraer número de póliza: {e}")
    
    return None

async def generate_claim_summary(subject: str, body: str) -> Optional[str]:
    """
    Genera un resumen del siniestro usando IA.
    
    Args:
        subject: Asunto del email
        body: Cuerpo del email
        
        Returns:
            str: Resumen generado por IA, None si hay error
    """
    try:
        prompt = f"""
        Analiza el siguiente email de notificación de siniestro y genera un resumen conciso.
        
        Asunto: {subject}
        Contenido: {body}
        
        El resumen debe incluir:
        - Tipo de incidente
        - Fecha del incidente (si se menciona)
        - Daños o pérdidas descritas
        - Monto estimado (si se menciona)
        - Información clave del cliente
        
        Responde con un resumen claro y estructurado.
        """
        
        summary = llm_service.get_response(prompt)
        return summary if summary else None
        
    except Exception as e:
        print(f"⚠️ Error generando resumen de IA: {e}")
        return None

async def log_error_communication(
    db: Session,
    sender: str,
    subject: str,
    body: str,
    error_message: str
):
    """
    Registra una comunicación de error cuando no se puede procesar un email.
    
    Args:
        db: Sesión de base de datos
        sender: Email del remitente
        subject: Asunto del email
        body: Cuerpo del email
        error_message: Mensaje de error
    """
    try:
        # Crear una comunicación sin claim_id para errores
        communication = crud.log_communication(
            db=db,
            claim_id=None,  # Sin claim asociado
            channel="EMAIL_INBOUND_ERROR",
            content={
                "subject": subject,
                "body": body,
                "error": error_message,
                "sender": sender
            },
            direction="inbound",
            sender=sender,
            subject=subject
        )
        print(f"📝 Error registrado: {communication.id}")
    except Exception as e:
        print(f"❌ Error registrando comunicación de error: {e}") 