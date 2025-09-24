#!/usr/bin/env python3
"""
LiteLLM Debug Suppression Script
================================

This script sets all necessary environment variables to suppress verbose debug output
from LiteLLM and its proxy components. It can be imported or run directly.

Usage:
    python3 scripts/suppress_litellm_debug.py
    # or
    from scripts.suppress_litellm_debug import suppress_litellm_debug
    suppress_litellm_debug()
"""

import os
import sys
from pathlib import Path

def suppress_litellm_debug():
    """
    Set all LiteLLM debug suppression environment variables.
    
    This function sets environment variables to suppress verbose debug output
    from LiteLLM and its proxy components, ensuring clean terminal output.
    """
    # Core LiteLLM verbose settings
    os.environ['LITELLM_VERBOSE'] = 'false'
    os.environ['LITELLM_LOG'] = 'WARNING'
    os.environ['LITELLM_LOG_LEVEL'] = 'WARNING'
    
    # Proxy-specific settings
    os.environ['LITELLM_PROXY_DEBUG'] = 'false'
    os.environ['LITELLM_PROXY_LOG_LEVEL'] = 'WARNING'
    os.environ['LITELLM_PROXY_VERBOSE'] = 'false'
    os.environ['LITELLM_PROXY_DEBUG_MODE'] = 'false'
    os.environ['LITELLM_PROXY_LOG_LEVEL_DEBUG'] = 'false'
    
    # Cold storage and other components
    os.environ['LITELLM_COLD_STORAGE_LOG_LEVEL'] = 'WARNING'
    
    # Additional Discernus-specific settings
    os.environ['DISCERNUS_LOG_LEVEL'] = 'WARNING'
    os.environ['DISCERNUS_VERBOSE'] = 'false'
    
    # Also try to configure litellm directly if it's available
    try:
        import litellm
        litellm.set_verbose = False
        
        # Configure verbose logger if available
        if hasattr(litellm, 'verbose_logger'):
            litellm.verbose_logger.setLevel('WARNING')
            
        print("✅ LiteLLM debug suppression configured programmatically")
        
    except ImportError:
        print("⚠️  LiteLLM not available for direct configuration")
    
    print("✅ LiteLLM debug suppression environment variables set")
    print(f"   LITELLM_LOG_LEVEL: {os.environ.get('LITELLM_LOG_LEVEL', 'NOT SET')}")
    print(f"   LITELLM_PROXY_LOG_LEVEL: {os.environ.get('LITELLM_PROXY_LOG_LEVEL', 'NOT SET')}")
    print(f"   LITELLM_VERBOSE: {os.environ.get('LITELLM_VERBOSE', 'NOT SET')}")

if __name__ == "__main__":
    suppress_litellm_debug()
