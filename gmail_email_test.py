#!/usr/bin/env python3
"""
Script completo para probar envío y recepción de emails usando Gmail API.
Este script reemplaza toda la funcionalidad de Resend con Google Gmail API.
"""

import os
import base64
import json
import time
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from dotenv import load_dotenv

# Google API imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Cargar variables de entorno
load_dotenv()

# Configuración de Gmail API
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify'
]

CREDENTIALS_FILE = 'client_secret_60100775754-vrb6oq8eopesebg3iala0d9ootr6cbih.apps.googleusercontent.com.json'
TOKEN_FILE = 'token.json'

class GmailEmailTester:
    def __init__(self):
        self.service = None
        self.user_email = "gerardo_mayel_fernandez_alamilla@chiefdataaiofficer.com"
        
    def authenticate_gmail(self):
        """Autentica con Gmail API usando OAuth2."""
        print("🔐 Autenticando con Gmail API...")
        
        creds = None
        
        # Verificar si ya existe un token válido
        if os.path.exists(TOKEN_FILE):
            try:
                creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
                print("✅ Token existente encontrado")
            except Exception as e:
                print(f"⚠️ Error cargando token: {e}")
                creds = None
        
        # Si no hay credenciales válidas, hacer el flujo de OAuth
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    print("✅ Token refrescado")
                except Exception as e:
                    print(f"❌ Error refrescando token: {e}")
                    creds = None
            
            if not creds:
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                    creds = flow.run_local_server(port=8080)
                    print("✅ Nuevo token generado")
                except Exception as e:
                    print(f"❌ Error en autenticación OAuth: {e}")
                    return False
            
            # Guardar las credenciales para la próxima vez
            try:
                with open(TOKEN_FILE, 'w') as token:
                    token.write(creds.to_json())
                print("✅ Token guardado")
            except Exception as e:
                print(f"⚠️ Error guardando token: {e}")
        
        # Construir el servicio de Gmail
        try:
            self.service = build('gmail', 'v1', credentials=creds)
            print("✅ Servicio de Gmail construido")
            return True
        except Exception as e:
            print(f"❌ Error construyendo servicio: {e}")
            return False
    
    def send_email(self, to_email, subject, body, is_html=False):
        """Envía un email usando Gmail API."""
        if not self.service:
            print("❌ Servicio de Gmail no disponible")
            return False
        
        try:
            # Crear el mensaje
            message = MIMEMultipart('alternative')
            message['to'] = to_email
            message['from'] = self.user_email
            message['subject'] = subject
            
            # Agregar contenido
            if is_html:
                html_part = MIMEText(body, 'html')
                message.attach(html_part)
            else:
                text_part = MIMEText(body, 'plain')
                message.attach(text_part)
            
            # Codificar el mensaje
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            # Enviar el email
            sent_message = self.service.users().messages().send(
                userId='me', 
                body={'raw': raw_message}
            ).execute()
            
            print(f"✅ Email enviado exitosamente")
            print(f"   ID del mensaje: {sent_message['id']}")
            return True
            
        except HttpError as error:
            print(f"❌ Error enviando email: {error}")
            return False
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return False
    
    def read_recent_emails(self, max_results=10):
        """Lee los emails más recientes de la bandeja de entrada."""
        if not self.service:
            print("❌ Servicio de Gmail no disponible")
            return []
        
        try:
            # Obtener mensajes recientes
            results = self.service.users().messages().list(
                userId='me', 
                labelIds=['INBOX'],
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            
            if not messages:
                print("📭 No hay mensajes en la bandeja de entrada")
                return []
            
            print(f"📧 Encontrados {len(messages)} mensajes recientes")
            
            email_details = []
            
            for message in messages:
                try:
                    # Obtener detalles del mensaje
                    msg = self.service.users().messages().get(
                        userId='me', 
                        id=message['id']
                    ).execute()
                    
                    # Extraer headers
                    headers = msg['payload']['headers']
                    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'Sin asunto')
                    sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Desconocido')
                    date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Desconocida')
                    
                    # Extraer contenido y adjuntos
                    content_data = self._extract_email_content(msg['payload'])
                    
                    email_info = {
                        'id': message['id'],
                        'subject': subject,
                        'from': sender,
                        'date': date,
                        'snippet': msg.get('snippet', ''),
                        'text_content': content_data['text_content'],
                        'html_content': content_data['html_content'],
                        'attachments': content_data['attachments'],
                        'metadata': content_data['metadata']
                    }
                    
                    email_details.append(email_info)
                    
                except Exception as e:
                    print(f"⚠️ Error procesando mensaje {message['id']}: {e}")
                    continue
            
            return email_details
            
        except HttpError as error:
            print(f"❌ Error leyendo emails: {error}")
            return []
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return []
    
    def _extract_email_content(self, payload):
        """Extrae el contenido completo del email incluyendo adjuntos y metadatos."""
        email_data = {
            'text_content': '',
            'html_content': '',
            'attachments': [],
            'metadata': {}
        }
        
        def process_part(part, part_id=''):
            """Procesa una parte del email recursivamente."""
            current_part_id = f"{part_id}.{part.get('partId', '')}" if part_id else part.get('partId', '')
            
            # Extraer metadatos de la parte
            part_info = {
                'part_id': current_part_id,
                'mime_type': part.get('mimeType', ''),
                'filename': part.get('filename', ''),
                'size': part.get('body', {}).get('size', 0),
                'attachment_id': part.get('body', {}).get('attachmentId', '')
            }
            
            # Procesar contenido de texto
            if part.get('mimeType') == 'text/plain':
                if 'data' in part.get('body', {}):
                    try:
                        content = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                        email_data['text_content'] = content
                        part_info['content'] = content[:200] + '...' if len(content) > 200 else content
                    except Exception as e:
                        part_info['error'] = f"Error decodificando texto: {e}"
            
            elif part.get('mimeType') == 'text/html':
                if 'data' in part.get('body', {}):
                    try:
                        content = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                        email_data['html_content'] = content
                        part_info['content'] = content[:200] + '...' if len(content) > 200 else content
                    except Exception as e:
                        part_info['error'] = f"Error decodificando HTML: {e}"
            
            # Procesar archivos adjuntos
            elif part.get('filename') and part.get('body', {}).get('attachmentId'):
                attachment_info = {
                    'filename': part.get('filename', ''),
                    'mime_type': part.get('mimeType', ''),
                    'size': part.get('body', {}).get('size', 0),
                    'attachment_id': part.get('body', {}).get('attachmentId', ''),
                    'part_id': current_part_id,
                    'is_image': part.get('mimeType', '').startswith('image/'),
                    'is_document': part.get('mimeType', '') in [
                        'application/pdf', 'application/msword', 
                        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                        'application/vnd.ms-excel',
                        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                        'text/plain', 'text/csv'
                    ]
                }
                email_data['attachments'].append(attachment_info)
                part_info['is_attachment'] = True
            
            # Procesar partes anidadas (multipart)
            if 'parts' in part:
                for sub_part in part['parts']:
                    process_part(sub_part, current_part_id)
            
            # Agregar metadatos de la parte
            if part_info.get('filename') or part_info.get('content'):
                email_data['metadata'][current_part_id] = part_info
        
        # Procesar el payload principal
        process_part(payload)
        
        return email_data

    def get_attachment_content(self, message_id, attachment_id):
        """Obtiene el contenido de un archivo adjunto específico."""
        if not self.service:
            print("❌ Servicio de Gmail no disponible")
            return None
        
        try:
            attachment = self.service.users().messages().attachments().get(
                userId='me',
                messageId=message_id,
                id=attachment_id
            ).execute()
            
            if 'data' in attachment:
                return base64.urlsafe_b64decode(attachment['data'])
            else:
                print("❌ No se encontraron datos en el adjunto")
                return None
                
        except HttpError as error:
            print(f"❌ Error obteniendo adjunto: {error}")
            return None
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return None

    def read_email_detailed(self, message_id):
        """Lee un email específico con todos sus detalles."""
        if not self.service:
            print("❌ Servicio de Gmail no disponible")
            return None
        
        try:
            # Obtener el mensaje completo
            msg = self.service.users().messages().get(
                userId='me', 
                id=message_id,
                format='full'  # Obtener formato completo
            ).execute()
            
            # Extraer headers completos
            headers = msg['payload']['headers']
            email_info = {
                'id': message_id,
                'thread_id': msg.get('threadId', ''),
                'label_ids': msg.get('labelIds', []),
                'snippet': msg.get('snippet', ''),
                'history_id': msg.get('historyId', ''),
                'internal_date': msg.get('internalDate', ''),
                'headers': {
                    'subject': next((h['value'] for h in headers if h['name'] == 'Subject'), 'Sin asunto'),
                    'from': next((h['value'] for h in headers if h['name'] == 'From'), 'Desconocido'),
                    'to': next((h['value'] for h in headers if h['name'] == 'To'), ''),
                    'cc': next((h['value'] for h in headers if h['name'] == 'Cc'), ''),
                    'bcc': next((h['value'] for h in headers if h['name'] == 'Bcc'), ''),
                    'date': next((h['value'] for h in headers if h['name'] == 'Date'), 'Desconocida'),
                    'message_id': next((h['value'] for h in headers if h['name'] == 'Message-ID'), ''),
                    'reply_to': next((h['value'] for h in headers if h['name'] == 'Reply-To'), ''),
                    'content_type': next((h['value'] for h in headers if h['name'] == 'Content-Type'), ''),
                    'mime_version': next((h['value'] for h in headers if h['name'] == 'MIME-Version'), ''),
                    'x_mailer': next((h['value'] for h in headers if h['name'] == 'X-Mailer'), ''),
                    'user_agent': next((h['value'] for h in headers if h['name'] == 'User-Agent'), ''),
                    'all_headers': {h['name']: h['value'] for h in headers}
                }
            }
            
            # Extraer contenido y adjuntos
            content_data = self._extract_email_content(msg['payload'])
            email_info.update(content_data)
            
            return email_info
            
        except HttpError as error:
            print(f"❌ Error leyendo email: {error}")
            return None
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return None
    
    def search_emails(self, query, max_results=5):
        """Busca emails con criterios específicos."""
        if not self.service:
            print("❌ Servicio de Gmail no disponible")
            return []
        
        try:
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            
            if not messages:
                print(f"🔍 No se encontraron emails con la búsqueda: {query}")
                return []
            
            print(f"🔍 Encontrados {len(messages)} emails con la búsqueda: {query}")
            
            email_details = []
            for message in messages:
                try:
                    msg = self.service.users().messages().get(
                        userId='me', 
                        id=message['id']
                    ).execute()
                    
                    headers = msg['payload']['headers']
                    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'Sin asunto')
                    sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Desconocido')
                    date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Desconocida')
                    
                    # Extraer contenido y adjuntos
                    content_data = self._extract_email_content(msg['payload'])
                    
                    email_info = {
                        'id': message['id'],
                        'subject': subject,
                        'from': sender,
                        'date': date,
                        'snippet': msg.get('snippet', ''),
                        'text_content': content_data['text_content'],
                        'html_content': content_data['html_content'],
                        'attachments': content_data['attachments'],
                        'metadata': content_data['metadata']
                    }
                    
                    email_details.append(email_info)
                    
                except Exception as e:
                    print(f"⚠️ Error procesando mensaje {message['id']}: {e}")
                    continue
            
            return email_details
            
        except HttpError as error:
            print(f"❌ Error buscando emails: {error}")
            return []
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return []

