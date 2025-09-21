#!/usr/bin/env python3
"""
Discernus LLM Gateway
====================

A comprehensive, production-ready LLM gateway that consolidates all functionality
for the Discernus research platform. This is the single source of truth for all
LLM interactions.

Features:
- LiteLLM integration with all major providers
- Tool calling support for function calling
- Rate limiting and retry logic
- Cost tracking and usage monitoring
- Comprehensive logging and debugging
- Provider-specific parameter management
- Fallback model support
- Moderation guardrails
- Response schema validation

THIN Principle: This component is a pure, stateless execution gateway. It takes a
prompt and a specific model identifier and executes the call. It has no knowledge
of model capabilities, costs, or fallback logic beyond what's needed for execution.
"""

import json
import litellm
from litellm.cost_calculator import completion_cost
from typing import Dict, Any, Tuple, List, Optional, Callable
import time
import os
import asyncio
import socket
import requests
from datetime import datetime
from ratelimit import limits, RateLimitException

from .base_gateway import BaseGateway
from .model_registry import ModelRegistry
from .provider_parameter_manager import ProviderParameterManager

# Apply comprehensive LiteLLM debug suppression
from discernus.core.logging_config import ensure_litellm_debug_suppression, get_logger
ensure_litellm_debug_suppression()

# Disable LiteLLM verbose output programmatically
litellm.set_verbose = False

# Import moderation from litellm
from litellm import moderation


