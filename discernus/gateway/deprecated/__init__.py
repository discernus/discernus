"""
Deprecated Gateway Components
============================

This directory contains deprecated gateway components that are no longer
recommended for use. These components are kept for backward compatibility
but will be removed in future versions.

Components:
- llm_gateway_deprecated.py: Basic LLMGateway (use EnhancedLLMGateway instead)
"""

# Import deprecated components for backward compatibility
from .llm_gateway_deprecated import LLMGateway

__all__ = ['LLMGateway']
