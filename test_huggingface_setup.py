#!/usr/bin/env python3
"""
HuggingFace Integration Test

Quick test to verify your HuggingFace API key and integration is working.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_api_key():
    """Test that API key is properly configured."""
    print("🔑 Testing API Key Configuration...")
    
    api_key = os.getenv('HUGGINGFACE_API_KEY', '')
    
    if not api_key:
        print("  ❌ HUGGINGFACE_API_KEY not found in environment")
        print("  💡 Make sure you have:")
        print("     1. Created a .env file from env.example")
        print("     2. Added your HF token: HUGGINGFACE_API_KEY=hf_your_token_here")
        return False
    
    if not api_key.startswith('hf_'):
        print(f"  ⚠️  API key doesn't start with 'hf_': {api_key[:10]}...")
        print("  💡 HuggingFace tokens should start with 'hf_'")
        return False
    
    print(f"  ✅ API key found: {api_key[:10]}...{api_key[-5:]}")
    return True

def test_huggingface_client():
    """Test HuggingFace client initialization."""
    print("\n🤖 Testing HuggingFace Client...")
    
    try:
        from src.tasks.huggingface_client import HuggingFaceClient
        client = HuggingFaceClient()
        
        frameworks = client.get_available_frameworks()
        print(f"  ✅ Client initialized successfully")
        print(f"  ✅ Available frameworks: {frameworks}")
        
        return client
        
    except Exception as e:
        print(f"  ❌ Client initialization failed: {e}")
        return None

def test_simple_model():
    """Test a simple model call."""
    print("\n🧪 Testing Simple Model Call...")
    
    try:
        import requests
        
        api_key = os.getenv('HUGGINGFACE_API_KEY')
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Test with a simple sentiment model
        url = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
        
        payload = {
            "inputs": "I love working with AI systems!"
        }
        
        print("  📡 Making test API call...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"  ✅ API call successful!")
            print(f"  📊 Test result: {result}")
            return True
        elif response.status_code == 429:
            print("  ⚠️  Rate limited - but API key is working!")
            return True
        else:
            print(f"  ❌ API call failed: {response.status_code}")
            print(f"  📄 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"  ❌ Test API call failed: {e}")
        return False

def test_framework_analysis():
    """Test a full framework analysis."""
    print("\n🎯 Testing Framework Analysis...")
    
    try:
        from src.tasks.huggingface_client import HuggingFaceClient
        client = HuggingFaceClient()
        
        # Test with a simple text and civic virtue framework
        test_text = "We must work together with dignity and respect for all people."
        
        # Use a small, fast model for testing
        test_model = "microsoft/DialoGPT-medium"
        
        print(f"  📝 Test text: {test_text}")
        print(f"  🤖 Test model: {test_model}")
        
        result, cost = client.analyze_text(test_text, "civic_virtue", test_model)
        
        print(f"  ✅ Analysis completed!")
        print(f"  💰 Estimated cost: ${cost:.4f}")
        print(f"  📊 Scores: {result.get('scores', {})}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Framework analysis failed: {e}")
        print(f"  💡 This might be expected if the model needs warming up")
        return False

def main():
    """Run all HuggingFace setup tests."""
    print("🚀 HuggingFace Setup Test Suite")
    print("=" * 50)
    
    tests = [
        test_api_key,
        test_huggingface_client,
        test_simple_model,
        # test_framework_analysis  # Comment out for now - may need model warming
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 50)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 ALL TESTS PASSED ({passed}/{total})")
        print("✅ Your HuggingFace integration is ready!")
        print("\n📋 Next Steps:")
        print("   1. Run: python tests/utilities/run_epic_validation.py")
        print("   2. Test live analysis with real models")
        print("   3. Start the API: python scripts/run_api.py")
        return 0
    else:
        print(f"⚠️  SOME TESTS FAILED ({passed}/{total})")
        print("❌ Check the failed tests above and fix configuration")
        print("\n🔧 Common fixes:")
        print("   1. Verify your .env file has HUGGINGFACE_API_KEY=hf_...")
        print("   2. Check your HF token has Read permissions")
        print("   3. Ensure you have internet connectivity")
        return 1

if __name__ == "__main__":
    exit(main()) 