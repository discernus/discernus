#!/usr/bin/env python3
"""
Debug Response Parsing
"""

from src.api_clients.direct_api_client import DirectAPIClient

def test_response_parsing():
    """Test to see the raw response and understand parsing issues"""
    
    print("🧪 Testing Response Parsing Debug")
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
    
    try:
        result, cost = client.analyze_text(test_text, "civic_virtue", "gpt-4o")
        
        print(f"\n📄 RAW RESPONSE:")
        print("=" * 80)
        print(result.get('raw_response', 'No raw response found'))
        print("=" * 80)
        
        print(f"\n📊 PARSED SCORES:")
        print(result.get('scores', 'No scores found'))
        
        print(f"\n🔍 PARSED STATUS:")
        print(f"Parsed: {result.get('parsed', 'Unknown')}")
        
        print(f"\n💰 Cost: ${cost:.4f}")
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_response_parsing() 