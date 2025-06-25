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
import sys

# Add project root to path for TPM rate limiter import
project_root = os.path.join(os.path.dirname(__file__), '..', '..')
if project_root not in sys.path:
    sys.path.append(project_root)

try:
    from experimental.prototypes.tpm_rate_limiter import TPMRateLimiter
    TPM_RATE_LIMITER_AVAILABLE = True
except ImportError:
    TPM_RATE_LIMITER_AVAILABLE = False

# Import cost manager
try:
    from src.utils.cost_manager import CostManager
except ImportError:
    # Fallback if cost manager not available
    CostManager = None

# Load environment variables
load_dotenv()


from .providers.openai_client import OpenAIProvider
from .providers.anthropic_client import AnthropicProvider
from .providers.mistral_client import MistralProvider
from .providers.google_client import GoogleAIProvider


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
        
        # Add rate limiting to be polite to APIs
        self._last_request_time = {}
        self._rate_limits = {
            'openai': 2.0,     # 2 seconds between requests (more polite)
            'anthropic': 1.5,   # 1.5 seconds between requests 
            'mistral': 1.0,     # 1 second between requests
            'google_ai': 1.0    # 1 second between requests
        }
        
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
            self.openai_client = OpenAIProvider(openai_key, self.cost_manager)
            print("✅ OpenAI client initialized (2025 models available)")
        else:
            print("⚠️ OpenAI API key not found in environment")
        
        # Initialize Anthropic
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_key:
            self.anthropic_client = AnthropicProvider(anthropic_key, self.cost_manager)
            print("✅ Anthropic client initialized (Claude 4 series available)")
        else:
            print("⚠️ Anthropic API key not found in environment")
        
        # Initialize Mistral
        mistral_key = os.getenv("MISTRAL_API_KEY")
        if mistral_key:
            try:
                self.mistral_client = MistralProvider(mistral_key, self.cost_manager)
                print("✅ Mistral client initialized (latest models available)")
            except Exception as e:
                print(f"⚠️ Mistral client initialization failed: {e}")
                self.mistral_client = None
        else:
            print("⚠️ Mistral API key not found in environment")
            self.mistral_client = None
        
        # Initialize Google AI
        google_ai_key = os.getenv("GOOGLE_AI_API_KEY")
        if google_ai_key:
            self.google_ai_client = GoogleAIProvider(google_ai_key, self.cost_manager)
            print("✅ Google AI client initialized (Gemini 2.5 series available)")
        else:
            print("⚠️ Google AI API key not found in environment")
        
        # Initialize TPM rate limiter if available
        if TPM_RATE_LIMITER_AVAILABLE:
            self.tpm_limiter = TPMRateLimiter()
            print("✅ TPM Rate Limiter initialized")
        else:
            self.tpm_limiter = None
            print("⚠️ TPM Rate Limiter not available - rate limiting disabled")
    
    def test_connections(self) -> Dict[str, bool]:
        """Test all API connections with latest models"""
        results = {}
        
        # Test OpenAI with GPT-4.1-mini (most cost-effective latest model)
        if self.openai_client:
            try:
                response = self.openai_client.client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[{"role": "user", "content": "Hello"}],
                    max_tokens=5
                )
                results["openai"] = True
                print("✅ OpenAI connection successful (GPT-4.1 series)")
            except Exception as e:
                # Fallback to older model if 4.1 not available yet
                try:
                    response = self.openai_client.client.chat.completions.create(
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
                response = self.anthropic_client.client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=5,
                    messages=[{"role": "user", "content": "Hello"}]
                )
                results["anthropic"] = True
                print("✅ Anthropic connection successful (Claude 3.5 Sonnet)")
            except Exception as e:
                # Fallback to older model
                try:
                    response = self.anthropic_client.client.messages.create(
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
                response = self.mistral_client.client.chat.complete(
                    model="mistral-large-latest",
                    messages=[{"role": "user", "content": "Hello"}],
                    max_tokens=5
                )
                results["mistral"] = True
                print("✅ Mistral connection successful (latest models)")
            except Exception as e:
                # Fallback to small model
                try:
                    response = self.mistral_client.client.chat.complete(
                        model="mistral-small-latest",
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
            print("⚠️ Mistral client not available (no API key)")
        
        # Test Google AI with Gemini 2.5 Flash (confirmed working)
        if self.google_ai_client:
            try:
                model = self.google_ai_client.client.GenerativeModel('gemini-2.5-flash')
                response = model.generate_content("Hello")
                results["google_ai"] = True
                print("✅ Google AI connection successful (Gemini 2.5 series)")
            except Exception as e:
                # Fallback to older model
                try:
                    model = self.google_ai_client.client.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content("Hello")
                    results["google_ai"] = True
                    print("✅ Google AI connection successful (fallback model)")
                except Exception as e2:
                    results["google_ai"] = False
                    print(f"❌ Google AI connection failed: {e2}")
        else:
            results["google_ai"] = False
        
        return results
    
    def _enforce_rate_limit(self, provider: str):
        """Enforce rate limiting to be polite to API providers"""
        current_time = time.time()
        
        if provider in self._last_request_time:
            time_since_last = current_time - self._last_request_time[provider]
            required_delay = self._rate_limits.get(provider, 1.0)
            
            if time_since_last < required_delay:
                sleep_time = required_delay - time_since_last
                print(f"💤 Rate limiting: waiting {sleep_time:.1f}s for {provider}")
                time.sleep(sleep_time)
        
        self._last_request_time[provider] = time.time()
    
    def analyze_text(self, text: str, framework: str, model_name: str) -> Tuple[Dict[str, Any], float]:
        """
        Analyze text using specified model and framework
        Compatible with existing narrative gravity framework
        🚀 ENHANCED: Now includes TPM-aware rate limiting
        """
        # Store context for quality assurance
        self._current_text = text
        self._current_framework = framework
        
        # Import the prompt template manager
        try:
            from src.prompts.template_manager import PromptTemplateManager
            template_manager = PromptTemplateManager()
            prompt = template_manager.generate_api_prompt(text, framework, model_name)
        except ImportError as e:
            # Error out instead of using generic fallback
            raise RuntimeError(f"PromptTemplateManager is required for proper analysis but could not be imported: {e}")
        except Exception as e:
            # Error out on any prompt generation failure
            raise RuntimeError(f"Failed to generate proper analysis prompt: {e}")
        
        # 🚀 NEW: TPM Rate Limiting Logic
        if self.tpm_limiter:
            try:
                # Estimate tokens for the full prompt (text + framework + instructions)
                estimated_tokens = self.tpm_limiter.estimate_tokens(prompt, model_name)
                
                print(f"🔍 TPM Check: {model_name} - {estimated_tokens:,} tokens estimated")
                
                # Wait if needed to respect TPM limits
                can_proceed = self.tpm_limiter.wait_if_needed(
                    model=model_name, 
                    estimated_tokens=estimated_tokens,
                    prompt_text=text[:200]  # Preview for debugging
                )
                
                if not can_proceed:
                    print("🚫 TPM rate limiting cancelled the request")
                    return {"error": "TPM rate limiting cancelled request"}, 0.0
                    
            except Exception as tpm_error:
                print(f"⚠️ TPM rate limiting failed: {tpm_error}")
                print("🔄 Continuing without TPM protection...")
        
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
        start_time = time.time()
        
        if model_name.startswith("gpt") or model_name.startswith("openai"):
            result, cost = self._analyze_with_openai(prompt, model_name)
        elif model_name.startswith("claude") or model_name.startswith("anthropic"):
            result, cost = self._analyze_with_anthropic(prompt, model_name)
        elif model_name.startswith("mistral"):
            result, cost = self._analyze_with_mistral(prompt, model_name)
        elif model_name.startswith("gemini") or model_name.startswith("google"):
            result, cost = self._analyze_with_google_ai(prompt, model_name)
        elif model_name.startswith("ollama/"):
            result, cost = self._analyze_with_ollama(prompt, model_name)
        else:
            # Try to determine provider by model name
            provider = self._get_provider_from_model(model_name)
            if provider == "openai":
                result, cost = self._analyze_with_openai(prompt, model_name)
            elif provider == "anthropic":
                result, cost = self._analyze_with_anthropic(prompt, model_name)
            elif provider == "mistral":
                result, cost = self._analyze_with_mistral(prompt, model_name)
            elif provider == "google_ai":
                result, cost = self._analyze_with_google_ai(prompt, model_name)
            else:
                raise ValueError(f"Unknown model: {model_name}. Supported providers: openai, anthropic, mistral, google_ai, ollama")
        
        # 🚀 NEW: Record actual token usage for TPM tracking
        if self.tpm_limiter and 'error' not in result:
            try:
                # Estimate tokens used (input + output)
                response_text = result.get('raw_response', '')
                output_tokens = self.tpm_limiter.estimate_tokens(response_text, model_name)
                total_tokens = estimated_tokens + output_tokens
                
                # Record usage for future rate limiting
                self.tpm_limiter.record_usage(model_name, total_tokens)
                
                end_time = time.time()
                duration = end_time - start_time
                
                print(f"✅ TPM Tracking: {model_name} used {total_tokens:,} tokens in {duration:.1f}s")
                
                # Add TPM info to result for monitoring
                if 'tpm_info' not in result:
                    result['tpm_info'] = {}
                result['tpm_info']['estimated_input_tokens'] = estimated_tokens
                result['tpm_info']['estimated_output_tokens'] = output_tokens
                result['tpm_info']['total_tokens'] = total_tokens
                result['tpm_info']['model'] = model_name
                
            except Exception as tracking_error:
                print(f"⚠️ TPM usage tracking failed: {tracking_error}")
        
        return result, cost
    
    def _get_provider_from_model(self, model_name: str) -> str:
        """Get provider name from model name"""
        if model_name.startswith("ollama/"):
            return "ollama"
        elif any(x in model_name.lower() for x in ["gpt", "openai", "o1", "o3", "o4"]):
            return "openai"
        elif any(x in model_name.lower() for x in ["claude", "anthropic"]):
            return "anthropic"
        elif any(x in model_name.lower() for x in ["mistral", "codestral", "devstral", "saba"]):
            return "mistral"
        elif any(x in model_name.lower() for x in ["gemini", "google"]):
            return "google_ai"
        elif any(x in model_name.lower() for x in ["deepseek", "qwen", "llama"]):
            # For open-source models hosted on cloud services
            # Many hosting services (like Together AI, Fireworks) provide these
            return "openai"  # Use OpenAI client for compatibility
        else:
            return "unknown"
    
    def _analyze_with_openai(self, prompt: str, model_name: str = "gpt-4.1") -> Tuple[Dict[str, Any], float]:
        """Analyze with OpenAI models via provider class."""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized")

        # Use retry handler if available, otherwise basic error handling
        if self.retry_handler:
            return self._openai_api_call_with_retry_provider(prompt, model_name)
        else:
            return self._openai_api_call_basic_provider(prompt, model_name)
    
    def _openai_api_call_with_retry_provider(self, prompt: str, model: str) -> Tuple[Dict[str, Any], float]:
        """OpenAI API call with retry logic using provider."""
        
        # Enforce polite rate limiting before making request
        self._enforce_rate_limit("openai")
        
        @self.retry_handler.with_retry("openai", model)
        def make_openai_call():
            content, cost, _ = self.openai_client._analyze(prompt, model)
            
            # Mark provider as healthy on success
            if self.failover_handler:
                self.failover_handler.mark_provider_healthy("openai")
            
            return self._parse_response(content, self._current_text, self._current_framework), cost
        
        return make_openai_call()
    
    def _openai_api_call_basic_provider(self, prompt: str, model: str) -> Tuple[Dict[str, Any], float]:
        """Basic OpenAI API call with simple error handling using provider."""
        self._enforce_rate_limit("openai")
        
        try:
            content, cost, _ = self.openai_client._analyze(prompt, model)
            return self._parse_response(content, self._current_text, self._current_framework), cost
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return {"error": str(e)}, 0.0
    
    def _analyze_with_anthropic(self, prompt: str, model_name: str = "claude-4-opus") -> Tuple[Dict[str, Any], float]:
        """Analyze with Anthropic models via provider class."""
        if not self.anthropic_client:
            raise ValueError("Anthropic client not initialized")

        # Use retry handler if available, otherwise basic error handling
        if self.retry_handler:
            return self._anthropic_api_call_with_retry_provider(prompt, model_name)
        else:
            return self._anthropic_api_call_basic_provider(prompt, model_name)
    
    def _anthropic_api_call_with_retry_provider(self, prompt: str, model: str) -> Tuple[Dict[str, Any], float]:
        """Anthropic API call with retry logic using provider."""
        
        # Enforce polite rate limiting before making request
        self._enforce_rate_limit("anthropic")
        
        @self.retry_handler.with_retry("anthropic", model)
        def make_anthropic_call():
            content, cost, _ = self.anthropic_client._analyze(prompt, model)
            
            # Mark provider as healthy on success
            if self.failover_handler:
                self.failover_handler.mark_provider_healthy("anthropic")
            
            return self._parse_response(content, self._current_text, self._current_framework), cost
        
        return make_anthropic_call()
    
    def _anthropic_api_call_basic_provider(self, prompt: str, model: str) -> Tuple[Dict[str, Any], float]:
        """Basic Anthropic API call with simple error handling using provider."""
        self._enforce_rate_limit("anthropic")
        
        try:
            content, cost, _ = self.anthropic_client._analyze(prompt, model)
            return self._parse_response(content, self._current_text, self._current_framework), cost
        except Exception as e:
            print(f"Anthropic API error: {e}")
            return {"error": str(e)}, 0.0
    
    def _analyze_with_mistral(self, prompt: str, model_name: str = "mistral-medium-3") -> Tuple[Dict[str, Any], float]:
        """Analyze with Mistral models via provider class."""
        if not self.mistral_client:
            raise ValueError("Mistral client not initialized")

        # Use retry handler if available, otherwise basic error handling
        if self.retry_handler:
            return self._mistral_api_call_with_retry_provider(prompt, model_name)
        else:
            return self._mistral_api_call_basic_provider(prompt, model_name)
    
    def _mistral_api_call_with_retry_provider(self, prompt: str, model: str) -> Tuple[Dict[str, Any], float]:
        """Mistral API call with retry logic using provider."""
        
        # Enforce polite rate limiting before making request
        self._enforce_rate_limit("mistral")
        
        @self.retry_handler.with_retry("mistral", model)
        def make_mistral_call():
            content, cost, _ = self.mistral_client._analyze(prompt, model)
            
            # Mark provider as healthy on success
            if self.failover_handler:
                self.failover_handler.mark_provider_healthy("mistral")
            
            return self._parse_response(content, self._current_text, self._current_framework), cost
        
        return make_mistral_call()
    
    def _mistral_api_call_basic_provider(self, prompt: str, model: str) -> Tuple[Dict[str, Any], float]:
        """Basic Mistral API call with simple error handling using provider."""
        self._enforce_rate_limit("mistral")
        
        try:
            content, cost, _ = self.mistral_client._analyze(prompt, model)
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
        """Analyze with Google AI models via provider class."""
        if not self.google_ai_client:
            raise ValueError("Google AI client not initialized")

        # Use retry handler if available, otherwise basic error handling
        if self.retry_handler:
            return self._google_ai_api_call_with_retry_provider(prompt, model_name)
        else:
            return self._google_ai_api_call_basic_provider(prompt, model_name)
    
    def _google_ai_api_call_with_retry_provider(self, prompt: str, model: str) -> Tuple[Dict[str, Any], float]:
        """Google AI API call with retry logic using provider."""
        
        # Enforce polite rate limiting before making request
        self._enforce_rate_limit("google_ai")
        
        @self.retry_handler.with_retry("google_ai", model)
        def make_google_ai_call():
            content, cost, _ = self.google_ai_client._analyze(prompt, model)
            
            # Mark provider as healthy on success
            if self.failover_handler:
                self.failover_handler.mark_provider_healthy("google_ai")
            
            return self._parse_response(content, self._current_text, self._current_framework), cost
        
        return make_google_ai_call()
    
    def _google_ai_api_call_basic_provider(self, prompt: str, model: str) -> Tuple[Dict[str, Any], float]:
        """Basic Google AI API call with simple error handling using provider."""
        self._enforce_rate_limit("google_ai")
        
        try:
            content, cost, _ = self.google_ai_client._analyze(prompt, model)
            return self._parse_response(content, self._current_text, self._current_framework), cost
        except Exception as e:
            print(f"Google AI API error: {e}")
            return {"error": str(e)}, 0.0

    def _analyze_with_ollama(self, prompt: str, model_name: str = "ollama/llama3.2") -> Tuple[Dict[str, Any], float]:
        """Analyze with Ollama models running locally."""
        try:
            import requests
            import json
            
            # Extract actual model name from ollama/model_name format
            actual_model = model_name.replace("ollama/", "")
            
            # Ollama API endpoint (local)
            url = "http://localhost:11434/api/generate"
            
            payload = {
                "model": actual_model,
                "prompt": prompt,
                "stream": False,
                "format": "json"
            }
            
            print(f"🦙 Calling Ollama: {model_name} (local, $0 cost)")
            
            response = requests.post(url, json=payload, timeout=300)  # 5 min timeout for local models
            
            if response.status_code == 200:
                result = response.json()
                content = result.get("response", "")
                
                # Ollama models are free (local)
                cost = 0.0
                
                return self._parse_response(content, self._current_text, self._current_framework), cost
            else:
                error_msg = f"Ollama API error {response.status_code}: {response.text}"
                print(f"❌ {error_msg}")
                return {"error": error_msg}, 0.0
                
        except requests.exceptions.ConnectionError:
            error_msg = "Ollama server not running. Start with: ollama serve"
            print(f"❌ {error_msg}")
            return {"error": error_msg}, 0.0
        except Exception as e:
            error_msg = f"Ollama error: {str(e)}"
            print(f"❌ {error_msg}")
            return {"error": error_msg}, 0.0
    
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
        
        # Ollama models (local, cost-free)
        models["ollama"] = [
            "ollama/llama3.2",      # Meta Llama 3.2 (3B/11B/90B)
            "ollama/llama3.1",      # Meta Llama 3.1 (8B/70B/405B)
            "ollama/mistral",       # Mistral 7B
            "ollama/codellama",     # Code Llama
            "ollama/phi3",          # Microsoft Phi-3
            "ollama/gemma2",        # Google Gemma 2
            "ollama/qwen2.5",       # Alibaba Qwen 2.5
            "ollama/deepseek-v2",   # DeepSeek V2
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