#!/usr/bin/env python3
"""
Script completo para probar el flujo de:
1. Leer archivos del Google Cloud Storage
2. Procesarlos con OCR usando Gemini
3. Guardar resultados en la base de datos
"""

import sys
import os
from pathlib import Path
import asyncio
import io
from datetime import datetime

# Agregar el directorio backend al path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

# Agregar el directorio raíz al path para encontrar el .env
root_dir = backend_dir.parent
sys.path.insert(0, str(root_dir))

from dotenv import load_dotenv
load_dotenv()

# Configurar PYTHONPATH
os.environ['PYTHONPATH'] = f"{backend_dir}:{os.environ.get('PYTHONPATH', '')}"

from app.services.storage_service import StorageService
from app.services.gemini_ocr_service import GeminiOCRService
from app.core.database import get_db
from app.core.models import DocumentOCR

def test_storage_connection():
    """Prueba la conexión al Google Cloud Storage"""
    print("🔍 Probando conexión a Google Cloud Storage...")
    
    try:
        storage_service = StorageService()
        
        if not storage_service.bucket:
            print("❌ No se pudo conectar a Google Cloud Storage")
            print("   Verifica las credenciales en .env")
            return None
        
        print("✅ Conexión a Google Cloud Storage exitosa")
        print(f"   Bucket: {storage_service.bucket_name}")
        print(f"   Proyecto: {storage_service.project_id}")
        
        return storage_service
        
    except Exception as e:
        print(f"❌ Error conectando a Google Cloud Storage: {e}")
        return None

def test_gemini_ocr():
    """Prueba el servicio de OCR con Gemini"""
    print("\n🤖 Probando servicio de OCR con Gemini...")
    
    try:
        gemini_service = GeminiOCRService()
        print("✅ Servicio de OCR con Gemini inicializado")
        return gemini_service
        
    except Exception as e:
        print(f"❌ Error inicializando Gemini OCR: {e}")
        return None

def test_database_connection():
    """Prueba la conexión a la base de datos"""
    print("\n🗄️ Probando conexión a la base de datos...")
    
    try:
        db = next(get_db())
        # Hacer una consulta simple para verificar conexión
        from sqlalchemy import text
        result = db.execute(text("SELECT 1")).fetchone()
        db.close()
        
        if result:
            print("✅ Conexión a la base de datos exitosa")
            return True
        else:
            print("❌ No se pudo verificar la conexión a la base de datos")
            return False
            
    except Exception as e:
        print(f"❌ Error conectando a la base de datos: {e}")
        return False

