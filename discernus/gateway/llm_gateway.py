#!/usr/bin/env python3
"""
DEPRECATED LLM Gateway - Redirect Module
=======================================

⚠️  DEPRECATED: This basic LLMGateway is deprecated and will be removed.
    Use EnhancedLLMGateway instead for all new code.

    Migration:
    - Replace: from discernus.gateway.llm_gateway import LLMGateway
    - With:    from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway
    - Replace: LLMGateway(model_registry)
    - With:    EnhancedLLMGateway(model_registry)

This module redirects to the deprecated implementation for backward compatibility.
"""

import warnings

# Issue deprecation warning on import
warnings.warn(
    "discernus.gateway.llm_gateway is deprecated. Use discernus.gateway.llm_gateway_enhanced instead.",
    DeprecationWarning,
    stacklevel=2
)

# Import from deprecated location
from .deprecated.llm_gateway_deprecated import LLMGateway

# Re-export for backward compatibility
__all__ = ['LLMGateway']