#!/usr/bin/env python3
"""
Script simple para procesar el email de prueba con PDF.
Crea siniestro y almacena documento en Google Cloud Storage.
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Leer directamente el archivo .env y establecer DATABASE_URL
env_path = os.path.abspath('.env')
with open(env_path, 'r') as f:
    for line in f:
        if line.startswith('DATABASE_URL='):
            db_url = line.split('=', 1)[1].strip()
            os.environ['DATABASE_URL'] = db_url
            break

load_dotenv()

from app.services.gmail_service import GmailService
from app.services.gcs_storage import gcs_storage
from app.core.database import get_db
from app.core.models import Siniestro, Documento, generar_numero_siniestro

def procesar_email_prueba():
    """Procesa el email de prueba con PDF."""
    try:
        print("🔍 Buscando email de prueba con PDF...")
        
        # Inicializar servicios
        gmail_service = GmailService()
        storage_service = gcs_storage
        
        # Buscar emails con palabras clave de claims
        emails = gmail_service.buscar_emails_claims(max_results=5)
        
        if not emails:
            print("❌ No se encontraron emails con palabras clave de claims")
            return
        
        print(f"📧 Encontrados {len(emails)} emails")
        
        # Procesar el primer email que tenga adjuntos
        for i, email in enumerate(emails):
            print(f"\n📧 Procesando email {i+1}: {email.get('subject', 'Sin asunto')}")
            
            # Verificar si ya fue procesado
            db = next(get_db())
            email_existente = db.query(Siniestro).filter(
                Siniestro.gmail_message_id == email['id']
            ).first()
            
            if email_existente:
                print(f"⚠️ Email ya procesado anteriormente (Siniestro: {email_existente.numero_siniestro})")
                db.close()
                continue
            
            db.close()
            
            # Verificar si tiene adjuntos
            attachments = email.get('attachments', [])
            if not attachments:
                print("⚠️ Email sin adjuntos, continuando...")
                continue
            
            print(f"📎 Encontrados {len(attachments)} adjuntos")
            
            # Procesar este email
            resultado = procesar_email_completo(email, gmail_service, storage_service)
            
            if resultado['status'] == 'success':
                print("✅ Email procesado exitosamente")
                return resultado
            else:
                print(f"❌ Error: {resultado.get('message', 'Error desconocido')}")
        
        print("❌ No se encontró un email válido para procesar")
        
    except Exception as e:
        print(f"❌ Error en procesamiento: {e}")
        return {'status': 'error', 'message': str(e)}

def procesar_email_completo(email_data, gmail_service, storage_service):
    """Procesa un email completo."""
    try:
        # Extraer información básica
        email_id = email_data['id']
        subject = email_data.get('subject', 'Sin asunto')
        from_header = email_data.get('from', '')
        text_content = email_data.get('text_content', '')
        attachments = email_data.get('attachments', [])
        
        print(f"📧 Email ID: {email_id}")
        print(f"📧 Asunto: {subject}")
        print(f"📧 Remitente: {from_header}")
        print(f"📧 Contenido: {text_content[:100]}...")
        
        # Generar número de siniestro
        numero_siniestro = generar_numero_siniestro()
        print(f"🚨 Número de siniestro generado: {numero_siniestro}")
        
        # Crear siniestro en base de datos
        db = next(get_db())
        
        # Extraer email del remitente
        remitente_email = from_header
        if '<' in from_header and '>' in from_header:
            remitente_email = from_header.split('<')[1].split('>')[0]
        
        siniestro = Siniestro(
            numero_siniestro=numero_siniestro,
            gmail_message_id=email_id,
            remitente_email=remitente_email,
            remitente_nombre=from_header.split('<')[0].strip() if '<' in from_header else None,
            subject=subject,
            contenido_texto=text_content,
            fecha_reporte=datetime.now()
        )
        
        db.add(siniestro)
        db.commit()
        db.refresh(siniestro)
        
        print(f"✅ Siniestro creado en BD: {siniestro.id}")
        
        # Procesar adjuntos
        documentos_procesados = []
        for attachment in attachments:
            resultado_doc = procesar_adjunto(
                email_id, 
                attachment, 
                numero_siniestro,
                siniestro.id,
                gmail_service, 
                storage_service,
                db
            )
            if resultado_doc:
                documentos_procesados.append(resultado_doc)
        
        print(f"\n📊 RESUMEN DEL PROCESAMIENTO:")
        print(f"   Email ID: {email_id}")
        print(f"   Siniestro: {numero_siniestro}")
        print(f"   Documentos procesados: {len(documentos_procesados)}")
        
        db.close()
        
        return {
            'status': 'success',
            'numero_siniestro': numero_siniestro,
            'documentos_procesados': documentos_procesados
        }
        
    except Exception as e:
        print(f"❌ Error procesando email: {e}")
        return {'status': 'error', 'message': str(e)}

def procesar_adjunto(email_id, attachment, numero_siniestro, siniestro_id, gmail_service, storage_service, db):
    """Procesa un adjunto individual."""
    try:
        filename = attachment['filename']
        mime_type = attachment['mime_type']
        size = attachment['size']
        attachment_id = attachment['attachment_id']
        
        print(f"\n📎 Procesando adjunto: {filename}")
        print(f"   Tipo: {mime_type}")
        print(f"   Tamaño: {size} bytes")
        
        # Descargar adjunto de Gmail
        adjunto_data = gmail_service.descargar_adjunto(email_id, attachment_id)
        
        if not adjunto_data:
            print(f"❌ Error descargando adjunto: {filename}")
            return None
        
        # Subir a Google Cloud Storage
        url_storage = storage_service.upload_file(
            file_content=adjunto_data['content'],
            filename=filename,
            numero_siniestro=numero_siniestro,
            email_id=email_id,
            content_type=mime_type
        )
        
        if url_storage:
            print(f"✅ Documento subido exitosamente")
            print(f"   URL: {url_storage}")
            
            # Crear registro en base de datos
            documento = Documento(
                siniestro_id=siniestro_id,
                nombre_archivo=filename,
                tipo_mime=mime_type,
                tamaño_bytes=size,
                url_storage=url_storage,
                ruta_storage=f"{numero_siniestro}/email-{email_id}/{filename}"
            )
            
            db.add(documento)
            db.commit()
            
            print(f"✅ Documento registrado en BD: {documento.id}")
            
            return {
                'filename': filename,
                'url_storage': url_storage
            }
        else:
            print(f"❌ Error subiendo documento: {filename}")
            return None
            
    except Exception as e:
        print(f"❌ Error procesando adjunto {filename}: {e}")
        return None

def main():
    """Función principal."""
    print("🚀 PROCESADOR DE EMAIL DE PRUEBA")
    print("=" * 50)
    
    resultado = procesar_email_prueba()
    
    if resultado and resultado.get('status') == 'success':
        print("\n🎉 ¡Email procesado exitosamente!")
        print(f"   Siniestro: {resultado.get('numero_siniestro')}")
        print(f"   Documentos: {len(resultado.get('documentos_procesados', []))}")
    else:
        print("\n❌ Error procesando email")

if __name__ == "__main__":
    main() 