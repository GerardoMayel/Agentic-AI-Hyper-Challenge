import reflex as rx

# Configuración de la aplicación Reflex
config = rx.Config(
    app_name="app",
    db_url="sqlite:///claims_management.db",  # Base de datos local para desarrollo
    env=rx.Env.DEV,
    frontend_port=3000,
    backend_port=8000,
    api_url="http://localhost:8000",
    deploy_url="https://your-app.onrender.com",  # URL de producción
    tailwind=None  # Disable tailwind to avoid deprecation warnings
) 