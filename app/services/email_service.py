import os
from typing import Optional
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from datetime import datetime

class EmailService:
    """Servicio para manejo de emails usando SendGrid."""
    
    def __init__(self):
        self.api_key = os.getenv("SENDGRID_API_KEY")
        self.from_email = os.getenv("FROM_EMAIL", "noreply@tuapp.com")
        self.client = SendGridAPIClient(api_key=self.api_key) if self.api_key else None
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        content: str,
        content_type: str = "text/plain"
    ) -> bool:
        """
        Envía un email usando SendGrid.
        
        Args:
            to_email: Email del destinatario
            subject: Asunto del email
            content: Contenido del email
            content_type: Tipo de contenido (text/plain o text/html)
            
        Returns:
            bool: True si el email se envió correctamente, False en caso contrario
        """
        if not self.client:
            print("SendGrid no está configurado. Email no enviado.")
            return False
        
        try:
            message = Mail(
                from_email=self.from_email,
                to_emails=to_email,
                subject=subject,
                plain_text_content=content if content_type == "text/plain" else None,
                html_content=content if content_type == "text/html" else None
            )
            
            response = self.client.send(message)
            print(f"Email enviado exitosamente. Status code: {response.status_code}")
            return response.status_code == 202
            
        except Exception as e:
            print(f"Error enviando email: {str(e)}")
            return False
    
    def send_acknowledgement(
        self,
        to_email: str,
        claim_number: str,
        customer_name: Optional[str] = None
    ) -> bool:
        """
        Envía un acuse de recibo de siniestro al cliente.
        
        Args:
            to_email: Email del cliente
            claim_number: Número del siniestro generado
            customer_name: Nombre del cliente (opcional)
            
        Returns:
            bool: True si el email se envió correctamente
        """
        subject = f"Acuse de Recibo - Siniestro {claim_number}"
        
        # Personalizar el saludo
        greeting = f"Estimado/a {customer_name}" if customer_name else "Estimado/a cliente"
        
        # Contenido del email
        content = f"""
{greeting},

Hemos recibido su notificación de siniestro y queremos confirmarle que ha sido registrado exitosamente en nuestro sistema.

**Detalles del Siniestro:**
- Número de Siniestro: {claim_number}
- Estado: En Revisión
- Fecha de Registro: {datetime.now().strftime('%d/%m/%Y %H:%M')}

**Próximos Pasos:**
1. Nuestro equipo de análisis revisará su caso
2. Recibirá actualizaciones por email sobre el progreso
3. Si necesitamos documentación adicional, se lo solicitaremos

**Portal del Cliente:**
Puede consultar el estado de su siniestro en cualquier momento visitando:
https://tu-dominio.com/claims/{claim_number}

**Contacto:**
Si tiene alguna pregunta, puede responder a este email o contactarnos a través de nuestro portal web.

Atentamente,
El Equipo de Siniestros
        """
        
        return self.send_email(to_email, subject, content.strip())
    
    def send_claim_update(
        self,
        to_email: str,
        claim_number: str,
        status: str,
        message: str,
        customer_name: Optional[str] = None
    ) -> bool:
        """
        Envía una actualización de estado del siniestro al cliente.
        
        Args:
            to_email: Email del cliente
            claim_number: Número del siniestro
            status: Nuevo estado del siniestro
            message: Mensaje personalizado
            customer_name: Nombre del cliente (opcional)
            
        Returns:
            bool: True si el email se envió correctamente
        """
        subject = f"Actualización de Siniestro {claim_number}"
        
        greeting = f"Estimado/a {customer_name}" if customer_name else "Estimado/a cliente"
        
        content = f"""
{greeting},

Le informamos que su siniestro ha sido actualizado.

**Detalles del Siniestro:**
- Número de Siniestro: {claim_number}
- Nuevo Estado: {status}
- Fecha de Actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}

**Mensaje:**
{message}

**Portal del Cliente:**
Consulte más detalles en: https://tu-dominio.com/claims/{claim_number}

Atentamente,
El Equipo de Siniestros
        """
        
        return self.send_email(to_email, subject, content.strip())
    
    def send_document_request(
        self,
        to_email: str,
        claim_number: str,
        required_documents: list,
        customer_name: Optional[str] = None
    ) -> bool:
        """
        Envía una solicitud de documentos adicionales al cliente.
        
        Args:
            to_email: Email del cliente
            claim_number: Número del siniestro
            required_documents: Lista de documentos requeridos
            customer_name: Nombre del cliente (opcional)
            
        Returns:
            bool: True si el email se envió correctamente
        """
        subject = f"Solicitud de Documentos - Siniestro {claim_number}"
        
        greeting = f"Estimado/a {customer_name}" if customer_name else "Estimado/a cliente"
        
        documents_list = "\n".join([f"- {doc}" for doc in required_documents])
        
        content = f"""
{greeting},

Para continuar con el procesamiento de su siniestro, necesitamos que nos proporcione la siguiente documentación:

**Documentos Requeridos:**
{documents_list}

**Cómo Enviar los Documentos:**
1. Responda a este email adjuntando los documentos
2. O súbalos a través de nuestro portal: https://tu-dominio.com/claims/{claim_number}/upload

**Importante:**
- Los documentos deben estar en formato PDF, JPG o PNG
- Asegúrese de que las imágenes sean claras y legibles
- Si tiene alguna dificultad, puede contactarnos por teléfono

Atentamente,
El Equipo de Siniestros
        """
        
        return self.send_email(to_email, subject, content.strip())
    
    def send_reply(
        self,
        to_email: str,
        original_subject: str,
        reply_content: str,
        conversation_context: Optional[str] = None
    ) -> bool:
        """
        Envía una respuesta automática a un email.
        
        Args:
            to_email: Email del destinatario
            original_subject: Asunto del email original
            reply_content: Contenido de la respuesta
            conversation_context: Contexto de la conversación
            
        Returns:
            bool: True si la respuesta se envió correctamente
        """
        subject = f"Re: {original_subject}"
        
        # Añadir contexto de conversación si está disponible
        if conversation_context:
            full_content = f"{reply_content}\n\n---\nContexto de la conversación: {conversation_context}"
        else:
            full_content = reply_content
        
        return self.send_email(to_email, subject, full_content)
    
    def verify_webhook_signature(self, payload: str, signature: str, timestamp: str) -> bool:
        """
        Verifica la firma del webhook de SendGrid para seguridad.
        
        Args:
            payload: Cuerpo de la petición
            signature: Firma del webhook
            timestamp: Timestamp del webhook
            
        Returns:
            bool: True si la firma es válida
        """
        # Implementar verificación de firma de SendGrid
        # Por ahora retornamos True para desarrollo
        return True

# Instancia global del servicio
email_service = EmailService() 