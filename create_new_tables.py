#!/usr/bin/env python3
"""
Script para crear las nuevas tablas del sistema de claims en inglés.
"""

import os
import sys
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

from app.core.database import engine
from app.core.models import Base, Claim, ClaimDocument, ClaimFormSubmission, ClaimExpense, Coverage, CoverageType

def crear_tablas():
    """Crea todas las tablas en la base de datos."""
    try:
        print("🗄️ Creando nuevas tablas del sistema de claims...")
        
        # Crear todas las tablas
        Base.metadata.create_all(bind=engine)
        
        print("✅ Tablas creadas exitosamente:")
        print("   - claims")
        print("   - claim_documents")
        print("   - claim_form_submissions")
        print("   - claim_expenses")
        print("   - coverages")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando tablas: {e}")
        return False

def insertar_coberturas_iniciales():
    """Inserta las coberturas iniciales disponibles."""
    try:
        from app.core.database import get_db
        
        db = next(get_db())
        
        # Verificar si ya existen coberturas
        existing_coverages = db.query(Coverage).count()
        if existing_coverages > 0:
            print("ℹ️ Las coberturas ya existen, saltando inserción...")
            db.close()
            return True
        
        # Definir coberturas iniciales
        coverages_data = [
            {
                'coverage_type': CoverageType.TRIP_CANCELLATION,
                'name': 'Trip Cancellation',
                'description': 'For reimbursement of non-refundable trip payments when the customer cannot travel.'
            },
            {
                'coverage_type': CoverageType.TRIP_DELAY,
                'name': 'Trip Delay',
                'description': 'For reimbursement of out-of-pocket expenses (hotel, meals) due to an unforeseen delay.'
            },
            {
                'coverage_type': CoverageType.TRIP_INTERRUPTION,
                'name': 'Trip Interruption',
                'description': 'For reimbursement of unused trip portions or additional transportation costs due to an interruption.'
            },
            {
                'coverage_type': CoverageType.BAGGAGE_DELAY,
                'name': 'Baggage Delay',
                'description': 'For reimbursement of essential item purchases when luggage is delayed.'
            }
        ]
        
        # Insertar coberturas
        for coverage_data in coverages_data:
            coverage = Coverage(**coverage_data)
            db.add(coverage)
        
        db.commit()
        print("✅ Coberturas iniciales insertadas exitosamente")
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Error insertando coberturas: {e}")
        return False

def mostrar_estructura():
    """Muestra la estructura de las tablas."""
    print("\n📋 ESTRUCTURA DE TABLAS:")
    print("=" * 50)
    
    # Tabla claims
    print("\n🚨 claims:")
    print("   - id (PK)")
    print("   - claim_number (UNIQUE)")
    print("   - gmail_message_id (UNIQUE)")
    print("   - sender_email")
    print("   - sender_name")
    print("   - subject")
    print("   - email_content")
    print("   - notification_date")
    print("   - status (ENUM)")
    print("   - response_sent")
    print("   - response_sent_date")
    print("   - form_link_sent")
    print("   - form_link_sent_date")
    print("   - created_at")
    print("   - updated_at")
    
    # Tabla claim_documents
    print("\n📎 claim_documents:")
    print("   - id (PK)")
    print("   - claim_id (FK -> claims)")
    print("   - filename")
    print("   - mime_type")
    print("   - file_size_bytes")
    print("   - storage_url")
    print("   - storage_path")
    print("   - source_type")
    print("   - created_at")
    
    # Tabla claim_form_submissions
    print("\n📝 claim_form_submissions:")
    print("   - id (PK)")
    print("   - claim_id (FK -> claims)")
    print("   - coverage_type (ENUM)")
    print("   - claimant_name")
    print("   - all_claimants_names")
    print("   - email_address")
    print("   - mobile_phone")
    print("   - mailing_address")
    print("   - city")
    print("   - state")
    print("   - postal_code")
    print("   - policy_number")
    print("   - travel_agency")
    print("   - initial_deposit_date")
    print("   - incident_description")
    print("   - loss_date")
    print("   - total_amount_requested")
    print("   - submitted_via")
    print("   - submitted_at")
    
    # Tabla claim_expenses
    print("\n💰 claim_expenses:")
    print("   - id (PK)")
    print("   - form_submission_id (FK -> claim_form_submissions)")
    print("   - description")
    print("   - expense_date")
    print("   - amount_cents")
    print("   - created_at")
    
    # Tabla coverages
    print("\n🛡️ coverages:")
    print("   - id (PK)")
    print("   - coverage_type (ENUM, UNIQUE)")
    print("   - name")
    print("   - description")
    print("   - is_active")
    print("   - created_at")
    print("   - updated_at")

def main():
    """Función principal."""
    print("🚀 SISTEMA DE CLAIMS - CREACIÓN DE TABLAS NUEVAS")
    print("=" * 60)
    
    # Mostrar estructura
    mostrar_estructura()
    
    # Preguntar confirmación
    print("\n" + "=" * 60)
    confirmacion = input("¿Deseas crear las nuevas tablas? (y/N): ").strip().lower()
    
    if confirmacion in ['y', 'yes', 'sí', 'si']:
        if crear_tablas():
            print("\n✅ Tablas creadas exitosamente")
            
            # Insertar coberturas iniciales
            print("\n🛡️ Insertando coberturas iniciales...")
            if insertar_coberturas_iniciales():
                print("\n🎉 ¡Sistema de claims configurado exitosamente!")
                print("   El sistema está listo para procesar claims.")
            else:
                print("\n⚠️ Error insertando coberturas")
        else:
            print("\n❌ Error creando las tablas.")
    else:
        print("\n⚠️ Operación cancelada.")

if __name__ == "__main__":
    main() 