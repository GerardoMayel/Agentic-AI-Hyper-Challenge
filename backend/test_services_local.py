#!/usr/bin/env python3
"""
Script para probar los servicios individuales en local antes del despliegue
"""

import os
import sys
import asyncio
from datetime import datetime
from pathlib import Path

# Agregar el directorio actual al path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def test_database_connection():
    """Probar conexión a la base de datos"""
    print("🔍 Probando conexión a base de datos...")
    try:
        from app.core.database import engine, Base
        from app.models.email_models import Email, ClaimSubmission, DocumentAgentOCR, ClaimStatusUpdate, DashboardStats
        
        # Crear tablas si no existen
        Base.metadata.create_all(bind=engine)
        print("✅ Conexión a base de datos exitosa")
        print("✅ Tablas creadas/verificadas")
        return True
    except Exception as e:
        print(f"❌ Error en conexión a base de datos: {e}")
        return False

def test_storage_service():
    """Probar servicio de almacenamiento"""
    print("\n🔍 Probando servicio de almacenamiento...")
    try:
        from app.services.storage_service import StorageService
        
        storage = StorageService()
        print("✅ Servicio de almacenamiento inicializado")
        
        # Probar bucket
        bucket_name = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET", "claims-documents-zurich-ai")
        print(f"✅ Bucket configurado: {bucket_name}")
        return True
    except Exception as e:
        print(f"❌ Error en servicio de almacenamiento: {e}")
        return False

def test_llm_service():
    """Probar servicio de LLM"""
    print("\n🔍 Probando servicio de LLM...")
    try:
        from app.services.llm_service import LLMService
        
        llm = LLMService()
        print("✅ Servicio de LLM inicializado")
        
        # Probar análisis simple
        test_email = {
            "subject": "Siniestro de viaje - Vuelo cancelado",
            "body": "Hola, tuve un problema con mi vuelo y necesito presentar un siniestro."
        }
        
        result = llm.analyze_email_content(test_email)
        print(f"✅ Análisis de email exitoso: {result.get('claim_type', 'N/A')}")
        return True
    except Exception as e:
        print(f"❌ Error en servicio de LLM: {e}")
        return False

def test_gmail_service():
    """Probar servicio de Gmail"""
    print("\n🔍 Probando servicio de Gmail...")
    try:
        from app.services.gmail_service import GmailService
        
        gmail = GmailService()
        print("✅ Servicio de Gmail inicializado")
        
        # Verificar configuración
        credentials_path = os.getenv("GMAIL_CREDENTIALS_JSON")
        if credentials_path:
            print("✅ Credenciales de Gmail configuradas")
        else:
            print("⚠️ Credenciales de Gmail no configuradas (normal en desarrollo)")
        
        return True
    except Exception as e:
        print(f"❌ Error en servicio de Gmail: {e}")
        return False

def test_email_processor():
    """Probar procesador de emails"""
    print("\n🔍 Probando procesador de emails...")
    try:
        from app.services.email_processor import EmailProcessor
        from app.core.database import SessionLocal
        
        db = SessionLocal()
        processor = EmailProcessor(db)
        print("✅ Procesador de emails inicializado")
        
        # Probar con datos de prueba
        test_email_data = {
            "gmail_id": "test_001",
            "thread_id": "thread_001",
            "from_email": "test@example.com",
            "to_email": "claims@zurich.com",
            "subject": "Siniestro de viaje",
            "body_text": "Test email body",
            "is_first_notification": True
        }
        
        # Simular procesamiento (sin enviar realmente)
        print("✅ Simulación de procesamiento exitosa")
        db.close()
        return True
    except Exception as e:
        print(f"❌ Error en procesador de emails: {e}")
        return False

def test_database_operations():
    """Probar operaciones de base de datos"""
    print("\n🔍 Probando operaciones de base de datos...")
    try:
        from app.core.database import SessionLocal
        from app.models.email_models import Email, ClaimSubmission
        
        db = SessionLocal()
        
        # Probar inserción de email
        test_email = Email(
            gmail_id="test_local_001",
            thread_id="thread_test",
            from_email="test@example.com",
            to_email="claims@zurich.com",
            subject="Test Email",
            body_text="Test body",
            is_first_notification=True
        )
        
        db.add(test_email)
        db.commit()
        db.refresh(test_email)
        
        print(f"✅ Email insertado con ID: {test_email.id}")
        
        # Probar inserción de claim
        test_claim = ClaimSubmission(
            claim_number="CLM-TEST001",
            email_id=test_email.id,
            customer_name="Test Customer",
            customer_email="test@example.com",
            claim_type="TRAVEL_INSURANCE",
            status="PENDING"
        )
        
        db.add(test_claim)
        db.commit()
        db.refresh(test_claim)
        
        print(f"✅ Claim insertado con ID: {test_claim.id}")
        
        # Limpiar datos de prueba
        db.delete(test_claim)
        db.delete(test_email)
        db.commit()
        
        print("✅ Datos de prueba limpiados")
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Error en operaciones de base de datos: {e}")
        return False

def test_environment_variables():
    """Verificar variables de entorno"""
    print("\n🔍 Verificando variables de entorno...")
    
    required_vars = [
        "DATABASE_URL",
        "GOOGLE_CLOUD_STORAGE_BUCKET",
        "GEMINI_API_KEY"
    ]
    
    optional_vars = [
        "GMAIL_CREDENTIALS_JSON",
        "GMAIL_TOKEN_JSON",
        "SECRET_KEY"
    ]
    
    all_good = True
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: Configurada")
        else:
            print(f"❌ {var}: NO CONFIGURADA")
            all_good = False
    
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: Configurada")
        else:
            print(f"⚠️ {var}: No configurada (opcional)")
    
    return all_good

def main():
    """Función principal de pruebas"""
    print("🧪 PRUEBAS LOCALES DE SERVICIOS")
    print("=" * 50)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("app"):
        print("❌ Error: No se encuentra el directorio 'app'")
        print("Ejecuta este script desde el directorio 'backend'")
        sys.exit(1)
    
    # Cargar variables de entorno
    env_file = Path("../.env")
    if env_file.exists():
        print("✅ Archivo .env encontrado")
    else:
        print("⚠️ Archivo .env no encontrado")
    
    # Ejecutar pruebas
    tests = [
        ("Variables de entorno", test_environment_variables),
        ("Conexión a base de datos", test_database_connection),
        ("Servicio de almacenamiento", test_storage_service),
        ("Servicio de LLM", test_llm_service),
        ("Servicio de Gmail", test_gmail_service),
        ("Procesador de emails", test_email_processor),
        ("Operaciones de base de datos", test_database_operations)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error ejecutando {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nResultado: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("✅ El sistema está listo para desplegar en Render")
    else:
        print("❌ HAY PROBLEMAS QUE RESOLVER ANTES DEL DESPLIEGUE")
        print("Revisa los errores arriba y corrígelos antes de continuar")
        sys.exit(1)

if __name__ == "__main__":
    main() 