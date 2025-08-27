#!/usr/bin/env python3
"""
LLM Gateway
===========

THIN Principle: This component is a pure, stateless execution gateway. It takes a
prompt and a specific model identifier and executes the call. It has no knowledge
of model capabilities, costs, or fallback logic.
"""

import litellm
from litellm.cost_calculator import completion_cost
from typing import Dict, Any, Tuple, List, Optional, Callable
from .model_registry import ModelRegistry
from .provider_parameter_manager import ProviderParameterManager
import time
import os
import asyncio
from .base_gateway import BaseGateway

# Add moderation import
from litellm import moderation

# Add rate limiting import
from ratelimit import limits, RateLimitException

# LLMArchiveManager was removed during cleanup - functionality moved to agents
# from discernus.core.llm_archive_manager import LLMArchiveManager

import json
from ..core.logging_config import get_logger


class LLMGateway(BaseGateway):
    """
    A unified gateway for making calls to various Large Language Models (LLMs)
    through the LiteLLM library. It includes logic for intelligent model fallback
    in case of failures.
    """
    def __init__(self, model_registry: ModelRegistry):
        """
        Initialize the gateway.
        
        Args:
            model_registry: An instance of ModelRegistry.
        """
        self.model_registry = model_registry
        self.param_manager = ProviderParameterManager()
        self.logger = get_logger("llm_gateway")
        
        # Create rate-limited completion functions per provider
        self._rate_limited_completions = self._create_rate_limiters()

    def _create_rate_limiters(self) -> Dict[str, Callable]:
        """
        Create rate-limited completion functions per provider using the ratelimit library.
        Uses rate limits from models.yaml provider_defaults or individual model specifications.
        """
        limiters = {}
        
        for provider, config in self.param_manager.provider_defaults.items():
            # Get RPM limit from provider defaults or use conservative default
            rpm_limit = config.get('default_rpm_limit', 60)
            
            # Handle None values (e.g., for vertex_ai DSQ providers)
            if rpm_limit is None:
                # No rate limiting for providers with None limits (Dynamic Shared Quota)
                limiters[provider] = litellm.completion
            else:
                # Create a rate-limited completion function for this provider
                @limits(calls=rpm_limit, period=60)  # RPM limit over 60 seconds
                def rate_limited_completion(model: str, messages: List[Dict], **kwargs):
                    return litellm.completion(model=model, messages=messages, **kwargs)
                
                limiters[provider] = rate_limited_completion
        
        return limiters

    def _get_rate_limited_completion(self, model: str) -> Callable:
        """
        Get the appropriate rate-limited completion function for a model.
        Falls back to unrestricted litellm.completion if no rate limiter is configured.
        """
        provider = self.param_manager.get_provider_from_model(model)
        return self._rate_limited_completions.get(provider, litellm.completion)

    def execute_call(self, model: str, prompt: str, system_prompt: str = "You are a helpful assistant.", max_retries: int = 3, response_schema: Optional[Dict[str, Any]] = None, **kwargs) -> Tuple[str, Dict[str, Any]]:
        """
        Executes a call to an LLM provider via LiteLLM, with intelligent fallback.
        """
        current_model = model
        attempts = 0

        while attempts < max_retries:
            attempts += 1
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]

            try:
                # --- Moderation Guardrail ---
                provider = self.param_manager.get_provider_from_model(current_model)
                provider_config = self.param_manager.provider_defaults.get(provider, {})
                
                if provider_config.get("requires_pre_moderation"):
                    mod_response = moderation(input=prompt)
                    if mod_response and mod_response.results and mod_response.results[0].flagged:
                        categories = mod_response.results[0].categories
                        flagged_categories = []
                        if categories:
                            flagged_categories = [category for category, flagged in categories.items() if flagged]
                        error_msg = f"Prompt flagged by moderation API for categories: {', '.join(flagged_categories)}"
                        
                        return None, {"success": False, "error": error_msg, "model": current_model, "attempts": attempts}

                print(f"Attempting call with {current_model} (Attempt {attempts}/{max_retries})...")
                
                # Clean parameters based on provider requirements
                call_kwargs = kwargs.copy()
                if response_schema:
                    call_kwargs['response_format'] = {
                        "type": "json_object",
                        "schema": response_schema
                    }

                clean_params = self.param_manager.get_clean_parameters(current_model, call_kwargs)
                
                # Use rate-limited completion function for this provider
                completion_func = self._get_rate_limited_completion(current_model)
                response = completion_func(model=current_model, messages=messages, stream=False, **clean_params)
                
                # Extract content from response
                content = getattr(getattr(getattr(response, 'choices', [{}])[0], 'message', {}), 'content', '') or ""
                
                # If the response is a JSON string, parse it for structured output
                if isinstance(content, str) and content.strip().startswith('{'):
                    try:
                        parsed_content = json.loads(content)
                        content = parsed_content
                    except json.JSONDecodeError as e:
                        # Not a valid JSON string, leave content as is
                        pass

                usage_obj = getattr(response, 'usage', None)
                
                # Extract cost data from LiteLLM response
                response_cost = 0.0
                cost_debug_info = {}
                try:
                    # LiteLLM provides cost in response._hidden_params["response_cost"]
                    hidden_params = getattr(response, '_hidden_params', {})
                    response_cost = hidden_params.get('response_cost', 0.0)
                    cost_debug_info['hidden_params_cost'] = response_cost
                    # Success case - no need to print, cost tracking working
                except Exception as e:
                    cost_debug_info['hidden_params_error'] = str(e)
                    # Fallback: calculate cost using LiteLLM's completion_cost function
                    try:
                        response_cost = completion_cost(completion_response=response)
                        cost_debug_info['completion_cost'] = response_cost
                    except Exception as e2:
                        cost_debug_info['completion_cost_error'] = str(e2)
                        response_cost = 0.0
                        print(f"⚠️ Cost calculation failed for {current_model}: hidden_params={e}, completion_cost={e2}")
                
                if response_cost == 0.0 and usage_obj:
                    print(f"⚠️ Zero cost detected for {current_model} with tokens: {getattr(usage_obj, 'total_tokens', 0)}")
                
                usage_data = {
                    "prompt_tokens": getattr(usage_obj, 'prompt_tokens', 0) if usage_obj else 0,
                    "completion_tokens": getattr(usage_obj, 'completion_tokens', 0) if usage_obj else 0,
                    "total_tokens": getattr(usage_obj, 'total_tokens', 0) if usage_obj else 0,
                    "response_cost_usd": response_cost
                }
                
                if "flash" in current_model.lower():
                    self.logger.debug(f"Full successful response from {current_model}:\n{content}")

                return content, {"success": True, "model": current_model, "usage": usage_data, "attempts": attempts}
            
            except litellm.exceptions.APIConnectionError as e:
                print(f"⚠️ APIConnectionError with {current_model}: {e}. Retrying after delay...")
                time.sleep(2)
                continue

            except litellm.exceptions.RateLimitError as e:
                print(f"⚠️ RateLimitError with {current_model}: {e}. Implementing exponential backoff...")
                # Exponential backoff: 2^attempt seconds, max 60 seconds
                backoff_delay = min(2 ** attempts, 60)
                print(f"⏳ Waiting {backoff_delay} seconds before retry...")
                time.sleep(backoff_delay)
                continue

            except RateLimitException as e:
                print(f"⚠️ Proactive rate limit reached for {current_model}: {e}. Waiting...")
                # Simple 1-second wait for proactive rate limiting
                time.sleep(1)
                continue

            except Exception as e:
                print(f"❌ Unhandled exception with {current_model}: {e}. Attempting fallback.")
                fallback_model = self.model_registry.get_fallback_model(current_model)
                if fallback_model:
                    print(f"Retrying with fallback model: {fallback_model}")
                    current_model = fallback_model
                else:
                    error_msg = f"All fallbacks failed. Last error on {current_model}: {str(e)}"
                    
                    return None, {"success": False, "error": error_msg, "model": current_model, "attempts": attempts}
        
        # Archive final max retries failure
        final_error = f"Max retries exceeded for {model}"
        return None, {"success": False, "error": final_error, "model": current_model, "attempts": max_retries}

    async def check_model_health(self, model_name: str) -> Dict[str, Any]:
        """
        Checks the health of a single model by attempting a simple completion.
        """
        try:
            # Attempt a very basic completion to check if the model is responsive
            # This is a very basic check and might not cover all potential issues
            # A more robust health check would involve model-specific parameters
            # and potentially a more complex prompt.
            messages = [{"role": "user", "content": "Hello, model!"}]
            clean_params = self.param_manager.get_clean_parameters(model_name, {}) # Assuming no specific parameters needed for this basic check
            
            # Use rate-limited completion function for health checks too
            completion_func = self._get_rate_limited_completion(model_name)
            completion_func(model=model_name, messages=messages, stream=False, **clean_params)
            
            # If the call completes without an exception, we consider it healthy.
            return {'is_healthy': True, 'message': 'Model is responsive.'}
        except litellm.exceptions.APIConnectionError as e:
            return {'is_healthy': False, 'message': f'APIConnectionError: {e}'}
        except RateLimitException as e:
            return {'is_healthy': False, 'message': f'Rate limit reached during health check: {e}'}
        except Exception as e:
            # Fallback for any other unexpected errors
            print(f"ERROR: An unexpected error occurred during health check for {model_name}: {e}")
            return {'is_healthy': False, 'message': f'Unexpected error: {str(e)}'}

    async def check_many_models_health(self, model_names: List[str]) -> Dict[str, Any]:
        """
        Checks the health of multiple models concurrently.
        """
        tasks = [self.check_model_health(model_name) for model_name in model_names]
        results = await asyncio.gather(*tasks)
        
        return {
            "status": "completed",
            "results": {model_name: result for model_name, result in zip(model_names, results)}
        }

    def _get_model_from_registry(self, model_name: str) -> Optional[Dict[str, Any]]:
        """Helper to get model details from the registry."""
        return self.model_registry.get_model_details(model_name)

if __name__ == '__main__':
    # Demo of how to use the LLMGateway
    registry = ModelRegistry()
    gateway = LLMGateway(registry, gcp_project_id="your-gcp-project-id")
    
    print("Executing call with Claude Haiku...")
    response, metadata = gateway.execute_call(
        model="claude-3-haiku-20240307",
        prompt="Tell me a short story about a robot who learns to paint."
    )
    
    print("\nResponse:")
    print(response)
    
    print("\nMetadata:")
    print(metadata) 