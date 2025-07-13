#!/usr/bin/env python3
"""
Script simplificado para generar token de Gmail usando las credenciales del .env
"""

import os
import json
import tempfile
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

# Scopes necesarios para Gmail
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/userinfo.email',
    'openid'
]

def main():
    print("🔑 Generador de token OAuth para Gmail API")
    
    # Obtener credenciales del .env
    gmail_creds_json = os.getenv('GMAIL_CREDENTIALS_JSON')
    if not gmail_creds_json:
        print("❌ No se encontró GMAIL_CREDENTIALS_JSON en el .env")
        return
    
    try:
        creds_data = json.loads(gmail_creds_json)
    except json.JSONDecodeError:
        print("❌ Error al parsear GMAIL_CREDENTIALS_JSON")
        return
    
    # Detectar tipo de credenciales
    if 'installed' in creds_data:
        client_config = creds_data['installed']
    elif 'web' in creds_data:
        client_config = creds_data['web']
    else:
        print("❌ Formato de credenciales no válido")
        return
    
    print(f"✅ Credenciales detectadas: {list(creds_data.keys())[0]}")
    
    # Crear archivo temporal con formato compatible
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
        json.dump({"installed": client_config}, temp_file)
        temp_path = temp_file.name
    
    try:
        print("🌐 Iniciando flujo OAuth...")
        print("Se abrirá una ventana del navegador para autorizar el acceso.")
        print("Acepta todos los permisos solicitados.")
        
        # Flujo OAuth
        flow = InstalledAppFlow.from_client_secrets_file(temp_path, SCOPES)
        creds = flow.run_local_server(
            port=8080, 
            prompt='consent',
            authorization_prompt_message='Autoriza el acceso a Gmail para el procesamiento de emails'
        )
        
        # Crear token data
        token_data = {
            "token": creds.token,
            "refresh_token": creds.refresh_token,
            "token_uri": "https://oauth2.googleapis.com/token",
            "client_id": creds.client_id,
            "client_secret": creds.client_secret,
            "scopes": creds.scopes,
            "expiry": creds.expiry.isoformat() if creds.expiry else None
        }
        
        # Guardar token
        token_path = "gmail_token_new.json"
        with open(token_path, 'w') as f:
            json.dump(token_data, f, indent=2)
        
        print(f"✅ Token guardado en: {token_path}")
        print(f"✅ Refresh token incluido: {'SÍ' if creds.refresh_token else 'NO'}")
        
        # Mostrar contenido del token (sin datos sensibles)
        print("\n📋 Contenido del token generado:")
        safe_token = token_data.copy()
        safe_token['token'] = safe_token['token'][:20] + "..." if safe_token['token'] else None
        safe_token['refresh_token'] = safe_token['refresh_token'][:20] + "..." if safe_token['refresh_token'] else None
        safe_token['client_secret'] = safe_token['client_secret'][:10] + "..." if safe_token['client_secret'] else None
        print(json.dumps(safe_token, indent=2))
        
        print(f"\n💡 Copia el contenido completo de {token_path} y reemplaza GMAIL_TOKEN_JSON en tu .env")
        
    except Exception as e:
        print(f"❌ Error durante el flujo OAuth: {e}")
    finally:
        # Limpiar archivo temporal
        os.unlink(temp_path)

if __name__ == "__main__":
    main() 