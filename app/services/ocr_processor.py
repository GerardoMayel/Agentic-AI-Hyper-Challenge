"""
Procesador asíncrono para OCR de documentos usando Gemini.
"""

import asyncio
import logging
import time
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.core.database import get_db
from app.core.models import DocumentOCR
from app.services.gemini_ocr_service import GeminiOCRService
from app.services.storage_service import StorageService

# Importar Document desde el modelo correcto
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))
from app.models.claim_models import Document

logger = logging.getLogger(__name__)

class OCRProcessor:
    """Procesador asíncrono para OCR de documentos."""
    
    def __init__(self):
        """Inicializa el procesador OCR."""
        self.gemini_service = GeminiOCRService()
        self.storage_service = StorageService()
        self.is_running = False
        self.processing_interval = 60  # segundos
        
    async def start_processing_loop(self):
        """Inicia el bucle de procesamiento continuo."""
        self.is_running = True
        logger.info("Iniciando bucle de procesamiento OCR")
        
        while self.is_running:
            try:
                await self.process_pending_documents()
                await asyncio.sleep(self.processing_interval)
            except Exception as e:
                logger.error(f"Error en bucle de procesamiento OCR: {str(e)}")
                await asyncio.sleep(10)  # Esperar antes de reintentar
    
    def stop_processing_loop(self):
        """Detiene el bucle de procesamiento."""
        self.is_running = False
        logger.info("Deteniendo bucle de procesamiento OCR")
    
    async def process_pending_documents(self):
        """Procesa todos los documentos pendientes de OCR."""
        try:
            # Obtener documentos pendientes
            pending_docs = self._get_pending_documents()
            
            if not pending_docs:
                logger.debug("No hay documentos pendientes de OCR")
                return
            
            logger.info(f"Procesando {len(pending_docs)} documentos pendientes de OCR")
            
            # Procesar cada documento
            for doc in pending_docs:
                try:
                    await self._process_single_document(doc)
                except Exception as e:
                    logger.error(f"Error procesando documento {doc.id}: {str(e)}")
                    self._mark_document_failed(doc.id, str(e))
                    
        except Exception as e:
            logger.error(f"Error en process_pending_documents: {str(e)}")
    
    def _get_pending_documents(self) -> List[Document]:
        """Obtiene documentos que necesitan procesamiento OCR."""
        db = next(get_db())
        try:
            # Buscar documentos que no tienen OCR o tienen OCR fallido
            pending_docs = db.query(Document).outerjoin(DocumentOCR).filter(
                and_(
                    Document.mime_type.like('image/%'),  # Solo imágenes
                    DocumentOCR.id.is_(None)  # No tiene OCR aún
                )
            ).limit(10).all()  # Limitar a 10 por vez
            
            return pending_docs
        finally:
            db.close()
    
    async def _process_single_document(self, document: Document):
        """Procesa un documento individual."""
        logger.info(f"Procesando documento {document.id}: {document.filename}")
        
        # Marcar como procesando
        self._mark_document_processing(document.id)
        
        try:
            # Descargar documento desde storage
            file_data = await self._download_document(document)
            
            if not file_data:
                raise Exception("No se pudo descargar el documento desde storage")
            
            # Procesar con Gemini OCR
            ocr_result = self.gemini_service.process_document_image(
                file_data, 
                document.filename
            )
            
            # Guardar resultado en base de datos
            self._save_ocr_result(document.id, ocr_result)
            
            logger.info(f"Documento {document.id} procesado exitosamente")
            
        except Exception as e:
            logger.error(f"Error procesando documento {document.id}: {str(e)}")
            self._mark_document_failed(document.id, str(e))
    
    async def _download_document(self, document: Document) -> Optional[bytes]:
        """Descarga un documento desde Google Cloud Storage."""
        try:
            if not document.storage_path:
                raise Exception("Documento no tiene path de storage")
            
            # Descargar desde GCS
            file_data = self.storage_service.download_file(document.storage_path)
            return file_data
            
        except Exception as e:
            logger.error(f"Error descargando documento {document.id}: {str(e)}")
            return None
    
    def _mark_document_processing(self, document_id: int):
        """Marca un documento como en procesamiento."""
        db = next(get_db())
        try:
            # Crear o actualizar registro OCR
            ocr_record = db.query(DocumentOCR).filter(
                DocumentOCR.document_id == document_id
            ).first()
            
            if not ocr_record:
                ocr_record = DocumentOCR(
                    document_id=document_id,
                    processing_status='processing',
                    processed_at=datetime.now()
                )
                db.add(ocr_record)
            else:
                ocr_record.processing_status = 'processing'
                ocr_record.processed_at = datetime.now()
                ocr_record.error_message = None
            
            db.commit()
            
        except Exception as e:
            logger.error(f"Error marcando documento {document_id} como procesando: {str(e)}")
            db.rollback()
        finally:
            db.close()
    
    def _save_ocr_result(self, document_id: int, ocr_result: dict):
        """Guarda el resultado del OCR en la base de datos."""
        db = next(get_db())
        try:
            # Buscar o crear registro OCR
            ocr_record = db.query(DocumentOCR).filter(
                DocumentOCR.document_id == document_id
            ).first()
            
            if not ocr_record:
                ocr_record = DocumentOCR(document_id=document_id)
                db.add(ocr_record)
            
            # Actualizar con resultados
            ocr_record.processing_status = ocr_result.get('processing_status', 'completed')
            ocr_record.processed_at = datetime.now()
            ocr_record.raw_text = ocr_result.get('raw_text')
            ocr_record.structured_data = ocr_result.get('structured_data')
            ocr_record.confidence_score = ocr_result.get('confidence_score')
            ocr_record.gemini_model_used = ocr_result.get('gemini_model_used')
            ocr_record.processing_time_seconds = ocr_result.get('processing_time_seconds')
            ocr_record.error_message = ocr_result.get('error_message')
            
            db.commit()
            
        except Exception as e:
            logger.error(f"Error guardando resultado OCR para documento {document_id}: {str(e)}")
            db.rollback()
        finally:
            db.close()
    
    def _mark_document_failed(self, document_id: int, error_message: str):
        """Marca un documento como fallido en OCR."""
        db = next(get_db())
        try:
            ocr_record = db.query(DocumentOCR).filter(
                DocumentOCR.document_id == document_id
            ).first()
            
            if not ocr_record:
                ocr_record = DocumentOCR(document_id=document_id)
                db.add(ocr_record)
            
            ocr_record.processing_status = 'failed'
            ocr_record.processed_at = datetime.now()
            ocr_record.error_message = error_message
            
            db.commit()
            
        except Exception as e:
            logger.error(f"Error marcando documento {document_id} como fallido: {str(e)}")
            db.rollback()
        finally:
            db.close()
    
    def process_document_immediately(self, document_id: int) -> bool:
        """
        Procesa un documento inmediatamente (síncrono).
        Útil para procesamiento bajo demanda.
        """
        try:
            db = next(get_db())
            document = db.query(Document).filter(
                Document.id == document_id
            ).first()
            
            if not document:
                logger.error(f"Documento {document_id} no encontrado")
                return False
            
            # Ejecutar procesamiento en el loop de eventos
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Si ya hay un loop corriendo, crear una tarea
                asyncio.create_task(self._process_single_document(document))
            else:
                # Si no hay loop, ejecutar directamente
                loop.run_until_complete(self._process_single_document(document))
            
            return True
            
        except Exception as e:
            logger.error(f"Error en process_document_immediately: {str(e)}")
            return False
        finally:
            db.close()

# Instancia global del procesador
ocr_processor = OCRProcessor() 