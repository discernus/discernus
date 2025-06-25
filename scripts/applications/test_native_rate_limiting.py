#!/usr/bin/env python3
"""
Speed Test: Custom Rate Limiting vs LiteLLM Native Rate Limiting
Demonstrates the performance difference for experiments
"""

import os
import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def test_speed_comparison():
    """Compare speed of custom delays vs LiteLLM native rate limiting"""
    
    print("🏁 SPEED COMPARISON: Custom Delays vs LiteLLM Native Rate Limiting")
    print("=" * 70)
    
    try:
        from src.api_clients.litellm_client import LiteLLMClient
        
        # Initialize the enhanced LiteLLM client
        print("1. Initializing enhanced LiteLLM client...")
        client = LiteLLMClient()
        
        # Test with local models first (should be fastest)
        test_models = ['ollama/llama3.2', 'ollama/mistral']
        available_models = []
        
        print("\n2. Testing model availability...")
        for model in test_models:
            results = client.test_connections()
            if any('ollama' in key and results[key] for key in results):
                available_models.extend(['ollama/llama3.2', 'ollama/mistral'])
                break
        
        if not available_models:
            print("⚠️ No Ollama models available, will test cloud APIs")
            # Fall back to cloud models (will be slower but still demonstrate the difference)
            available_models = ['gpt-3.5-turbo']  # Most reliable cloud option
        
        if not available_models:
            print("❌ No models available for testing")
            return
        
        model_to_test = available_models[0]
        print(f"✅ Testing with model: {model_to_test}")
        
        # Speed test parameters
        num_requests = 3  # Small number for quick testing
        test_text = "This is a test for speed comparison of rate limiting approaches."
        framework = "moral_foundations_theory"
        
        print(f"\n3. Speed test: {num_requests} requests to {model_to_test}")
        print("   Text: 'This is a test for speed comparison...'")
        
        # Test current approach
        print(f"\n🚀 Testing ENHANCED LiteLLM Native Rate Limiting:")
        start_time = time.time()
        
        for i in range(num_requests):
            print(f"   Request {i+1}/{num_requests}...")
            result, cost = client.analyze_text(test_text, framework, model_to_test)
            
            if 'error' in result:
                print(f"   ⚠️ Request {i+1} failed: {result['error']}")
            else:
                print(f"   ✅ Request {i+1} completed (cost: ${cost:.4f})")
        
        native_time = time.time() - start_time
        print(f"   📊 Total time with NATIVE rate limiting: {native_time:.1f} seconds")
        print(f"   📊 Average per request: {native_time/num_requests:.1f} seconds")
        
        # Calculate theoretical old approach time
        if model_to_test.startswith('ollama/'):
            old_delay = 0.5  # Our old rate limit for Ollama
        elif 'gpt' in model_to_test:
            old_delay = 2.0  # Our old rate limit for OpenAI
        elif 'claude' in model_to_test:
            old_delay = 1.5  # Our old rate limit for Anthropic
        else:
            old_delay = 1.0  # Default
        
        theoretical_old_time = num_requests * old_delay
        
        print(f"\n📈 COMPARISON RESULTS:")
        print(f"   🚀 Native LiteLLM: {native_time:.1f} seconds")
        print(f"   🐌 Old custom delays: ~{theoretical_old_time:.1f} seconds (theoretical)")
        
        if theoretical_old_time > native_time:
            speedup = theoretical_old_time / native_time
            print(f"   ⚡ SPEEDUP: {speedup:.1f}x faster with native rate limiting!")
        
        print(f"\n💡 For larger experiments:")
        experiment_requests = 50
        native_experiment_time = (native_time / num_requests) * experiment_requests
        old_experiment_time = experiment_requests * old_delay
        
        print(f"   📊 {experiment_requests} requests with native: ~{native_experiment_time:.1f} seconds")
        print(f"   📊 {experiment_requests} requests with old approach: ~{old_experiment_time:.1f} seconds")
        print(f"   ⚡ Experiment speedup: {old_experiment_time/native_experiment_time:.1f}x faster!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure LiteLLM is installed: pip install litellm")
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_speed_comparison() 