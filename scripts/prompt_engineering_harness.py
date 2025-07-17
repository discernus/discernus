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
    
    # --- Load Real-World Assets ---
    try:
        framework_path = project_root / "projects" / "attesor" / "pdaf_v1.1_sanitized_framework.md"
        corpus_path = project_root / "projects" / "attesor" / "corpus_original" / "cory_booker_2018_first_step_act.txt"
        
        instructions = framework_path.read_text()
        corpus_text = corpus_path.read_text()
        print("✅ Successfully loaded real-world framework and corpus file.")
    except FileNotFoundError as e:
        print(f"❌ ERROR: Could not load required asset file: {e}")
        sys.exit(1)


    # --- The Prompt to be Engineered ---
    # This is where we will iterate. The goal is a universal prompt template
    # that works for any framework, including the complex PDAF.
    analysis_prompt = f"""You are an expert analyst with a secure code interpreter.
Your task is to apply the following analytical framework to the provided text.

FRAMEWORK:
---
{instructions}
---

TEXT TO ANALYZE:
---
{corpus_text}
---

Your analysis must have two parts:
1.  A detailed, qualitative analysis in natural language, explaining your reasoning for each of the 10 PDAF anchors.
2.  A final JSON object containing a numerical score from 0.0 to 1.0 for each of the 10 anchors.

You MUST return your response as a single, raw JSON object and nothing else. Do not wrap it in markdown fences (e.g., '```json') or any other text. Your response must start with '{{' and end with '}}'.

The JSON object must have the following structure:
{{
  "analysis_text": "Your detailed, qualitative analysis for all 10 anchors here...",
  "pdaf_scores": {{
    "manichaean_people_elite_framing": 0.8,
    "crisis_restoration_narrative": 0.9,
    "popular_sovereignty_claims": 0.6,
    "anti_pluralist_exclusion": 0.1,
    "elite_conspiracy_systemic_corruption": 0.7,
    "authenticity_vs_political_class": 0.5,
    "homogeneous_people_construction": 0.4,
    "nationalist_exclusion": 0.2,
    "economic_redistributive_appeals": 0.3,
    "economic_direction_classification": 0.0
  }}
}}

Your response MUST be the raw JSON object, starting with '{{' and ending with '}}'.
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