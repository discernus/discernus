"""
Enhanced Hugging Face Client for Narrative Gravity Analysis
Integrates with framework system to provide LLM-powered narrative analysis.
"""

import os
import json
import time
import requests
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from pathlib import Path

from src.prompts.template_manager import PromptTemplateManager

logger = logging.getLogger(__name__)

class HuggingFaceClient:
    """
    Enhanced Hugging Face client for narrative gravity analysis.
    
    Features:
    - Framework-aware prompt generation
    - Automatic retry with exponential backoff
    - Cost tracking and rate limiting
    - Response validation and score extraction
    """
    
    def __init__(self):
        self.api_key = os.getenv('HUGGINGFACE_API_KEY', '')
        self.base_url = "https://api-inference.huggingface.co/models"
        self.frameworks_path = Path("frameworks")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })
        
        # Load framework configurations
        self.frameworks = self._load_frameworks()
        
        # Initialize template manager for sophisticated prompt generation
        self.template_manager = PromptTemplateManager()
        
    def _load_frameworks(self) -> Dict[str, Dict[str, Any]]:
        """Load all available frameworks."""
        frameworks = {}
        
        if not self.frameworks_path.exists():
            logger.warning(f"Frameworks directory not found: {self.frameworks_path}")
            return frameworks
            
        for framework_dir in self.frameworks_path.iterdir():
            if framework_dir.is_dir():
                framework_name = framework_dir.name
                
                # Load dipoles.json and framework.json
                dipoles_file = framework_dir / "dipoles.json"
                framework_file = framework_dir / "framework.json"
                
                if dipoles_file.exists() and framework_file.exists():
                    try:
                        with open(dipoles_file) as f:
                            dipoles = json.load(f)
                        with open(framework_file) as f:
                            framework_config = json.load(f)
                            
                        frameworks[framework_name] = {
                            "dipoles": dipoles,
                            "framework": framework_config
                        }
                        logger.info(f"Loaded framework: {framework_name}")
                        
                    except Exception as e:
                        logger.error(f"Failed to load framework {framework_name}: {e}")
                        
        return frameworks
    
    def analyze_text(self, text: str, framework: str, model: str) -> Tuple[Dict[str, Any], float]:
        """
        Analyze text using specified framework and model.
        
        Args:
            text: Text to analyze
            framework: Framework name (civic_virtue, political_spectrum, etc.)
            model: Hugging Face model name
            
        Returns:
            Tuple of (analysis_result, api_cost)
        """
        if framework not in self.frameworks:
            raise ValueError(f"Unknown framework: {framework}. Available: {list(self.frameworks.keys())}")
        
        # Generate framework-specific prompt using template manager
        prompt = self.template_manager.generate_api_prompt(text, framework, model)
        
        # Call LLM with retry logic
        raw_response = self._call_llm_with_retry(model, prompt)
        
        # Extract and validate scores
        scores = self._extract_framework_scores(raw_response, framework)
        
        # Calculate API cost
        api_cost = self._estimate_cost(text, model)
        
        # Prepare analysis result
        analysis_result = {
            "framework": framework,
            "model": model,
            "text_length": len(text),
            "scores": scores,
            "raw_response": raw_response,
            "prompt_used": prompt[:200] + "..." if len(prompt) > 200 else prompt,
            "processed_at": datetime.utcnow().isoformat(),
            "api_cost": api_cost
        }
        
        return analysis_result, api_cost
    
    def analyze_text_experimental(self, text: str, framework: str, model: str, 
                                 experiment_id: str, variant: str) -> Tuple[Dict[str, Any], float]:
        """
        Analyze text using experimental prompt variations for A/B testing.
        
        Args:
            text: Text to analyze
            framework: Framework name
            model: Hugging Face model name
            experiment_id: Experiment identifier
            variant: Prompt variant to use
            
        Returns:
            Tuple of (analysis_result, api_cost)
        """
        if framework not in self.frameworks:
            raise ValueError(f"Unknown framework: {framework}. Available: {list(self.frameworks.keys())}")
        
        # Generate experimental prompt
        prompt = self.template_manager.generate_experimental_prompt(text, framework, experiment_id, variant)
        
        # Call LLM with retry logic
        raw_response = self._call_llm_with_retry(model, prompt)
        
        # Extract and validate scores
        scores = self._extract_framework_scores(raw_response, framework)
        
        # Calculate API cost
        api_cost = self._estimate_cost(text, model)
        
        # Prepare analysis result with experimental metadata
        analysis_result = {
            "framework": framework,
            "model": model,
            "text_length": len(text),
            "scores": scores,
            "raw_response": raw_response,
            "prompt_used": prompt[:200] + "..." if len(prompt) > 200 else prompt,
            "processed_at": datetime.utcnow().isoformat(),
            "api_cost": api_cost,
            "experiment_id": experiment_id,
            "variant": variant
        }
        
        return analysis_result, api_cost
    
    def _generate_framework_prompt(self, text: str, framework: str) -> str:
        """Generate framework-specific analysis prompt."""
        framework_config = self.frameworks[framework]
        dipoles = framework_config["dipoles"]["dipoles"]
        
        # Build well descriptions
        well_descriptions = []
        for dipole in dipoles:
            positive = dipole["positive"]
            negative = dipole["negative"]
            
            well_descriptions.append(f"""
{positive['name']}: {positive['description']}
Language cues: {', '.join(positive.get('language_cues', [])[:3])}

{negative['name']}: {negative['description']}  
Language cues: {', '.join(negative.get('language_cues', [])[:3])}
""")
        
        # Create the prompt
        prompt = f"""You are analyzing text for narrative gravity using the {framework} framework.

FRAMEWORK WELLS:
{''.join(well_descriptions)}

TASK: Analyze the following text and provide scores from 0.0 to 1.0 for each well, indicating how strongly the text aligns with that narrative gravity well.

IMPORTANT: 
- Use decimal scores between 0.0 and 1.0 only
- Higher scores indicate stronger alignment
- Provide brief justification for each score

TEXT TO ANALYZE:
{text}

RESPONSE FORMAT (JSON):
{{
  "scores": {{
    "{dipoles[0]['positive']['name']}": 0.0,
    "{dipoles[0]['negative']['name']}": 0.0,
    etc...
  }},
  "analysis": "Brief explanation of scoring rationale"
}}"""

        return prompt
    
    def _call_llm_with_retry(self, model: str, prompt: str, max_retries: int = 3) -> Dict[str, Any]:
        """Call LLM API with retry logic and exponential backoff."""
        url = f"{self.base_url}/{model}"
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 500,
                "temperature": 0.1,
                "top_p": 0.9,
                "do_sample": True
            }
        }
        
        for attempt in range(max_retries):
            try:
                response = self.session.post(url, json=payload, timeout=30)
                
                # Handle rate limiting
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 60))
                    if attempt < max_retries - 1:
                        logger.warning(f"Rate limited. Waiting {retry_after}s before retry {attempt + 1}")
                        time.sleep(retry_after)
                        continue
                    else:
                        raise Exception(f"Rate limited after {max_retries} attempts")
                
                # Handle server errors
                if response.status_code >= 500:
                    if attempt < max_retries - 1:
                        wait_time = (2 ** attempt) * 5  # Exponential backoff
                        logger.warning(f"Server error {response.status_code}. Waiting {wait_time}s before retry {attempt + 1}")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise Exception(f"Server error {response.status_code} after {max_retries} attempts")
                
                # Handle client errors (don't retry)
                if response.status_code >= 400:
                    raise Exception(f"Client error {response.status_code}: {response.text}")
                
                response.raise_for_status()
                result = response.json()
                
                # Handle different response formats
                if isinstance(result, list) and len(result) > 0:
                    return result[0]
                elif isinstance(result, dict):
                    return result
                else:
                    raise Exception(f"Unexpected response format: {type(result)}")
                    
            except requests.RequestException as e:
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) * 5
                    logger.warning(f"Request failed: {e}. Waiting {wait_time}s before retry {attempt + 1}")
                    time.sleep(wait_time)
                    continue
                else:
                    raise Exception(f"Request failed after {max_retries} attempts: {e}")
        
        raise Exception("Max retries exceeded")
    
    def _extract_framework_scores(self, llm_response: Dict[str, Any], framework: str) -> Dict[str, float]:
        """Extract and validate scores from LLM response."""
        framework_config = self.frameworks[framework]
        dipoles = framework_config["dipoles"]["dipoles"]
        
        # Get all expected well names
        expected_wells = set()
        for dipole in dipoles:
            expected_wells.add(dipole["positive"]["name"])
            expected_wells.add(dipole["negative"]["name"])
        
        scores = {}
        
        try:
            # Try to extract JSON from response
            response_text = llm_response.get("generated_text", "")
            if not response_text:
                response_text = str(llm_response)
            
            # Look for JSON in the response
            json_start = response_text.find("{")
            json_end = response_text.rfind("}") + 1
            
            if json_start >= 0 and json_end > json_start:
                json_text = response_text[json_start:json_end]
                parsed = json.loads(json_text)
                
                # Extract scores
                if "scores" in parsed:
                    for well_name, score in parsed["scores"].items():
                        if well_name in expected_wells:
                            # Validate and normalize score
                            if isinstance(score, (int, float)):
                                # Convert 1-10 scale to 0-1 scale if needed
                                if score > 1.0:
                                    score = score / 10.0
                                scores[well_name] = max(0.0, min(1.0, float(score)))
                            
        except Exception as e:
            logger.warning(f"Failed to parse LLM response as JSON: {e}")
        
        # Fill in missing scores with defaults
        for well_name in expected_wells:
            if well_name not in scores:
                scores[well_name] = 0.0
                logger.warning(f"Missing score for {well_name}, defaulting to 0.0")
        
        return scores
    
    def _estimate_cost(self, text: str, model: str) -> float:
        """Estimate API cost based on text length and model."""
        # Rough cost estimation - adjust based on actual pricing
        base_cost = 0.001  # Base cost per request
        
        # Character-based pricing (very rough estimate)
        char_cost = len(text) * 0.00001  # $0.00001 per character
        
        # Model-specific multipliers
        model_multipliers = {
            "gpt-3.5-turbo": 1.0,
            "gpt-4": 10.0,
            "claude": 5.0,
            "distilbert": 0.1,  # Much cheaper for simpler models
        }
        
        multiplier = 1.0
        for model_pattern, mult in model_multipliers.items():
            if model_pattern.lower() in model.lower():
                multiplier = mult
                break
        
        return (base_cost + char_cost) * multiplier
    
    def get_available_frameworks(self) -> List[str]:
        """Get list of available frameworks."""
        return list(self.frameworks.keys())
    
    def validate_framework_config(self, framework: str) -> Tuple[bool, str]:
        """Validate framework configuration."""
        if framework not in self.frameworks:
            return False, f"Framework {framework} not found"
        
        config = self.frameworks[framework]
        
        # Check required components
        if "dipoles" not in config or "framework" not in config:
            return False, "Missing dipoles or framework configuration"
        
        dipoles = config["dipoles"].get("dipoles", [])
        if not dipoles:
            return False, "No dipoles defined"
        
        wells = config["framework"].get("wells", {})
        if not wells:
            return False, "No wells defined in framework"
        
        # Check consistency between dipoles and wells
        expected_wells = set()
        for dipole in dipoles:
            expected_wells.add(dipole["positive"]["name"])
            expected_wells.add(dipole["negative"]["name"])
        
        actual_wells = set(wells.keys())
        
        if expected_wells != actual_wells:
            missing = expected_wells - actual_wells
            extra = actual_wells - expected_wells
            return False, f"Well mismatch. Missing: {missing}, Extra: {extra}"
        
        return True, "Framework configuration valid"


# Convenience functions for backward compatibility
def analyze_civic_virtue(text: str, model: str) -> Tuple[Dict[str, Any], float]:
    """Analyze text for civic virtue using Hugging Face models."""
    client = HuggingFaceClient()
    return client.analyze_text(text, "civic_virtue", model)

def analyze_moral_rhetorical_posture(text: str, model: str) -> Tuple[Dict[str, Any], float]:
    """Analyze text for moral rhetorical posture using Hugging Face models.""" 
    client = HuggingFaceClient()
    return client.analyze_text(text, "moral_rhetorical_posture", model)

def analyze_political_spectrum(text: str, model: str) -> Tuple[Dict[str, Any], float]:
    """Analyze text for political spectrum positioning using Hugging Face models."""
    client = HuggingFaceClient()
    return client.analyze_text(text, "political_spectrum", model) 