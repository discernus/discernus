#!/usr/bin/env python3
"""
Test Direct API Integration
Tests OpenAI, Anthropic, and Mistral API connections and narrative analysis
"""

import sys
from pathlib import Path
import json
import time

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.api_clients.direct_api_client import DirectAPIClient

def test_api_connections():
    """Test all API connections"""
    print("🔧 Testing API Connections...")
    print("=" * 50)
    
    client = DirectAPIClient()
    results = client.test_connections()
    
    print(f"\n📊 Connection Results:")
    for provider, status in results.items():
        status_emoji = "✅" if status else "❌"
        print(f"  {status_emoji} {provider.title()}: {'Connected' if status else 'Failed'}")
    
    return client, results

def test_narrative_analysis(client, test_text=None):
    """Test narrative analysis with all available models"""
    if test_text is None:
        test_text = """
        In these challenging times, we must come together as a community to rebuild our economy. 
        While some may focus on past failures, I believe we have the strength and innovation 
        to create new opportunities for all our citizens. The path forward requires both 
        individual responsibility and collective action.
        """
    
    print(f"\n🧪 Testing Narrative Analysis...")
    print("=" * 50)
    print(f"Test Text: {test_text[:100]}...")
    
    # Get available models
    available_models = client.get_available_models()
    print(f"\n📋 Available Models:")
    for provider, models in available_models.items():
        print(f"  {provider.title()}: {', '.join(models)}")
    
    # Test with each available model using civic_virtue framework
    framework = "civic_virtue"
    print(f"\n🎯 Testing with Framework: {framework}")
    
    all_results = {}
    
    for provider, models in available_models.items():
        if not models:
            continue
            
        # Test with first model from each provider
        model = models[0]
        print(f"\n🔄 Testing {provider.title()} - {model}")
        
        try:
            start_time = time.time()
            result, cost = client.analyze_text(test_text, framework, model)
            duration = time.time() - start_time
            
            all_results[f"{provider}_{model}"] = {
                "result": result,
                "cost": cost,
                "duration": duration,
                "success": True
            }
            
            print(f"  ✅ Success! Cost: ${cost:.4f}, Duration: {duration:.2f}s")
            
            # Show parsed scores if available
            if "scores" in result and result["scores"]:
                print(f"  📊 Scores: {result['scores']}")
            elif "error" not in result:
                print(f"  📝 Response: {str(result)[:100]}...")
            
        except Exception as e:
            all_results[f"{provider}_{model}"] = {
                "error": str(e),
                "success": False
            }
            print(f"  ❌ Failed: {e}")
    
    return all_results

def save_test_results(results):
    """Save test results to file"""
    results_file = "test_results_direct_apis.json"
    
    # Format results for JSON serialization
    formatted_results = {}
    for key, result in results.items():
        formatted_results[key] = {
            "success": result.get("success", False),
            "cost": result.get("cost", 0.0),
            "duration": result.get("duration", 0.0),
            "has_scores": bool(result.get("result", {}).get("scores", {})),
            "error": result.get("error", None)
        }
    
    with open(results_file, 'w') as f:
        json.dump(formatted_results, f, indent=2)
    
    print(f"\n💾 Results saved to: {results_file}")

def main():
    """Main test function"""
    print("🚀 Direct API Integration Test")
    print("Testing OpenAI, Anthropic, and Mistral APIs")
    print("=" * 60)
    
    # Test connections
    client, connection_results = test_api_connections()
    
    # Check if any connections work
    if not any(connection_results.values()):
        print("\n❌ No API connections successful. Please check your API keys in .env file.")
        print("\nRequired environment variables:")
        print("  OPENAI_API_KEY=your_openai_key")
        print("  ANTHROPIC_API_KEY=your_anthropic_key") 
        print("  MISTRAL_API_KEY=your_mistral_key")
        return
    
    # Test narrative analysis
    analysis_results = test_narrative_analysis(client)
    
    # Save results
    save_test_results(analysis_results)
    
    # Summary
    successful_tests = sum(1 for r in analysis_results.values() if r.get("success", False))
    total_tests = len(analysis_results)
    total_cost = sum(r.get("cost", 0) for r in analysis_results.values())
    
    print(f"\n📊 Test Summary:")
    print(f"  Successful Tests: {successful_tests}/{total_tests}")
    print(f"  Total Cost: ${total_cost:.4f}")
    print(f"  Available Providers: {len([p for p, connected in connection_results.items() if connected])}/3")
    
    if successful_tests > 0:
        print(f"\n🎉 SUCCESS! You can now run narrative gravity analysis with flagship LLMs!")
        print(f"\nNext steps:")
        print(f"  1. Run full analysis: python run_flagship_analysis.py")
        print(f"  2. Try different frameworks: civic_virtue, political_spectrum, moral_rhetorical_posture")
        print(f"  3. Analyze your own text samples")
    else:
        print(f"\n⚠️  No successful analyses. Check API keys and models.")

if __name__ == "__main__":
    main() 