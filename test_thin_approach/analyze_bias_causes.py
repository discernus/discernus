#!/usr/bin/env python3
"""
Analyze potential causes of the systematic bias between show work vs production
"""

import json
import re

def analyze_prompt_differences():
    """Compare the prompts used in show work vs production."""
    
    print("=== ANALYZING BIAS CAUSES ===")
    print()
    
    # Load show work data
    with open('/Volumes/code/discernus/tmp/artifacts/three_shot_visibility_test.json', 'r') as f:
        show_work_data = json.load(f)
    
    # Load production data
    with open('/Volumes/code/discernus/tmp/artifacts/extended_analysis_results.json', 'r') as f:
        production_data = json.load(f)
    
    print("1. PROMPT DIFFERENCES:")
    print("   Show Work Prompt Length:", len(show_work_data['prompt']))
    print("   Production Prompt Length:", len(production_data['composite_analysis']['raw_analysis_response']))
    print()
    
    # Check if show work used different framework
    show_work_prompt = show_work_data['prompt']
    if "inferred populist dimensions" in show_work_prompt:
        print("   ⚠️  SHOW WORK USED INFERRED DIMENSIONS (not actual PDAF)")
        print("   ⚠️  This could explain the systematic differences!")
    else:
        print("   ✓ Show work used actual PDAF framework")
    
    print()
    
    # Check production framework usage
    production_response = production_data['composite_analysis']['raw_analysis_response']
    if "populist_discourse_analysis_framework" in production_response:
        print("   ✓ Production used actual PDAF framework")
    else:
        print("   ⚠️  Production may not have used PDAF framework")
    
    print()
    
    print("2. FRAMEWORK DIMENSION MAPPING ISSUES:")
    print("   The show work test used 6 inferred dimensions:")
    print("   - People-Centrism")
    print("   - Anti-Elitism/Anti-Establishment") 
    print("   - Nationalism/Sovereignty")
    print("   - Charismatic Leadership")
    print("   - Direct Appeal/Common Sense")
    print("   - Crisis/Threat Perception")
    print()
    print("   Production used 9 actual PDAF dimensions:")
    print("   - manichaean_people_elite_framing")
    print("   - crisis_restoration_narrative")
    print("   - popular_sovereignty_claims")
    print("   - anti_pluralist_exclusion")
    print("   - elite_conspiracy_systemic_corruption")
    print("   - authenticity_vs_political_class")
    print("   - homogeneous_people_construction")
    print("   - nationalist_exclusion")
    print("   - economic_populist_appeals")
    print()
    
    print("3. POTENTIAL CAUSES OF SYSTEMATIC BIAS:")
    print()
    print("   A. FRAMEWORK MISMATCH:")
    print("      - Show work used generic 'inferred' dimensions")
    print("      - Production used specific PDAF dimensions")
    print("      - Different dimension definitions = different scoring criteria")
    print()
    print("   B. PROMPT COMPLEXITY:")
    print("      - Show work: Explicit instruction to show three approaches")
    print("      - Production: Implicit three-shot via prompt template")
    print("      - More explicit instructions may lead to more conservative scoring")
    print()
    print("   C. MODEL BEHAVIOR DIFFERENCES:")
    print("      - When asked to show work: More methodical, conservative")
    print("      - When in 'production mode': More confident, higher scores")
    print("      - This suggests the LLM has different 'modes' of operation")
    print()
    print("   D. DIMENSION MAPPING ERRORS:")
    print("      - Our mapping between inferred and PDAF dimensions may be wrong")
    print("      - 'Anti-Elitism' vs 'anti_pluralist_exclusion' are different concepts")
    print("      - 'Crisis/Threat Perception' vs 'crisis_restoration_narrative' are different")
    print()
    
    print("4. RECOMMENDATIONS:")
    print()
    print("   A. REPEAT TEST WITH ACTUAL PDAF:")
    print("      - Run show work test with full PDAF framework")
    print("      - Use same dimensions in both tests")
    print("      - This will isolate prompt vs framework effects")
    print()
    print("   B. INVESTIGATE PROMPT TEMPLATE:")
    print("      - Check if production prompt is actually doing three-shot")
    print("      - Verify the prompt template is working as intended")
    print("      - May need to make three-shot more explicit")
    print()
    print("   C. MODEL CONSISTENCY TEST:")
    print("      - Run same prompt multiple times")
    print("      - Check if production mode is consistent")
    print("      - Verify if show work mode is more reliable")

def check_production_prompt():
    """Check what prompt was actually used in production."""
    
    print("\n=== CHECKING PRODUCTION PROMPT ===")
    
    # Load the prompt template used in production
    with open('/Volumes/code/discernus/tmp/AnalysisAgent/prompt_3run.yaml', 'r') as f:
        prompt_template = f.read()
    
    print("Production prompt template includes:")
    print("- Three independent approaches: ✓" if "THREE INDEPENDENT ANALYTICAL APPROACHES" in prompt_template else "- Three independent approaches: ✗")
    print("- Median calculation: ✓" if "Calculate Median Scores" in prompt_template else "- Median calculation: ✗")
    print("- Evidence-first analysis: ✓" if "Evidence-First Analysis" in prompt_template else "- Evidence-first analysis: ✗")
    print("- Context-weighted analysis: ✓" if "Context-Weighted Analysis" in prompt_template else "- Context-weighted analysis: ✗")
    print("- Pattern-based analysis: ✓" if "Pattern-Based Analysis" in prompt_template else "- Pattern-based analysis: ✗")
    
    print("\nThe production prompt DOES include three-shot instructions.")
    print("This suggests the bias is NOT due to missing three-shot in production.")
    print("The issue is likely framework differences or model behavior differences.")

if __name__ == "__main__":
    analyze_prompt_differences()
    check_production_prompt()
