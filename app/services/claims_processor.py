"""
Servicio principal para procesar emails de claims automáticamente.
"""

import os
import re
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from app.core.models import EmailRecibido, DocumentoAdjunto, SiniestroReportado, Base
from app.core.database import get_db, engine
from app.services.storage_service import storage_service_gcs
from app.core.models import generar_numero_siniestro, extraer_info_remitente, es_nuevo_siniestro

load_dotenv()

class ClaimsProcessor:
    """Servicio para procesar emails de claims automáticamente."""
    
    def __init__(self):
        self.gmail_user = os.getenv('GMAIL_USER_EMAIL', 'gerardo_mayel_fernandez_alamilla@chiefdataaiofficer.com')
    
    def procesar_email_gmail(self, email_data: Dict) -> Dict:
        """
        Procesa un email de Gmail y determina si es un claim.
        
        Args:
            email_data: Datos del email extraídos de Gmail API
            
        Returns:
            Diccionario con el resultado del procesamiento
        """
        try:
            # Verificar si el email ya fue procesado
            db = next(get_db())
            email_existente = db.query(EmailRecibido).filter_by(
                gmail_message_id=email_data['id']
            ).first()
            
            if email_existente:
                print(f"⚠️ Email ya procesado: {email_data['id']}")
                return {
                    'status': 'already_processed',
                    'email_id': email_existente.id,
                    'message': 'Email ya fue procesado anteriormente'
                }
            
            # Extraer información básica
            subject = email_data.get('subject', '')
            from_header = email_data.get('from', '')
            to_header = email_data.get('to', '')
            date_header = email_data.get('date', '')
            text_content = email_data.get('text_content', '')
            html_content = email_data.get('html_content', '')
            snippet = email_data.get('snippet', '')
            attachments = email_data.get('attachments', [])
            
            # Verificar si contiene palabras clave de claim
            if not self._contiene_palabras_claim(subject, text_content, html_content):
                print(f"⚠️ Email no contiene palabras clave de claim: {subject}")
                return {
                    'status': 'no_claim_keywords',
                    'message': 'Email no contiene palabras clave de claim'
                }
            
            # Extraer información del remitente
            remitente_email, remitente_nombre = extraer_info_remitente(from_header)
            
            # Parsear fecha
            fecha_recibido = self._parsear_fecha(date_header)
            
            # Determinar si es nuevo siniestro
            es_nuevo = es_nuevo_siniestro(remitente_email, subject, text_content)
            
            # Crear registro de email
            email_recibido = EmailRecibido(
                gmail_message_id=email_data['id'],
                thread_id=email_data.get('thread_id', ''),
                remitente_email=remitente_email,
                remitente_nombre=remitente_nombre,
                destinatario_email=to_header,
                subject=subject,
                contenido_texto=text_content,
                contenido_html=html_content,
                snippet=snippet,
                fecha_recibido=fecha_recibido,
                metadata=email_data.get('metadata', {}),
                headers=email_data.get('headers', {}),
                es_nuevo_siniestro=es_nuevo,
                estado_procesamiento='procesando'
            )
            
            db.add(email_recibido)
            db.commit()
            db.refresh(email_recibido)
            
            print(f"✅ Email registrado: {email_recibido.id}")
            
            # Procesar adjuntos
            documentos_procesados = []
            if attachments:
                documentos_procesados = self._procesar_adjuntos(
                    db, email_recibido, attachments, email_data['id']
                )
            
            # Procesar siniestro
            resultado_siniestro = None
            if es_nuevo:
                resultado_siniestro = self._crear_nuevo_siniestro(db, email_recibido)
            else:
                resultado_siniestro = self._vincular_siniestro_existente(db, email_recibido)
            
            # Actualizar estado del email
            email_recibido.estado_procesamiento = 'completado'
            if resultado_siniestro and resultado_siniestro.get('numero_siniestro'):
                email_recibido.numero_siniestro = resultado_siniestro['numero_siniestro']
            
            db.commit()
            
            return {
                'status': 'success',
                'email_id': email_recibido.id,
                'es_nuevo_siniestro': es_nuevo,
                'numero_siniestro': resultado_siniestro.get('numero_siniestro') if resultado_siniestro else None,
                'documentos_procesados': len(documentos_procesados),
                'message': 'Email procesado exitosamente'
            }
            
        except Exception as e:
            print(f"❌ Error procesando email: {e}")
            return {
                'status': 'error',
                'message': f'Error procesando email: {str(e)}'
            }
        finally:
            db.close()
    
    def _contiene_palabras_claim(self, subject: str, text_content: str, html_content: str) -> bool:
        """
        Verifica si el email contiene palabras clave relacionadas con claims.
        
        Args:
            subject: Asunto del email
            text_content: Contenido de texto
            html_content: Contenido HTML
            
        Returns:
            True si contiene palabras clave de claim
        """
        palabras_clave = [
            'claim', 'claims', 'siniestro', 'siniestros', 'accidente', 'daño',
            'pérdida', 'robo', 'incendio', 'reclamo', 'reclamos', 'avería',
            'breakdown', 'damage', 'loss', 'theft', 'fire', 'accident'
        ]
        
        texto_completo = f"{subject} {text_content} {html_content}".lower()
        
        for palabra in palabras_clave:
            if palabra in texto_completo:
                return True
        
        return False
    
    def _parsear_fecha(self, date_header: str) -> datetime:
        """
        Parsea la fecha del header del email.
        
        Args:
            date_header: Header de fecha del email
            
        Returns:
            Objeto datetime
        """
        try:
            # Intentar parsear con diferentes formatos
            formatos = [
                '%a, %d %b %Y %H:%M:%S %z',  # RFC 2822
                '%d %b %Y %H:%M:%S %z',      # Sin día de la semana
                '%a, %d %b %Y %H:%M:%S',     # Sin zona horaria
                '%d %b %Y %H:%M:%S'          # Formato simple
            ]
            
            for formato in formatos:
                try:
                    return datetime.strptime(date_header, formato)
                except ValueError:
                    continue
            
            # Si no se puede parsear, usar fecha actual
            print(f"⚠️ No se pudo parsear fecha: {date_header}")
            return datetime.now()
            
        except Exception as e:
            print(f"❌ Error parseando fecha: {e}")
            return datetime.now()
    
    def _procesar_adjuntos(self, db: Session, email_recibido: EmailRecibido, 
                          attachments: List[Dict], email_id: str) -> List[Dict]:
        """
        Procesa los adjuntos del email.
        
        Args:
            db: Sesión de base de datos
            email_recibido: Registro del email
            attachments: Lista de adjuntos
            email_id: ID del email de Gmail
            
        Returns:
            Lista de documentos procesados
        """
        documentos_procesados = []
        
        for attachment in attachments:
            try:
                # Crear registro de documento
                documento = DocumentoAdjunto(
                    email_id=email_recibido.id,
                    nombre_archivo=attachment['filename'],
                    tipo_mime=attachment['mime_type'],
                    tamaño_bytes=attachment['size'],
                    gmail_attachment_id=attachment['attachment_id'],
                    es_imagen=attachment['is_image'],
                    es_documento=attachment['is_document']
                )
                
                db.add(documento)
                db.commit()
                db.refresh(documento)
                
                print(f"✅ Documento registrado: {documento.nombre_archivo}")
                documentos_procesados.append(documento)
                
            except Exception as e:
                print(f"❌ Error procesando adjunto {attachment.get('filename', 'N/A')}: {e}")
                continue
        
        return documentos_procesados
    
    def _crear_nuevo_siniestro(self, db: Session, email_recibido: EmailRecibido) -> Dict:
        """
        Crea un nuevo siniestro.
        
        Args:
            db: Sesión de base de datos
            email_recibido: Registro del email
            
        Returns:
            Diccionario con información del siniestro creado
        """
        try:
            # Generar número único de siniestro
            numero_siniestro = generar_numero_siniestro()
            
            # Extraer información adicional del contenido
            info_adicional = self._extraer_info_siniestro(
                email_recibido.subject,
                email_recibido.contenido_texto,
                email_recibido.contenido_html
            )
            
            # Crear siniestro
            siniestro = SiniestroReportado(
                numero_siniestro=numero_siniestro,
                email_inicial_id=email_recibido.id,
                remitente_email=email_recibido.remitente_email,
                remitente_nombre=email_recibido.remitente_nombre,
                fecha_reporte=email_recibido.fecha_recibido,
                fecha_siniestro=info_adicional.get('fecha_siniestro'),
                tipo_siniestro=info_adicional.get('tipo_siniestro'),
                descripcion=info_adicional.get('descripcion'),
                asegurado=info_adicional.get('asegurado'),
                numero_poliza=info_adicional.get('numero_poliza'),
                monto_estimado=info_adicional.get('monto_estimado'),
                ubicacion_siniestro=info_adicional.get('ubicacion_siniestro')
            )
            
            db.add(siniestro)
            db.commit()
            db.refresh(siniestro)
            
            print(f"✅ Nuevo siniestro creado: {numero_siniestro}")
            
            return {
                'numero_siniestro': numero_siniestro,
                'siniestro_id': siniestro.id,
                'message': 'Nuevo siniestro creado exitosamente'
            }
            
        except Exception as e:
            print(f"❌ Error creando siniestro: {e}")
            return {
                'error': str(e),
                'message': 'Error creando siniestro'
            }
    
    def _vincular_siniestro_existente(self, db: Session, email_recibido: EmailRecibido) -> Dict:
        """
        Vincula el email a un siniestro existente.
        
        Args:
            db: Sesión de base de datos
            email_recibido: Registro del email
            
        Returns:
            Diccionario con información del siniestro vinculado
        """
        try:
            # Buscar siniestro existente por remitente
            siniestro_existente = db.query(SiniestroReportado).filter_by(
                remitente_email=email_recibido.remitente_email
            ).order_by(SiniestroReportado.fecha_reporte.desc()).first()
            
            if siniestro_existente:
                print(f"✅ Email vinculado a siniestro existente: {siniestro_existente.numero_siniestro}")
                return {
                    'numero_siniestro': siniestro_existente.numero_siniestro,
                    'siniestro_id': siniestro_existente.id,
                    'message': 'Email vinculado a siniestro existente'
                }
            else:
                # Si no hay siniestro existente, crear uno nuevo
                print("⚠️ No se encontró siniestro existente, creando nuevo")
                return self._crear_nuevo_siniestro(db, email_recibido)
                
        except Exception as e:
            print(f"❌ Error vinculando siniestro: {e}")
            return {
                'error': str(e),
                'message': 'Error vinculando siniestro'
            }
    
    def _extraer_info_siniestro(self, subject: str, text_content: str, html_content: str) -> Dict:
        """
        Extrae información adicional del siniestro del contenido del email.
        
        Args:
            subject: Asunto del email
            text_content: Contenido de texto
            html_content: Contenido HTML
            
        Returns:
            Diccionario con información extraída
        """
        info = {}
        
        # Extraer número de póliza
        poliza_pattern = r'\b(?:póliza|poliza|policy)\s*(?:número|numero|#|no\.?)?\s*:?\s*([A-Z0-9\-]+)\b'
        poliza_match = re.search(poliza_pattern, f"{subject} {text_content}", re.IGNORECASE)
        if poliza_match:
            info['numero_poliza'] = poliza_match.group(1)
        
        # Extraer monto estimado
        monto_pattern = r'\b(?:monto|amount|valor|value|costo|cost)\s*:?\s*\$?\s*([0-9,]+(?:\.[0-9]{2})?)\b'
        monto_match = re.search(monto_pattern, f"{subject} {text_content}", re.IGNORECASE)
        if monto_match:
            try:
                monto_str = monto_match.group(1).replace(',', '')
                info['monto_estimado'] = float(monto_str)
            except ValueError:
                pass
        
        # Extraer tipo de siniestro
        tipos_siniestro = {
            'accidente': ['accidente', 'accident', 'colisión', 'collision'],
            'robo': ['robo', 'theft', 'hurto', 'robbery'],
            'incendio': ['incendio', 'fire', 'fuego'],
            'daño': ['daño', 'damage', 'avería', 'breakdown'],
            'pérdida': ['pérdida', 'loss', 'perdida']
        }
        
        texto_completo = f"{subject} {text_content}".lower()
        for tipo, palabras in tipos_siniestro.items():
            if any(palabra in texto_completo for palabra in palabras):
                info['tipo_siniestro'] = tipo
                break
        
        # Extraer descripción (primeras 500 caracteres del contenido)
        if text_content:
            info['descripcion'] = text_content[:500] + '...' if len(text_content) > 500 else text_content
        
        return info

# Instancia global del procesador
claims_processor = ClaimsProcessor() 