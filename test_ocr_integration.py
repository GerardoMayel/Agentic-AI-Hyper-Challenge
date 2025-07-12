#!/usr/bin/env python3
"""
Script de prueba para la integración OCR con las tablas existentes.
Prueba: CLAIM_FORM, DOCUMENTS y DOCUMENTS_OCR
"""

import os
import sys
import asyncio
from datetime import datetime
from dotenv import load_dotenv

# Agregar el directorio backend al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.core.database import get_db
# Importar desde el directorio backend
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
from app.models.claim_models import ClaimForm, Document
from app.services.storage_service import StorageService

load_dotenv()

def test_database_integration():
    """Prueba la integración entre las tablas existentes."""
    try:
        print("🔍 Probando integración de base de datos...")
        
        db = next(get_db())
        
        # 1. Crear un claim form de prueba
        print("📝 Creando claim form de prueba...")
        test_claim = ClaimForm(
            coverage_type="TRIP_CANCELLATION",
            full_name="Test User",
            email="test@example.com",
            phone="1234567890",
            policy_number="POL123456",
            incident_date=datetime.now(),
            incident_location="Test Location",
            description="Test incident description",
            estimated_amount=1000.0,
            status="PENDING"
        )
        
        db.add(test_claim)
        db.commit()
        db.refresh(test_claim)
        
        print(f"✅ Claim form creado: ID={test_claim.id}, Claim ID={test_claim.claim_id}")
        
        # 2. Crear un documento de prueba
        print("📄 Creando documento de prueba...")
        
        # Simular subida a storage
        storage_service = StorageService()
        test_file_content = b"fake_image_data_for_testing"
        storage_url = storage_service.upload_file(
            file_content=test_file_content,
            filename="test_receipt.jpg",
            numero_siniestro=test_claim.claim_id,
            email_id="test_email_123",
            content_type="image/jpeg"
        )
        
        if not storage_url:
            print("⚠️ No se pudo subir archivo a storage, usando URL simulada")
            storage_url = "https://storage.googleapis.com/test-bucket/test_receipt.jpg"
        
        test_document = Document(
            claim_form_id=test_claim.id,
            filename="test_receipt.jpg",
            original_filename="test_receipt.jpg",
            file_type="image/jpeg",
            file_size=len(test_file_content),
            document_type="RECEIPT",
            storage_url=storage_url,
            storage_path=f"documentos/{test_claim.claim_id}/test_receipt.jpg",
            uploaded_by="test_user",
            upload_notes="Test document for OCR"
        )
        
        db.add(test_document)
        db.commit()
        db.refresh(test_document)
        
        print(f"✅ Documento creado: ID={test_document.id}, Filename={test_document.filename}")
        
        # 3. Crear registro OCR de prueba
        print("🤖 Creando registro OCR de prueba...")
        
        # Usar SQL directo para evitar problemas de importación
        ocr_insert_sql = """
        INSERT INTO documents_ocr (
            document_id, processing_status, raw_text, structured_data, 
            confidence_score, gemini_model_used, processing_time_seconds
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s
        ) RETURNING id
        """
        
        from sqlalchemy import text
        result = db.execute(text(ocr_insert_sql), {
            'document_id': test_document.id,
            'processing_status': 'completed',
            'raw_text': 'Test receipt\nStore: Test Store\nDate: 2024-01-15\nTotal: $50.00',
            'structured_data': '{"merchant_name": "Test Store", "date": "2024-01-15", "total_amount": 50.00}',
            'confidence_score': 0.95,
            'gemini_model_used': 'gemini-1.5-flash',
            'processing_time_seconds': 2.5
        })
        
        ocr_id = result.fetchone()[0]
        db.commit()
        
        print(f"✅ Registro OCR creado: ID={ocr_id}")
        
        # 4. Verificar la integración
        print("🔍 Verificando integración...")
        
        # Consultar datos relacionados
        result = db.execute(text("""
            SELECT 
                cf.claim_id,
                cf.full_name,
                d.filename,
                d.document_type,
                doc.processing_status,
                doc.raw_text,
                doc.structured_data
            FROM CLAIM_FORM cf
            JOIN DOCUMENTS d ON cf.id = d.claim_form_id
            LEFT JOIN documents_ocr doc ON d.id = doc.document_id
            WHERE cf.id = :claim_id
        """), {'claim_id': test_claim.id})
        
        row = result.fetchone()
        if row:
            print("✅ Integración verificada:")
            print(f"   Claim ID: {row[0]}")
            print(f"   Claimant: {row[1]}")
            print(f"   Document: {row[2]} ({row[3]})")
            print(f"   OCR Status: {row[4]}")
            print(f"   Raw Text: {row[5][:50]}...")
            print(f"   Structured Data: {row[6]}")
        
        # 5. Limpiar datos de prueba
        print("🧹 Limpiando datos de prueba...")
        
        db.execute(text("DELETE FROM documents_ocr WHERE document_id = :doc_id"), 
                  {'doc_id': test_document.id})
        db.execute(text("DELETE FROM DOCUMENTS WHERE id = :doc_id"), 
                  {'doc_id': test_document.id})
        db.execute(text("DELETE FROM CLAIM_FORM WHERE id = :claim_id"), 
                  {'claim_id': test_claim.id})
        
        db.commit()
        print("✅ Datos de prueba eliminados")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en prueba: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def test_gemini_ocr_service():
    """Prueba el servicio de Gemini OCR."""
    try:
        print("\n🤖 Probando servicio Gemini OCR...")
        
        # Verificar que tenemos la API key
        if not os.getenv('GEMINI_API_KEY'):
            print("⚠️ GEMINI_API_KEY no configurada, saltando prueba de OCR")
            return None
        
        # Importar el servicio
        from app.services.gemini_ocr_service import GeminiOCRService
        
        gemini_service = GeminiOCRService()
        
        # Crear una imagen de prueba simple
        from PIL import Image, ImageDraw
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

if __name__ == "__main__":
    print("🚀 Probando integración OCR con tablas existentes")
    print("=" * 60)
    
    # Probar integración de base de datos
    db_success = test_database_integration()
    
    # Probar servicio Gemini OCR
    ocr_success = test_gemini_ocr_service()
    
    if db_success:
        print("\n🎉 Prueba de integración completada exitosamente")
    else:
        print("\n💥 Prueba de integración falló")
    
    if ocr_success:
        print("🎉 Prueba de OCR completada exitosamente")
    else:
        print("💥 Prueba de OCR falló o se saltó") 