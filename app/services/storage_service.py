import os
import boto3
from typing import Optional, BinaryIO
from botocore.exceptions import ClientError

class StorageService:
    """Servicio para almacenamiento de archivos usando Cloudflare R2 (compatible con S3)."""
    
    def __init__(self):
        self.account_id = os.getenv("R2_ACCOUNT_ID")
        self.access_key_id = os.getenv("R2_ACCESS_KEY_ID")
        self.secret_access_key = os.getenv("R2_SECRET_ACCESS_KEY")
        self.bucket_name = os.getenv("R2_BUCKET_NAME")
        self.public_url = os.getenv("R2_PUBLIC_URL")
        
        # Configurar cliente S3 compatible con R2
        if all([self.account_id, self.access_key_id, self.secret_access_key]):
            self.s3_client = boto3.client(
                's3',
                endpoint_url=f'https://{self.account_id}.r2.cloudflarestorage.com',
                aws_access_key_id=self.access_key_id,
                aws_secret_access_key=self.secret_access_key
            )
        else:
            self.s3_client = None
            print("R2 no está configurado completamente.")
    
    def upload_file(
        self,
        file_path: str,
        object_name: Optional[str] = None,
        content_type: Optional[str] = None
    ) -> Optional[str]:
        """
        Sube un archivo al almacenamiento R2.
        
        Args:
            file_path: Ruta del archivo local
            object_name: Nombre del objeto en R2 (opcional)
            content_type: Tipo de contenido del archivo
            
        Returns:
            str: URL pública del archivo si se subió correctamente, None en caso contrario
        """
        if not self.s3_client or not self.bucket_name:
            print("R2 no está configurado. Archivo no subido.")
            return None
        
        if object_name is None:
            object_name = os.path.basename(file_path)
        
        try:
            extra_args = {}
            if content_type:
                extra_args['ContentType'] = content_type
            
            self.s3_client.upload_file(
                file_path,
                self.bucket_name,
                object_name,
                ExtraArgs=extra_args
            )
            
            # Construir URL pública
            if self.public_url:
                file_url = f"{self.public_url}/{object_name}"
            else:
                file_url = f"https://{self.bucket_name}.r2.cloudflarestorage.com/{object_name}"
            
            print(f"Archivo subido exitosamente: {file_url}")
            return file_url
            
        except ClientError as e:
            print(f"Error subiendo archivo: {str(e)}")
            return None
    
    def upload_fileobj(
        self,
        file_obj: BinaryIO,
        object_name: str,
        content_type: Optional[str] = None
    ) -> Optional[str]:
        """
        Sube un objeto de archivo al almacenamiento R2.
        
        Args:
            file_obj: Objeto de archivo (BytesIO, etc.)
            object_name: Nombre del objeto en R2
            content_type: Tipo de contenido del archivo
            
        Returns:
            str: URL pública del archivo si se subió correctamente, None en caso contrario
        """
        if not self.s3_client or not self.bucket_name:
            print("R2 no está configurado. Archivo no subido.")
            return None
        
        try:
            extra_args = {}
            if content_type:
                extra_args['ContentType'] = content_type
            
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket_name,
                object_name,
                ExtraArgs=extra_args
            )
            
            # Construir URL pública
            if self.public_url:
                file_url = f"{self.public_url}/{object_name}"
            else:
                file_url = f"https://{self.bucket_name}.r2.cloudflarestorage.com/{object_name}"
            
            print(f"Archivo subido exitosamente: {file_url}")
            return file_url
            
        except ClientError as e:
            print(f"Error subiendo archivo: {str(e)}")
            return None
    
    def delete_file(self, object_name: str) -> bool:
        """
        Elimina un archivo del almacenamiento R2.
        
        Args:
            object_name: Nombre del objeto a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        if not self.s3_client or not self.bucket_name:
            print("R2 no está configurado. Archivo no eliminado.")
            return False
        
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=object_name
            )
            print(f"Archivo eliminado exitosamente: {object_name}")
            return True
            
        except ClientError as e:
            print(f"Error eliminando archivo: {str(e)}")
            return False
    
    def get_file_url(self, object_name: str) -> Optional[str]:
        """
        Obtiene la URL pública de un archivo.
        
        Args:
            object_name: Nombre del objeto
            
        Returns:
            str: URL pública del archivo, None si no está configurado
        """
        if not self.bucket_name:
            return None
        
        if self.public_url:
            return f"{self.public_url}/{object_name}"
        else:
            return f"https://{self.bucket_name}.r2.cloudflarestorage.com/{object_name}"

# Instancia global del servicio
storage_service = StorageService() 