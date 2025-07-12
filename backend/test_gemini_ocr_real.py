#!/usr/bin/env python3
import os
from sqlalchemy import create_engine, text
from app.core.database import DATABASE_URL
from app.models.claim_models import Document
from app.services.gemini_ocr_service import GeminiOCRService
from datetime import datetime
from PIL import Image, ImageDraw
import io

# 1. Crear una imagen de prueba
img = Image.new('RGB', (400, 200), color='white')
draw = ImageDraw.Draw(img)
draw.text((20, 20), "RECEIPT\nStore: Test Store\nDate: 2024-01-15\nTotal: $50.00", fill='black')
img_bytes = io.BytesIO()
img.save(img_bytes, format='JPEG')
img_data = img_bytes.getvalue()

# 2. Crear un documento de prueba en la base de datos
engine = create_engine(DATABASE_URL)
with engine.connect() as conn:
    # Insertar en DOCUMENTS
    result = conn.execute(text('''
        INSERT INTO "DOCUMENTS" (
            claim_form_id, filename, original_filename, file_type, file_size,
            document_type, storage_url, storage_path, uploaded_by, upload_notes, uploaded_at
        ) VALUES (
            1, 'test_receipt.jpg', 'test_receipt.jpg', 'image/jpeg', :size,
            'RECEIPT', 'https://storage.googleapis.com/test-bucket/test_receipt.jpg',
            'documentos/TEST-OCR-REAL/test_receipt.jpg', 'test_user', 'Test Gemini OCR', :now
        ) RETURNING id
    '''), {'size': len(img_data), 'now': datetime.now()})
    doc_id = result.fetchone()[0]
    conn.commit()

    # 3. Procesar con Gemini OCR
    gemini = GeminiOCRService()
    ocr_result = gemini.process_document_image(img_data, "test_receipt.jpg")

    # 4. Insertar resultado en documents_ocr
    conn.execute(text('''
        INSERT INTO documents_ocr (
            document_id, processing_status, raw_text, structured_data, confidence_score, gemini_model_used, processing_time_seconds, created_at, updated_at
        ) VALUES (
            :doc_id, :status, :raw_text, :structured_data, :confidence, :model, :ptime, :now, :now
        )
    '''), {
        'doc_id': doc_id,
        'status': ocr_result.get('processing_status', 'completed'),
        'raw_text': ocr_result.get('raw_text'),
        'structured_data': str(ocr_result.get('structured_data')),
        'confidence': ocr_result.get('confidence_score'),
        'model': ocr_result.get('gemini_model_used'),
        'ptime': ocr_result.get('processing_time_seconds'),
        'now': datetime.now()
    })
    conn.commit()

    print("\n✅ Resultado OCR guardado en la base de datos.\n")
    # 5. Mostrar el resultado
    result = conn.execute(text('SELECT * FROM documents_ocr WHERE document_id = :doc_id ORDER BY id DESC LIMIT 1'), {'doc_id': doc_id})
    for row in result:
        print("-" * 60)
        for k, v in dict(row).items():
            print(f"{k}: {v}") 