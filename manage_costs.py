#!/usr/bin/env python3
"""
API Cost Management CLI - Updated for 2025 Models
Command-line tool for managing API costs and limits with advanced model comparison
"""

import sys
import argparse
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.utils.cost_manager import CostManager

def show_status(cost_manager: CostManager):
    """Show current cost status"""
    summary = cost_manager.get_spending_summary()
    
    print("💰 API Cost Status")
    print("=" * 50)
    
    # Current limits
    limits = summary["current_limits"]
    print(f"📊 Current Limits:")
    print(f"  Daily: ${limits['daily_limit']:.2f}")
    print(f"  Weekly: ${limits['weekly_limit']:.2f}")
    print(f"  Monthly: ${limits['monthly_limit']:.2f}")
    print(f"  Single Request: ${limits['single_request_limit']:.2f}")
    
    # Current spending
    spending = summary["spending"]
    print(f"\n💸 Current Spending:")
    print(f"  Today: ${spending['today']:.4f}")
    print(f"  This Week: ${spending['this_week']:.4f}")
    print(f"  This Month: ${spending['this_month']:.4f}")
    print(f"  Total: ${spending['total']:.4f}")
    
    # Usage by provider
    if summary["usage_by_provider"]:
        print(f"\n🤖 Usage by Provider:")
        for provider, usage in summary["usage_by_provider"].items():
            print(f"  {provider.title()}: ${usage['cost']:.4f} ({usage['requests']} requests)")
    
    # Usage by model
    if summary["usage_by_model"]:
        print(f"\n📱 Usage by Model:")
        for model, usage in summary["usage_by_model"].items():
            print(f"  {model}: ${usage['cost']:.4f} ({usage['requests']} requests)")
    
    print(f"\n📈 Total Requests: {summary['total_requests']}")

def set_limits(cost_manager: CostManager, args):
    """Set cost limits"""
    print("🛡️ Setting Cost Limits")
    print("=" * 30)
    
    cost_manager.set_limits(
        daily=args.daily,
        weekly=args.weekly,
        monthly=args.monthly,
        single_request=args.single_request
    )

def estimate_cost(cost_manager: CostManager, args):
    """Estimate cost for text analysis"""
    print("📊 Cost Estimation")
    print("=" * 30)
    
    total_cost = 0.0
    
    # Estimate for each provider/model
    providers = ["openai", "anthropic", "mistral", "google_ai"]
    models = {
        "openai": ["gpt-4.1", "gpt-4.1-mini", "gpt-4o", "o1"],
        "anthropic": ["claude-4-sonnet", "claude-3.5-sonnet", "claude-3.7-sonnet"],
        "mistral": ["mistral-medium-3", "mistral-large-2411", "codestral-2501"],
        "google_ai": ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.0-flash"]
    }
    
    print(f"📝 Text length: {len(args.text)} characters, {len(args.text.split())} words")
    print(f"\n💰 Estimated costs for 2025 models:")
    
    for provider in providers:
        print(f"\n  🏢 {provider.upper()}:")
        for model in models[provider]:
            cost, input_tokens, output_tokens = cost_manager.estimate_cost(args.text, provider, model)
            model_info = cost_manager.get_model_info(provider, model)
            generation = model_info.get("generation", "unknown")
            
            print(f"    {model}: ${cost:.4f} ({input_tokens} in + {output_tokens} out) [{generation}]")
            total_cost += cost
    
    print(f"\n🎯 Total for all latest models: ${total_cost:.4f}")
    
    # Check against limits
    can_proceed, message = cost_manager.check_limits_before_request(total_cost)
    if can_proceed:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")

def compare_models(cost_manager: CostManager, args):
    """Compare models for cost and capabilities"""
    print("🔍 Model Comparison for 2025")
    print("=" * 40)
    
    comparison = cost_manager.get_cost_comparison(args.text)
    
    print(f"📝 Analyzing text: {args.text[:100]}{'...' if len(args.text) > 100 else ''}")
    print(f"📏 Length: {len(args.text)} characters, {len(args.text.split())} words\n")
    
    for provider, models in comparison.items():
        print(f"🏢 {provider.upper()}")
        print("-" * 30)
        
        # Sort models by cost
        sorted_models = sorted(models.items(), key=lambda x: x[1]["estimated_cost"])
        
        for model, info in sorted_models:
            generation_icon = "🆕" if info["generation"] == "2025" else "🔄" if info["generation"] == "2024" else "📜"
            capabilities = ", ".join(info["capabilities"][:3])  # Show first 3 capabilities
            
            print(f"  {generation_icon} {model}")
            print(f"    💰 Cost: ${info['estimated_cost']:.4f}")
            print(f"    🎯 Use: {info['recommended_use']}")
            if capabilities:
                print(f"    ⚡ Features: {capabilities}")
            print()

