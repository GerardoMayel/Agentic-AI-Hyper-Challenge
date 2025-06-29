#!/usr/bin/env python3
"""
Script simple para iniciar el servidor local para recibir emails.
"""

import subprocess
import sys
import time

def main():
    """Inicia el servidor FastAPI local."""
    print("="*60)
    print("🚀 SERVIDOR LOCAL PARA RECIBIR EMAILS")
    print("="*60)
    
    print("\n🌐 Iniciando servidor FastAPI...")
    print("📍 URL local: http://localhost:8000")
    print("📧 Webhook: http://localhost:8000/webhook/email")
    print("🔍 Status: http://localhost:8000/webhook/email")
    
    print("\n📋 INSTRUCCIONES:")
    print("1. El servidor estará disponible en: http://localhost:8000")
    print("2. Para recibir emails reales, necesitas configurar ngrok")
    print("3. Los emails recibidos se mostrarán en esta consola")
    print("4. Presiona Ctrl+C para detener")
    
    print("\n🔍 MONITOREO ACTIVO - Esperando emails...")
    print("="*60)
    
    try:
        # Iniciar servidor
        subprocess.run([
            sys.executable, '-m', 'uvicorn', 'main:app',
            '--host', '0.0.0.0',
            '--port', '8000',
            '--reload'
        ])
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor detenido")
        print("👋 ¡Hasta luego!")

if __name__ == "__main__":
    main() 