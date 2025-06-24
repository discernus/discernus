#!/usr/bin/env python3
"""
Test Latest Available Models for Discernus Advisor Custom GPT Context Generation
Verifies which flagship models are actually available through our API clients
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

def test_model_availability():
    """Test which models are actually available from each provider"""
    print("🔍 Testing Latest Model Availability for Custom GPT Context Generation")
    print("=" * 70)
    
    # Initialize API client
    try:
        client = DirectAPIClient()
        print("✅ API Client initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize API client: {e}")
        return
    
    # Test connections
    print("\n📡 Testing API Connections...")
    connection_results = client.test_connections()
    
    for provider, status in connection_results.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {provider.upper()}: {'Connected' if status else 'Failed'}")
    
    # Get available models
    print("\n🤖 Available Models by Provider:")
    available_models = client.get_available_models()
    
    # Test specific flagship models for our experiment
    flagship_models_to_test = {
        "openai": ["gpt-4.1", "gpt-4.1-mini", "gpt-4o", "o1", "o3"],
        "anthropic": ["claude-4.0-sonnet", "claude-4-sonnet", "claude-3-5-sonnet-20241022"],
        "google_ai": ["gemini-2.5-pro", "gemini-2.0-flash", "gemini-2-0-flash-exp"]
    }
    
    verified_models = {}
    
    for provider, models in available_models.items():
        print(f"\n{provider.upper()} Models:")
        verified_models[provider] = []
        
        for model in models:
            print(f"  📋 {model}")
            
            # Test if the model actually works with a simple query
            if connection_results.get(provider, False):
                try:
                    print(f"    🧪 Testing {model}...")
                    # Use a very simple test prompt to minimize cost
                    result, cost = client.analyze_text(
                        text="Test", 
                        framework="simple_test", 
                        model_name=model
                    )
                    
                    if "error" not in result:
                        print(f"    ✅ {model} works (cost: ${cost:.4f})")
                        verified_models[provider].append(model)
                    else:
                        print(f"    ❌ {model} failed: {result.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    print(f"    ❌ {model} failed: {str(e)}")
            else:
                print(f"    ⚠️ Skipping {model} - provider not connected")
    
    # Generate recommendations for the experiment
    print("\n🎯 RECOMMENDATIONS FOR CUSTOM GPT EXPERIMENT:")
    print("=" * 50)
    
    recommended_models = {}
    
    # OpenAI recommendation
    if verified_models.get("openai"):
        if "gpt-4.1" in verified_models["openai"]:
            recommended_models["openai"] = "gpt-4.1"
            print("✅ OpenAI: gpt-4.1 (Latest flagship)")
        elif "gpt-4o" in verified_models["openai"]:
            recommended_models["openai"] = "gpt-4o"
            print("⚠️ OpenAI: gpt-4o (GPT-4.1 not available, using current flagship)")
        else:
            recommended_models["openai"] = verified_models["openai"][0]
            print(f"⚠️ OpenAI: {verified_models['openai'][0]} (Latest available)")
    else:
        print("❌ OpenAI: No working models found")
    
    # Anthropic recommendation
    if verified_models.get("anthropic"):
        if any("claude-4" in model for model in verified_models["anthropic"]):
            claude_4_models = [m for m in verified_models["anthropic"] if "claude-4" in m]
            recommended_models["anthropic"] = claude_4_models[0]
            print(f"✅ Anthropic: {claude_4_models[0]} (Latest Claude 4 series)")
        else:
            recommended_models["anthropic"] = verified_models["anthropic"][0]
            print(f"⚠️ Anthropic: {verified_models['anthropic'][0]} (Claude 4 not available)")
    else:
        print("❌ Anthropic: No working models found")
    
    # Google recommendation
    if verified_models.get("google_ai"):
        if any("2.5" in model for model in verified_models["google_ai"]):
            gemini_25_models = [m for m in verified_models["google_ai"] if "2.5" in m]
            recommended_models["google_ai"] = gemini_25_models[0]
            print(f"✅ Google: {gemini_25_models[0]} (Latest Gemini 2.5 series)")
        elif any("2.0" in model or "2-0" in model for model in verified_models["google_ai"]):
            gemini_20_models = [m for m in verified_models["google_ai"] if "2.0" in m or "2-0" in m]
            recommended_models["google_ai"] = gemini_20_models[0]
            print(f"⚠️ Google: {gemini_20_models[0]} (Gemini 2.5 not available)")
        else:
            recommended_models["google_ai"] = verified_models["google_ai"][0]
            print(f"⚠️ Google: {verified_models['google_ai'][0]} (Latest available)")
    else:
        print("❌ Google: No working models found")
    
    # Generate updated experiment YAML snippet
    print("\n📝 UPDATED EXPERIMENT YAML MODELS SECTION:")
    print("-" * 40)
    print("  models:")
    
    for provider, model in recommended_models.items():
        if provider == "openai":
            print(f'    - id: "{model}"')
            print(f'      provider: "openai"')
            print(f'      version: "latest"')
        elif provider == "anthropic":
            print(f'    - id: "{model}"')
            print(f'      provider: "anthropic"')
            print(f'      version: "latest"')
        elif provider == "google_ai":
            print(f'    - id: "{model}"')
            print(f'      provider: "google"')
            print(f'      version: "latest"')
    
    # Save results to file
    results = {
        "timestamp": datetime.now().isoformat(),
        "connection_status": connection_results,
        "available_models": available_models,
        "verified_models": verified_models,
        "recommended_models": recommended_models
    }
    
    results_file = Path(__file__).parent / "model_availability_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: {results_file}")
    print("\n🎯 Ready to update your comprehensive experiment with verified models!")
    
    return recommended_models

if __name__ == "__main__":
    try:
        recommended = test_model_availability()
        
        if len(recommended) >= 2:
            print(f"\n🚀 SUCCESS: Found {len(recommended)} working flagship providers")
            print("   Ready for multi-LLM comprehensive study!")
        else:
            print(f"\n⚠️ WARNING: Only {len(recommended)} working providers found")
            print("   Consider single-LLM study or troubleshoot API connections")
            
    except KeyboardInterrupt:
        print("\n\n⏹️ Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Testing failed: {e}")
        import traceback
        traceback.print_exc() 