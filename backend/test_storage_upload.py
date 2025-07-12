#!/usr/bin/env python3
"""
Script para probar la conexión y subida de archivos a Google Cloud Storage
"""

import os
import sys
from dotenv import load_dotenv

# Buscar el archivo .env en el directorio raíz del proyecto
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
env_path = os.path.join(project_root, '.env')
load_dotenv(env_path)

def test_storage_connection():
    """Probar la conexión a Google Cloud Storage"""
    try:
        print("🔍 Probando conexión a Google Cloud Storage...")
        
        # Verificar variables de entorno
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        bucket_name = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")
        credentials_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
        
        print(f"📋 Configuración:")
        print(f"   - Project ID: {project_id}")
        print(f"   - Bucket: {bucket_name}")
        print(f"   - Credentials: {'✅ Configuradas' if credentials_json else '❌ No configuradas'}")
        
        if not all([project_id, bucket_name]):
            print("❌ Faltan variables de entorno necesarias (project_id, bucket_name)")
            return False
        
        if not credentials_json:
            print("⚠️  No hay credenciales JSON configuradas, usando credenciales por defecto")
        
        # Importar y probar el servicio de storage
        from app.services.storage_service import StorageService
        
        storage_service = StorageService()
        print("✅ Conexión a Google Cloud Storage exitosa")
        
        # Listar archivos existentes
        print("\n📁 Archivos existentes en el bucket:")
        try:
            files = storage_service.list_files_by_claim("test")
            if files:
                for file in files:
                    print(f"   - {file['name']} ({file['size']} bytes)")
            else:
                print("   📭 No hay archivos de prueba")
        except Exception as e:
            print(f"   ⚠️  No se pudieron listar archivos: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error conectando a Google Cloud Storage: {e}")
        return False

async def test_file_upload():
    """Probar la subida de un archivo de prueba"""
    try:
        print("\n📤 Probando subida de archivo...")
        
        from app.services.storage_service import StorageService
        import io
        
        storage_service = StorageService()
        
        # Crear un archivo de prueba
        test_content = "Este es un archivo de prueba para verificar la conexión a Google Cloud Storage"
        test_file = io.BytesIO(test_content.encode('utf-8'))
        
        # Subir archivo
        result = await storage_service.upload_file(
            file_content=test_file,
            claim_id="TEST-12345",
            document_type="TEST_DOCUMENT",
            original_filename="test_connection.txt"
        )
        
        print("✅ Archivo subido exitosamente!")
        print(f"📋 Resultado:")
        print(f"   - Storage URL: {result['storage_url']}")
        print(f"   - Storage Path: {result['storage_path']}")
        print(f"   - Filename: {result['filename']}")
        print(f"   - File Size: {result['file_size']} bytes")
        
        return result
        
    except Exception as e:
        print(f"❌ Error subiendo archivo: {e}")
        return None

async def main():
    print("☁️  PROBANDO GOOGLE CLOUD STORAGE")
    print("=" * 50)
    
    # Probar conexión
    connection_success = test_storage_connection()
    
    if connection_success:
        # Probar subida de archivo
        upload_result = await test_file_upload()
        
        if upload_result:
            print("\n🎉 ¡Google Cloud Storage configurado correctamente!")
            print("   Puedes proceder con el desarrollo del backend.")
        else:
            print("\n⚠️  La conexión funciona pero la subida falló.")
    else:
        print("\n❌ No se pudo conectar a Google Cloud Storage.")
        print("   Verifica las credenciales y configuración.")
        sys.exit(1)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 