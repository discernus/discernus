"""
Prompt Template Manager - Minimal implementation for analysis service
"""

from typing import Dict, Any, Optional
from enum import Enum
import json


class PromptMode(Enum):
    """Prompt generation modes"""
    API = "api"
    INTERACTIVE = "interactive"
    EXPERIMENTAL = "experimental"


class PromptTemplateManager:
    """
    Minimal prompt template manager for analysis service functionality.
    This is a basic implementation to fix import errors and get the pipeline working.
    """
    
    def __init__(self):
        self.templates = {}
        
    def generate_api_prompt(self, text: str, framework: str, model_name: str = None, model: str = None) -> str:
        """Generate API prompt for text analysis"""
        
        # Handle both parameter names
        model_name = model_name or model or "gpt-4o"
        
        # Basic prompt template for moral foundations theory
        if framework == "moral_foundations_theory":
            prompt = f"""
Analyze the following text using Moral Foundations Theory. Score each foundation from 0.0 to 1.0:

FOUNDATIONS TO ANALYZE:
- Care/Harm: Concern for suffering and protection of vulnerable
- Fairness/Cheating: Justice, reciprocity, and proportionality  
- Loyalty/Betrayal: Commitment to group, patriotism, sacrifice
- Authority/Subversion: Respect for hierarchy, tradition, leadership
- Sanctity/Degradation: Reverence, purity, spiritual significance
- Liberty/Oppression: Freedom from control and domination

SCORING SCALE:
- 0.0: Foundation completely absent from text
- 0.1-0.3: Minimal presence - weak or indirect references  
- 0.4-0.6: Moderate presence - clear but not central to argument
- 0.7-0.9: Strong presence - central to text's moral reasoning
- 1.0: Dominant presence - primary moral framework of text

TEXT TO ANALYZE:
{text}

RESPONSE FORMAT (JSON):
{{
    "care_harm": {{ "score": 0.0, "evidence": "quote from text", "reasoning": "explanation" }},
    "fairness_cheating": {{ "score": 0.0, "evidence": "quote from text", "reasoning": "explanation" }},
    "loyalty_betrayal": {{ "score": 0.0, "evidence": "quote from text", "reasoning": "explanation" }},
    "authority_subversion": {{ "score": 0.0, "evidence": "quote from text", "reasoning": "explanation" }},
    "sanctity_degradation": {{ "score": 0.0, "evidence": "quote from text", "reasoning": "explanation" }},
    "liberty_oppression": {{ "score": 0.0, "evidence": "quote from text", "reasoning": "explanation" }},
    "overall_analysis": "summary of moral foundations profile",
    "confidence": 0.85
}}

Provide only valid JSON in your response.
"""
        else:
            # Generic analysis prompt
            prompt = f"""
Analyze the following text using the {framework} framework.

TEXT TO ANALYZE:
{text}

Provide your analysis in JSON format with appropriate scores and evidence.
"""
        
        return prompt
    
    def generate_interactive_prompt(self, framework_name: str) -> str:
        """Generate interactive prompt for a framework"""
        return f"Interactive analysis prompt for {framework_name}"
    
    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """Get template by ID"""
        return self.templates.get(template_id)
    
    def list_templates(self) -> Dict[str, Any]:
        """List available templates"""
        return {
            "moral_foundations_analysis": {
                "name": "Moral Foundations Analysis",
                "framework": "moral_foundations_theory",
                "type": "api"
            }
        } 