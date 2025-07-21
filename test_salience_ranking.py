#!/usr/bin/env python3
"""
Test script for the Enhanced Emotional Climate Framework with Salience Ranking
=============================================================================

This script tests the new salience ranking feature added to the ECF framework.
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

def test_ecf_salience_ranking():
    """Test the ECF framework with salience ranking enhancement."""
    
    # Load the enhanced ECF framework
    framework_path = project_root / "frameworks" / "reference" / "core" / "ecf_v1.0_refined.md"
    if not framework_path.exists():
        print(f"❌ Framework not found: {framework_path}")
        return False
    
    try:
        framework_config = load_framework_json_config(framework_path)
    except Exception as e:
        print(f"❌ Failed to load framework configuration: {e}")
        return False
    
    # Load test text
    test_text_path = project_root / "test_salience_sample.txt"
    if not test_text_path.exists():
        print(f"❌ Test text not found: {test_text_path}")
        return False
    
    test_text = test_text_path.read_text()
    
    print("🧪 Testing Enhanced ECF with Salience Ranking")
    print("=" * 60)
    print(f"Framework: {framework_config.get('display_name', 'ECF v1.0')}")
    print(f"Test text length: {len(test_text)} characters")
    print(f"Expected output includes: salience_ranking")
    print()
    
    # Get the analysis prompt
    analysis_prompt = framework_config['analysis_variants']['default']['analysis_prompt']
    
    # Get output contract instructions
    output_instructions = framework_config['output_contract']['instructions']
    
    # Format the prompt with the test text and enforce JSON output
    full_prompt = f"""{analysis_prompt}

TEXT TO ANALYZE:
{test_text}

{output_instructions}

CRITICAL: You must respond with ONLY a valid JSON object. No explanations, no markdown, no text before or after - just the JSON."""
    
    # Use a fast, cost-effective model for testing
    model = "vertex_ai/gemini-2.5-flash"
    
    try:
        print(f"📤 Sending request to {model}...")
        
        messages = [
            {"role": "user", "content": full_prompt}
        ]
        
        response = litellm.completion(
            model=model,
            messages=messages,
            temperature=0.1,
            timeout=120
        )
        
        response_text = response.choices[0].message.content.strip()
        print("📥 Response received!")
        
        # Try to extract and parse JSON from response
        try:
            # Look for JSON in the response
            if '```json' in response_text:
                json_start = response_text.find('```json') + 7
                json_end = response_text.find('```', json_start)
                json_text = response_text[json_start:json_end].strip()
            else:
                # Assume the entire response is JSON
                json_text = response_text
            
            result = json.loads(json_text)
            
            print("✅ JSON parsing successful!")
            print()
            
            # Validate expected schema
            expected_fields = ['worldview', 'scores', 'evidence', 'confidence', 'reasoning', 'salience_ranking']
            missing_fields = []
            present_fields = []
            
            for field in expected_fields:
                if field in result:
                    present_fields.append(field)
                    print(f"✅ {field}: Present")
                else:
                    missing_fields.append(field)
                    print(f"❌ {field}: Missing")
            
            # Focus on the new salience_ranking field
            if 'salience_ranking' in result:
                print("\n🏆 SALIENCE RANKING ANALYSIS:")
                print("-" * 50)
                
                salience_data = result['salience_ranking']
                if isinstance(salience_data, list) and len(salience_data) > 0:
                    print(f"   📊 Contains {len(salience_data)} ranked dimensions")
                    
                    print("\n📈 RANKING RESULTS:")
                    for item in salience_data:
                        if all(key in item for key in ['dimension', 'salience_score', 'rank']):
                            print(f"   #{item['rank']}: {item['dimension']} (salience: {item['salience_score']:.2f})")
                        else:
                            print(f"   ⚠️  Malformed ranking item: {item}")
                    
                    # Validate ranking structure
                    print("\n🔍 VALIDATION RESULTS:")
                    print("-" * 30)
                    
                    # Check if all dimensions are present
                    expected_dimensions = ['fear', 'hope', 'enmity', 'amity', 'envy', 'compersion']
                    found_dimensions = [item.get('dimension', '').lower() for item in salience_data if 'dimension' in item]
                    
                    all_dimensions_present = all(dim in found_dimensions for dim in expected_dimensions)
                    print(f"   All 6 dimensions present: {'✅' if all_dimensions_present else '❌'}")
                    
                    # Check if ranking is properly ordered (1,2,3,4,5,6)
                    ranks = [item.get('rank', 999) for item in salience_data if 'rank' in item]
                    properly_ranked = sorted(ranks) == list(range(1, len(salience_data) + 1))
                    print(f"   Properly ranked (1-6): {'✅' if properly_ranked else '❌'}")
                    
                    # Check salience scores are in valid range
                    salience_scores = [item.get('salience_score', -1) for item in salience_data if 'salience_score' in item]
                    valid_scores = all(0.0 <= score <= 1.0 for score in salience_scores)
                    print(f"   Valid salience scores (0.0-1.0): {'✅' if valid_scores else '❌'}")
                    
                    # Show most and least salient dimensions
                    if salience_data:
                        most_salient = min(salience_data, key=lambda x: x.get('rank', 999))
                        least_salient = max(salience_data, key=lambda x: x.get('rank', 0))
                        
                        print(f"\n🥇 Most salient: {most_salient.get('dimension', 'unknown')} (score: {most_salient.get('salience_score', 0):.2f})")
                        print(f"🥉 Least salient: {least_salient.get('dimension', 'unknown')} (score: {least_salient.get('salience_score', 0):.2f})")
                        
                        # Compare with raw emotional scores if available
                        if 'scores' in result:
                            scores = result['scores']
                            most_dim = most_salient.get('dimension', '')
                            if f"{most_dim}_score" in scores:
                                raw_score = scores[f"{most_dim}_score"]
                                salience_score = most_salient.get('salience_score', 0)
                                print(f"\n📊 Most salient dimension comparison:")
                                print(f"   Raw emotional score: {raw_score:.2f}")
                                print(f"   Salience score: {salience_score:.2f}")
                                print(f"   💡 Note: Salience measures prominence in discourse, not emotional intensity")
                
                else:
                    print("❌ salience_ranking: Empty or invalid format")
                    return False
            
            else:
                print("❌ CRITICAL: salience_ranking field missing from output!")
                return False
            
            # Show sample of the response for debugging
            print(f"\n📄 RESPONSE SAMPLE:")
            print("-" * 30)
            response_sample = json.dumps(result, indent=2)
            if len(response_sample) > 800:
                print(response_sample[:800] + "\n... (truncated)")
            else:
                print(response_sample)
            
            # Overall test result
            critical_success = 'salience_ranking' in result and isinstance(result['salience_ranking'], list)
            
            print(f"\n{'🎉 SALIENCE RANKING TEST PASSED!' if critical_success else '❌ SALIENCE RANKING TEST FAILED!'}")
            return critical_success
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
            print(f"Raw response preview:\n{response_text[:500]}...")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_ecf_salience_ranking()
    sys.exit(0 if success else 1)