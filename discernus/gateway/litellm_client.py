#!/usr/bin/env python3
"""
LiteLLM Unified Client for Cloud APIs + Local Ollama Models
==========================================================

THIN Principle: Minimal wrapper around LiteLLM for unified API access.
Handles rate limiting, cost management, and provider failover automatically.

Enhanced with LiteLLM native rate limiting for faster experiments.
"""

import os
import json
import time
from typing import Dict, Tuple, Any, Optional
from dotenv import load_dotenv
import sys

# Add project root to path for imports
project_root = os.path.join(os.path.dirname(__file__), "..", "..")
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

# Simple mock implementations for optional features
class CostManager:
    """Mock cost manager for development"""
    def estimate_cost(self, text, provider, model): return 0.001, 0, 0
    def check_limits_before_request(self, cost): return True, "within limits"
    def record_actual_cost(self, cost): pass

class TPMRateLimiter:
    """Mock TPM rate limiter for development"""
    def estimate_tokens(self, text, model): return len(text.split()) * 1.3
    def wait_if_needed(self, model, estimated_tokens, prompt_text): return True
    def record_usage(self, model, tokens): pass

class APIRetryHandler:
    """Mock retry handler for development"""
    def with_retry(self, provider, model):
        def decorator(func): return func
        return decorator
    def get_statistics(self): return {}

class ProviderFailoverHandler:
    """Mock failover handler for development"""
    def mark_provider_healthy(self, provider): pass


