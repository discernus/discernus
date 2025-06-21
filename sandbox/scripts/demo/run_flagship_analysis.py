#!/usr/bin/env python3
"""
Flagship LLM Analysis Runner - Updated for 2025 Models
Comprehensive narrative gravity analysis using latest OpenAI, Anthropic, Mistral, and Google AI models
"""

import sys
import json
import time
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.api_clients.direct_api_client import DirectAPIClient

# Analysis frameworks available
FRAMEWORKS = [
    "civic_virtue",
    "political_spectrum", 
    "moral_rhetorical_posture"
]

# Default test texts for analysis
DEFAULT_TEXTS = {
    "political_speech": """
    My fellow Americans, in these challenging times, we must come together as one nation to rebuild our economy and restore our values. While some may focus on past failures, I believe we have the strength and innovation to create new opportunities for all our citizens. The path forward requires both individual responsibility and collective action. We must invest in our infrastructure, support our small businesses, and ensure that every child has access to quality education. Together, we can build a stronger, more prosperous future for generations to come.
    """,
    
    "policy_debate": """
    The proposed healthcare reform represents a fundamental choice between two competing visions of America. On one hand, we have those who believe that healthcare is a fundamental right that should be guaranteed by government. On the other hand, we have those who argue that market-based solutions will provide better care at lower costs. Both sides raise important concerns about access, quality, and fiscal responsibility. The challenge is finding a balanced approach that protects the vulnerable while maintaining innovation and choice.
    """,
    
    "corporate_message": """
    At TechCorp, we believe that innovation drives progress, and progress drives prosperity for all. Our commitment to sustainability isn't just about doing the right thing for the environment – it's about creating long-term value for our shareholders, our employees, and our communities. We're investing in clean energy, developing eco-friendly products, and fostering a culture of responsibility. Because when businesses lead with purpose, everyone benefits.
    """
}

# 2025 Model recommendations by use case
RECOMMENDED_MODELS_2025 = {
    "cost_effective": [
        "gpt-4.1-mini",
        "claude-3.5-haiku", 
        "gemini-2.0-flash",
        "mistral-small-2409"
    ],
    "advanced_reasoning": [
        "o1",
        "o3",
        "claude-4-opus",
        "claude-3.7-sonnet",
        "gemini-2.5-pro"
    ],
    "balanced_performance": [
        "gpt-4.1",
        "claude-4-sonnet",
        "mistral-medium-3",
        "gemini-2.5-flash"
    ],
    "specialized": [
        "codestral-2501",  # For coding analysis
        "devstral-small-2505",  # For technical analysis
        "mistral-saba-2502",  # For multilingual analysis
    ]
}

