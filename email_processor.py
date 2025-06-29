#!/usr/bin/env python3
"""
Script Principal para Procesar Emails con Gmail API y Gemini
Lee emails con asunto "test", extrae texto e imágenes, y las procesa con Gemini
"""

import os
import sys
import json
from dotenv import load_dotenv
load_dotenv()

# Agregar el directorio app al path
sys.path.append('app')

from services.gmail_service import GmailService
from services.llm_service import LLMService

class EmailProcessor:
    """Procesador principal de emails con integración Gmail + Gemini."""
    
    def __init__(self):
        self.gmail_service = GmailService()
        self.llm_service = LLMService()
        
        # Variables para almacenar resultados
        self.email_text = ""
        self.image_analysis = {}
        
    def process_test_emails(self, max_results: int = 3):
        """
        Procesa emails con asunto "test".
        
        Args:
            max_results: Número máximo de emails a procesar
        """
        print("🚀 Procesador de Emails - Gmail + Gemini")
        print("=" * 60)
        
        # Verificar configuración
        if not self.gmail_service.service:
            print("❌ Servicio de Gmail no disponible")
            return
        
        if not self.llm_service.client:
            print("❌ Servicio de Gemini no disponible")
            return
        
        print("✅ Servicios configurados correctamente")
        print("\n📧 Buscando emails con asunto 'test'...")
        
        # Obtener emails con asunto "test"
        emails = self.gmail_service.get_test_emails(max_results)
        
        if not emails:
            print("📭 No se encontraron emails con asunto 'test'")
            print("💡 Envía un email con asunto 'test' desde tu email personal a geramfernandez@gmail.com")
            return
        
        print(f"\n📧 Procesando {len(emails)} emails encontrados...")
        
        # Procesar cada email
        for i, email_data in enumerate(emails, 1):
            print(f"\n{'='*60}")
            print(f"📧 Procesando Email {i}/{len(emails)}")
            print(f"{'='*60}")
            
            self._process_single_email(email_data)
    
    def _process_single_email(self, email_data: dict):
        """
        Procesa un email individual.
        
        Args:
            email_data: Datos del email
        """
        # Mostrar resumen del email
        self.gmail_service.print_email_summary(email_data)
        
        # Extraer texto del email
        email_body = email_data.get('body', '')
        self.email_text = email_body
        
        print(f"\n📄 Texto del Email:")
        print(f"{'='*40}")
        print(email_body)
        print(f"{'='*40}")
        
        # Procesar adjuntos (imágenes)
        attachments = email_data.get('attachments', [])
        
        if attachments:
            print(f"\n🖼️  Procesando {len(attachments)} adjuntos...")
            
            for j, attachment in enumerate(attachments, 1):
                print(f"\n📎 Adjunto {j}: {attachment['filename']}")
                
                if attachment['mime_type'].startswith('image/'):
                    self._process_image_attachment(attachment)
                else:
                    print(f"   ⚠️  Tipo de archivo no soportado: {attachment['mime_type']}")
        else:
            print("\n📎 No hay adjuntos en este email")
        
        # Analizar contenido completo del email
        print(f"\n🤖 Analizando contenido completo con Gemini...")
        analysis = self.llm_service.analyze_email_content(email_body, attachments)
        
        # Mostrar resultados
        self._display_analysis_results(analysis)
    
    def _process_image_attachment(self, attachment: dict):
        """
        Procesa un adjunto de imagen con Gemini.
        
        Args:
            attachment: Datos del adjunto
        """
        try:
            print(f"   🔍 Analizando imagen con Gemini...")
            
            # Analizar imagen con Gemini
            analysis = self.llm_service.analyze_image(
                attachment['data'],
                "Analyze this image and extract all text content. Return the result as a JSON object with the following structure: {'text_content': 'extracted text', 'description': 'brief description of the image', 'confidence': 'high/medium/low'}"
            )
            
            if analysis:
                # Guardar análisis en variable
                self.image_analysis[attachment['filename']] = analysis
                
                print(f"   ✅ Análisis completado")
                print(f"   📝 Texto extraído: {analysis.get('text_content', 'N/A')}")
                print(f"   📋 Descripción: {analysis.get('description', 'N/A')}")
                print(f"   🎯 Confianza: {analysis.get('confidence', 'N/A')}")
                
                # Mostrar JSON completo
                print(f"   📊 JSON completo:")
                print(f"   {json.dumps(analysis, indent=2, ensure_ascii=False)}")
            else:
                print(f"   ❌ Error analizando imagen")
                
        except Exception as e:
            print(f"   ❌ Error procesando imagen: {str(e)}")
    
    def _display_analysis_results(self, analysis: dict):
        """
        Muestra los resultados del análisis.
        
        Args:
            analysis: Resultados del análisis
        """
        print(f"\n📊 Resultados del Análisis Completo")
        print(f"{'='*60}")
        
        # Mostrar resumen
        summary = analysis.get('summary', {})
        if isinstance(summary, dict):
            print(f"📋 Resumen: {summary.get('summary', 'N/A')}")
            print(f"🎯 Puntos clave: {', '.join(summary.get('key_points', []))}")
            print(f"⚡ Acción requerida: {summary.get('action_required', False)}")
        else:
            print(f"📋 Resumen: {summary}")
        
        # Mostrar análisis de adjuntos
        attachments_analysis = analysis.get('attachments_analysis', [])
        if attachments_analysis:
            print(f"\n🖼️  Análisis de Imágenes:")
            for img_analysis in attachments_analysis:
                print(f"   📎 {img_analysis['filename']}:")
                print(f"      Texto: {img_analysis['analysis'].get('text_content', 'N/A')}")
                print(f"      Confianza: {img_analysis['analysis'].get('confidence', 'N/A')}")
        
        # Guardar resultados en variables
        self._save_results_to_variables(analysis)
    
    def _save_results_to_variables(self, analysis: dict):
        """
        Guarda los resultados en variables para uso posterior.
        
        Args:
            analysis: Resultados del análisis
        """
        print(f"\n💾 Guardando resultados en variables...")
        
        # Variable con texto del email
        self.email_text = analysis.get('email_text', '')
        
        # Variable con análisis de imágenes
        self.image_analysis = {}
        for img_analysis in analysis.get('attachments_analysis', []):
            self.image_analysis[img_analysis['filename']] = img_analysis['analysis']
        
        # Variable con resumen completo
        self.complete_analysis = analysis
        
        print(f"✅ Variables guardadas:")
        print(f"   📄 email_text: {len(self.email_text)} caracteres")
        print(f"   🖼️  image_analysis: {len(self.image_analysis)} imágenes")
        print(f"   📊 complete_analysis: Análisis completo disponible")
    
    def get_email_text(self) -> str:
        """Retorna el texto del email procesado."""
        return self.email_text
    
    def get_image_analysis(self) -> dict:
        """Retorna el análisis de imágenes."""
        return self.image_analysis
    
    def get_complete_analysis(self) -> dict:
        """Retorna el análisis completo."""
        return self.complete_analysis

def main():
    """Función principal."""
    print("🔧 Configurando Procesador de Emails...")
    
    # Crear procesador
    processor = EmailProcessor()
    
    # Procesar emails
    processor.process_test_emails(max_results=3)
    
    # Mostrar variables finales
    print(f"\n🎯 Variables Finales:")
    print(f"{'='*60}")
    
    email_text = processor.get_email_text()
    image_analysis = processor.get_image_analysis()
    complete_analysis = processor.get_complete_analysis()
    
    print(f"📄 email_text: {email_text[:100]}..." if len(email_text) > 100 else f"📄 email_text: {email_text}")
    print(f"🖼️  image_analysis: {json.dumps(image_analysis, indent=2, ensure_ascii=False)}")
    print(f"📊 complete_analysis: {json.dumps(complete_analysis, indent=2, ensure_ascii=False)}")
    
    print(f"\n🎉 ¡Procesamiento completado!")
    print(f"💡 Las variables están disponibles para uso posterior")

if __name__ == "__main__":
    main() 