#!/usr/bin/env python3
"""
Script para verificar qué tablas existen actualmente en la base de datos.
"""

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Agregar el directorio backend al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.core.database import DATABASE_URL

load_dotenv()

def check_existing_tables():
    """Verifica qué tablas existen en la base de datos."""
    try:
        print("🔍 Verificando tablas existentes en la base de datos...")
        
        # Crear engine
        engine = create_engine(DATABASE_URL)
        
        # Consultar tablas existentes
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            
            tables = [row[0] for row in result]
            
            print(f"📋 Tablas encontradas ({len(tables)}):")
            print("-" * 40)
            
            if tables:
                for table in tables:
                    print(f"  ✅ {table}")
            else:
                print("  ❌ No se encontraron tablas")
            
            # Verificar tablas específicas que necesitamos
            required_tables = [
                'claims',
                'claim_documents', 
                'claim_form_submissions',
                'claim_expenses',
                'coverages',
                'documents_ocr'
            ]
            
            print(f"\n🎯 Verificación de tablas requeridas:")
            print("-" * 40)
            
            missing_tables = []
            for table in required_tables:
                if table in tables:
                    print(f"  ✅ {table}")
                else:
                    print(f"  ❌ {table} - FALTA")
                    missing_tables.append(table)
            
            if missing_tables:
                print(f"\n⚠️ Tablas faltantes: {', '.join(missing_tables)}")
                return missing_tables
            else:
                print(f"\n🎉 Todas las tablas requeridas existen")
                return []
                
    except Exception as e:
        print(f"❌ Error verificando tablas: {e}")
        return None

def create_missing_tables(missing_tables):
    """Crea las tablas que faltan."""
    try:
        print(f"\n🔧 Creando tablas faltantes...")
        
        engine = create_engine(DATABASE_URL)
        
        # Importar modelos
        from app.core.models import Base, Claim, ClaimDocument, ClaimFormSubmission, ClaimExpense, Coverage, DocumentOCR
        
        # Mapeo de nombres de tabla a modelos
        table_models = {
            'claims': Claim,
            'claim_documents': ClaimDocument,
            'claim_form_submissions': ClaimFormSubmission,
            'claim_expenses': ClaimExpense,
            'coverages': Coverage,
            'documents_ocr': DocumentOCR
        }
        
        for table_name in missing_tables:
            if table_name in table_models:
                model = table_models[table_name]
                print(f"  🔨 Creando tabla: {table_name}")
                
                try:
                    model.__table__.create(engine, checkfirst=True)
                    print(f"    ✅ {table_name} creada exitosamente")
                except Exception as e:
                    print(f"    ❌ Error creando {table_name}: {e}")
            else:
                print(f"  ⚠️ Modelo no encontrado para tabla: {table_name}")
        
        print(f"\n🎉 Proceso de creación completado")
        
    except Exception as e:
        print(f"❌ Error creando tablas: {e}")

if __name__ == "__main__":
    print("🚀 Verificando estado de la base de datos")
    print("=" * 50)
    
    missing = check_existing_tables()
    
    if missing is not None and missing:
        create_missing_tables(missing)
    elif missing is None:
        print("\n💥 Error en la verificación")
        sys.exit(1)
    else:
        print("\n🎉 Base de datos está completa") 