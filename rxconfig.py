# rxconfig.py - Configuración para frontend estático desconectado
import reflex as rx
import os

# Configuración para modo estático desconectado
STATIC_MODE = os.getenv("STATIC_MODE", "false").lower() == "true"

if STATIC_MODE:
    # Modo estático: no requiere base de datos ni API
    config = rx.Config(
        app_name="app",
        db_url=None,  # Sin base de datos
        api_url="http://localhost:8000",  # URL dummy para validación
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
else:
    # Modo normal con backend
    API_URL = os.getenv("REFLEX_API_URL", "http://localhost:8000")
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    if not DATABASE_URL and not os.getenv("FRONTEND_ONLY"):
        raise ValueError("La variable de entorno DATABASE_URL no está configurada.")

    # Handle Render PostgreSQL URL format
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    config = rx.Config(
        app_name="app",
        db_url=DATABASE_URL if DATABASE_URL else None,
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