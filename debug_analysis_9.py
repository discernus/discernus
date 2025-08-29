#!/usr/bin/env python3
"""Debug script to check the 9th analysis result."""

import json
import os
from pathlib import Path

# Load all analysis result artifacts
artifacts_dir = Path("shared_cache/artifacts")
analysis_files = sorted([f for f in os.listdir(artifacts_dir) if f.startswith("analysis_result_")])

print(f"Found {len(analysis_files)} analysis result files")

if len(analysis_files) >= 9:
    ninth_file = analysis_files[8]  # 0-indexed
    print(f"9th analysis file: {ninth_file}")
    
    with open(artifacts_dir / ninth_file, 'r') as f:
        analysis_data = json.load(f)
    
    raw_response = analysis_data.get('raw_analysis_response', '')
    
    print(f"Has start marker: {'<<<DISCERNUS_ANALYSIS_JSON_v6>>>' in raw_response}")
    print(f"Has end marker: {'<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>' in raw_response}")
    print(f"Raw response length: {len(raw_response)}")
    
    if raw_response:
        print("\nFirst 200 chars of raw response:")
        print(repr(raw_response[:200]))
        
        print("\nLast 200 chars of raw response:")
        print(repr(raw_response[-200:]))
else:
    print("Not enough analysis files found")

