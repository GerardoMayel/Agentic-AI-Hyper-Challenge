"""
Servicio para manejar el almacenamiento en Google Cloud Storage.
"""

import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, BinaryIO
from google.cloud import storage
from google.auth.exceptions import DefaultCredentialsError
from dotenv import load_dotenv

load_dotenv()

class GoogleCloudStorageService:
    """Servicio para interactuar con Google Cloud Storage."""
    
    def __init__(self):
        self.project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID', 'velvety-glyph-464401-v6')
        self.bucket_name = os.getenv('GOOGLE_CLOUD_STORAGE_BUCKET', 'claims-documents-zurich-ai')
        self.base_folder = os.getenv('GOOGLE_CLOUD_STORAGE_FOLDER', 'documentos')
        
        try:
            # Intentar usar Application Default Credentials
            self.client = storage.Client(project=self.project_id)
            self.bucket = self.client.bucket(self.bucket_name)
            print(f"✅ Conectado a Google Cloud Storage: {self.bucket_name}")
        except DefaultCredentialsError:
            print("❌ Error: No se encontraron credenciales de Google Cloud")
            print("   Ejecuta: gcloud auth application-default login")
            self.client = None
            self.bucket = None
        except Exception as e:
            print(f"❌ Error conectando a Google Cloud Storage: {e}")
            self.client = None
            self.bucket = None
    
    def upload_file(self, 
                   file_content: bytes, 
                   filename: str, 
                   numero_siniestro: str,
                   email_id: str,
                   content_type: Optional[str] = None) -> Optional[str]:
        """
        Sube un archivo a Google Cloud Storage.
        
        Args:
            file_content: Contenido del archivo en bytes
            filename: Nombre del archivo
            numero_siniestro: Número del siniestro
            email_id: ID del email
            content_type: Tipo MIME del archivo
            
        Returns:
            URL pública del archivo o None si hay error
        """
        if not self.bucket:
            print("❌ No hay conexión a Google Cloud Storage")
            return None
        
        try:
            # Crear ruta en el bucket
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_filename = self._sanitize_filename(filename)
            blob_path = f"{self.base_folder}/{numero_siniestro}/email-{email_id}/{timestamp}_{safe_filename}"
            
            # Crear blob y subir contenido
            blob = self.bucket.blob(blob_path)
            
            # Configurar metadatos
            if content_type:
                blob.content_type = content_type
            
            # Subir archivo con el content_type correcto
            if content_type:
                blob.upload_from_string(
                    file_content,
                    content_type=content_type
                )
            else:
                blob.upload_from_string(file_content)
            
            # Generar URL pública (sin hacer público el archivo)
            url = f"https://storage.googleapis.com/{self.bucket_name}/{blob_path}"
            
            print(f"✅ Archivo subido: {filename}")
            print(f"   URL: {url}")
            print(f"   Ruta: {blob_path}")
            
            return url
            
        except Exception as e:
            print(f"❌ Error subiendo archivo {filename}: {e}")
            return None
    
    def _sanitize_filename(self, filename: str) -> str:
        """
        Sanitiza el nombre del archivo para evitar problemas de compatibilidad.
        
        Args:
            filename: Nombre original del archivo
            
        Returns:
            Nombre sanitizado
        """
        # Caracteres problemáticos
        invalid_chars = '<>:"/\\|?*'
        
        # Reemplazar caracteres inválidos
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Limitar longitud
        if len(filename) > 200:
            name, ext = os.path.splitext(filename)
            filename = name[:200-len(ext)] + ext
        
        return filename

# Instancia global del servicio
gcs_storage = GoogleCloudStorageService() 