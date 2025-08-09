#!/usr/bin/env python3
"""
Debug what statistical artifacts are actually being generated and passed to synthesis.
"""

import json
import sys
sys.path.insert(0, '/Volumes/code/discernus')

# Load the most recent run's combined analysis
with open('projects/simple_test/shared_cache/artifacts/combined_analysis_v6_da853078', 'r') as f:
    analysis_data = f.read()

print("=== RAW ANALYSIS DATA ===")
combined_analysis = json.loads(analysis_data)
print("Document analyses:", len(combined_analysis.get('document_analyses', [])))

for i, doc in enumerate(combined_analysis.get('document_analyses', [])[:2]):
    print(f"\nDocument {i+1}: {doc.get('document_name', 'unknown')}")
    scores = doc.get('analysis_scores', {})
    print("  Available scores:", len(scores))
    print("  Sample scores:", {k: v for k, v in list(scores.items())[:5]})
    
    # Check for missing/NaN values
    missing_scores = [k for k, v in scores.items() if v is None or (isinstance(v, float) and str(v) == 'nan')]
    if missing_scores:
        print(f"  Missing/NaN scores: {missing_scores}")

# Test what MathToolkit would produce with this data
print("\n=== TESTING MATHTOOLKIT OUTPUT ===")

from discernus.core.math_toolkit import execute_analysis_plan_thin

# Simple descriptive stats plan
simple_plan = {
    "tasks": {
        "basic_descriptive": {
            "tool": "calculate_descriptive_stats",
            "config": {
                "columns": ["tribal_dominance_score", "individual_dignity_score", "amity_score", "hope_score"]
            }
        }
    }
}

try:
    results = execute_analysis_plan_thin(analysis_data, simple_plan)
    print("MathToolkit execution:")
    print("- Success:", len(results.get('errors', [])) == 0)
    print("- Errors:", results.get('errors', []))
    
    for task_name, result in results.get('results', {}).items():
        print(f"\nTask: {task_name}")
        if isinstance(result, dict) and 'groups' in result:
            print("Groups found:", list(result['groups'].keys()))
            for group_name, group_data in result['groups'].items():
                print(f"  {group_name}:")
                for metric, values in group_data.items():
                    if isinstance(values, dict) and 'mean' in values:
                        mean_val = values.get('mean', 'N/A')
                        print(f"    {metric}: mean={mean_val}")
        elif isinstance(result, dict):
            print("Result keys:", list(result.keys())[:5])
            
except Exception as e:
    print(f"MathToolkit failed: {e}")
    import traceback
    traceback.print_exc()
