#!/usr/bin/env python3
"""
Script de utilidad para gestionar la base de datos del sistema de siniestros.
"""

import sys
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def show_help():
    """Show script help."""
    print("""
🔧 Database Manager - Claims System

Usage: python manage_db.py [command]

Available commands:
  init      - Initialize database with tables and sample data
  reset     - Reset database (WARNING! Deletes all data)
  test      - Test database connection
  migrate   - Run Alembic migrations
  create-migration - Create a new migration
  test-claim - Create a test claim
  stats     - Show database statistics
  help      - Show this help

Examples:
  python manage_db.py init
  python manage_db.py test
  python manage_db.py migrate
  python manage_db.py test-claim
  python manage_db.py stats
""")

def test_connection():
    """Test database connection."""
    try:
        from app.core.database import test_connection
        if test_connection():
            print("✅ Database connection successful")
            return True
        else:
            print("❌ Error: Could not connect to database")
            return False
    except Exception as e:
        print(f"❌ Error testing connection: {e}")
        return False

def run_migrations():
    """Ejecuta las migraciones de Alembic."""
    try:
        import subprocess
        result = subprocess.run(["alembic", "upgrade", "head"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Migraciones ejecutadas exitosamente")
            print(result.stdout)
        else:
            print("❌ Error ejecutando migraciones:")
            print(result.stderr)
            return False
        return True
    except FileNotFoundError:
        print("❌ Error: Alembic no está instalado o no está en el PATH")
        return False
    except Exception as e:
        print(f"❌ Error ejecutando migraciones: {e}")
        return False

def create_migration(message):
    """Crea una nueva migración de Alembic."""
    try:
        import subprocess
        result = subprocess.run(
            ["alembic", "revision", "--autogenerate", "-m", message], 
            capture_output=True, 
            text=True
        )
        if result.returncode == 0:
            print("✅ Migración creada exitosamente")
            print(result.stdout)
        else:
            print("❌ Error creando migración:")
            print(result.stderr)
            return False
        return True
    except FileNotFoundError:
        print("❌ Error: Alembic no está instalado o no está en el PATH")
        return False
    except Exception as e:
        print(f"❌ Error creando migración: {e}")
        return False

def show_stats():
    """Muestra estadísticas de la base de datos."""
    try:
        from app.core.database import SessionLocal
        from app.core.models import User, Policy, Coverage, Claim, Document, Communication
        
        db = SessionLocal()
        try:
            print("📊 Estadísticas de la Base de Datos:")
            print(f"   👥 Usuarios: {db.query(User).count()}")
            print(f"   📋 Pólizas: {db.query(Policy).count()}")
            print(f"   🛡️  Coberturas: {db.query(Coverage).count()}")
            print(f"   📝 Siniestros: {db.query(Claim).count()}")
            print(f"   📄 Documentos: {db.query(Document).count()}")
            print(f"   💬 Comunicaciones: {db.query(Communication).count()}")
            
            # Estadísticas por estado de siniestros
            from app.core.models import StatusEnum
            for status in StatusEnum:
                count = db.query(Claim).filter(Claim.status == status).count()
                if count > 0:
                    print(f"      - {status.value}: {count}")
                    
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Error obteniendo estadísticas: {e}")

def main():
    """Función principal del script."""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "help":
        show_help()
    
    elif command == "test":
        test_connection()
    
    elif command == "init":
        print("🔧 Inicializando base de datos del sistema de siniestros...")
        try:
            from app.core.init_db import init_db
            if init_db():
                print("🎉 Base de datos inicializada exitosamente")
            else:
                print("❌ Error inicializando la base de datos")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    elif command == "reset":
        print("⚠️  ¡ADVERTENCIA! Esto eliminará todos los datos de la base de datos.")
        confirm = input("¿Estás seguro? Escribe 'yes' para continuar: ")
        if confirm.lower() == "yes":
            try:
                from app.core.init_db import reset_db
                if reset_db():
                    print("🎉 Base de datos reseteada exitosamente")
                else:
                    print("❌ Error reseteando la base de datos")
            except Exception as e:
                print(f"❌ Error: {e}")
        else:
            print("❌ Operación cancelada")
    
    elif command == "migrate":
        print("🔄 Ejecutando migraciones...")
        run_migrations()
    
    elif command == "create-migration":
        if len(sys.argv) < 3:
            print("❌ Error: Debes proporcionar un mensaje para la migración")
            print("Uso: python manage_db.py create-migration 'Descripción de la migración'")
            return
        
        message = sys.argv[2]
        print(f"📝 Creando migración: {message}")
        create_migration(message)
    
    elif command == "test-claim":
        print("📝 Creando siniestro de prueba...")
        try:
            from app.core.init_db import create_test_claim
            claim = create_test_claim()
            if claim:
                print(f"✅ Siniestro de prueba creado: {claim.claim_number}")
            else:
                print("❌ Error creando siniestro de prueba")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    elif command == "stats":
        show_stats()
    
    else:
        print(f"❌ Comando desconocido: {command}")
        show_help()

if __name__ == "__main__":
    main() 