def run_comprehensive_analysis(client: DirectAPIClient, text: str, output_dir: str = "analysis_results", 
                             model_selection: str = "balanced"):
    """Run analysis across selected frameworks and models"""
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Get available models
    available_models = client.get_available_models()
    
    # Select models based on user preference
    selected_models = select_models_for_analysis(available_models, model_selection)
    
    print(f"🎯 Running Comprehensive Analysis with 2025 Models")
    print(f"📁 Output Directory: {output_path}")
    print(f"📊 Frameworks: {len(FRAMEWORKS)}")
    print(f"🤖 Model Selection: {model_selection}")
    print(f"🔧 Selected Models: {sum(len(models) for models in selected_models.values())}")
    print("=" * 60)
    
    all_results = {}
    total_cost = 0.0
    
    # Run analysis for each framework
    for framework in FRAMEWORKS:
        print(f"\n🔍 Framework: {framework.upper()}")
        print("-" * 40)
        
        framework_results = {}
        
        # Test each selected model
        for provider, models in selected_models.items():
            for model in models:
                model_key = f"{provider}_{model}"
                print(f"  🤖 Testing {provider.title()} - {model}")
                
                try:
                    start_time = time.time()
                    result, cost = client.analyze_text(text, framework, model)
                    duration = time.time() - start_time
                    
                    framework_results[model_key] = {
                        "provider": provider,
                        "model": model,
                        "framework": framework,
                        "result": result,
                        "cost": cost,
                        "duration": duration,
                        "timestamp": datetime.now().isoformat(),
                        "success": True,
                        "model_generation": get_model_generation(provider, model)
                    }
                    
                    total_cost += cost
                    
                    print(f"    ✅ Cost: ${cost:.4f}, Duration: {duration:.1f}s")
                    
                    # Show key insights
                    if "scores" in result and result["scores"]:
                        top_scores = sorted(result["scores"].items(), key=lambda x: x[1], reverse=True)[:3]
                        print(f"    📊 Top Scores: {', '.join([f'{k}({v})' for k, v in top_scores])}")
                    
                except Exception as e:
                    framework_results[model_key] = {
                        "provider": provider,
                        "model": model, 
                        "framework": framework,
                        "error": str(e),
                        "success": False,
                        "timestamp": datetime.now().isoformat(),
                        "model_generation": get_model_generation(provider, model)
                    }
                    print(f"    ❌ Failed: {e}")
        
        all_results[framework] = framework_results
        
        # Save framework results
        framework_file = output_path / f"{framework}_results.json"
        with open(framework_file, 'w') as f:
            json.dump(framework_results, f, indent=2, default=str)
        print(f"  💾 Saved: {framework_file}")
    
    # Save comprehensive results
    summary = {
        "analysis_timestamp": datetime.now().isoformat(),
        "total_cost": total_cost,
        "model_selection": model_selection,
        "frameworks_tested": len(FRAMEWORKS),
        "models_tested": sum(len(models) for models in selected_models.values()),
        "text_analyzed": text[:200] + "..." if len(text) > 200 else text,
        "selected_models": selected_models,
        "results": all_results
    }
    
    summary_file = output_path / "comprehensive_analysis.json"
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2, default=str)
    
    return summary, total_cost

def select_models_for_analysis(available_models: Dict, selection: str) -> Dict:
    """Select models based on user preference and 2025 recommendations"""
    
    if selection == "all":
        return available_models
    
    elif selection == "2025_only":
        # Only 2025 models
        selected = {}
        for provider, models in available_models.items():
            selected[provider] = []
            for model in models:
                if get_model_generation(provider, model) == "2025":
                    selected[provider].append(model)
        return {k: v for k, v in selected.items() if v}
    
    elif selection in RECOMMENDED_MODELS_2025:
        # Use recommended models for specific use case
        recommended = RECOMMENDED_MODELS_2025[selection]
        selected = {}
        
        for provider, models in available_models.items():
            selected[provider] = []
            for model in models:
                if model in recommended:
                    selected[provider].append(model)
        return {k: v for k, v in selected.items() if v}
    
    else:  # "balanced" or default
        # Balanced selection: latest from each provider
        selected = {}
        for provider, models in available_models.items():
            selected[provider] = []
            
            if provider == "openai":
                # Prefer GPT-4.1 series, fallback to GPT-4o
                for model in ["gpt-4.1", "gpt-4.1-mini", "gpt-4o"]:
                    if model in models:
                        selected[provider].append(model)
                        break
                        
            elif provider == "anthropic":
                # Prefer Claude 4, fallback to Claude 3.5
                for model in ["claude-4-sonnet", "claude-3.5-sonnet"]:
                    if model in models:
                        selected[provider].append(model)
                        break
                        
            elif provider == "mistral":
                # Prefer Medium 3, fallback to Large 2411
                for model in ["mistral-medium-3", "mistral-large-2411"]:
                    if model in models:
                        selected[provider].append(model)
                        break
                        
            elif provider == "google_ai":
                # Prefer Gemini 2.5, fallback to 2.0
                for model in ["gemini-2.5-flash", "gemini-2.0-flash"]:
                    if model in models:
                        selected[provider].append(model)
                        break
        
        return {k: v for k, v in selected.items() if v}

