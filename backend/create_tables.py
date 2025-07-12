#!/usr/bin/env python3
"""
Script para crear las tablas CLAIM_FORM y DOCUMENTS en la base de datos.
"""

import os
import sys
from dotenv import load_dotenv

# Buscar el archivo .env en el directorio raíz del proyecto
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
env_path = os.path.join(project_root, '.env')
load_dotenv(env_path)

def create_tables():
    """Crear las tablas en la base de datos."""
    try:
        print("🔧 Creando tablas en la base de datos...")
        
        # Importar los modelos y la base de datos
        from app.core.database import engine, Base
        from app.models.claim_models import ClaimForm, Document
        
        # Crear todas las tablas
        Base.metadata.create_all(bind=engine)
        
        print("✅ Tablas creadas exitosamente!")
        print("📋 Tablas creadas:")
        print("   - CLAIM_FORM")
        print("   - DOCUMENTS")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando las tablas: {e}")
        print("\n🔧 Posibles soluciones:")
        print("1. Verifica que la base de datos esté conectada")
        print("2. Verifica que las credenciales sean correctas")
        print("3. Verifica que el usuario tenga permisos para crear tablas")
        return False

def verify_tables():
    """Verificar que las tablas se crearon correctamente."""
    try:
        print("\n🔍 Verificando que las tablas se crearon...")
        
        from sqlalchemy import create_engine, text, inspect
        
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            raise ValueError("DATABASE_URL no está configurada en el archivo .env")
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            
            print(f"📋 Tablas encontradas: {len(tables)}")
            
            if 'claim_form' in tables and 'documents' in tables:
                print("✅ Tablas CLAIM_FORM y DOCUMENTS creadas correctamente")
                
                # Mostrar estructura de CLAIM_FORM
                print("\n📊 Estructura de CLAIM_FORM:")
                columns = inspector.get_columns('claim_form')
                for column in columns:
                    nullable = "NULL" if column['nullable'] else "NOT NULL"
                    print(f"   - {column['name']}: {column['type']} {nullable}")
                
                # Mostrar estructura de DOCUMENTS
                print("\n📊 Estructura de DOCUMENTS:")
                columns = inspector.get_columns('documents')
                for column in columns:
                    nullable = "NULL" if column['nullable'] else "NOT NULL"
                    print(f"   - {column['name']}: {column['type']} {nullable}")
                
                return True
            else:
                print("❌ No se encontraron las tablas esperadas")
                print(f"   Tablas encontradas: {tables}")
                return False
                
    except Exception as e:
        print(f"❌ Error verificando las tablas: {e}")
        return False

if __name__ == "__main__":
    print("🏗️ CREANDO TABLAS EN LA BASE DE DATOS")
    print("=" * 50)
    
    # Crear las tablas
    success = create_tables()
    
    if success:
        # Verificar que se crearon correctamente
        verify_success = verify_tables()
        
        if verify_success:
            print("\n🎉 ¡Tablas creadas y verificadas exitosamente!")
            print("   La base de datos está lista para usar.")
        else:
            print("\n⚠️  Las tablas se crearon pero la verificación falló.")
    else:
        print("\n❌ No se pudieron crear las tablas.")
        sys.exit(1) 