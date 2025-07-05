import reflex as rx
import os

# Get environment variables
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
# Check if we're in production environment
IS_PRODUCTION = os.getenv("ENVIRONMENT") == "production" or os.getenv("RENDER") == "true"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///claims_management.db")

# Handle Render PostgreSQL URL format
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Configure the app
config = rx.Config(
    app_name="app",
    db_url=DATABASE_URL,
    env=rx.Env.DEV if not IS_PRODUCTION else rx.Env.PROD,
    frontend_port=3000,
    backend_port=8000,
    backend_host="0.0.0.0",  # Important for Render
    api_url="http://localhost:8000" if not IS_PRODUCTION else os.getenv("REFLEX_API_URL", "https://claims-management-system-j7jz.onrender.com"),
    deploy_url="https://claims-management-system-j7jz.onrender.com" if IS_PRODUCTION else None,
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
    # Add Tailwind plugin explicitly
    plugins=[]
) 