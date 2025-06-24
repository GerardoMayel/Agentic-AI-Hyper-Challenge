import reflex as rx

# Configuración de la aplicación Reflex
config = rx.Config(
    app_name="agentic_ai",
    db_url="sqlite:///agentic_ai.db",  # Base de datos local para desarrollo
    env=rx.Env.DEV,
    frontend_port=3000,
    backend_port=8000,
    api_url="http://localhost:8000",
    deploy_url="https://your-app.onrender.com",  # URL de producción
    tailwind={
        "theme": {
            "extend": {
                "colors": {
                    "primary": {
                        "50": "#eff6ff",
                        "100": "#dbeafe",
                        "200": "#bfdbfe",
                        "300": "#93c5fd",
                        "400": "#60a5fa",
                        "500": "#3b82f6",
                        "600": "#2563eb",
                        "700": "#1d4ed8",
                        "800": "#1e40af",
                        "900": "#1e3a8a",
                    }
                }
            }
        }
    }
) 