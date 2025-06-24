#!/usr/bin/env python3
"""
Script Rápido de Prueba de Email
Para validaciones básicas del sistema de correo
"""

import os
from dotenv import load_dotenv
load_dotenv()
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime

def quick_email_test():
    """Prueba rápida de envío de email."""
    print("🚀 Prueba Rápida de Email - chiefdataaiofficer.com")
    print("=" * 50)
    
    # Configuración
    sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
    from_email = "gerardo_mayel_fernandez_alamilla@chiefdataaiofficer.com"
    to_email = "geramfernandez@gmail.com"
    
    if not sendgrid_api_key:
        print("❌ Error: SENDGRID_API_KEY no está configurada")
        print("   Configura la variable de entorno o crea un archivo .env")
        return False
    
    try:
        # Crear cliente SendGrid
        sg = SendGridAPIClient(api_key=sendgrid_api_key)
        
        # Crear mensaje
        subject = f"Prueba Rápida - {datetime.now().strftime('%H:%M:%S')}"
        content = f"""
Hola,

Esta es una prueba rápida del sistema de email de chiefdataaiofficer.com.

**Detalles:**
- Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
- Desde: {from_email}
- Hacia: {to_email}
- Servicio: SendGrid

Si recibes este email, el sistema está funcionando correctamente.

Saludos,
Sistema de Pruebas
        """.strip()
        
        message = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject=subject,
            plain_text_content=content
        )
        
        # Enviar email
        print("📧 Enviando email de prueba...")
        response = sg.send(message)
        
        if response.status_code == 202:
            print("✅ Email enviado exitosamente!")
            print(f"   Status: {response.status_code}")
            print(f"   Asunto: {subject}")
            print(f"   Destinatario: {to_email}")
            return True
        else:
            print(f"❌ Error en el envío. Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = quick_email_test()
    if success:
        print("\n🎉 ¡Prueba completada exitosamente!")
        print("   Revisa tu bandeja de entrada en geramfernandez@gmail.com")
    else:
        print("\n❌ La prueba falló. Revisa la configuración.") 