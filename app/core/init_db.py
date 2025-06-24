"""
Script para inicializar la base de datos con datos de ejemplo para el sistema de siniestros.
Útil para desarrollo y testing.
"""

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, create_tables, test_connection
from app.core import crud
from app.core.models import User, Policy, Coverage, StatusEnum
from datetime import datetime, timedelta

def init_db():
    """
    Inicializa la base de datos creando las tablas y datos de ejemplo.
    """
    print("🔧 Inicializando base de datos del sistema de siniestros...")
    
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
        # 1. Crear usuarios de ejemplo
        print("👥 Creando usuarios de ejemplo...")
        
        # Usuario administrador
        admin_user = crud.get_user_by_username(db, "admin")
        if not admin_user:
            admin_user = crud.create_user(
                db=db,
                username="admin",
                hashed_password="hashed_admin_password",  # En producción usar bcrypt
                role="admin"
            )
            print(f"✅ Usuario administrador creado: {admin_user.username}")
        else:
            print(f"✅ Usuario administrador ya existe: {admin_user.username}")
        
        # Usuario analista
        analyst_user = crud.get_user_by_username(db, "analyst1")
        if not analyst_user:
            analyst_user = crud.create_user(
                db=db,
                username="analyst1",
                hashed_password="hashed_analyst_password",
                role="analyst"
            )
            print(f"✅ Usuario analista creado: {analyst_user.username}")
        else:
            print(f"✅ Usuario analista ya existe: {analyst_user.username}")
        
        # 2. Crear pólizas de ejemplo
        print("📋 Creando pólizas de ejemplo...")
        
        # Póliza 1 - Viaje
        policy1 = crud.get_policy_by_number(db, "POL-VIAJE-2024-001")
        if not policy1:
            policy1 = crud.create_policy(
                db=db,
                policy_number="POL-VIAJE-2024-001",
                customer_email="cliente1@example.com",
                customer_name="María González",
                start_date=datetime.now() - timedelta(days=30),
                end_date=datetime.now() + timedelta(days=335)
            )
            print(f"✅ Póliza de viaje creada: {policy1.policy_number}")
        else:
            print(f"✅ Póliza de viaje ya existe: {policy1.policy_number}")
        
        # Póliza 2 - Hogar
        policy2 = crud.get_policy_by_number(db, "POL-HOGAR-2024-002")
        if not policy2:
            policy2 = crud.create_policy(
                db=db,
                policy_number="POL-HOGAR-2024-002",
                customer_email="cliente2@example.com",
                customer_name="Juan Pérez",
                start_date=datetime.now() - timedelta(days=60),
                end_date=datetime.now() + timedelta(days=305)
            )
            print(f"✅ Póliza de hogar creada: {policy2.policy_number}")
        else:
            print(f"✅ Póliza de hogar ya existe: {policy2.policy_number}")
        
        # Póliza 3 - Auto
        policy3 = crud.get_policy_by_number(db, "POL-AUTO-2024-003")
        if not policy3:
            policy3 = crud.create_policy(
                db=db,
                policy_number="POL-AUTO-2024-003",
                customer_email="cliente3@example.com",
                customer_name="Ana Rodríguez",
                start_date=datetime.now() - timedelta(days=15),
                end_date=datetime.now() + timedelta(days=350)
            )
            print(f"✅ Póliza de auto creada: {policy3.policy_number}")
        else:
            print(f"✅ Póliza de auto ya existe: {policy3.policy_number}")
        
        # 3. Crear coberturas para las pólizas
        print("🛡️ Creando coberturas de ejemplo...")
        
        # Coberturas para póliza de viaje
        if not crud.get_coverages_by_policy(db, policy1.id):
            crud.create_coverage(
                db=db,
                policy_id=policy1.id,
                coverage_type="BAGGAGE_DELAY",
                limit_amount=500.0,
                deductible=50.0,
                description="Cobertura por retraso de equipaje"
            )
            crud.create_coverage(
                db=db,
                policy_id=policy1.id,
                coverage_type="MEDICAL_EXPENSES",
                limit_amount=10000.0,
                deductible=100.0,
                description="Gastos médicos durante el viaje"
            )
            crud.create_coverage(
                db=db,
                policy_id=policy1.id,
                coverage_type="TRIP_CANCELLATION",
                limit_amount=2000.0,
                deductible=0.0,
                description="Cancelación de viaje"
            )
            print(f"✅ Coberturas creadas para póliza {policy1.policy_number}")
        
        # Coberturas para póliza de hogar
        if not crud.get_coverages_by_policy(db, policy2.id):
            crud.create_coverage(
                db=db,
                policy_id=policy2.id,
                coverage_type="FIRE_DAMAGE",
                limit_amount=50000.0,
                deductible=500.0,
                description="Daños por incendio"
            )
            crud.create_coverage(
                db=db,
                policy_id=policy2.id,
                coverage_type="THEFT",
                limit_amount=10000.0,
                deductible=200.0,
                description="Robo de bienes personales"
            )
            print(f"✅ Coberturas creadas para póliza {policy2.policy_number}")
        
        # Coberturas para póliza de auto
        if not crud.get_coverages_by_policy(db, policy3.id):
            crud.create_coverage(
                db=db,
                policy_id=policy3.id,
                coverage_type="COLLISION",
                limit_amount=25000.0,
                deductible=500.0,
                description="Daños por colisión"
            )
            crud.create_coverage(
                db=db,
                policy_id=policy3.id,
                coverage_type="LIABILITY",
                limit_amount=100000.0,
                deductible=0.0,
                description="Responsabilidad civil"
            )
            print(f"✅ Coberturas creadas para póliza {policy3.policy_number}")
        
        # 4. Crear algunos siniestros de ejemplo
        print("📝 Creando siniestros de ejemplo...")
        
        # Siniestro 1 - Retraso de equipaje
        if not crud.get_claims_by_policy(db, policy1.id):
            claim1 = crud.create_claim(db, policy1)
            crud.update_claim_summary(
                db=db,
                claim_id=claim1.id,
                summary_ai="Cliente reporta retraso de equipaje en vuelo Madrid-Barcelona. Equipaje llegó 24 horas después. Solicitando compensación por gastos de ropa y artículos de aseo."
            )
            crud.assign_claim_to_analyst(db, claim1.id, analyst_user.id)
            print(f"✅ Siniestro de retraso de equipaje creado: {claim1.claim_number}")
        
        # Siniestro 2 - Daños por agua en hogar
        if not crud.get_claims_by_policy(db, policy2.id):
            claim2 = crud.create_claim(db, policy2)
            crud.update_claim_summary(
                db=db,
                claim_id=claim2.id,
                summary_ai="Fuga de agua en baño causó daños en paredes y suelo. Cliente estima daños en €3,000. Necesita evaluación de perito."
            )
            crud.update_claim_status(db, claim2.id, StatusEnum.PENDING_CUSTOMER_DOCUMENTS)
            print(f"✅ Siniestro de daños por agua creado: {claim2.claim_number}")
        
        print("🎉 Base de datos del sistema de siniestros inicializada exitosamente")
        print("\n📊 Datos de ejemplo creados:")
        print(f"   - Usuarios: {db.query(User).count()}")
        print(f"   - Pólizas: {db.query(Policy).count()}")
        print(f"   - Coberturas: {db.query(Coverage).count()}")
        print(f"   - Siniestros: {db.query(Claim).count()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error inicializando base de datos: {e}")
        return False
    finally:
        db.close()

