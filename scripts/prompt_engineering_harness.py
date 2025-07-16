#!/usr/bin/env python3
"""
Prompt Engineering Harness
==========================

A simple, standalone script for iteratively developing and testing prompts
against a live LLM without running the full Discernus application.

This is the equivalent of "walking down the hallway" to have a direct
conversation with the LLM to resolve misunderstandings.
"""

import sys
import os
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry

def main():
    """
    Main function to run the prompt engineering harness.
    """
    # --- Configuration ---
    # We will target a model with known code interpreter capabilities.
    model_name = "openai/gpt-4o"
    
    # --- Hardcoded Inputs (from simple_experiment) ---
    instructions = """# Simple Test Framework

This is a very simple framework for testing.

## Analysis Dimensions

- **Tone**: Is the overall tone positive, negative, or neutral?
- **Main Idea**: What is the single main idea of the text?"""

    corpus_text = """Shall I compare thee to a summer's day?
Thou art more lovely and more temperate:
Rough winds do shake the darling buds of May,
And summer's lease hath all too short a date;
Sometime too hot the eye of heaven shines,
And often is his gold complexion dimm'd;
And every fair from fair sometime declines,
By chance or nature's changing course untrimm'd;
But thy eternal summer shall not fade,
Nor lose possession of that fair thou ow'st;
Nor shall death brag thou wander'st in his shade,
When in eternal lines to time thou grow'st:
   So long as men can breathe or eyes can see,
   So long lives this, and this gives life to thee."""

    # --- The Prompt to be Engineered ---
    analysis_prompt = f"""You are an expert analyst with a secure code interpreter.
Your task is to apply the following analytical framework to the provided text.

FRAMEWORK:
{instructions}

TEXT TO ANALYZE:
{corpus_text}

Your analysis must have two parts:
1.  A detailed, qualitative analysis in natural language.
2.  A final numerical score from 0.0 to 1.0, which you must generate by writing and executing a simple Python script.

You MUST return your response as a single, valid JSON object with the following structure:
{{
  "analysis_text": "Your detailed, qualitative analysis here...",
  "score_calculation": {{
    "code": "The simple Python script you wrote to generate the score. e.g., 'return 0.8'",
    "result": "The numerical result of executing that script. e.g., 0.8"
  }}
}}

Before returning your response, double-check that it is a single, valid JSON object and nothing else.
"""

    # --- LLM Gateway Call ---
    print(f"--- Sending Prompt to {model_name} ---")
    print(analysis_prompt)
    
    try:
        model_registry = ModelRegistry()
        gateway = LLMGateway(model_registry)
        
        response, metadata = gateway.execute_call(model_name, analysis_prompt)
        
        print("\n--- Raw LLM Response ---")
        print(response)
        
        print("\n--- Metadata ---")
        print(metadata)

    except Exception as e:
        print(f"\n--- ERROR ---")
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main() 