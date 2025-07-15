#!/usr/bin/env python3
"""
LLM Gateway
===========

THIN Principle: This component is a pure, stateless execution gateway. It takes a
prompt and a specific model identifier and executes the call. It has no knowledge
of model capabilities, costs, or fallback logic.
"""

import litellm
from typing import Dict, Any, Tuple, List, Optional
from .model_registry import ModelRegistry
from .provider_parameter_manager import ProviderParameterManager
import time
import os
import asyncio

class LLMGateway:
    """
    A unified gateway for making calls to various Large Language Models (LLMs)
    through the LiteLLM library. It includes logic for intelligent model fallback
    in case of failures.
    """
    def __init__(self, model_registry: ModelRegistry):
        self.model_registry = model_registry
        self.parameter_manager = ProviderParameterManager()

    def execute_call(self, model: str, prompt: str, system_prompt: str = "You are a helpful assistant.", max_retries: int = 3, **kwargs) -> Tuple[str, Dict[str, Any]]:
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
                print(f"Attempting call with {current_model} (Attempt {attempts}/{max_retries})...")
                
                # Clean parameters based on provider requirements
                clean_params = self.parameter_manager.get_clean_parameters(current_model, kwargs)
                
                response = litellm.completion(model=current_model, messages=messages, stream=False, **clean_params)
                
                content = getattr(getattr(getattr(response, 'choices', [{}])[0], 'message', {}), 'content', '') or ""
                usage_obj = getattr(response, 'usage', None)
                usage_data = {
                    "prompt_tokens": getattr(usage_obj, 'prompt_tokens', 0) if usage_obj else 0,
                    "completion_tokens": getattr(usage_obj, 'completion_tokens', 0) if usage_obj else 0,
                    "total_tokens": getattr(usage_obj, 'total_tokens', 0) if usage_obj else 0
                }
                
                return content, {"success": True, "model": current_model, "usage": usage_data, "attempts": attempts}
            
            except litellm.exceptions.APIConnectionError as e:
                print(f"⚠️ APIConnectionError with {current_model}: {e}. Retrying after delay...")
                time.sleep(2)
                continue

            except Exception as e:
                print(f"❌ Unhandled exception with {current_model}: {e}. Attempting fallback.")
                fallback_model = self.model_registry.get_fallback_model(current_model)
                if fallback_model:
                    print(f"Retrying with fallback model: {fallback_model}")
                    current_model = fallback_model
                else:
                    return "", {"success": False, "error": f"All fallbacks failed. Last error on {current_model}: {str(e)}", "model": current_model, "attempts": attempts}
        
        return "", {"success": False, "error": f"Max retries exceeded for {model}", "model": current_model, "attempts": max_retries}

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
            clean_params = self.parameter_manager.get_clean_parameters(model_name, {}) # Assuming no specific parameters needed for this basic check
            litellm.completion(model=model_name, messages=messages, stream=False, **clean_params)
            
            # If the call completes without an exception, we consider it healthy.
            return {'is_healthy': True, 'message': 'Model is responsive.'}
        except litellm.exceptions.APIConnectionError as e:
            return {'is_healthy': False, 'message': f'APIConnectionError: {e}'}
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
    gateway = LLMGateway(registry)
    
    print("Executing call with Claude Haiku...")
    response, metadata = gateway.execute_call(
        model="claude-3-haiku-20240307",
        prompt="Tell me a short story about a robot who learns to paint."
    )
    
    print("\nResponse:")
    print(response)
    
    print("\nMetadata:")
    print(metadata) 