#!/usr/bin/env python3
"""
Script simple para probar conexión a la base de datos
"""

import os
from dotenv import load_dotenv
import psycopg2
from sqlalchemy import create_engine, text

# Cargar variables de entorno
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
print(f"🔗 URL de la base de datos: {DATABASE_URL}")

# Probar con psycopg2 directamente
print("\n🧪 Probando con psycopg2...")
try:
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"✅ Conexión psycopg2 exitosa: {version[0]}")
    cursor.close()
    conn.close()
except Exception as e:
    print(f"❌ Error psycopg2: {str(e)}")

# Probar con SQLAlchemy
print("\n🧪 Probando con SQLAlchemy...")
try:
    # Agregar parámetros SSL
    if DATABASE_URL.startswith("postgresql://"):
        if "?" not in DATABASE_URL:
            sqlalchemy_url = DATABASE_URL + "?sslmode=require"
        elif "sslmode" not in DATABASE_URL:
            sqlalchemy_url = DATABASE_URL + "&sslmode=require"
        else:
            sqlalchemy_url = DATABASE_URL
    else:
        sqlalchemy_url = DATABASE_URL
    
    print(f"🔗 URL SQLAlchemy: {sqlalchemy_url}")
    
    engine = create_engine(sqlalchemy_url, pool_pre_ping=True)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        version = result.fetchone()
        print(f"✅ Conexión SQLAlchemy exitosa: {version[0]}")
        
        # Probar lectura de tablas
        result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"))
        tables = result.fetchall()
        print(f"📋 Tablas encontradas: {[table[0] for table in tables]}")
        
except Exception as e:
    print(f"❌ Error SQLAlchemy: {str(e)}")

print("\n✅ Prueba de conexión completada") 