def get_model_generation(provider: str, model: str) -> str:
    """Determine model generation (2025, 2024, legacy)"""
    if provider == "openai":
        if "4.1" in model or model.startswith("o"):
            return "2025"
        elif "4o" in model:
            return "2024"
        else:
            return "legacy"
    
    elif provider == "anthropic":
        if "claude-4" in model or "3.7" in model:
            return "2025"
        elif "3.5" in model or "3-5" in model:
            return "2024"
        else:
            return "legacy"
    
    elif provider == "mistral":
        if any(x in model for x in ["medium-3", "codestral-2501", "devstral", "saba", "ocr-2505"]):
            return "2025"
        elif "2411" in model or "2409" in model:
            return "2024"
        else:
            return "legacy"
    
    elif provider == "google_ai":
        if "2.5" in model:
            return "2025"
        elif "2.0" in model or "2-0" in model:
            return "2024"
        else:
            return "legacy"
    
    return "unknown"

def analyze_text_samples(client: DirectAPIClient, output_dir: str = "analysis_results", 
                        model_selection: str = "balanced"):
    """Analyze multiple text samples with 2025 models"""
    
    print(f"🧪 Analyzing Default Text Samples with 2025 Models")
    print("=" * 55)
    
    all_summaries = {}
    total_cost = 0.0
    
    for text_name, text_content in DEFAULT_TEXTS.items():
        print(f"\n📄 Analyzing: {text_name.replace('_', ' ').title()}")
        print(f"📝 Text Preview: {text_content[:100]}...")
        
        # Create subdirectory for this text
        text_output_dir = Path(output_dir) / text_name
        
        summary, cost = run_comprehensive_analysis(
            client, text_content, str(text_output_dir), model_selection
        )
        all_summaries[text_name] = summary
        total_cost += cost
        
        print(f"💰 Cost for {text_name}: ${cost:.4f}")
    
    # Save overall summary
    overall_summary = {
        "analysis_timestamp": datetime.now().isoformat(),
        "total_cost": total_cost,
        "model_selection": model_selection,
        "texts_analyzed": len(DEFAULT_TEXTS),
        "summaries": all_summaries
    }
    
    overall_file = Path(output_dir) / "overall_analysis_summary.json"
    with open(overall_file, 'w') as f:
        json.dump(overall_summary, f, indent=2, default=str)
    
    print(f"\n📊 ANALYSIS COMPLETE")
    print(f"💰 Total Cost: ${total_cost:.4f}")
    print(f"📁 Results saved in: {output_dir}")
    print(f"📄 Summary: {overall_file}")
    
    return overall_summary

def compare_model_performance(results_dir: str = "analysis_results"):
    """Compare performance across different models and generations"""
    
    print(f"📊 2025 Model Performance Comparison")
    print("=" * 45)
    
    results_path = Path(results_dir)
    if not results_path.exists():
        print(f"❌ Results directory not found: {results_dir}")
        return
    
    # Look for comprehensive analysis results
    summary_file = results_path / "overall_analysis_summary.json"
    if not summary_file.exists():
        print(f"❌ Analysis summary not found: {summary_file}")
        return
    
    with open(summary_file, 'r') as f:
        summary = json.load(f)
    
    print(f"📈 Analysis from: {summary['analysis_timestamp']}")
    print(f"💰 Total cost: ${summary['total_cost']:.4f}")
    print(f"🔧 Model selection: {summary['model_selection']}")
    
    # Analyze results by generation
    generation_stats = {"2025": [], "2024": [], "legacy": []}
    
    for text_name, text_summary in summary["summaries"].items():
        for framework, framework_results in text_summary["results"].items():
            for model_key, result in framework_results.items():
                if result["success"]:
                    generation = result.get("model_generation", "unknown")
                    if generation in generation_stats:
                        generation_stats[generation].append({
                            "cost": result["cost"],
                            "duration": result["duration"],
                            "model": result["model"],
                            "provider": result["provider"]
                        })
    
    # Display comparison
    print(f"\n🆚 Performance by Generation:")
    for generation, results in generation_stats.items():
        if results:
            avg_cost = sum(r["cost"] for r in results) / len(results)
            avg_duration = sum(r["duration"] for r in results) / len(results)
            models = set(f"{r['provider']}-{r['model']}" for r in results)
            
            icon = "🆕" if generation == "2025" else "🔄" if generation == "2024" else "📜"
            print(f"  {icon} {generation.upper()}: {len(results)} tests")
            print(f"    💰 Avg Cost: ${avg_cost:.4f}")
            print(f"    ⏱️ Avg Duration: {avg_duration:.1f}s")
            print(f"    🤖 Models: {len(models)}")
            print()

