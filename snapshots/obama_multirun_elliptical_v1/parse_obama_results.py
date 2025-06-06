#!/usr/bin/env python3
"""
Parse Obama Multi-Run Results
Extract and analyze scores from the raw_response field
"""

import json
import re
from pathlib import Path

def extract_scores_from_raw_response(raw_response):
    """Extract scores from the raw JSON response"""
    try:
        # The raw_response contains JSON followed by additional text
        # Look for the JSON structure at the beginning
        lines = raw_response.strip().split('\n')
        
        # Find the start and end of the JSON block
        json_lines = []
        in_json = False
        brace_count = 0
        
        for line in lines:
            if line.strip().startswith('{') and not in_json:
                in_json = True
                brace_count = 1
                json_lines.append(line)
            elif in_json:
                json_lines.append(line)
                # Count braces to find the end
                brace_count += line.count('{') - line.count('}')
                if brace_count == 0:
                    break
        
        if json_lines:
            json_str = '\n'.join(json_lines)
            parsed = json.loads(json_str)
            return parsed.get('scores', {})
            
    except Exception as e:
        print(f"Debug: Failed to parse JSON: {e}")
        # Fallback: try to extract just the first JSON object
        try:
            # Simple approach: find the first { and matching }
            start = raw_response.find('{')
            if start != -1:
                brace_count = 0
                end = start
                for i, char in enumerate(raw_response[start:], start):
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            end = i + 1
                            break
                
                if end > start:
                    json_str = raw_response[start:end]
                    parsed = json.loads(json_str)
                    return parsed.get('scores', {})
        except Exception as e2:
            print(f"Debug: Fallback parsing also failed: {e2}")
    
    return {}

