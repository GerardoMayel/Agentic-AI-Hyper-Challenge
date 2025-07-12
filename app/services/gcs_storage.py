"""
Servicio para manejar el almacenamiento en Google Cloud Storage.
Importa la clase StorageService del archivo storage_service.py
"""

from app.services.storage_service import StorageService

# Instancia global del servicio
gcs_storage = StorageService() 