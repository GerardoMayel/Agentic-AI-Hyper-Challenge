#!/usr/bin/env python3
"""
Enhanced OCR Service using Gemini AI
Processes documents and extracts structured information
"""

import os
import json
import base64
from typing import Dict, Any, List, Optional
from app.services.llm_service import LLMService

class EnhancedOCRService:
    """Service for enhanced document processing with Gemini AI"""
    
    def __init__(self):
        self.gemini_service = LLMService()
        
        # Supported document types
        self.supported_types = [
            "POLICE_REPORT",
            "MEDICAL_REPORT", 
            "RECEIPT",
            "INVOICE",
            "INSURANCE_POLICY",
            "DRIVERS_LICENSE",
            "PASSPORT",
            "MEDICAL_CERTIFICATE",
            "TRAVEL_ITINERARY",
            "HOTEL_RECEIPT",
            "FLIGHT_TICKET",
            "CAR_RENTAL_AGREEMENT",
            "OTHER"
        ]
    
    def process_document_with_gemini(self, image_data: bytes, filename: str, document_type: str = "OTHER") -> Dict[str, Any]:
        """
        Process a document image using Gemini Vision API
        
        Args:
            image_data: Raw image bytes
            filename: Original filename
            document_type: Type of document for context
            
        Returns:
            Dictionary with extracted information
        """
        
        try:
            # Encode image to base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # Create prompt based on document type
            prompt = self._create_document_prompt(filename, document_type)
            
            # Process with Gemini Vision
            response = self.gemini_service.generate_text_with_image(prompt, image_base64)
            
            # Parse the response
            extracted_data = self._parse_ocr_response(response, document_type)
            
            return extracted_data
            
        except Exception as e:
            print(f"❌ Error in enhanced OCR processing: {e}")
            return self._get_default_ocr_result(filename, document_type)
    
    def _create_document_prompt(self, filename: str, document_type: str) -> str:
        """Create a specific prompt based on document type"""
        
        base_prompt = f"""
        Analyze this document image and extract all relevant information.
        
        FILENAME: {filename}
        DOCUMENT TYPE: {document_type}
        
        Please provide a comprehensive analysis in JSON format with the following structure:
        
        {{
            "document_type": "detected_document_type",
            "confidence": 0.0-1.0,
            "extracted_text": "All text found in the document",
            "structured_data": {{
                "dates": ["list of dates found"],
                "amounts": ["list of monetary amounts"],
                "names": ["list of names found"],
                "addresses": ["list of addresses"],
                "phone_numbers": ["list of phone numbers"],
                "email_addresses": ["list of email addresses"],
                "policy_numbers": ["list of policy/claim numbers"],
                "reference_numbers": ["list of reference numbers"]
            }},
            "key_information": {{
                "total_amount": "total monetary amount if applicable",
                "date": "main date of the document",
                "issuer": "who issued the document",
                "recipient": "who the document is for",
                "purpose": "what the document is for"
            }},
            "ocr_quality": "good|fair|poor",
            "processing_notes": "Any notes about the processing"
        }}
        
        """
        
        # Add specific instructions based on document type
        if document_type == "POLICE_REPORT":
            base_prompt += """
            For police reports, focus on:
            - Incident date and time
            - Location of incident
            - Parties involved
            - Officer information
            - Case/report numbers
            - Description of events
            """
        elif document_type == "MEDICAL_REPORT":
            base_prompt += """
            For medical reports, focus on:
            - Patient information
            - Diagnosis
            - Treatment provided
            - Dates of service
            - Medical codes
            - Prescriptions
            """
        elif document_type == "RECEIPT":
            base_prompt += """
            For receipts, focus on:
            - Merchant information
            - Date of purchase
            - Items purchased
            - Individual prices
            - Total amount
            - Payment method
            """
        elif document_type == "INSURANCE_POLICY":
            base_prompt += """
            For insurance policies, focus on:
            - Policy number
            - Coverage details
            - Effective dates
            - Premium amounts
            - Insured party information
            - Coverage limits
            """
        
        return base_prompt
    
    def _parse_ocr_response(self, response: str, document_type: str) -> Dict[str, Any]:
        """Parse the OCR response and validate it"""
        
        try:
            # Try to parse as JSON
            data = json.loads(response)
            
            # Validate and normalize the response
            data = self._validate_ocr_data(data, document_type)
            
            return data
            
        except json.JSONDecodeError:
            # If not valid JSON, create structured data from text
            return self._create_structured_data_from_text(response, document_type)
    
    def _validate_ocr_data(self, data: Dict[str, Any], document_type: str) -> Dict[str, Any]:
        """Validate and normalize OCR data"""
        
        # Ensure all required fields exist
        required_fields = {
            "document_type": document_type,
            "confidence": 0.5,
            "extracted_text": "",
            "structured_data": {
                "dates": [],
                "amounts": [],
                "names": [],
                "addresses": [],
                "phone_numbers": [],
                "email_addresses": [],
                "policy_numbers": [],
                "reference_numbers": []
            },
            "key_information": {
                "total_amount": "",
                "date": "",
                "issuer": "",
                "recipient": "",
                "purpose": ""
            },
            "ocr_quality": "fair",
            "processing_notes": "Processed with Gemini Vision API"
        }
        
        for field, default_value in required_fields.items():
            if field not in data:
                data[field] = default_value
        
        # Normalize confidence score
        data["confidence"] = max(0.0, min(1.0, float(data["confidence"])))
        
        return data
    
    def _create_structured_data_from_text(self, text: str, document_type: str) -> Dict[str, Any]:
        """Create structured data when JSON parsing fails"""
        
        return {
            "document_type": document_type,
            "confidence": 0.3,
            "extracted_text": text,
            "structured_data": {
                "dates": [],
                "amounts": [],
                "names": [],
                "addresses": [],
                "phone_numbers": [],
                "email_addresses": [],
                "policy_numbers": [],
                "reference_numbers": []
            },
            "key_information": {
                "total_amount": "",
                "date": "",
                "issuer": "",
                "recipient": "",
                "purpose": ""
            },
            "ocr_quality": "poor",
            "processing_notes": "JSON parsing failed, using raw text"
        }
    
    def _get_default_ocr_result(self, filename: str, document_type: str) -> Dict[str, Any]:
        """Return default OCR result when processing fails"""
        
        return {
            "document_type": document_type,
            "confidence": 0.0,
            "extracted_text": "Processing failed",
            "structured_data": {
                "dates": [],
                "amounts": [],
                "names": [],
                "addresses": [],
                "phone_numbers": [],
                "email_addresses": [],
                "policy_numbers": [],
                "reference_numbers": []
            },
            "key_information": {
                "total_amount": "",
                "date": "",
                "issuer": "",
                "recipient": "",
                "purpose": ""
            },
            "ocr_quality": "poor",
            "processing_notes": f"Failed to process {filename}"
        }
    
    def get_document_summary(self, ocr_data: Dict[str, Any]) -> str:
        """Generate a human-readable summary of the OCR data"""
        
        summary_parts = []
        
        # Document type and confidence
        doc_type = ocr_data.get("document_type", "Unknown")
        confidence = ocr_data.get("confidence", 0.0)
        summary_parts.append(f"Document Type: {doc_type} (Confidence: {confidence:.1%})")
        
        # Key information
        key_info = ocr_data.get("key_information", {})
        if key_info.get("date"):
            summary_parts.append(f"Date: {key_info['date']}")
        if key_info.get("total_amount"):
            summary_parts.append(f"Amount: {key_info['total_amount']}")
        if key_info.get("issuer"):
            summary_parts.append(f"Issuer: {key_info['issuer']}")
        
        # Structured data counts
        structured_data = ocr_data.get("structured_data", {})
        if structured_data.get("dates"):
            summary_parts.append(f"Dates found: {len(structured_data['dates'])}")
        if structured_data.get("amounts"):
            summary_parts.append(f"Amounts found: {len(structured_data['amounts'])}")
        if structured_data.get("names"):
            summary_parts.append(f"Names found: {len(structured_data['names'])}")
        
        return " | ".join(summary_parts) 