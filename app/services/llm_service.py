import os
from typing import List, Dict, Any, Optional
import google.generativeai as genai

class LLMService:
    """Servicio para interactuar con la API de Google Gemini."""
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
            print("GEMINI_API_KEY no está configurada.")
    
    def get_response(
        self,
        prompt: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Obtiene una respuesta del modelo Gemini.
        
        Args:
            prompt: El prompt o mensaje del usuario
            conversation_history: Historial de conversación previo
            
        Returns:
            str: La respuesta generada por el modelo
        """
        if not self.model:
            return "Lo siento, el servicio de IA no está disponible en este momento."
        
        try:
            if conversation_history:
                # Construir el contexto completo con el historial
                full_prompt = self._build_context_prompt(prompt, conversation_history)
                response = self.model.generate_content(full_prompt)
            else:
                response = self.model.generate_content(prompt)
            
            return response.text
            
        except Exception as e:
            print(f"Error llamando a Gemini API: {str(e)}")
            return "Lo siento, hubo un error procesando tu solicitud."
    
    def get_gemini_response(self, conversation_history: List[Dict[str, str]]) -> str:
        """
        Obtiene una respuesta del modelo Gemini basado en un historial de conversación.
        
        Args:
            conversation_history: Una lista de diccionarios con roles y contenido.
                                 Formato: [{"role": "user", "content": "..."}, ...]
        
        Returns:
            str: La respuesta en texto generada por el modelo.
        """
        if not self.model:
            print("Gemini API no está configurada. Respuesta simulada.")
            return "Esta es una respuesta simulada del LLM."
        
        try:
            # Construir el prompt con el historial de conversación
            prompt = self._format_conversation_history(conversation_history)
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"Error llamando a la API de Gemini: {str(e)}")
            return "Lo siento, hubo un error procesando tu solicitud."
    
    def _build_context_prompt(
        self,
        current_prompt: str,
        conversation_history: List[Dict[str, str]]
    ) -> str:
        """
        Construye un prompt con contexto basado en el historial de conversación.
        
        Args:
            current_prompt: El prompt actual
            conversation_history: Historial de conversación
            
        Returns:
            str: Prompt completo con contexto
        """
        context = "Contexto de la conversación anterior:\n"
        
        for message in conversation_history[-5:]:  # Últimos 5 mensajes para contexto
            role = message.get("role", "unknown")
            content = message.get("content", "")
            context += f"{role.upper()}: {content}\n"
        
        context += f"\nMensaje actual: {current_prompt}\n\nPor favor, responde al mensaje actual considerando el contexto proporcionado."
        
        return context
    
    def _format_conversation_history(self, history: List[Dict[str, str]]) -> str:
        """
        Formatea el historial de conversación para enviarlo al modelo.
        
        Args:
            history: Lista de mensajes con roles y contenido
            
        Returns:
            str: Historial formateado
        """
        formatted = "Historial de la conversación:\n\n"
        
        for message in history:
            role = message.get("role", "unknown")
            content = message.get("content", "")
            formatted += f"{role.upper()}: {content}\n\n"
        
        formatted += "Por favor, continúa la conversación de manera natural y útil."
        
        return formatted
    
    def analyze_email_content(self, email_content: str) -> Dict[str, Any]:
        """
        Analiza el contenido de un email para extraer información relevante.
        
        Args:
            email_content: Contenido del email
            
        Returns:
            Dict: Información analizada del email
        """
        if not self.model:
            return {
                "sentiment": "neutral",
                "urgency": "low",
                "category": "general",
                "summary": "No se pudo analizar el contenido."
            }
        
        try:
            analysis_prompt = f"""
            Analiza el siguiente email y proporciona:
            1. Sentimiento (positive, negative, neutral)
            2. Urgencia (high, medium, low)
            3. Categoría (support, sales, general, complaint, inquiry)
            4. Resumen breve del contenido
            
            Email:
            {email_content}
            
            Responde en formato JSON:
            {{
                "sentiment": "...",
                "urgency": "...",
                "category": "...",
                "summary": "..."
            }}
            """
            
            response = self.model.generate_content(analysis_prompt)
            # Aquí deberías parsear la respuesta JSON
            # Por simplicidad, retornamos un análisis básico
            return {
                "sentiment": "neutral",
                "urgency": "medium",
                "category": "general",
                "summary": response.text[:200] + "..." if len(response.text) > 200 else response.text
            }
            
        except Exception as e:
            print(f"Error analizando email: {str(e)}")
            return {
                "sentiment": "neutral",
                "urgency": "low",
                "category": "general",
                "summary": "Error en el análisis."
            }

# Instancia global del servicio
llm_service = LLMService() 