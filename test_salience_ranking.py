#!/usr/bin/env python3
"""
Test script for the Enhanced Emotional Climate Framework with Salience Ranking
=============================================================================

This script tests the new salience ranking feature added to the ECF framework.
"""

import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from discernus.core.spec_loader import load_framework_from_file
from discernus.gateway.llm_gateway import LLMGateway

def test_salience_ranking():
    """Test the ECF framework with salience ranking enhancement."""
    
    # Load the enhanced ECF framework
    framework_path = project_root / "frameworks" / "reference" / "core" / "ecf_v1.0_refined.md"
    framework = load_framework_from_file(str(framework_path))
    
    # Load test text
    test_text_path = project_root / "test_salience_sample.txt"
    test_text = test_text_path.read_text()
    
    # Create LLM gateway 
    gateway = LLMGateway()
    
    # Get the analysis prompt
    analysis_prompt = framework['analysis_variants']['default']['analysis_prompt']
    
    # Format the prompt with the test text
    full_prompt = f"{analysis_prompt}\n\nTEXT TO ANALYZE:\n{test_text}"
    
    print("🧪 Testing Enhanced ECF with Salience Ranking")
    print("=" * 60)
    print(f"Framework: {framework['display_name']}")
    print(f"Test text length: {len(test_text)} characters")
    print(f"Expected output includes: salience_ranking")
    print()
    
    try:
        # Execute the analysis
        print("📤 Sending request to LLM...")
        response = gateway.chat_completion(
            model="gemini-2.0-flash-exp",  # Fast model for testing
            messages=[{"role": "user", "content": full_prompt}],
            temperature=0.1
        )
        
        print("📥 Response received!")
        
        # Parse the JSON response
        response_text = response.choices[0].message.content.strip()
        
        # Try to extract JSON from response
        try:
            # Look for JSON in the response
            if '```json' in response_text:
                json_start = response_text.find('```json') + 7
                json_end = response_text.find('```', json_start)
                json_text = response_text[json_start:json_end].strip()
            else:
                json_text = response_text
                
            result = json.loads(json_text)
            
            print("✅ JSON parsing successful!")
            print()
            
            # Validate the standard schema
            required_fields = ['worldview', 'scores', 'evidence', 'confidence', 'reasoning']
            for field in required_fields:
                if field in result:
                    print(f"✅ {field}: Present")
                else:
                    print(f"❌ {field}: Missing")
            
            # Check for the new salience_ranking field
            if 'salience_ranking' in result:
                print("✅ salience_ranking: Present")
                
                salience_data = result['salience_ranking']
                if isinstance(salience_data, list) and len(salience_data) > 0:
                    print(f"   📊 Contains {len(salience_data)} ranked dimensions")
                    
                    print("\n🏆 SALIENCE RANKING RESULTS:")
                    print("-" * 40)
                    for item in salience_data:
                        if all(key in item for key in ['dimension', 'salience_score', 'rank']):
                            print(f"#{item['rank']}: {item['dimension']} (salience: {item['salience_score']:.2f})")
                        else:
                            print(f"   ⚠️  Malformed ranking item: {item}")
                    
                    # Analyze the ranking
                    print("\n📈 SALIENCE ANALYSIS:")
                    print("-" * 40)
                    
                    # Check if ranking is properly ordered
                    ranks = [item['rank'] for item in salience_data if 'rank' in item]
                    is_properly_ordered = ranks == sorted(ranks)
                    print(f"   Properly ordered: {'✅' if is_properly_ordered else '❌'}")
                    
                    # Show most salient dimension
                    if salience_data:
                        top_dimension = min(salience_data, key=lambda x: x.get('rank', 999))
                        print(f"   Most salient: {top_dimension.get('dimension', 'unknown')}")
                        
                        # Compare to raw scores
                        if 'scores' in result:
                            scores = result['scores']
                            if isinstance(scores, dict):
                                top_dim_name = top_dimension.get('dimension', '')
                                if f"{top_dim_name}_score" in scores:
                                    raw_score = scores[f"{top_dim_name}_score"]
                                    salience_score = top_dimension.get('salience_score', 0)
                                    print(f"   Raw score: {raw_score}, Salience: {salience_score}")
                                    print(f"   📝 Note: Salience measures prominence, not intensity")
                
                else:
                    print("❌ salience_ranking: Empty or invalid format")
            else:
                print("❌ salience_ranking: Missing")
            
            print("\n📄 FULL RESPONSE PREVIEW:")
            print("-" * 40)
            print(json.dumps(result, indent=2)[:500] + "..." if len(json.dumps(result)) > 500 else json.dumps(result, indent=2))
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
            print("Raw response preview:")
            print(response_text[:300] + "..." if len(response_text) > 300 else response_text)
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_salience_ranking()