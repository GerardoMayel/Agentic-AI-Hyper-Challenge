#!/usr/bin/env python3
"""
Script de Prueba Rápida para Lectura de Emails
Verifica la configuración y muestre instrucciones
"""

import os
import sys
from dotenv import load_dotenv
load_dotenv()

# Agregar el directorio app al path
sys.path.append('app')

def test_configuration():
    """Prueba la configuración de las APIs."""
    print("🔍 Prueba Rápida de Lectura de Emails")
    print("=" * 50)
    
    # Verificar variables de entorno
    gemini_key = os.getenv("GEMINI_API_KEY")
    resend_key = os.getenv("RESEND_API_KEY")
    
    print("📋 Verificando Configuración:")
    print(f"   🔑 GEMINI_API_KEY: {'✅ Configurada' if gemini_key else '❌ No configurada'}")
    print(f"   📧 RESEND_API_KEY: {'✅ Configurada' if resend_key else '❌ No configurada'}")
    
    # Verificar archivo de credenciales de Gmail
    credentials_file = "credentials.json"
    if os.path.exists(credentials_file):
        print(f"   📁 credentials.json: ✅ Encontrado")
        gmail_configured = True
    else:
        print(f"   📁 credentials.json: ❌ No encontrado")
        gmail_configured = False
    
    print(f"\n📊 Estado de Configuración:")
    print(f"   🤖 Gemini: {'✅' if gemini_key else '❌'}")
    print(f"   📧 Gmail API: {'✅' if gmail_configured else '❌'}")
    print(f"   📤 Resend: {'✅' if resend_key else '❌'}")
    
    return gemini_key, gmail_configured, resend_key

def test_gemini_only():
    """Prueba solo la funcionalidad de Gemini."""
    print("\n🤖 Probando Gemini API...")
    
    try:
        from services.llm_service import LLMService
        
        llm_service = LLMService()
        
        if not llm_service.client:
            print("❌ Gemini no está configurado correctamente")
            return False
        
        # Prueba simple de Gemini
        print("✅ Cliente de Gemini configurado correctamente")
        
        # Crear una imagen de prueba simple (1x1 pixel)
        test_image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf5\xd7\xd4\xc2\x00\x00\x00\x00IEND\xaeB`\x82'
        
        print("🔍 Probando análisis de imagen...")
        result = llm_service.analyze_image(
            test_image_data,
            "Describe this image briefly. Return as JSON: {'description': 'brief description'}"
        )
        
        if result:
            print("✅ Análisis de imagen exitoso")
            print(f"   Resultado: {result}")
            return True
        else:
            print("❌ Error en análisis de imagen")
            return False
            
    except Exception as e:
        print(f"❌ Error probando Gemini: {str(e)}")
        return False

def show_instructions():
    """Muestra instrucciones para completar la configuración."""
    print("\n📋 Instrucciones para Completar la Configuración:")
    print("=" * 60)
    
    print("\n1. 🔑 Configurar Gemini API:")
    print("   - Ve a: https://aistudio.google.com/app/apikey")
    print("   - Crea una nueva API key")
    print("   - Agrega GEMINI_API_KEY=tu_api_key en .env")
    
    print("\n2. 📧 Configurar Gmail API:")
    print("   - Ve a: https://console.cloud.google.com/")
    print("   - Crea un proyecto o selecciona uno existente")
    print("   - Habilita Gmail API")
    print("   - Crea credenciales OAuth 2.0 (Desktop application)")
    print("   - Descarga y renombra a credentials.json")
    
    print("\n3. 📤 Configurar Resend (opcional para pruebas):")
    print("   - Ve a: https://resend.com/api-keys")
    print("   - Crea una API key")
    print("   - Agrega RESEND_API_KEY=tu_api_key en .env")
    
    print("\n4. 🧪 Ejecutar Pruebas:")
    print("   - python quick_email_read_test.py")
    print("   - python email_processor.py")

def simulate_email_processing():
    """Simula el procesamiento de emails para demostración."""
    print("\n🎭 Simulación de Procesamiento de Emails")
    print("=" * 50)
    
    # Simular datos de email
    simulated_email = {
        "id": "simulated_email_123",
        "subject": "test",
        "sender": "tu-email@gmail.com",
        "date": "Mon, 23 Jun 2025 22:45:00 +0000",
        "body": "Este es un email de prueba con texto e imagen adjunta.",
        "attachments": [
            {
                "filename": "imagen_prueba.jpg",
                "mime_type": "image/jpeg",
                "size": 1024
            }
        ]
    }
    
    print("📧 Email Simulado:")
    print(f"   ID: {simulated_email['id']}")
    print(f"   Asunto: {simulated_email['subject']}")
    print(f"   Remitente: {simulated_email['sender']}")
    print(f"   Fecha: {simulated_email['date']}")
    print(f"   Cuerpo: {simulated_email['body']}")
    print(f"   Adjuntos: {len(simulated_email['attachments'])}")
    
    # Simular variables de salida
    email_text = simulated_email['body']
    image_analysis = {
        "imagen_prueba.jpg": {
            "text_content": "Texto extraído de la imagen (simulado)",
            "description": "Imagen de prueba con texto",
            "confidence": "high"
        }
    }
    complete_analysis = {
        "email_text": email_text,
        "attachments_analysis": [
            {
                "filename": "imagen_prueba.jpg",
                "mime_type": "image/jpeg",
                "analysis": image_analysis["imagen_prueba.jpg"]
            }
        ],
        "summary": {
            "summary": "Email de prueba con imagen adjunta",
            "key_points": ["prueba", "imagen", "texto"],
            "action_required": False
        }
    }
    
    print("\n📊 Variables de Salida (Simuladas):")
    print(f"   📄 email_text: {email_text}")
    print(f"   🖼️  image_analysis: {image_analysis}")
    print(f"   📋 complete_analysis: {complete_analysis['summary']}")
    
    print("\n✅ Simulación completada")
    print("💡 Una vez configuradas las APIs, el sistema procesará emails reales")

def main():
    """Función principal."""
    print("🚀 Prueba Rápida de Lectura de Emails")
    print("=" * 60)
    
    # Verificar configuración
    gemini_key, gmail_configured, resend_key = test_configuration()
    
    # Probar Gemini si está configurado
    if gemini_key:
        gemini_working = test_gemini_only()
    else:
        gemini_working = False
    
    # Mostrar estado general
    print(f"\n📊 Estado General:")
    print(f"   🤖 Gemini: {'✅ Funcionando' if gemini_working else '❌ No configurado'}")
    print(f"   📧 Gmail API: {'✅ Configurado' if gmail_configured else '❌ No configurado'}")
    print(f"   📤 Resend: {'✅ Configurado' if resend_key else '❌ No configurado'}")
    
    # Mostrar instrucciones si algo falta
    if not gmail_configured or not gemini_working:
        show_instructions()
    
    # Simular procesamiento
    simulate_email_processing()
    
    print(f"\n🎯 Resumen:")
    if gmail_configured and gemini_working:
        print("✅ Sistema listo para procesar emails reales")
        print("💡 Ejecuta: python email_processor.py")
    else:
        print("⚠️  Configuración incompleta")
        print("💡 Sigue las instrucciones para completar la configuración")

if __name__ == "__main__":
    main() 