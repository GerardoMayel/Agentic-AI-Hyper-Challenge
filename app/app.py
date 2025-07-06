"""
Main Reflex application file for the Claims Management System.
Static frontend mode without backend dependencies.
"""

import reflex as rx

# Import pages
from app.pages.index_page import index_page
from app.pages.login_page import login_page
from app.pages.dashboard_page import dashboard_page
from app.pages.claim_form_page import claim_form_page

# Create Reflex app
app = rx.App()

# Add pages to the application
app.add_page(index_page, route="/")
app.add_page(login_page, route="/login")
app.add_page(dashboard_page, route="/dashboard")
app.add_page(claim_form_page, route="/claim-form")

print("🚀 Claims Management System - Frontend Ready for Export") 