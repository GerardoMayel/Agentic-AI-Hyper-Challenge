#!/usr/bin/env python3
"""
Script para probar la conexión a la base de datos desde el contexto del backend
"""

import sys
import os
from pathlib import Path

# Agregar el directorio backend al path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Agregar el directorio raíz al path para encontrar el .env
root_dir = backend_dir.parent
sys.path.insert(0, str(root_dir))

from app.core.database import engine, get_db
from sqlalchemy import text

def test_database_connection():
    """Probar conexión a la base de datos desde el contexto del backend"""
    print("🧪 Probando conexión a la base de datos desde el contexto del backend...")
    
    try:
        # Probar conexión directa
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()
            print(f"✅ Conexión exitosa: {version[0]}")
            
            # Probar lectura de tablas
            result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"))
            tables = result.fetchall()
            print(f"📋 Tablas encontradas: {[table[0] for table in tables]}")
            
            # Probar inserción de prueba
            result = conn.execute(text("SELECT COUNT(*) FROM CLAIM_FORM;"))
            count = result.fetchone()
            print(f"📊 Registros en CLAIM_FORM: {count[0]}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
        return False

def test_session():
    """Probar sesión de base de datos"""
    print("\n🧪 Probando sesión de base de datos...")
    
    try:
        db_gen = get_db()
        db = next(db_gen)
        
        result = db.execute(text("SELECT 1 as test;"))
        test = result.fetchone()
        print(f"✅ Sesión funcionando: {test[0]}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Error de sesión: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de base de datos del backend...")
    
    # Probar conexión
    connection_ok = test_database_connection()
    
    # Probar sesión
    session_ok = test_session()
    
    if connection_ok and session_ok:
        print("\n✅ Todas las pruebas de base de datos pasaron")
        print("ℹ️  El backend debería poder conectarse correctamente")
    else:
        print("\n❌ Algunas pruebas fallaron")
        print("ℹ️  Revisa la configuración de la base de datos") 