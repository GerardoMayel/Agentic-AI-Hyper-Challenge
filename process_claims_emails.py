#!/usr/bin/env python3
"""
Script para procesar emails de claims automáticamente.
Combina Gmail API, Google Cloud Storage y base de datos PostgreSQL.
"""

import os
import sys
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from app.services.gmail_service import GmailService
from app.services.storage_service import gcs_storage
from app.services.claims_processor import claims_processor
from app.core.database import get_db
from app.core.models import EmailRecibido, DocumentoAdjunto, SiniestroReportado

class ClaimsEmailProcessor:
    """Procesador principal de emails de claims."""
    
    def __init__(self):
        self.gmail_service = GmailService()
        self.storage_service = gcs_storage
        self.claims_processor = claims_processor
        
    def procesar_emails_nuevos(self, max_emails: int = 10) -> Dict:
        """
        Procesa emails nuevos que contengan palabras clave de claims.
        
        Args:
            max_emails: Número máximo de emails a procesar
            
        Returns:
            Diccionario con estadísticas del procesamiento
        """
        try:
            print("🔍 Buscando emails con palabras clave de claims...")
            
            # Buscar emails con palabras clave
            emails = self.gmail_service.buscar_emails_claims(max_results=max_emails)
            
            if not emails:
                print("✅ No se encontraron emails nuevos con palabras clave de claims")
                return {
                    'status': 'no_emails',
                    'emails_procesados': 0,
                    'nuevos_siniestros': 0,
                    'documentos_procesados': 0
                }
            
            print(f"📧 Encontrados {len(emails)} emails para procesar")
            
            estadisticas = {
                'emails_procesados': 0,
                'nuevos_siniestros': 0,
                'documentos_procesados': 0,
                'errores': 0,
                'detalles': []
            }
            
            for i, email in enumerate(emails, 1):
                print(f"\n📧 Procesando email {i}/{len(emails)}: {email.get('subject', 'Sin asunto')}")
                
                try:
                    # Procesar email
                    resultado = self.procesar_email_completo(email)
                    
                    if resultado['status'] == 'success':
                        estadisticas['emails_procesados'] += 1
                        
                        if resultado.get('es_nuevo_siniestro'):
                            estadisticas['nuevos_siniestros'] += 1
                        
                        estadisticas['documentos_procesados'] += resultado.get('documentos_procesados', 0)
                        
                        print(f"✅ Email procesado exitosamente")
                        if resultado.get('numero_siniestro'):
                            print(f"   Siniestro: {resultado['numero_siniestro']}")
                    
                    elif resultado['status'] == 'already_processed':
                        print(f"⚠️ Email ya procesado anteriormente")
                    
                    elif resultado['status'] == 'no_claim_keywords':
                        print(f"⚠️ Email no contiene palabras clave de claim")
                    
                    else:
                        estadisticas['errores'] += 1
                        print(f"❌ Error procesando email: {resultado.get('message', 'Error desconocido')}")
                    
                    estadisticas['detalles'].append(resultado)
                    
                    # Pausa entre emails para no sobrecargar las APIs
                    time.sleep(1)
                    
                except Exception as e:
                    estadisticas['errores'] += 1
                    print(f"❌ Error inesperado procesando email: {e}")
                    estadisticas['detalles'].append({
                        'status': 'error',
                        'message': str(e)
                    })
            
            print(f"\n📊 RESUMEN DEL PROCESAMIENTO:")
            print(f"   Emails procesados: {estadisticas['emails_procesados']}")
            print(f"   Nuevos siniestros: {estadisticas['nuevos_siniestros']}")
            print(f"   Documentos procesados: {estadisticas['documentos_procesados']}")
            print(f"   Errores: {estadisticas['errores']}")
            
            return estadisticas
            
        except Exception as e:
            print(f"❌ Error en procesamiento masivo: {e}")
            return {
                'status': 'error',
                'message': str(e),
                'emails_procesados': 0,
                'nuevos_siniestros': 0,
                'documentos_procesados': 0
            }
    
    def procesar_email_completo(self, email_data: Dict) -> Dict:
        """
        Procesa un email completo incluyendo adjuntos y almacenamiento.
        
        Args:
            email_data: Datos del email de Gmail API
            
        Returns:
            Diccionario con resultado del procesamiento
        """
        try:
            # Procesar email con claims processor
            resultado = self.claims_processor.procesar_email_gmail(email_data)
            
            if resultado['status'] != 'success':
                return resultado
            
            # Si hay documentos, procesarlos en Google Cloud Storage
            if resultado.get('documentos_procesados', 0) > 0:
                self._procesar_documentos_storage(email_data['id'], resultado.get('numero_siniestro'))
            
            return resultado
            
        except Exception as e:
            print(f"❌ Error procesando email completo: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _procesar_documentos_storage(self, email_id: str, numero_siniestro: str):
        """
        Procesa los documentos del email en Google Cloud Storage.
        
        Args:
            email_id: ID del email
            numero_siniestro: Número del siniestro
        """
        try:
            if not numero_siniestro:
                print("⚠️ No hay número de siniestro para procesar documentos")
                return
            
            print(f"📁 Procesando documentos para siniestro: {numero_siniestro}")
            
            # Obtener documentos de la base de datos
            db = next(get_db())
            documentos = db.query(DocumentoAdjunto).filter_by(
                gmail_attachment_id=email_id
            ).all()
            
            for documento in documentos:
                try:
                    # Descargar adjunto de Gmail
                    adjunto_data = self.gmail_service.descargar_adjunto(
                        email_id, 
                        documento.gmail_attachment_id
                    )
                    
                    if adjunto_data:
                        # Subir a Google Cloud Storage
                        url_storage = self.storage_service.upload_file(
                            file_content=adjunto_data['content'],
                            filename=documento.nombre_archivo,
                            numero_siniestro=numero_siniestro,
                            email_id=email_id,
                            content_type=documento.tipo_mime
                        )
                        
                        if url_storage:
                            # Actualizar registro en base de datos
                            documento.url_storage = url_storage
                            documento.contenido_descargado = True
                            documento.fecha_descarga = datetime.now()
                            documento.ruta_storage = f"{numero_siniestro}/email-{email_id}/{documento.nombre_archivo}"
                            
                            db.commit()
                            print(f"✅ Documento subido: {documento.nombre_archivo}")
                        else:
                            print(f"❌ Error subiendo documento: {documento.nombre_archivo}")
                    else:
                        print(f"❌ Error descargando adjunto: {documento.nombre_archivo}")
                
                except Exception as e:
                    print(f"❌ Error procesando documento {documento.nombre_archivo}: {e}")
                    continue
            
            db.close()
            
        except Exception as e:
            print(f"❌ Error procesando documentos en storage: {e}")
    
    def mostrar_estadisticas_sistema(self):
        """Muestra estadísticas del sistema."""
        try:
            db = next(get_db())
            
            # Contar emails procesados
            total_emails = db.query(EmailRecibido).count()
            emails_pendientes = db.query(EmailRecibido).filter_by(
                estado_procesamiento='pendiente'
            ).count()
            emails_completados = db.query(EmailRecibido).filter_by(
                estado_procesamiento='completado'
            ).count()
            
            # Contar siniestros
            total_siniestros = db.query(SiniestroReportado).count()
            siniestros_nuevos = db.query(SiniestroReportado).filter_by(
                estado='nuevo'
            ).count()
            
            # Contar documentos
            total_documentos = db.query(DocumentoAdjunto).count()
            documentos_descargados = db.query(DocumentoAdjunto).filter_by(
                contenido_descargado=True
            ).count()
            
            print("\n📊 ESTADÍSTICAS DEL SISTEMA:")
            print("=" * 40)
            print(f"📧 Emails procesados: {total_emails}")
            print(f"   - Pendientes: {emails_pendientes}")
            print(f"   - Completados: {emails_completados}")
            print(f"🚨 Siniestros reportados: {total_siniestros}")
            print(f"   - Nuevos: {siniestros_nuevos}")
            print(f"📎 Documentos adjuntos: {total_documentos}")
            print(f"   - Descargados: {documentos_descargados}")
            
            # Últimos siniestros
            ultimos_siniestros = db.query(SiniestroReportado).order_by(
                SiniestroReportado.fecha_reporte.desc()
            ).limit(5).all()
            
            if ultimos_siniestros:
                print(f"\n🕒 ÚLTIMOS SINIESTROS:")
                for siniestro in ultimos_siniestros:
                    print(f"   - {siniestro.numero_siniestro} ({siniestro.fecha_reporte.strftime('%Y-%m-%d %H:%M')})")
                    print(f"     Remitente: {siniestro.remitente_email}")
                    print(f"     Estado: {siniestro.estado}")
            
            db.close()
            
        except Exception as e:
            print(f"❌ Error obteniendo estadísticas: {e}")

def main():
    """Función principal."""
    print("🚀 PROCESADOR DE EMAILS DE CLAIMS")
    print("=" * 50)
    
    processor = ClaimsEmailProcessor()
    
    while True:
        print("\n📋 OPCIONES DISPONIBLES:")
        print("1. Procesar emails nuevos")
        print("2. Mostrar estadísticas del sistema")
        print("3. Salir")
        
        opcion = input("\nSelecciona una opción (1-3): ").strip()
        
        if opcion == "1":
            max_emails = input("Número máximo de emails a procesar (default: 10): ").strip()
            max_emails = int(max_emails) if max_emails.isdigit() else 10
            
            print(f"\n🔄 Procesando hasta {max_emails} emails...")
            resultado = processor.procesar_emails_nuevos(max_emails)
            
            if resultado.get('status') == 'no_emails':
                print("✅ No hay emails nuevos para procesar")
        
        elif opcion == "2":
            processor.mostrar_estadisticas_sistema()
        
        elif opcion == "3":
            print("👋 ¡Hasta luego!")
            break
        
        else:
            print("❌ Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main() 