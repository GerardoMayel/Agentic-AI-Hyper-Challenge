"""
Script para inicializar la base de datos con datos de ejemplo para el sistema de claims.
Útil para desarrollo y testing.
"""

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, create_tables, test_connection
from app.core import crud
from app.core.models import Coverage, CoverageType
from datetime import datetime, timedelta

def init_db():
    """
    Inicializa la base de datos creando las tablas y datos de ejemplo.
    """
    print("🔧 Inicializando base de datos del sistema de claims...")
    
    # Crear las tablas
    create_tables()
    print("✅ Tablas creadas exitosamente")
    
    # Verificar conexión
    if not test_connection():
        print("❌ Error: No se pudo conectar a la base de datos")
        return False
    
    print("✅ Conexión a la base de datos verificada")
    
    # Crear datos de ejemplo
    db = SessionLocal()
    try:
        # Crear coberturas de ejemplo
        print("🛡️ Creando coberturas de ejemplo...")
        
        coverages_data = [
            {
                "coverage_type": CoverageType.TRIP_CANCELLATION,
                "name": "Trip Cancellation",
                "description": "Coverage for trip cancellation due to covered reasons"
            },
            {
                "coverage_type": CoverageType.TRIP_DELAY,
                "name": "Trip Delay",
                "description": "Coverage for trip delays and related expenses"
            },
            {
                "coverage_type": CoverageType.TRIP_INTERRUPTION,
                "name": "Trip Interruption",
                "description": "Coverage for trip interruption and early return"
            },
            {
                "coverage_type": CoverageType.BAGGAGE_DELAY,
                "name": "Baggage Delay",
                "description": "Coverage for delayed or lost baggage"
            }
        ]
        
        for coverage_data in coverages_data:
            existing = crud.get_coverage_by_type(db, coverage_data["coverage_type"])
            if not existing:
                coverage = Coverage(**coverage_data)
                db.add(coverage)
                print(f"✅ Cobertura creada: {coverage.name}")
            else:
                print(f"✅ Cobertura ya existe: {existing.name}")
        
        db.commit()
        print("✅ Base de datos inicializada correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error inicializando base de datos: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def reset_db():
    """
    Resetea la base de datos eliminando todas las tablas y recreándolas.
    ¡CUIDADO! Esto eliminará todos los datos.
    """
    print("⚠️  RESETEANDO BASE DE DATOS - TODOS LOS DATOS SERÁN ELIMINADOS")
    response = input("¿Estás seguro? Escribe 'SI' para confirmar: ")
    
    if response != "SI":
        print("❌ Operación cancelada")
        return False
    
    try:
        from app.core.database import engine, Base
        Base.metadata.drop_all(bind=engine)
        print("✅ Todas las tablas eliminadas")
        
        return init_db()
        
    except Exception as e:
        print(f"❌ Error reseteando base de datos: {e}")
        return False

def create_test_claim():
    """
    Crea un claim de prueba para testing.
    """
    print("🧪 Creando claim de prueba...")
    
    db = SessionLocal()
    try:
        from app.core.models import Claim, ClaimStatus, generate_claim_number
        
        # Crear claim de prueba
        claim = Claim(
            claim_number=generate_claim_number(),
            gmail_message_id="test_message_123",
            sender_email="test@example.com",
            sender_name="Test User",
            subject="Test Claim",
            email_content="This is a test claim for testing purposes.",
            notification_date=datetime.now(),
            status=ClaimStatus.INITIAL_NOTIFICATION
        )
        
        db.add(claim)
        db.commit()
        db.refresh(claim)
        
        print(f"✅ Claim de prueba creado: {claim.claim_number}")
        return claim
        
    except Exception as e:
        print(f"❌ Error creando claim de prueba: {e}")
        db.rollback()
        return None
    finally:
        db.close()

if __name__ == "__main__":
    init_db() 