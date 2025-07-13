#!/usr/bin/env python3
"""
Script para generar el token de Gmail (con refresh_token) usando OAuth 2.0
"""

import os
import json
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

# Scopes necesarios para Gmail
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/userinfo.email',
    'openid',
    'offline_access'
]

def main():
    print("🔑 Generador de token OAuth para Gmail API")
    cred_path = input("Ruta al archivo de credenciales OAuth (JSON): ").strip()
    token_path = input("Ruta donde guardar el token generado (ej: gmail_token.json): ").strip()

    if not os.path.exists(cred_path):
        print(f"❌ No se encontró el archivo: {cred_path}")
        return

    # Leer credenciales
    with open(cred_path, 'r') as f:
        creds_json = json.load(f)

    # Detectar si es tipo 'web' o 'installed'
    if 'installed' in creds_json:
        client_config = creds_json['installed']
    elif 'web' in creds_json:
        client_config = creds_json['web']
    else:
        print("❌ El archivo de credenciales no es válido (falta 'installed' o 'web')")
        return

    # Guardar temporalmente el archivo en formato compatible
    temp_path = Path("temp_gmail_oauth.json")
    with open(temp_path, 'w') as f:
        json.dump({"installed": client_config}, f)

    # Flujo OAuth
    flow = InstalledAppFlow.from_client_secrets_file(
        str(temp_path), SCOPES)
    creds = flow.run_local_server(port=8080, prompt='consent', authorization_prompt_message='')

    # Guardar token
    token_data = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes,
        "expiry": creds.expiry.isoformat() if creds.expiry else None
    }
    with open(token_path, 'w') as f:
        json.dump(token_data, f, indent=2)
    print(f"✅ Token guardado en: {token_path}")

    # Limpiar archivo temporal
    temp_path.unlink()

if __name__ == "__main__":
    main() 