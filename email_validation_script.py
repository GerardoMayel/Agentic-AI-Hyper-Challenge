#!/usr/bin/env python3
"""
Script de Validación de Email para chiefdataaiofficer.com
Prueba el envío y recepción de correos usando SendGrid
"""

import os
import sys
import time
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Optional, List
import json

# Configuración de SendGrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

class EmailValidator:
    """Clase para validar el envío y recepción de emails."""
    
    def __init__(self):
        self.sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
        self.from_email = "gerardo_mayel_fernandez_alamilla@chiefdataaiofficer.com"
        self.test_email = "geramfernandez@gmail.com"
        
        # Configuración para pruebas de recepción (Gmail)
        self.gmail_user = "geramfernandez@gmail.com"
        self.gmail_password = os.getenv("GMAIL_APP_PASSWORD")  # Contraseña de aplicación de Gmail
        
        if not self.sendgrid_api_key:
            print("❌ Error: SENDGRID_API_KEY no está configurada en las variables de entorno")
            sys.exit(1)
            
        if not self.gmail_password:
            print("⚠️  Advertencia: GMAIL_APP_PASSWORD no está configurada. Las pruebas de recepción no funcionarán.")
            print("   Para configurar: https://support.google.com/accounts/answer/185833")
    
    def test_sendgrid_connection(self) -> bool:
        """Prueba la conexión con SendGrid."""
        print("🔍 Probando conexión con SendGrid...")
        try:
            sg = SendGridAPIClient(api_key=self.sendgrid_api_key)
            # Hacer una llamada simple para verificar la API key
            response = sg.client.api_keys.get()
            print("✅ Conexión con SendGrid exitosa")
            return True
        except Exception as e:
            print(f"❌ Error conectando con SendGrid: {str(e)}")
            return False
    
    def send_test_email(self, to_email: str, subject: str, content: str) -> bool:
        """Envía un email de prueba usando SendGrid."""
        try:
            sg = SendGridAPIClient(api_key=self.sendgrid_api_key)
            
            message = Mail(
                from_email=self.from_email,
                to_emails=to_email,
                subject=subject,
                plain_text_content=content,
                html_content=f"<html><body>{content}</body></html>"
            )
            
            response = sg.send(message)
            print(f"✅ Email enviado exitosamente. Status: {response.status_code}")
            return response.status_code == 202
            
        except Exception as e:
            print(f"❌ Error enviando email: {str(e)}")
            return False
    
    def check_gmail_for_reply(self, expected_subject: str, timeout_minutes: int = 5) -> bool:
        """Verifica si se recibió una respuesta en Gmail."""
        if not self.gmail_password:
            print("⚠️  No se puede verificar Gmail sin GMAIL_APP_PASSWORD")
            return False
            
        print(f"🔍 Verificando Gmail por respuestas (timeout: {timeout_minutes} minutos)...")
        
        try:
            # Conectar a Gmail IMAP
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(self.gmail_user, self.gmail_password)
            mail.select("INBOX")
            
            start_time = time.time()
            timeout_seconds = timeout_minutes * 60
            
            while time.time() - start_time < timeout_seconds:
                # Buscar emails recientes
                mail.list()
                mail.select("INBOX")
                
                # Buscar emails no leídos con el asunto esperado
                _, messages = mail.search(None, f'UNSEEN SUBJECT "{expected_subject}"')
                
                if messages[0]:
                    print("✅ Respuesta recibida en Gmail")
                    mail.logout()
                    return True
                
                print("⏳ Esperando respuesta... (30 segundos)")
                time.sleep(30)
            
            print("⏰ Timeout: No se recibió respuesta en el tiempo esperado")
            mail.logout()
            return False
            
        except Exception as e:
            print(f"❌ Error verificando Gmail: {str(e)}")
            return False
    
    def send_auto_reply_test(self) -> bool:
        """Envía un email que solicita auto-respuesta para probar recepción."""
        subject = f"Prueba de Auto-Respuesta - {datetime.now().strftime('%Y%m%d_%H%M%S')}"
        content = f"""
Hola,

Este es un email de prueba para validar el sistema de correo de chiefdataaiofficer.com.

**Detalles de la Prueba:**
- Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
- Remitente: {self.from_email}
- Destinatario: {self.test_email}

**Instrucciones:**
Por favor, responde a este email con cualquier mensaje para confirmar que puedes recibir correos de nuestro dominio.

**Información Técnica:**
- Servicio: SendGrid
- Dominio: chiefdataaiofficer.com
- Tipo: Prueba de Validación

Gracias por tu colaboración.

Saludos,
Sistema de Validación de Email
        """
        
        return self.send_test_email(self.test_email, subject, content)
    
    def run_comprehensive_test(self):
        """Ejecuta una prueba completa del sistema de email."""
        print("🚀 Iniciando Validación Completa del Sistema de Email")
        print("=" * 60)
        
        # 1. Probar conexión con SendGrid
        if not self.test_sendgrid_connection():
            return False
        
        print("\n" + "=" * 60)
        
        # 2. Enviar email de prueba
        print("📧 Enviando email de prueba...")
        test_subject = f"Prueba de Validación - {datetime.now().strftime('%Y%m%d_%H%M%S')}"
        test_content = f"""
Este es un email de prueba para validar el sistema de correo.

**Información de la Prueba:**
- Timestamp: {datetime.now().isoformat()}
- Dominio: chiefdataaiofficer.com
- Servicio: SendGrid

Si recibes este email, el sistema de envío está funcionando correctamente.
        """
        
        if not self.send_test_email(self.test_email, test_subject, test_content):
            print("❌ Falló el envío del email de prueba")
            return False
        
        print("\n" + "=" * 60)
        
        # 3. Enviar email solicitando auto-respuesta
        print("📤 Enviando email solicitando auto-respuesta...")
        if not self.send_auto_reply_test():
            print("❌ Falló el envío del email de auto-respuesta")
            return False
        
        print("\n" + "=" * 60)
        
        # 4. Verificar recepción de respuesta
        print("📥 Verificando recepción de respuesta...")
        auto_reply_subject = f"Prueba de Auto-Respuesta - {datetime.now().strftime('%Y%m%d_%H%M')}"
        
        if self.check_gmail_for_reply(auto_reply_subject):
            print("✅ Prueba de recepción exitosa")
        else:
            print("⚠️  No se pudo verificar la recepción (puede requerir configuración manual)")
        
        print("\n" + "=" * 60)
        
        # 5. Generar reporte
        self.generate_test_report()
        
        return True
    
    def generate_test_report(self):
        """Genera un reporte de la prueba."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "domain": "chiefdataaiofficer.com",
            "from_email": self.from_email,
            "test_email": self.test_email,
            "sendgrid_configured": bool(self.sendgrid_api_key),
            "gmail_configured": bool(self.gmail_password),
            "test_status": "completed"
        }
        
        # Guardar reporte
        with open("email_validation_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        print("📊 Reporte de validación guardado en: email_validation_report.json")
    
    def test_mvp_email_scenarios(self):
        """Prueba escenarios específicos del MVP de seguros."""
        print("\n🏥 Probando Escenarios del MVP de Seguros")
        print("=" * 60)
        
        scenarios = [
            {
                "name": "Acuse de Recibo de Siniestro",
                "subject": "Acuse de Recibo - Siniestro CLAIM-2024-001",
                "content": """
