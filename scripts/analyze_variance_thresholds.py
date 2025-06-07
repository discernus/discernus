#!/usr/bin/env python3
"""
Analyze logged variance data to suggest empirical thresholds.
Run this script after collecting sufficient multi-run data.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.utils.statistical_logger import logger
import json
from datetime import datetime

def main():
    """Analyze variance data and suggest thresholds"""
    
    print("📊 Analyzing Variance Threshold Data...")
    print("=" * 50)
    
    # Get variance analysis
    analysis = logger.get_variance_threshold_analysis()
    
    if "error" in analysis:
        print(f"❌ {analysis['error']}")
        print("\n💡 Run some multi-run analyses first to collect variance data.")
        return
    
    # Display current data
    stats = analysis["variance_stats"]
    print(f"📈 Total variance samples: {analysis['total_samples']}")
    print(f"📊 Variance range: {stats['min']:.6f} to {stats['max']:.6f}")
    print(f"📊 Mean variance: {stats['mean']:.6f}")
    print(f"📊 Median variance: {stats['median']:.6f}")
    print()
    
    # Show percentiles
    print("📊 Variance Percentiles:")
    for pct, value in stats["percentiles"].items():
        print(f"   {pct}: {value:.6f}")
    print()
    
    # Current vs suggested thresholds
    current_individual = 0.02
    current_sum = 0.05
    
    suggested = analysis["suggested_thresholds"]
    
    print("🎯 Threshold Comparison:")
    print(f"   Current Individual Threshold: {current_individual:.6f}")
    print(f"   Suggested Individual (10th %): {suggested['individual_minimal']:.6f}")
    print(f"   Suggested Individual (25th %): {suggested['individual_low']:.6f}")
    print()
    print(f"   Current Sum Threshold: {current_sum:.6f}")
    print(f"   Suggested Sum (10th % × 10): {suggested['sum_minimal']:.6f}")
    print()
    
    # Recommendations
    print("💡 Recommendations:")
    
    if suggested['individual_minimal'] > current_individual:
        print(f"   ⬆️  Consider increasing individual threshold to {suggested['individual_minimal']:.6f}")
    elif suggested['individual_minimal'] < current_individual:
        print(f"   ⬇️  Consider decreasing individual threshold to {suggested['individual_minimal']:.6f}")
    else:
        print(f"   ✅ Current individual threshold appears reasonable")
    
    if suggested['sum_minimal'] > current_sum:
        print(f"   ⬆️  Consider increasing sum threshold to {suggested['sum_minimal']:.6f}")
    elif suggested['sum_minimal'] < current_sum:
        print(f"   ⬇️  Consider decreasing sum threshold to {suggested['sum_minimal']:.6f}")
    else:
        print(f"   ✅ Current sum threshold appears reasonable")
    
    print()
    
    # Model performance comparison
    print("🏆 Model Performance Comparison:")
    print("=" * 50)
    
    performance = logger.get_model_performance_comparison()
    
    if performance["model_performance"]:
        for model_data in performance["model_performance"]:
            print(f"🤖 {model_data['model']} ({model_data['framework']}):")
            print(f"   Success Rate: {model_data['success_rate']:.1%}")
            print(f"   Avg Cost: ${model_data['avg_cost']:.4f}")
            print(f"   Avg Variance: {model_data['avg_variance']:.6f}")
            print(f"   Jobs: {model_data['job_count']}")
            print()
    else:
        print("❌ No performance data available yet")
    
    # Save analysis
    output_file = "logs/variance_threshold_analysis.json"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump({
            "analysis": analysis,
            "performance": performance,
            "current_thresholds": {
                "individual": current_individual,
                "sum": current_sum
            },
            "timestamp": str(datetime.now())
        }, f, indent=2)
    
    print(f"📁 Analysis saved to: {output_file}")

if __name__ == "__main__":
    main() 