#!/usr/bin/env python3
"""
Script para recrear todas las tablas con la nueva estructura alineada con el formulario.
"""

import os
import sys
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.models import Base, Claim, ClaimDocument, ClaimFormSubmission, ClaimExpense, Coverage, CoverageType, ClaimStatus

def get_database_url():
    """Obtiene la URL de la base de datos desde variables de entorno."""
    import os
    return os.getenv("DATABASE_URL", "sqlite:///claims_management.db")

def recreate_tables():
    """Recrea todas las tablas con la nueva estructura."""
    
    print("🔄 Recreando tablas con nueva estructura...")
    
    # Obtener la URL de la base de datos
    database_url = get_database_url()
    print(f"📊 Base de datos: {database_url}")
    
    # Crear engine
    engine = create_engine(database_url)
    
    # Eliminar todas las tablas existentes
    print("🗑️  Eliminando tablas existentes...")
    Base.metadata.drop_all(engine)
    
    # Crear todas las tablas con la nueva estructura
    print("🏗️  Creando nuevas tablas...")
    Base.metadata.create_all(engine)
    
    # Crear sesión para insertar datos de ejemplo
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    
    try:
        # Insertar tipos de cobertura
        print("📋 Insertando tipos de cobertura...")
        coverages = [
            Coverage(
                coverage_type=CoverageType.TRIP_CANCELLATION,
                name="Trip Cancellation",
                description="Cancellation of trip before departure"
            ),
            Coverage(
                coverage_type=CoverageType.TRIP_DELAY,
                name="Trip Delay", 
                description="Delay in trip departure or arrival"
            ),
            Coverage(
                coverage_type=CoverageType.TRIP_INTERRUPTION,
                name="Trip Interruption",
                description="Interruption during the trip"
            ),
            Coverage(
                coverage_type=CoverageType.BAGGAGE_DELAY,
                name="Baggage Delay",
                description="Delay or loss of baggage"
            )
        ]
        
        for coverage in coverages:
            session.add(coverage)
        
        # Crear un claim de ejemplo
        print("📝 Creando claim de ejemplo...")
        example_claim = Claim(
            claim_number="CLAIM-20240115-0001",
            gmail_message_id="example_message_id_123",
            sender_email="john.doe@example.com",
            sender_name="John Doe",
            subject="Trip Cancellation Claim",
            email_content="I need to cancel my trip due to illness",
            notification_date=datetime.now(),
            status=ClaimStatus.INITIAL_NOTIFICATION
        )
        session.add(example_claim)
        session.flush()  # Para obtener el ID del claim
        
        # Crear un formulario de ejemplo
        print("📄 Creando formulario de ejemplo...")
        example_form = ClaimFormSubmission(
            claim_id=example_claim.id,
            coverage_type=CoverageType.TRIP_CANCELLATION,
            claimant_name="John Doe",
            email_address="john.doe@example.com",
            all_claimants_names="John Doe, Jane Doe",
            mailing_address="123 Main St, Anytown, USA",
            city="Anytown",
            state="California",
            postal_code="90210",
            mobile_phone="+1-555-123-4567",
            other_phone="+1-555-987-6543",
            policy_number="POL-2024-001",
            travel_agency="TravelCo Inc",
            initial_deposit_date=datetime(2024, 1, 1),
            loss_date=datetime(2024, 1, 10),
            total_amount_requested=2500.00,
            incident_description="I had to cancel my trip due to a medical emergency. I was diagnosed with appendicitis and required immediate surgery. The doctor advised against travel for at least 4 weeks.",
            declaration_accepted=True,
            signature_name="John Doe",
            signature_date=datetime.now(),
            submitted_via="web_form",
            ip_address="192.168.1.1",
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        session.add(example_form)
        session.flush()  # Para obtener el ID del formulario
        
        # Crear gastos de ejemplo
        print("💰 Creando gastos de ejemplo...")
        example_expenses = [
            ClaimExpense(
                form_submission_id=example_form.id,
                description="Hotel cancellation fee",
                expense_date=datetime(2024, 1, 10),
                amount=500.00
            ),
            ClaimExpense(
                form_submission_id=example_form.id,
                description="Airline cancellation fee",
                expense_date=datetime(2024, 1, 10),
                amount=200.00
            ),
            ClaimExpense(
                form_submission_id=example_form.id,
                description="Travel insurance premium",
                expense_date=datetime(2024, 1, 1),
                amount=150.00
            )
        ]
        
        for expense in example_expenses:
            session.add(expense)
        
        # Crear documento de ejemplo
        print("📎 Creando documento de ejemplo...")
        example_document = ClaimDocument(
            claim_id=example_claim.id,
            filename="medical_certificate.pdf",
            mime_type="application/pdf",
            file_size_bytes=1024000,  # 1MB
            storage_url="https://storage.googleapis.com/claims-bucket/documents/medical_certificate.pdf",
            storage_path="documents/medical_certificate.pdf",
            source_type="web_form"
        )
        session.add(example_document)
        
        # Commit todos los cambios
        session.commit()
        
        print("✅ Tablas recreadas exitosamente!")
        print("📊 Datos de ejemplo insertados:")
        print(f"   - Tipos de cobertura: {len(coverages)}")
        print(f"   - Claims: 1")
        print(f"   - Formularios: 1")
        print(f"   - Gastos: {len(example_expenses)}")
        print(f"   - Documentos: 1")
        
        # Verificar la estructura
        print("\n🔍 Verificando estructura de tablas...")
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        for table in tables:
            print(f"   📋 Tabla: {table}")
            columns = inspector.get_columns(table)
            for column in columns:
                print(f"      - {column['name']}: {column['type']}")
            print()
        
    except Exception as e:
        print(f"❌ Error al recrear tablas: {e}")
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == "__main__":
    recreate_tables() 