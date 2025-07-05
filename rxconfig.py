import reflex as rx
import os

# Handle Render PostgreSQL URL format
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///claims_management.db")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Configure the app
config = rx.Config(
    app_name="app",
    db_url=DATABASE_URL,
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