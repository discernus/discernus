#!/usr/bin/env python3
"""Test JSON cleaning logic"""

import json
from pathlib import Path

# Load the composite analysis
artifact_file = Path('projects/0mm/runs/20250926_233728/artifacts/analysis/composite_analysis_malcolm_x_ballot_or_bullet_25118944.json')
with open(artifact_file, 'r') as f:
    artifact_data = json.load(f)

raw_response = artifact_data.get('raw_analysis_response', '')
print('Raw response starts with:', repr(raw_response[:10]))

# Strip markdown like the score extraction method should
if raw_response.startswith('```json\n'):
    raw_response = raw_response[7:]
elif raw_response.startswith('```json'):
    raw_response = raw_response[7:]
if raw_response.endswith('\n```'):
    raw_response = raw_response[:-4]
elif raw_response.endswith('```'):
    raw_response = raw_response[:-3]

# Additional cleaning for any remaining newlines at start
raw_response = raw_response.lstrip('\n')

print('After cleaning, starts with:', repr(raw_response[:10]))

# Check if it's valid JSON now
try:
    import json5
    parsed = json5.loads(raw_response)
    print('\n✅ Cleaned response is valid JSON5')
    print('Keys:', list(parsed.keys()))
except Exception as e:
    print(f'\n❌ Cleaned response is still not valid JSON: {e}')
