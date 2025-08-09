#!/usr/bin/env python3
"""
Debug what prompt is actually being sent to the LLM by EnhancedAnalysisAgent.
"""

import json
import base64
import sys
sys.path.insert(0, '/Volumes/code/discernus')

# Load the CFF framework
with open('frameworks/reference/flagship/cff_v7.3.md', 'r') as f:
    framework_content = f.read()

# Load the JSON prompt template used by EnhancedAnalysisAgent
with open('discernus/agents/EnhancedAnalysisAgent/prompt.yaml', 'r') as f:
    import yaml
    prompt_config = yaml.safe_load(f)

print("=== CURRENT PROMPT TEMPLATE ===")
template = prompt_config['template']
print(f"Template length: {len(template)} characters")
print(f"Template preview:\n{template[:500]}...")

# Test what the agent would do with the framework
print("\n=== FRAMEWORK ANALYSIS ===")
framework_b64 = base64.b64encode(framework_content.encode('utf-8')).decode('utf-8')
print(f"Framework encoded length: {len(framework_b64)} characters")

# Extract analysis_prompt from framework
import re
json_pattern = r"```json\n(.*?)\n```"
json_match = re.search(json_pattern, framework_content, re.DOTALL)
if json_match:
    framework_config = json.loads(json_match.group(1))
    analysis_variants = framework_config.get("analysis_variants", {})
    default_variant = analysis_variants.get("default", {})
    analysis_prompt = default_variant.get("analysis_prompt", "")
    
    print(f"\nFramework has analysis_prompt: {len(analysis_prompt) > 0}")
    if analysis_prompt:
        print(f"Framework analysis_prompt length: {len(analysis_prompt)} characters")
        print(f"Framework analysis_prompt preview:\n{analysis_prompt[:300]}...")
    
    print(f"\nFramework dimensions: {list(framework_config.get('dimension_groups', {}).keys())}")
    all_dimensions = []
    for dims in framework_config.get('dimension_groups', {}).values():
        all_dimensions.extend(dims)
    print(f"All framework dimensions: {all_dimensions}")
    
    # Check if template would use framework's analysis_prompt
    print(f"\n=== PROMPT CONSTRUCTION ANALYSIS ===")
    print("Current template instructs agent to:")
    if "Decode the framework" in template:
        print("✅ Decode the framework")
    if "Apply the framework's `analysis_prompt`" in template:
        print("✅ Apply the framework's analysis_prompt")
    else:
        print("❌ Does NOT explicitly instruct to apply framework's analysis_prompt")
    
    if "Follow the framework's scoring protocol" in template:
        print("✅ Follow framework's scoring protocol")
    else:
        print("❌ Does NOT mention following framework's scoring protocol")

else:
    print("❌ Could not extract JSON from framework")
