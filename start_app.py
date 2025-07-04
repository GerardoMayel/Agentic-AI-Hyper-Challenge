#!/usr/bin/env python3
"""
Script to start the Claims Management System Reflex application.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check critical variables
required_vars = [
    'DATABASE_URL',
    'GEMINI_API_KEY',
    'GOOGLE_CLOUD_PROJECT_ID',
    'GOOGLE_CLOUD_BUCKET_NAME',
    'GOOGLE_APPLICATION_CREDENTIALS_JSON',
    'GMAIL_CREDENTIALS_JSON',
    'GMAIL_TOKEN_JSON'
]

missing_vars = []
for var in required_vars:
    if not os.getenv(var):
        missing_vars.append(var)

if missing_vars:
    print("❌ Missing environment variables:")
    for var in missing_vars:
        print(f"   - {var}")
    print("\n💡 Make sure to configure all variables in the .env file")
    sys.exit(1)

print("✅ All environment variables are configured")
print("🚀 Starting Claims Management System...")
print("📱 Application will be available at: http://localhost:3000")
print("⏹️  Press Ctrl+C to stop the server")

# Import and run Reflex app
try:
    import reflex as rx
    from app.app import app
    
    # Run the application
    app.run()
    
except ImportError as e:
    print(f"❌ Error importing Reflex: {e}")
    print("💡 Make sure to install all dependencies:")
    print("   pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error running application: {e}")
    sys.exit(1) 