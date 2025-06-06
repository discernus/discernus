#!/usr/bin/env python3
"""
Test JSON Parsing
"""

import json

def test_json_parsing():
    """Test JSON parsing of the response"""
    
    raw_response = '''```json
{
  "scores": {
    "Dignity": 0.9,
    "Tribalism": 0.1,
    "Truth": 0.5,
    "Manipulation": 0.1,
    "Justice": 0.6,
    "Resentment": 0.0,
    "Hope": 0.8,
    "Fantasy": 0.2,
    "Pragmatism": 0.7,
    "Fear": 0.0
  },
  "analysis": "The text strongly emphasizes dignity by advocating for respect for all Americans, suggesting a high score for Dignity (0.9). Tribalism is minimal (0.1) as the text does not prioritize any specific group. The call to work together implies a moderate commitment to Truth (0.5) and Pragmatism (0.7), as it suggests collaboration and feasible solutions. Justice is present (0.6) in the aim to build a stronger democracy, which implies fairness and inclusivity. Hope is also strong (0.8) due to the optimistic vision of a stronger democracy. There is little to no indication of Resentment (0.0) or Fear (0.0), and Fantasy is low (0.2) as the text does not promise unrealistic outcomes."
}
```'''
    
    print("🧪 Testing JSON Parsing")
    print("=" * 50)
    
    print("📄 Raw response:")
    print(raw_response)
    
    print("\n1️⃣ Testing direct JSON parsing:")
    try:
        result = json.loads(raw_response)
        print("✅ Direct JSON parsing successful")
        print(f"Scores: {result['scores']}")
    except json.JSONDecodeError as e:
        print(f"❌ Direct JSON parsing failed: {e}")
    
    print("\n2️⃣ Testing after removing code block markers:")
    # Remove ```json and ``` markers
    cleaned = raw_response.strip()
    if cleaned.startswith('```json'):
        cleaned = cleaned[7:]
    if cleaned.endswith('```'):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()
    
    print("Cleaned JSON:")
    print(cleaned)
    
    try:
        result = json.loads(cleaned)
        print("✅ Cleaned JSON parsing successful")
        print(f"Scores: {result['scores']}")
    except json.JSONDecodeError as e:
        print(f"❌ Cleaned JSON parsing failed: {e}")

if __name__ == "__main__":
    test_json_parsing() 