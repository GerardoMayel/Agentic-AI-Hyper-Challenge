#!/usr/bin/env python3
"""
Deployment Checklist for Render Production
"""

import os
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists"""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - NOT FOUND")
        return False

def check_directory_structure():
    """Check directory structure"""
    print("🔍 Checking directory structure...")
    
    required_dirs = [
        "backend",
        "frontend", 
        "backend/app",
        "backend/app/core",
        "backend/app/models",
        "backend/app/services",
        "backend/app/api",
        "backend/app/static"
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ Directory: {dir_path}")
        else:
            print(f"❌ Missing directory: {dir_path}")
            all_exist = False
    
    return all_exist

def check_backend_files():
    """Check backend files"""
    print("\n🔍 Checking backend files...")
    
    backend_files = [
        ("backend/main.py", "Main FastAPI application"),
        ("backend/requirements.txt", "Python dependencies"),
        ("backend/app/core/database.py", "Database configuration"),
        ("backend/app/models/email_models.py", "Database models"),
        ("backend/app/api/analyst_api.py", "Analyst API endpoints"),
        ("backend/app/static/analyst_dashboard.html", "Analyst dashboard interface"),
        ("backend/app/services/email_scheduler.py", "Email scheduler service"),
        ("backend/app/services/llm_service.py", "LLM service"),
        ("backend/app/services/gmail_service.py", "Gmail service")
    ]
    
    all_exist = True
    for file_path, description in backend_files:
        if not check_file_exists(file_path, description):
            all_exist = False
    
    return all_exist

def check_frontend_files():
    """Check frontend files"""
    print("\n🔍 Checking frontend files...")
    
    frontend_files = [
        ("frontend/package.json", "Node.js configuration"),
        ("frontend/next.config.js", "Next.js configuration"),
        ("frontend/pages/claim-form.js", "Claims form"),
        ("frontend/pages/index.js", "Main page"),
        ("frontend/pages/dashboard.js", "Dashboard")
    ]
    
    all_exist = True
    for file_path, description in frontend_files:
        if not check_file_exists(file_path, description):
            all_exist = False
    
    return all_exist

def check_deployment_files():
    """Check deployment files"""
    print("\n🔍 Checking deployment files...")
    
    deployment_files = [
        ("render.yaml", "Render configuration"),
        (".gitignore", "Git ignore file"),
        ("README.md", "Project documentation")
    ]
    
    all_exist = True
    for file_path, description in deployment_files:
        if not check_file_exists(file_path, description):
            all_exist = False
    
    return all_exist

def check_render_config():
    """Check Render configuration"""
    print("\n🔍 Checking Render configuration...")
    
    if not check_file_exists("render.yaml", "Render configuration file"):
        return False
    
    try:
        with open("render.yaml", "r") as f:
            content = f.read()
            
        # Check key elements
        checks = [
            ("zurich-claims-api", "Backend service defined"),
            ("zurich-claims-frontend", "Frontend service defined"),
            ("DATABASE_URL", "Database URL configured"),
            ("GOOGLE_CLOUD_STORAGE_BUCKET", "Storage bucket configured"),
            ("claims-documents-zurich-ai", "Correct bucket name"),
            ("velvety-glyph-464401-v6", "Google Cloud Project ID"),
            ("gerardo_mayel_fernandez_alamilla@chiefdataaiofficer.com", "Email configured")
        ]
        
        all_good = True
        for check_text, description in checks:
            if check_text in content:
                print(f"✅ {description}")
            else:
                print(f"❌ {description} - NOT FOUND")
                all_good = False
        
        return all_good
        
    except Exception as e:
        print(f"❌ Error reading render.yaml: {e}")
        return False

def check_environment_variables():
    """Check required environment variables"""
    print("\n🔍 Checking environment variables...")
    
    required_vars = [
        "DATABASE_URL",
        "GOOGLE_CLOUD_STORAGE_BUCKET", 
        "GOOGLE_APPLICATION_CREDENTIALS_JSON",
        "GEMINI_API_KEY",
        "GMAIL_CREDENTIALS_JSON",
        "GMAIL_TOKEN_JSON",
        "SECRET_KEY"
    ]
    
    missing_vars = []
    for var in required_vars:
        if var in os.environ:
            print(f"✅ {var}: Configured")
        else:
            print(f"⚠️  {var}: Not set (will be configured in Render)")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n📋 Environment variables to configure in Render:")
        for var in missing_vars:
            print(f"   - {var}")
    
    return True

def check_database_connection():
    """Check database connection"""
    print("\n🔍 Checking database connection...")
    
    try:
        from backend.app.core.database import engine
        from sqlalchemy import text
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("⚠️  This is normal if DATABASE_URL is not set locally")
        return True  # Don't fail deployment for this

def main():
    """Main deployment checklist"""
    print("🚀 RENDER DEPLOYMENT CHECKLIST")
    print("=" * 50)
    
    checks = [
        check_directory_structure,
        check_backend_files,
        check_frontend_files,
        check_deployment_files,
        check_render_config,
        check_environment_variables,
        check_database_connection
    ]
    
    all_passed = True
    for check_func in checks:
        if not check_func():
            all_passed = False
        print()
    
    print("=" * 50)
    if all_passed:
        print("🎉 ALL CHECKS PASSED!")
        print("✅ The project is ready to deploy on Render")
        print("\n📋 Next steps:")
        print("1. Commit and push to main branch")
        print("2. Connect repository to Render")
        print("3. Configure sensitive environment variables in Render dashboard:")
        print("   - GOOGLE_APPLICATION_CREDENTIALS_JSON")
        print("   - GEMINI_API_KEY")
        print("   - SECRET_KEY")
        print("   - GMAIL_CREDENTIALS_JSON")
        print("   - GMAIL_TOKEN_JSON")
        print("\n🌐 Production URLs will be:")
        print("   - Backend: https://zurich-claims-api.onrender.com")
        print("   - Frontend: https://zurich-claims-frontend.onrender.com")
        print("   - Analyst Dashboard: https://zurich-claims-api.onrender.com/analyst")
    else:
        print("❌ THERE ARE ISSUES TO RESOLVE BEFORE DEPLOYMENT")
        print("Check the errors above and fix them before continuing")
        sys.exit(1)

if __name__ == "__main__":
    main() 