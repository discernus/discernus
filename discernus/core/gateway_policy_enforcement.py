#!/usr/bin/env python3
"""
Gateway Policy Enforcement
=========================

Enforces the policy that all LLM calls must go through the project gateway,
preventing direct model client instantiation in agents.
"""

import functools
import inspect
from typing import Any, Callable, Dict, List, Set
import warnings


# Track allowed model client imports
ALLOWED_MODEL_IMPORTS = {
    'discernus.gateway.llm_gateway',
    'discernus.gateway.enhanced_llm_gateway', 
    'discernus.gateway.model_registry',
    'discernus.gateway.llm_client_factory'
}

# Track forbidden model client imports
FORBIDDEN_MODEL_IMPORTS = {
    'openai',
    'anthropic',
    'google.generativeai',
    'vertexai',
    'cohere',
    'replicate',
    'huggingface_hub'
}

# Track forbidden model client classes
FORBIDDEN_MODEL_CLASSES = {
    'OpenAI',
    'Anthropic',
    'GenerativeModel',
    'VertexAI',
    'Cohere',
    'Replicate',
    'HuggingFaceHub'
}


def enforce_gateway_policy(func: Callable) -> Callable:
    """
    Decorator that enforces gateway policy by checking for forbidden model client usage.
    
    This decorator scans the function's source code for:
    1. Forbidden imports (openai, anthropic, etc.)
    2. Direct model client instantiation
    3. Bypassing the gateway system
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function with policy enforcement
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Check for policy violations
        violations = _check_gateway_policy_violations(func)
        
        if violations:
            violation_messages = []
            for violation in violations:
                violation_messages.append(f"  - {violation}")
            
            error_msg = (
                f"Gateway policy violation in {func.__name__}:\n"
                f"All LLM calls must go through the project gateway.\n"
                f"Violations found:\n" + "\n".join(violation_messages) + "\n"
                f"Use LLMGateway or EnhancedLLMGateway instead."
            )
            
            warnings.warn(error_msg, UserWarning, stacklevel=2)
        
        return func(*args, **kwargs)
    
    return wrapper


def _check_gateway_policy_violations(func: Callable) -> List[str]:
    """
    Check for gateway policy violations in a function.
    
    Args:
        func: Function to check
        
    Returns:
        List of violation messages
    """
    violations = []
    
    try:
        # Get function source code
        source = inspect.getsource(func)
        source_lines = source.split('\n')
        
        # Check for forbidden imports
        for line_num, line in enumerate(source_lines, 1):
            line = line.strip()
            
            # Check for forbidden imports
            if line.startswith('import ') or line.startswith('from '):
                for forbidden_import in FORBIDDEN_MODEL_IMPORTS:
                    if forbidden_import in line:
                        violations.append(
                            f"Line {line_num}: Forbidden import '{forbidden_import}' - "
                            f"use LLMGateway instead"
                        )
            
            # Check for direct model client instantiation
            for forbidden_class in FORBIDDEN_MODEL_CLASSES:
                if f'{forbidden_class}(' in line or f'{forbidden_class}(' in line:
                    violations.append(
                        f"Line {line_num}: Direct model client instantiation '{forbidden_class}' - "
                        f"use LLMGateway instead"
                    )
            
            # Check for direct API calls
            if any(pattern in line for pattern in ['openai.', 'anthropic.', 'cohere.', 'replicate.']):
                violations.append(
                    f"Line {line_num}: Direct API call detected - use LLMGateway instead"
                )
    
    except (OSError, TypeError):
        # Function source not available (e.g., built-in functions)
        pass
    
    return violations


def validate_agent_gateway_usage(agent_class: type) -> List[str]:
    """
    Validate that an agent class follows gateway policy.
    
    Args:
        agent_class: Agent class to validate
        
    Returns:
        List of policy violation messages
    """
    violations = []
    
    # Check all methods in the class
    for method_name in dir(agent_class):
        method = getattr(agent_class, method_name)
        
        # Skip private methods and properties
        if method_name.startswith('_') or not callable(method):
            continue
        
        # Check method for violations
        method_violations = _check_gateway_policy_violations(method)
        if method_violations:
            violations.extend([f"{agent_class.__name__}.{method_name}: {v}" for v in method_violations])
    
    return violations


def require_gateway_usage(agent_class: type) -> type:
    """
    Class decorator that validates gateway policy compliance.
    
    Args:
        agent_class: Agent class to validate
        
    Returns:
        Validated agent class
    """
    violations = validate_agent_gateway_usage(agent_class)
    
    if violations:
        violation_messages = []
        for violation in violations:
            violation_messages.append(f"  - {violation}")
        
        error_msg = (
            f"Gateway policy violations in {agent_class.__name__}:\n"
            f"All LLM calls must go through the project gateway.\n"
            f"Violations found:\n" + "\n".join(violation_messages) + "\n"
            f"Use LLMGateway or EnhancedLLMGateway instead."
        )
        
        warnings.warn(error_msg, UserWarning, stacklevel=2)
    
    return agent_class


# Example usage and testing
if __name__ == "__main__":
    # Test the enforcement decorator
    @enforce_gateway_policy
    def good_function():
        from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway
        gateway = EnhancedLLMGateway()
        return gateway.call_llm("test")
    
    @enforce_gateway_policy
    def bad_function():
        import openai  # This should trigger a warning
        client = openai.OpenAI()  # This should trigger a warning
        return client.chat.completions.create()
    
    # Test the class decorator
    @require_gateway_usage
    class GoodAgent:
        def __init__(self):
            from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway
            self.gateway = EnhancedLLMGateway()
        
        def execute(self):
            return self.gateway.call_llm("test")
    
    @require_gateway_usage
    class BadAgent:
        def __init__(self):
            import openai  # This should trigger a warning
            self.client = openai.OpenAI()  # This should trigger a warning
        
        def execute(self):
            return self.client.chat.completions.create()
    
    print("Testing gateway policy enforcement...")
    print("Good function:", good_function())
    print("Bad function:", bad_function())
    print("Good agent:", GoodAgent().execute())
    print("Bad agent:", BadAgent().execute())
