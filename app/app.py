# Archivo principal de la aplicación Reflex.

import reflex as rx
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Importar las páginas
from app.pages.index_page import index_page
from app.pages.login_page import login_page
from app.pages.dashboard_page import dashboard_page

# Importar el webhook de la API
from app.web.api.email_webhook import email_webhook

# Importar funciones de base de datos
from app.core.database import test_connection, create_tables
from app.core.init_db import init_db

# Crear la aplicación Reflex
app = rx.App()

# Añadir las páginas a la aplicación
app.add_page(index_page)
app.add_page(login_page)
app.add_page(dashboard_page)

# Añadir la ruta de la API para el webhook de email
app.add_api_route("/api/email-webhook", email_webhook, methods=["POST"])

# Configuración adicional de la aplicación
app.title = "Agentic AI"
app.description = "Tu asistente inteligente para análisis y comunicación"

# Configurar el estado inicial
@app.on_load()
async def on_load():
    """Función que se ejecuta al cargar la aplicación."""
    print("🚀 Aplicación Agentic AI iniciada")
    
    # Verificar variables de entorno críticas
    required_env_vars = [
        "DATABASE_URL",
        "GEMINI_API_KEY", 
        "SENDGRID_API_KEY"
    ]
    
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    if missing_vars:
        print(f"⚠️  Variables de entorno faltantes: {', '.join(missing_vars)}")
        print("Algunas funcionalidades pueden no estar disponibles.")
    else:
        print("✅ Todas las variables de entorno críticas están configuradas.")
    
    # Verificar conexión a la base de datos
    print("🔍 Verificando conexión a la base de datos...")
    if test_connection():
        print("✅ Conexión a la base de datos exitosa")
        
        # Crear tablas si no existen (solo en desarrollo)
        if os.getenv("ENVIRONMENT", "development") == "development":
            try:
                create_tables()
                print("✅ Tablas de base de datos verificadas")
            except Exception as e:
                print(f"⚠️  Error creando tablas: {e}")
    else:
        print("❌ Error: No se pudo conectar a la base de datos")
        print("💡 Asegúrate de que la base de datos esté configurada correctamente")

if __name__ == "__main__":
    app.run() 