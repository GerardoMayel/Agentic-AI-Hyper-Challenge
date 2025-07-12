#!/usr/bin/env python3
"""
Script de prueba completo para el flujo de OCR con Gemini.
Integra: Base de datos, Google Cloud Storage y Gemini OCR.
"""

import os
import sys
import asyncio
import time
from datetime import datetime
from dotenv import load_dotenv

# Agregar el directorio backend al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.core.database import get_db
from app.core.models import Claim, ClaimDocument, DocumentOCR
from app.services.storage_service import StorageService
from app.services.gemini_ocr_service import GeminiOCRService
from app.services.ocr_processor import OCRProcessor

load_dotenv()

def create_test_claim():
    """Crea un claim de prueba en la base de datos."""
    try:
        print("📝 Creando claim de prueba...")
        
        db = next(get_db())
        
        # Crear claim de prueba
        test_claim = Claim(
            claim_number="TEST-OCR-001",
            gmail_message_id="test_message_123",
            sender_email="test@example.com",
            sender_name="Test User",
            subject="Test Claim for OCR",
            email_content="This is a test claim for OCR processing",
            notification_date=datetime.now(),
            status="initial_notification"
        )
        
        db.add(test_claim)
        db.commit()
        db.refresh(test_claim)
        
        print(f"✅ Claim creado: ID={test_claim.id}, Number={test_claim.claim_number}")
        return test_claim
        
    except Exception as e:
        print(f"❌ Error creando claim: {e}")
        db.rollback()
        return None
    finally:
        db.close()

def create_test_document(claim_id: int):
    """Crea un documento de prueba y lo sube a storage."""
    try:
        print("📄 Creando documento de prueba...")
        
        # Crear contenido de imagen de prueba (simulado)
        test_image_content = b"fake_image_data_for_testing"
        filename = "test_receipt.jpg"
        
        # Subir a Google Cloud Storage
        storage_service = StorageService()
        storage_url = storage_service.upload_file(
            file_content=test_image_content,
            filename=filename,
            numero_siniestro="TEST-OCR-001",
            email_id="test_message_123",
            content_type="image/jpeg"
        )
        
        if not storage_url:
            print("❌ Error subiendo archivo a storage")
            return None
        
        # Guardar en base de datos
        db = next(get_db())
        
        test_document = ClaimDocument(
            claim_id=claim_id,
            filename=filename,
            mime_type="image/jpeg",
            file_size_bytes=len(test_image_content),
            storage_url=storage_url,
            storage_path=f"documentos/TEST-OCR-001/email-test_message_123/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}",
            source_type="web_form"
        )
        
        db.add(test_document)
        db.commit()
        db.refresh(test_document)
        
        print(f"✅ Documento creado: ID={test_document.id}, Filename={test_document.filename}")
        print(f"   Storage URL: {test_document.storage_url}")
        
        return test_document
        
    except Exception as e:
        print(f"❌ Error creando documento: {e}")
        db.rollback()
        return None
    finally:
        db.close()

def test_gemini_ocr_service():
    """Prueba el servicio de Gemini OCR con una imagen real."""
    try:
        print("🤖 Probando servicio Gemini OCR...")
        
        # Verificar que tenemos la API key
        if not os.getenv('GEMINI_API_KEY'):
            print("⚠️ GEMINI_API_KEY no configurada, saltando prueba de OCR")
            return None
        
        gemini_service = GeminiOCRService()
        
        # Crear una imagen de prueba simple (texto en imagen)
        from PIL import Image, ImageDraw, ImageFont
        import io
        
        # Crear imagen con texto
        img = Image.new('RGB', (400, 200), color='white')
        draw = ImageDraw.Draw(img)
        
        # Agregar texto de prueba
        text = "RECEIPT\nStore: Test Store\nDate: 2024-01-15\nTotal: $50.00"
        draw.text((20, 20), text, fill='black')
        
        # Convertir a bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_data = img_bytes.getvalue()
        
        # Procesar con Gemini
        result = gemini_service.process_document_image(img_data, "test_receipt.jpg")
        
        print("✅ OCR procesado exitosamente")
        print(f"   Status: {result.get('processing_status')}")
        print(f"   Processing time: {result.get('processing_time_seconds', 0):.3f}s")
        print(f"   Raw text: {result.get('raw_text', '')[:100]}...")
        
        if result.get('structured_data'):
            print(f"   Structured data: {result.get('structured_data')}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error en prueba de Gemini OCR: {e}")
        return None

