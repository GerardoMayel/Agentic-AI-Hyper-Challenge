#!/usr/bin/env python3
"""
Script simplificado para probar el flujo de:
1. Leer archivos del Google Cloud Storage
2. Procesarlos con OCR usando Gemini
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from dotenv import load_dotenv
load_dotenv()

from app.services.storage_service import StorageService
from app.services.gemini_ocr_service import GeminiOCRService

def test_storage_connection():
    """Prueba la conexión al Google Cloud Storage"""
    print("🔍 Probando conexión a Google Cloud Storage...")
    
    try:
        storage_service = StorageService()
        
        if not storage_service.bucket:
            print("❌ No se pudo conectar a Google Cloud Storage")
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
        for i, file_path in enumerate(processable_files[:5], 1):
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
        
        # Mostrar datos estructurados si están disponibles
        structured_data = ocr_result.get('structured_data')
        if structured_data:
            print(f"   📊 Datos estructurados: {json.dumps(structured_data, indent=2, ensure_ascii=False)}")
        
        return ocr_result
        
    except Exception as e:
        print(f"   ❌ Error procesando documento: {e}")
        return None

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
    
    # 3. Listar archivos procesables
    processable_files = list_storage_files(storage_service)
    if not processable_files:
        print("❌ No hay documentos procesables para procesar")
        return False
    
    # 4. Procesar el primer documento
    first_document = processable_files[0]
    ocr_result = download_and_process_document(storage_service, gemini_service, first_document)
    
    if not ocr_result:
        print("❌ No se pudo procesar el documento")
        return False
    
    print("\n🎉 ¡PRUEBA COMPLETA EXITOSA!")
    print("✅ Se pudo:")
    print("   - Conectar a Google Cloud Storage")
    print("   - Inicializar servicio de OCR con Gemini")
    print("   - Descargar documento del storage")
    print("   - Procesar documento con OCR")
    print("   - Extraer texto y datos estructurados")
    
    return True

if __name__ == "__main__":
    import json
    
    success = test_complete_flow()
    
    if success:
        print("\n🎯 RESULTADO: Todo funciona correctamente")
        print("✅ El flujo de Storage + OCR está operativo")
        sys.exit(0)
    else:
        print("\n💥 RESULTADO: Hay problemas que necesitan ser resueltos")
        sys.exit(1) 