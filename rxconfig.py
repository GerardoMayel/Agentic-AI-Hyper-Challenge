import reflex as rx
import os

# Configuración simple y directa para Render
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("La variable de entorno DATABASE_URL no está configurada.")

# Handle Render PostgreSQL URL format
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Configuración mínima para funcionar en Render
config = rx.Config(
    app_name="app",
    db_url=DATABASE_URL,
    env=rx.Env.PROD,
    backend_host="0.0.0.0",
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