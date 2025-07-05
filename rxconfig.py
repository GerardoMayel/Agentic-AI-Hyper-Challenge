import reflex as rx
import os

# Se obtiene la URL de la base de datos directamente de las variables de entorno.
# En Render, esta variable es inyectada automáticamente por el archivo render.yaml.
# Esto elimina la dependencia de un archivo SQLite local.
DATABASE_URL = os.getenv("DATABASE_URL")

# Verificación para asegurar que la app no inicie sin una base de datos en producción.
if not DATABASE_URL:
    raise ValueError("La variable de entorno DATABASE_URL no está configurada.")

# Handle Render PostgreSQL URL format
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

config = rx.Config(
    app_name="app",
    db_url=DATABASE_URL,
    
    # Se eliminan las configuraciones de puerto y API URL condicionales.
    # Reflex en modo de producción ahora manejará esto de forma inteligente.
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