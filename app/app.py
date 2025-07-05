"""
Main Reflex application file for the Claims Management System.
Basic web interface without email processing for now.
"""

import reflex as rx
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import pages
from app.pages.index_page import index_page
from app.pages.login_page import login_page
from app.pages.dashboard_page import dashboard_page
from app.pages.claim_form_page import claim_form_page

# Import database functions
from app.core.database import test_connection, create_tables

# Create Reflex app
app = rx.App()

# Add pages to the application
app.add_page(index_page, route="/")
app.add_page(login_page, route="/login")
app.add_page(dashboard_page, route="/dashboard")
app.add_page(claim_form_page, route="/claim-form")

def initialize_app():
    """Initialize the application."""
    print("🚀 Claims Management System started")
    
    # Test database connection
    print("🔍 Testing database connection...")
    if test_connection():
        print("✅ Database connection successful")
        
        # Create tables if they don't exist (development only)
        if os.getenv("ENVIRONMENT", "development") == "development":
            try:
                create_tables()
                print("✅ Database tables verified")
            except Exception as e:
                print(f"⚠️  Error creating tables: {e}")
    else:
        print("❌ Error: Could not connect to database")
        print("💡 Make sure the database is configured correctly")

# Initialize the application
initialize_app() 