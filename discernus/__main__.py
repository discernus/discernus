#!/usr/bin/env python3
"""
Discernus Main Entry Point
==========================

Entry point for python -m discernus execution.
"""

# Set LiteLLM debug suppression environment variables before any imports
import os
os.environ['LITELLM_VERBOSE'] = 'false'
os.environ['LITELLM_LOG'] = 'WARNING'
os.environ['LITELLM_PROXY_DEBUG'] = 'false'
os.environ['LITELLM_PROXY_LOG_LEVEL'] = 'WARNING'
os.environ['LITELLM_LOG_LEVEL'] = 'WARNING'
os.environ['LITELLM_COLD_STORAGE_LOG_LEVEL'] = 'WARNING'
os.environ['LITELLM_PROXY_VERBOSE'] = 'false'
os.environ['LITELLM_PROXY_DEBUG_MODE'] = 'false'
os.environ['LITELLM_PROXY_LOG_LEVEL_DEBUG'] = 'false'

from .cli import cli

if __name__ == "__main__":
    cli()
