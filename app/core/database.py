import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy.sql import text

# Cargar variables de entorno
load_dotenv()

# Obtener la URL de la base de datos desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./agentic_ai.db")

# Crear el motor de la base de datos
engine = create_engine(
    DATABASE_URL,
    # Configuraciones adicionales para PostgreSQL
    pool_pre_ping=True,  # Verificar conexiones antes de usarlas
    pool_recycle=300,    # Reciclar conexiones cada 5 minutos
    echo=False,          # Cambiar a True para ver las consultas SQL en desarrollo
)

# Crear la clase SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear la clase Base para los modelos
Base = declarative_base()

def get_db():
    """
    Función que proporciona una sesión de base de datos.
    Usa yield para asegurar que la sesión se cierre correctamente.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """
    Crea todas las tablas definidas en los modelos.
    Útil para desarrollo y testing.
    """
    Base.metadata.create_all(bind=engine)

def drop_tables():
    """
    Elimina todas las tablas.
    ¡CUIDADO! Solo usar en desarrollo/testing.
    """
    Base.metadata.drop_all(bind=engine)

# Función para verificar la conexión a la base de datos
def test_connection():
    """Test database connection."""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            result.fetchone()
            print("✅ Database connection successful")
            return True
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        return False 