def main():
    """Main analysis function with 2025 model support"""
    parser = argparse.ArgumentParser(
        description="Run narrative gravity analysis with 2025 flagship LLMs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Model Selection Options:
  balanced         - Latest model from each provider (default)
  2025_only        - Only 2025 models (GPT-4.1, Claude 4, etc.)
  cost_effective   - Cheapest 2025 models with good performance
  advanced_reasoning - Models optimized for complex reasoning
  specialized      - Domain-specific models (coding, multilingual)
  all              - Test all available models

Examples:
  %(prog)s --samples --models balanced
  %(prog)s --text "Your text" --models 2025_only
  %(prog)s --compare results/
        """
    )
    
    parser.add_argument("--text", type=str, help="Custom text to analyze")
    parser.add_argument("--framework", choices=FRAMEWORKS, help="Specific framework to use")
    parser.add_argument("--output", default="analysis_results", help="Output directory")
    parser.add_argument("--samples", action="store_true", help="Analyze default text samples")
    parser.add_argument("--models", choices=["balanced", "2025_only", "cost_effective", 
                                            "advanced_reasoning", "specialized", "all"],
                       default="balanced", help="Model selection strategy")
    parser.add_argument("--compare", type=str, help="Compare results from directory")
    
    args = parser.parse_args()
    
    print("🚀 Flagship LLM Narrative Gravity Analysis (2025 Edition)")
    print("🤖 Using OpenAI GPT-4.1, Claude 4, Mistral Medium 3, Gemini 2.5")
    print("=" * 65)
    
    # Handle comparison mode
    if args.compare:
        compare_model_performance(args.compare)
        return
    
    # Initialize client
    try:
        client = DirectAPIClient()
        available_models = client.get_available_models()
        
        if not available_models:
            print("❌ No API clients available. Check your .env file.")
            return
        
        print(f"✅ Connected to {len(available_models)} providers")
        
        # Show available 2025 models
        print(f"\n🆕 Available 2025 Models:")
        for provider, models in available_models.items():
            gen_2025_models = [m for m in models if get_model_generation(provider, m) == "2025"]
            if gen_2025_models:
                print(f"  {provider.upper()}: {', '.join(gen_2025_models)}")
        
        # Run analysis based on arguments
        if args.samples:
            analyze_text_samples(client, args.output, args.models)
        elif args.text:
            if args.framework:
                # Single framework analysis
                result, cost = client.analyze_text(args.text, args.framework, "gpt-4.1")
                print(f"Result: {result}")
                print(f"Cost: ${cost:.4f}")
            else:
                # Comprehensive analysis
                summary, cost = run_comprehensive_analysis(
                    client, args.text, args.output, args.models
                )
                print(f"\n📊 Analysis Complete")
                print(f"💰 Total Cost: ${cost:.4f}")
                print(f"📁 Results: {args.output}")
        else:
            # Show help and model info
            print(f"\n🔧 Selected Model Strategy: {args.models}")
            selected_models = select_models_for_analysis(available_models, args.models)
            
            print(f"\n📋 Models that would be tested:")
            for provider, models in selected_models.items():
                if models:
                    print(f"  {provider.upper()}: {', '.join(models)}")
            
            print(f"\nTo run analysis:")
            print(f"  --samples                    # Test with default texts")
            print(f"  --text 'Your text here'      # Analyze custom text")
            print(f"  --compare results/           # Compare existing results")
            
    except Exception as e:
        print(f"❌ Error initializing client: {e}")
        return

if __name__ == "__main__":
    main() 