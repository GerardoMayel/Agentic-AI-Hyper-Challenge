#!/usr/bin/env python3
"""
Script de Configuración de Variables de Entorno
Para las pruebas de email de chiefdataaiofficer.com
"""

import os
import getpass
from pathlib import Path

def setup_env_file():
    """Configura el archivo .env con las variables necesarias."""
    print("🔧 Configuración de Variables de Entorno")
    print("=" * 50)
    
    # Verificar si ya existe el archivo .env
    env_file = Path(".env")
    if env_file.exists():
        print("📁 Archivo .env encontrado")
        overwrite = input("¿Deseas sobrescribir el archivo existente? (y/N): ").lower()
        if overwrite != 'y':
            print("❌ Configuración cancelada")
            return False
    else:
        print("📁 Creando nuevo archivo .env")
    
    print("\n📝 Configurando variables de entorno...")
    print("(Presiona Enter para usar valores por defecto)")
    
    # Preguntar qué servicio de email usar
    print("\n📧 Servicio de Email:")
    print("   1. SendGrid")
    print("   2. Resend")
    email_service = input("   Selecciona el servicio (1-2): ").strip()
    
    sendgrid_key = "your_sendgrid_api_key_here"
    resend_key = "your_resend_api_key_here"
    
    if email_service == "1":
        # Obtener SendGrid API Key
        print("\n🔑 SendGrid API Key:")
        print("   Obtén tu API key en: https://app.sendgrid.com/settings/api_keys")
        sendgrid_key = getpass.getpass("   Ingresa tu SendGrid API Key: ").strip()
        
        if not sendgrid_key:
            print("   ⚠️  Usando valor por defecto (deberás configurarlo manualmente)")
            sendgrid_key = "your_sendgrid_api_key_here"
    elif email_service == "2":
        # Obtener Resend API Key
        print("\n🔑 Resend API Key:")
        print("   Obtén tu API key en: https://resend.com/api-keys")
        resend_key = getpass.getpass("   Ingresa tu Resend API Key: ").strip()
        
        if not resend_key:
            print("   ⚠️  Usando valor por defecto (deberás configurarlo manualmente)")
            resend_key = "your_resend_api_key_here"
    else:
        print("   ⚠️  Opción no válida, usando valores por defecto")
    
    # Obtener Gmail App Password (opcional)
    print("\n📧 Gmail App Password (opcional):")
    print("   Para pruebas de recepción, configura una contraseña de aplicación")
    print("   Guía: https://support.google.com/accounts/answer/185833")
    gmail_password = getpass.getpass("   Ingresa tu Gmail App Password (opcional): ").strip()
    
    if not gmail_password:
        gmail_password = "your_gmail_app_password_here"
    
    # Crear contenido del archivo .env
    env_content = f"""# PostgreSQL Database
DATABASE_URL=postgresql://user:password@host:port/dbname

# External Services
GEMINI_API_KEY=your_gemini_api_key_here
SENDGRID_API_KEY={sendgrid_key}
RESEND_API_KEY={resend_key}

# Email Testing (Optional - for email validation script)
GMAIL_APP_PASSWORD={gmail_password}

# Cloudflare R2
R2_ACCOUNT_ID=your_r2_account_id_here
R2_ACCESS_KEY_ID=your_r2_access_key_id_here
R2_SECRET_ACCESS_KEY=your_r2_secret_access_key_here
R2_BUCKET_NAME=your_bucket_name_here
R2_PUBLIC_URL=https://your-public-url.r2.dev

# App Configuration
APP_SECRET_KEY=your_secret_key_here
ENVIRONMENT=development
"""
    
    # Escribir archivo .env
    try:
        with open(".env", "w") as f:
            f.write(env_content)
        
        print("\n✅ Archivo .env creado exitosamente!")
        
        # Verificar configuración
        print("\n🔍 Verificando configuración...")
        if email_service == "1" and sendgrid_key != "your_sendgrid_api_key_here":
            print("✅ SendGrid API Key configurada")
        elif email_service == "2" and resend_key != "your_resend_api_key_here":
            print("✅ Resend API Key configurada")
        else:
            print("⚠️  API Key necesita configuración manual")
        
        if gmail_password != "your_gmail_app_password_here":
            print("✅ Gmail App Password configurada")
        else:
            print("⚠️  Gmail App Password opcional (no configurada)")
        
        print("\n📋 Próximos pasos:")
        print("   1. Si usaste valores por defecto, edita manualmente el archivo .env")
        if email_service == "2":
            print("   2. Ejecuta: python quick_email_test_resend.py")
        else:
            print("   2. Ejecuta: python quick_email_test.py")
        print("   3. O ejecuta: python email_validation_script.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando archivo .env: {str(e)}")
        return False

def verify_env_config():
    """Verifica la configuración actual del archivo .env."""
    print("🔍 Verificando Configuración Actual")
    print("=" * 40)
    
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ Archivo .env no encontrado")
        return False
    
    # Cargar variables de entorno
    from dotenv import load_dotenv
    load_dotenv()
    
    sendgrid_key = os.getenv("SENDGRID_API_KEY")
    resend_key = os.getenv("RESEND_API_KEY")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")
    
    print(f"📁 Archivo .env: {'✅ Encontrado' if env_file.exists() else '❌ No encontrado'}")
    print(f"🔑 SendGrid API Key: {'✅ Configurada' if sendgrid_key and sendgrid_key != 'your_sendgrid_api_key_here' else '❌ No configurada'}")
    print(f"🔑 Resend API Key: {'✅ Configurada' if resend_key and resend_key != 'your_resend_api_key_here' else '❌ No configurada'}")
    print(f"📧 Gmail App Password: {'✅ Configurada' if gmail_password and gmail_password != 'your_gmail_app_password_here' else '⚠️  No configurada (opcional)'}")
    
    return True

def main():
    """Función principal."""
    print("🔧 Configurador de Variables de Entorno")
    print("=" * 50)
    
    # Verificar configuración actual
    verify_env_config()
    
    print("\n" + "=" * 50)
    
    # Preguntar si quiere configurar
    action = input("\n¿Qué deseas hacer?\n1. Configurar variables de entorno\n2. Solo verificar configuración\n3. Salir\n\nSelecciona (1-3): ").strip()
    
    if action == "1":
        setup_env_file()
    elif action == "2":
        print("\n✅ Verificación completada")
    elif action == "3":
        print("\n👋 ¡Hasta luego!")
    else:
        print("\n❌ Opción no válida")

if __name__ == "__main__":
    main() 