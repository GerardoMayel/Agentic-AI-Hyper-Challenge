#!/usr/bin/env python3
"""
Sentiment Analysis Service using Gemini AI
Analyzes claim descriptions and provides detailed recommendations
"""

import os
import json
from typing import Dict, Any, Optional
from app.services.llm_service import GeminiService

class SentimentAnalysisService:
    """Service for analyzing claim sentiment and generating recommendations"""
    
    def __init__(self):
        self.gemini_service = GeminiService()
        
        # Available coverage types in the system
        self.coverage_types = [
            "AUTO_INSURANCE",
            "HOME_INSURANCE", 
            "TRAVEL_INSURANCE",
            "HEALTH_INSURANCE",
            "LIFE_INSURANCE",
            "MEDICAL_INSURANCE",
            "HOTEL_INSURANCE",
            "OTHER"
        ]
        
    def analyze_claim_sentiment(self, claim_description: str, customer_name: str = "", claim_type: str = "") -> Dict[str, Any]:
        """
        Analyze the sentiment of a claim description and generate detailed recommendations
        
        Args:
            claim_description: The claim description text
            customer_name: Customer name for context
            claim_type: Type of claim for context (must be one of the defined coverage types)
            
        Returns:
            Dictionary with sentiment analysis results
        """
        
        # Validate claim type
        if claim_type and claim_type not in self.coverage_types:
            claim_type = "OTHER"
        
        prompt = f"""
        Analyze the following insurance claim and provide a detailed analysis:

        CUSTOMER: {customer_name}
        CLAIM TYPE: {claim_type}
        DESCRIPTION: {claim_description}

        Please provide a comprehensive analysis in JSON format with the following fields:

        {{
            "sentiment_score": 0.0-1.0,  // 0.0 = very negative, 1.0 = very positive
            "sentiment_label": "positive|negative|neutral",
            "risk_score": 0.0-1.0,  // 0.0 = low risk, 1.0 = high risk
            "priority_level": "low|medium|high|urgent",
            "traffic_light": "red|yellow|green",  // Risk traffic light
            "sentiment_analysis": "Detailed analysis of customer sentiment",
            "risk_factors": ["List of identified risk factors"],
            "recommendations": {{
                "immediate_actions": ["Immediate actions recommended"],
                "investigation_steps": ["Suggested investigation steps"],
                "documentation_needed": ["Additional documents required"],
                "communication_strategy": "Recommended communication strategy",
                "escalation_needed": true/false,
                "estimated_processing_time": "Estimated processing time"
            }},
            "ai_confidence": 0.0-1.0  // AI confidence level
        }}

        Consider:
        - Customer emotional tone
        - Risk factors in the description
        - Claim urgency
        - Case complexity
        - Need for additional documentation
        - Coverage type specific considerations
        """

        try:
            response = self.gemini_service.generate_text(prompt)
            
            # Parse the JSON response
            analysis = json.loads(response)
            
            # Validate and normalize the response
            analysis = self._validate_analysis(analysis)
            
            return analysis
            
        except Exception as e:
            print(f"❌ Error in sentiment analysis: {e}")
            # Return default analysis
            return self._get_default_analysis()
    
    def _validate_analysis(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and normalize the analysis response"""
        
        # Ensure all required fields exist
        required_fields = {
            "sentiment_score": 0.5,
            "sentiment_label": "neutral",
            "risk_score": 0.5,
            "priority_level": "medium",
            "traffic_light": "yellow",
            "sentiment_analysis": "Analysis not available",
            "risk_factors": [],
            "recommendations": {
                "immediate_actions": ["Review documentation"],
                "investigation_steps": ["Contact customer"],
                "documentation_needed": ["Additional documents"],
                "communication_strategy": "Direct contact",
                "escalation_needed": False,
                "estimated_processing_time": "5-7 days"
            },
            "ai_confidence": 0.5
        }
        
        for field, default_value in required_fields.items():
            if field not in analysis:
                analysis[field] = default_value
        
        # Normalize scores to 0.0-1.0 range
        analysis["sentiment_score"] = max(0.0, min(1.0, float(analysis["sentiment_score"])))
        analysis["risk_score"] = max(0.0, min(1.0, float(analysis["risk_score"])))
        analysis["ai_confidence"] = max(0.0, min(1.0, float(analysis["ai_confidence"])))
        
        return analysis
    
    def _get_default_analysis(self) -> Dict[str, Any]:
        """Return default analysis when AI fails"""
        return {
            "sentiment_score": 0.5,
            "sentiment_label": "neutral",
            "risk_score": 0.5,
            "priority_level": "medium",
            "traffic_light": "yellow",
            "sentiment_analysis": "Analysis not available - using default values",
            "risk_factors": ["Limited information"],
            "recommendations": {
                "immediate_actions": ["Review available documentation"],
                "investigation_steps": ["Contact customer for more information"],
                "documentation_needed": ["Additional documents required"],
                "communication_strategy": "Direct contact recommended",
                "escalation_needed": False,
                "estimated_processing_time": "5-7 days"
            },
            "ai_confidence": 0.0
        }
    
    def get_traffic_light_color(self, risk_score: float) -> str:
        """Get traffic light color based on risk score"""
        if risk_score >= 0.7:
            return "red"
        elif risk_score >= 0.4:
            return "yellow"
        else:
            return "green"
    
    def get_priority_level(self, risk_score: float, sentiment_score: float) -> str:
        """Get priority level based on risk and sentiment scores"""
        combined_score = (risk_score + (1 - sentiment_score)) / 2
        
        if combined_score >= 0.8:
            return "urgent"
        elif combined_score >= 0.6:
            return "high"
        elif combined_score >= 0.4:
            return "medium"
        else:
            return "low" 