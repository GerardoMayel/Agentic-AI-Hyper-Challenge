#!/usr/bin/env python3
"""
Script para revisar una base de datos específica proporcionando la URL.
Uso: python check_specific_database.py "postgresql://usuario:password@host:puerto/nombre_db"
"""

import os
import sys
from sqlalchemy import create_engine, text, inspect

def check_database(database_url):
    """Revisa una base de datos específica."""
    try:
        print(f"🔍 Revisando base de datos...")
        
        # Ocultar credenciales para mostrar
        if '://' in database_url:
            protocol, rest = database_url.split('://', 1)
            if '@' in rest:
                credentials, host_part = rest.split('@', 1)
                safe_url = f"{protocol}://***:***@{host_part}"
            else:
                safe_url = database_url
        else:
            safe_url = database_url
        
        print(f"🔍 URL de base de datos: {safe_url}")
        
        # Crear engine y conectar
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Probar conexión básica
            result = conn.execute(text("SELECT 1 as test"))
            row = result.fetchone()
            
            if row and row[0] == 1:
                print("✅ Conexión a la base de datos exitosa")
                
                # Obtener nombre de la base de datos
                result = conn.execute(text("SELECT current_database()"))
                db_row = result.fetchone()
                if db_row:
                    db_name = db_row[0]
                    print(f"✅ Conectado a la base de datos: {db_name}")
                
                # Obtener versión de PostgreSQL
                result = conn.execute(text("SELECT version()"))
                version_row = result.fetchone()
                if version_row:
                    print(f"📊 Versión PostgreSQL: {version_row[0]}")
                
                # Leer tablas existentes
                inspector = inspect(engine)
                tables = inspector.get_table_names()
                
                print(f"\n📋 Tablas encontradas en la base de datos: {len(tables)}")
                
                if not tables:
                    print("  📭 No hay tablas - la base de datos está vacía")
                else:
                    print("  📊 Tablas existentes:")
                    for i, table_name in enumerate(tables, 1):
                        print(f"    {i}. {table_name}")
                        
                        # Obtener columnas de cada tabla
                        columns = inspector.get_columns(table_name)
                        print(f"       Columnas ({len(columns)}):")
                        for column in columns:
                            nullable = "NULL" if column['nullable'] else "NOT NULL"
                            print(f"         - {column['name']}: {column['type']} {nullable}")
                        
                        # Obtener índices
                        indexes = inspector.get_indexes(table_name)
                        if indexes:
                            print(f"       Índices ({len(indexes)}):")
                            for index in indexes:
                                unique = "UNIQUE" if index['unique'] else ""
                                column_names = [name for name in index['column_names'] if name is not None]
                                print(f"         - {index['name']}: {', '.join(column_names)} {unique}")
                        
                        print()  # Línea vacía entre tablas
                
                return True
            else:
                print("❌ Conexión fallida - respuesta inesperada")
                return False
                
    except Exception as e:
        print(f"❌ Error conectando a la base de datos: {e}")
        print("\n🔧 Posibles soluciones:")
        print("1. Verifica que la URL de la base de datos sea correcta")
        print("2. Verifica que la base de datos esté ejecutándose")
        print("3. Verifica que las credenciales sean correctas")
        print("4. Verifica que el puerto y host sean accesibles")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❌ Uso incorrecto!")
        print("Uso: python check_specific_database.py \"postgresql://usuario:password@host:puerto/nombre_db\"")
        print("\nEjemplo:")
        print("python check_specific_database.py \"postgresql://user:pass@localhost:5432/mydb\"")
        sys.exit(1)
    
    database_url = sys.argv[1]
    
    print("🔍 REVISANDO BASE DE DATOS ESPECÍFICA")
    print("=" * 60)
    
    success = check_database(database_url)
    
    if success:
        print("\n🎉 ¡Base de datos revisada correctamente!")
    else:
        print("\n❌ No se pudo revisar la base de datos.")
        sys.exit(1) 