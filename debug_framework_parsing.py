#!/usr/bin/env python3
"""
Debug framework parsing to see what dimensions should be generated.
"""

import sys
sys.path.insert(0, '/Volumes/code/discernus')

from discernus.agents.EnhancedAnalysisAgent.framework_parser import FrameworkParser

# Load the actual CFF v7.3 framework
with open('frameworks/reference/flagship/cff_v7.3.md', 'r') as f:
    framework_content = f.read()

parser = FrameworkParser()

try:
    config = parser.parse_framework(framework_content, "test_hash")
    
    print("=== CFF V7.3 FRAMEWORK ANALYSIS ===")
    print(f"Total dimensions found: {len(config.dimensions)}")
    print(f"Dimensions: {config.dimensions}")
    
    print(f"\nDimension groups:")
    for group_name, dimensions in config.dimension_groups.items():
        print(f"  {group_name}: {dimensions}")
    
    # Check what the raw config has
    print(f"\nRaw config keys: {list(config.raw_config.keys())}")
    
    # Check if there's an analysis_prompt
    analysis_variants = config.raw_config.get("analysis_variants", {})
    default_variant = analysis_variants.get("default", {})
    analysis_prompt = default_variant.get("analysis_prompt", "")
    
    print(f"\nHas analysis_prompt: {len(analysis_prompt) > 0}")
    if analysis_prompt:
        print(f"Analysis prompt length: {len(analysis_prompt)} characters")
        print(f"Analysis prompt preview: {analysis_prompt[:200]}...")
    
    # Check what's in the output contract
    output_contract = config.raw_config.get("output_contract", {})
    print(f"\nOutput contract keys: {list(output_contract.keys())}")
    
except Exception as e:
    print(f"Framework parsing failed: {e}")
    import traceback
    traceback.print_exc()
