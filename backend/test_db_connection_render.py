#!/usr/bin/env python3
"""
Test direct database connection from backend (Render)
"""
import os
import sys
import psycopg2


def main():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("❌ DATABASE_URL no está definida en el entorno.")
        sys.exit(1)
    print(f"🔍 DATABASE_URL: {db_url[:60]}...")
    try:
        print("🔌 Intentando conectar a la base de datos...")
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        result = cur.fetchone()
        print(f"✅ Conexión exitosa. Resultado SELECT 1: {result}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        sys.exit(2)

if __name__ == "__main__":
    main() 