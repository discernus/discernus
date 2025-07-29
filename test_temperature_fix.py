#!/usr/bin/env python3
"""
Test to isolate temperature parameter impact on CFF v5.0 CSV generation
"""

import sys
from pathlib import Path
from dotenv import load_dotenv
import litellm

# Load environment
load_dotenv()

def test_temperature_impact():
    """Test different temperature settings to isolate the issue"""
    
    # Load the exact prompt that EnhancedAnalysisAgent generated
    prompt_file = Path("debug_enhanced_agent_actual_prompt.txt")
    if not prompt_file.exists():
        print("❌ Please run debug_enhanced_agent_prompt.py first")
        return
    
    prompt_text = prompt_file.read_text()
    
    temperatures = [0.0, 0.1, 0.3]  # Test different temperatures
    
    for temp in temperatures:
        print(f"\n🌡️  Testing temperature: {temp}")
        print("=" * 50)
        
        try:
            # Call LLM with different temperatures
            response = litellm.completion(
                model="vertex_ai/gemini-2.5-flash-lite",
                messages=[{"role": "user", "content": prompt_text}],
                temperature=temp,
                safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
                ]
            )
            
            # Extract content
            if not response or not response.choices:
                print(f"❌ Temperature {temp}: Empty response")
                continue
            
            result_content = response.choices[0].message.content
            if not result_content:
                print(f"❌ Temperature {temp}: Empty content")
                continue
            
            # Check for CSV sections
            scores_start = result_content.rfind("<<<DISCERNUS_SCORES_CSV_v1>>>")
            scores_end = result_content.rfind("<<<END_DISCERNUS_SCORES_CSV_v1>>>")
            evidence_start = result_content.rfind("<<<DISCERNUS_EVIDENCE_CSV_v1>>>")
            evidence_end = result_content.rfind("<<<END_DISCERNUS_EVIDENCE_CSV_v1>>>")
            
            scores_found = scores_start >= 0 and scores_end > scores_start
            evidence_found = evidence_start >= 0 and evidence_end > evidence_start
            
            print(f"📊 Temperature {temp} Results:")
            print(f"   - Response length: {len(result_content)} chars")
            print(f"   - Scores CSV: {'✅' if scores_found else '❌'}")
            print(f"   - Evidence CSV: {'✅' if evidence_found else '❌'}")
            
            if scores_found and evidence_found:
                print(f"   - ✅ SUCCESS: Both CSV sections generated!")
            elif scores_found or evidence_found:
                print(f"   - ⚠️  PARTIAL: Only one CSV section generated")
            else:
                print(f"   - ❌ FAILED: No CSV sections generated")
                # Show sample of malformed output
                print(f"   - Sample output: {result_content[-200:]}")
            
        except Exception as e:
            print(f"❌ Temperature {temp}: Error - {e}")

    print(f"\n🎯 CONCLUSION:")
    print(f"   If temperature 0.1+ works but 0.0 fails, then temperature=0.0 is the issue!")
    print(f"   If all fail, there may be another parameter or prompt construction issue.")

if __name__ == "__main__":
    test_temperature_impact() 