def reset_db():
    """
    Resetea la base de datos eliminando todas las tablas y recreándolas.
    ¡CUIDADO! Esto elimina todos los datos.
    """
    from app.core.database import drop_tables
    
    print("⚠️  Reseteando base de datos del sistema de siniestros...")
    print("⚠️  ¡ADVERTENCIA! Esto eliminará todos los datos existentes.")
    
    try:
        drop_tables()
        print("✅ Tablas eliminadas")
        
        init_db()
        print("✅ Base de datos reseteada exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error reseteando base de datos: {e}")
        return False

def create_test_claim():
    """
    Crea un siniestro de prueba para testing.
    """
    db = SessionLocal()
    try:
        # Buscar una póliza existente
        policy = db.query(Policy).first()
        if not policy:
            print("❌ No hay pólizas disponibles para crear siniestro de prueba")
            return None
        
        # Crear siniestro
        claim = crud.create_claim(db, policy)
        print(f"✅ Siniestro de prueba creado: {claim.claim_number}")
        return claim
        
    except Exception as e:
        print(f"❌ Error creando siniestro de prueba: {e}")
        return None
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "reset":
            reset_db()
        elif sys.argv[1] == "test-claim":
            create_test_claim()
        else:
            print("Comandos disponibles: reset, test-claim")
    else:
        init_db() 