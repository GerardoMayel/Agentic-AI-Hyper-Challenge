#!/usr/bin/env python3
"""
Script para procesar el email de prueba con PDF.
Funciona sin base de datos para probar Gmail API y Google Cloud Storage.
"""

import os
import sys
import time
from datetime import datetime
from dotenv import load_dotenv

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from app.services.gmail_service import GmailService
from app.services.storage_service import storage_service_gcs

class TestClaimsProcessor:
    """Procesador de prueba para emails de claims."""
    
    def __init__(self):
        self.gmail_service = GmailService()
        self.storage_service = storage_service_gcs
        
    def procesar_email_prueba(self):
        """Procesa el email de prueba con PDF."""
        try:
            print("🔍 Buscando email de prueba con PDF...")
            
            # Buscar emails con palabras clave de claims
            emails = self.gmail_service.buscar_emails_claims(max_results=5)
            
            if not emails:
                print("❌ No se encontraron emails con palabras clave de claims")
                return
            
            print(f"📧 Encontrados {len(emails)} emails")
            
            # Procesar el primer email que tenga adjuntos
            for i, email in enumerate(emails):
                print(f"\n📧 Procesando email {i+1}: {email.get('subject', 'Sin asunto')}")
                
                # Verificar si tiene adjuntos
                attachments = email.get('attachments', [])
                if not attachments:
                    print("⚠️ Email sin adjuntos, continuando...")
                    continue
                
                print(f"📎 Encontrados {len(attachments)} adjuntos")
                
                # Procesar este email
                resultado = self._procesar_email_completo(email)
                
                if resultado['status'] == 'success':
                    print("✅ Email procesado exitosamente")
                    return resultado
                else:
                    print(f"❌ Error: {resultado.get('message', 'Error desconocido')}")
            
            print("❌ No se encontró un email válido para procesar")
            
        except Exception as e:
            print(f"❌ Error en procesamiento: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _procesar_email_completo(self, email_data):
        """Procesa un email completo."""
        try:
            # Extraer información básica
            email_id = email_data['id']
            subject = email_data.get('subject', 'Sin asunto')
            from_header = email_data.get('from', '')
            to_header = email_data.get('to', '')
            date_header = email_data.get('date', '')
            text_content = email_data.get('text_content', '')
            html_content = email_data.get('html_content', '')
            snippet = email_data.get('snippet', '')
            attachments = email_data.get('attachments', [])
            
            print(f"📧 Email ID: {email_id}")
            print(f"📧 Asunto: {subject}")
            print(f"📧 Remitente: {from_header}")
            print(f"📧 Fecha: {date_header}")
            print(f"📧 Contenido: {snippet[:100]}...")
            
            # Generar número de siniestro de prueba
            numero_siniestro = self._generar_numero_siniestro()
            print(f"🚨 Número de siniestro generado: {numero_siniestro}")
            
            # Procesar adjuntos
            documentos_procesados = []
            for attachment in attachments:
                resultado_doc = self._procesar_adjunto(
                    email_id, 
                    attachment, 
                    numero_siniestro
                )
                if resultado_doc:
                    documentos_procesados.append(resultado_doc)
            
            # Simular registro en base de datos
            email_info = {
                'gmail_message_id': email_id,
                'remitente_email': from_header,
                'destinatario_email': to_header,
                'subject': subject,
                'contenido_texto': text_content,
                'contenido_html': html_content,
                'snippet': snippet,
                'fecha_recibido': date_header,
                'es_nuevo_siniestro': True,
                'numero_siniestro': numero_siniestro,
                'estado_procesamiento': 'completado'
            }
            
            print(f"\n📊 RESUMEN DEL PROCESAMIENTO:")
            print(f"   Email ID: {email_id}")
            print(f"   Siniestro: {numero_siniestro}")
            print(f"   Documentos procesados: {len(documentos_procesados)}")
            print(f"   Es nuevo siniestro: Sí")
            
            return {
                'status': 'success',
                'email_info': email_info,
                'documentos_procesados': documentos_procesados,
                'numero_siniestro': numero_siniestro
            }
            
        except Exception as e:
            print(f"❌ Error procesando email: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _procesar_adjunto(self, email_id, attachment, numero_siniestro):
        """Procesa un adjunto individual."""
        try:
            filename = attachment['filename']
            mime_type = attachment['mime_type']
            size = attachment['size']
            attachment_id = attachment['attachment_id']
            
            print(f"\n📎 Procesando adjunto: {filename}")
            print(f"   Tipo: {mime_type}")
            print(f"   Tamaño: {size} bytes")
            
            # Descargar adjunto de Gmail
            adjunto_data = self.gmail_service.descargar_adjunto(email_id, attachment_id)
            
            if not adjunto_data:
                print(f"❌ Error descargando adjunto: {filename}")
                return None
            
            # Subir a Google Cloud Storage
            url_storage = self.storage_service.upload_file(
                file_content=adjunto_data['content'],
                filename=filename,
                numero_siniestro=numero_siniestro,
                email_id=email_id,
                content_type=mime_type
            )
            
            if url_storage:
                print(f"✅ Documento subido exitosamente")
                print(f"   URL: {url_storage}")
                
                return {
                    'filename': filename,
                    'mime_type': mime_type,
                    'size': size,
                    'url_storage': url_storage,
                    'ruta_storage': f"{numero_siniestro}/email-{email_id}/{filename}"
                }
            else:
                print(f"❌ Error subiendo documento: {filename}")
                return None
                
        except Exception as e:
            print(f"❌ Error procesando adjunto {filename}: {e}")
            return None
    
    def _generar_numero_siniestro(self):
        """Genera un número único de siniestro."""
        from datetime import datetime
        import random
        
        fecha = datetime.now().strftime("%Y%m%d")
        numero_aleatorio = random.randint(1000, 9999)
        return f"CLAIM-{fecha}-{numero_aleatorio}"
    
    def mostrar_estadisticas_storage(self):
        """Muestra estadísticas del storage."""
        try:
            print("\n📊 ESTADÍSTICAS DE GOOGLE CLOUD STORAGE:")
            print("=" * 50)
            
            # Listar archivos en el bucket
            archivos = self.storage_service.list_files(prefix="documentos/")
            
            if archivos:
                print(f"📁 Archivos encontrados: {len(archivos)}")
                for archivo in archivos[:10]:  # Mostrar solo los primeros 10
                    print(f"   - {archivo}")
                
                if len(archivos) > 10:
                    print(f"   ... y {len(archivos) - 10} más")
            else:
                print("📁 No se encontraron archivos en el bucket")
                
        except Exception as e:
            print(f"❌ Error obteniendo estadísticas: {e}")

def main():
    """Función principal."""
    print("🚀 PROCESADOR DE PRUEBA - EMAILS DE CLAIMS")
    print("=" * 60)
    
    processor = TestClaimsProcessor()
    
    while True:
        print("\n📋 OPCIONES DISPONIBLES:")
        print("1. Procesar email de prueba")
        print("2. Mostrar estadísticas de storage")
        print("3. Salir")
        
        opcion = input("\nSelecciona una opción (1-3): ").strip()
        
        if opcion == "1":
            print(f"\n🔄 Procesando email de prueba...")
            resultado = processor.procesar_email_prueba()
            
            if resultado and resultado.get('status') == 'success':
                print("\n🎉 ¡Email procesado exitosamente!")
                print(f"   Siniestro: {resultado.get('numero_siniestro')}")
                print(f"   Documentos: {len(resultado.get('documentos_procesados', []))}")
            else:
                print("\n❌ Error procesando email")
        
        elif opcion == "2":
            processor.mostrar_estadisticas_storage()
        
        elif opcion == "3":
            print("👋 ¡Hasta luego!")
            break
        
        else:
            print("❌ Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main() 