#!/usr/bin/env python3
"""
Direct API Client for Flagship LLMs - Updated for 2025 Models
Integrates OpenAI, Anthropic, Mistral, and Google AI APIs with latest model versions
"""

import os
import json
import time
from typing import Dict, Tuple, Any
from dotenv import load_dotenv
from pathlib import Path

# Import cost manager
try:
    from src.utils.cost_manager import CostManager
except ImportError:
    # Fallback if cost manager not available
    CostManager = None

# Load environment variables
load_dotenv()

try:
    import openai
except ImportError:
    print("Installing OpenAI library...")
    os.system("pip install openai")
    import openai

try:
    import anthropic
except ImportError:
    print("Installing Anthropic library...")
    os.system("pip install anthropic")
    import anthropic

try:
    from mistralai.client import MistralClient
except ImportError:
    print("Installing Mistral library...")
    os.system("pip install mistralai")
    from mistralai.client import MistralClient

try:
    import google.generativeai as genai
except ImportError:
    print("Installing Google AI library...")
    os.system("pip install google-generativeai")
    import google.generativeai as genai


class DirectAPIClient:
    """Direct API client for flagship LLMs - Updated with latest 2025 models"""
    
    def __init__(self):
        """Initialize API clients"""
        self.openai_client = None
        self.anthropic_client = None
        self.mistral_client = None
        self.google_ai_client = None
        
        # Initialize cost manager
        self.cost_manager = CostManager() if CostManager else None
        
        # Store current analysis context for quality assurance
        self._current_text = None
        self._current_framework = None
        
        # Initialize retry handler for robust API calls
        try:
            from ..utils.api_retry_handler import APIRetryHandler, ProviderFailoverHandler
            self.retry_handler = APIRetryHandler()
            self.failover_handler = ProviderFailoverHandler()
        except ImportError:
            print("⚠️ Retry handler not available - using basic error handling")
            self.retry_handler = None
            self.failover_handler = None
        
        # Initialize OpenAI
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            self.openai_client = openai.OpenAI(api_key=openai_key)
            print("✅ OpenAI client initialized (2025 models available)")
        else:
            print("⚠️ OpenAI API key not found in environment")
        
        # Initialize Anthropic
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_key:
            self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key)
            print("✅ Anthropic client initialized (Claude 4 series available)")
        else:
            print("⚠️ Anthropic API key not found in environment")
        
        # Initialize Mistral (handle deprecated client gracefully)
        mistral_key = os.getenv("MISTRAL_API_KEY")
        if mistral_key:
            try:
                self.mistral_client = MistralClient(api_key=mistral_key)
                print("✅ Mistral client initialized (2025 models available)")
            except NotImplementedError:
                print("⚠️ Mistral client deprecated - skipping Mistral support")
                self.mistral_client = None
        else:
            print("⚠️ Mistral API key not found in environment")
            self.mistral_client = None
        
        # Initialize Google AI
        google_ai_key = os.getenv("GOOGLE_AI_API_KEY")
        if google_ai_key:
            genai.configure(api_key=google_ai_key)
            self.google_ai_client = genai
            print("✅ Google AI client initialized (Gemini 2.5 series available)")
        else:
            print("⚠️ Google AI API key not found in environment")
    
    def test_connections(self) -> Dict[str, bool]:
        """Test all API connections with latest models"""
        results = {}
        
        # Test OpenAI with GPT-4.1-mini (most cost-effective latest model)
        if self.openai_client:
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[{"role": "user", "content": "Hello"}],
                    max_tokens=5
                )
                results["openai"] = True
                print("✅ OpenAI connection successful (GPT-4.1 series)")
            except Exception as e:
                # Fallback to older model if 4.1 not available yet
                try:
                    response = self.openai_client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": "Hello"}],
                        max_tokens=5
                    )
                    results["openai"] = True
                    print("✅ OpenAI connection successful (fallback model)")
                except Exception as e2:
                    results["openai"] = False
                    print(f"❌ OpenAI connection failed: {e2}")
        else:
            results["openai"] = False
        
        # Test Anthropic with Claude 3.5 Sonnet (current production model)
        if self.anthropic_client:
            try:
                response = self.anthropic_client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=5,
                    messages=[{"role": "user", "content": "Hello"}]
                )
                results["anthropic"] = True
                print("✅ Anthropic connection successful (Claude 3.5 Sonnet)")
            except Exception as e:
                # Fallback to older model
                try:
                    response = self.anthropic_client.messages.create(
                        model="claude-3-haiku-20240307",
                        max_tokens=5,
                        messages=[{"role": "user", "content": "Hello"}]
                    )
                    results["anthropic"] = True
                    print("✅ Anthropic connection successful (fallback model)")
                except Exception as e2:
                    results["anthropic"] = False
                    print(f"❌ Anthropic connection failed: {e2}")
        else:
            results["anthropic"] = False
        
        # Test Mistral with latest production model
        if self.mistral_client:
            try:
                response = self.mistral_client.chat(
                    model="mistral-large-2411",
                    messages=[{"role": "user", "content": "Hello"}],
                    max_tokens=5
                )
                results["mistral"] = True
                print("✅ Mistral connection successful (2024/2025 models)")
            except Exception as e:
                # Fallback to older model
                try:
                    response = self.mistral_client.chat(
                        model="mistral-tiny",
                        messages=[{"role": "user", "content": "Hello"}],
                        max_tokens=5
                    )
                    results["mistral"] = True
                    print("✅ Mistral connection successful (fallback model)")
                except Exception as e2:
                    results["mistral"] = False
                    print(f"❌ Mistral connection failed: {e2}")
        else:
            results["mistral"] = False
            print("⚠️ Mistral client not available (deprecated or no API key)")
        
        # Test Google AI with Gemini 2.0 Flash
        if self.google_ai_client:
            try:
                model = self.google_ai_client.GenerativeModel('gemini-2.0-flash-exp')
                response = model.generate_content("Hello")
                results["google_ai"] = True
                print("✅ Google AI connection successful (Gemini 2.x series)")
            except Exception as e:
                # Fallback to older model
                try:
                    model = self.google_ai_client.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content("Hello")
                    results["google_ai"] = True
                    print("✅ Google AI connection successful (fallback model)")
                except Exception as e2:
                    results["google_ai"] = False
                    print(f"❌ Google AI connection failed: {e2}")
        else:
            results["google_ai"] = False
        
        return results
    
    def analyze_text(self, text: str, framework: str, model_name: str) -> Tuple[Dict[str, Any], float]:
        """
        Analyze text using specified model and framework
        Compatible with existing narrative gravity framework
        """
        # Store context for quality assurance
        self._current_text = text
        self._current_framework = framework
        
        # Import the prompt template manager
        try:
            from src.narrative_gravity.prompts.template_manager import PromptTemplateManager
            template_manager = PromptTemplateManager()
            prompt = template_manager.generate_api_prompt(text, framework, model_name)
        except ImportError as e:
            # Error out instead of using generic fallback
            raise RuntimeError(f"PromptTemplateManager is required for proper analysis but could not be imported: {e}")
        except Exception as e:
            # Error out on any prompt generation failure
            raise RuntimeError(f"Failed to generate proper analysis prompt: {e}")
        
        # Check cost limits before proceeding
        if self.cost_manager:
            provider = self._get_provider_from_model(model_name)
            estimated_cost, _, _ = self.cost_manager.estimate_cost(text, provider, model_name)
            can_proceed, message = self.cost_manager.check_limits_before_request(estimated_cost)
            
            if not can_proceed:
                print(f"🚫 Cost limit check failed: {message}")
                return {"error": f"Cost limit exceeded: {message}"}, 0.0
            else:
                print(f"💰 Estimated cost: ${estimated_cost:.4f} - {message}")
        
        # Route to appropriate model
        if model_name.startswith("gpt") or model_name.startswith("openai"):
            return self._analyze_with_openai(prompt, model_name)
        elif model_name.startswith("claude") or model_name.startswith("anthropic"):
            return self._analyze_with_anthropic(prompt, model_name)
        elif model_name.startswith("mistral"):
            return self._analyze_with_mistral(prompt, model_name)
        elif model_name.startswith("gemini") or model_name.startswith("google"):
            return self._analyze_with_google_ai(prompt, model_name)
        else:
            raise ValueError(f"Unknown model: {model_name}")
    
    def _get_provider_from_model(self, model_name: str) -> str:
        """Get provider name from model name"""
        if any(x in model_name.lower() for x in ["gpt", "openai", "o1", "o3", "o4"]):
            return "openai"
        elif any(x in model_name.lower() for x in ["claude", "anthropic"]):
            return "anthropic"
        elif any(x in model_name.lower() for x in ["mistral", "codestral", "devstral", "saba"]):
            return "mistral"
        elif any(x in model_name.lower() for x in ["gemini", "google"]):
            return "google_ai"
        elif any(x in model_name.lower() for x in ["deepseek", "qwen", "llama"]):
            # For open-source models, we'll use OpenAI-compatible APIs
            # Many hosting services (like Together AI, Fireworks) provide these
            return "openai"  # Use OpenAI client for compatibility
        else:
            return "unknown"
    
    def _analyze_with_openai(self, prompt: str, model_name: str = "gpt-4.1") -> Tuple[Dict[str, Any], float]:
        """Analyze with OpenAI models - Updated for 2025 with retry handling"""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized")
        
        # Updated model mappings for 2025
        model_map = {
            # Legacy mappings
            "gpt-4": "gpt-4.1",
            "gpt-3.5-turbo": "gpt-4.1-mini",
            "openai": "gpt-4.1",
            
            # 2025 GPT-4.1 series (April 2025)
            "gpt-4.1": "gpt-4.1",
            "gpt-4.1-mini": "gpt-4.1-mini", 
            "gpt-4.1-nano": "gpt-4.1-nano",
            
            # o-series reasoning models (2025)
            "o1": "o1",
            "o3": "o3",  
            "o4-mini": "o4-mini",
            
            # GPT-4o variants
            "gpt-4o": "gpt-4o",
            "gpt-4o-mini": "gpt-4o-mini",
            
            # Open-source models (using compatible APIs)
            "deepseek-r1": "gpt-4.1",  # Map to GPT-4.1 for now
            "qwen3-235b": "gpt-4.1",   # Map to GPT-4.1 for now
            "llama-4-scout": "gpt-4.1", # Map to GPT-4.1 for now
            "llama-3.3-70b": "gpt-4.1", # Map to GPT-4.1 for now
            
            # Current production fallbacks
            "gpt-4-turbo": "gpt-4-turbo-2024-04-09",
        }
        
        model = model_map.get(model_name, "gpt-4.1")
        
        # Use retry handler if available, otherwise basic error handling
        if self.retry_handler:
            return self._openai_api_call_with_retry(prompt, model)
        else:
            return self._openai_api_call_basic(prompt, model)
    
    def _openai_api_call_with_retry(self, prompt: str, model: str) -> Tuple[Dict[str, Any], float]:
        """OpenAI API call with retry logic."""
        
        @self.retry_handler.with_retry("openai", model)
        def make_openai_call():
            # Check if model supports extended context for narrative analysis
            max_tokens = 2000
            if "4.1" in model:
                max_tokens = 4000  # GPT-4.1 series supports longer outputs
            elif model.startswith("o"):
                max_tokens = 3000  # o-series optimized for reasoning
                
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.1
            )
            
            content = response.choices[0].message.content
            usage = response.usage
            
            # Calculate cost with updated 2025 pricing
            if "4.1" in model:
                if "mini" in model:
                    cost = (usage.prompt_tokens * 0.00015 / 1000) + (usage.completion_tokens * 0.0006 / 1000)
                elif "nano" in model:
                    cost = (usage.prompt_tokens * 0.0001 / 1000) + (usage.completion_tokens * 0.0004 / 1000)
                else:  # GPT-4.1 standard
                    cost = (usage.prompt_tokens * 0.005 / 1000) + (usage.completion_tokens * 0.015 / 1000)
            elif model.startswith("o"):
                # o-series reasoning models (premium pricing for reasoning)
                if "mini" in model:
                    cost = (usage.prompt_tokens * 0.003 / 1000) + (usage.completion_tokens * 0.012 / 1000)
                else:
                    cost = (usage.prompt_tokens * 0.015 / 1000) + (usage.completion_tokens * 0.06 / 1000)
            elif "4o" in model:
                if "mini" in model:
                    cost = (usage.prompt_tokens * 0.00015 / 1000) + (usage.completion_tokens * 0.0006 / 1000)
                else:
                    cost = (usage.prompt_tokens * 0.0025 / 1000) + (usage.completion_tokens * 0.01 / 1000)
            else:
                # Fallback pricing for older models
                cost = (usage.prompt_tokens * 0.01 / 1000) + (usage.completion_tokens * 0.03 / 1000)
            
            # Record actual cost
            if self.cost_manager:
                self.cost_manager.record_cost(
                    provider="openai",
                    model=model,
                    actual_cost=cost,
                    tokens_input=usage.prompt_tokens,
                    tokens_output=usage.completion_tokens,
                    request_type="analysis"
                )
            
            # Mark provider as healthy on success
            if self.failover_handler:
                self.failover_handler.mark_provider_healthy("openai")
            
            return self._parse_response(content, self._current_text, self._current_framework), cost
        
        return make_openai_call()
    
    def _openai_api_call_basic(self, prompt: str, model: str) -> Tuple[Dict[str, Any], float]:
        """Basic OpenAI API call with simple error handling (fallback)."""
        try:
            # Check if model supports extended context for narrative analysis
            max_tokens = 2000
            if "4.1" in model:
                max_tokens = 4000  # GPT-4.1 series supports longer outputs
            elif model.startswith("o"):
                max_tokens = 3000  # o-series optimized for reasoning
                
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.1
            )
            
            content = response.choices[0].message.content
            
            # Calculate cost with updated 2025 pricing
            usage = response.usage
            
            # Updated pricing for 2025 models (significantly reduced costs)
            if "4.1" in model:
                if "mini" in model:
                    cost = (usage.prompt_tokens * 0.00015 / 1000) + (usage.completion_tokens * 0.0006 / 1000)
                elif "nano" in model:
                    cost = (usage.prompt_tokens * 0.0001 / 1000) + (usage.completion_tokens * 0.0004 / 1000)
                else:  # GPT-4.1 standard
                    cost = (usage.prompt_tokens * 0.005 / 1000) + (usage.completion_tokens * 0.015 / 1000)
            elif model.startswith("o"):
                # o-series reasoning models (premium pricing for reasoning)
                if "mini" in model:
                    cost = (usage.prompt_tokens * 0.003 / 1000) + (usage.completion_tokens * 0.012 / 1000)
                else:
                    cost = (usage.prompt_tokens * 0.015 / 1000) + (usage.completion_tokens * 0.06 / 1000)
            elif "4o" in model:
                if "mini" in model:
                    cost = (usage.prompt_tokens * 0.00015 / 1000) + (usage.completion_tokens * 0.0006 / 1000)
                else:
                    cost = (usage.prompt_tokens * 0.0025 / 1000) + (usage.completion_tokens * 0.01 / 1000)
            else:
                # Fallback pricing for older models
                cost = (usage.prompt_tokens * 0.01 / 1000) + (usage.completion_tokens * 0.03 / 1000)
            
            # Record actual cost
            if self.cost_manager:
                self.cost_manager.record_cost(
                    provider="openai",
                    model=model,
                    actual_cost=cost,
                    tokens_input=usage.prompt_tokens,
                    tokens_output=usage.completion_tokens,
                    request_type="analysis"
                )
            
            return self._parse_response(content, self._current_text, self._current_framework), cost
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return {"error": str(e)}, 0.0
    
    def _analyze_with_anthropic(self, prompt: str, model_name: str = "claude-4-opus") -> Tuple[Dict[str, Any], float]:
        """Analyze with Anthropic models - Updated for 2025"""
        if not self.anthropic_client:
            raise ValueError("Anthropic client not initialized")
        
        # Updated model mappings for 2025
        model_map = {
            # Legacy mappings updated to latest
            "claude": "claude-3-5-sonnet-20241022",
            "claude-3": "claude-3-5-sonnet-20241022",
            "claude-3-sonnet": "claude-3-5-sonnet-20241022",
            "claude-3-haiku": "claude-3-5-haiku-20241022",
            "anthropic": "claude-4-sonnet",
            
            # Claude 4 series (May 2025)
            "claude-4": "claude-4-sonnet",
            "claude-4-opus": "claude-4-opus",
            "claude-4-sonnet": "claude-4-sonnet",
            
            # Claude 3.7 with extended thinking (February 2025)
            "claude-3.7": "claude-3-7-sonnet",
            "claude-3.7-sonnet": "claude-3-7-sonnet",
            
            # Latest Claude 3.5 series
            "claude-3.5-sonnet": "claude-3-5-sonnet-20241022",
            "claude-3.5-haiku": "claude-3-5-haiku-20241022",
            
            # Production models
            "claude-3-5-sonnet-20241022": "claude-3-5-sonnet-20241022",
            "claude-3-5-haiku-20241022": "claude-3-5-haiku-20241022",
        }
        
        model = model_map.get(model_name, "claude-3-5-sonnet-20241022")
        
        try:
            # Adjust max tokens based on model capabilities
            max_tokens = 2000
            if "claude-4" in model:
                max_tokens = 4000  # Claude 4 has enhanced output capabilities
            elif "3.7" in model:
                max_tokens = 3000  # Extended thinking models
                
            response = self.anthropic_client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text
            
            # Calculate cost with updated 2025 pricing
            usage = response.usage
            
            if "claude-4" in model:
                if "opus" in model:
                    # Claude 4 Opus - premium model
                    cost = (usage.input_tokens * 0.025 / 1000) + (usage.output_tokens * 0.125 / 1000)
                else:  # Claude 4 Sonnet
                    cost = (usage.input_tokens * 0.006 / 1000) + (usage.output_tokens * 0.024 / 1000)
            elif "3.7" in model:
                # Claude 3.7 with extended thinking
                cost = (usage.input_tokens * 0.004 / 1000) + (usage.output_tokens * 0.018 / 1000)
            elif "3-5" in model or "3.5" in model:
                if "sonnet" in model:
                    cost = (usage.input_tokens * 0.003 / 1000) + (usage.output_tokens * 0.015 / 1000)
                else:  # haiku
                    cost = (usage.input_tokens * 0.00025 / 1000) + (usage.output_tokens * 0.00125 / 1000)
            else:
                # Fallback for older models
                cost = (usage.input_tokens * 0.003 / 1000) + (usage.output_tokens * 0.015 / 1000)
            
            # Record actual cost
            if self.cost_manager:
                self.cost_manager.record_cost(
                    provider="anthropic",
                    model=model,
                    actual_cost=cost,
                    tokens_input=usage.input_tokens,
                    tokens_output=usage.output_tokens,
                    request_type="analysis"
                )
            
            return self._parse_response(content, self._current_text, self._current_framework), cost
            
        except Exception as e:
            print(f"Anthropic API error: {e}")
            return {"error": str(e)}, 0.0
    
    def _analyze_with_mistral(self, prompt: str, model_name: str = "mistral-medium-3") -> Tuple[Dict[str, Any], float]:
        """Analyze with Mistral models - Updated for 2025"""
        if not self.mistral_client:
            raise ValueError("Mistral client not initialized")
        
        # Updated model mappings for 2025
        model_map = {
            # Legacy mappings updated
            "mistral": "mistral-large-2411",
            "mistral-large": "mistral-large-2411",
            "mistral-medium": "mistral-medium-3",
            "mistral-small": "mistral-small-3.1",
            
            # 2025 Models
            "mistral-medium-3": "mistral-medium-3",  # May 2025 - frontier multimodal
            "mistral-small-3.1": "mistral-small-3.1",  # Latest small model
            "codestral-2501": "codestral-2501",  # January 2025 - coding
            "mistral-ocr-2505": "mistral-ocr-2505",  # May 2025 - OCR
            "mistral-saba-2502": "mistral-saba-2502",  # February 2025 - multilingual
            "devstral-small-2505": "devstral-small-2505",  # May 2025 - software engineering
            
            # Production models
            "mistral-large-2411": "mistral-large-2411",
            "mistral-small-2409": "mistral-small-2409",
        }
        
        model = model_map.get(model_name, "mistral-large-2411")
        
        try:
            # Adjust parameters based on model type
            max_tokens = 2000
            if "medium-3" in model:
                max_tokens = 4000  # Frontier model with enhanced capabilities
            elif "codestral" in model or "devstral" in model:
                max_tokens = 3000  # Coding-optimized models
                
            response = self.mistral_client.chat(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=max_tokens
            )
            
            content = response.choices[0].message.content
            
            # Calculate cost with 2025 pricing
            # Estimate tokens if not provided
            input_tokens = len(prompt.split()) * 1.3
            output_tokens = len(content.split()) * 1.3
            
            if "medium-3" in model:
                # Frontier multimodal model - premium pricing
                cost = (input_tokens * 0.02 / 1000) + (output_tokens * 0.06 / 1000)
            elif "codestral-2501" in model or "devstral" in model:
                # Specialized coding models
                cost = (input_tokens * 0.012 / 1000) + (output_tokens * 0.036 / 1000)
            elif "ocr" in model:
                # OCR service pricing (per operation)
                cost = 0.02  # Flat rate per OCR operation
            elif "saba" in model:
                # Multilingual model
                cost = (input_tokens * 0.008 / 1000) + (output_tokens * 0.024 / 1000)
            elif "large-2411" in model:
                cost = (input_tokens * 0.008 / 1000) + (output_tokens * 0.024 / 1000)
            elif "small" in model:
                cost = (input_tokens * 0.002 / 1000) + (output_tokens * 0.006 / 1000)
            else:
                # Fallback pricing
                cost = (input_tokens * 0.008 / 1000) + (output_tokens * 0.024 / 1000)
            
            # Record actual cost
            if self.cost_manager:
                self.cost_manager.record_cost(
                    provider="mistral",
                    model=model,
                    actual_cost=cost,
                    tokens_input=int(input_tokens),
                    tokens_output=int(output_tokens),
                    request_type="analysis"
                )
            
            return self._parse_response(content, self._current_text, self._current_framework), cost
            
        except Exception as e:
            print(f"Mistral API error: {e}")
            return {"error": str(e)}, 0.0
    
    def _parse_response(self, content: str, text_input: str = None, framework: str = None) -> Dict[str, Any]:
        """Parse LLM response with integrated quality assurance validation - supports both simple and hierarchical formats"""
        # Step 1: Parse the LLM response
        raw_response = {}
        parsed_scores = {}
        
        try:
            # Try to parse as JSON first
            raw_response = json.loads(content)
            
            # Check if it's a hierarchical response (3-stage format)
            if self._is_hierarchical_response(raw_response):
                # Convert hierarchical format to simple format
                parsed_scores = self._extract_hierarchical_scores(raw_response)
                # Create a simplified response in the expected format
                simplified_response = {
                    'scores': parsed_scores,
                    'analysis': raw_response.get('analysis', 'Hierarchical analysis completed'),
                    'hierarchical_details': raw_response  # Keep original for debugging
                }
                raw_response = simplified_response
            else:
                # Handle simple format
                parsed_scores = raw_response.get('scores', {})
                
        except json.JSONDecodeError:
            # Try to extract JSON from code blocks (remove ```json and ```)
            cleaned_content = content.strip()
            if cleaned_content.startswith('```json'):
                cleaned_content = cleaned_content[7:]
            elif cleaned_content.startswith('```'):
                cleaned_content = cleaned_content[3:]
            if cleaned_content.endswith('```'):
                cleaned_content = cleaned_content[:-3]
            cleaned_content = cleaned_content.strip()
            
            try:
                raw_response = json.loads(cleaned_content)
                
                # Check hierarchical format again after cleaning
                if self._is_hierarchical_response(raw_response):
                    parsed_scores = self._extract_hierarchical_scores(raw_response)
                    simplified_response = {
                        'scores': parsed_scores,
                        'analysis': raw_response.get('analysis', 'Hierarchical analysis completed'),
                        'hierarchical_details': raw_response
                    }
                    raw_response = simplified_response
                else:
                    parsed_scores = raw_response.get('scores', {})
                    
            except json.JSONDecodeError:
                # If still not JSON, try to extract structured data
                raw_response = self._extract_narrative_scores(content)
                parsed_scores = raw_response.get('scores', {})
        
        # Step 2: Run Quality Assurance Validation (if context available)
        if text_input and framework and parsed_scores:
            try:
                from ..utils.llm_quality_assurance import validate_llm_analysis
                
                quality_assessment = validate_llm_analysis(
                    text_input=text_input,
                    framework=framework,
                    llm_response=raw_response,
                    parsed_scores=parsed_scores
                )
                
                # Add quality assurance results to response
                raw_response['quality_assurance'] = {
                    'confidence_level': quality_assessment.confidence_level,
                    'confidence_score': quality_assessment.confidence_score,
                    'summary': quality_assessment.summary,
                    'requires_second_opinion': quality_assessment.requires_second_opinion,
                    'anomalies_detected': quality_assessment.anomalies_detected,
                    'validation_timestamp': quality_assessment.quality_metadata['validation_timestamp'],
                    'checks_passed': quality_assessment.quality_metadata['checks_passed'],
                    'total_checks': quality_assessment.quality_metadata['total_checks']
                }
                
                # Log quality issues for monitoring
                if quality_assessment.confidence_level == 'LOW':
                    print(f"🚨 LOW confidence analysis detected: {quality_assessment.summary}")
                elif quality_assessment.requires_second_opinion:
                    print(f"⚠️ Second opinion recommended: {quality_assessment.summary}")
                elif quality_assessment.anomalies_detected:
                    print(f"📊 Anomalies detected: {len(quality_assessment.anomalies_detected)} issues")
                    
                # Issue warnings for critical patterns (Roosevelt 1933 case)
                for check in quality_assessment.individual_checks:
                    if check.check_name == 'default_value_ratio' and not check.passed:
                        print(f"🔴 CRITICAL: High default value ratio detected - {check.message}")
                    elif check.check_name == 'position_calculation' and not check.passed:
                        print(f"🔴 CRITICAL: Suspicious position calculation - {check.message}")
                
            except Exception as qa_error:
                print(f"⚠️ Quality assurance validation failed: {qa_error}")
                # Add minimal quality info to indicate QA failure
                raw_response['quality_assurance'] = {
                    'confidence_level': 'UNKNOWN',
                    'confidence_score': 0.5,
                    'summary': f"Quality validation failed: {str(qa_error)}",
                    'validation_error': str(qa_error)
                }
        
        return raw_response
    
    def _is_hierarchical_response(self, response: Dict[str, Any]) -> bool:
        """Check if response is in hierarchical 3-stage format"""
        hierarchical_keys = {
            'Stage 1 Ranking', 
            'Stage 2 Weights', 
            'Stage 3 Evidence and Scores'
        }
        response_keys = set(response.keys())
        
        # If response contains hierarchical stage keys, it's hierarchical
        return len(hierarchical_keys.intersection(response_keys)) >= 2
    
    def _extract_hierarchical_scores(self, response: Dict[str, Any]) -> Dict[str, float]:
        """Extract scores from hierarchical 3-stage response format"""
        scores = {}
        
        # Try to extract from Stage 3 Evidence and Scores
        stage3 = response.get('Stage 3 Evidence and Scores', {})
        if stage3:
            for well_name, well_data in stage3.items():
                if isinstance(well_data, dict) and 'score' in well_data:
                    try:
                        scores[well_name] = float(well_data['score'])
                    except (ValueError, TypeError):
                        print(f"⚠️ Could not parse score for {well_name}: {well_data}")
        
        # Fallback: try to extract from Stage 2 Weights (convert percentages to 0-1 scale)
        if not scores:
            stage2 = response.get('Stage 2 Weights', {})
            if stage2:
                for well_name, weight in stage2.items():
                    try:
                        # Convert percentage (0-100) to decimal (0-1.0), capped at 1.0
                        score = min(float(weight) / 60.0, 1.0)  # Divide by 60 as per hierarchical template
                        scores[well_name] = score
                    except (ValueError, TypeError):
                        print(f"⚠️ Could not parse weight for {well_name}: {weight}")
        
        return scores
    
    def _extract_narrative_scores(self, content: str) -> Dict[str, Any]:
        """Extract narrative gravity scores from text response"""
        result = {
            "raw_response": content,
            "scores": {},
            "parsed": False
        }
        
        # Try to extract scores using pattern matching
        import re
        
        # Look for score patterns like "Hope: 8.5" or "Hope (8.5)"
        score_patterns = [
            r'(\w+):\s*(\d+\.?\d*)',
            r'(\w+)\s*\((\d+\.?\d*)\)',
            r'(\w+)\s*=\s*(\d+\.?\d*)',
            r'(\w+)\s*-\s*(\d+\.?\d*)'
        ]
        
        for pattern in score_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                for concept, score in matches:
                    try:
                        result["scores"][concept.title()] = float(score)
                        result["parsed"] = True
                    except ValueError:
                        continue
        
        return result
    
    def _analyze_with_google_ai(self, prompt: str, model_name: str = "gemini-2.5-pro") -> Tuple[Dict[str, Any], float]:
        """Analyze with Google AI models - Updated for 2025"""
        if not self.google_ai_client:
            raise ValueError("Google AI client not initialized")
        
        # Updated model mappings for 2025
        model_map = {
            # Legacy mappings updated
            "gemini": "gemini-2-0-flash-exp",
            "gemini-pro": "gemini-2-0-flash-exp",
            "gemini-1.5-flash": "gemini-2-0-flash-exp",
            "gemini-1.5-pro": "gemini-2-0-flash-exp",
            "google": "gemini-2-0-flash-exp",
            
            # Gemini 2.5 series (2025)
            "gemini-2.5-pro": "gemini-2-5-pro-preview",  # June 2025 - most intelligent
            "gemini-2.5-flash": "gemini-2-5-flash-preview",  # May 2025 - adaptive thinking
            
            # Gemini 2.0 series
            "gemini-2.0-flash": "gemini-2-0-flash-exp",
            "gemini-2.0-pro": "gemini-2-0-flash-exp",
            
            # Production models (current availability)
            "gemini-2-0-flash-exp": "gemini-2-0-flash-exp",
            "gemini-2-5-pro-preview": "gemini-2-5-pro-preview",
            "gemini-2-5-flash-preview": "gemini-2-5-flash-preview",
        }
        
        model = model_map.get(model_name, "gemini-2-0-flash-exp")
        
        try:
            # Create model instance with advanced configuration
            generation_config = {
                "temperature": 0.1,
                "max_output_tokens": 4000 if "2.5" in model else 2000,
            }
            
            # For Gemini 2.5, enable Deep Think reasoning
            if "2.5" in model:
                generation_config["reasoning_budget"] = "high"  # Enable adaptive thinking
            
            ai_model = self.google_ai_client.GenerativeModel(
                model_name=model,
                generation_config=generation_config
            )
            
            # Generate content
            response = ai_model.generate_content(prompt)
            content = response.text
            
            # Calculate cost with 2025 pricing
            input_chars = len(prompt)
            output_chars = len(content)
            
            if "2.5-pro" in model:
                # Gemini 2.5 Pro - premium with Deep Think
                cost = (input_chars * 0.002 / 1000) + (output_chars * 0.008 / 1000)
            elif "2.5-flash" in model:
                # Gemini 2.5 Flash - adaptive thinking
                cost = (input_chars * 0.001 / 1000) + (output_chars * 0.004 / 1000)
            elif "2.0" in model or "2-0" in model:
                # Gemini 2.0 series
                cost = (input_chars * 0.0008 / 1000) + (output_chars * 0.003 / 1000)
            else:
                # Fallback pricing
                cost = (input_chars * 0.0005 / 1000) + (output_chars * 0.0015 / 1000)
            
            # Estimate tokens for recording (chars / 4 approximate)
            input_tokens = input_chars // 4
            output_tokens = output_chars // 4
            
            # Record actual cost
            if self.cost_manager:
                self.cost_manager.record_cost(
                    provider="google_ai",
                    model=model,
                    actual_cost=cost,
                    tokens_input=input_tokens,
                    tokens_output=output_tokens,
                    request_type="analysis"
                )
            
            return self._parse_response(content, self._current_text, self._current_framework), cost
            
        except Exception as e:
            print(f"Google AI API error: {e}")
            return {"error": str(e)}, 0.0
    
    def get_available_models(self) -> Dict[str, list]:
        """Get list of available models - Updated for 2025"""
        models = {}
        
        if self.openai_client:
            models["openai"] = [
                # 2025 GPT-4.1 series (April 2025) - Recommended
                "gpt-4.1",
                "gpt-4.1-mini", 
                "gpt-4.1-nano",
                
                # o-series reasoning models (2025)
                "o1",
                "o3",  
                "o4-mini",
                
                # GPT-4o variants (current production)
                "gpt-4o",
                "gpt-4o-mini",
                
                # Legacy support
                "gpt-4-turbo",
            ]
        
        if self.anthropic_client:
            models["anthropic"] = [
                # Claude 4 series (May 2025) - Recommended
                "claude-4-opus",
                "claude-4-sonnet",
                
                # Claude 3.7 with extended thinking (February 2025)
                "claude-3.7-sonnet",
                
                # Latest Claude 3.5 series (current production)
                "claude-3.5-sonnet",
                "claude-3.5-haiku",
                
                # Legacy support
                "claude-3-5-sonnet-20241022",
                "claude-3-5-haiku-20241022",
            ]
        
        if self.mistral_client:
            models["mistral"] = [
                # 2025 Models - Recommended
                "mistral-medium-3",      # May 2025 - frontier multimodal
                "codestral-2501",        # January 2025 - coding
                "devstral-small-2505",   # May 2025 - software engineering
                "mistral-saba-2502",     # February 2025 - multilingual
                "mistral-ocr-2505",      # May 2025 - OCR service
                
                # Production models
                "mistral-large-2411",
                "mistral-small-2409",
            ]
        
        if self.google_ai_client:
            models["google_ai"] = [
                # Gemini 2.5 series (2025) - Recommended
                "gemini-2.5-pro",        # June 2025 - most intelligent with Deep Think
                "gemini-2.5-flash",      # May 2025 - adaptive thinking
                
                # Gemini 2.0 series (current production)
                "gemini-2.0-flash",
                "gemini-2.0-pro",
                
                # Legacy support
                "gemini-1.5-flash",
                "gemini-1.5-pro",
            ]
        
        return {k: v for k, v in models.items() if v}  # Only return providers with models
    
    def get_retry_statistics(self) -> Dict[str, Any]:
        """Get comprehensive retry and reliability statistics."""
        stats = {
            'retry_handler_available': self.retry_handler is not None,
            'failover_handler_available': self.failover_handler is not None
        }
        
        if self.retry_handler:
            retry_stats = self.retry_handler.get_retry_stats()
            stats.update(retry_stats)
        
        if self.failover_handler:
            health_status = self.failover_handler.get_health_status()
            stats['provider_health'] = health_status
        
        return stats
    
    def log_reliability_report(self):
        """Log comprehensive reliability report."""
        print("\n📊 DIRECTAPICLIENT RELIABILITY REPORT")
        print("=" * 50)
        
        stats = self.get_retry_statistics()
        
        if stats['retry_handler_available']:
            print(f"✅ Retry Handler: Active")
            print(f"   Total API calls: {stats.get('total_calls', 0)}")
            print(f"   Success rate: {stats.get('success_rate', 0):.1%}")
            print(f"   Retry rate: {stats.get('retry_rate', 0):.1%}")
            
            if stats.get('retries_by_reason'):
                print("   Retries by reason:")
                for reason, count in stats['retries_by_reason'].items():
                    print(f"     {reason}: {count}")
        else:
            print("⚠️ Retry Handler: Not available (basic error handling)")
        
        if stats['failover_handler_available']:
            provider_health = stats['provider_health']
            print(f"✅ Failover Handler: Active")
            print(f"   Healthy providers: {len(provider_health['healthy_providers'])}")
            for provider, healthy in provider_health['provider_health'].items():
                status = "✅ Healthy" if healthy else "❌ Unhealthy"
                failures = provider_health['failure_counts'].get(provider, 0)
                print(f"     {provider}: {status} ({failures} failures)")
        else:
            print("⚠️ Failover Handler: Not available")
        
        print("=" * 50) 