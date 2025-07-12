#!/usr/bin/env python3
"""
Script para verificar que todo esté listo para el despliegue en Render
"""

import os
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """Verifica que un archivo existe"""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - NO ENCONTRADO")
        return False

def check_directory_structure():
    """Verifica la estructura de directorios"""
    print("🔍 Verificando estructura de directorios...")
    
    required_dirs = [
        "backend",
        "frontend", 
        "backend/app",
        "backend/app/core",
        "backend/app/models",
        "backend/app/services"
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ Directorio: {dir_path}")
        else:
            print(f"❌ Directorio faltante: {dir_path}")
            all_exist = False
    
    return all_exist

def check_backend_files():
    """Verifica archivos del backend"""
    print("\n🔍 Verificando archivos del backend...")
    
    backend_files = [
        ("backend/main.py", "Archivo principal del backend"),
        ("backend/requirements.txt", "Dependencias de Python"),
        ("backend/app/core/database.py", "Configuración de base de datos"),
        ("backend/app/models/claim_models.py", "Modelos de datos"),
        ("backend/app/models/schemas.py", "Esquemas Pydantic"),
        ("backend/app/services/storage_service.py", "Servicio de almacenamiento")
    ]
    
    all_exist = True
    for file_path, description in backend_files:
        if not check_file_exists(file_path, description):
            all_exist = False
    
    return all_exist

def check_frontend_files():
    """Verifica archivos del frontend"""
    print("\n🔍 Verificando archivos del frontend...")
    
    frontend_files = [
        ("frontend/package.json", "Configuración de Node.js"),
        ("frontend/next.config.js", "Configuración de Next.js"),
        ("frontend/pages/claim-form.js", "Formulario de siniestros"),
        ("frontend/pages/index.js", "Página principal"),
        ("frontend/pages/dashboard.js", "Dashboard")
    ]
    
    all_exist = True
    for file_path, description in frontend_files:
        if not check_file_exists(file_path, description):
            all_exist = False
    
    return all_exist

def check_deployment_files():
    """Verifica archivos de despliegue"""
    print("\n🔍 Verificando archivos de despliegue...")
    
    deployment_files = [
        ("render.yaml", "Configuración de Render"),
        (".gitignore", "Archivo .gitignore"),
        ("README.md", "Documentación del proyecto")
    ]
    
    all_exist = True
    for file_path, description in deployment_files:
        if not check_file_exists(file_path, description):
            all_exist = False
    
    return all_exist

def check_render_config():
    """Verifica la configuración de Render"""
    print("\n🔍 Verificando configuración de Render...")
    
    if not check_file_exists("render.yaml", "Archivo render.yaml"):
        return False
    
    try:
        with open("render.yaml", "r") as f:
            content = f.read()
            
        # Verificar elementos clave
        checks = [
            ("zurich-claims-api", "Servicio backend definido"),
            ("zurich-claims-frontend", "Servicio frontend definido"),
            ("DATABASE_URL", "URL de base de datos configurada"),
            ("GOOGLE_CLOUD_STORAGE_BUCKET", "Bucket de storage configurado"),
            ("claims-documents-zurich-ai", "Nombre del bucket correcto"),
            ("velvety-glyph-464401-v6", "Project ID de Google Cloud"),
            ("gerardo_mayel_fernandez_alamilla@chiefdataaiofficer.com", "Email configurado")
        ]
        
        all_good = True
        for check_text, description in checks:
            if check_text in content:
                print(f"✅ {description}")
            else:
                print(f"❌ {description} - NO ENCONTRADO")
                all_good = False
        
        return all_good
        
    except Exception as e:
        print(f"❌ Error leyendo render.yaml: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 VERIFICACIÓN DE DESPLIEGUE EN RENDER")
    print("=" * 50)
    
    checks = [
        check_directory_structure,
        check_backend_files,
        check_frontend_files,
        check_deployment_files,
        check_render_config
    ]
    
    all_passed = True
    for check_func in checks:
        if not check_func():
            all_passed = False
        print()
    
    print("=" * 50)
    if all_passed:
        print("🎉 ¡TODAS LAS VERIFICACIONES PASARON!")
        print("✅ El proyecto está listo para desplegar en Render")
        print("\n📋 Próximos pasos:")
        print("1. Commit y push a la rama main")
        print("2. Conectar el repositorio a Render")
        print("3. Configurar las variables de entorno sensibles en Render:")
        print("   - GOOGLE_APPLICATION_CREDENTIALS_JSON")
        print("   - GEMINI_API_KEY")
        print("   - SECRET_KEY")
        print("   - GMAIL_CREDENTIALS_JSON")
        print("   - GMAIL_TOKEN_JSON")
        print("   - RESEND_API_KEY")
        print("   - RESEND_WEBHOOK_SECRET")
    else:
        print("❌ HAY PROBLEMAS QUE RESOLVER ANTES DEL DESPLIEGUE")
        print("Revisa los errores arriba y corrígelos antes de continuar")
        sys.exit(1)

if __name__ == "__main__":
    main() 