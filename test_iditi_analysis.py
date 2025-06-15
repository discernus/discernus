#!/usr/bin/env python3
"""
Forensic Test: IDITI Framework Analysis
Testing if the DirectAPIClient can actually analyze text with IDITI framework
"""

import sys
import os
sys.path.insert(0, 'src')

from narrative_gravity.api_clients.direct_api_client import DirectAPIClient

def test_iditi_analysis():
    """Test IDITI framework analysis with a simple dignity-focused text."""
    print("🔬 Forensic Test: IDITI Framework Analysis")
    print("=" * 50)
    
    # Initialize client
    try:
        client = DirectAPIClient()
        print("✅ DirectAPIClient initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        return False
    
    # Test text (should score high on dignity)
    test_text = "Every American, regardless of background, deserves equal dignity and respect. We must judge people by their character, not their group identity."
    
    print(f"\n📝 Test Text: {test_text}")
    print(f"🎯 Framework: iditi")
    print(f"🤖 Model: gpt-4o")
    
    # Run analysis
    try:
        result, cost = client.analyze_text(test_text, 'iditi', 'gpt-4o')
        
        print(f"\n💰 Cost: ${cost:.4f}")
        print(f"📊 Result Keys: {list(result.keys())}")
        
        if 'error' in result:
            print(f"❌ Analysis Error: {result['error']}")
            return False
        
        # Check for scores
        if 'scores' in result:
            scores = result['scores']
            print(f"🎯 Scores: {scores}")
            
            # Check for IDITI-specific wells
            if 'Dignity' in scores:
                print(f"   Dignity: {scores['Dignity']}")
            if 'Tribalism' in scores:
                print(f"   Tribalism: {scores['Tribalism']}")
        
        print(f"\n✅ IDITI Analysis SUCCESSFUL!")
        print(f"📋 Full Result: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return False

if __name__ == "__main__":
    success = test_iditi_analysis()
    if success:
        print("\n🎉 FORENSIC CONCLUSION: IDITI framework works with DirectAPIClient!")
        exit(0)
    else:
        print("\n💥 FORENSIC CONCLUSION: IDITI framework analysis failed!")
        exit(1) 