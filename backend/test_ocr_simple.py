#!/usr/bin/env python3
"""
Script simple para probar la integración OCR con las tablas existentes.
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

def test_ocr_integration():
    """Prueba la integración OCR con las tablas existentes."""
    try:
        print("🔍 Probando integración OCR...")
        
        # Conectar a la base de datos
        from app.core.database import DATABASE_URL
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            # 1. Verificar que las tablas existen
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_name IN ('CLAIM_FORM', 'DOCUMENTS', 'documents_ocr')
                ORDER BY table_name
            """))
            
            tables = [row[0] for row in result]
            print(f"📋 Tablas encontradas: {tables}")
            
            if len(tables) != 3:
                print("❌ Faltan tablas necesarias")
                return False
            
            # 2. Crear un claim form de prueba
            print("📝 Creando claim form de prueba...")
            
            claim_insert = """
            INSERT INTO "CLAIM_FORM" (
                claim_id, coverage_type, full_name, email, phone, 
                policy_number, incident_date, incident_location, description, estimated_amount, status
            ) VALUES (
                'TEST-OCR-001', 'TRIP_CANCELLATION', 'Test User', 'test@example.com', '1234567890',
                'POL123456', NOW(), 'Test Location', 'Test incident description', 1000.0, 'PENDING'
            ) RETURNING id, claim_id
            """
            
            result = conn.execute(text(claim_insert))
            claim_data = result.fetchone()
            claim_id = claim_data[0]
            claim_number = claim_data[1]
            conn.commit()
            
            print(f"✅ Claim form creado: ID={claim_id}, Claim ID={claim_number}")
            
            # 3. Crear un documento de prueba
            print("📄 Creando documento de prueba...")
            
            doc_insert = """
            INSERT INTO "DOCUMENTS" (
                claim_form_id, filename, original_filename, file_type, file_size,
                document_type, storage_url, storage_path, uploaded_by, upload_notes
            ) VALUES (
                :claim_id, 'test_receipt.jpg', 'test_receipt.jpg', 'image/jpeg', 1024,
                'RECEIPT', 'https://storage.googleapis.com/test-bucket/test_receipt.jpg',
                'documentos/TEST-OCR-001/test_receipt.jpg', 'test_user', 'Test document for OCR'
            ) RETURNING id
            """
            
            result = conn.execute(text(doc_insert), {'claim_id': claim_id})
            doc_id = result.fetchone()[0]
            conn.commit()
            
            print(f"✅ Documento creado: ID={doc_id}")
            
            # 4. Crear registro OCR de prueba
            print("🤖 Creando registro OCR de prueba...")
            
            ocr_insert = """
            INSERT INTO documents_ocr (
                document_id, processing_status, raw_text, structured_data,
                confidence_score, gemini_model_used, processing_time_seconds
            ) VALUES (
                :doc_id, 'completed', 'Test receipt\nStore: Test Store\nDate: 2024-01-15\nTotal: $50.00',
                '{"merchant_name": "Test Store", "date": "2024-01-15", "total_amount": 50.00}',
                0.95, 'gemini-1.5-flash', 2.5
            ) RETURNING id
            """
            
            result = conn.execute(text(ocr_insert), {'doc_id': doc_id})
            ocr_id = result.fetchone()[0]
            conn.commit()
            
            print(f"✅ Registro OCR creado: ID={ocr_id}")
            
            # 5. Verificar la integración
            print("🔍 Verificando integración...")
            
            integration_query = """
            SELECT 
                cf.claim_id,
                cf.full_name,
                d.filename,
                d.document_type,
                doc.processing_status,
                doc.raw_text,
                doc.structured_data
            FROM "CLAIM_FORM" cf
            JOIN "DOCUMENTS" d ON cf.id = d.claim_form_id
            LEFT JOIN documents_ocr doc ON d.id = doc.document_id
            WHERE cf.id = :claim_id
            """
            
            result = conn.execute(text(integration_query), {'claim_id': claim_id})
            row = result.fetchone()
            
            if row:
                print("✅ Integración verificada:")
                print(f"   Claim ID: {row[0]}")
                print(f"   Claimant: {row[1]}")
                print(f"   Document: {row[2]} ({row[3]})")
                print(f"   OCR Status: {row[4]}")
                print(f"   Raw Text: {row[5][:50]}...")
                print(f"   Structured Data: {row[6]}")
            
            # 6. Limpiar datos de prueba
            print("🧹 Limpiando datos de prueba...")
            
            conn.execute(text("DELETE FROM documents_ocr WHERE document_id = :doc_id"), 
                        {'doc_id': doc_id})
            conn.execute(text('DELETE FROM "DOCUMENTS" WHERE id = :doc_id'), 
                        {'doc_id': doc_id})
            conn.execute(text('DELETE FROM "CLAIM_FORM" WHERE id = :claim_id'), 
                        {'claim_id': claim_id})
            conn.commit()
            
            print("✅ Datos de prueba eliminados")
            
            return True
            
    except Exception as e:
        print(f"❌ Error en prueba: {e}")
        return False

def test_gemini_service():
    """Prueba el servicio de Gemini OCR."""
    try:
        print("\n🤖 Probando servicio Gemini OCR...")
        
        # Verificar API key
        if not os.getenv('GEMINI_API_KEY'):
            print("⚠️ GEMINI_API_KEY no configurada, saltando prueba de OCR")
            return None
        
        # Importar servicio
        from app.services.gemini_ocr_service import GeminiOCRService
        
        gemini_service = GeminiOCRService()
        
        # Crear imagen de prueba
        from PIL import Image, ImageDraw
        import io
        
        img = Image.new('RGB', (400, 200), color='white')
        draw = ImageDraw.Draw(img)
        text = "RECEIPT\nStore: Test Store\nDate: 2024-01-15\nTotal: $50.00"
        draw.text((20, 20), text, fill='black')
        
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
    db_success = test_ocr_integration()
    
    # Probar servicio Gemini OCR
    ocr_success = test_gemini_service()
    
    if db_success:
        print("\n🎉 Prueba de integración completada exitosamente")
    else:
        print("\n💥 Prueba de integración falló")
    
    if ocr_success:
        print("🎉 Prueba de OCR completada exitosamente")
    else:
        print("💥 Prueba de OCR falló o se saltó") 