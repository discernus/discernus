#!/usr/bin/env python3
"""
LLM Gateway
===========

THIN Principle: This component is a pure, stateless execution gateway. It takes a
prompt and a specific model identifier and executes the call. It has no knowledge
of model capabilities, costs, or fallback logic.
"""

import litellm
from typing import Dict, Any, Tuple
from .model_registry import ModelRegistry
import time
import os

class LLMGateway:
    """
    A unified gateway for making calls to various Large Language Models (LLMs)
    through the LiteLLM library. It includes logic for intelligent model fallback
    in case of failures.
    """
    def __init__(self, model_registry: ModelRegistry):
        self.model_registry = model_registry

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
                response = litellm.completion(model=current_model, messages=messages, stream=False, **kwargs)
                
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