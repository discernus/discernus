#!/usr/bin/env python3
"""
LiteLLM Unified Client for Cloud APIs + Local Ollama Models
ENHANCED: Uses LiteLLM native rate limiting for faster experiments
"""

import os
import json
import time
from typing import Dict, Tuple, Any, Optional
from dotenv import load_dotenv
import sys

# Add project root to path for imports
project_root = os.path.join(os.path.dirname(__file__), '..', '..')
if project_root not in sys.path:
    sys.path.append(project_root)

try:
    import litellm
    from litellm import completion, acompletion
    LITELLM_AVAILABLE = True
except ImportError:
    LITELLM_AVAILABLE = False
    print("❌ LiteLLM not available. Install with: pip install litellm")

# Import existing components to preserve architecture
load_dotenv()

# Import cost and rate limiting (preserved for compatibility)  
try:
    from ..utils.cost_management import CostManager, TPMRateLimiter
    COST_MANAGER_AVAILABLE = True
    TPM_RATE_LIMITER_AVAILABLE = True
except ImportError:
    print("⚠️ Cost management not available")
    COST_MANAGER_AVAILABLE = False
    TPM_RATE_LIMITER_AVAILABLE = False

class LiteLLMClient:
    """
    Unified LLM client using LiteLLM for cloud APIs + local Ollama models
    ENHANCED: Uses LiteLLM's native rate limiting for maximum experiment speed
    """
    
    def __init__(self):
        if not LITELLM_AVAILABLE:
            raise ImportError("LiteLLM is required but not available. Install with: pip install litellm")
        
        print("🚀 Initializing LiteLLM Unified Client with NATIVE RATE LIMITING")
        
        # Cost and QA management (preserved from DirectAPIClient)
        if COST_MANAGER_AVAILABLE:
            self.cost_manager = CostManager()
            print("✅ Cost Manager initialized")
        else:
            self.cost_manager = None
            print("⚠️ Cost Manager not available")
        
        # Context for quality assurance (preserved from DirectAPIClient)
        self._current_text = None
        self._current_framework = None

        # REMOVED: Custom rate limiting - using LiteLLM native instead
        # No more: self._last_request_time = {} or self._rate_limits = {}
        print("✅ Using LiteLLM native rate limiting (FASTER for experiments!)")
        
        # Initialize retry handler (preserved)
        try:
            from ..utils.api_retry_handler import APIRetryHandler, ProviderFailoverHandler
            self.retry_handler = APIRetryHandler()
            self.failover_handler = ProviderFailoverHandler()
        except ImportError:
            print("⚠️ Retry handler not available - using basic error handling")
            self.retry_handler = None
            self.failover_handler = None
        
        # Initialize TPM rate limiter (preserved)
        if TPM_RATE_LIMITER_AVAILABLE:
            self.tpm_limiter = TPMRateLimiter()
            print("✅ TPM Rate Limiter initialized")
        else:
            self.tpm_limiter = None
            print("⚠️ TPM Rate Limiter not available")
        
        # Configure LiteLLM settings with NATIVE RATE LIMITING
        self._configure_litellm()
        
        # Test available models
        self._test_model_availability()
    
    def _configure_litellm(self):
        """Configure LiteLLM with unified settings and NATIVE RATE LIMITING"""
        # Set API keys from environment
        api_keys = {
            'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
            'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY'),
            'MISTRAL_API_KEY': os.getenv('MISTRAL_API_KEY'),
            'GOOGLE_AI_API_KEY': os.getenv('GOOGLE_AI_API_KEY')
        }
        
        available_providers = []
        for key, value in api_keys.items():
            if value:
                provider = key.replace('_API_KEY', '').lower()
                available_providers.append(provider)
        
        # Check Ollama availability
        try:
            import requests
            response = requests.get('http://localhost:11434/api/tags', timeout=5)
            if response.status_code == 200:
                available_providers.append('ollama')
                print("✅ Ollama local models available")
            else:
                print("⚠️ Ollama not responding")
        except Exception as e:
            print(f"⚠️ Ollama check failed: {e}")
        
        print(f"✅ LiteLLM configured with providers: {', '.join(available_providers)}")
        
        # Configure LiteLLM global settings for NATIVE RATE LIMITING
        litellm.drop_params = True  # Drop unsupported params gracefully
        litellm.set_verbose = False  # Can be enabled for debugging
        
        # ENHANCED: Configure native rate limiting for faster experiments
        litellm.request_timeout = 60  # 60 second timeout
        litellm.num_retries = 2  # LiteLLM handles retries intelligently
        
        print("🏎️ LiteLLM native rate limiting enabled - experiments will run FASTER!")
    
    def _test_model_availability(self):
        """Test availability of key models"""
        test_models = [
            'gpt-3.5-turbo',
            'claude-3-5-haiku-20241022',
            'ollama/llama3.2',
            'ollama/mistral'
        ]
        
        available_models = []
        for model in test_models:
            if self._test_single_model(model):
                available_models.append(model)
        
        print(f"✅ Available models: {', '.join(available_models)}")
        return available_models
    
    def _test_single_model(self, model: str) -> bool:
        """Test if a single model is available"""
        try:
            response = completion(
                model=model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=1,
                timeout=10
            )
            return True
        except Exception:
            return False
    
    def test_connections(self) -> Dict[str, bool]:
        """
        Test all model connections (maintains DirectAPIClient interface)
        """
        test_models = {
            'openai': 'gpt-3.5-turbo',
            'anthropic': 'claude-3-5-haiku-20241022', 
            'mistral': 'mistral-small-latest',
            'google_ai': 'gemini-1.5-flash',
            'ollama_llama': 'ollama/llama3.2',
            'ollama_mistral': 'ollama/mistral'
        }
        
        results = {}
        for provider, model in test_models.items():
            try:
                response = completion(
                    model=model,
                    messages=[{"role": "user", "content": "Hello"}],
                    max_tokens=5,
                    timeout=10
                )
                results[provider] = True
                print(f"✅ {provider} connection successful ({model})")
            except Exception as e:
                results[provider] = False
                print(f"❌ {provider} connection failed: {e}")
        
        return results
    
    def analyze_text(self, text: str, framework: str, model_name: str) -> Tuple[Dict[str, Any], float]:
        """
        Analyze text using specified model and framework
        ENHANCED: No custom rate limiting delays - uses LiteLLM native for speed
        
        Args:
            text: Text to analyze
            framework: Framework to use (e.g., 'moral_foundations_theory')
            model_name: Model name (cloud: 'gpt-4o', local: 'ollama/llama3.2')
        
        Returns:
            Tuple[analysis_result, cost]
        """
        # Store context for quality assurance (preserved from DirectAPIClient)
        self._current_text = text
        self._current_framework = framework
        
        # Generate prompt using existing template manager (preserved architecture)
        try:
            from src.prompts.template_manager import PromptTemplateManager
            template_manager = PromptTemplateManager()
            prompt = template_manager.generate_api_prompt(text, framework, model_name)
        except ImportError as e:
            raise RuntimeError(f"PromptTemplateManager is required but could not be imported: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to generate proper analysis prompt: {e}")
        
        # TPM Rate Limiting (preserved from DirectAPIClient)
        if self.tpm_limiter:
            try:
                estimated_tokens = self.tpm_limiter.estimate_tokens(prompt, model_name)
                print(f"🔍 TPM Check: {model_name} - {estimated_tokens:,} tokens estimated")
                
                can_proceed = self.tpm_limiter.wait_if_needed(
                    model=model_name,
                    estimated_tokens=estimated_tokens,
                    prompt_text=text[:200]
                )
                
                if not can_proceed:
                    print("🚫 TPM rate limiting cancelled the request")
                    return {"error": "TPM rate limiting cancelled request"}, 0.0
            except Exception as tpm_error:
                print(f"⚠️ TPM rate limiting failed: {tpm_error}")
        
        # Cost limit checks (preserved from DirectAPIClient)
        if self.cost_manager:
            provider = self._get_provider_from_model(model_name)
            estimated_cost, _, _ = self.cost_manager.estimate_cost(text, provider, model_name)
            can_proceed, message = self.cost_manager.check_limits_before_request(estimated_cost)
            
            if not can_proceed:
                print(f"🚫 Cost limit check failed: {message}")
                return {"error": f"Cost limit exceeded: {message}"}, 0.0
            else:
                print(f"💰 Estimated cost: ${estimated_cost:.4f} - {message}")
        
        # Route to LiteLLM unified completion with NATIVE RATE LIMITING
        start_time = time.time()
        result, cost = self._analyze_with_litellm_native(prompt, model_name)
        
        # TPM usage tracking (preserved from DirectAPIClient)
        if self.tpm_limiter and 'error' not in result:
            try:
                response_text = result.get('raw_response', '')
                output_tokens = self.tpm_limiter.estimate_tokens(response_text, model_name)
                total_tokens = estimated_tokens + output_tokens
                
                self.tpm_limiter.record_usage(model_name, total_tokens)
                
                end_time = time.time()
                duration = end_time - start_time
                print(f"✅ TPM Tracking: {model_name} used {total_tokens:,} tokens in {duration:.1f}s")
                
                # Add TPM info to result
                if 'tpm_info' not in result:
                    result['tpm_info'] = {}
                result['tpm_info'].update({
                    'estimated_input_tokens': estimated_tokens,
                    'estimated_output_tokens': output_tokens,
                    'total_tokens': total_tokens,
                    'model': model_name
                })
            except Exception as tracking_error:
                print(f"⚠️ TPM usage tracking failed: {tracking_error}")
        
        return result, cost
    
    def _analyze_with_litellm_native(self, prompt: str, model_name: str) -> Tuple[Dict[str, Any], float]:
        """
        ENHANCED: Smart rate limiting based on model type
        - Native LiteLLM for cloud APIs (faster for high-volume experiments)
        - Simple delays for local Ollama (more efficient for local models)
        """
        provider = self._get_provider_from_model(model_name)
        
        # Smart rate limiting strategy
        if provider == 'ollama':
            # For local Ollama: simple delay is more efficient
            self._enforce_simple_rate_limit(provider, 0.1)  # Minimal delay for local
            print(f"🏠 Making local Ollama call with simple rate limiting to {model_name}")
        else:
            # For cloud APIs: use LiteLLM native for maximum speed
            print(f"☁️ Making cloud API call with NATIVE rate limiting to {model_name}")
        
        # Use retry handler if available (preserved from DirectAPIClient)
        if self.retry_handler:
            return self._litellm_call_with_retry(prompt, model_name)
        else:
            return self._litellm_call_basic(prompt, model_name)
    
    def _enforce_simple_rate_limit(self, provider: str, delay: float):
        """Simple rate limiting for local models"""
        current_time = time.time()
        
        if not hasattr(self, '_last_local_request'):
            self._last_local_request = {}
        
        if provider in self._last_local_request:
            time_since_last = current_time - self._last_local_request[provider]
            if time_since_last < delay:
                sleep_time = delay - time_since_last
                time.sleep(sleep_time)
        
        self._last_local_request[provider] = time.time()
    
    def _litellm_call_with_retry(self, prompt: str, model_name: str) -> Tuple[Dict[str, Any], float]:
        """LiteLLM call with retry logic and NATIVE rate limiting"""
        provider = self._get_provider_from_model(model_name)
        
        @self.retry_handler.with_retry(provider, model_name)
        def make_litellm_call():
            response = completion(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=2000,
                timeout=60
                # LiteLLM handles rate limiting natively - no custom delays!
            )
            
            # Mark provider as healthy on success
            if self.failover_handler:
                self.failover_handler.mark_provider_healthy(provider)
            
            # Extract response content and cost
            content = response.choices[0].message.content
            cost = getattr(response, 'response_cost', 0.0) if hasattr(response, 'response_cost') else 0.0
            
            return self._parse_response(content, self._current_text, self._current_framework), cost
        
        return make_litellm_call()
    
    def _litellm_call_basic(self, prompt: str, model_name: str) -> Tuple[Dict[str, Any], float]:
        """Basic LiteLLM call with NATIVE rate limiting (much faster!)"""
        try:
            response = completion(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=2000,
                timeout=60
                # LiteLLM will handle rate limits automatically based on provider limits!
            )
            
            # Extract response content and cost
            content = response.choices[0].message.content
            cost = getattr(response, 'response_cost', 0.0) if hasattr(response, 'response_cost') else 0.0
            
            return self._parse_response(content, self._current_text, self._current_framework), cost
            
        except Exception as e:
            print(f"LiteLLM API error for {model_name}: {e}")
            # Handle rate limit errors gracefully - LiteLLM will retry automatically
            return {"error": str(e)}, 0.0
    
    def _get_provider_from_model(self, model_name: str) -> str:
        """Get provider name from model name (enhanced for Ollama)"""
        model_lower = model_name.lower()
        
        if model_lower.startswith('ollama/'):
            return 'ollama'
        elif any(x in model_lower for x in ["gpt", "openai", "o1", "o3", "o4"]):
            return "openai"
        elif any(x in model_lower for x in ["claude", "anthropic"]):
            return "anthropic"
        elif any(x in model_lower for x in ["mistral", "codestral"]):
            return "mistral"
        elif any(x in model_lower for x in ["gemini", "google"]):
            return "google_ai"
        else:
            return "unknown"
    
    def _parse_response(self, content: str, text_input: str = None, framework: str = None) -> Dict[str, Any]:
        """
        Parse LLM response with integrated quality assurance validation
        PRESERVED from DirectAPIClient for full compatibility
        """
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
            # Fallback: extract scores from text format
            parsed_scores = self._extract_narrative_scores(content)
            raw_response = {
                'scores': parsed_scores,
                'analysis': 'Text format response parsed',
                'raw_text': content
            }
        
        # The old QA system has been removed from this client.
        # We now return the parsed scores and raw response directly.
        result = {
            'scores': parsed_scores,
            'raw_response': content,
            'parsed': True
        }
        
        # Add any additional analysis info from the original response
        if isinstance(raw_response, dict):
            for key, value in raw_response.items():
                if key not in result:
                    result[key] = value
                    
        return result
    
    def _is_hierarchical_response(self, response: Dict[str, Any]) -> bool:
        """Check if response is in hierarchical 3-stage format (preserved from DirectAPIClient)"""
        if not isinstance(response, dict):
            return False
        
        # Look for stage indicators
        stage_keys = ['stage_1', 'stage_2', 'stage_3', 'stages']
        return any(key in response for key in stage_keys)
    
    def _extract_hierarchical_scores(self, response: Dict[str, Any]) -> Dict[str, float]:
        """Extract scores from hierarchical response format (preserved from DirectAPIClient)"""
        scores = {}
        
        # Try different hierarchical formats
        if 'stage_3' in response and isinstance(response['stage_3'], dict):
            stage_3 = response['stage_3']
            if 'scores' in stage_3:
                scores.update(stage_3['scores'])
            elif 'final_scores' in stage_3:
                scores.update(stage_3['final_scores'])
        
        elif 'stages' in response and isinstance(response['stages'], dict):
            stages = response['stages']
            if 'final' in stages or 'stage_3' in stages:
                final_stage = stages.get('final', stages.get('stage_3', {}))
                if isinstance(final_stage, dict) and 'scores' in final_stage:
                    scores.update(final_stage['scores'])
        
        # Fallback: look for any scores in the response
        if not scores and 'scores' in response:
            scores.update(response['scores'])
        
        return scores
    
    def _extract_narrative_scores(self, content: str) -> Dict[str, Any]:
        """Extract narrative scores from text format (preserved from DirectAPIClient)"""
        import re
        
        scores = {}
        
        # Try to find JSON-like structures in the text
        json_pattern = r'\{[^{}]*\}'
        json_matches = re.findall(json_pattern, content)
        
        for match in json_matches:
            try:
                parsed = json.loads(match)
                if isinstance(parsed, dict):
                    scores.update(parsed)
            except:
                continue
        
        # Try to find key-value pairs
        kv_pattern = r'(\w+):\s*([0-9]*\.?[0-9]+)'
        kv_matches = re.findall(kv_pattern, content)
        
        for key, value in kv_matches:
            try:
                scores[key] = float(value)
            except:
                continue
        
        return scores
    
    def get_available_models(self) -> Dict[str, list]:
        """
        Get available models by provider (maintains DirectAPIClient interface)
        Enhanced to include Ollama local models
        """
        models = {
            "openai": [
                "gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo", "gpt-4-turbo",
                "o1-preview", "o1-mini", "gpt-4.1-mini"
            ],
            "anthropic": [
                "claude-3-5-sonnet-20241022", "claude-3-5-haiku-20241022",
                "claude-3-opus-20240229", "claude-3-sonnet-20240229"
            ],
            "mistral": [
                "mistral-large-latest", "mistral-medium-latest", "mistral-small-latest",
                "codestral-latest", "mistral-tiny"
            ],
            "google_ai": [
                "gemini-2.5-flash", "gemini-1.5-pro", "gemini-1.5-flash"
            ],
            "ollama": []  # Will be populated dynamically
        }
        
        # Get available Ollama models dynamically
        try:
            import requests
            response = requests.get('http://localhost:11434/api/tags', timeout=5)
            if response.status_code == 200:
                ollama_data = response.json()
                for model_info in ollama_data.get('models', []):
                    model_name = model_info.get('name', '')
                    if model_name:
                        models["ollama"].append(f"ollama/{model_name}")
        except Exception as e:
            print(f"⚠️ Could not fetch Ollama models: {e}")
        
        return models
    
    def get_retry_statistics(self) -> Dict[str, Any]:
        """Get retry statistics (maintains DirectAPIClient interface)"""
        if self.retry_handler:
            return self.retry_handler.get_statistics()
        else:
            return {"retry_handler": "not_available"}
    
    def log_reliability_report(self):
        """Log reliability report (maintains DirectAPIClient interface)"""
        print("\n📊 LITELLM UNIFIED CLIENT RELIABILITY REPORT")
        print("=" * 60)
        
        # Test connections
        connection_results = self.test_connections()
        total_providers = len(connection_results)
        working_providers = sum(1 for status in connection_results.values() if status)
        
        print(f"Provider Connectivity: {working_providers}/{total_providers} providers working")
        for provider, status in connection_results.items():
            emoji = "✅" if status else "❌"
            print(f"  {emoji} {provider}")
        
        # Available models
        models = self.get_available_models()
        total_models = sum(len(model_list) for model_list in models.values())
        print(f"\nAvailable Models: {total_models} total models across {len(models)} providers")
        for provider, model_list in models.items():
            if model_list:
                print(f"  • {provider}: {len(model_list)} models")
        
        # Retry statistics
        if self.retry_handler:
            retry_stats = self.get_retry_statistics()
            print(f"\nRetry Handler: {retry_stats}")
        
        print("\n" + "=" * 60) 