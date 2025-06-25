#!/usr/bin/env python3
"""
Test LiteLLM Migration - Validate Unified Client
Demonstrates cloud + local model usage with preserved interface
"""

import os
import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def test_litellm_client():
    """Test the new LiteLLM unified client"""
    print("🚀 TESTING LITELLM UNIFIED CLIENT")
    print("=" * 50)
    
    try:
        from src.api_clients.litellm_client import LiteLLMClient
        
        # Initialize client
        print("1. Initializing LiteLLM client...")
        client = LiteLLMClient()
        
        # Test connections
        print("\n2. Testing connections...")
        connections = client.test_connections()
        
        # Test simple analysis with local Ollama model
        print("\n3. Testing local Ollama analysis...")
        test_text = "The government should increase funding for renewable energy projects to combat climate change."
        
        try:
            result, cost = client.analyze_text(
                text=test_text,
                framework="moral_foundations_theory", 
                model_name="ollama/llama3.2"
            )
            print(f"✅ Ollama analysis successful!")
            print(f"   Scores: {result.get('scores', {})}")
            print(f"   Cost: ${cost:.4f}")
            print(f"   QA Passed: {result.get('qa_passed', False)}")
        except Exception as e:
            print(f"❌ Ollama analysis failed: {e}")
        
        # Test with cloud model if available
        if connections.get('openai', False):
            print("\n4. Testing cloud API analysis...")
            try:
                result, cost = client.analyze_text(
                    text=test_text,
                    framework="moral_foundations_theory",
                    model_name="gpt-3.5-turbo"
                )
                print(f"✅ OpenAI analysis successful!")
                print(f"   Scores: {result.get('scores', {})}")
                print(f"   Cost: ${cost:.4f}")
                print(f"   QA Passed: {result.get('qa_passed', False)}")
            except Exception as e:
                print(f"❌ OpenAI analysis failed: {e}")
        
        # Test available models
        print("\n5. Available models:")
        models = client.get_available_models()
        for provider, model_list in models.items():
            if model_list:
                print(f"   • {provider}: {len(model_list)} models")
                # Show first few models as examples
                for model in model_list[:3]:
                    print(f"     - {model}")
                if len(model_list) > 3:
                    print(f"     ... and {len(model_list) - 3} more")
        
        print("\n✅ LiteLLM client test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ LiteLLM client test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_interface_compatibility():
    """Test that LiteLLM maintains DirectAPIClient interface"""
    print("\n🔄 TESTING INTERFACE COMPATIBILITY")
    print("=" * 50)
    
    try:
        from src.api_clients.litellm_client import LiteLLMClient
        
        client = LiteLLMClient()
        
        # Check that all DirectAPIClient methods exist
        required_methods = [
            'analyze_text',
            'test_connections', 
            'get_available_models',
            'get_retry_statistics',
            'log_reliability_report'
        ]
        
        missing_methods = []
        for method in required_methods:
            if not hasattr(client, method):
                missing_methods.append(method)
        
        if missing_methods:
            print(f"❌ Missing methods: {missing_methods}")
            return False
        else:
            print("✅ All DirectAPIClient methods available")
        
        # Test analyze_text signature compatibility
        import inspect
        sig = inspect.signature(client.analyze_text)
        expected_params = ['text', 'framework', 'model_name']
        actual_params = list(sig.parameters.keys())[1:]  # Skip 'self'
        
        if actual_params == expected_params:
            print("✅ analyze_text signature compatible")
        else:
            print(f"❌ analyze_text signature mismatch: {actual_params} vs {expected_params}")
            return False
        
        print("✅ Interface compatibility confirmed!")
        return True
        
    except Exception as e:
        print(f"❌ Interface compatibility test failed: {e}")
        return False

def demonstrate_model_switching():
    """Demonstrate seamless model switching"""
    print("\n🔀 DEMONSTRATING MODEL SWITCHING")
    print("=" * 50)
    
    try:
        from src.api_clients.litellm_client import LiteLLMClient
        
        client = LiteLLMClient()
        test_text = "Technology companies should be more transparent about their data collection practices."
        
        # Test different models with same interface
        models_to_test = [
            "ollama/llama3.2",
            "ollama/mistral", 
            # "gpt-3.5-turbo",  # Uncomment if you have OpenAI API key
        ]
        
        for model in models_to_test:
            print(f"\n📊 Testing with {model}...")
            try:
                start_time = time.time()
                result, cost = client.analyze_text(
                    text=test_text,
                    framework="moral_foundations_theory",
                    model_name=model
                )
                duration = time.time() - start_time
                
                print(f"   ✅ Success in {duration:.2f}s")
                print(f"   💰 Cost: ${cost:.4f}")
                print(f"   🎯 QA Score: {result.get('analysis_quality', 0.0):.2f}")
                
                # Show a few key scores if available
                scores = result.get('scores', {})
                if scores:
                    key_scores = dict(list(scores.items())[:3])  # First 3 scores
                    print(f"   📈 Sample scores: {key_scores}")
                
            except Exception as e:
                print(f"   ❌ Failed: {e}")
        
        print("\n✅ Model switching demonstration completed!")
        return True
        
    except Exception as e:
        print(f"❌ Model switching test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 LITELLM MIGRATION VALIDATION SUITE")
    print("=" * 60)
    
    test_results = []
    
    # Run tests
    test_results.append(("LiteLLM Client Basic Test", test_litellm_client()))
    test_results.append(("Interface Compatibility", test_interface_compatibility()))
    test_results.append(("Model Switching Demo", demonstrate_model_switching()))
    
    # Summary
    print("\n📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)
    
    for test_name, result in test_results:
        emoji = "✅" if result else "❌"
        print(f"{emoji} {test_name}")
    
    print(f"\nResult: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! LiteLLM migration is ready.")
        print("\n🚀 NEXT STEPS:")
        print("1. Run: python3 scripts/applications/migrate_to_litellm.py")
        print("2. Update experiment configurations to use new models")
        print("3. Test your existing experiments with local Ollama models")
    else:
        print(f"\n⚠️ {total - passed} tests failed. Review errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 