#!/usr/bin/env python3
"""
Debug LLM response to see exactly what Gemini is returning
"""

import sys
import os
import yaml
import json
from litellm import completion

# Add the orchestrator path
sys.path.append('agents/OrchestratorAgent')

def test_orchestrator_llm_call():
    """Test the exact LLM call the orchestrator makes"""
    
    # Load the orchestrator prompt
    prompt_path = 'agents/OrchestratorAgent/prompt.yaml'
    with open(prompt_path, 'r') as f:
        prompt_data = yaml.safe_load(f)
    
    prompt_template = prompt_data['template']
    
    # Create test data (simplified)
    experiment = {
        "name": "test_experiment",
        "description": "Simple test",
        "framework_file": "framework.md",
        "corpus_files": ["test1.txt", "test2.txt"]
    }
    
    framework_hash = "test_framework_hash"
    corpus_hashes = {"test1.txt": "hash1", "test2.txt": "hash2"}
    
    # Format the prompt exactly like orchestrator does
    prompt_text = prompt_template.format(
        experiment=json.dumps(experiment, indent=2),
        framework_hash=framework_hash,
        corpus_hashes=json.dumps(corpus_hashes, indent=2)
    )
    
    print("=== TESTING LLM CALL ===")
    print(f"Prompt length: {len(prompt_text)} characters")
    print("\nFirst 500 chars of prompt:")
    print(prompt_text[:500] + "..." if len(prompt_text) > 500 else prompt_text)
    
    print("\n=== CALLING LLM ===")
    try:
        response = completion(
            model="gemini-2.5-flash",
            messages=[{"role": "user", "content": prompt_text}],
            temperature=0.0,
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ]
        )
        
        print("LLM call successful!")
        print(f"Response type: {type(response)}")
        
        if hasattr(response, 'choices') and response.choices:
            content = response.choices[0].message.content
            print(f"Content type: {type(content)}")
            print(f"Content length: {len(content) if content else 0}")
            print(f"Content is None: {content is None}")
            print(f"Content is empty string: {content == ''}")
            
            if content:
                print("\nFirst 500 chars of response:")
                print(content[:500])
                
                # Try to parse as JSON
                try:
                    parsed = json.loads(content)
                    print("\nJSON parsing successful!")
                    print(f"Parsed keys: {list(parsed.keys()) if isinstance(parsed, dict) else 'Not a dict'}")
                except json.JSONDecodeError as e:
                    print(f"\nJSON parsing failed: {e}")
                    print("Raw content (first 200 chars):")
                    print(repr(content[:200]))
            else:
                print("\nContent is empty or None!")
                
        else:
            print("No choices in response!")
            print(f"Full response: {response}")
            
    except Exception as e:
        print(f"LLM call failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_orchestrator_llm_call() 