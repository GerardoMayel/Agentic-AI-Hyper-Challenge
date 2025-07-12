#!/usr/bin/env python3
"""
Script para crear la tabla DOCUMENTS_OCR en la base de datos.
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Agregar el directorio backend al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.core.database import DATABASE_URL
from app.core.models import Base, DocumentOCR

load_dotenv()

def create_ocr_table():
    """Crea la tabla DOCUMENTS_OCR en la base de datos."""
    try:
        print("🔧 Creando tabla DOCUMENTS_OCR...")
        
        # Crear engine
        engine = create_engine(DATABASE_URL)
        
        # Crear la tabla
        DocumentOCR.__table__.create(engine, checkfirst=True)
        
        print("✅ Tabla DOCUMENTS_OCR creada exitosamente")
        
        # Verificar que la tabla existe
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_name = 'documents_ocr'
            """))
            
            if result.fetchone():
                print("✅ Verificación: Tabla DOCUMENTS_OCR existe en la base de datos")
                
                # Mostrar estructura de la tabla
                result = conn.execute(text("""
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns 
                    WHERE table_name = 'documents_ocr'
                    ORDER BY ordinal_position
                """))
                
                print("\n📋 Estructura de la tabla DOCUMENTS_OCR:")
                print("-" * 50)
                for row in result:
                    nullable = "NULL" if row.is_nullable == "YES" else "NOT NULL"
                    print(f"{row.column_name:<25} {row.data_type:<15} {nullable}")
                
            else:
                print("❌ Error: La tabla no se creó correctamente")
                
    except Exception as e:
        print(f"❌ Error creando tabla: {e}")
        return False
    
    return True

def test_ocr_table():
    """Prueba la tabla DOCUMENTS_OCR con datos de ejemplo."""
    try:
        print("\n🧪 Probando tabla DOCUMENTS_OCR...")
        
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Crear un registro de prueba
        test_ocr = DocumentOCR(
            document_id=1,  # Asumiendo que existe un documento con ID 1
            processing_status='completed',
            raw_text='Texto de prueba extraído por OCR',
            structured_data={'test': 'data'},
            confidence_score=0.95,
            gemini_model_used='gemini-1.5-flash',
            processing_time_seconds=2.5
        )
        
        db.add(test_ocr)
        db.commit()
        
        print("✅ Registro de prueba creado exitosamente")
        
        # Verificar el registro
        result = db.query(DocumentOCR).filter(DocumentOCR.document_id == 1).first()
        if result:
            print(f"✅ Registro encontrado: ID={result.id}, Status={result.processing_status}")
        else:
            print("❌ No se encontró el registro de prueba")
        
        # Limpiar registro de prueba
        db.delete(test_ocr)
        db.commit()
        print("✅ Registro de prueba eliminado")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Error en prueba: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando creación de tabla DOCUMENTS_OCR")
    print("=" * 50)
    
    if create_ocr_table():
        test_ocr_table()
        print("\n🎉 Proceso completado exitosamente")
    else:
        print("\n💥 Proceso falló")
        sys.exit(1) 