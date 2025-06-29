#!/usr/bin/env python3
"""
Script para validar la conexión a la base de datos.
"""

import os
import sys
from dotenv import load_dotenv

# Línea temporal para debug
env_path = os.path.abspath('.env')
print("RUTA ABSOLUTA .env:", env_path)

# Leer directamente el archivo .env
print("\nLEYENDO ARCHIVO .env DIRECTAMENTE:")
with open(env_path, 'r') as f:
    for i, line in enumerate(f, 1):
        if 'DATABASE_URL' in line:
            print(f"Línea {i}: {repr(line.strip())}")
            # Establecer la variable directamente
            if line.startswith('DATABASE_URL='):
                db_url = line.split('=', 1)[1].strip()
                os.environ['DATABASE_URL'] = db_url
                print(f"Variable establecida directamente: {repr(db_url)}")

# Forzar la lectura del archivo .env específico
load_dotenv(env_path)

# Debug: ver qué valor tiene DATABASE_URL después de load_dotenv
print("\nDATABASE_URL después de load_dotenv:", repr(os.getenv('DATABASE_URL')))

def test_database_connection():
    """Prueba la conexión a la base de datos."""
    try:
        # Mostrar la URL de la base de datos (sin credenciales)
        database_url = os.getenv('DATABASE_URL', 'No configurada')
        
        # Ocultar credenciales para mostrar
        if database_url != 'No configurada':
            # Extraer partes de la URL para mostrar de forma segura
            if '://' in database_url:
                protocol, rest = database_url.split('://', 1)
                if '@' in rest:
                    credentials, host_part = rest.split('@', 1)
                    safe_url = f"{protocol}://***:***@{host_part}"
                else:
                    safe_url = database_url
            else:
                safe_url = database_url
        else:
            safe_url = database_url
        
        print(f"🔍 URL de base de datos: {safe_url}")
        
        # Intentar importar y conectar
        from sqlalchemy import create_engine, text
        
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as test"))
            row = result.fetchone()
            
            if row and row[0] == 1:
                print("✅ Conexión a la base de datos exitosa")
                return True
            else:
                print("❌ Conexión fallida - respuesta inesperada")
                return False
                
    except Exception as e:
        print(f"❌ Error conectando a la base de datos: {e}")
        print("\n🔧 Posibles soluciones:")
        print("1. Verifica que DATABASE_URL esté configurado correctamente en .env")
        print("2. Verifica que la base de datos esté ejecutándose")
        print("3. Verifica que las credenciales sean correctas")
        print("4. Verifica que el puerto y host sean accesibles")
        return False

if __name__ == "__main__":
    print("🔍 VALIDANDO CONEXIÓN A BASE DE DATOS")
    print("=" * 50)
    
    success = test_database_connection()
    
    if success:
        print("\n🎉 ¡Base de datos conectada correctamente!")
        print("   Puedes proceder con la creación de tablas.")
    else:
        print("\n❌ No se pudo conectar a la base de datos.")
        print("   Por favor, verifica la configuración antes de continuar.") 