from fastapi import Request, Response, HTTPException, APIRouter, Form, File, UploadFile, Header
from typing import Dict, Any, List, Optional
import json
import os
from datetime import datetime
from dotenv import load_dotenv
import base64
import hmac
import hashlib

load_dotenv()

router = APIRouter()

def verify_resend_signature(request_body: bytes, signature: str) -> bool:
    """
    Verifica que el webhook viene realmente de Resend usando el signing secret.
    """
    webhook_secret = os.getenv('RESEND_WEBHOOK_SECRET')
    
    if not webhook_secret or webhook_secret == 'your_resend_webhook_secret_here':
        print("⚠️ RESEND_WEBHOOK_SECRET no configurado, saltando verificación")
        return True
    
    try:
        # Crear el hash esperado
        expected_signature = hmac.new(
            webhook_secret.encode('utf-8'),
            request_body,
            hashlib.sha256
        ).hexdigest()
        
        # Comparar con la firma recibida
        return hmac.compare_digest(f"sha256={expected_signature}", signature)
        
    except Exception as e:
        print(f"❌ Error verificando firma: {e}")
        return False

@router.post("/webhook/email")
async def email_webhook(
    request: Request,
    from_email: str = Form(...),
    to_email: str = Form(...),
    subject: str = Form(default="Sin asunto"),
    text: Optional[str] = Form(default=None),
    html: Optional[str] = Form(default=None),
    attachments: Optional[List[UploadFile]] = File(default=[]),
    resend_signature: Optional[str] = Header(None, alias="resend-signature")
):
    """
    Webhook para recibir emails de Resend en formato multipart/form-data.
    Procesa el email y extrae toda la información relevante.
    """
    try:
        print("\n" + "="*80)
        print("📧 EMAIL RECIBIDO - " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        print("="*80)
        
        # Verificar firma de Resend
        if resend_signature:
            body = await request.body()
            if not verify_resend_signature(body, resend_signature):
                print("❌ Firma de Resend inválida - posible ataque")
                raise HTTPException(status_code=401, detail="Invalid signature")
            print("✅ Firma de Resend verificada")
        else:
            print("⚠️ No se recibió firma de Resend (prueba local)")
        
        # Imprimir información básica del email
        print(f"\n📋 INFORMACIÓN BÁSICA:")
        print(f"   De: {from_email}")
        print(f"   Para: {to_email}")
        print(f"   Asunto: {subject}")
        print(f"   Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        # Imprimir contenido del email
        print(f"\n📝 CONTENIDO DEL EMAIL:")
        
        # Texto plano
        if text:
            print(f"\n   📄 TEXTO PLANO:")
            print(f"   {text}")
        
        # HTML
        if html:
            print(f"\n   🌐 HTML:")
            print(f"   {html}")
        
        # Adjuntos
        if attachments:
            print(f"\n   📎 ADJUNTOS ({len(attachments)} archivos):")
            for i, attachment in enumerate(attachments, 1):
                print(f"\n   📎 Adjunto {i}:")
                print(f"      Nombre: {attachment.filename}")
                print(f"      Tipo: {attachment.content_type}")
                
                # Leer el contenido del archivo
                content = await attachment.read()
                print(f"      Tamaño: {len(content)} bytes")
                
                # Si es una imagen, mostrar información adicional
                if attachment.content_type and attachment.content_type.startswith('image/'):
                    print(f"      ✅ Es una imagen")
                    print(f"      📊 Datos: {len(content)} bytes")
                    print(f"      🔍 Primeros 50 bytes: {content[:50]}")
        
        # Imprimir headers para debugging
        print(f"\n🔍 HEADERS DEL REQUEST:")
        for header, value in request.headers.items():
            if header.lower() in ['content-type', 'content-length', 'user-agent', 'x-forwarded-for', 'resend-signature']:
                print(f"   {header}: {value}")
        
        # Intentar obtener datos adicionales del body raw para debugging
        try:
            body = await request.body()
            print(f"\n🔍 DATOS RAW DEL REQUEST:")
            print(f"   Tamaño del body: {len(body)} bytes")
            print(f"   Content-Type: {request.headers.get('content-type', 'No disponible')}")
            
            # Mostrar los primeros bytes del body para debugging
            if body:
                print(f"   Primeros 200 bytes del body:")
                print(f"   {body[:200]}")
                
        except Exception as body_error:
            print(f"   ⚠️ Error leyendo body: {body_error}")
        
        print("\n" + "="*80)
        print("✅ EMAIL PROCESADO - FIN")
        print("="*80 + "\n")
        
        # Responder con éxito
        return {
            "status": "success",
            "message": "Email recibido y procesado",
            "timestamp": datetime.now().isoformat(),
            "from": from_email,
            "to": to_email,
            "subject": subject
        }
        
    except Exception as e:
        print(f"\n❌ ERROR PROCESANDO WEBHOOK: {str(e)}")
        print("="*80 + "\n")
        
        # Intentar obtener más información del error
        try:
            body = await request.body()
            print(f"Body recibido: {len(body)} bytes")
            print(f"Headers: {dict(request.headers)}")
        except:
            pass
        
        raise HTTPException(
            status_code=500,
            detail=f"Error procesando webhook: {str(e)}"
        )

@router.get("/webhook/email")
async def webhook_status():
    """Endpoint para verificar que el webhook está funcionando."""
    return {
        "status": "ok",
        "message": "Email webhook está funcionando",
        "timestamp": datetime.now().isoformat()
    } 