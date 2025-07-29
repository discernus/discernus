#!/usr/bin/env python3
"""
Test script using EXACT same LLM parameters as EnhancedAnalysisAgent
"""

import sys
from pathlib import Path
from dotenv import load_dotenv
import litellm

# Load environment
load_dotenv()

def test_with_exact_agent_params():
    """Test CFF v5.0 with exact same parameters as EnhancedAnalysisAgent"""
    
    # Load the exact prompt that EnhancedAnalysisAgent generated
    prompt_file = Path("debug_enhanced_agent_actual_prompt.txt")
    if not prompt_file.exists():
        print("❌ Please run debug_enhanced_agent_prompt.py first")
        return
    
    prompt_text = prompt_file.read_text()
    
    print("🎯 Testing with EXACT EnhancedAnalysisAgent parameters:")
    print("   - model: vertex_ai/gemini-2.5-flash-lite")
    print("   - temperature: 0.0")
    print("   - messages: [{'role': 'user', 'content': '...'}] (no system prompt)")
    print("   - safety_settings: BLOCK_NONE for all categories")
    print("=" * 70)
    
    try:
        # Call LLM with EXACT same parameters as EnhancedAnalysisAgent
        response = litellm.completion(
            model="vertex_ai/gemini-2.5-flash-lite",
            messages=[{"role": "user", "content": prompt_text}],  # No system prompt!
            temperature=0.0,  # Exact same temperature
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ]
        )
        
        # Extract content like EnhancedAnalysisAgent does
        if not response or not response.choices:
            print("❌ LLM returned empty response")
            return
        
        result_content = response.choices[0].message.content
        if not result_content or result_content.strip() == "":
            print("❌ LLM returned empty content")
            return
        
        print(f"✅ SUCCESS - Response length: {len(result_content)} characters")
        
        # Check for CSV sections like EnhancedAnalysisAgent does
        scores_start = result_content.rfind("<<<DISCERNUS_SCORES_CSV_v1>>>")
        scores_end = result_content.rfind("<<<END_DISCERNUS_SCORES_CSV_v1>>>")
        evidence_start = result_content.rfind("<<<DISCERNUS_EVIDENCE_CSV_v1>>>")
        evidence_end = result_content.rfind("<<<END_DISCERNUS_EVIDENCE_CSV_v1>>>")
        
        print(f"\n🔍 CSV Section Detection:")
        print(f"   - Scores CSV start: {scores_start} (found: {'✅' if scores_start >= 0 else '❌'})")
        print(f"   - Scores CSV end: {scores_end} (found: {'✅' if scores_end > scores_start else '❌'})")
        print(f"   - Evidence CSV start: {evidence_start} (found: {'✅' if evidence_start >= 0 else '❌'})")
        print(f"   - Evidence CSV end: {evidence_end} (found: {'✅' if evidence_end > evidence_start else '❌'})")
        
        # Extract CSV sections like EnhancedAnalysisAgent does
        scores_csv = ""
        evidence_csv = ""
        
        if scores_start >= 0 and scores_end > scores_start:
            scores_csv = result_content[scores_start + len("<<<DISCERNUS_SCORES_CSV_v1>>>"):scores_end].strip()
            
        if evidence_start >= 0 and evidence_end > evidence_start:
            evidence_csv = result_content[evidence_start + len("<<<DISCERNUS_EVIDENCE_CSV_v1>>>"):evidence_end].strip()
        
        print(f"\n📊 CSV Extraction Results:")
        print(f"   - Scores CSV length: {len(scores_csv)} characters")
        print(f"   - Evidence CSV length: {len(evidence_csv)} characters")
        
        if scores_csv:
            print(f"\n✅ SCORES CSV EXTRACTED:")
            print(f"   First 200 chars: {scores_csv[:200]}")
        else:
            print(f"\n❌ SCORES CSV EMPTY")
            
        if evidence_csv:
            print(f"\n✅ EVIDENCE CSV EXTRACTED:")
            print(f"   First 200 chars: {evidence_csv[:200]}")
        else:
            print(f"\n❌ EVIDENCE CSV EMPTY")
        
        # Show a sample of the response for debugging
        print(f"\n📄 Response sample (last 1000 chars):")
        print(f"   {result_content[-1000:]}")
        
    except Exception as e:
        print(f"❌ FAILED: {e}")

if __name__ == "__main__":
    test_with_exact_agent_params() 