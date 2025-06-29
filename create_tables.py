#!/usr/bin/env python3
"""
Script para crear las tablas de la base de datos para el sistema de claims.
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import text

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
from app.core.models import Base, Siniestro, Documento

def crear_tablas():
    """Crea todas las tablas en la base de datos."""
    try:
        print("🗄️ Creando tablas en la base de datos...")
        
        # Crear todas las tablas
        Base.metadata.create_all(bind=engine)
        
        print("✅ Tablas creadas exitosamente:")
        print("   - siniestros")
        print("   - documentos")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando tablas: {e}")
        return False

def verificar_conexion():
    """Verifica la conexión a la base de datos."""
    try:
        # Intentar conectar
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Conexión a la base de datos exitosa")
            return True
    except Exception as e:
        print(f"❌ Error conectando a la base de datos: {e}")
        print("   Verifica que DATABASE_URL esté configurado correctamente en .env")
        return False

def mostrar_estructura():
    """Muestra la estructura de las tablas."""
    print("\n📋 ESTRUCTURA DE TABLAS:")
    print("=" * 50)
    
    # Tabla siniestros
    print("\n🚨 siniestros:")
    print("   - id (PK)")
    print("   - numero_siniestro (UNIQUE)")
    print("   - gmail_message_id (UNIQUE)")
    print("   - remitente_email")
    print("   - remitente_nombre")
    print("   - subject")
    print("   - contenido_texto")
    print("   - fecha_reporte")
    print("   - created_at")
    
    # Tabla documentos
    print("\n📎 documentos:")
    print("   - id (PK)")
    print("   - siniestro_id (FK -> siniestros)")
    print("   - nombre_archivo")
    print("   - tipo_mime")
    print("   - tamaño_bytes")
    print("   - url_storage")
    print("   - ruta_storage")
    print("   - created_at")

def main():
    """Función principal."""
    print("🚀 SISTEMA DE CLAIMS - CREACIÓN DE TABLAS")
    print("=" * 50)
    
    # Verificar conexión
    if not verificar_conexion():
        return
    
    # Mostrar estructura
    mostrar_estructura()
    
    # Preguntar confirmación
    print("\n" + "=" * 50)
    confirmacion = input("¿Deseas crear las tablas? (y/N): ").strip().lower()
    
    if confirmacion in ['y', 'yes', 'sí', 'si']:
        if crear_tablas():
            print("\n🎉 ¡Tablas creadas exitosamente!")
            print("   El sistema está listo para procesar emails de claims.")
        else:
            print("\n❌ Error creando las tablas.")
    else:
        print("\n⚠️ Operación cancelada.")

if __name__ == "__main__":
    main() 