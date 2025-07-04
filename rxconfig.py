import reflex as rx
import os

# Get environment variables
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///claims_management.db")

# Handle Render PostgreSQL URL format
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Configure the app
config = rx.Config(
    app_name="app",
    db_url=DATABASE_URL,
    env=rx.Env.DEV if ENVIRONMENT == "development" else rx.Env.PROD,
    frontend_port=3000,
    backend_port=8000,
    backend_host="0.0.0.0",  # Important for Render
    api_url="http://localhost:8000" if ENVIRONMENT == "development" else None,
    deploy_url="https://claims-management-system.onrender.com" if ENVIRONMENT == "production" else None,
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
    }
) 