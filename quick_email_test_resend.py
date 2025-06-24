#!/usr/bin/env python3
"""
Script Rápido de Prueba de Email con Resend
Para validaciones básicas del sistema de correo
"""

import os
from dotenv import load_dotenv
load_dotenv()
import resend
from datetime import datetime

def quick_email_test_resend():
    """Prueba rápida de envío de email usando Resend."""
    print("🚀 Prueba Rápida de Email - chiefdataaiofficer.com (Resend)")
    print("=" * 60)
    
    # Configuración
    resend_api_key = os.getenv("RESEND_API_KEY")
    from_email = "gerardo_mayel_fernandez_alamilla@chiefdataaiofficer.com"
    to_email = "geramfernandez@gmail.com"
    
    if not resend_api_key:
        print("❌ Error: RESEND_API_KEY no está configurada")
        print("   Configura la variable de entorno RESEND_API_KEY en tu archivo .env")
        return False
    
    try:
        # Configurar Resend
        resend.api_key = resend_api_key
        
        # Crear mensaje
        subject = f"Prueba Rápida Resend - {datetime.now().strftime('%H:%M:%S')}"
        content = f"""
Hola,

Esta es una prueba rápida del sistema de email de chiefdataaiofficer.com usando Resend.

**Detalles:**
- Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
- Desde: {from_email}
- Hacia: {to_email}
- Servicio: Resend
- Dominio: chiefdataaiofficer.com

Si recibes este email, el sistema está funcionando correctamente.

Saludos,
Sistema de Pruebas
        """.strip()
        
        # Enviar email
        print("📧 Enviando email de prueba con Resend...")
        response = resend.Emails.send({
            "from": from_email,
            "to": to_email,
            "subject": subject,
            "text": content
        })
        
        print("✅ Email enviado exitosamente!")
        print(f"   Asunto: {subject}")
        print(f"   Destinatario: {to_email}")
        print(f"   Servicio: Resend")
        print(f"   Respuesta: {response}")
        return True
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = quick_email_test_resend()
    if success:
        print("\n🎉 ¡Prueba completada exitosamente!")
        print("   Revisa tu bandeja de entrada en geramfernandez@gmail.com")
    else:
        print("\n❌ La prueba falló. Revisa la configuración.") 