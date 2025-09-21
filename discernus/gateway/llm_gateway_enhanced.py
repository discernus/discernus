#!/usr/bin/env python3
"""
Enhanced LLM Gateway with Tool Calling Support
==============================================

Extends the base LLM Gateway with tool calling capabilities for the
Show Your Work architecture.
"""

import json
from typing import Dict, Any, Tuple, List, Optional
from .llm_gateway import LLMGateway

class EnhancedLLMGateway(LLMGateway):
    
    def execute_call_with_tools(self, model: str, prompt: str, system_prompt: str = "You are a helpful assistant.",
                               tools: List[Dict[str, Any]] = None, max_retries: int = 3,
                               context: Optional[str] = None, force_function_calling: bool = False, **kwargs) -> Tuple[str, Dict[str, Any]]:
        """
        Executes a call to an LLM provider with tool calling support.
        
        Args:
            model: The identifier of the model to use
            prompt: The user prompt
            system_prompt: The system prompt
            tools: List of tool definitions for function calling
            max_retries: Maximum number of retry attempts
            context: Optional context for progress messages
            force_function_calling: If True, forces the model to make function calls (ANY mode)
            **kwargs: Additional parameters for the LLM call
            
        Returns:
            Tuple of (response_content, metadata)
        """
        import litellm
        from litellm.cost_calculator import completion_cost
        import time
        from datetime import datetime
        from ..core.logging_config import get_logger
        from ..core.unified_logger import get_unified_logger
        
        current_model = model
        attempts = 0
        
        while attempts < max_retries:
            attempts += 1
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            try:
                # Enhanced progress message with context
                from ..core.unified_logger import get_unified_logger
                unified_logger = get_unified_logger()
                
                if context:
                    unified_logger.llm_call(current_model, attempts, max_retries, context=context)
                else:
                    unified_logger.llm_call(current_model, attempts, max_retries)
                
                # Clean parameters based on provider requirements
                call_kwargs = kwargs.copy()
                if tools:
                    call_kwargs['tools'] = tools
                    if force_function_calling:
                        # Force the model to make function calls (ANY mode)
                        call_kwargs['tool_choice'] = "required"
                    else:
                        # Let the model decide when to use tools (AUTO mode)
                        call_kwargs['tool_choice'] = "auto"
                
                clean_params = self.param_manager.get_clean_parameters(current_model, call_kwargs)
                
                # Log detailed LLM interaction request
                llm_logger = get_logger("llm_interactions")
                
                request_data = {
                    "model": current_model,
                    "messages": messages,
                    "tools": tools,
                    "clean_params": clean_params,
                    "attempt": attempts,
                    "timestamp": datetime.now().isoformat()
                }
                llm_logger.info("LLM Tool Call Request", extra={"llm_request": request_data})
                
                # Use rate-limited completion function for this provider
                completion_func = self._get_rate_limited_completion(current_model)
                response = completion_func(model=current_model, messages=messages, stream=False, **clean_params)
                
                # Extract content and tool calls from response
                message = getattr(getattr(response, 'choices', [{}])[0], 'message', {})
                content = getattr(message, 'content', '') or ""
                tool_calls = getattr(message, 'tool_calls', [])
                
                # Log detailed LLM interaction response
                response_data = {
                    "model": current_model,
                    "response_type": type(response).__name__,
                    "response_content": content,
                    "tool_calls": tool_calls,
                    "response_content_length": len(str(content)),
                    "usage": getattr(response, 'usage', None).__dict__ if getattr(response, 'usage', None) else None,
                    "attempt": attempts,
                    "timestamp": datetime.now().isoformat()
                }
                llm_logger.info("LLM Tool Call Response", extra={"llm_response": response_data})
                
                # Extract cost data from LiteLLM response
                usage_obj = getattr(response, 'usage', None)
                response_cost = 0.0
                try:
                    hidden_params = getattr(response, '_hidden_params', {})
                    response_cost = hidden_params.get('response_cost', 0.0)
                except Exception:
                    try:
                        response_cost = completion_cost(completion_response=response)
                    except Exception:
                        response_cost = 0.0
                
                usage_data = {
                    "prompt_tokens": getattr(usage_obj, 'prompt_tokens', 0) if usage_obj else 0,
                    "completion_tokens": getattr(usage_obj, 'completion_tokens', 0) if usage_obj else 0,
                    "total_tokens": getattr(usage_obj, 'total_tokens', 0) if usage_obj else 0,
                    "response_cost_usd": response_cost
                }
                
                return response, {
                    "success": True, 
                    "model": current_model, 
                    "usage": usage_data, 
                    "attempts": attempts,
                    "tool_calls": tool_calls
                }
                
            except Exception as e:
                unified_logger.error(f"Tool call failed with {current_model}: {e}", critical=True)
                if attempts < max_retries:
                    time.sleep(2)
                    continue
                else:
                    return None, {"success": False, "error": str(e), "model": current_model, "attempts": attempts}
        
        return None, {"success": False, "error": "Max retries exceeded", "model": current_model, "attempts": attempts}
