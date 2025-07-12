#!/usr/bin/env python3
"""
Script para procesar documentos del Google Cloud Storage con Gemini OCR
y guardar los resultados en la tabla DOCUMENTS_OCR.
"""

import os
import sys
import time
import json
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

# Añadir la raíz del repo al sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Importar módulos del proyecto
from app.core.database import engine
from app.services.storage_service import StorageService
from app.services.gemini_ocr_service import GeminiOCRService
from app.models.claim_models import Document
from app.core.models import DocumentOCR
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import text

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv('/Users/mayelmacbookm4pro/repos/Agentic-AI-Hyper-Challenge/.env')

# Crear sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class StorageDocumentOCRProcessor:
    def __init__(self):
        self.storage_service = StorageService()
        self.gemini_service = GeminiOCRService()
        
    def get_documents_from_storage(self) -> List[Dict[str, Any]]:
        """Obtiene la lista de documentos del Google Cloud Storage"""
        try:
            print("🔍 Buscando documentos en Google Cloud Storage...")
            
            bucket_name = os.getenv('GOOGLE_CLOUD_STORAGE_BUCKET')
            folder = os.getenv('GOOGLE_CLOUD_STORAGE_FOLDER', 'documentos')
            
            if not bucket_name:
                raise ValueError("GOOGLE_CLOUD_STORAGE_BUCKET no está configurado en .env")
            
            # Listar archivos usando el cliente del storage service
            blobs = self.storage_service.client.list_blobs(bucket_name, prefix=folder)
            
            documents = []
            for blob in blobs:
                # Solo procesar archivos de imagen
                if blob.name.lower().endswith(('.jpg', '.jpeg', '.png', '.pdf', '.tiff', '.bmp')):
                    documents.append({
                        'name': blob.name,
                        'size': blob.size,
                        'updated': blob.updated,
                        'bucket': bucket_name
                    })
            
            print(f"✅ Encontrados {len(documents)} documentos para procesar")
            return documents
            
        except Exception as e:
            print(f"❌ Error obteniendo documentos del storage: {e}")
            return []
    
    def get_document_from_db(self, filename: str) -> Document:
        """Busca un documento en la base de datos por nombre de archivo"""
        try:
            db = SessionLocal()
            # Buscar documento por filename
            document = db.query(Document).filter(
                Document.filename == filename
            ).first()
            db.close()
            return document
        except Exception as e:
            print(f"❌ Error buscando documento en DB: {e}")
            return None
    
    def check_if_ocr_processed(self, document_id: int) -> bool:
        """Verifica si un documento ya fue procesado con OCR"""
        try:
            db = SessionLocal()
            ocr_record = db.query(DocumentOCR).filter(
                DocumentOCR.document_id == document_id,
                DocumentOCR.processing_status == 'completed'
            ).first()
            db.close()
            return ocr_record is not None
        except Exception as e:
            print(f"❌ Error verificando OCR: {e}")
            return False
    
    def download_document(self, bucket_name: str, blob_name: str) -> bytes:
        """Descarga un documento del storage"""
        try:
            blob = self.storage_service.bucket.blob(blob_name)
            return blob.download_as_bytes()
        except Exception as e:
            print(f"❌ Error descargando archivo: {e}")
            return None
    
    def process_document_with_gemini(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Procesa un documento con Gemini OCR"""
        try:
            print(f"🔍 Procesando con Gemini OCR...")
            start_time = time.time()
            
            # Procesar con Gemini OCR usando el método correcto
            ocr_result = self.gemini_service.process_document_image(file_content, filename)
            
            processing_time = time.time() - start_time
            
            return {
                'success': True,
                'raw_text': ocr_result.get('raw_text', ''),
                'structured_data': ocr_result.get('structured_data', {}),
                'confidence_score': ocr_result.get('confidence_score', 0.0),
                'processing_time': processing_time,
                'error': None
            }
            
        except Exception as e:
            print(f"❌ Error procesando documento: {e}")
            return {
                'success': False,
                'raw_text': '',
                'structured_data': {},
                'confidence_score': 0.0,
                'processing_time': 0.0,
                'error': str(e)
            }
    
    def save_ocr_result(self, document_id: int, ocr_result: Dict[str, Any]) -> bool:
        """Guarda el resultado del OCR en la base de datos"""
        try:
            db = SessionLocal()
            
            # Crear registro OCR
            ocr_record = DocumentOCR(
                document_id=document_id,
                processed_at=datetime.utcnow(),
                processing_status='completed' if ocr_result['success'] else 'failed',
                error_message=ocr_result.get('error'),
                raw_text=ocr_result.get('raw_text', ''),
                structured_data=ocr_result.get('structured_data', {}),
                confidence_score=ocr_result.get('confidence_score', 0.0),
                gemini_model_used='gemini-1.5-flash',
                processing_time_seconds=ocr_result.get('processing_time', 0.0),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            db.add(ocr_record)
            db.commit()
            db.close()
            
            print(f"✅ OCR guardado en DB para documento ID: {document_id}")
            return True
            
        except Exception as e:
            print(f"❌ Error guardando OCR en DB: {e}")
            return False
    
    def process_all_documents(self):
        """Procesa todos los documentos del storage con OCR"""
        print("🚀 INICIANDO PROCESAMIENTO OCR DE DOCUMENTOS DEL STORAGE")
        print("=" * 60)
        
        # Obtener documentos del storage
        storage_documents = self.get_documents_from_storage()
        
        if not storage_documents:
            print("📭 No se encontraron documentos para procesar")
            return
        
        processed_count = 0
        success_count = 0
        error_count = 0
        
        for doc_info in storage_documents:
            try:
                print(f"\n📄 Procesando: {doc_info['name']}")
                
                # Buscar documento en la base de datos
                db_document = self.get_document_from_db(doc_info['name'])
                
                if not db_document:
                    print(f"⚠️  Documento no encontrado en DB: {doc_info['name']}")
                    continue
                
                # Verificar si ya fue procesado
                if self.check_if_ocr_processed(db_document.id):
                    print(f"⏭️  Documento ya procesado: {doc_info['name']}")
                    continue
                
                # Descargar documento
                file_content = self.download_document(doc_info['bucket'], doc_info['name'])
                if not file_content:
                    print(f"❌ No se pudo descargar: {doc_info['name']}")
                    continue
                
                # Procesar documento
                ocr_result = self.process_document_with_gemini(file_content, doc_info['name'])
                
                # Guardar resultado
                if self.save_ocr_result(db_document.id, ocr_result):
                    success_count += 1
                    print(f"✅ Procesado exitosamente: {doc_info['name']}")
                else:
                    error_count += 1
                    print(f"❌ Error guardando resultado: {doc_info['name']}")
                
                processed_count += 1
                
                # Pausa entre documentos para no sobrecargar la API
                time.sleep(2)
                
            except Exception as e:
                error_count += 1
                print(f"❌ Error procesando {doc_info['name']}: {e}")
        
        print("\n" + "=" * 60)
        print("📊 RESUMEN DEL PROCESAMIENTO")
        print("=" * 60)
        print(f"📄 Documentos encontrados: {len(storage_documents)}")
        print(f"🔄 Documentos procesados: {processed_count}")
        print(f"✅ Exitosos: {success_count}")
        print(f"❌ Errores: {error_count}")
        print("=" * 60)

def main():
    """Función principal"""
    try:
        processor = StorageDocumentOCRProcessor()
        processor.process_all_documents()
        
    except Exception as e:
        print(f"💥 Error en el procesamiento: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 