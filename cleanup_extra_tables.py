#!/usr/bin/env python3
"""
Script para limpiar las tablas extra que se crearon innecesariamente.
Solo mantenemos CLAIM_FORM, DOCUMENTS y creamos DOCUMENTS_OCR.
"""

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Agregar el directorio backend al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.core.database import DATABASE_URL

load_dotenv()

def cleanup_extra_tables():
    """Elimina las tablas extra y mantiene solo las necesarias."""
    try:
        print("🧹 Limpiando tablas extra...")
        
        # Crear engine
        engine = create_engine(DATABASE_URL)
        
        # Tablas que queremos mantener
        tables_to_keep = ['CLAIM_FORM', 'DOCUMENTS']
        
        # Tablas que queremos eliminar
        tables_to_drop = [
            'claims',
            'claim_documents', 
            'claim_form_submissions',
            'claim_expenses',
            'coverages'
        ]
        
        with engine.connect() as conn:
            # Verificar qué tablas existen
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            
            existing_tables = [row[0] for row in result]
            
            print(f"📋 Tablas existentes: {existing_tables}")
            
            # Eliminar tablas extra
            for table in tables_to_drop:
                if table in existing_tables:
                    print(f"🗑️ Eliminando tabla: {table}")
                    conn.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
                    conn.commit()
                    print(f"  ✅ {table} eliminada")
                else:
                    print(f"  ℹ️ {table} no existe, saltando")
            
            print(f"\n✅ Limpieza completada")
            print(f"📋 Tablas que se mantienen: {tables_to_keep}")
            
    except Exception as e:
        print(f"❌ Error en limpieza: {e}")

def create_documents_ocr_table():
    """Crea solo la tabla DOCUMENTS_OCR que necesitamos."""
    try:
        print("\n🔧 Creando tabla DOCUMENTS_OCR...")
        
        engine = create_engine(DATABASE_URL)
        
        # Crear la tabla DOCUMENTS_OCR con foreign key a DOCUMENTS
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS documents_ocr (
            id SERIAL PRIMARY KEY,
            document_id INTEGER NOT NULL,
            processed_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
            processing_status VARCHAR(50) DEFAULT 'pending',
            error_message TEXT,
            raw_text TEXT,
            structured_data JSON,
            confidence_score NUMERIC(5, 4),
            gemini_model_used VARCHAR(100),
            processing_time_seconds NUMERIC(10, 3),
            created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
            FOREIGN KEY(document_id) REFERENCES DOCUMENTS(id) ON DELETE CASCADE
        );
        """
        
        with engine.connect() as conn:
            conn.execute(text(create_table_sql))
            conn.commit()
            
        print("✅ Tabla DOCUMENTS_OCR creada exitosamente")
        
        # Verificar que se creó
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_name = 'documents_ocr'
            """))
            
            if result.fetchone():
                print("✅ Verificación: Tabla DOCUMENTS_OCR existe")
                
                # Mostrar estructura
                result = conn.execute(text("""
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns 
                    WHERE table_name = 'documents_ocr'
                    ORDER BY ordinal_position
                """))
                
                print("\n📋 Estructura de DOCUMENTS_OCR:")
                print("-" * 50)
                for row in result:
                    nullable = "NULL" if row.is_nullable == "YES" else "NOT NULL"
                    print(f"{row.column_name:<25} {row.data_type:<15} {nullable}")
            else:
                print("❌ Error: La tabla no se creó correctamente")
                
    except Exception as e:
        print(f"❌ Error creando tabla: {e}")

if __name__ == "__main__":
    print("🚀 Limpiando y creando solo las tablas necesarias")
    print("=" * 60)
    
    cleanup_extra_tables()
    create_documents_ocr_table()
    
    print("\n🎉 Proceso completado") 