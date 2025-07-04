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

# Import stubbed dependencies for full isolation
from ..utils.stubs import CostManager, TPMRateLimiter, APIRetryHandler, ProviderFailoverHandler

from ..engine.prompt_engine import create_prompt_from_experiment
from ..engine.signature_engine import FrameworkLoader as ExperimentLoader  # Rename for clarity


class LiteLLMClient:
    """
    Unified LLM client using LiteLLM for cloud APIs + local Ollama models.
    This version is fully isolated for the rebooted application.
    """

    def __init__(self):
        if not LITELLM_AVAILABLE:
            raise ImportError("LiteLLM is required but not available. Install with: pip install litellm")

        print("🚀 Initializing ISOLATED LiteLLM Unified Client")

        self.cost_manager = CostManager()
        self._current_text = None
        self._current_framework = None
        self.retry_handler = APIRetryHandler()
        self.failover_handler = ProviderFailoverHandler()
        self.tpm_limiter = TPMRateLimiter()

        self._configure_litellm()
        self._test_model_availability()

    def _configure_litellm(self):
        """Configure LiteLLM with unified settings and NATIVE RATE LIMITING"""
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

        # Configure LiteLLM global settings for NATIVE RATE LIMITING
        litellm.drop_params = True  # Drop unsupported params gracefully
        litellm.set_verbose = False  # Can be enabled for debugging

        # ENHANCED: Configure native rate limiting for faster experiments
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
        """
        Test all model connections (maintains DirectAPIClient interface)
        """
        test_models = {
            "openai": "gpt-3.5-turbo",
            "anthropic": "claude-3-5-haiku-20241022",
            "mistral": "mistral/mistral-small-latest",
            "vertex_ai": "vertex_ai/gemini-2.5-flash",  # Updated to latest
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

    def validate_corpus_for_models(self, corpus_dir: str, models: list, 
                                   experiment_def: Dict[str, Any]) -> Dict[str, Dict]:
        """
        INTELLIGENT CORPUS PRE-VALIDATION
        
        Validates corpus files against model capabilities BEFORE expensive API calls.
        Prevents costly failures and provides detailed compatibility reports.
        """
        if not self.tpm_limiter:
            return {"error": "TPM limiter not available for validation"}
        
        print(f"\n🔍 VALIDATING CORPUS COMPATIBILITY")
        print(f"📂 Corpus: {corpus_dir}")
        print(f"🤖 Models: {len(models)} flagship models")
        print("=" * 70)
        
        validation_results = {}
        corpus_files = []
        
        # Collect corpus files
        import os
        if os.path.isdir(corpus_dir):
            for filename in os.listdir(corpus_dir):
                if filename.endswith('.txt'):
                    file_path = os.path.join(corpus_dir, filename)
                    corpus_files.append((filename, file_path))
        
        if not corpus_files:
            return {"error": f"No .txt files found in {corpus_dir}"}
        
        # Validate each model against each file
        for model_name in models:
            model_results = {
                "compatible_files": [],
                "incompatible_files": [],
                "total_estimated_cost": 0.0,
                "total_estimated_time_minutes": 0.0
            }
            
            for filename, file_path in corpus_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text_content = f.read()
                    
                    # Validate compatibility
                    is_compatible, message = self.tpm_limiter.validate_corpus_compatibility(
                        text_content, model_name
                    )
                    
                    # Estimate cost
                    provider = self._get_provider_from_model(model_name)
                    estimated_cost, _, _ = self.cost_manager.estimate_cost(
                        text_content, provider, model_name
                    ) if self.cost_manager else (0.0, 0.0, 0.0)
                    
                    file_result = {
                        "filename": filename,
                        "compatible": is_compatible,
                        "message": message,
                        "estimated_cost": estimated_cost,
                        "file_size_chars": len(text_content),
                        "estimated_tokens": self.tpm_limiter.estimate_tokens(text_content, model_name)
                    }
                    
                    if is_compatible:
                        model_results["compatible_files"].append(file_result)
                        model_results["total_estimated_cost"] += estimated_cost
                        
                        # Rough time estimate based on TPM limits
                        tokens = file_result["estimated_tokens"] + 5000  # +prompt+output
                        tpm_limit = self.tpm_limiter.model_tpm_limits.get(model_name, 30000)
                        time_minutes = tokens / tpm_limit
                        model_results["total_estimated_time_minutes"] += time_minutes
                    else:
                        model_results["incompatible_files"].append(file_result)
                
                except Exception as e:
                    model_results["incompatible_files"].append({
                        "filename": filename,
                        "compatible": False,
                        "message": f"File read error: {e}",
                        "estimated_cost": 0.0
                    })
            
            validation_results[model_name] = model_results
            
            # Print model summary
            compatible_count = len(model_results["compatible_files"])
            incompatible_count = len(model_results["incompatible_files"])
            total_cost = model_results["total_estimated_cost"]
            total_time = model_results["total_estimated_time_minutes"]
            
            status_emoji = "✅" if incompatible_count == 0 else "⚠️" if compatible_count > 0 else "❌"
            print(f"{status_emoji} {model_name:<30} {compatible_count:>2}/{len(corpus_files)} files  "
                  f"${total_cost:>6.3f}  ~{total_time:>4.1f}m")
        
        # Summary statistics
        total_analyses = sum(len(results["compatible_files"]) for results in validation_results.values())
        total_cost = sum(results["total_estimated_cost"] for results in validation_results.values())
        total_time = sum(results["total_estimated_time_minutes"] for results in validation_results.values())
        
        print("=" * 70)
        print(f"📊 VALIDATION SUMMARY")
        print(f"   Total compatible analyses: {total_analyses}")
        print(f"   Estimated total cost: ${total_cost:.2f}")
        print(f"   Estimated total time: ~{total_time:.1f} minutes")
        
        # Check for critical issues
        completely_incompatible_models = [
            model for model, results in validation_results.items() 
            if len(results["compatible_files"]) == 0
        ]
        
        if completely_incompatible_models:
            print(f"⚠️  CRITICAL: Models with no compatible files: {completely_incompatible_models}")
        
        return {
            "validation_results": validation_results,
            "summary": {
                "total_analyses": total_analyses,
                "total_estimated_cost": total_cost,
                "total_estimated_time_minutes": total_time,
                "completely_incompatible_models": completely_incompatible_models
            }
        }

    def analyze_text(self, text: str, experiment_def: Dict[str, Any], model_name: str) -> Tuple[Dict[str, Any], float]:
        """
        Analyze text using an experiment definition file.
        """
        # Store context for quality assurance (preserved from DirectAPIClient)
        self._current_text = text
        self._current_framework = experiment_def.get("framework", {}).get("name", "unknown")

        # Generate prompt using the new PromptEngine
        prompt = create_prompt_from_experiment(experiment_def, text)
        
        # Store prompt for debugging (will be added to result)
        self._current_prompt = prompt

        # TPM Rate Limiting (preserved from DirectAPIClient)
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
        ENHANCED: Smart rate limiting based on model type
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

        # Use retry handler if available (preserved from DirectAPIClient)
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
        """LiteLLM call with retry logic and NATIVE rate limiting"""
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
                temperature=0.7,  # Increased for analytical variation - was 0.1
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
        """Basic LiteLLM call with NATIVE rate limiting (much faster!)"""
        # Track current model for parsing
        self._last_model_used = model_name
        
        try:
            # Dynamic timeout based on provider 
            provider = self._get_provider_from_model(model_name)
            timeout_duration = 300 if provider == "ollama" else 60  # 5 minutes for Ollama, 1 minute for others
            
            response = completion(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,  # Increased for analytical variation - was 0.1
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
        """Get provider name from model name (enhanced for Vertex AI and Ollama)"""
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
            return "vertex_ai"  # Default Gemini to Vertex AI now
        else:
            return "unknown"

    def _is_coordinate_free_response(self, content: str) -> bool:
        """
        Detect if response is in coordinate-free structured text format
        that should be handled by orchestrator instead of JSON parsing
        """
        if not content or not isinstance(content, str):
            return False
        
        content_stripped = content.strip()
        
        # Check for coordinate-free structured field indicators
        coordinate_free_patterns = [
            r'\[PRESENCE\]:', r'\[CONFIDENCE\]:', r'\[SCORE\]:', r'\[CORE_EVIDENCE\]:',
            r'\[DETAILED_ANALYSIS\]:', r'\[EDGE_CASES\]:', r'\[MINORITY_REPORT\]:',
            r'\[THEMATIC_OPPOSITION\]:', r'\[COEXISTENCE_AREAS\]:',
            r'\[COVERAGE\]:', r'\[THEMATIC_GAPS\]:', r'\[RELEVANCE\]:',
            'POPULISM:', 'PLURALISM:'
        ]
        
        # If any coordinate-free patterns are found, it's a coordinate-free response
        import re
        for pattern in coordinate_free_patterns:
            if re.search(pattern, content_stripped, re.IGNORECASE):
                return True
        
        # Check for discovery stage numbered responses (1., 2., 3., etc.)
        if re.search(r'^\s*\d+\.\s+', content_stripped, re.MULTILINE):
            return True
        
        return False

    def _parse_response(self, content: str, text_input: str = None, framework: str = None) -> Dict[str, Any]:
        """
        Parse LLM response using robust multi-strategy parsing
        ENHANCED: Uses RobustResponseParser to handle Claude "Extra data" issues
        COORDINATE-FREE FIX: Return raw response for structured text formats
        """
        
        # COORDINATE-FREE FIX: Check if this is a structured text response
        # that should be handled by coordinate-free orchestrator instead of JSON parsing
        if self._is_coordinate_free_response(content):
            return {
                "raw_response": content,
                "parsed": False,  # Signal that orchestrator should handle parsing
                "parsing_method": "coordinate_free_passthrough",
                "prompt_used": getattr(self, '_current_prompt', 'prompt_not_available')
            }
        
        from ..utils.robust_parser import parse_llm_response
        
        try:
            # Use the new robust parser with model name for debugging
            model_name = getattr(self, '_last_model_used', 'unknown')
            parsed_result = parse_llm_response(content, model_name)
            
            # Extract scores - handle both direct scores and nested format
            parsed_scores = parsed_result.get("scores", {})
            
            # Handle nested score format like {"Care": {"score": 0.8, "evidence": "..."}}
            normalized_scores = {}
            for key, value in parsed_scores.items():
                if isinstance(value, dict) and "score" in value:
                    normalized_scores[key] = value["score"]
                elif isinstance(value, (int, float)):
                    normalized_scores[key] = value
                else:
                    # Skip non-numeric scores
                    continue
            
            # Check if it's a hierarchical response (3-stage format) for backward compatibility
            if self._is_hierarchical_response(parsed_result):
                hierarchical_scores = self._extract_hierarchical_scores(parsed_result)
                if hierarchical_scores:
                    normalized_scores.update(hierarchical_scores)
            
            # Build final result
            result = {
                "scores": normalized_scores,
                "raw_response": content,
                "parsed": True,
                "parsing_method": parsed_result.get("parsing_method", "robust_parser"),
                "prompt_used": getattr(self, '_current_prompt', 'prompt_not_available')  # For debugging
            }
            
            # Add any additional analysis info from the parsed result
            for key, value in parsed_result.items():
                if key not in result and key != "scores":
                    result[key] = value
            
            return result
            
        except Exception as e:
            # For coordinate-free responses that failed JSON parsing, return raw
            if self._is_coordinate_free_response(content):
                print(f"🔄 Coordinate-free response detected after parse failure, returning raw for {getattr(self, '_last_model_used', 'unknown')}")
                return {
                    "raw_response": content,
                    "parsed": False,
                    "parsing_method": "coordinate_free_fallback",
                    "prompt_used": getattr(self, '_current_prompt', 'prompt_not_available')
                }
            
            # Final fallback to old parsing method
            print(f"⚠️ Robust parser failed for model {getattr(self, '_last_model_used', 'unknown')}: {e}")
            return self._parse_response_fallback(content, text_input, framework)

    def _is_hierarchical_response(self, response: Dict[str, Any]) -> bool:
        """Check if response is in hierarchical 3-stage format (preserved from DirectAPIClient)"""
        if not isinstance(response, dict):
            return False

        # Look for stage indicators
        stage_keys = ["stage_1", "stage_2", "stage_3", "stages"]
        return any(key in response for key in stage_keys)

    def _extract_hierarchical_scores(self, response: Dict[str, Any]) -> Dict[str, float]:
        """Extract scores from hierarchical response format (preserved from DirectAPIClient)"""
        scores = {}

        # Try different hierarchical formats
        if "stage_3" in response and isinstance(response["stage_3"], dict):
            stage_3 = response["stage_3"]
            if "scores" in stage_3:
                scores.update(stage_3["scores"])
            elif "final_scores" in stage_3:
                scores.update(stage_3["final_scores"])

        elif "stages" in response and isinstance(response["stages"], dict):
            stages = response["stages"]
            if "final" in stages or "stage_3" in stages:
                final_stage = stages.get("final", stages.get("stage_3", {}))
                if isinstance(final_stage, dict) and "scores" in final_stage:
                    scores.update(final_stage["scores"])

        # Fallback: look for any scores in the response
        if not scores and "scores" in response:
            scores.update(response["scores"])

        return scores

    def _extract_narrative_scores(self, content: str) -> Dict[str, Any]:
        """Extract narrative scores from text format (preserved from DirectAPIClient)"""
        import re

        scores = {}

        # Try to find JSON-like structures in the text
        json_pattern = r"\{[^{}]*\}"
        json_matches = re.findall(json_pattern, content)

        for match in json_matches:
            try:
                parsed = json.loads(match)
                if isinstance(parsed, dict):
                    scores.update(parsed)
            except:
                continue

        # Try to find key-value pairs
        kv_pattern = r"(\w+):\s*([0-9]*\.?[0-9]+)"
        kv_matches = re.findall(kv_pattern, content)

        for key, value in kv_matches:
            try:
                scores[key] = float(value)
            except:
                continue

        return scores
    
    def _parse_response_fallback(self, content: str, text_input: str = None, framework: str = None) -> Dict[str, Any]:
        """
        Fallback parsing method using original logic
        Used when robust parser fails
        """
        raw_response = {}
        parsed_scores = {}

        try:
            # Try to parse as JSON first
            raw_response = json.loads(content)

            # Check if it's a hierarchical response (3-stage format)
            if self._is_hierarchical_response(raw_response):
                # Convert hierarchical format to simple format
                parsed_scores = self._extract_hierarchical_scores(raw_response)
            else:
                # Handle simple format
                parsed_scores = raw_response.get("scores", {})

        except json.JSONDecodeError:
            # Fallback: extract scores from text format
            parsed_scores = self._extract_narrative_scores(content)

        return {
            "scores": parsed_scores, 
            "raw_response": content, 
            "parsed": True,
            "parsing_method": "fallback"
        }

    def get_available_models(self) -> Dict[str, list]:
        """
        Get available models by provider (maintains DirectAPIClient interface)
        Enhanced to include Ollama local models
        """
        models = {
            "openai": [
                "gpt-4o",
                "gpt-4o-mini",
                "gpt-3.5-turbo",
                "gpt-4-turbo",
                "o1-preview",
                "o1-mini",
                "gpt-4.1-mini",
            ],
            "anthropic": [
                "claude-3-5-sonnet-20241022",
                "claude-3-5-haiku-20241022",
                "claude-3-opus-20240229",
                "claude-3-sonnet-20240229",
            ],
            "mistral": [
                "mistral/mistral-large-latest",
                "mistral/mistral-medium-latest",
                "mistral/mistral-small-latest",
                "mistral/codestral-latest",
                "mistral/mistral-tiny",
            ],
            "google_ai": ["gemini-2.5-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
            "ollama": [],  # Will be populated dynamically
        }

        # Get available Ollama models dynamically
        try:
            import requests

            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                ollama_data = response.json()
                for model_info in ollama_data.get("models", []):
                    model_name = model_info.get("name", "")
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
