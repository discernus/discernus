#!/usr/bin/env python3
"""
LLM Gateway - Simplified API Wrapper
===================================

THIN Principle: Ultra-thin wrapper around LiteLLM client for clean API access.
Provides minimal abstraction layer for LLM calls without adding complexity.

Purpose: Hide LiteLLM implementation details while maintaining simple interface.
"""

from .litellm_client import LiteLLMClient
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables from .env file
load_dotenv()

# Instantiate a single, reusable client instance
# This is more efficient than creating a new client for every request.
llm_client = LiteLLMClient()


async def get_llm_analysis(text: str, experiment_def: Dict[str, Any], model: str) -> dict:
    """
    A simple wrapper to call the existing LiteLLMClient.

    This function serves as the clean entry point,
    hiding the implementation details of the underlying client.
    """
    # For now, we are not handling the 'cost' return value, but we can add it later.
    analysis_result, _ = llm_client.analyze_text(text=text, experiment_def=experiment_def, model_name=model)
    return analysis_result
