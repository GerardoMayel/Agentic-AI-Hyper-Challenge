# rxconfig.py - Configuración para arquitectura de dos servicios
import reflex as rx
import os

# La URL de la API se inyecta durante la construcción en Render
# a través de la variable de entorno REFLEX_API_URL.
# Para el desarrollo local, se usa el valor por defecto.
API_URL = os.getenv("REFLEX_API_URL", "http://localhost:8000")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("La variable de entorno DATABASE_URL no está configurada.")

# Handle Render PostgreSQL URL format
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

config = rx.Config(
    app_name="app",
    db_url=DATABASE_URL,
    api_url=API_URL,
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