async def test_ocr_processor():
    """Prueba el procesador OCR asíncrono."""
    try:
        print("⚙️ Probando procesador OCR asíncrono...")
        
        processor = OCRProcessor()
        
        # Obtener documentos pendientes
        pending_docs = processor._get_pending_documents()
        
        if not pending_docs:
            print("ℹ️ No hay documentos pendientes de OCR")
            return
        
        print(f"📋 Encontrados {len(pending_docs)} documentos pendientes")
        
        # Procesar el primer documento
        if pending_docs:
            doc = pending_docs[0]
            print(f"🔄 Procesando documento: {doc.filename}")
            
            # Procesar inmediatamente
            success = processor.process_document_immediately(doc.id)
            
            if success:
                print("✅ Documento procesado exitosamente")
            else:
                print("❌ Error procesando documento")
        
    except Exception as e:
        print(f"❌ Error en prueba de procesador OCR: {e}")

def test_ocr_results():
    """Verifica los resultados del OCR en la base de datos."""
    try:
        print("🔍 Verificando resultados de OCR...")
        
        db = next(get_db())
        
        # Buscar registros OCR
        ocr_records = db.query(DocumentOCR).all()
        
        if not ocr_records:
            print("ℹ️ No hay registros OCR en la base de datos")
            return
        
        print(f"📊 Encontrados {len(ocr_records)} registros OCR:")
        
        for record in ocr_records:
            print(f"\n📄 Documento ID: {record.document_id}")
            print(f"   Status: {record.processing_status}")
            print(f"   Processed at: {record.processed_at}")
            print(f"   Model: {record.gemini_model_used}")
            print(f"   Processing time: {record.processing_time_seconds}s")
            
            if record.raw_text is not None:
                print(f"   Raw text: {record.raw_text[:100]}...")
            
            if record.structured_data is not None:
                print(f"   Structured data: {record.structured_data}")
            
            if record.error_message is not None:
                print(f"   Error: {record.error_message}")
        
    except Exception as e:
        print(f"❌ Error verificando resultados: {e}")
    finally:
        db.close()

def cleanup_test_data():
    """Limpia los datos de prueba."""
    try:
        print("🧹 Limpiando datos de prueba...")
        
        db = next(get_db())
        
        # Eliminar registros OCR de prueba
        test_ocr_records = db.query(DocumentOCR).join(ClaimDocument).join(Claim).filter(
            Claim.claim_number == "TEST-OCR-001"
        ).all()
        
        for record in test_ocr_records:
            db.delete(record)
        
        # Eliminar documentos de prueba
        test_docs = db.query(ClaimDocument).join(Claim).filter(
            Claim.claim_number == "TEST-OCR-001"
        ).all()
        
        for doc in test_docs:
            db.delete(doc)
        
        # Eliminar claim de prueba
        test_claims = db.query(Claim).filter(
            Claim.claim_number == "TEST-OCR-001"
        ).all()
        
        for claim in test_claims:
            db.delete(claim)
        
        db.commit()
        
        print(f"✅ Limpieza completada: {len(test_ocr_records)} OCR, {len(test_docs)} docs, {len(test_claims)} claims")
        
    except Exception as e:
        print(f"❌ Error en limpieza: {e}")
        db.rollback()
    finally:
        db.close()

async def main():
    """Función principal de prueba."""
    print("🚀 Iniciando prueba completa del flujo OCR")
    print("=" * 60)
    
    try:
        # 1. Crear claim de prueba
        claim = create_test_claim()
        if not claim:
            return
        
        # 2. Crear documento de prueba
        document = create_test_document(claim.id)
        if not document:
            return
        
        # 3. Probar servicio Gemini OCR
        ocr_result = test_gemini_ocr_service()
        
        # 4. Probar procesador OCR asíncrono
        await test_ocr_processor()
        
        # 5. Verificar resultados
        test_ocr_results()
        
        # 6. Limpiar datos de prueba
        cleanup_test_data()
        
        print("\n🎉 Prueba completa finalizada exitosamente")
        
    except Exception as e:
        print(f"\n💥 Error en prueba principal: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 