#!/usr/bin/env python3
"""
Extract the actual analysis_prompt from CFF v7.3 to see if it constrains dimensions properly.
"""

import json
import re

with open('frameworks/reference/flagship/cff_v7.3.md', 'r') as f:
    content = f.read()

json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
if json_match:
    config = json.loads(json_match.group(1))
    analysis_prompt = config['analysis_variants']['default']['analysis_prompt']
    
    print('=== CFF V7.3 ANALYSIS_PROMPT ===')
    print(analysis_prompt)
    
    print(f'\n=== DIMENSION CONSTRAINT ANALYSIS ===')
    # Check if the prompt explicitly mentions each dimension
    all_dimensions = []
    for dims in config.get('dimension_groups', {}).values():
        all_dimensions.extend(dims)
    
    for dim in all_dimensions:
        if dim in analysis_prompt:
            print(f'✅ {dim}: mentioned in analysis_prompt')
        else:
            print(f'❌ {dim}: NOT mentioned in analysis_prompt')
    
    print(f'\n=== OUTPUT FORMAT ANALYSIS ===')
    if 'JSON' in analysis_prompt or 'json' in analysis_prompt:
        print('✅ Analysis prompt specifies JSON output format')
    else:
        print('❌ Analysis prompt does not specify JSON output format')
        
    if 'dimensional_scores' in analysis_prompt or 'dimension' in analysis_prompt:
        print('✅ Analysis prompt mentions dimensional scoring')
    else:
        print('❌ Analysis prompt does not mention dimensional scoring')

else:
    print("Could not extract JSON configuration from framework")
