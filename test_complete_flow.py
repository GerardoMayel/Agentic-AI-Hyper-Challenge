#!/usr/bin/env python3
"""
Script para probar el flujo completo del sistema de claims.
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

def test_complete_flow():
    """Prueba el flujo completo del sistema de claims."""
    try:
        print("🚀 PRUEBA DEL FLUJO COMPLETO DEL SISTEMA DE CLAIMS")
        print("=" * 60)
        
        # 1. Verificar que las tablas existan
        print("\n1️⃣ Verificando base de datos...")
        from app.core.database import get_db
        from app.core.models import Claim, ClaimDocument, Coverage
        
        db = next(get_db())
        claims_count = db.query(Claim).count()
        coverages_count = db.query(Coverage).count()
        db.close()
        
        print(f"   ✅ Claims en BD: {claims_count}")
        print(f"   ✅ Coberturas en BD: {coverages_count}")
        
        # 2. Verificar conexión a Gmail
        print("\n2️⃣ Verificando conexión a Gmail...")
        from app.services.gmail_service import GmailService
        gmail_service = GmailService()
        
        if gmail_service.service:
            print("   ✅ Conexión a Gmail exitosa")
        else:
            print("   ❌ Error conectando a Gmail")
            return False
        
        # 3. Verificar conexión a Storage
        print("\n3️⃣ Verificando conexión a Google Cloud Storage...")
        from app.services.gcs_storage import gcs_storage
        
        if gcs_storage.bucket:
            print("   ✅ Conexión a Google Cloud Storage exitosa")
        else:
            print("   ❌ Error conectando a Google Cloud Storage")
            return False
        
        # 4. Buscar emails de claims
        print("\n4️⃣ Buscando emails de claims...")
        emails = gmail_service.buscar_emails_claims(max_results=5)
        
        if not emails:
            print("   ⚠️ No se encontraron emails de claims")
            print("   💡 Envía un email con 'claim' en el asunto para probar")
            return False
        
        print(f"   ✅ Encontrados {len(emails)} emails de claims")
        
        # 5. Procesar el primer email
        print("\n5️⃣ Procesando primer email de claim...")
        from app.services.claims_processor import ClaimsProcessor
        
        processor = ClaimsProcessor()
        email_to_process = emails[0]
        
        print(f"   📧 Email: {email_to_process.get('subject', 'Sin asunto')}")
        print(f"   👤 Remitente: {email_to_process.get('sender', 'Desconocido')}")
        
        result = processor.process_claim_email(email_to_process)
        
        if result.get('status') == 'success':
            print(f"   ✅ Claim procesado exitosamente")
            print(f"   📋 Número de claim: {result.get('claim_number')}")
            print(f"   📎 Documentos: {len(result.get('documents_processed', []))}")
            print(f"   📧 Respuesta enviada: {'✅' if result.get('response_sent') else '❌'}")
        elif result.get('status') == 'already_processed':
            print(f"   ℹ️ Email ya procesado: {result.get('claim_number')}")
        else:
            print(f"   ❌ Error procesando claim: {result.get('message')}")
            return False
        
        # 6. Verificar que se creó en la base de datos
        print("\n6️⃣ Verificando registro en base de datos...")
        db = next(get_db())
        claim = db.query(Claim).filter(
            Claim.gmail_message_id == email_to_process['id']
        ).first()
        
        if claim:
            print(f"   ✅ Claim encontrado en BD: {claim.claim_number}")
            print(f"   📊 Estado: {claim.status.value}")
            print(f"   📧 Respuesta enviada: {'✅' if claim.response_sent else '❌'}")
            
            # Verificar documentos
            documents = db.query(ClaimDocument).filter(
                ClaimDocument.claim_id == claim.id
            ).all()
            
            print(f"   📎 Documentos registrados: {len(documents)}")
            for doc in documents:
                print(f"      - {doc.filename} ({doc.source_type})")
        else:
            print("   ❌ Claim no encontrado en BD")
            return False
        
        db.close()
        
        print("\n🎉 ¡FLUJO COMPLETO EXITOSO!")
        print("=" * 60)
        print("✅ Base de datos funcionando")
        print("✅ Gmail API funcionando")
        print("✅ Google Cloud Storage funcionando")
        print("✅ Procesamiento de claims funcionando")
        print("✅ Envío de respuestas funcionando")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error en el flujo completo: {e}")
        return False

def show_system_status():
    """Muestra el estado actual del sistema."""
    print("\n📊 ESTADO DEL SISTEMA:")
    print("=" * 30)
    
    try:
        # Verificar base de datos
        from app.core.database import get_db
        from app.core.models import Claim, ClaimDocument, Coverage
        
        db = next(get_db())
        claims_count = db.query(Claim).count()
        documents_count = db.query(ClaimDocument).count()
        coverages_count = db.query(Coverage).count()
        db.close()
        
        print(f"   📋 Claims registrados: {claims_count}")
        print(f"   📎 Documentos almacenados: {documents_count}")
        print(f"   🛡️ Coberturas disponibles: {coverages_count}")
        
    except Exception as e:
        print(f"   ❌ Error verificando BD: {e}")
    
    try:
        # Verificar Gmail
        from app.services.gmail_service import GmailService
        gmail_service = GmailService()
        print(f"   📧 Gmail API: {'✅' if gmail_service.service else '❌'}")
    except Exception as e:
        print(f"   ❌ Error verificando Gmail: {e}")
    
    try:
        # Verificar Storage
        from app.services.gcs_storage import gcs_storage
        print(f"   ☁️ Google Cloud Storage: {'✅' if gcs_storage.bucket else '❌'}")
    except Exception as e:
        print(f"   ❌ Error verificando Storage: {e}")

def main():
    """Función principal."""
    print("🧪 TEST DEL FLUJO COMPLETO - SISTEMA DE CLAIMS")
    print("=" * 60)
    
    # Mostrar estado del sistema
    show_system_status()
    
    # Preguntar confirmación
    print("\n" + "=" * 60)
    confirmacion = input("¿Deseas probar el flujo completo? (y/N): ").strip().lower()
    
    if confirmacion in ['y', 'yes', 'sí', 'si']:
        if test_complete_flow():
            print("\n🎉 ¡Sistema funcionando correctamente!")
            print("   El flujo completo está operativo.")
        else:
            print("\n❌ Error en el flujo completo")
            print("   Revisa los logs para identificar el problema.")
    else:
        print("\n⚠️ Prueba cancelada")

if __name__ == "__main__":
    main() 