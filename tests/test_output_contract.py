#!/usr/bin/env python3
"""
Test script to evaluate whether lightweight output_contract improves parsing reliability.

This tests our durable infrastructure's ability to reliably extract data from LLM responses,
using CAF v7.1 as a concrete test case but focusing on the general parsing question.
"""

import json
import re
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry

def load_test_prompts():
    """Load the two test prompts."""
    generic_prompt = (Path(__file__).parent / "prompt_generic.txt").read_text()
    contract_prompt = (Path(__file__).parent / "prompt_contract.txt").read_text()
    return generic_prompt, contract_prompt

def load_test_text():
    """Load a sample text for analysis."""
    # Use a simple, consistent test text
    return """
    We must stand together as Americans, united in our commitment to justice and equality. 
    The challenges we face require honest dialogue, not divisive rhetoric that tears us apart. 
    Our democracy depends on truth-telling and genuine leadership, not manipulation or fear-mongering.
    We can build a better future through hope, pragmatism, and respect for human dignity.
    """

def extract_scores_generic(response_text):
    """Attempt to extract scores from free-form response."""
    scores = {}
    
    # Look for patterns like "Dignity: 0.8" or "Dignity Score: 0.8"
    patterns = [
        r'(\w+)(?:\s+Score)?:\s*([0-9.]+)',
        r'(\w+)\s*=\s*([0-9.]+)',
        r'(\w+)\s*-\s*([0-9.]+)'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, response_text, re.IGNORECASE)
        for dimension, score in matches:
            try:
                scores[dimension.lower()] = float(score)
            except ValueError:
                continue
    
    return scores

def extract_scores_contract(response_text):
    """Attempt to extract scores from structured response."""
    scores = {}
    
    # Look for the specific markdown pattern: **Dimension Score**: value (handles any dimension name)
    pattern = r'\*\*([^*]+?)\s+Score\*\*:\s*([0-9.]+)'
    matches = re.findall(pattern, response_text, re.IGNORECASE)
    
    for dimension, score in matches:
        try:
            # Clean up dimension name and use it as key
            clean_dimension = dimension.strip().lower().replace(' ', '_').replace('/', '_')
            scores[clean_dimension] = float(score)
        except ValueError:
            continue
    
    return scores

def evaluate_parsing_reliability(prompt_type, prompt_text, test_text, extract_function, runs=3):
    """Evaluate parsing reliability for a given prompt approach."""
    model_registry = ModelRegistry()
    gateway = LLMGateway(model_registry)
    
    results = {
        'successful_parses': 0,
        'total_dimensions_extracted': [],
        'consistency_scores': [],
        'raw_responses': []
    }
    
    for run in range(runs):
        try:
            # Make LLM call
            full_prompt = f"{prompt_text}\n\nText to analyze:\n{test_text}"
            response_text, metadata = gateway.execute_call(
                model="vertex_ai/gemini-2.5-flash",
                prompt=full_prompt
            )
            results['raw_responses'].append(response_text)
            
            # Attempt to extract scores
            extracted_scores = extract_function(response_text)
            
            if extracted_scores:
                results['successful_parses'] += 1
                results['total_dimensions_extracted'].append(len(extracted_scores))
                
                # Framework-agnostic: just measure if we got any structured data
                # A good response should have at least 3-5 dimensions
                min_expected_dimensions = 3
                consistency_score = 1.0 if len(extracted_scores) >= min_expected_dimensions else 0.0
                results['consistency_scores'].append(consistency_score)
            else:
                results['total_dimensions_extracted'].append(0)
                results['consistency_scores'].append(0.0)
                
        except Exception as e:
            print(f"Error in {prompt_type} run {run}: {e}")
            results['total_dimensions_extracted'].append(0)
            results['consistency_scores'].append(0.0)
    
    return results

def main():
    """Run the output contract evaluation."""
    print("🧪 Testing Output Contract vs Generic Prompting")
    print("=" * 50)
    
    # Load test materials
    generic_prompt, contract_prompt = load_test_prompts()
    test_text = load_test_text()
    
    print(f"Test text length: {len(test_text)} characters")
    print(f"Generic prompt length: {len(generic_prompt)} characters")
    print(f"Contract prompt length: {len(contract_prompt)} characters")
    print()
    
    # Test generic approach
    print("Testing Generic Approach...")
    generic_results = evaluate_parsing_reliability(
        "Generic", generic_prompt, test_text, extract_scores_generic, runs=3
    )
    
    # Test contract approach  
    print("Testing Contract Approach...")
    contract_results = evaluate_parsing_reliability(
        "Contract", contract_prompt, test_text, extract_scores_contract, runs=3
    )
    
    # Compare results
    print("\n📊 RESULTS COMPARISON")
    print("=" * 30)
    
    def calculate_avg(values):
        return sum(values) / len(values) if values else 0
    
    print(f"Generic Approach:")
    print(f"  - Successful parses: {generic_results['successful_parses']}/3")
    print(f"  - Avg dimensions extracted: {calculate_avg(generic_results['total_dimensions_extracted']):.1f}")
    print(f"  - Avg consistency score: {calculate_avg(generic_results['consistency_scores']):.2f}")
    
    print(f"\nContract Approach:")
    print(f"  - Successful parses: {contract_results['successful_parses']}/3")
    print(f"  - Avg dimensions extracted: {calculate_avg(contract_results['total_dimensions_extracted']):.1f}")
    print(f"  - Avg consistency score: {calculate_avg(contract_results['consistency_scores']):.2f}")
    
    # Determine recommendation
    contract_better = (
        contract_results['successful_parses'] > generic_results['successful_parses'] or
        calculate_avg(contract_results['consistency_scores']) > calculate_avg(generic_results['consistency_scores'])
    )
    
    print(f"\n🎯 RECOMMENDATION")
    print("=" * 20)
    if contract_better:
        print("✅ Output contracts improve parsing reliability")
        print("   Recommend implementing lightweight output_contract in v7.3 spec")
    else:
        print("❌ Output contracts do not significantly improve parsing")
        print("   Current free-form approach is sufficient")
    
    # Save detailed results
    results_file = Path(__file__).parent / "output_contract_test_results.json"
    with open(results_file, 'w') as f:
        json.dump({
            'generic_results': generic_results,
            'contract_results': contract_results,
            'recommendation': 'implement' if contract_better else 'skip'
        }, f, indent=2)
    
    print(f"\n📁 Detailed results saved to: {results_file}")

if __name__ == "__main__":
    main()