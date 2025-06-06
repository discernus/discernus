#!/usr/bin/env python3
"""
Test Script to Verify Prompt Generation Fix
"""

from src.api_clients.direct_api_client import DirectAPIClient

def test_prompt_generation():
    """Test that the DirectAPIClient is now generating proper prompts"""
    
    print("🧪 Testing DirectAPIClient Prompt Generation Fix")
    print("=" * 50)
    
    # Initialize client
    try:
        client = DirectAPIClient()
        print("✅ DirectAPIClient initialized")
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        return
    
    # Test text
    test_text = "We must work together with dignity and respect for all Americans to build a stronger democracy."
    
    print(f"\n📝 Test text: {test_text}")
    print(f"🤖 Using model: gpt-4o")
    print(f"📊 Framework: civic_virtue")
    
    try:
        result, cost = client.analyze_text(test_text, "civic_virtue", "gpt-4o")
        
        print(f"\n✅ Analysis completed!")
        print(f"💰 Cost: ${cost:.4f}")
        
        # Check if we got proper scores
        if "scores" in result and result["scores"]:
            print(f"🎯 SUCCESS: Got numerical scores!")
            print(f"📊 Scores: {result['scores']}")
            
            # Check if we have the expected civic virtue wells
            expected_wells = ["Dignity", "Truth", "Hope", "Justice", "Pragmatism", 
                             "Tribalism", "Manipulation", "Fantasy", "Resentment", "Fear"]
            
            found_wells = list(result["scores"].keys())
            print(f"🔍 Found wells: {found_wells}")
            
            missing_wells = [w for w in expected_wells if w not in found_wells]
            if missing_wells:
                print(f"⚠️ Missing wells: {missing_wells}")
            else:
                print("✅ All expected wells found!")
                
        else:
            print(f"❌ FAILED: No numerical scores found")
            print(f"📄 Raw response (first 200 chars): {result.get('raw_response', 'No raw response')[:200]}...")
            
        return result
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return None

if __name__ == "__main__":
    test_prompt_generation() 