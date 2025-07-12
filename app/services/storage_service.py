"""
Servicio para manejar el almacenamiento en Google Cloud Storage.
"""

import os
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, BinaryIO
from google.cloud import storage
from google.auth.exceptions import DefaultCredentialsError
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

class StorageService:
    """Servicio para interactuar con Google Cloud Storage."""
    
    def __init__(self):
        self.project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID', 'velvety-glyph-464401-v6')
        self.bucket_name = os.getenv('GOOGLE_CLOUD_STORAGE_BUCKET', 'claims-documents-zurich-ai')
        self.base_folder = os.getenv('GOOGLE_CLOUD_STORAGE_FOLDER', 'documentos')
        
        try:
            # Intentar usar Service Account JSON desde variable de entorno
            credentials_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
            if credentials_json:
                try:
                    credentials_info = json.loads(credentials_json)
                    credentials = service_account.Credentials.from_service_account_info(credentials_info)
                    self.client = storage.Client(project=self.project_id, credentials=credentials)
                    print(f"✅ Conectado a Google Cloud Storage usando Service Account JSON: {self.bucket_name}")
                except (json.JSONDecodeError, Exception) as e:
                    print(f"⚠️ Error con Service Account JSON: {e}")
                    print("   Intentando Application Default Credentials...")
                    # Fallback a Application Default Credentials
                    self.client = storage.Client(project=self.project_id)
                    print(f"✅ Conectado a Google Cloud Storage usando ADC: {self.bucket_name}")
            else:
                # Usar Application Default Credentials
                self.client = storage.Client(project=self.project_id)
                print(f"✅ Conectado a Google Cloud Storage usando ADC: {self.bucket_name}")
            
            self.bucket = self.client.bucket(self.bucket_name)
            
        except DefaultCredentialsError:
            print("❌ Error: No se encontraron credenciales de Google Cloud")
            print("   Opciones:")
            print("   1. Ejecuta: gcloud auth application-default login")
            print("   2. Configura GOOGLE_APPLICATION_CREDENTIALS_JSON en .env")
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
    
    def download_file(self, storage_path: str) -> Optional[bytes]:
        """
        Descarga un archivo desde Google Cloud Storage.
        
        Args:
            storage_path: Ruta del archivo en el bucket (sin el bucket name)
            
        Returns:
            Contenido del archivo en bytes o None si hay error
        """
        if not self.bucket:
            print("❌ No hay conexión a Google Cloud Storage")
            return None
        
        try:
            # Obtener el blob
            blob = self.bucket.blob(storage_path)
            
            # Verificar si existe
            if not blob.exists():
                print(f"❌ Archivo no encontrado: {storage_path}")
                return None
            
            # Descargar contenido
            content = blob.download_as_bytes()
            
            print(f"✅ Archivo descargado: {storage_path}")
            print(f"   Tamaño: {len(content)} bytes")
            
            return content
            
        except Exception as e:
            print(f"❌ Error descargando archivo {storage_path}: {e}")
            return None
    
    def get_file_url(self, storage_path: str) -> Optional[str]:
        """
        Genera la URL pública de un archivo.
        
        Args:
            storage_path: Ruta del archivo en el bucket
            
        Returns:
            URL pública del archivo
        """
        if not self.bucket or not self.bucket_name:
            return None
        
        return f"https://storage.googleapis.com/{self.bucket_name}/{storage_path}"
    
    def delete_file(self, blob_path: str) -> bool:
        """
        Elimina un archivo de Google Cloud Storage.
        
        Args:
            blob_path: Ruta del archivo en el bucket
            
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        if not self.bucket:
            print("❌ No hay conexión a Google Cloud Storage")
            return False
        
        try:
            blob = self.bucket.blob(blob_path)
            
            if not blob.exists():
                print(f"⚠️ Archivo no existe: {blob_path}")
                return True
            
            blob.delete()
            print(f"✅ Archivo eliminado: {blob_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error eliminando archivo {blob_path}: {e}")
            return False
    
    def list_files(self, prefix: str = None) -> list:
        """
        Lista archivos en el bucket con un prefijo opcional.
        
        Args:
            prefix: Prefijo para filtrar archivos
            
        Returns:
            Lista de nombres de archivos
        """
        if not self.bucket:
            print("❌ No hay conexión a Google Cloud Storage")
            return []
        
        try:
            blobs = self.bucket.list_blobs(prefix=prefix)
            files = [blob.name for blob in blobs]
            print(f"✅ Encontrados {len(files)} archivos con prefijo: {prefix}")
            return files
            
        except Exception as e:
            print(f"❌ Error listando archivos: {e}")
            return []
    
    def get_file_info(self, blob_path: str) -> Optional[dict]:
        """
        Obtiene información de un archivo.
        
        Args:
            blob_path: Ruta del archivo en el bucket
            
        Returns:
            Diccionario con información del archivo o None si hay error
        """
        if not self.bucket:
            print("❌ No hay conexión a Google Cloud Storage")
            return None
        
        try:
            blob = self.bucket.blob(blob_path)
            
            if not blob.exists():
                print(f"❌ Archivo no encontrado: {blob_path}")
                return None
            
            blob.reload()
            
            info = {
                'name': blob.name,
                'size': blob.size,
                'content_type': blob.content_type,
                'created': blob.time_created,
                'updated': blob.updated,
                'public_url': blob.public_url,
                'md5_hash': blob.md5_hash
            }
            
            return info
            
        except Exception as e:
            print(f"❌ Error obteniendo información del archivo {blob_path}: {e}")
            return None
    
    def create_folder_structure(self, numero_siniestro: str) -> bool:
        """
        Crea la estructura de carpetas para un siniestro.
        
        Args:
            numero_siniestro: Número del siniestro
            
        Returns:
            True si se creó correctamente, False en caso contrario
        """
        if not self.bucket:
            print("❌ No hay conexión a Google Cloud Storage")
            return False
        
        try:
            # En GCS, las carpetas se crean automáticamente al subir archivos
            # Pero podemos crear un archivo placeholder para asegurar que existe
            folder_path = f"{self.base_folder}/{numero_siniestro}/"
            placeholder_blob = self.bucket.blob(folder_path + ".placeholder")
            placeholder_blob.upload_from_string("")
            
            print(f"✅ Estructura de carpetas creada: {folder_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error creando estructura de carpetas: {e}")
            return False

# Instancia global para uso en otros módulos
gcs_storage = StorageService() 