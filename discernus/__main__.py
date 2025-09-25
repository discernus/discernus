#!/usr/bin/env python3
"""
Discernus Main Entry Point
==========================

Entry point for python -m discernus execution.
"""

# Comprehensive LiteLLM debug suppression - must be done before ANY imports
import os
import logging

# Set critical environment variables immediately
os.environ['LITELLM_VERBOSE'] = 'false'
os.environ['LITELLM_LOG_LEVEL'] = 'ERROR'
os.environ['LITELLM_PROXY_LOG_LEVEL'] = 'ERROR'
os.environ['LITELLM_PROXY_DEBUG'] = 'false'
os.environ['JSON_LOGS'] = 'false'
os.environ['LITELLM_COLD_STORAGE_LOG_LEVEL'] = 'ERROR'

# Disable problematic loggers immediately
logging.getLogger('LiteLLM Proxy').setLevel(logging.ERROR)
logging.getLogger('LiteLLM Proxy').disabled = True
logging.getLogger('litellm.proxy').setLevel(logging.ERROR) 
logging.getLogger('litellm.proxy').disabled = True

from .cli import cli

if __name__ == "__main__":
    cli()
