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

class LLMGateway:
    """
    A stateless gateway for executing LLM calls via LiteLLM.
    """

    def __init__(self):
        # The gateway itself is stateless and requires no initialization
        pass

    def execute_call(self, model: str, prompt: str, system_prompt: str = "You are a helpful assistant.") -> Tuple[str, Dict[str, Any]]:
        """
        Executes a single, direct call to a specified LLM.

        Args:
            model: The exact model identifier to use (e.g., "claude-3-5-sonnet-20240620").
            prompt: The user prompt for the model.
            system_prompt: The system prompt to set the model's persona.

        Returns:
            A tuple containing the raw response string and a metadata dictionary.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]

        try:
            response = litellm.completion(model=model, messages=messages, stream=False)
            
            # Extract content and usage with runtime attribute access
            content = getattr(getattr(getattr(response, 'choices', [{}])[0], 'message', {}), 'content', '') or ""
            
            usage_obj = getattr(response, 'usage', None)
            usage_data = {
                "prompt_tokens": getattr(usage_obj, 'prompt_tokens', 0) if usage_obj else 0,
                "completion_tokens": getattr(usage_obj, 'completion_tokens', 0) if usage_obj else 0,
                "total_tokens": getattr(usage_obj, 'total_tokens', 0) if usage_obj else 0
            }
            
            return content, {
                "success": True,
                "model": model,
                "usage": usage_data
            }
            
        except Exception as e:
            error_message = f"LLM call failed for model {model}: {str(e)}"
            print(f"❌ {error_message}")
            return "", {"success": False, "error": error_message, "model": model}

if __name__ == '__main__':
    # Demo of how to use the LLMGateway
    gateway = LLMGateway()
    
    print("Executing call with Claude Haiku...")
    response, metadata = gateway.execute_call(
        model="claude-3-haiku-20240307",
        prompt="Tell me a short story about a robot who learns to paint."
    )
    
    print("\nResponse:")
    print(response)
    
    print("\nMetadata:")
    print(metadata) 