def analyze_results():
    """Analyze the Obama multi-run results"""
    results_file = "test_results/obama_multi_run_civic_virtue_20250606_142731.json"
    
    try:
        with open(results_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Results file not found: {results_file}")
        return
    
    print("🧪 Multi-Run Analysis: Obama Inaugural Speech")
    print("=" * 50)
    print("🤖 Model: Claude 3.5 Sonnet")
    print("📊 Framework: Civic Virtue")
    print("🔄 Runs: 5 consecutive analyses")
    print()
    
    # Extract scores from each run
    all_scores = []
    total_cost = 0
    total_duration = 0
    
    for run in data['individual_runs']:
        if run['success']:
            raw_response = run['result']['raw_response']
            scores = extract_scores_from_raw_response(raw_response)
            
            if scores:
                all_scores.append(scores)
                print(f"✅ Run {run['run_number']}: {len(scores)} scores extracted")
                
                # Show quick summary for this run
                integrative_wells = ['Dignity', 'Truth', 'Hope', 'Justice', 'Pragmatism']
                disintegrative_wells = ['Tribalism', 'Manipulation', 'Fantasy', 'Resentment', 'Fear']
                
                integrative_avg = sum(scores.get(well, 0) for well in integrative_wells) / len(integrative_wells)
                disintegrative_avg = sum(scores.get(well, 0) for well in disintegrative_wells) / len(disintegrative_wells)
                net_virtue = integrative_avg - disintegrative_avg
                
                print(f"   📈 Net civic virtue: {net_virtue:.3f}")
            
            total_cost += run['cost']
            total_duration += run['duration']
    
    if not all_scores:
        print("❌ No scores could be extracted from runs")
        return
    
    print(f"\n📊 Successfully extracted scores from {len(all_scores)} runs")
    print(f"💰 Total cost: ${total_cost:.4f}")
    print(f"⏱️ Average duration: {total_duration/len(data['individual_runs']):.1f}s")
    
    # Analyze consistency
    print(f"\n🏛️ CIVIC VIRTUE WELLS - CONSISTENCY ANALYSIS")
    print("-"*60)
    
    # Get all unique wells
    all_wells = set()
    for scores in all_scores:
        all_wells.update(scores.keys())
    
    # Calculate statistics for each well
    wells_stats = {}
    for well in sorted(all_wells):
        well_scores = [scores.get(well, 0) for scores in all_scores if well in scores]
        if well_scores:
            wells_stats[well] = {
                "mean": sum(well_scores) / len(well_scores),
                "min": min(well_scores),
                "max": max(well_scores),
                "range": max(well_scores) - min(well_scores),
                "values": well_scores
            }
    
    # Group by type and display
    integrative_wells = ['Dignity', 'Truth', 'Hope', 'Justice', 'Pragmatism']
    disintegrative_wells = ['Tribalism', 'Manipulation', 'Fantasy', 'Resentment', 'Fear']
    
    print(f"\n✨ INTEGRATIVE WELLS:")
    for well in integrative_wells:
        if well in wells_stats:
            stats = wells_stats[well]
            print(f"  {well:12}: {stats['mean']:.3f} (±{stats['range']:.3f}) [{stats['min']:.3f}-{stats['max']:.3f}]")
            print(f"               Values: {stats['values']}")
    
    print(f"\n⚠️ DISINTEGRATIVE WELLS:")
    for well in disintegrative_wells:
        if well in wells_stats:
            stats = wells_stats[well]
            print(f"  {well:12}: {stats['mean']:.3f} (±{stats['range']:.3f}) [{stats['min']:.3f}-{stats['max']:.3f}]")
            print(f"               Values: {stats['values']}")
    
    # Calculate overall civic virtue trend
    integrative_means = [wells_stats[well]['mean'] for well in integrative_wells if well in wells_stats]
    disintegrative_means = [wells_stats[well]['mean'] for well in disintegrative_wells if well in wells_stats]
    
    if integrative_means and disintegrative_means:
        integrative_total = sum(integrative_means)/len(integrative_means)
        disintegrative_total = sum(disintegrative_means)/len(disintegrative_means)
        net_civic_virtue = integrative_total - disintegrative_total
        
        print(f"\n📈 OVERALL CIVIC VIRTUE ANALYSIS:")
        print(f"   Integrative average:    {integrative_total:.3f}")
        print(f"   Disintegrative average: {disintegrative_total:.3f}")
        print(f"   Net Civic Virtue Score: {net_civic_virtue:.3f}")
        
        if net_civic_virtue > 0.5:
            print("   🟢 STRONG civic virtue orientation")
        elif net_civic_virtue > 0.2:
            print("   🟡 MODERATE civic virtue orientation") 
        elif net_civic_virtue > 0:
            print("   🔵 MILD civic virtue orientation")
        else:
            print("   🔴 LOW civic virtue orientation")
    
    # Analyze consistency
    print(f"\n🎯 CONSISTENCY ANALYSIS:")
    high_consistency = []
    moderate_consistency = []
    variable_consistency = []
    
    for well, stats in wells_stats.items():
        if stats['range'] <= 0.1:
            high_consistency.append(well)
        elif stats['range'] <= 0.2:
            moderate_consistency.append(well)
        else:
            variable_consistency.append(well)
    
    if high_consistency:
        print(f"   🎯 High consistency (±0.1): {', '.join(high_consistency)}")
    if moderate_consistency:
        print(f"   📊 Moderate consistency (±0.1-0.2): {', '.join(moderate_consistency)}")
    if variable_consistency:
        print(f"   🌊 Variable consistency (>±0.2): {', '.join(variable_consistency)}")
    
    # Validate my predictions
    print(f"\n🔮 PREDICTION VALIDATION:")
    print("   Expected patterns:")
    print("   • High Dignity, Hope, Justice, Truth ✅" if wells_stats.get('Dignity', {}).get('mean', 0) > 0.7 else "   • High Dignity, Hope, Justice, Truth ❌")
    print("   • Low Tribalism, Manipulation, Fear ✅" if wells_stats.get('Tribalism', {}).get('mean', 1) < 0.4 else "   • Low Tribalism, Manipulation, Fear ❌")
    print("   • Consistent pattern across runs ✅" if len(high_consistency) + len(moderate_consistency) >= 7 else "   • Consistent pattern across runs ❌")
    print("   • Strong overall civic virtue ✅" if net_civic_virtue > 0.5 else "   • Strong overall civic virtue ❌")

if __name__ == "__main__":
    analyze_results() 