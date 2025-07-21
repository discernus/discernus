#!/usr/bin/env python3
"""
Comprehensive ECF Salience Ranking Test Suite
============================================

Tests the salience ranking feature across multiple text samples
to validate it correctly identifies which emotional dimensions
are most prominent in different types of discourse.
"""

import json
import re
import sys
from pathlib import Path
import litellm

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def load_framework_json_config(framework_path: Path) -> dict:
    """Extract JSON configuration from V4 framework markdown file."""
    content = framework_path.read_text()
    
    # Find the JSON configuration block
    details_pattern = r'<details><summary>Machine-Readable Configuration</summary>\s*```json\s*(.*?)\s*```\s*</details>'
    match = re.search(details_pattern, content, re.DOTALL)
    
    if not match:
        raise ValueError(f"No JSON configuration found in {framework_path}")
    
    json_content = match.group(1).strip()
    return json.loads(json_content)

def run_ecf_analysis(framework_config: dict, text_content: str, model: str = "vertex_ai/gemini-2.5-flash") -> dict:
    """Run ECF analysis on given text and return parsed results."""
    
    # Get the analysis prompt and output instructions
    analysis_prompt = framework_config['analysis_variants']['default']['analysis_prompt']
    output_instructions = framework_config['output_contract']['instructions']
    
    # Format the prompt with strong JSON enforcement
    full_prompt = f"""{analysis_prompt}

TEXT TO ANALYZE:
{text_content}

{output_instructions}

CRITICAL: You must respond with ONLY a valid JSON object. No explanations, no markdown, no text before or after - just the JSON."""
    
    try:
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": full_prompt}],
            temperature=0.1,
            timeout=120
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Try to extract JSON from response
        if '```json' in response_text:
            json_start = response_text.find('```json') + 7
            json_end = response_text.find('```', json_start)
            json_text = response_text[json_start:json_end].strip()
        else:
            json_text = response_text
        
        result = json.loads(json_text)
        return {"success": True, "data": result}
        
    except json.JSONDecodeError as e:
        return {"success": False, "error": f"JSON parse error: {e}", "raw_response": response_text[:500]}
    except Exception as e:
        return {"success": False, "error": f"API error: {e}"}

def validate_salience_ranking(result_data: dict, expected_top_dimension: str = None) -> dict:
    """Validate salience ranking structure and content."""
    validation = {
        "has_salience_ranking": False,
        "proper_structure": False,
        "all_dimensions_present": False,
        "valid_scores": False,
        "properly_ranked": False,
        "most_salient": None,
        "expected_match": None,
        "ranking_details": []
    }
    
    if 'salience_ranking' not in result_data:
        return validation
    
    validation["has_salience_ranking"] = True
    salience_data = result_data['salience_ranking']
    
    if not isinstance(salience_data, list) or len(salience_data) == 0:
        return validation
    
    validation["proper_structure"] = True
    
    # Check all expected dimensions
    expected_dimensions = ['fear', 'hope', 'enmity', 'amity', 'envy', 'compersion']
    found_dimensions = [item.get('dimension', '').lower() for item in salience_data if 'dimension' in item]
    validation["all_dimensions_present"] = all(dim in found_dimensions for dim in expected_dimensions)
    
    # Check score validity
    salience_scores = [item.get('salience_score', -1) for item in salience_data if 'salience_score' in item]
    validation["valid_scores"] = all(0.0 <= score <= 1.0 for score in salience_scores)
    
    # Check ranking order
    ranks = [item.get('rank', 999) for item in salience_data if 'rank' in item]
    validation["properly_ranked"] = sorted(ranks) == list(range(1, len(salience_data) + 1))
    
    # Get most salient dimension
    if salience_data:
        most_salient_item = min(salience_data, key=lambda x: x.get('rank', 999))
        validation["most_salient"] = most_salient_item.get('dimension', '').lower()
        
        # Check against expected
        if expected_top_dimension:
            validation["expected_match"] = validation["most_salient"] == expected_top_dimension.lower()
    
    # Store ranking details
    validation["ranking_details"] = sorted(salience_data, key=lambda x: x.get('rank', 999))
    
    return validation

