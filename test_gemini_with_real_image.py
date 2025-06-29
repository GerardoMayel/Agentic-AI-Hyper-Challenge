#!/usr/bin/env python3
"""
Script para Probar Gemini con Imagen Real
Crea una imagen de prueba y la analiza con Gemini
"""

import os
import sys
from dotenv import load_dotenv
load_dotenv()

# Agregar el directorio app al path
sys.path.append('app')

from PIL import Image, ImageDraw, ImageFont
import io

def create_test_image():
    """Crea una imagen de prueba con texto."""
    print("🎨 Creando imagen de prueba...")
    
    # Crear una imagen blanca de 400x200
    img = Image.new('RGB', (400, 200), color='white')
    draw = ImageDraw.Draw(img)
    
    # Agregar texto a la imagen
    try:
        # Intentar usar una fuente del sistema
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 20)
    except:
        # Usar fuente por defecto si no está disponible
        font = ImageFont.load_default()
    
    # Dibujar texto
    text = "TEST EMAIL\nImagen de prueba\nTexto para extraer"
    draw.text((50, 50), text, fill='black', font=font)
    
    # Dibujar un rectángulo
    draw.rectangle([50, 120, 350, 150], outline='blue', width=2)
    
    # Convertir a bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    print("✅ Imagen de prueba creada")
    return img_bytes.getvalue()

def test_gemini_with_real_image():
    """Prueba Gemini con una imagen real."""
    print("🤖 Probando Gemini con Imagen Real")
    print("=" * 50)
    
    try:
        from services.llm_service import LLMService
        
        llm_service = LLMService()
        
        if not llm_service.client:
            print("❌ Gemini no está configurado correctamente")
            return False
        
        print("✅ Cliente de Gemini configurado correctamente")
        
        # Crear imagen de prueba
        test_image_data = create_test_image()
        
        print("🔍 Analizando imagen con Gemini...")
        
        # Probar análisis de imagen
        result = llm_service.analyze_image(
            test_image_data,
            "Analyze this image and extract all text content. Return the result as a JSON object with the following structure: {'text_content': 'extracted text', 'description': 'brief description of the image', 'confidence': 'high/medium/low'}"
        )
        
        if result:
            print("✅ Análisis de imagen exitoso")
            print(f"📝 Texto extraído: {result.get('text_content', 'N/A')}")
            print(f"📋 Descripción: {result.get('description', 'N/A')}")
            print(f"🎯 Confianza: {result.get('confidence', 'N/A')}")
            print(f"📊 JSON completo: {result}")
            return True
        else:
            print("❌ Error en análisis de imagen")
            return False
            
    except Exception as e:
        print(f"❌ Error probando Gemini: {str(e)}")
        return False

def test_text_extraction():
    """Prueba la extracción de texto específicamente."""
    print("\n📝 Probando Extracción de Texto")
    print("=" * 40)
    
    try:
        from services.llm_service import LLMService
        
        llm_service = LLMService()
        
        if not llm_service.client:
            print("❌ Gemini no está configurado")
            return False
        
        # Crear imagen de prueba
        test_image_data = create_test_image()
        
        print("🔍 Extrayendo texto de la imagen...")
        
        # Probar extracción de texto
        extracted_text = llm_service.extract_text_from_image(test_image_data)
        
        if extracted_text:
            print("✅ Extracción de texto exitosa")
            print(f"📄 Texto extraído: '{extracted_text}'")
            return True
        else:
            print("❌ Error extrayendo texto")
            return False
            
    except Exception as e:
        print(f"❌ Error en extracción de texto: {str(e)}")
        return False

def main():
    """Función principal."""
    print("🧪 Prueba de Gemini con Imagen Real")
    print("=" * 60)
    
    # Verificar configuración de Gemini
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        print("❌ GEMINI_API_KEY no está configurada")
        print("💡 Configura la variable de entorno GEMINI_API_KEY")
        return
    
    print("✅ GEMINI_API_KEY configurada")
    
    # Probar análisis de imagen
    image_analysis_success = test_gemini_with_real_image()
    
    # Probar extracción de texto
    text_extraction_success = test_text_extraction()
    
    # Resumen
    print(f"\n📊 Resumen de Pruebas:")
    print(f"   🖼️  Análisis de imagen: {'✅' if image_analysis_success else '❌'}")
    print(f"   📝 Extracción de texto: {'✅' if text_extraction_success else '❌'}")
    
    if image_analysis_success and text_extraction_success:
        print(f"\n🎉 ¡Todas las pruebas exitosas!")
        print(f"💡 Gemini está listo para procesar emails con imágenes")
    else:
        print(f"\n⚠️  Algunas pruebas fallaron")
        print(f"💡 Revisa la configuración de Gemini API")

if __name__ == "__main__":
    main() 