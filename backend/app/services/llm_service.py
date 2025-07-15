"""
LLM Service using Google Gemini API
"""

import os
import json
import google.generativeai as genai
from typing import Dict, Any

class LLMService:
    """Service for LLM operations using Gemini"""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def analyze_text(self, prompt: str) -> str:
        """Analyze text using Gemini"""
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"❌ Error in LLM analysis: {e}")
            return ""
    
    def generate_text(self, prompt: str) -> str:
        """Generate text using Gemini (alias for analyze_text)"""
        return self.analyze_text(prompt)
    
    def generate_text_with_image(self, prompt: str, image_base64: str) -> str:
        """Generate text from image using Gemini Vision API"""
        try:
            import base64
            from PIL import Image
            import io
            
            # Decode base64 image
            image_data = base64.b64decode(image_base64)
            image = Image.open(io.BytesIO(image_data))
            
            # Use Gemini Vision model
            vision_model = genai.GenerativeModel('gemini-1.5-flash')
            response = vision_model.generate_content([prompt, image])
            
            return response.text.strip()
        except Exception as e:
            print(f"❌ Error in image analysis: {e}")
            return ""
    
    def extract_structured_data(self, text: str, fields: list) -> Dict[str, Any]:
        """Extract structured data from text"""
        try:
            prompt = f"""
            Extract the following fields from this text and return as JSON:
            Fields: {', '.join(fields)}
            
            Text: {text}
            
            Return ONLY valid JSON with the requested fields.
            """
            
            response = self.analyze_text(prompt)
            
            try:
                return json.loads(response)
            except:
                return {}
                
        except Exception as e:
            print(f"❌ Error extracting structured data: {e}")
            return {}
    
    def classify_document(self, text: str) -> str:
        """Classify document type"""
        try:
            prompt = f"""
            Classify this document as one of the following types:
            - FLIGHT_TICKET
            - HOTEL_RECEIPT
            - RESTAURANT_BILL
            - MEDICAL_DOCUMENT
            - POLICE_REPORT
            - OTHER
            
            Document text: {text[:1000]}
            
            Return ONLY the classification type.
            """
            
            return self.analyze_text(prompt).strip()
            
        except Exception as e:
            print(f"❌ Error classifying document: {e}")
            return "OTHER"
    
    def extract_costs(self, text: str) -> Dict[str, float]:
        """Extract costs from document text"""
        try:
            prompt = f"""
            Extract all monetary amounts and their descriptions from this text.
            Return as JSON with format: {{"description": amount}}
            
            Text: {text}
            
            Example: {{"Flight Cost": 500.00, "Hotel Fee": 200.00}}
            """
            
            response = self.analyze_text(prompt)
            
            try:
                return json.loads(response)
            except:
                return {}
                
        except Exception as e:
            print(f"❌ Error extracting costs: {e}")
            return {}
    
    def generate_summary(self, text: str) -> str:
        """Generate a summary of the text"""
        try:
            prompt = f"""
            Provide a brief summary of this text in 2-3 sentences:
            
            {text}
            """
            
            return self.analyze_text(prompt)
            
        except Exception as e:
            print(f"❌ Error generating summary: {e}")
            return "Summary not available"
    
    def analyze_email_content(self, email_data: Dict[str, str]) -> Dict[str, Any]:
        """Analyze email content to determine claim type and extract information"""
        try:
            subject = email_data.get("subject", "")
            body = email_data.get("body", "")
            
            prompt = f"""
            Analyze this email to determine if it's a claim notification and extract relevant information.
            
            Subject: {subject}
            Body: {body}
            
            Return a JSON object with the following structure:
            {{
                "is_claim": true/false,
                "claim_type": "TRAVEL_INSURANCE|HOTEL_INSURANCE|MEDICAL_INSURANCE|OTHER",
                "customer_name": "extracted name or null",
                "policy_number": "extracted policy number or null",
                "incident_date": "extracted date or null",
                "estimated_amount": "extracted amount or null",
                "priority": "LOW|NORMAL|HIGH|URGENT",
                "summary": "brief summary of the claim"
            }}
            
            Return ONLY valid JSON.
            """
            
            response = self.analyze_text(prompt)
            
            try:
                result = json.loads(response)
                return result
            except:
                # Fallback response
                return {
                    "is_claim": True,
                    "claim_type": "OTHER",
                    "customer_name": None,
                    "policy_number": None,
                    "incident_date": None,
                    "estimated_amount": None,
                    "priority": "NORMAL",
                    "summary": "Claim notification detected"
                }
                
        except Exception as e:
            print(f"❌ Error analyzing email content: {e}")
            return {
                "is_claim": True,
                "claim_type": "OTHER",
                "customer_name": None,
                "policy_number": None,
                "incident_date": None,
                "estimated_amount": None,
                "priority": "NORMAL",
                "summary": "Error analyzing email content"
            } 