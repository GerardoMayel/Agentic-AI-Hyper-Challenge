#!/usr/bin/env python3
"""
Script de Configuración para Gmail API
Ayuda a configurar las credenciales necesarias para acceder a Gmail
"""

import os
import json
from pathlib import Path

def setup_gmail_credentials():
    """Configura las credenciales de Gmail API."""
    print("🔧 Configuración de Gmail API")
    print("=" * 50)
    
    print("📋 Pasos para configurar Gmail API:")
    print("\n1. Ve a Google Cloud Console:")
    print("   https://console.cloud.google.com/")
    
    print("\n2. Crea un nuevo proyecto o selecciona uno existente")
    
    print("\n3. Habilita la Gmail API:")
    print("   - Ve a 'APIs & Services' > 'Library'")
    print("   - Busca 'Gmail API' y habilítala")
    
    print("\n4. Crea credenciales:")
    print("   - Ve a 'APIs & Services' > 'Credentials'")
    print("   - Haz clic en 'Create Credentials' > 'OAuth 2.0 Client IDs'")
    print("   - Selecciona 'Desktop application'")
    print("   - Descarga el archivo JSON")
    
    print("\n5. Renombra el archivo descargado a 'credentials.json'")
    print("   y colócalo en el directorio raíz del proyecto")
    
    # Verificar si existe el archivo de credenciales
    credentials_file = Path("credentials.json")
    if credentials_file.exists():
        print(f"\n✅ Archivo credentials.json encontrado")
        
        # Verificar contenido básico
        try:
            with open(credentials_file, 'r') as f:
                creds_data = json.load(f)
            
            if 'installed' in creds_data or 'web' in creds_data:
                print("✅ Formato de credenciales válido")
                return True
            else:
                print("❌ Formato de credenciales inválido")
                return False
                
        except json.JSONDecodeError:
            print("❌ Error leyendo archivo de credenciales")
            return False
    else:
        print(f"\n❌ Archivo credentials.json no encontrado")
        print("   Sigue los pasos anteriores para crear las credenciales")
        return False

def create_sample_credentials():
    """Crea un archivo de ejemplo de credenciales."""
    sample_creds = {
        "installed": {
            "client_id": "your-client-id.apps.googleusercontent.com",
            "project_id": "your-project-id",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": "your-client-secret",
            "redirect_uris": ["http://localhost"]
        }
    }
    
    with open("credentials.example.json", "w") as f:
        json.dump(sample_creds, f, indent=2)
    
    print("📄 Archivo credentials.example.json creado")
    print("   Usa este archivo como referencia para crear tus credenciales")

def main():
    """Función principal."""
    print("🔧 Configurador de Gmail API")
    print("=" * 50)
    
    # Verificar configuración actual
    if setup_gmail_credentials():
        print("\n✅ Gmail API configurada correctamente")
        print("\n📋 Próximos pasos:")
        print("   1. Ejecuta: python email_processor.py")
        print("   2. Se abrirá una ventana del navegador para autorizar")
        print("   3. Autoriza el acceso a tu cuenta de Gmail")
    else:
        print("\n❌ Configuración incompleta")
        print("\n💡 Opciones:")
        print("   1. Crear archivo de ejemplo: python setup_gmail_api.py --example")
        print("   2. Seguir los pasos manuales mostrados arriba")
        
        # Crear archivo de ejemplo si se solicita
        if len(sys.argv) > 1 and sys.argv[1] == "--example":
            create_sample_credentials()

if __name__ == "__main__":
    import sys
    main() 