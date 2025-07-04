"""
Procesador de claims que maneja el flujo completo desde la recepción del email.
"""

import os
from datetime import datetime
from typing import Dict, List, Optional
from app.core.database import get_db
from app.core.models import Claim, ClaimDocument, ClaimStatus, generate_claim_number
from app.services.gmail_service import GmailService
from app.services.gcs_storage import gcs_storage

class ClaimsProcessor:
    """Procesador principal de claims."""
    
    def __init__(self):
        self.gmail_service = GmailService()
        self.storage_service = gcs_storage
    
    def process_claim_email(self, email_data: Dict) -> Dict:
        """
        Procesa un email de claim completo.
        
        Args:
            email_data: Datos del email con adjuntos
            
        Returns:
            Diccionario con el resultado del procesamiento
        """
        try:
            print(f"🚨 Procesando claim email: {email_data.get('subject', 'Sin asunto')}")
            
            # Verificar si ya fue procesado
            db = next(get_db())
            existing_claim = db.query(Claim).filter(
                Claim.gmail_message_id == email_data['id']
            ).first()
            
            if existing_claim:
                print(f"⚠️ Email ya procesado anteriormente (Claim: {existing_claim.claim_number})")
                db.close()
                return {
                    'status': 'already_processed',
                    'claim_number': existing_claim.claim_number,
                    'message': 'Email already processed'
                }
            
            # Generar número de claim
            claim_number = generate_claim_number()
            print(f"📋 Número de claim generado: {claim_number}")
            
            # Extraer información del email
            sender_email = self._extract_sender_email(email_data.get('sender', ''))
            sender_name = self._extract_sender_name(email_data.get('sender', ''))
            
            # Crear claim en base de datos
            claim = Claim(
                claim_number=claim_number,
                gmail_message_id=email_data['id'],
                sender_email=sender_email,
                sender_name=sender_name,
                subject=email_data.get('subject', 'Sin asunto'),
                email_content=email_data.get('text_content', ''),
                notification_date=datetime.now(),
                status=ClaimStatus.INITIAL_NOTIFICATION
            )
            
            db.add(claim)
            db.commit()
            db.refresh(claim)
            
            print(f"✅ Claim creado en BD: {claim.id}")
            
            # Procesar adjuntos
            documents_processed = []
            attachments = email_data.get('attachments', [])
            
            for attachment in attachments:
                doc_result = self._process_attachment(
                    claim.id, 
                    claim_number,
                    email_data['id'],
                    attachment,
                    db
                )
                if doc_result:
                    documents_processed.append(doc_result)
            
            # Enviar respuesta al cliente
            response_sent = self._send_claim_response(claim, email_data)
            
            # Actualizar estado del claim
            claim.response_sent = response_sent
            claim.response_sent_date = datetime.now() if response_sent else None
            claim.form_link_sent = response_sent
            claim.form_link_sent_date = datetime.now() if response_sent else None
            claim.status = ClaimStatus.FORM_SENT if response_sent else ClaimStatus.INITIAL_NOTIFICATION
            
            db.commit()
            db.close()
            
            print(f"\n📊 RESUMEN DEL PROCESAMIENTO:")
            print(f"   Email ID: {email_data['id']}")
            print(f"   Claim Number: {claim_number}")
            print(f"   Documentos procesados: {len(documents_processed)}")
            print(f"   Respuesta enviada: {'✅' if response_sent else '❌'}")
            
            return {
                'status': 'success',
                'claim_number': claim_number,
                'documents_processed': documents_processed,
                'response_sent': response_sent
            }
            
        except Exception as e:
            print(f"❌ Error procesando claim: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _extract_sender_email(self, sender_header: str) -> str:
        """Extrae el email del remitente del header."""
        if '<' in sender_header and '>' in sender_header:
            return sender_header.split('<')[1].split('>')[0]
        return sender_header
    
    def _extract_sender_name(self, sender_header: str) -> Optional[str]:
        """Extrae el nombre del remitente del header."""
        if '<' in sender_header and '>' in sender_header:
            return sender_header.split('<')[0].strip()
        return None
    
    def _process_attachment(self, claim_id: int, claim_number: str, email_id: str, 
                          attachment: Dict, db) -> Optional[Dict]:
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
            attachment_data = self.gmail_service.descargar_adjunto(email_id, attachment_id)
            
            if not attachment_data:
                print(f"❌ Error descargando adjunto: {filename}")
                return None
            
            # Subir a Google Cloud Storage
            storage_url = self.storage_service.upload_file(
                file_content=attachment_data['content'],
                filename=filename,
                numero_siniestro=claim_number,
                email_id=email_id,
                content_type=mime_type
            )
            
            if storage_url:
                print(f"✅ Documento subido exitosamente")
                print(f"   URL: {storage_url}")
                
                # Crear registro en base de datos
                document = ClaimDocument(
                    claim_id=claim_id,
                    filename=filename,
                    mime_type=mime_type,
                    file_size_bytes=size,
                    storage_url=storage_url,
                    storage_path=f"{claim_number}/email-{email_id}/{filename}",
                    source_type='email_attachment'
                )
                
                db.add(document)
                db.commit()
                
                print(f"✅ Documento registrado en BD: {document.id}")
                
                return {
                    'filename': filename,
                    'storage_url': storage_url
                }
            else:
                print(f"❌ Error subiendo documento: {filename}")
                return None
                
        except Exception as e:
            print(f"❌ Error procesando adjunto {filename}: {e}")
            return None
    
    def _send_claim_response(self, claim: Claim, email_data: Dict) -> bool:
        """Envía la respuesta al cliente con el número de claim y enlaces."""
        try:
            # Obtener URL del formulario web (ajustar según tu configuración)
            web_form_url = f"https://your-app-domain.com/claim-form?claim={claim.claim_number}"
            
            # Obtener URL del PDF (ubicación fija del PDF existente)
            pdf_url = "https://storage.googleapis.com/claims-documents-zurich-ai/claim_form/Claim_Form.pdf"
            
            # Crear contenido del email de respuesta
            subject = f"Claim Received - {claim.claim_number}"
            
            body = f"""
Dear {claim.sender_name or 'Valued Customer'},

Thank you for submitting your travel insurance claim. We have received your notification and assigned the following claim number:

CLAIM NUMBER: {claim.claim_number}

To complete your claim, you have two options:

OPTION 1: DIGITAL FORM (Recommended)
Complete our online form for faster processing:
{web_form_url}

OPTION 2: MANUAL PDF FORM
Download, fill out, and return the attached claim form:
{pdf_url}

Please include all relevant documentation such as:
• Receipts for all expenses
• Travel itinerary
• Police reports (if applicable)
• Medical certificates (if applicable)
• Any other relevant documentation

IMPORTANT NOTES:
- You can use either the digital form OR the manual PDF form
- If you have additional documents, you can attach them to your email response
- You can also upload documents through the digital form
- Please include your claim number ({claim.claim_number}) in all communications

If you have any questions, please reply to this email with your claim number.

Best regards,
Travel Insurance Claims Team
            """
            
            # Enviar email de respuesta
            response_sent = self.gmail_service.enviar_email_con_adjunto(
                to_email=claim.sender_email,
                subject=subject,
                body=body,
                adjunto_nombre="Claim_Form.pdf",
                adjunto_contenido=self._get_claim_pdf_content(),
                adjunto_tipo="application/pdf"
            )
            
            if response_sent:
                print(f"✅ Respuesta enviada exitosamente a {claim.sender_email}")
                return True
            else:
                print(f"❌ Error enviando respuesta a {claim.sender_email}")
                return False
                
        except Exception as e:
            print(f"❌ Error enviando respuesta: {e}")
            return False
    
    def _get_claim_pdf_content(self) -> bytes:
        """Obtiene el contenido del PDF del formulario desde storage."""
        try:
            # Obtener desde la ubicación fija del PDF existente
            blob = self.storage_service.bucket.blob("claim_form/Claim_Form.pdf")
            if blob.exists():
                print("✅ PDF encontrado en storage")
                return blob.download_as_bytes()
            else:
                print("❌ PDF no encontrado en storage")
                return self._create_claim_pdf()
        except Exception as e:
            print(f"❌ Error obteniendo PDF: {e}")
            return self._create_claim_pdf()
    
    def _create_claim_pdf(self) -> bytes:
        """Crea un PDF básico del formulario (fallback)."""
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        from io import BytesIO
        
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        p.drawString(100, 750, "TRAVEL INSURANCE CLAIM FORM")
        p.drawString(100, 720, "Please fill out this form completely and return with supporting documentation.")
        p.drawString(100, 690, "This is a basic version of the form.")
        
        p.save()
        buffer.seek(0)
        return buffer.getvalue()
    
    def process_new_claim_emails(self, max_results: int = 10) -> List[Dict]:
        """
        Procesa emails nuevos con palabras clave de claims.
        
        Args:
            max_results: Número máximo de emails a procesar
            
        Returns:
            Lista de resultados del procesamiento
        """
        try:
            print("🔍 Buscando emails nuevos con palabras clave de claims...")
            
            # Buscar emails con palabras clave
            emails = self.gmail_service.buscar_emails_claims(max_results=max_results)
            
            if not emails:
                print("📭 No se encontraron emails nuevos con palabras clave de claims")
                return []
            
            print(f"📧 Encontrados {len(emails)} emails para procesar")
            
            results = []
            for email in emails:
                result = self.process_claim_email(email)
                results.append(result)
                
                if result.get('status') == 'success':
                    print(f"✅ Email procesado: {result.get('claim_number')}")
                else:
                    print(f"⚠️ Email no procesado: {result.get('message', 'Error desconocido')}")
            
            return results
            
        except Exception as e:
            print(f"❌ Error procesando emails: {e}")
            return [] 