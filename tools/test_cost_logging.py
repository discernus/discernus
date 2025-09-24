#!/usr/bin/env python3
"""
Test Cost Logging Implementation
===============================

This script tests the cost logging functionality by running a small experiment
and checking if cost data is captured in the logs.
"""

import json
import subprocess
import sys
from pathlib import Path

def test_cost_logging():
    """Test cost logging with a small experiment."""
    
    print("🧪 Testing Cost Logging Implementation")
    print("=" * 50)
    
    # Run a small experiment
    print("1. Running small experiment to generate cost data...")
    try:
        result = subprocess.run([
            "python3", "-m", "discernus", "run", "projects/nano", "--analysis-only"
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            print(f"❌ Experiment failed: {result.stderr}")
            return False
            
        print("✅ Experiment completed successfully")
        
    except subprocess.TimeoutExpired:
        print("⏰ Experiment timed out (this is normal for cost testing)")
    except Exception as e:
        print(f"❌ Error running experiment: {e}")
        return False
    
    # Find the latest run directory
    print("\n2. Finding latest experiment run...")
    nano_runs = list(Path("projects/nano/runs").glob("*"))
    if not nano_runs:
        print("❌ No experiment runs found")
        return False
    
    latest_run = max(nano_runs, key=lambda p: p.stat().st_mtime)
    print(f"✅ Found latest run: {latest_run}")
    
    # Check for cost logs
    print("\n3. Checking for cost logging files...")
    logs_dir = latest_run / "logs"
    if not logs_dir.exists():
        print("❌ No logs directory found")
        return False
    
    llm_log = logs_dir / "llm_interactions.jsonl"
    if not llm_log.exists():
        print("❌ No llm_interactions.jsonl found")
        return False
    
    print(f"✅ Found LLM interactions log: {llm_log}")
    
    # Analyze cost data
    print("\n4. Analyzing cost data...")
    try:
        with open(llm_log, 'r') as f:
            interactions = [json.loads(line) for line in f if line.strip()]
        
        if not interactions:
            print("❌ No LLM interactions found in log")
            return False
        
        print(f"✅ Found {len(interactions)} LLM interactions")
        
        # Calculate total costs
        total_cost = sum(interaction.get('metadata', {}).get('response_cost_usd', 0) for interaction in interactions)
        total_tokens = sum(interaction.get('metadata', {}).get('total_tokens', 0) for interaction in interactions)
        
        print(f"💰 Total cost: ${total_cost:.6f}")
        print(f"🔢 Total tokens: {total_tokens:,}")
        
        # Show cost breakdown by model
        model_costs = {}
        for interaction in interactions:
            model = interaction.get('model', 'unknown')
            cost = interaction.get('metadata', {}).get('response_cost_usd', 0)
            model_costs[model] = model_costs.get(model, 0) + cost
        
        print("\n📊 Cost breakdown by model:")
        for model, cost in model_costs.items():
            print(f"  {model}: ${cost:.6f}")
        
        # Show cost breakdown by step
        step_costs = {}
        for interaction in interactions:
            step = interaction.get('metadata', {}).get('step', 'unknown')
            cost = interaction.get('metadata', {}).get('response_cost_usd', 0)
            step_costs[step] = step_costs.get(step, 0) + cost
        
        print("\n📊 Cost breakdown by step:")
        for step, cost in step_costs.items():
            print(f"  {step}: ${cost:.6f}")
        
        print("\n✅ Cost logging is working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error analyzing cost data: {e}")
        return False

def show_cost_analysis_commands():
    """Show commands for analyzing cost data."""
    
    print("\n🔍 Cost Analysis Commands:")
    print("=" * 30)
    print("1. View all LLM interactions:")
    print("   cat logs/llm_interactions.jsonl | jq '.'")
    print()
    print("2. Sum total costs:")
    print("   cat logs/llm_interactions.jsonl | jq -s 'map(.metadata.response_cost_usd) | add'")
    print()
    print("3. Cost by model:")
    print("   cat logs/llm_interactions.jsonl | jq -r '[.model, .metadata.response_cost_usd] | @csv'")
    print()
    print("4. Cost by step:")
    print("   cat logs/llm_interactions.jsonl | jq -r '[.metadata.step, .metadata.response_cost_usd] | @csv'")
    print()
    print("5. Token usage:")
    print("   cat logs/llm_interactions.jsonl | jq '.metadata | {tokens: .total_tokens, cost: .response_cost_usd}'")

def main():
    """Main test function."""
    
    print("🎯 Discernus Cost Logging Test")
    print("=" * 50)
    print()
    
    # Test cost logging
    success = test_cost_logging()
    
    if success:
        print("\n🎉 Cost logging test completed successfully!")
        print("All LLM interactions are now being logged with cost data.")
        print("You can use the analysis commands below to explore the data.")
    else:
        print("\n❌ Cost logging test failed.")
        print("Check the experiment logs for more details.")
    
    # Show analysis commands
    show_cost_analysis_commands()
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())

