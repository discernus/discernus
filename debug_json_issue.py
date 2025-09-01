#!/usr/bin/env python3
"""
Debug script to investigate JSON serialization issue
"""

import json
from pathlib import Path

def debug_json_serialization():
    # Load the last LLM interaction
    log_file = Path("/Volumes/code/discernus/projects/bolsonaro_2018/session/20250901T044126Z/logs/llm_interactions.jsonl")

    if not log_file.exists():
        print("Log file not found")
        return

    with open(log_file, 'r') as f:
        lines = f.readlines()

    if not lines:
        print("No log entries found")
        return

    # Get the last entry
    last_entry = lines[-1]
    try:
        data = json.loads(last_entry)
        response = data.get('response', '')

        print("Last LLM interaction:")
        print(f"Agent: {data.get('agent_name')}")
        print(f"Success: {data.get('success')}")
        print(f"Response length: {len(response)}")

        # Try to extract and parse the JSON from the response
        import re
        json_pattern = r'<<<DISCERNUS_ANALYSIS_JSON_v6>>>\s*({.*?})\s*<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>'
        json_match = re.search(json_pattern, response, re.DOTALL)

        if json_match:
            print("Found JSON in response")
            json_str = json_match.group(1).strip()
            print(f"JSON string length: {len(json_str)}")

            try:
                analysis_data = json.loads(json_str)
                print("JSON parsed successfully")
                print(f"Document analyses: {len(analysis_data.get('document_analyses', []))}")

                # Try to serialize it back
                test_serialize = json.dumps(analysis_data, indent=2)
                print("Re-serialization successful")

            except json.JSONDecodeError as e:
                print(f"JSON parsing failed: {e}")
                print(f"JSON content preview: {json_str[:500]}...")
        else:
            print("No JSON found in response")

    except json.JSONDecodeError as e:
        print(f"Failed to parse log entry: {e}")

if __name__ == "__main__":
    debug_json_serialization()
