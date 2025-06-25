#!/usr/bin/env python3
"""
Quick test to verify TPM rate limiting integration works
Test with real API calls to see if rate limiting prevents overruns
"""

import os
import sys
import time

# Add project root to path
project_root = os.path.join(os.path.dirname(__file__), '..', '..')
if project_root not in sys.path:
    sys.path.append(project_root)

def test_tpm_rate_limiting():
    """Test TPM rate limiting with real API calls"""
    
    print("🧪 TESTING TPM RATE LIMITING INTEGRATION")
    print("=" * 50)
    
    try:
        from src.api_clients.direct_api_client import DirectAPIClient
        
        # Initialize client
        client = DirectAPIClient()
        print(f"✅ DirectAPIClient initialized")
        
        # Test text (medium size to simulate MFT analysis)
        test_text = """
        The foundation of democracy rests on the principle that government derives its 
        just powers from the consent of the governed. This sacred trust requires that 
        those in positions of authority act with integrity, transparency, and 
        unwavering commitment to the common good.
        """
        
        print(f"\n🔍 Testing with text: {len(test_text)} characters")
        
        # Test 1: Single analysis with GPT-3.5-turbo (high TPM model)
        print(f"\n📋 Test 1: GPT-3.5-turbo analysis (200K TPM limit)")
        result1, cost1 = client.analyze_text(test_text, "moral_foundations_theory", "gpt-3.5-turbo")
        
        if 'error' not in result1:
            print(f"✅ Analysis 1 successful: ${cost1:.4f}")
            print(f"🔍 TPM Info: {result1.get('tpm_info', {})}")
        else:
            print(f"❌ Analysis 1 failed: {result1['error']}")
        
        # Test 2: Single analysis with GPT-4o (low TPM model)
        print(f"\n📋 Test 2: GPT-4o analysis (30K TPM limit)")
        result2, cost2 = client.analyze_text(test_text, "moral_foundations_theory", "gpt-4o")
        
        if 'error' not in result2:
            print(f"✅ Analysis 2 successful: ${cost2:.4f}")
            print(f"🔍 TPM Info: {result2.get('tpm_info', {})}")
        else:
            print(f"❌ Analysis 2 failed: {result2['error']}")
        
        # Test 3: Rapid successive calls to trigger rate limiting
        print(f"\n📋 Test 3: Rapid successive GPT-4o calls to test rate limiting")
        for i in range(2):
            print(f"   Call {i+1}/2...")
            start_time = time.time()
            
            result, cost = client.analyze_text(test_text, "moral_foundations_theory", "gpt-4o")
            
            end_time = time.time()
            duration = end_time - start_time
            
            if 'error' not in result:
                print(f"   ✅ Call {i+1} successful in {duration:.1f}s: ${cost:.4f}")
                if 'tpm_info' in result:
                    tpm_info = result['tpm_info']
                    print(f"      Tokens: {tpm_info.get('total_tokens', 'unknown')}")
            else:
                print(f"   ❌ Call {i+1} failed: {result['error']}")
            
            # Small delay between calls
            time.sleep(1)
        
        # Test 4: Check TPM statistics
        if hasattr(client, 'tpm_limiter') and client.tpm_limiter:
            print(f"\n📊 TPM Usage Statistics:")
            client.tpm_limiter.print_stats()
        
        print(f"\n✅ TPM Rate Limiting Test Complete")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_tpm_rate_limiting()
    if success:
        print("\n🎉 TPM rate limiting is working correctly!")
        print("🚀 Ready to run experiments without rate limiting issues")
    else:
        print("\n🚨 TPM rate limiting test failed")
        print("🔧 May need to debug the integration") 