def get_recommendations(cost_manager: CostManager, args):
    """Get model recommendations based on value"""
    print("🎯 Best Value Model Recommendations")
    print("=" * 40)
    
    max_cost = getattr(args, 'max_cost', None)
    recommendations = cost_manager.get_best_value_models(args.text, max_cost)
    
    print(f"📝 Analyzing: {args.text[:100]}{'...' if len(args.text) > 100 else ''}")
    if max_cost:
        print(f"💰 Maximum cost filter: ${max_cost:.4f}")
    print()
    
    for i, rec in enumerate(recommendations[:5], 1):  # Show top 5
        generation_icon = "🆕" if rec["generation"] == "2025" else "🔄" if rec["generation"] == "2024" else "📜"
        
        print(f"{i}. {generation_icon} {rec['provider'].upper()} - {rec['model']}")
        print(f"   💰 Cost: ${rec['estimated_cost']:.4f}")
        print(f"   ⭐ Value Score: {rec['value_score']:.1f}")
        print(f"   🎯 Best for: {rec['recommended_use']}")
        if rec['capabilities']:
            print(f"   ⚡ Key features: {', '.join(rec['capabilities'][:2])}")
        print()

def model_info(cost_manager: CostManager, args):
    """Show detailed information about a specific model"""
    print(f"📋 Model Information: {args.provider.upper()} - {args.model}")
    print("=" * 50)
    
    info = cost_manager.get_model_info(args.provider, args.model)
    
    if "error" in info:
        print(f"❌ {info['error']}")
        return
    
    # Basic info
    generation_icon = "🆕" if info["generation"] == "2025" else "🔄" if info["generation"] == "2024" else "📜"
    print(f"{generation_icon} Generation: {info['generation']}")
    print(f"🎯 Recommended use: {info['recommended_use']}")
    
    if info["context_window"] != "unknown":
        print(f"📏 Context window: {info['context_window']}")
    
    # Pricing
    pricing = info["pricing"]
    print(f"\n💰 Pricing:")
    if "per_operation" in pricing:
        print(f"  Per operation: ${pricing['per_operation']:.4f}")
    else:
        print(f"  Input: ${pricing['input']:.6f} per 1K tokens/chars")
        print(f"  Output: ${pricing['output']:.6f} per 1K tokens/chars")
    
    # Capabilities
    if info["capabilities"]:
        print(f"\n⚡ Key Capabilities:")
        for capability in info["capabilities"]:
            print(f"  • {capability}")
    
    # Cost estimate for sample text
    if hasattr(args, 'sample_text') and args.sample_text:
        cost, input_tokens, output_tokens = cost_manager.estimate_cost(
            args.sample_text, args.provider, args.model
        )
        print(f"\n📊 Sample Analysis Estimate:")
        print(f"  Text: {args.sample_text[:50]}{'...' if len(args.sample_text) > 50 else ''}")
        print(f"  Cost: ${cost:.4f}")
        print(f"  Tokens: {input_tokens} input + {output_tokens} output")

def export_data(cost_manager: CostManager, args):
    """Export cost data"""
    filename = cost_manager.export_costs(args.filename)
    print(f"✅ Cost data exported to: {filename}")

def reset_costs(cost_manager: CostManager):
    """Reset cost tracking (with confirmation)"""
    print("⚠️ WARNING: This will delete all cost tracking data!")
    response = input("Type 'YES' to confirm: ")
    
    if response == "YES":
        # Clear costs
        cost_manager.costs = []
        cost_manager._save_costs()
        print("✅ Cost tracking data reset")
    else:
        print("❌ Reset cancelled")

def monitor_mode(cost_manager: CostManager):
    """Interactive monitoring mode"""
    import time
    
    print("📊 Cost Monitor Mode (Press Ctrl+C to exit)")
    print("=" * 50)
    
    try:
        while True:
            # Clear screen (works on most terminals)
            print("\033[H\033[J")
            
            show_status(cost_manager)
            
            # Sleep for 10 seconds
            print(f"\n🔄 Refreshing in 10 seconds... (Ctrl+C to exit)")
            time.sleep(10)
            
            # Reload cost data
            cost_manager._load_costs()
            
    except KeyboardInterrupt:
        print("\n👋 Exiting monitor mode")