def list_storage_files(storage_service):
    """Lista archivos en el storage para encontrar documentos procesables"""
    print("\n📁 Listando archivos en el storage...")
    
    try:
        # Listar archivos en la carpeta documentos
        files = storage_service.list_files(prefix="documentos/")
        
        if not files:
            print("⚠️ No se encontraron archivos en el storage")
            return []
        
        # Filtrar archivos procesables (imágenes y PDFs)
        processable_files = []
        for file_path in files:
            if any(ext in file_path.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.pdf']):
                processable_files.append(file_path)
        
        print(f"✅ Encontrados {len(processable_files)} archivos procesables:")
        for i, file_path in enumerate(processable_files[:5], 1):  # Mostrar solo los primeros 5
            file_type = "🖼️" if any(ext in file_path.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']) else "📕"
            print(f"   {i}. {file_type} {file_path}")
        
        if len(processable_files) > 5:
            print(f"   ... y {len(processable_files) - 5} más")
        
        return processable_files
        
    except Exception as e:
        print(f"❌ Error listando archivos: {e}")
        return []

def download_and_process_document(storage_service, gemini_service, file_path):
    """Descarga y procesa un documento con OCR"""
    print(f"\n📄 Procesando documento: {file_path}")
    
    try:
        # Descargar documento del storage
        print("   📥 Descargando documento...")
        file_data = storage_service.download_file(file_path)
        
        if not file_data:
            print("   ❌ No se pudo descargar el documento")
            return None
        
        print(f"   ✅ Documento descargado: {len(file_data)} bytes")
        
        # Determinar tipo de archivo
        filename = os.path.basename(file_path)
        file_extension = os.path.splitext(filename)[1].lower()
        
        # Procesar con OCR según el tipo de archivo
        print("   🔍 Procesando con OCR...")
        
        if file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
            # Es una imagen
            ocr_result = gemini_service.process_document_image(file_data, filename)
        elif file_extension == '.pdf':
            # Es un PDF
            ocr_result = gemini_service.process_document_pdf(file_data, filename)
        else:
            print(f"   ⚠️ Tipo de archivo no soportado: {file_extension}")
            return None
        
        if not ocr_result:
            print("   ❌ No se pudo procesar con OCR")
            return None
        
        print("   ✅ OCR completado exitosamente")
        print(f"   📝 Texto extraído: {len(ocr_result.get('raw_text', ''))} caracteres")
        print(f"   🎯 Confianza: {ocr_result.get('confidence_score', 'N/A')}")
        
        # Mostrar una muestra del texto extraído
        raw_text = ocr_result.get('raw_text', '')
        if raw_text:
            preview = raw_text[:200] + "..." if len(raw_text) > 200 else raw_text
            print(f"   📋 Vista previa: {preview}")
        
        return ocr_result
        
    except Exception as e:
        print(f"   ❌ Error procesando documento: {e}")
        return None

def save_ocr_result_to_db(image_path, ocr_result):
    """Guarda el resultado del OCR en la base de datos"""
    print("   💾 Guardando resultado en base de datos...")
    
    try:
        db = next(get_db())
        
        # Crear registro OCR con document_id temporal
        ocr_record = DocumentOCR(
            document_id=999,  # ID temporal para la prueba
            processing_status=ocr_result.get('processing_status', 'completed'),
            processed_at=datetime.now(),
            raw_text=ocr_result.get('raw_text'),
            structured_data=ocr_result.get('structured_data'),
            confidence_score=ocr_result.get('confidence_score'),
            gemini_model_used=ocr_result.get('gemini_model_used'),
            processing_time_seconds=ocr_result.get('processing_time_seconds'),
            error_message=ocr_result.get('error_message')
        )
        db.add(ocr_record)
        db.commit()
        
        print(f"   ✅ Resultado guardado en DB (OCR ID: {ocr_record.id})")
        print(f"   📝 Texto extraído: {ocr_result.get('raw_text', '')[:100]}...")
        db.close()
        return True
        
    except Exception as e:
        print(f"   ❌ Error guardando en DB: {e}")
        if 'db' in locals():
            db.rollback()
            db.close()
        return False

def test_complete_flow():
    """Prueba el flujo completo"""
    print("🚀 INICIANDO PRUEBA COMPLETA DE STORAGE + OCR")
    print("=" * 60)
    
    # 1. Probar conexión al storage
    storage_service = test_storage_connection()
    if not storage_service:
        print("❌ No se puede continuar sin conexión al storage")
        return False
    
    # 2. Probar servicio de OCR
    gemini_service = test_gemini_ocr()
    if not gemini_service:
        print("❌ No se puede continuar sin servicio de OCR")
        return False
    
    # 3. Probar conexión a la base de datos
    if not test_database_connection():
        print("❌ No se puede continuar sin conexión a la base de datos")
        return False
    
    # 4. Listar archivos procesables
    processable_files = list_storage_files(storage_service)
    if not processable_files:
        print("❌ No hay documentos procesables para procesar")
        return False
    
    # 5. Procesar el primer documento
    first_document = processable_files[0]
    ocr_result = download_and_process_document(storage_service, gemini_service, first_document)
    
    if not ocr_result:
        print("❌ No se pudo procesar el documento")
        return False
    
    # 6. Guardar resultado en la base de datos
    if save_ocr_result_to_db(first_document, ocr_result):
        print("\n🎉 ¡PRUEBA COMPLETA EXITOSA!")
        print("✅ Se pudo:")
        print("   - Conectar a Google Cloud Storage")
        print("   - Inicializar servicio de OCR con Gemini")
        print("   - Conectar a la base de datos")
        print("   - Descargar imagen del storage")
        print("   - Procesar imagen con OCR")
        print("   - Guardar resultado en la base de datos")
        return True
    else:
        print("\n❌ La prueba falló al guardar en la base de datos")
        return False

if __name__ == "__main__":
    success = test_complete_flow()
    
    if success:
        print("\n🎯 RESULTADO: Todo funciona correctamente")
        sys.exit(0)
    else:
        print("\n💥 RESULTADO: Hay problemas que necesitan ser resueltos")
        sys.exit(1) 