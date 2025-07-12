#!/usr/bin/env python3
"""
Script para configurar las credenciales de Google Cloud Storage
"""

import os
import json
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def create_service_account_credentials():
    """Crear credenciales de cuenta de servicio para Google Cloud Storage"""
    
    # Credenciales de cuenta de servicio (ejemplo - reemplazar con las reales)
    service_account_credentials = {
        "type": "service_account",
        "project_id": "velvety-glyph-464401-v6",
        "private_key_id": "YOUR_PRIVATE_KEY_ID",
        "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n",
        "client_email": "claims-storage@velvety-glyph-464401-v6.iam.gserviceaccount.com",
        "client_id": "YOUR_CLIENT_ID",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/claims-storage%40velvety-glyph-464401-v6.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }
    
    return service_account_credentials

def setup_gcs_environment():
    """Configurar variables de entorno para Google Cloud Storage"""
    
    print("🔧 Configurando Google Cloud Storage...")
    
    # Verificar variables existentes
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    bucket_name = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")
    folder = os.getenv("GOOGLE_CLOUD_STORAGE_FOLDER")
    
    print(f"📋 Configuración actual:")
    print(f"   - Project ID: {project_id}")
    print(f"   - Bucket: {bucket_name}")
    print(f"   - Folder: {folder}")
    
    # Crear credenciales de ejemplo
    credentials = create_service_account_credentials()
    credentials_json = json.dumps(credentials, indent=2)
    
    print(f"\n🔑 Credenciales de ejemplo generadas:")
    print(f"   - Client Email: {credentials['client_email']}")
    print(f"   - Project ID: {credentials['project_id']}")
    
    # Guardar en archivo temporal para referencia
    with open("gcs_credentials_example.json", "w") as f:
        f.write(credentials_json)
    
    print(f"\n📄 Credenciales guardadas en: gcs_credentials_example.json")
    print(f"\n⚠️  IMPORTANTE:")
    print(f"   1. Ve a Google Cloud Console")
    print(f"   2. Crea una cuenta de servicio para Storage")
    print(f"   3. Descarga el archivo JSON de credenciales")
    print(f"   4. Copia el contenido al .env como GOOGLE_APPLICATION_CREDENTIALS_JSON")
    
    return credentials_json

def test_gcs_connection():
    """Probar la conexión a Google Cloud Storage"""
    
    print(f"\n🧪 Probando conexión...")
    
    try:
        from google.cloud import storage
        
        # Intentar conectar
        client = storage.Client()
        print("✅ Conexión exitosa usando credenciales por defecto")
        
        # Listar buckets
        buckets = list(client.list_buckets())
        print(f"📦 Buckets disponibles: {len(buckets)}")
        
        for bucket in buckets:
            print(f"   - {bucket.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print(f"\n💡 Soluciones:")
        print(f"   1. Ejecuta: gcloud auth application-default login")
        print(f"   2. O configura GOOGLE_APPLICATION_CREDENTIALS_JSON en .env")
        return False

if __name__ == "__main__":
    print("☁️  CONFIGURACIÓN DE GOOGLE CLOUD STORAGE")
    print("=" * 50)
    
    # Configurar entorno
    setup_gcs_environment()
    
    # Probar conexión
    test_gcs_connection()
    
    print(f"\n🎯 Próximos pasos:")
    print(f"   1. Configura las credenciales reales en .env")
    print(f"   2. Ejecuta: python backend/test_storage_upload.py")
    print(f"   3. Verifica que puedas subir y leer archivos") 