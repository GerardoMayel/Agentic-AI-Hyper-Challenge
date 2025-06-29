#!/usr/bin/env python3
"""
Script para enviar un email de prueba con PDF para probar el sistema de claims.
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import base64

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

def crear_pdf_prueba():
    """Crea un PDF de prueba simple."""
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from io import BytesIO
    
    # Crear PDF en memoria
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Agregar contenido
    p.drawString(100, 750, "REPORTE DE SINIESTRO DE PRUEBA")
    p.drawString(100, 720, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    p.drawString(100, 690, "Este es un documento de prueba para el sistema de claims.")
    p.drawString(100, 660, "Contiene información simulada de un siniestro.")
    p.drawString(100, 630, "Archivo generado automáticamente para pruebas.")
    
    p.save()
    buffer.seek(0)
    return buffer.getvalue()

def enviar_email_prueba():
    """Envía un email de prueba con PDF."""
    try:
        print("📧 Enviando email de prueba...")
        
        # Crear PDF de prueba
        pdf_content = crear_pdf_prueba()
        print("✅ PDF de prueba creado")
        
        # Inicializar servicio Gmail
        from app.services.gmail_service import GmailService
        gmail_service = GmailService()
        
        # Obtener información del usuario autenticado
        profile = gmail_service.service.users().getProfile(userId='me').execute()
        user_email = profile['emailAddress']
        print(f"📧 Usuario autenticado: {user_email}")
        
        # Configurar email
        to_email = user_email  # Enviar a nosotros mismos
        subject = f"TEST CLAIMS - {datetime.now().strftime('%Y%m%d_%H%M%S')}"
        body = f"""
        Este es un email de prueba para el sistema de claims.
        
        Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        Contenido: claim-test-body
        
        Este email contiene un PDF adjunto para probar el procesamiento.
        """
        
        # Enviar email con adjunto
        resultado = gmail_service.enviar_email_con_adjunto(
            to_email=to_email,
            subject=subject,
            body=body,
            adjunto_nombre="Reporte_Siniestro_Prueba.pdf",
            adjunto_contenido=pdf_content,
            adjunto_tipo="application/pdf"
        )
        
        if resultado:
            print("✅ Email de prueba enviado exitosamente")
            print(f"   Asunto: {subject}")
            print(f"   Destinatario: {to_email}")
            print(f"   PDF adjunto: Reporte_Siniestro_Prueba.pdf")
            return True
        else:
            print("❌ Error enviando email de prueba")
            return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal."""
    print("🚀 ENVIADOR DE EMAIL DE PRUEBA")
    print("=" * 50)
    
    # Preguntar confirmación
    confirmacion = input("¿Deseas enviar un email de prueba? (y/N): ").strip().lower()
    
    if confirmacion in ['y', 'yes', 'sí', 'si']:
        if enviar_email_prueba():
            print("\n🎉 ¡Email de prueba enviado!")
            print("   Ahora puedes ejecutar: python procesar_email_prueba.py")
        else:
            print("\n❌ Error enviando email de prueba")
    else:
        print("\n⚠️ Operación cancelada.")

if __name__ == "__main__":
    main() 