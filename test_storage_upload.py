#!/usr/bin/env python3
"""
Script para probar la subida de archivos a Google Cloud Storage.
Crea un PDF de prueba, lo sube al storage y obtiene la URL de regreso.
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Leer directamente el archivo .env y establecer DATABASE_URL
env_path = os.path.abspath('.env')
with open(env_path, 'r') as f:
    for line in f:
        if line.startswith('DATABASE_URL='):
            db_url = line.split('=', 1)[1].strip()
            os.environ['DATABASE_URL'] = db_url
            break

load_dotenv()

def crear_pdf_prueba():
    """Crea un PDF de prueba simple."""
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from io import BytesIO
    
    # Crear PDF en memoria
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Agregar contenido
    p.drawString(100, 750, "PRUEBA DE STORAGE - GOOGLE CLOUD")
    p.drawString(100, 720, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    p.drawString(100, 690, "Este es un documento de prueba para verificar")
    p.drawString(100, 660, "la funcionalidad de subida a Google Cloud Storage.")
    p.drawString(100, 630, "Si puedes ver este PDF, la subida fue exitosa.")
    p.drawString(100, 600, "Archivo generado automáticamente para pruebas.")
    
    p.save()
    buffer.seek(0)
    return buffer.getvalue()

def probar_storage_upload():
    """Prueba la subida de archivos al storage."""
    try:
        print("🚀 PRUEBA DE STORAGE - GOOGLE CLOUD")
        print("=" * 50)
        
        # Crear PDF de prueba
        print("📄 Creando PDF de prueba...")
        pdf_content = crear_pdf_prueba()
        print(f"✅ PDF creado: {len(pdf_content)} bytes")
        
        # Inicializar servicio de storage
        print("\n☁️ Inicializando Google Cloud Storage...")
        from app.services.gcs_storage import gcs_storage
        
        if not gcs_storage.bucket:
            print("❌ Error: No se pudo conectar a Google Cloud Storage")
            return False
        
        # Configurar parámetros de prueba
        numero_siniestro = f"TEST-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        email_id = "test-email-123"
        filename = "Documento_Prueba_Storage.pdf"
        content_type = "application/pdf"
        
        print(f"\n📤 Subiendo archivo...")
        print(f"   Número siniestro: {numero_siniestro}")
        print(f"   Email ID: {email_id}")
        print(f"   Archivo: {filename}")
        print(f"   Tipo: {content_type}")
        
        # Subir archivo
        url_storage = gcs_storage.upload_file(
            file_content=pdf_content,
            filename=filename,
            numero_siniestro=numero_siniestro,
            email_id=email_id,
            content_type=content_type
        )
        
        if url_storage:
            print(f"\n✅ ¡Archivo subido exitosamente!")
            print(f"   URL: {url_storage}")
            
            # Mostrar información adicional
            print(f"\n📊 INFORMACIÓN ADICIONAL:")
            print(f"   Bucket: {gcs_storage.bucket_name}")
            print(f"   Proyecto: {gcs_storage.project_id}")
            print(f"   Ruta esperada: {gcs_storage.base_folder}/{numero_siniestro}/email-{email_id}/")
            
            # Probar acceso a la URL
            print(f"\n🔗 Probando acceso a la URL...")
            import requests
            try:
                response = requests.head(url_storage, timeout=10)
                if response.status_code == 200:
                    print(f"✅ URL accesible (Status: {response.status_code})")
                    print(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")
                    print(f"   Content-Length: {response.headers.get('content-length', 'N/A')} bytes")
                else:
                    print(f"⚠️ URL no accesible (Status: {response.status_code})")
            except Exception as e:
                print(f"⚠️ Error probando URL: {e}")
            
            return True
        else:
            print(f"\n❌ Error subiendo archivo")
            return False
            
    except Exception as e:
        print(f"\n❌ Error en la prueba: {e}")
        return False

def mostrar_configuracion():
    """Muestra la configuración actual del storage."""
    print("\n⚙️ CONFIGURACIÓN ACTUAL:")
    print("=" * 30)
    
    from app.services.gcs_storage import gcs_storage
    
    print(f"   Proyecto ID: {gcs_storage.project_id}")
    print(f"   Bucket: {gcs_storage.bucket_name}")
    print(f"   Folder base: {gcs_storage.base_folder}")
    print(f"   Conectado: {'✅' if gcs_storage.bucket else '❌'}")

def main():
    """Función principal."""
    print("🧪 TEST DE STORAGE - GOOGLE CLOUD")
    print("=" * 50)
    
    # Mostrar configuración
    mostrar_configuracion()
    
    # Preguntar confirmación
    print("\n" + "=" * 50)
    confirmacion = input("¿Deseas probar la subida de archivos? (y/N): ").strip().lower()
    
    if confirmacion in ['y', 'yes', 'sí', 'si']:
        if probar_storage_upload():
            print("\n🎉 ¡Prueba completada exitosamente!")
            print("   El sistema de storage está funcionando correctamente.")
        else:
            print("\n❌ Error en la prueba de storage")
    else:
        print("\n⚠️ Prueba cancelada")

if __name__ == "__main__":
    main() 