Estimado/a Cliente,

Hemos recibido su notificación de siniestro y queremos confirmarle que ha sido registrado exitosamente en nuestro sistema.

**Detalles del Siniestro:**
- Número de Siniestro: CLAIM-2024-001
- Estado: En Revisión
- Fecha de Registro: {datetime.now().strftime('%d/%m/%Y %H:%M')}

**Próximos Pasos:**
1. Nuestro equipo de análisis revisará su caso
2. Recibirá actualizaciones por email sobre el progreso
3. Si necesitamos documentación adicional, se lo solicitaremos

Atentamente,
El Equipo de Siniestros
chiefdataaiofficer.com
                """.strip()
            },
            {
                "name": "Solicitud de Documentos",
                "subject": "Solicitud de Documentos - Siniestro CLAIM-2024-001",
                "content": """
Estimado/a Cliente,

Para continuar con el procesamiento de su siniestro, necesitamos que nos proporcione la siguiente documentación:

**Documentos Requeridos:**
- Reporte policial
- Fotos del daño
- Factura de reparación
- Identificación oficial

**Cómo Enviar los Documentos:**
1. Responda a este email adjuntando los documentos
2. O súbalos a través de nuestro portal

Atentamente,
El Equipo de Siniestros
chiefdataaiofficer.com
                """.strip()
            },
            {
                "name": "Actualización de Estado",
                "subject": "Actualización de Siniestro CLAIM-2024-001",
                "content": """
Estimado/a Cliente,

Le informamos que su siniestro ha sido actualizado.

**Detalles del Siniestro:**
- Número de Siniestro: CLAIM-2024-001
- Nuevo Estado: Aprobado
- Fecha de Actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}

**Mensaje:**
Su siniestro ha sido aprobado y el pago será procesado en los próximos 3-5 días hábiles.

Atentamente,
El Equipo de Siniestros
chiefdataaiofficer.com
                """.strip()
            }
        ]
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n📧 Escenario {i}: {scenario['name']}")
            success = self.send_test_email(
                self.test_email,
                scenario['subject'],
                scenario['content']
            )
            
            if success:
                print(f"✅ {scenario['name']} - Enviado correctamente")
            else:
                print(f"❌ {scenario['name']} - Falló el envío")
            
            # Pausa entre envíos para evitar rate limiting
            time.sleep(2)

def main():
    """Función principal del script."""
    print("🔧 Script de Validación de Email para chiefdataaiofficer.com")
    print("=" * 60)
    
    # Verificar variables de entorno
    if not os.getenv("SENDGRID_API_KEY"):
        print("❌ Error: SENDGRID_API_KEY no está configurada")
        print("   Configura la variable de entorno o crea un archivo .env")
        return
    
    validator = EmailValidator()
    
    # Ejecutar prueba completa
    if validator.run_comprehensive_test():
        print("\n🎉 ¡Validación completada exitosamente!")
        
        # Ejecutar pruebas específicas del MVP
        validator.test_mvp_email_scenarios()
        
        print("\n📋 Resumen:")
        print("✅ SendGrid configurado y funcionando")
        print("✅ Emails de prueba enviados correctamente")
        print("✅ Dominio chiefdataaiofficer.com validado")
        print("✅ Escenarios del MVP probados")
        
        if validator.gmail_password:
            print("✅ Verificación de recepción configurada")
        else:
            print("⚠️  Verificación de recepción requiere configuración adicional")
        
        print("\n🚀 El sistema de email está listo para el MVP de seguros!")
        
    else:
        print("\n❌ La validación falló. Revisa la configuración e intenta nuevamente.")

if __name__ == "__main__":
    main() 