# rxconfig.py - VERSIÓN CORREGIDA FINAL
import reflex as rx
import os

# Detecta si la aplicación está corriendo en el entorno de Render.
# Render establece la variable de entorno 'RENDER' a 'true' automáticamente.
IS_PRODUCTION = os.getenv("RENDER") == "true"

# Define la configuración de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("La variable de entorno DATABASE_URL no está configurada.")

# Handle Render PostgreSQL URL format
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Configuración principal de la aplicación
config = rx.Config(
    app_name="app",
    db_url=DATABASE_URL,
    
    # --- CAMBIOS CLAVE AQUÍ ---
    # En producción, el frontend (servido por el backend) necesita saber
    # que la API está en la misma URL, no en localhost.
    # Reflex usa la variable RENDER_EXTERNAL_URL que definimos en render.yaml.
    api_url=os.getenv("RENDER_EXTERNAL_URL", "http://0.0.0.0:8000") if IS_PRODUCTION else "http://localhost:8000",

    cors_allowed_origins=["*"],
    loglevel="info",
    # Tailwind configuration
    tailwind={
        "theme": {
            "extend": {
                "colors": {
                    "zurich": {
                        "blue": "#0066CC",
                        "dark-blue": "#004499",
                        "light-blue": "#E6F3FF",
                        "gray": "#666666",
                        "light-gray": "#F5F5F5"
                    }
                }
            }
        }
    },
    plugins=[]
) 