def run_comprehensive_test():
    """Run comprehensive salience ranking test across multiple samples."""
    
    # Load framework
    framework_path = project_root / "frameworks" / "reference" / "core" / "ecf_v1.0_refined.md"
    if not framework_path.exists():
        print(f"❌ Framework not found: {framework_path}")
        return False
    
    try:
        framework_config = load_framework_json_config(framework_path)
    except Exception as e:
        print(f"❌ Failed to load framework: {e}")
        return False
    
    # Define test cases
    test_cases = [
        {
            "name": "Balanced Political Speech",
            "file": "test_salience_sample.txt",
            "expected_top": "enmity",  # Based on previous test results
            "description": "Mixed emotional appeals with adversarial framing"
        },
        {
            "name": "Fear-Dominant Crisis Text",
            "file": "test_fear_dominant_sample.txt", 
            "expected_top": "fear",
            "description": "Crisis language with existential threats"
        },
        {
            "name": "Hope-Dominant Optimistic Text",
            "file": "test_hope_dominant_sample.txt",
            "expected_top": "hope", 
            "description": "Opportunity language with positive future framing"
        }
    ]
    
    print("🧪 COMPREHENSIVE ECF SALIENCE RANKING TEST")
    print("=" * 70)
    print(f"Framework: {framework_config.get('display_name', 'ECF v1.0')}")
    print(f"Test Cases: {len(test_cases)}")
    print()
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"📝 Test {i}: {test_case['name']}")
        print("-" * 40)
        
        # Load test text
        test_file = project_root / test_case['file']
        if not test_file.exists():
            print(f"❌ Test file not found: {test_case['file']}")
            results.append({"case": test_case["name"], "success": False, "error": "File not found"})
            continue
        
        test_text = test_file.read_text()
        print(f"   Description: {test_case['description']}")
        print(f"   Expected top dimension: {test_case['expected_top'].upper()}")
        print(f"   Text length: {len(test_text)} characters")
        
        # Run analysis
        analysis_result = run_ecf_analysis(framework_config, test_text)
        
        if not analysis_result["success"]:
            print(f"❌ Analysis failed: {analysis_result['error']}")
            results.append({"case": test_case["name"], "success": False, "error": analysis_result["error"]})
            continue
        
        # Validate salience ranking
        validation = validate_salience_ranking(analysis_result["data"], test_case["expected_top"])
        
        # Print results
        print(f"   Salience ranking present: {'✅' if validation['has_salience_ranking'] else '❌'}")
        print(f"   Proper structure: {'✅' if validation['proper_structure'] else '❌'}")
        print(f"   All dimensions present: {'✅' if validation['all_dimensions_present'] else '❌'}")
        print(f"   Valid scores (0.0-1.0): {'✅' if validation['valid_scores'] else '❌'}")
        print(f"   Properly ranked (1-6): {'✅' if validation['properly_ranked'] else '❌'}")
        
        if validation["most_salient"]:
            print(f"   Most salient: {validation['most_salient'].upper()}")
            if validation["expected_match"] is not None:
                match_status = "✅" if validation["expected_match"] else "❌"
                print(f"   Expected match: {match_status}")
            
            # Show top 3 dimensions
            if validation["ranking_details"]:
                print("   Top 3 dimensions:")
                for j, item in enumerate(validation["ranking_details"][:3], 1):
                    dim = item.get('dimension', 'unknown')
                    score = item.get('salience_score', 0)
                    print(f"     #{j}: {dim.capitalize()} ({score:.2f})")
        
        # Store result
        test_success = (validation["has_salience_ranking"] and validation["proper_structure"] 
                       and validation["all_dimensions_present"] and validation["valid_scores"]
                       and validation["properly_ranked"])
        
        results.append({
            "case": test_case["name"],
            "success": test_success,
            "validation": validation,
            "expected_match": validation.get("expected_match", False)
        })
        
        print(f"   Overall result: {'✅ PASSED' if test_success else '❌ FAILED'}")
        print()
    
    # Summary
    print("📊 COMPREHENSIVE TEST SUMMARY")
    print("=" * 50)
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r["success"])
    expected_matches = sum(1 for r in results if r.get("expected_match", False))
    
    print(f"Total tests: {total_tests}")
    print(f"Technical tests passed: {passed_tests}/{total_tests}")
    print(f"Expected dimension matches: {expected_matches}/{total_tests}")
    
    overall_success = passed_tests == total_tests and expected_matches >= (total_tests * 0.67)  # Allow some flexibility
    
    print(f"\n🎯 OVERALL RESULT: {'🎉 SUCCESS' if overall_success else '❌ NEEDS ATTENTION'}")
    
    if not overall_success:
        print("\n🔍 Issues found:")
        for result in results:
            if not result["success"]:
                print(f"   - {result['case']}: Technical failure")
            elif not result.get("expected_match", True):
                print(f"   - {result['case']}: Dimension mismatch")
    
    return overall_success

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1) 