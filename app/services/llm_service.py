import os
import base64
import json
from typing import List, Dict, Any, Optional
from google import genai

class LLMService:
    """Servicio para interactuar con Google Gemini LLM."""
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None
            print("⚠️  GEMINI_API_KEY no está configurada")
    
    def analyze_image(self, image_data: bytes, prompt: str = "Analyze this image and extract all text content. Return the result as a JSON object with the following structure: {'text_content': 'extracted text', 'description': 'brief description of the image', 'confidence': 'high/medium/low'}") -> Optional[Dict[str, Any]]:
        """
        Analiza una imagen usando Gemini Vision.
        
        Args:
            image_data: Datos de la imagen en bytes
            prompt: Prompt para el análisis
            
        Returns:
            Diccionario con el resultado del análisis o None si hay error
        """
        if not self.client:
            print("❌ Cliente de Gemini no disponible")
            return None
        
        try:
            # Codificar la imagen en base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # Crear el contenido con imagen y texto
            content = [
                {
                    "role": "user",
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": image_base64
                            }
                        }
                    ]
                }
            ]
            
            # Generar respuesta
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-lite",
                contents=content
            )
            
            # Intentar parsear como JSON
            try:
                result = json.loads(response.text)
                return result
            except json.JSONDecodeError:
                # Si no es JSON válido, devolver como texto
                return {
                    "text_content": response.text,
                    "description": "Análisis de imagen completado",
                    "confidence": "medium"
                }
                
        except Exception as e:
            print(f"❌ Error analizando imagen: {str(e)}")
            return None
    
    def extract_text_from_image(self, image_data: bytes) -> Optional[str]:
        """
        Extrae texto de una imagen.
        
        Args:
            image_data: Datos de la imagen en bytes
            
        Returns:
            Texto extraído o None si hay error
        """
        result = self.analyze_image(
            image_data, 
            "Extract all text content from this image. Return only the extracted text, nothing else."
        )
        
        if result and isinstance(result, dict):
            return result.get('text_content', '')
        
        return result if isinstance(result, str) else None
    
    def analyze_email_content(self, email_body: str, attachments: list) -> Dict[str, Any]:
        """
        Analiza el contenido de un email y sus adjuntos.
        
        Args:
            email_body: Cuerpo del email
            attachments: Lista de adjuntos
            
        Returns:
            Diccionario con el análisis completo
        """
        analysis = {
            "email_text": email_body,
            "attachments_analysis": [],
            "summary": ""
        }
        
        # Analizar adjuntos de imagen
        for attachment in attachments:
            if attachment['mime_type'].startswith('image/'):
                print(f"🔍 Analizando imagen: {attachment['filename']}")
                
                image_analysis = self.analyze_image(
                    attachment['data'],
                    "Analyze this image and extract all text content. Return as JSON: {'text_content': 'extracted text', 'description': 'brief description', 'confidence': 'high/medium/low'}"
                )
                
                if image_analysis:
                    analysis["attachments_analysis"].append({
                        "filename": attachment['filename'],
                        "mime_type": attachment['mime_type'],
                        "analysis": image_analysis
                    })
        
        # Generar resumen del email
        if self.client:
            try:
                summary_prompt = f"""
                Analyze this email content and provide a brief summary:
                
                Email Body: {email_body}
                
                Attachments: {len(analysis['attachments_analysis'])} images analyzed
                
                Provide a concise summary in JSON format:
                {{"summary": "brief summary", "key_points": ["point1", "point2"], "action_required": true/false}}
                """
                
                response = self.client.models.generate_content(
                    model="gemini-2.0-flash-lite",
                    contents=summary_prompt
                )
                
                try:
                    summary_result = json.loads(response.text)
                    analysis["summary"] = summary_result
                except json.JSONDecodeError:
                    analysis["summary"] = {
                        "summary": response.text,
                        "key_points": [],
                        "action_required": False
                    }
                    
            except Exception as e:
                print(f"❌ Error generando resumen: {str(e)}")
                analysis["summary"] = {
                    "summary": "Error generando resumen",
                    "key_points": [],
                    "action_required": False
                }
        
        return analysis

# Instancia global del servicio
llm_service = LLMService() 