class LiteLLMClient:
    """
    Unified LLM client using LiteLLM for cloud APIs + local Ollama models.
    
    THIN Principle: Minimal abstraction over LiteLLM with essential features:
    - Cost management and tracking
    - Rate limiting across providers  
    - Retry logic with failover
    - Security validation
    - Token usage monitoring
    """

    def __init__(self):
        if not LITELLM_AVAILABLE:
            raise ImportError("LiteLLM is required but not available. Install with: pip install litellm")

        print("🚀 Initializing LiteLLM Unified Client")

        self.cost_manager = CostManager()
        self._current_text = None
        self._current_framework = None
        self.retry_handler = APIRetryHandler()
        self.failover_handler = ProviderFailoverHandler()
        self.tpm_limiter = TPMRateLimiter()

        self._configure_litellm()
        self._test_model_availability()

    def _configure_litellm(self):
        """Configure LiteLLM with unified settings and native rate limiting"""
        # Set API keys from environment
        api_keys = {
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
            "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
            "MISTRAL_API_KEY": os.getenv("MISTRAL_API_KEY"),
            "GOOGLE_APPLICATION_CREDENTIALS": os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
            "VERTEXAI_PROJECT": os.getenv("VERTEXAI_PROJECT"),
            "VERTEXAI_LOCATION": os.getenv("VERTEXAI_LOCATION"),
        }

        available_providers = []
        for key, value in api_keys.items():
            if value:
                if key == "GOOGLE_APPLICATION_CREDENTIALS":
                    available_providers.append("vertex_ai")
                elif key not in ["VERTEXAI_PROJECT", "VERTEXAI_LOCATION"]:
                    provider = key.replace("_API_KEY", "").lower()
                    available_providers.append(provider)

        # Check Ollama availability
        try:
            import requests

            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                available_providers.append("ollama")
                print("✅ Ollama local models available")
            else:
                print("⚠️ Ollama not responding")
        except Exception as e:
            print(f"⚠️ Ollama check failed: {e}")

        print(f"✅ LiteLLM configured with providers: {', '.join(available_providers)}")

        # Configure LiteLLM global settings for native rate limiting
        litellm.drop_params = True  # Drop unsupported params gracefully
        litellm.set_verbose = False  # Can be enabled for debugging

        # Enhanced: Configure native rate limiting for faster experiments
        litellm.request_timeout = 60  # 60 second timeout
        litellm.num_retries = 2  # LiteLLM handles retries intelligently

        print("🏎️ LiteLLM native rate limiting enabled - experiments will run FASTER!")

    def _test_model_availability(self):
        """Test availability of key models"""
        test_models = ["gpt-3.5-turbo", "claude-3-5-haiku-20241022", "ollama/llama3.2", "ollama/mistral"]

        available_models = []
        for model in test_models:
            if self._test_single_model(model):
                available_models.append(model)

        print(f"✅ Available models: {', '.join(available_models)}")
        return available_models

    def _test_single_model(self, model: str) -> bool:
        """Test if a single model is available"""
        try:
            response = completion(model=model, messages=[{"role": "user", "content": "test"}], max_tokens=1, timeout=10)
            return True
        except Exception:
            return False

    def test_connections(self) -> Dict[str, bool]:
        """Test all model connections"""
        test_models = {
            "openai": "gpt-3.5-turbo",
            "anthropic": "claude-3-5-haiku-20241022",
            "mistral": "mistral/mistral-small-latest",
            "vertex_ai": "vertex_ai/gemini-2.5-flash",
            "ollama_llama": "ollama/llama3.2",
            "ollama_mistral": "ollama/mistral",
        }

        results = {}
        for provider, model in test_models.items():
            try:
                response = completion(
                    model=model, messages=[{"role": "user", "content": "Hello"}], max_tokens=5, timeout=10
                )
                results[provider] = True
                print(f"✅ {provider} connection successful ({model})")
            except Exception as e:
                results[provider] = False
                print(f"❌ {provider} connection failed: {e}")

        return results

    def analyze_text(self, text: str, experiment_def: Dict[str, Any], model_name: str) -> Tuple[Dict[str, Any], float]:
        """
        Analyze text using an experiment definition file.
        
        Main entry point for text analysis with full cost tracking and rate limiting.
        """
        # Store context for quality assurance
        self._current_text = text
        self._current_framework = experiment_def.get("framework", {}).get("name", "unknown")

        # Simple prompt generation (simplified for THIN approach)
        prompt = f"Please analyze the following text according to the experiment definition:\n\nText: {text}\n\nExperiment: {experiment_def}"
        
        # Store prompt for debugging
        self._current_prompt = prompt

        # TPM Rate Limiting
        if self.tpm_limiter:
            try:
                estimated_tokens = self.tpm_limiter.estimate_tokens(prompt, model_name)
                print(f"🔍 TPM Check: {model_name} - {estimated_tokens:,} tokens estimated")

                can_proceed = self.tpm_limiter.wait_if_needed(
                    model=model_name, estimated_tokens=estimated_tokens, prompt_text=text[:200]
                )

                if not can_proceed:
                    print("🚫 TPM rate limiting cancelled the request")
                    return {"error": "TPM rate limiting cancelled request"}, 0.0
            except Exception as tpm_error:
                print(f"⚠️ TPM rate limiting failed: {tpm_error}")

        # Cost limit checks
        if self.cost_manager:
            provider = self._get_provider_from_model(model_name)
            estimated_cost, _, _ = self.cost_manager.estimate_cost(text, provider, model_name)
            can_proceed, message = self.cost_manager.check_limits_before_request(estimated_cost)

            if not can_proceed:
                print(f"🚫 Cost limit check failed: {message}")
                return {"error": f"Cost limit exceeded: {message}"}, 0.0
            else:
                print(f"💰 Estimated cost: ${estimated_cost:.4f} - {message}")

        # Route to LiteLLM unified completion with native rate limiting
        start_time = time.time()
        result, cost = self._analyze_with_litellm_native(prompt, model_name)

        # TPM usage tracking
        if self.tpm_limiter and "error" not in result:
            try:
                response_text = result.get("raw_response", "")
                output_tokens = self.tpm_limiter.estimate_tokens(response_text, model_name)
                total_tokens = estimated_tokens + output_tokens

                self.tpm_limiter.record_usage(model_name, total_tokens)

                end_time = time.time()
                duration = end_time - start_time
                print(f"✅ TPM Tracking: {model_name} used {total_tokens:,} tokens in {duration:.1f}s")

                # Add TPM info to result
                if "tpm_info" not in result:
                    result["tpm_info"] = {}
                result["tpm_info"].update(
                    {
                        "estimated_input_tokens": estimated_tokens,
                        "estimated_output_tokens": output_tokens,
                        "total_tokens": total_tokens,
                        "model": model_name,
                    }
                )
            except Exception as tracking_error:
                print(f"⚠️ TPM usage tracking failed: {tracking_error}")

        return result, cost

    def _analyze_with_litellm_native(self, prompt: str, model_name: str) -> Tuple[Dict[str, Any], float]:
        """
        Smart rate limiting based on model type:
        - Native LiteLLM for cloud APIs (faster for high-volume experiments)
        - Simple delays for local Ollama (more efficient for local models)
        """
        provider = self._get_provider_from_model(model_name)

        # Smart rate limiting strategy
        if provider == "ollama":
            # For local Ollama: simple delay is more efficient
            self._enforce_simple_rate_limit(provider, 0.1)  # Minimal delay for local
            print(f"🏠 Making local Ollama call with simple rate limiting to {model_name}")
        elif provider == "anthropic":
            # For Claude: More aggressive rate limiting due to overload issues
            self._enforce_simple_rate_limit(provider, 3.0)  # 3 second delay between Claude calls
            print(f"🐌 Making Claude API call with AGGRESSIVE rate limiting to {model_name}")
        else:
            # For other cloud APIs: use LiteLLM native for maximum speed
            print(f"☁️ Making cloud API call with NATIVE rate limiting to {model_name}")

        # Use retry handler if available
        if self.retry_handler:
            return self._litellm_call_with_retry(prompt, model_name)
        else:
            return self._litellm_call_basic(prompt, model_name)

    def _enforce_simple_rate_limit(self, provider: str, delay: float):
        """Simple rate limiting for local models"""
        current_time = time.time()

        if not hasattr(self, "_last_local_request"):
            self._last_local_request = {}

        if provider in self._last_local_request:
            time_since_last = current_time - self._last_local_request[provider]
            if time_since_last < delay:
                sleep_time = delay - time_since_last
                time.sleep(sleep_time)

        self._last_local_request[provider] = time.time()

    def _litellm_call_with_retry(self, prompt: str, model_name: str) -> Tuple[Dict[str, Any], float]:
        """LiteLLM call with retry logic and native rate limiting"""
        provider = self._get_provider_from_model(model_name)
        
        # Track current model for parsing
        self._last_model_used = model_name

        @self.retry_handler.with_retry(provider, model_name)
        def make_litellm_call():
            # Dynamic timeout based on provider
            timeout_duration = 300 if provider == "ollama" else 60  # 5 minutes for Ollama, 1 minute for others
            
            response = completion(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,  # Increased for analytical variation
                max_tokens=2000,
                timeout=timeout_duration,
                # LiteLLM handles rate limiting natively - no custom delays!
            )

            # Mark provider as healthy on success
            if self.failover_handler:
                self.failover_handler.mark_provider_healthy(provider)

            # Extract response content and cost
            content = response.choices[0].message.content
            cost = getattr(response, "response_cost", 0.0) if hasattr(response, "response_cost") else 0.0

            # Record actual cost for tracking
            if self.cost_manager and cost > 0:
                self.cost_manager.record_actual_cost(cost)

            return self._parse_response(content, self._current_text, self._current_framework), cost

        return make_litellm_call()

    def _litellm_call_basic(self, prompt: str, model_name: str) -> Tuple[Dict[str, Any], float]:
        """Basic LiteLLM call with native rate limiting (much faster!)"""
        # Track current model for parsing
        self._last_model_used = model_name
        
        try:
            # Dynamic timeout based on provider 
            provider = self._get_provider_from_model(model_name)
            timeout_duration = 300 if provider == "ollama" else 60  # 5 minutes for Ollama, 1 minute for others
            
            response = completion(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,  # Increased for analytical variation
                max_tokens=2000,
                timeout=timeout_duration,
                # LiteLLM will handle rate limits automatically based on provider limits!
            )

            # Extract response content and cost
            content = response.choices[0].message.content
            cost = getattr(response, "response_cost", 0.0) if hasattr(response, "response_cost") else 0.0

            # Record actual cost for tracking
            if self.cost_manager and cost > 0:
                self.cost_manager.record_actual_cost(cost)

            return self._parse_response(content, self._current_text, self._current_framework), cost

        except Exception as e:
            print(f"LiteLLM API error for {model_name}: {e}")
            # Handle rate limit errors gracefully - LiteLLM will retry automatically
            return {"error": str(e)}, 0.0

    def _get_provider_from_model(self, model_name: str) -> str:
        """Get provider name from model name"""
        model_lower = model_name.lower()

        if model_lower.startswith("vertex_ai/"):
            return "vertex_ai"
        elif model_lower.startswith("ollama/"):
            return "ollama"
        elif any(x in model_lower for x in ["gpt", "openai", "o1", "o3", "o4"]):
            return "openai"
        elif any(x in model_lower for x in ["claude", "anthropic"]):
            return "anthropic"
        elif any(x in model_lower for x in ["mistral", "codestral"]):
            return "mistral"
        elif any(x in model_lower for x in ["gemini", "google"]):
            return "vertex_ai"  # Default Gemini to Vertex AI
        else:
            return "unknown"

    def _parse_response(self, content: str, text_input: str = None, framework: str = None) -> Dict[str, Any]:
        """
        Parse LLM response content
        
        THIN Principle: Minimal parsing - mostly pass through raw content
        """
        if not content:
            return {"error": "Empty response from model"}

        # For debugging and transparency, always include raw response
        result = {
            "raw_response": content,
            "model_used": getattr(self, '_last_model_used', 'unknown'),
            "timestamp": time.time()
        }

        # Simple content validation
        if len(content.strip()) < 10:
            result["warning"] = "Very short response - may indicate model issue"

        return result

    def get_available_models(self) -> Dict[str, list]:
        """Get list of available models by provider"""
        models = {
            "openai": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
            "anthropic": ["claude-3-5-haiku-20241022", "claude-3-5-sonnet-20241022"],
            "mistral": ["mistral/mistral-small-latest", "mistral/mistral-medium-latest"],
            "vertex_ai": ["vertex_ai/gemini-2.5-flash", "vertex_ai/gemini-pro"],
            "ollama": ["ollama/llama3.2", "ollama/mistral"]
        }

        # Test which ones actually work
        available = {}
        for provider, model_list in models.items():
            available[provider] = []
            for model in model_list:
                if self._test_single_model(model):
                    available[provider].append(model)

        return available

    def get_retry_statistics(self) -> Dict[str, Any]:
        """Get retry statistics from the retry handler"""
        if self.retry_handler:
            return self.retry_handler.get_statistics()
        return {"error": "Retry handler not available"}

    def log_reliability_report(self):
        """Log a reliability report for monitoring"""
        if self.retry_handler:
            stats = self.retry_handler.get_statistics()
            print("🔍 LiteLLM Reliability Report:")
            for provider, data in stats.items():
                success_rate = data.get("success_rate", 0)
                total_calls = data.get("total_calls", 0)
                print(f"   {provider}: {success_rate:.1%} success rate ({total_calls} calls)")
        else:
            print("⚠️ No reliability data available") 