#!/usr/bin/env python3
"""
Test Exact Cursor Model Names for Discernus Advisor
Tests the exact model identifiers shown in Cursor's model menu
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.api_clients.direct_api_client import DirectAPIClient
import json
from datetime import datetime

def test_exact_cursor_models():
    """Test the exact model names shown in Cursor's UI"""
    print("🎯 Testing Exact Cursor Model Names")
    print("=" * 50)
    
    # Exact models from Cursor screenshot + Mistral
    cursor_models = {
        "anthropic": [
            "claude-4-sonnet",  # Exact from Cursor
            "claude-3.5-sonnet"  # Fallback
        ],
        "google": [
            "gemini-2.5-pro",   # Exact from Cursor
            "gemini-2.5-flash", # Exact from Cursor
            "gemini-1.5-pro"    # Fallback
        ],
        "openai": [
            "gpt-4.1",          # Exact from Cursor
            "o4-mini",          # Exact from Cursor
            "gpt-4o"            # Fallback
        ],
        "mistral": [
            "mistral-large-latest",  # Current working model
            "mistral-small-latest"   # Fallback
        ]
    }
    
    # Initialize API client
    try:
        client = DirectAPIClient()
        print("✅ API Client initialized")
    except Exception as e:
        print(f"❌ Failed to initialize API client: {e}")
        return
    
    # Test connections first
    connection_results = client.test_connections()
    print("\n📡 Connection Status:")
    for provider, status in connection_results.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {provider.upper()}")
    
    verified_cursor_models = {}
    
    # Test each provider with exact Cursor model names
    for provider, models in cursor_models.items():
        print(f"\n🧪 Testing {provider.upper()} with Cursor model names:")
        verified_cursor_models[provider] = []
        
        # Map provider names to connection result keys
        connection_key = provider
        if provider == "google":
            connection_key = "google_ai"
        
        if not connection_results.get(connection_key, False):
            print(f"   ⚠️ Skipping {provider} - not connected")
            continue
            
        for model in models:
            print(f"   Testing: {model}")
            try:
                # Simple test with minimal cost
                result, cost = client.analyze_text(
                    text="Hello", 
                    framework="test", 
                    model_name=model
                )
                
                if "error" not in result:
                    print(f"   ✅ {model} WORKS! (${cost:.4f})")
                    verified_cursor_models[provider].append(model)
                    break  # Use first working model
                else:
                    print(f"   ❌ {model} failed: {result.get('error', 'Unknown')}")
                    
            except Exception as e:
                error_msg = str(e)
                if "404" in error_msg or "not_found" in error_msg:
                    print(f"   ❌ {model} not found (404)")
                elif "401" in error_msg or "unauthorized" in error_msg:
                    print(f"   ❌ {model} unauthorized (need beta access?)")
                else:
                    print(f"   ❌ {model} error: {error_msg[:100]}...")
    
    # Results summary
    print(f"\n🎯 CURSOR MODEL VERIFICATION RESULTS:")
    print("=" * 40)
    
    working_models = {}
    for provider, models in verified_cursor_models.items():
        if models:
            working_models[provider] = models[0]
            print(f"✅ {provider.upper()}: {models[0]}")
        else:
            print(f"❌ {provider.upper()}: No working models")
    
    if len(working_models) >= 2:
        print(f"\n🚀 SUCCESS: {len(working_models)} providers verified!")
        print("   Ready for multi-LLM experiment with Cursor-compatible models")
        
        # Generate corrected YAML
        print(f"\n📝 CORRECTED EXPERIMENT YAML:")
        print("  models:")
        for provider, model in working_models.items():
            if provider == "anthropic":
                print(f'    - id: "{model}"')
                print(f'      provider: "anthropic"')
                print(f'      version: "latest"')
            elif provider == "google":
                print(f'    - id: "{model}"')
                print(f'      provider: "google"')
                print(f'      version: "latest"')
            elif provider == "openai":
                print(f'    - id: "{model}"')
                print(f'      provider: "openai"')
                print(f'      version: "latest"')
            elif provider == "mistral":
                print(f'    - id: "{model}"')
                print(f'      provider: "mistral"')
                print(f'      version: "latest"')
    else:
        print(f"\n⚠️ Only {len(working_models)} provider(s) working")
        print("   Need to investigate API access or model naming")
    
    # Save results
    results = {
        "timestamp": datetime.now().isoformat(),
        "cursor_models_tested": cursor_models,
        "verified_models": verified_cursor_models,
        "working_models": working_models,
        "connection_status": connection_results
    }
    
    results_file = Path(__file__).parent / "cursor_model_verification.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: {results_file}")
    return working_models

if __name__ == "__main__":
    try:
        working = test_exact_cursor_models()
        print(f"\n🏁 Final result: {len(working)} working providers")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Testing interrupted")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc() 