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
import json

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
        # Use the MVA framework and corpus
        framework_path = project_root / "projects" / "MVA" / "experiment_1" / "cff_v4_mva.md"
        corpus_path = project_root / "projects" / "MVA" / "experiment_1" / "corpus" / "sanitized_speech_a1c5e7d2.md"
        
        framework_content = framework_path.read_text()
        corpus_text = corpus_path.read_text()
        print("✅ Successfully loaded MVA framework and corpus file.")
        print(f"📄 Testing with corpus file: {corpus_path.name}")
        print(f"📊 Corpus length: {len(corpus_text)} characters")
    except FileNotFoundError as e:
        print(f"❌ ERROR: Could not load required asset file: {e}")
        sys.exit(1)

    # --- Extract the fully_normative prompt from the framework ---
    # This is the new prompt format that should enforce evidence requirements
    analysis_prompt = """You are an expert political discourse analyst executing a multi-part analysis using the Cohesive Flourishing Framework (CFF) v3.1.

Your task is to analyze the provided text according to this framework's rigorous methodology, which requires comprehensive evidence documentation for all analytical conclusions.

Step 1: Classify the political worldview of the text.
Determine whether this text primarily expresses a "Progressive", "Conservative", "Libertarian", or "Other" worldview based on the rhetorical patterns, policy positions, and value frameworks expressed.

Step 2: Score the text on all five CFF axes.
Analyze the text carefully for each dimension using the framework's linguistic markers and theoretical foundations. For each axis, provide a score from -1.0 to +1.0:
- identity_axis: Individual Dignity (+1.0) ↔ Tribal Dominance (-1.0)
- fear_hope_axis: Optimistic Possibility (+1.0) ↔ Threat Perception (-1.0)
- envy_compersion_axis: Others' Success Celebration (+1.0) ↔ Elite Resentment (-1.0)
- enmity_amity_axis: Social Goodwill (+1.0) ↔ Interpersonal Hostility (-1.0)
- goal_axis: Cohesive Generosity (+1.0) ↔ Fragmentative Power (-1.0)

Step 3: Provide comprehensive evidence documentation.
For each axis score, you must provide:
- At least 3 direct quotations from the text that support your assessment
- Confidence rating (0.0-1.0) based on evidence strength and clarity
- Evidence type classification for each quote (lexical/semantic/rhetorical)
- Brief reasoning explaining how the evidence supports the score

Step 4: Format the output as a single JSON object.
Return a JSON object with these top-level keys:
- "worldview": String classification from Step 1
- "scores": Dictionary with all five axis scores
- "evidence": Dictionary with axis names as keys and arrays of direct quotations as values
- "confidence": Dictionary with axis names as keys and confidence ratings as values
- "evidence_types": Dictionary with axis names as keys and arrays of evidence type classifications as values
- "reasoning": Dictionary with axis names as keys and explanatory text as values

The output MUST be a valid JSON object that implements the framework's evidence requirements."""

    # Add the corpus text to the prompt
    full_prompt = f"""{analysis_prompt}

TEXT TO ANALYZE:
---
{corpus_text}
---

Apply the framework systematically to this text and return the JSON object as specified above."""

    # --- LLM Gateway Call ---
    print(f"--- Sending Prompt to {model_name} ---")
    print("PROMPT:")
    print(full_prompt)
    print("\n" + "="*80 + "\n")
    
    try:
        model_registry = ModelRegistry()
        gateway = LLMGateway(model_registry)
        
        response, metadata = gateway.execute_call(model_name, full_prompt)
        
        print("--- Raw LLM Response ---")
        print(response)
        
        print("\n--- Attempting to Parse JSON ---")
        try:
            # Find and extract JSON block from the response
            clean_response = response.strip()
            
            # Look for JSON block markers
            json_start = -1
            json_end = -1
            
            # Try to find ```json markers
            if '```json' in clean_response:
                json_start = clean_response.find('```json') + 7
                json_end = clean_response.find('```', json_start)
            # Try to find ``` markers 
            elif '```' in clean_response:
                json_start = clean_response.find('```') + 3
                json_end = clean_response.find('```', json_start)
            # Try to find JSON by looking for opening brace
            elif '{' in clean_response:
                json_start = clean_response.find('{')
                json_end = clean_response.rfind('}') + 1
            
            if json_start != -1 and json_end != -1:
                clean_response = clean_response[json_start:json_end].strip()
            
            parsed = json.loads(clean_response)
            print("✅ Valid JSON response!")
            
            # Check if it has the expected structure
            required_keys = ["worldview", "scores", "evidence", "confidence", "evidence_types", "reasoning"]
            missing_keys = [key for key in required_keys if key not in parsed]
            
            if missing_keys:
                print(f"❌ Missing required keys: {missing_keys}")
            else:
                print("✅ All required keys present!")
                
                # Check evidence requirements
                evidence_dict = parsed.get("evidence", {})
                print("\n📊 Evidence Count Check:")
                for axis, quotes in evidence_dict.items():
                    quote_count = len(quotes) if isinstance(quotes, list) else 0
                    print(f"  {axis}: {quote_count} quotes {'✅' if quote_count >= 3 else '❌'}")
                
                # Check axis scores
                print("\n📊 Axis Scores:")
                scores_dict = parsed.get("scores", {})
                for axis, score in scores_dict.items():
                    print(f"  {axis}: {score}")
                    
                # Check confidence ratings
                print("\n📊 Confidence Ratings:")
                confidence_dict = parsed.get("confidence", {})
                for axis, conf in confidence_dict.items():
                    print(f"  {axis}: {conf}")
                    
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON response: {e}")
            print("First 200 chars of cleaned response:")
            print(repr(clean_response[:200]))
        
        print("\n--- Metadata ---")
        print(metadata)

    except Exception as e:
        print(f"\n--- ERROR ---")
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main() 