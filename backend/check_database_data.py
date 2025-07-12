#!/usr/bin/env python3
"""
Script para verificar los datos guardados en las tablas CLAIM_FORM y DOCUMENTS
"""

import os
import sys
from dotenv import load_dotenv

# Buscar el archivo .env en el directorio raíz del proyecto
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
env_path = os.path.join(project_root, '.env')
load_dotenv(env_path)

def check_database_data():
    """Verificar los datos guardados en la base de datos"""
    try:
        print("🔍 Verificando datos en la base de datos...")
        
        from sqlalchemy import create_engine, text
        
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            raise ValueError("DATABASE_URL no está configurada en el archivo .env")
        
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Verificar datos en CLAIM_FORM
            print("\n📋 Datos en tabla CLAIM_FORM:")
            result = conn.execute(text("SELECT * FROM \"CLAIM_FORM\" ORDER BY created_at DESC"))
            claims = result.fetchall()
            
            if not claims:
                print("   📭 No hay registros en CLAIM_FORM")
            else:
                print(f"   📊 Total de reclamos: {len(claims)}")
                for i, claim in enumerate(claims, 1):
                    print(f"\n   🏷️  Reclamo {i}:")
                    print(f"      - ID: {claim.id}")
                    print(f"      - Claim ID: {claim.claim_id}")
                    print(f"      - Nombre: {claim.full_name}")
                    print(f"      - Email: {claim.email}")
                    print(f"      - Tipo de cobertura: {claim.coverage_type}")
                    print(f"      - Estado: {claim.status}")
                    print(f"      - Creado: {claim.created_at}")
            
            # Verificar datos en DOCUMENTS
            print("\n📄 Datos en tabla DOCUMENTS:")
            result = conn.execute(text("SELECT * FROM \"DOCUMENTS\" ORDER BY uploaded_at DESC"))
            documents = result.fetchall()
            
            if not documents:
                print("   📭 No hay registros en DOCUMENTS")
            else:
                print(f"   📊 Total de documentos: {len(documents)}")
                for i, doc in enumerate(documents, 1):
                    print(f"\n   📎 Documento {i}:")
                    print(f"      - ID: {doc.id}")
                    print(f"      - Claim Form ID: {doc.claim_form_id}")
                    print(f"      - Nombre original: {doc.original_filename}")
                    print(f"      - Nombre en storage: {doc.filename}")
                    print(f"      - Tipo: {doc.document_type}")
                    print(f"      - Tamaño: {doc.file_size} bytes")
                    print(f"      - Ruta: {doc.storage_path}")
                    print(f"      - Subido: {doc.uploaded_at}")
            
            # Verificar relaciones
            if claims and documents:
                print("\n🔗 Verificando relaciones:")
                for claim in claims:
                    claim_docs = [doc for doc in documents if doc.claim_form_id == claim.id]
                    print(f"   - Reclamo {claim.claim_id}: {len(claim_docs)} documentos")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando datos: {e}")
        return False

if __name__ == "__main__":
    print("📊 VERIFICANDO DATOS EN LA BASE DE DATOS")
    print("=" * 50)
    
    success = check_database_data()
    
    if success:
        print("\n✅ Verificación completada")
    else:
        print("\n❌ Error en la verificación")
        sys.exit(1) 