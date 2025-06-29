#!/usr/bin/env python3
"""
Script para configurar las variables de entorno del proyecto.
"""

import os
from pathlib import Path

def create_env_file():
    """Crea el archivo .env con las variables necesarias."""
    
    env_content = """# PostgreSQL Database
DATABASE_URL=postgresql://user:password@host:port/dbname

# External Services
GEMINI_API_KEY=your_gemini_api_key_here
RESEND_API_KEY=your_resend_api_key_here

# Email Testing (Optional - for email validation script)
GMAIL_APP_PASSWORD=your_gmail_app_password_here

# Cloudflare R2
R2_ACCOUNT_ID=your_r2_account_id_here
R2_ACCESS_KEY_ID=your_r2_access_key_id_here
R2_SECRET_ACCESS_KEY=your_r2_secret_access_key_here
R2_BUCKET_NAME=your_bucket_name_here
R2_PUBLIC_URL=https://your-public-url.r2.dev

# App Configuration
APP_SECRET_KEY=your_secret_key_here
ENVIRONMENT=development

# Email Configuration
FROM_EMAIL=gerardo_mayel_fernandez_alamilla@chiefdataaiofficer.com

# ngrok Configuration (for local development)
NGROK_AUTHTOKEN=your_ngrok_authtoken_here

# Domain Configuration
DOMAIN_NAME=chiefdataaiofficer.com
WEBHOOK_EMAIL=test@chiefdataaiofficer.com
"""
    
    env_file = Path('.env')
    
    if env_file.exists():
        print("⚠️  El archivo .env ya existe.")
        response = input("¿Quieres sobrescribirlo? (y/N): ")
        if response.lower() != 'y':
            print("❌ Operación cancelada.")
            return False
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ Archivo .env creado exitosamente.")
        return True
    except Exception as e:
        print(f"❌ Error creando archivo .env: {e}")
        return False

def configure_ngrok():
    """Configura ngrok con el token del archivo .env."""
    
    # Cargar variables de entorno
    from dotenv import load_dotenv
    load_dotenv()
    
    ngrok_token = os.getenv('NGROK_AUTHTOKEN')
    
    if not ngrok_token or ngrok_token == 'your_ngrok_authtoken_here':
        print("\n⚠️  NGROK_AUTHTOKEN no está configurado en .env")
        print("📋 Para configurar ngrok:")
        print("1. Ve a https://dashboard.ngrok.com/get-started/your-authtoken")
        print("2. Copia tu authtoken")
        print("3. Edita el archivo .env y reemplaza 'your_ngrok_authtoken_here' con tu token")
        print("4. Ejecuta este script nuevamente")
        return False
    
    try:
        import subprocess
        result = subprocess.run([
            'ngrok', 'config', 'add-authtoken', ngrok_token
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ ngrok configurado exitosamente con el token del .env")
            return True
        else:
            print(f"❌ Error configurando ngrok: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error configurando ngrok: {e}")
        return False

def check_env_variables():
    """Verifica que las variables de entorno estén configuradas."""
    
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = [
        'RESEND_API_KEY',
        'GEMINI_API_KEY',
        'NGROK_AUTHTOKEN'
    ]
    
    optional_vars = [
        'DATABASE_URL',
        'R2_ACCOUNT_ID',
        'R2_ACCESS_KEY_ID',
        'R2_SECRET_ACCESS_KEY',
        'R2_BUCKET_NAME',
        'R2_PUBLIC_URL'
    ]
    
    print("\n🔍 Verificando variables de entorno:")
    print("="*50)
    
    # Verificar variables requeridas
    print("\n📋 Variables Requeridas:")
    missing_required = []
    for var in required_vars:
        value = os.getenv(var)
        if value and value != f'your_{var.lower()}_here':
            print(f"✅ {var}: Configurada")
        else:
            print(f"❌ {var}: No configurada")
            missing_required.append(var)
    
    # Verificar variables opcionales
    print("\n📋 Variables Opcionales:")
    for var in optional_vars:
        value = os.getenv(var)
        if value and value != f'your_{var.lower()}_here':
            print(f"✅ {var}: Configurada")
        else:
            print(f"⚠️  {var}: No configurada (opcional)")
    
    if missing_required:
        print(f"\n❌ Faltan {len(missing_required)} variables requeridas:")
        for var in missing_required:
            print(f"   - {var}")
        return False
    
    print("\n✅ Todas las variables requeridas están configuradas.")
    return True

def main():
    """Función principal."""
    print("="*60)
    print("🔧 CONFIGURADOR DE VARIABLES DE ENTORNO")
    print("="*60)
    
    # Crear archivo .env si no existe
    if not Path('.env').exists():
        print("\n📝 Creando archivo .env...")
        if not create_env_file():
            return
    
    # Configurar ngrok
    print("\n🚀 Configurando ngrok...")
    configure_ngrok()
    
    # Verificar variables
    print("\n🔍 Verificando configuración...")
    check_env_variables()
    
    print("\n" + "="*60)
    print("📋 PRÓXIMOS PASOS:")
    print("="*60)
    print("1. Edita el archivo .env con tus credenciales reales")
    print("2. Ejecuta: python start_local_webhook.py")
    print("3. Configura el webhook en Resend con la URL de ngrok")
    print("4. Envía un email real para probar")
    print("="*60)

if __name__ == "__main__":
    main() 