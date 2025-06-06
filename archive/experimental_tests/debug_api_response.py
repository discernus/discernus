#!/usr/bin/env python3

import sys
sys.path.append('.')

from src.api_clients.direct_api_client import DirectAPIClient
import json

def debug_api_response():
    """Debug what the DirectAPIClient returns from LLM analysis."""
    print("🔍 Debugging DirectAPIClient response format...")
    
    client = DirectAPIClient()
    
    # Use a small text for testing
    test_text = """
    My fellow Americans, today we celebrate the peaceful transfer of power that is the hallmark of our democracy.
    We must come together as one nation, united in our common purpose and shared values.
    The challenges ahead are great, but so is our resolve.
    """
    
    try:
        print(f"📝 Test text length: {len(test_text)} characters")
        
        result, cost = client.analyze_text(
            text=test_text,
            framework='civic_virtue',
            model_name='gpt-4o'
        )
        
        print(f"💰 Cost: ${cost:.4f}")
        print(f"\n📊 Result structure:")
        print(f"Keys in result: {list(result.keys())}")
        
        print(f"\n🔍 Full result:")
        print(json.dumps(result, indent=2))
        
        # Check if we have wells or scores
        if 'wells' in result:
            print(f"\n✅ Found 'wells' structure:")
            for well in result['wells']:
                print(f"  {well}")
        elif 'scores' in result:
            print(f"\n✅ Found 'scores' structure:")
            print(f"  {result['scores']}")
        else:
            print(f"\n❌ No 'wells' or 'scores' found!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def main():
    debug_api_response()

if __name__ == "__main__":
    main() 