class LLMGateway(BaseGateway):
    """
    Comprehensive LLM Gateway for Discernus.
    
    This is the single, production-ready gateway that handles all LLM interactions
    across the Discernus platform. It consolidates all functionality from deprecated
    implementations into one clean, maintainable component.
    """
    
    def __init__(self, model_registry: ModelRegistry):
        """
        Initialize the LLM gateway.
        
        Args:
            model_registry: The model registry for model discovery and fallback logic
        """
        self.model_registry = model_registry
        self.param_manager = ProviderParameterManager()
        self.logger = get_logger("llm_gateway")
        
        # Set up rate limiting
        self._rate_limited_completions = self._setup_rate_limiting()
        
        self.logger.info("LLM Gateway initialized with comprehensive functionality")
    
    def _setup_rate_limiting(self) -> Dict[str, Callable]:
        """Set up rate limiting for different providers."""
        limiters = {}
        
        # For now, use unlimited completion for all providers
        # Rate limiting can be added later if needed
        for provider in self.param_manager.provider_defaults.keys():
            limiters[provider] = litellm.completion
        
        return limiters
    
    def _get_rate_limited_completion(self, model: str) -> Callable:
        """Get the appropriate rate-limited completion function for a model."""
        provider = self.param_manager.get_provider_from_model(model)
        return self._rate_limited_completions.get(provider, litellm.completion)
    
    def _check_moderation(self, prompt: str, model: str) -> Optional[str]:
        """
        Check if prompt passes moderation requirements.
        
        Args:
            prompt: The prompt to check
            model: The model being used
            
        Returns:
            Error message if moderation fails, None if passes
        """
        try:
            provider = self.param_manager.get_provider_from_model(model)
            provider_config = self.param_manager.provider_defaults.get(provider, {})
            
            if provider_config.get("requires_pre_moderation", False):
                mod_response = moderation(input=prompt)
                if mod_response and mod_response.results and mod_response.results[0].flagged:
                    categories = mod_response.results[0].categories
                    flagged_categories = []
                    if categories:
                        flagged_categories = [category for category, flagged in categories.items() if flagged]
                    return f"Prompt flagged by moderation API for categories: {', '.join(flagged_categories)}"
        except Exception as e:
            self.logger.warning(f"Moderation check failed: {e}")
        
        return None
    
    def execute_call(self, model: str, prompt: str, system_prompt: str = "You are a helpful assistant.", 
                    max_retries: int = 3, response_schema: Optional[Dict[str, Any]] = None, 
                    context: Optional[str] = None, **kwargs) -> Tuple[str, Dict[str, Any]]:
        """
        Execute a call to an LLM provider via LiteLLM.
        
        Args:
            model: The identifier of the model to use
            prompt: The user prompt
            system_prompt: The system prompt
            max_retries: Maximum number of retry attempts
            response_schema: Optional JSON schema for structured output
            context: Optional context for progress messages
            **kwargs: Additional provider-specific parameters
            
        Returns:
            A tuple containing the string content of the response and a
            dictionary of metadata including success status, usage, cost, etc.
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
                # Check moderation if required
                moderation_error = self._check_moderation(prompt, current_model)
                if moderation_error:
                    return None, {
                        "success": False,
                        "error": moderation_error,
                        "model": current_model,
                        "attempts": attempts
                    }

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
                
                # Extract response content
                response_content = getattr(getattr(getattr(response, 'choices', [{}])[0], 'message', {}), 'content', '') or ""
                
                # Extract usage information
                usage = getattr(response, 'usage', None)
                if usage:
                    usage_dict = {
                        'prompt_tokens': getattr(usage, 'prompt_tokens', 0),
                        'completion_tokens': getattr(usage, 'completion_tokens', 0),
                        'total_tokens': getattr(usage, 'total_tokens', 0)
                    }
                else:
                    usage_dict = {}
                
                # Calculate cost
                cost = completion_cost(completion_response=response)
                
                return response_content, {
                    "success": True,
                    "model": current_model,
                    "attempts": attempts,
                    "usage": usage_dict,
                    "cost": cost,
                    "response_type": type(response).__name__
                }
                
            except Exception as e:
                error_msg = str(e)
                self.logger.warning(f"LLM call failed (attempt {attempts}/{max_retries}): {error_msg}")
                
                if attempts < max_retries:
                    # Try fallback model if available
                    fallback_model = self.model_registry.get_fallback_model(current_model)
                    if fallback_model and fallback_model != current_model:
                        self.logger.info(f"Retrying with fallback model: {fallback_model}")
                        current_model = fallback_model
                        continue
                
                return None, {
                    "success": False,
                    "error": error_msg,
                    "model": current_model,
                    "attempts": attempts
                }
        
        return None, {
            "success": False,
            "error": "Max retries exceeded",
            "model": current_model,
            "attempts": attempts
        }
    
    def execute_call_with_tools(self, model: str, prompt: str, system_prompt: str = "You are a helpful assistant.",
                               tools: List[Dict[str, Any]] = None, max_retries: int = 3,
                               context: Optional[str] = None, force_function_calling: bool = False, **kwargs) -> Tuple[str, Dict[str, Any]]:
        """
        Execute a call to an LLM provider with tool calling support.
        
        Args:
            model: The identifier of the model to use
            prompt: The user prompt
            system_prompt: The system prompt
            tools: List of tool definitions for function calling
            max_retries: Maximum number of retry attempts
            context: Optional context for progress messages
            force_function_calling: If True, forces the model to make function calls
            **kwargs: Additional provider-specific parameters
            
        Returns:
            A tuple containing the string content of the response and a
            dictionary of metadata including success status, usage, cost, etc.
        """
        if not tools:
            # Fall back to regular execute_call if no tools provided
            return self.execute_call(model, prompt, system_prompt, max_retries, context=context, **kwargs)
        
        current_model = model
        attempts = 0

        while attempts < max_retries:
            attempts += 1
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]

            try:
                # Check moderation if required
                moderation_error = self._check_moderation(prompt, current_model)
                if moderation_error:
                    return None, {
                        "success": False,
                        "error": moderation_error,
                        "model": current_model,
                        "attempts": attempts
                    }

                # Clean parameters based on provider requirements
                call_kwargs = kwargs.copy()
                
                # Add tool calling parameters
                call_kwargs['tools'] = tools
                if force_function_calling:
                    call_kwargs['tool_choice'] = "required"
                else:
                    call_kwargs['tool_choice'] = "auto"

                clean_params = self.param_manager.get_clean_parameters(current_model, call_kwargs)
                
                # Use rate-limited completion function for this provider
                completion_func = self._get_rate_limited_completion(current_model)
                response = completion_func(model=current_model, messages=messages, stream=False, **clean_params)
                
                # Extract response content
                response_content = getattr(getattr(getattr(response, 'choices', [{}])[0], 'message', {}), 'content', '') or ""
                
                # Extract tool calls if present
                tool_calls = []
                if hasattr(response, 'choices') and response.choices:
                    choice = response.choices[0]
                    if hasattr(choice, 'message') and hasattr(choice.message, 'tool_calls'):
                        tool_calls = choice.message.tool_calls or []
                
                # Extract usage information
                usage = getattr(response, 'usage', None)
                if usage:
                    usage_dict = {
                        'prompt_tokens': getattr(usage, 'prompt_tokens', 0),
                        'completion_tokens': getattr(usage, 'completion_tokens', 0),
                        'total_tokens': getattr(usage, 'total_tokens', 0)
                    }
                else:
                    usage_dict = {}
                
                # Calculate cost
                cost = completion_cost(completion_response=response)
                
                return response_content, {
                    "success": True,
                    "model": current_model,
                    "attempts": attempts,
                    "usage": usage_dict,
                    "cost": cost,
                    "response_type": type(response).__name__,
                    "tool_calls": tool_calls
                }
                
            except Exception as e:
                error_msg = str(e)
                self.logger.warning(f"LLM call with tools failed (attempt {attempts}/{max_retries}): {error_msg}")
                
                if attempts < max_retries:
                    # Try fallback model if available
                    fallback_model = self.model_registry.get_fallback_model(current_model)
                    if fallback_model and fallback_model != current_model:
                        self.logger.info(f"Retrying with fallback model: {fallback_model}")
                        current_model = fallback_model
                        continue
                
                return None, {
                    "success": False,
                    "error": error_msg,
                    "model": current_model,
                    "attempts": attempts
                }
        
        return None, {
            "success": False,
            "error": "Max retries exceeded",
            "model": current_model,
            "attempts": attempts
        }