def list_models(cost_manager: CostManager):
    """List all available models with their capabilities"""
    print("🤖 Available Models for 2025")
    print("=" * 40)
    
    providers = ["openai", "anthropic", "mistral", "google_ai"]
    
    for provider in providers:
        print(f"\n🏢 {provider.upper()}")
        print("-" * 30)
        
        if provider in cost_manager.model_costs:
            models = cost_manager.model_costs[provider]
            
            # Group by generation
            gen_2025 = []
            gen_2024 = []
            legacy = []
            
            for model in models:
                info = cost_manager.get_model_info(provider, model)
                if info["generation"] == "2025":
                    gen_2025.append((model, info))
                elif info["generation"] == "2024":
                    gen_2024.append((model, info))
                else:
                    legacy.append((model, info))
            
            # Show 2025 models first
            if gen_2025:
                print("  🆕 2025 Models (Latest):")
                for model, info in gen_2025:
                    cost_str = f"${info['pricing']['input']:.6f}" if 'input' in info['pricing'] else "Variable"
                    print(f"    • {model} - {cost_str}/1K - {info['recommended_use']}")
            
            if gen_2024:
                print("  🔄 2024 Models (Current):")
                for model, info in gen_2024:
                    cost_str = f"${info['pricing']['input']:.6f}" if 'input' in info['pricing'] else "Variable"
                    print(f"    • {model} - {cost_str}/1K - {info['recommended_use']}")
            
            if legacy:
                print("  📜 Legacy Models:")
                for model, info in legacy:
                    cost_str = f"${info['pricing']['input']:.6f}" if 'input' in info['pricing'] else "Variable"
                    print(f"    • {model} - {cost_str}/1K")

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="Manage API costs and compare 2025 models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s status                           # Show current spending
  %(prog)s compare "Your text here"         # Compare all models
  %(prog)s recommend "Your text here"       # Get best value recommendations
  %(prog)s info openai gpt-4.1             # Show model details
  %(prog)s estimate "Your text here"        # Estimate costs
  %(prog)s models                           # List all available models
        """
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Status command
    subparsers.add_parser("status", help="Show current cost status")
    
    # Set limits command
    limits_parser = subparsers.add_parser("limits", help="Set cost limits")
    limits_parser.add_argument("--daily", type=float, help="Daily limit in USD")
    limits_parser.add_argument("--weekly", type=float, help="Weekly limit in USD")
    limits_parser.add_argument("--monthly", type=float, help="Monthly limit in USD")
    limits_parser.add_argument("--single-request", type=float, help="Single request limit in USD")
    
    # Estimate command
    estimate_parser = subparsers.add_parser("estimate", help="Estimate cost for text")
    estimate_parser.add_argument("text", help="Text to estimate cost for")
    
    # Compare command
    compare_parser = subparsers.add_parser("compare", help="Compare models for text analysis")
    compare_parser.add_argument("text", help="Text to analyze")
    
    # Recommend command
    recommend_parser = subparsers.add_parser("recommend", help="Get best value model recommendations")
    recommend_parser.add_argument("text", help="Text to analyze")
    recommend_parser.add_argument("--max-cost", type=float, help="Maximum cost filter")
    
    # Model info command
    info_parser = subparsers.add_parser("info", help="Show detailed model information")
    info_parser.add_argument("provider", choices=["openai", "anthropic", "mistral", "google_ai"])
    info_parser.add_argument("model", help="Model name")
    info_parser.add_argument("--sample-text", help="Sample text for cost estimation")
    
    # List models command
    subparsers.add_parser("models", help="List all available models")
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export cost data to CSV")
    export_parser.add_argument("--filename", help="Output filename")
    
    # Reset command
    subparsers.add_parser("reset", help="Reset cost tracking data")
    
    # Monitor command
    subparsers.add_parser("monitor", help="Real-time cost monitoring")
    
    args = parser.parse_args()
    
    # Initialize cost manager
    cost_manager = CostManager()
    
    # Execute command
    if args.command == "status":
        show_status(cost_manager)
    elif args.command == "limits":
        set_limits(cost_manager, args)
    elif args.command == "estimate":
        estimate_cost(cost_manager, args)
    elif args.command == "compare":
        compare_models(cost_manager, args)
    elif args.command == "recommend":
        get_recommendations(cost_manager, args)
    elif args.command == "info":
        model_info(cost_manager, args)
    elif args.command == "models":
        list_models(cost_manager)
    elif args.command == "export":
        export_data(cost_manager, args)
    elif args.command == "reset":
        reset_costs(cost_manager)
    elif args.command == "monitor":
        monitor_mode(cost_manager)
    else:
        # Show help with new features
        print("🛡️ API Cost Management for 2025 Models")
        print("=" * 45)
        print("Available commands:")
        print("  status      - Show current spending and limits")
        print("  limits      - Set spending limits")
        print("  estimate    - Estimate cost for text analysis")
        print("  compare     - Compare 2025 models for text")
        print("  recommend   - Get best value model recommendations")
        print("  info        - Show detailed model information")
        print("  models      - List all available 2025 models")
        print("  export      - Export cost data to CSV")
        print("  reset       - Reset cost tracking")
        print("  monitor     - Real-time monitoring")
        print()
        print("🆕 New 2025 Features:")
        print("  • Latest GPT-4.1, Claude 4, Mistral Medium 3, Gemini 2.5")
        print("  • Cost comparisons across all providers")
        print("  • Smart model recommendations")
        print("  • Detailed capability analysis")

if __name__ == "__main__":
    main() 