#!/usr/bin/env python3
"""
Script para probar el servicio de email actualizado con Resend
"""

import os
import sys
from dotenv import load_dotenv
load_dotenv()

# Agregar el directorio app al path
sys.path.append('app')

from services.email_service import EmailService

def test_email_service():
    """Prueba el servicio de email actualizado."""
    print("🧪 Probando Servicio de Email Actualizado")
    print("=" * 50)
    
    # Crear instancia del servicio
    email_service = EmailService()
    
    # Verificar configuración
    print(f"🔑 API Key configurada: {'✅' if email_service.api_key else '❌'}")
    print(f"📧 Email remitente: {email_service.from_email}")
    
    if not email_service.api_key:
        print("❌ RESEND_API_KEY no está configurada")
        return False
    
    # Probar envío de email
    to_email = "geramfernandez@gmail.com"
    subject = "Prueba Servicio Email Actualizado"
    content = """
Hola,

Este es un email de prueba del servicio de email actualizado para usar Resend.

**Detalles:**
- Servicio: Resend
- Dominio: chiefdataaiofficer.com
- Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

El servicio está funcionando correctamente.

Saludos,
Sistema de Pruebas
    """.strip()
    
    print(f"\n📧 Enviando email de prueba...")
    print(f"   Destinatario: {to_email}")
    print(f"   Asunto: {subject}")
    
    success = email_service.send_email(to_email, subject, content)
    
    if success:
        print("\n✅ Servicio de email funcionando correctamente!")
        return True
    else:
        print("\n❌ Error en el servicio de email")
        return False

if __name__ == "__main__":
    from datetime import datetime
    success = test_email_service()
    if success:
        print("\n🎉 ¡Prueba completada exitosamente!")
    else:
        print("\n❌ La prueba falló.") 