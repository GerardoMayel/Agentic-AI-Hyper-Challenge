import os
import base64
import json
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import email
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import sys

class GmailService:
    """Servicio para leer emails de Gmail usando la API de Gmail."""
    
    # Si modificas estos scopes, elimina el archivo token.json
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']
    
    def __init__(self):
        self.creds = None
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Autentica usando el archivo token.json y verifica refresh_token."""
        try:
            self.creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
            # Verificar refresh_token
            if not hasattr(self.creds, 'refresh_token') or not self.creds.refresh_token:
                print("\n❌ ERROR: El archivo token.json no contiene refresh_token.")
                print("\nSOLUCIÓN:")
                print("1. Ve a https://myaccount.google.com/permissions y revoca el acceso de la app.")
                print("2. Borra el archivo token.json.")
                print("3. Ejecuta el script gmail_email_test.py --regenerate-token en modo incógnito.")
                print("4. Autoriza y asegúrate de que el nuevo token.json tenga refresh_token.")
                print("\nLa app se detendrá hasta que el token sea válido.\n")
                sys.exit(1)
        except Exception as e:
            print(f"\n❌ ERROR autenticando con Gmail API: {e}\n")
            sys.exit(1)
        
        try:
            # Llama a la API de Gmail
            self.service = build('gmail', 'v1', credentials=self.creds)
            print("✅ Autenticación con Gmail exitosa")
        except HttpError as error:
            print(f"❌ Error autenticando con Gmail: {error}")
    
    def search_emails(self, query: str = "subject:test", max_results: int = 10) -> List[Dict]:
        """
        Busca emails que coincidan con la consulta.
        
        Args:
            query: Consulta de búsqueda (ej: "subject:test")
            max_results: Número máximo de resultados
            
        Returns:
            Lista de emails encontrados
        """
        if not self.service:
            print("❌ Servicio de Gmail no disponible")
            return []
        
        try:
            # Buscar emails
            results = self.service.users().messages().list(
                userId='me', 
                q=query, 
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            
            if not messages:
                print(f"📭 No se encontraron emails con la consulta: {query}")
                return []
            
            print(f"📧 Encontrados {len(messages)} emails")
            
            # Obtener detalles de cada email
            emails = []
            for message in messages:
                email_data = self._get_email_details(message['id'])
                if email_data:
                    emails.append(email_data)
            
            return emails
            
        except HttpError as error:
            print(f"❌ Error buscando emails: {error}")
            return []
    
    def _get_email_details(self, message_id: str) -> Optional[Dict]:
        """
        Obtiene los detalles completos de un email.
        
        Args:
            message_id: ID del mensaje
            
        Returns:
            Diccionario con los detalles del email
        """
        try:
            message = self.service.users().messages().get(
                userId='me', 
                id=message_id, 
                format='full'
            ).execute()
            
            headers = message['payload']['headers']
            
            # Extraer información básica
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'Sin asunto')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Desconocido')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
            
            # Extraer contenido del email
            body, attachments = self._extract_email_content(message['payload'])
            
            return {
                'id': message_id,
                'subject': subject,
                'sender': sender,
                'date': date,
                'body': body,
                'attachments': attachments,
                'snippet': message.get('snippet', '')
            }
            
        except HttpError as error:
            print(f"❌ Error obteniendo detalles del email {message_id}: {error}")
            return None
    
    def _extract_email_content(self, payload: Dict) -> Tuple[str, List[Dict]]:
        """
        Extrae el contenido del email y los adjuntos.
        
        Args:
            payload: Payload del mensaje
            
        Returns:
            Tupla con (cuerpo del email, lista de adjuntos)
        """
        body = ""
        attachments = []
        
        if 'parts' in payload:
            # Email multipart
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    # Contenido de texto
                    if 'data' in part['body']:
                        body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                elif part['mimeType'].startswith('image/'):
                    # Imagen adjunta
                    attachment = self._extract_attachment(part)
                    if attachment:
                        attachments.append(attachment)
        else:
            # Email simple
            if 'data' in payload['body']:
                body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
        
        return body, attachments
    
    def _extract_attachment(self, part: Dict) -> Optional[Dict]:
        """
        Extrae un adjunto del email.
        
        Args:
            part: Parte del mensaje que contiene el adjunto
            
        Returns:
            Diccionario con información del adjunto
        """
        try:
            attachment_id = part['body']['attachmentId']
            attachment = self.service.users().messages().attachments().get(
                userId='me', 
                messageId=part['body'].get('messageId', ''), 
                id=attachment_id
            ).execute()
            
            data = base64.urlsafe_b64decode(attachment['data'])
            
            return {
                'filename': part.get('filename', 'adjunto'),
                'mime_type': part['mimeType'],
                'size': part['body'].get('size', 0),
                'data': data
            }
            
        except Exception as e:
            print(f"❌ Error extrayendo adjunto: {e}")
            return None
    
    def get_test_emails(self, max_results: int = 5) -> List[Dict]:
        """
        Obtiene emails de prueba para testing.
        
        Args:
            max_results: Número máximo de resultados
            
        Returns:
            Lista de emails de prueba
        """
        return self.search_emails("subject:test", max_results)
    
    def buscar_emails_claims(self, max_results: int = 10) -> List[Dict]:
        """
        Busca emails que contengan palabras clave de claims.
        
        Args:
            max_results: Número máximo de resultados
            
        Returns:
            Lista de emails con palabras clave de claims
        """
        # Buscar emails con palabras clave de claims
        query = "subject:(claim OR claims OR siniestro OR accidente OR daño OR robo OR incendio)"
        
        if not self.service:
            print("❌ Servicio de Gmail no disponible")
            return []
        
        try:
            # Buscar emails
            results = self.service.users().messages().list(
                userId='me', 
                q=query, 
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            
            if not messages:
                print(f"📭 No se encontraron emails con palabras clave de claims")
                return []
            
            print(f"📧 Encontrados {len(messages)} emails con palabras clave de claims")
            
            # Obtener detalles de cada email
            emails = []
            for message in messages:
                email_data = self._get_email_details_claims(message['id'])
                if email_data:
                    emails.append(email_data)
            
            return emails
            
        except HttpError as error:
            print(f"❌ Error buscando emails de claims: {error}")
            return []
    
    def _get_email_details_claims(self, message_id: str) -> Optional[Dict]:
        """
        Obtiene los detalles completos de un email para claims.
        
        Args:
            message_id: ID del mensaje
            
        Returns:
            Diccionario con los detalles del email
        """
        try:
            message = self.service.users().messages().get(
                userId='me', 
                id=message_id, 
                format='full'
            ).execute()
            
            headers = message['payload']['headers']
            
            # Extraer información básica
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'Sin asunto')
            from_header = next((h['value'] for h in headers if h['name'] == 'From'), 'Desconocido')
            to_header = next((h['value'] for h in headers if h['name'] == 'To'), '')
            date_header = next((h['value'] for h in headers if h['name'] == 'Date'), '')
            
            # Extraer contenido del email
            text_content, html_content, attachments = self._extract_email_content_claims(message['payload'])
            
            return {
                'id': message_id,
                'thread_id': message.get('threadId', ''),
                'subject': subject,
                'from': from_header,
                'to': to_header,
                'date': date_header,
                'text_content': text_content,
                'html_content': html_content,
                'snippet': message.get('snippet', ''),
                'attachments': attachments,
                'metadata': {
                    'labelIds': message.get('labelIds', []),
                    'internalDate': message.get('internalDate', '')
                },
                'headers': {h['name']: h['value'] for h in headers}
            }
            
        except HttpError as error:
            print(f"❌ Error obteniendo detalles del email {message_id}: {error}")
            return None
    
    def _extract_email_content_claims(self, payload: Dict) -> Tuple[str, str, List[Dict]]:
        """
        Extrae el contenido del email y los adjuntos para claims.
        
        Args:
            payload: Payload del mensaje
            
        Returns:
            Tupla con (contenido_texto, contenido_html, lista de adjuntos)
        """
        text_content = ""
        html_content = ""
        attachments = []
        
        def process_part(part):
            nonlocal text_content, html_content
            
            if part['mimeType'] == 'text/plain':
                # Contenido de texto
                if 'data' in part['body']:
                    text_content = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
            elif part['mimeType'] == 'text/html':
                # Contenido HTML
                if 'data' in part['body']:
                    html_content = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
            elif part['mimeType'].startswith('image/') or part['mimeType'] in ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                # Adjunto
                attachment = self._extract_attachment_claims(part)
                if attachment:
                    attachments.append(attachment)
        
        if 'parts' in payload:
            # Email multipart
            for part in payload['parts']:
                if 'parts' in part:
                    # Subpartes
                    for subpart in part['parts']:
                        process_part(subpart)
                else:
                    process_part(part)
        else:
            # Email simple
            if 'data' in payload['body']:
                if payload['mimeType'] == 'text/plain':
                    text_content = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8', errors='ignore')
                elif payload['mimeType'] == 'text/html':
                    html_content = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8', errors='ignore')
        
        return text_content, html_content, attachments
    
    def _extract_attachment_claims(self, part: Dict) -> Optional[Dict]:
        """
        Extrae un adjunto del email para claims.
        
        Args:
            part: Parte del mensaje que contiene el adjunto
            
        Returns:
            Diccionario con información del adjunto
        """
        try:
            if 'attachmentId' not in part['body']:
                return None
                
            attachment_id = part['body']['attachmentId']
            filename = part.get('filename', f'adjunto_{attachment_id}')
            mime_type = part['mimeType']
            size = part['body'].get('size', 0)
            
            # Determinar si es imagen o documento
            is_image = mime_type.startswith('image/')
            is_document = mime_type in [
                'application/pdf',
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/vnd.ms-excel',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            ]
            
            return {
                'filename': filename,
                'mime_type': mime_type,
                'size': size,
                'attachment_id': attachment_id,
                'is_image': is_image,
                'is_document': is_document
            }
            
        except Exception as e:
            print(f"❌ Error extrayendo adjunto: {e}")
            return None
    
    def descargar_adjunto(self, message_id: str, attachment_id: str) -> Optional[Dict]:
        """
        Descarga un adjunto específico de un email.
        
        Args:
            message_id: ID del mensaje
            attachment_id: ID del adjunto
            
        Returns:
            Diccionario con el contenido del adjunto
        """
        try:
            attachment = self.service.users().messages().attachments().get(
                userId='me', 
                messageId=message_id, 
                id=attachment_id
            ).execute()
            
            content = base64.urlsafe_b64decode(attachment['data'])
            
            return {
                'content': content,
                'size': len(content)
            }
            
        except HttpError as error:
            print(f"❌ Error descargando adjunto {attachment_id}: {error}")
            return None
    
    def print_email_summary(self, email_data: Dict):
        """Imprime un resumen del email."""
        print(f"\n📧 RESUMEN DEL EMAIL:")
        print(f"   ID: {email_data['id']}")
        print(f"   Asunto: {email_data['subject']}")
        print(f"   Remitente: {email_data['sender']}")
        print(f"   Fecha: {email_data['date']}")
        print(f"   Snippet: {email_data['snippet'][:100]}...")
        print(f"   Adjuntos: {len(email_data['attachments'])}")
    
    def enviar_email_con_adjunto(self, to_email: str, subject: str, body: str, 
                                adjunto_nombre: str, adjunto_contenido: bytes, 
                                adjunto_tipo: str = "application/pdf") -> bool:
        """
        Envía un email con adjunto usando la API de Gmail.
        
        Args:
            to_email: Email del destinatario
            subject: Asunto del email
            body: Cuerpo del email
            adjunto_nombre: Nombre del archivo adjunto
            adjunto_contenido: Contenido del archivo en bytes
            adjunto_tipo: Tipo MIME del adjunto
            
        Returns:
            True si se envió exitosamente, False en caso contrario
        """
        if not self.service:
            print("❌ Servicio de Gmail no disponible")
            return False
        
        try:
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            from email.mime.base import MIMEBase
            import base64
            
            # Crear mensaje con adjunto
            message = MIMEMultipart()
            message['to'] = to_email
            message['subject'] = subject
            
            # Agregar cuerpo del mensaje
            text_part = MIMEText(body, 'plain')
            message.attach(text_part)
            
            # Agregar adjunto
            adjunto_part = MIMEBase('application', 'pdf')
            adjunto_part.set_payload(adjunto_contenido)
            adjunto_part.add_header('Content-Disposition', 'attachment', filename=adjunto_nombre)
            message.attach(adjunto_part)
            
            # Codificar mensaje
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            # Enviar mensaje
            sent_message = self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            print(f"✅ Email enviado exitosamente")
            print(f"   Message ID: {sent_message['id']}")
            return True
            
        except Exception as e:
            print(f"❌ Error enviando email: {e}")
            return False 