#!/usr/bin/env python3
"""
Script para debuggear la URL de base de datos que está usando el backend
"""

import os
from dotenv import load_dotenv

print("🔍 DEBUGGING DATABASE URL")
print("=" * 50)

# 1. Variable de entorno del sistema
print("1. Variable de entorno del sistema:")
system_url = os.getenv("DATABASE_URL")
print(f"   DATABASE_URL: {system_url}")

# 2. Cargar .env manualmente
print("\n2. Cargando .env manualmente:")
load_dotenv()
env_url = os.getenv("DATABASE_URL")
print(f"   DATABASE_URL después de load_dotenv(): {env_url}")

# 3. Verificar si son iguales
print(f"\n3. Comparación:")
print(f"   ¿Son iguales?: {system_url == env_url}")

# 4. Verificar el archivo .env directamente
print("\n4. Leyendo .env directamente:")
try:
    with open('.env', 'r') as f:
        for line in f:
            if line.startswith('DATABASE_URL='):
                file_url = line.strip().split('=', 1)[1]
                print(f"   DATABASE_URL en .env: {file_url}")
                break
except Exception as e:
    print(f"   Error leyendo .env: {e}")

# 5. Simular el proceso del backend
print("\n5. Simulando proceso del backend:")
import sys
from pathlib import Path

# Agregar el directorio backend al path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

# Agregar el directorio raíz al path para encontrar el .env
root_dir = backend_dir.parent
sys.path.insert(0, str(root_dir))

try:
    from app.core.database import engine
    print(f"   ✅ Módulo database importado correctamente")
    
    # Obtener la URL del engine
    engine_url = str(engine.url)
    print(f"   URL del engine: {engine_url}")
    
except Exception as e:
    print(f"   ❌ Error importando módulo database: {e}")

print("\n✅ Debug completado") 