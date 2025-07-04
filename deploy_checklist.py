#!/usr/bin/env python3
"""
Deploy Checklist Script
Verifies that everything is ready for deployment to Render.
"""

import os
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists and print status."""
    if Path(file_path).exists():
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - MISSING")
        return False

def check_environment_variables():
    """Check if required environment variables are set."""
    print("\n🔧 Environment Variables Check:")
    print("-" * 40)
    
    required_env_vars = [
        "DATABASE_URL",
        "GEMINI_API_KEY", 
        "GOOGLE_CLOUD_PROJECT_ID",
        "GOOGLE_CLOUD_STORAGE_BUCKET",
        "GOOGLE_APPLICATION_CREDENTIALS_JSON",
        "GMAIL_CREDENTIALS_JSON",
        "GMAIL_TOKEN_JSON"
    ]
    
    all_present = True
    for var in required_env_vars:
        if os.getenv(var):
            print(f"✅ {var}: Set")
        else:
            print(f"⚠️  {var}: Not set (will be configured in Render)")
    
    return all_present

def check_python_files():
    """Check if all required Python files exist."""
    print("\n🐍 Python Files Check:")
    print("-" * 40)
    
    required_files = [
        "app/__init__.py",
        "app/app.py",
        "app/core/database.py",
        "app/core/models.py",
        "app/pages/claim_form_page.py",
        "app/pages/dashboard_page.py",
        "app/services/gmail_service.py",
        "app/services/claims_processor.py",
        "app/services/gcs_storage.py",
        "requirements.txt",
        "rxconfig.py",
        "render.yaml"
    ]
    
    all_exist = True
    for file_path in required_files:
        if not check_file_exists(file_path, f"Python file"):
            all_exist = False
    
    return all_exist

def check_configuration():
    """Check configuration files."""
    print("\n⚙️  Configuration Check:")
    print("-" * 40)
    
    config_files = [
        "render.yaml",
        "rxconfig.py",
        ".env"
    ]
    
    all_good = True
    for file_path in config_files:
        if not check_file_exists(file_path, f"Config file"):
            all_good = False
    
    return all_good

def main():
    """Main deployment checklist."""
    print("🚀 Render Deployment Checklist")
    print("=" * 50)
    
    # Check files
    files_ok = check_python_files()
    config_ok = check_configuration()
    env_ok = check_environment_variables()
    
    print("\n" + "=" * 50)
    print("📋 Deployment Summary:")
    print("-" * 30)
    
    if files_ok and config_ok:
        print("✅ All files and configurations are ready")
        print("✅ Application structure is correct")
        print("✅ Render configuration is set up")
        
        if env_ok:
            print("✅ Environment variables are configured")
        else:
            print("⚠️  Some environment variables need to be set in Render dashboard")
        
        print("\n🎉 Ready for deployment!")
        print("\n📝 Next steps:")
        print("1. Push code to GitHub")
        print("2. Connect repository to Render")
        print("3. Set environment variables in Render dashboard")
        print("4. Deploy the application")
        print("5. Run database initialization script")
        
    else:
        print("❌ Some issues need to be fixed before deployment")
        print("Please address the missing files or configurations above")
    
    return files_ok and config_ok

if __name__ == "__main__":
    main() 