def main():
    """Función principal del script."""
    print("="*80)
    print("📧 TESTER DE EMAIL CON GMAIL API")
    print("="*80)
    
    # Crear instancia del tester
    tester = GmailEmailTester()
    
    # Autenticar
    if not tester.authenticate_gmail():
        print("❌ No se pudo autenticar con Gmail API")
        return
    
    print("\n" + "="*80)
    print("🧪 PRUEBAS DISPONIBLES:")
    print("="*80)
    print("1. Enviar email de prueba")
    print("2. Leer emails recientes")
    print("3. Buscar emails específicos")
    print("4. Leer email específico (detallado)")
    print("5. Prueba completa (enviar + buscar)")
    print("6. Salir")
    
    while True:
        try:
            choice = input("\n🔍 Selecciona una opción (1-6): ").strip()
            
            if choice == '1':
                # Enviar email de prueba
                print("\n📤 ENVIANDO EMAIL DE PRUEBA...")
                
                to_email = input("📧 Email destinatario: ").strip()
                if not to_email:
                    to_email = "gerardo_mayel_fernandez_alamilla@chiefdataaiofficer.com"
                
                subject = "🧪 Prueba de Gmail API - " + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                
                body = f"""
                <html>
                <body>
                    <h2>🧪 Prueba de Gmail API</h2>
                    <p>Este es un email de prueba enviado usando la Gmail API de Google.</p>
                    <p><strong>Fecha y hora:</strong> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</p>
                    <p><strong>Remitente:</strong> {tester.user_email}</p>
                    <p><strong>Destinatario:</strong> {to_email}</p>
                    <hr>
                    <p><em>Este email fue enviado automáticamente por el script de prueba.</em></p>
                </body>
                </html>
                """
                
                if tester.send_email(to_email, subject, body, is_html=True):
                    print("✅ Email enviado exitosamente")
                else:
                    print("❌ Error enviando email")
            
            elif choice == '2':
                # Leer emails recientes
                print("\n📥 LEYENDO EMAILS RECIENTES...")
                
                max_results = input("📊 Número máximo de emails (default: 10): ").strip()
                max_results = int(max_results) if max_results.isdigit() else 10
                
                emails = tester.read_recent_emails(max_results)
                
                if emails:
                    print(f"\n📧 ÚLTIMOS {len(emails)} EMAILS:")
                    for i, email in enumerate(emails, 1):
                        print(f"\n--- Email {i} ---")
                        print(f"📧 De: {email['from']}")
                        print(f"📋 Asunto: {email['subject']}")
                        print(f"📅 Fecha: {email['date']}")
                        print(f"💬 Snippet: {email['snippet'][:100]}...")
                        
                        # Mostrar contenido de texto
                        if email['text_content']:
                            print(f"📝 Contenido texto: {email['text_content'][:200]}...")
                        
                        # Mostrar contenido HTML
                        if email['html_content']:
                            print(f"📄 Contenido HTML: {email['html_content'][:200]}...")
                        
                        # Mostrar adjuntos
                        if email['attachments']:
                            print(f"📎 Adjuntos ({len(email['attachments'])}):")
                            for j, attachment in enumerate(email['attachments'], 1):
                                print(f"   📎 {j}. {attachment['filename']}")
                                print(f"      Tipo: {attachment['mime_type']}")
                                print(f"      Tamaño: {attachment['size']} bytes")
                                print(f"      Es imagen: {'✅' if attachment['is_image'] else '❌'}")
                                print(f"      Es documento: {'✅' if attachment['is_document'] else '❌'}")
                                print(f"      ID: {attachment['attachment_id']}")
                        
                        # Mostrar metadatos
                        if email['metadata']:
                            print(f"🔍 Metadatos ({len(email['metadata'])} partes):")
                            for part_id, part_info in email['metadata'].items():
                                print(f"   📋 Parte {part_id}: {part_info.get('mime_type', 'N/A')}")
                                if part_info.get('filename'):
                                    print(f"      Archivo: {part_info['filename']}")
                                if part_info.get('size'):
                                    print(f"      Tamaño: {part_info['size']} bytes")
            
            elif choice == '3':
                # Buscar emails específicos
                print("\n🔍 BUSCANDO EMAILS...")
                
                query = input("🔍 Término de búsqueda: ").strip()
                if not query:
                    query = "test"
                
                max_results = input("📊 Número máximo de resultados (default: 5): ").strip()
                max_results = int(max_results) if max_results.isdigit() else 5
                
                emails = tester.search_emails(query, max_results)
                
                if emails:
                    print(f"\n🔍 RESULTADOS DE BÚSQUEDA: '{query}'")
                    for i, email in enumerate(emails, 1):
                        print(f"\n--- Resultado {i} ---")
                        print(f"📧 De: {email['from']}")
                        print(f"📋 Asunto: {email['subject']}")
                        print(f"📅 Fecha: {email['date']}")
                        print(f"💬 Snippet: {email['snippet'][:100]}...")
                        
                        # Mostrar contenido de texto
                        if email['text_content']:
                            print(f"📝 Contenido texto: {email['text_content'][:200]}...")
                        
                        # Mostrar contenido HTML
                        if email['html_content']:
                            print(f"📄 Contenido HTML: {email['html_content'][:200]}...")
                        
                        # Mostrar adjuntos
                        if email['attachments']:
                            print(f"📎 Adjuntos ({len(email['attachments'])}):")
                            for j, attachment in enumerate(email['attachments'], 1):
                                print(f"   📎 {j}. {attachment['filename']}")
                                print(f"      Tipo: {attachment['mime_type']}")
                                print(f"      Tamaño: {attachment['size']} bytes")
                                print(f"      Es imagen: {'✅' if attachment['is_image'] else '❌'}")
                                print(f"      Es documento: {'✅' if attachment['is_document'] else '❌'}")
                                print(f"      ID: {attachment['attachment_id']}")
                        
                        # Mostrar metadatos
                        if email['metadata']:
                            print(f"🔍 Metadatos ({len(email['metadata'])} partes):")
                            for part_id, part_info in email['metadata'].items():
                                print(f"   📋 Parte {part_id}: {part_info.get('mime_type', 'N/A')}")
                                if part_info.get('filename'):
                                    print(f"      Archivo: {part_info['filename']}")
                                if part_info.get('size'):
                                    print(f"      Tamaño: {part_info['size']} bytes")
            
            elif choice == '4':
                # Leer email específico (detallado)
                print("\n📥 LEYENDO EMAIL ESPECÍFICO...")
                
                message_id = input("📧 ID del email: ").strip()
                if not message_id:
                    message_id = "1"
                
                email = tester.read_email_detailed(message_id)
                
                if email:
                    print(f"\n📧 DETALLES DEL EMAIL:")
                    for key, value in email.items():
                        if isinstance(value, dict):
                            print(f"\n--- {key} ---")
                            for sub_key, sub_value in value.items():
                                if isinstance(sub_value, dict):
                                    print(f"--- {sub_key} ---")
                                    for sub_sub_key, sub_sub_value in sub_value.items():
                                        print(f"{sub_sub_key}: {sub_sub_value}")
                                else:
                                    print(f"{sub_key}: {sub_value}")
                        else:
                            print(f"{key}: {value}")
            
            elif choice == '5':
                # Prueba completa
                print("\n🔄 PRUEBA COMPLETA: ENVIAR + BUSCAR...")
                
                # Enviar email
                test_email = "gerardo_mayel_fernandez_alamilla@chiefdataaiofficer.com"
                subject = "🧪 Prueba Completa Gmail API - " + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                body = f"""
                <html>
                <body>
                    <h2>🧪 Prueba Completa Gmail API</h2>
                    <p>Este email es parte de una prueba completa del sistema.</p>
                    <p><strong>Timestamp:</strong> {datetime.now().isoformat()}</p>
                    <p><strong>ID único:</strong> {int(time.time())}</p>
                </body>
                </html>
                """
                
                print("📤 Enviando email de prueba...")
                if tester.send_email(test_email, subject, body, is_html=True):
                    print("✅ Email enviado")
                    
                    # Esperar un momento para que llegue
                    print("⏳ Esperando 10 segundos para que llegue el email...")
                    time.sleep(10)
                    
                    # Buscar el email
                    print("🔍 Buscando el email enviado...")
                    search_query = f"subject:Prueba Completa Gmail API"
                    emails = tester.search_emails(search_query, 5)
                    
                    if emails:
                        print("✅ Email encontrado en la bandeja de entrada:")
                        for email in emails:
                            print(f"   📧 De: {email['from']}")
                            print(f"   📋 Asunto: {email['subject']}")
                            print(f"   📅 Fecha: {email['date']}")
                    else:
                        print("⚠️ Email no encontrado (puede tardar más en llegar)")
                else:
                    print("❌ Error enviando email")
            
            elif choice == '6':
                print("\n👋 ¡Hasta luego!")
                break
            
            else:
                print("❌ Opción inválida. Por favor selecciona 1-6.")
        
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main() 