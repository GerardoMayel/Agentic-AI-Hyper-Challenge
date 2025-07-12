#!/usr/bin/env python3
"""
Script para probar específicamente el servicio de Google Cloud Storage
"""

import sys
import os
from pathlib import Path
import io
import asyncio

# Agregar el directorio backend al path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

# Agregar el directorio raíz al path para encontrar el .env
root_dir = backend_dir.parent
sys.path.insert(0, str(root_dir))

from backend.app.services.storage_service import StorageService

async def test_storage_service():
    """Probar el servicio de Google Cloud Storage"""
    print("🧪 Probando Google Cloud Storage Service...")
    
    try:
        # Crear instancia del servicio
        storage_service = StorageService()
        print("✅ StorageService creado exitosamente")
        
        # Crear archivo de prueba
        test_content = "Este es un archivo de prueba para verificar Google Cloud Storage"
        test_file = io.BytesIO(test_content.encode('utf-8'))
        test_file.name = "test_storage.txt"
        
        print("📁 Subiendo archivo de prueba...")
        
        # Subir archivo usando solo argumentos posicionales
        result = await storage_service.upload_file(
            test_file,
            "TEST-STORAGE",
            "test_document",
            "test_storage.txt"
        )
        
        print("✅ Archivo subido exitosamente")
        print(f"   📄 Filename: {result['filename']}")
        print(f"   📊 File size: {result['file_size']} bytes")
        print(f"   🔗 Storage URL: {result['storage_url']}")
        print(f"   📂 Storage path: {result['storage_path']}")
        
        # Verificar que el archivo existe
        print("\n🔍 Verificando que el archivo existe...")
        
        # Intentar obtener metadatos del archivo
        bucket_name = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET", "claims-documents-zurich-ai")
        blob_name = result['storage_path']
        
        from google.cloud import storage
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        
        if blob.exists():
            print("✅ Archivo existe en Google Cloud Storage")
            print(f"   📊 Tamaño real: {blob.size} bytes")
            print(f"   📅 Creado: {blob.time_created}")
            print(f"   🔗 URL pública: {blob.public_url}")
        else:
            print("❌ Archivo no encontrado en Google Cloud Storage")
            
        return True
        
    except Exception as e:
        print(f"❌ Error probando storage: {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(test_storage_service()) 