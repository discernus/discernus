#!/usr/bin/env python3
"""
Multi-Run Analysis Test: Obama Inaugural Speech with Claude
Tests consistency and variation in civic virtue analysis across 5 consecutive runs
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.api_clients.direct_api_client import DirectAPIClient

def load_obama_inaugural():
    """Load Obama's first inaugural address from golden set"""
    file_path = "corpus/golden_set/presidential_speeches/txt/golden_obama_inaugural_01.txt"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"✅ Obama inaugural text loaded ({len(content):,} characters)")
        return content
    except FileNotFoundError:
        print(f"❌ Could not find Obama inaugural text at: {file_path}")
        return None
    except Exception as e:
        print(f"❌ Error loading text: {e}")
        return None

def run_single_analysis(client: DirectAPIClient, text: str, run_number: int) -> Dict[str, Any]:
    """Run a single civic virtue analysis"""
    print(f"\n🔄 Run {run_number}/5 - Starting analysis...")
    start_time = time.time()
    
    try:
        # Use latest operational Claude model 
        result, cost = client.analyze_text(text, "civic_virtue", "claude-3.5-sonnet")
        duration = time.time() - start_time
        
        # Extract scores if available
        scores = result.get('scores', {})
        
        analysis_data = {
            "run_number": run_number,
            "success": True,
            "model": "claude-3.5-sonnet",
            "framework": "civic_virtue",
            "result": result,
            "scores": scores,
            "cost": cost,
            "duration": duration,
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"✅ Run {run_number} completed - Duration: {duration:.1f}s, Cost: ${cost:.4f}")
        
        # Show key metrics for this run
        if scores:
            print(f"   📊 Score summary:")
            integrative_wells = ['Dignity', 'Truth', 'Hope', 'Justice', 'Pragmatism']
            disintegrative_wells = ['Tribalism', 'Manipulation', 'Fantasy', 'Resentment', 'Fear']
            
            integrative_avg = sum(scores.get(well, 0) for well in integrative_wells) / len(integrative_wells)
            disintegrative_avg = sum(scores.get(well, 0) for well in disintegrative_wells) / len(disintegrative_wells)
            
            print(f"   ✨ Integrative avg: {integrative_avg:.3f}")
            print(f"   ⚠️ Disintegrative avg: {disintegrative_avg:.3f}")
            print(f"   📈 Net civic virtue: {integrative_avg - disintegrative_avg:.3f}")
        
        return analysis_data
        
    except Exception as e:
        print(f"❌ Run {run_number} failed: {e}")
        return {
            "run_number": run_number,
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

def analyze_consistency(runs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze consistency and variation across runs"""
    successful_runs = [run for run in runs if run.get('success', False)]
    
    if len(successful_runs) < 2:
        return {"error": "Insufficient successful runs for consistency analysis"}
    
    # Extract scores from each run
    all_scores = []
    for run in successful_runs:
        scores = run.get('scores', {})
        if scores:
            all_scores.append(scores)
    
    if not all_scores:
        return {"error": "No scores found in successful runs"}
    
    # Calculate statistics for each well
    wells = set()
    for scores in all_scores:
        wells.update(scores.keys())
    
    consistency_stats = {}
    
    for well in wells:
        well_scores = [scores.get(well, 0) for scores in all_scores]
        if well_scores:
            consistency_stats[well] = {
                "mean": sum(well_scores) / len(well_scores),
                "min": min(well_scores),
                "max": max(well_scores),
                "range": max(well_scores) - min(well_scores),
                "values": well_scores
            }
    
    # Overall statistics
    total_cost = sum(run.get('cost', 0) for run in successful_runs)
    avg_duration = sum(run.get('duration', 0) for run in successful_runs) / len(successful_runs)
    
    return {
        "successful_runs": len(successful_runs),
        "total_runs": len(runs),
        "success_rate": len(successful_runs) / len(runs),
        "total_cost": total_cost,
        "avg_duration": avg_duration,
        "well_statistics": consistency_stats,
        "runs": successful_runs
    }

def save_results(results: Dict[str, Any], filename: str = None):
    """Save results to JSON file"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"obama_multi_run_civic_virtue_{timestamp}.json"
    
    output_dir = Path("test_results")
    output_dir.mkdir(exist_ok=True)
    
    filepath = output_dir / filename
    
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"💾 Results saved to: {filepath}")
    return filepath

def print_summary(consistency_analysis: Dict[str, Any]):
    """Print a summary of the multi-run analysis"""
    print("\n" + "="*60)
    print("📊 MULTI-RUN ANALYSIS SUMMARY")
    print("="*60)
    
    print(f"🎯 Successful runs: {consistency_analysis['successful_runs']}/{consistency_analysis['total_runs']}")
    print(f"💰 Total cost: ${consistency_analysis['total_cost']:.4f}")
    print(f"⏱️ Average duration: {consistency_analysis['avg_duration']:.1f}s")
    print(f"✅ Success rate: {consistency_analysis['success_rate']:.1%}")
    
    if 'well_statistics' in consistency_analysis:
        print(f"\n🏛️ CIVIC VIRTUE WELLS - CONSISTENCY ANALYSIS")
        print("-"*50)
        
        wells_stats = consistency_analysis['well_statistics']
        
        # Group by type
        integrative_wells = ['Dignity', 'Truth', 'Hope', 'Justice', 'Pragmatism']
        disintegrative_wells = ['Tribalism', 'Manipulation', 'Fantasy', 'Resentment', 'Fear']
        
        print(f"\n✨ INTEGRATIVE WELLS:")
        for well in integrative_wells:
            if well in wells_stats:
                stats = wells_stats[well]
                print(f"  {well:12}: {stats['mean']:.3f} (±{stats['range']:.3f}) [{stats['min']:.3f}-{stats['max']:.3f}]")
        
        print(f"\n⚠️ DISINTEGRATIVE WELLS:")
        for well in disintegrative_wells:
            if well in wells_stats:
                stats = wells_stats[well]
                print(f"  {well:12}: {stats['mean']:.3f} (±{stats['range']:.3f}) [{stats['min']:.3f}-{stats['max']:.3f}]")
        
        # Calculate overall civic virtue trend
        integrative_means = [wells_stats[well]['mean'] for well in integrative_wells if well in wells_stats]
        disintegrative_means = [wells_stats[well]['mean'] for well in disintegrative_wells if well in wells_stats]
        
        if integrative_means and disintegrative_means:
            net_civic_virtue = sum(integrative_means)/len(integrative_means) - sum(disintegrative_means)/len(disintegrative_means)
            print(f"\n📈 Net Civic Virtue Score: {net_civic_virtue:.3f}")
            
            if net_civic_virtue > 0.2:
                print("🟢 Strong civic virtue orientation")
            elif net_civic_virtue > 0:
                print("🟡 Moderate civic virtue orientation") 
            else:
                print("🔴 Low civic virtue orientation")

def main():
    """Main function to run the multi-run analysis"""
    print("🧪 Multi-Run Analysis: Obama Inaugural Speech")
    print("=" * 50)
    print("🤖 Model: Claude 3.5 Sonnet")
    print("📊 Framework: Civic Virtue")
    print("🔄 Runs: 5 consecutive analyses")
    print("📄 Text: Obama's First Inaugural Address (2009)")
    print()
    
    # Initialize client
    try:
        client = DirectAPIClient()
        print("✅ DirectAPIClient initialized")
    except Exception as e:
        print(f"❌ Failed to initialize API client: {e}")
        return
    
    # Load Obama's inaugural text
    text = load_obama_inaugural()
    if not text:
        return
    
    print(f"📝 Text preview: {text[:200]}...")
    print()
    
    # Run 5 consecutive analyses
    print("🚀 Starting 5 consecutive runs...")
    all_runs = []
    
    for run_num in range(1, 6):
        run_result = run_single_analysis(client, text, run_num)
        all_runs.append(run_result)
        
        # Brief pause between runs to avoid overwhelming the API
        if run_num < 5:
            time.sleep(2)
    
    # Analyze consistency across runs
    print(f"\n🔍 Analyzing consistency across runs...")
    consistency_analysis = analyze_consistency(all_runs)
    
    # Prepare final results
    final_results = {
        "test_metadata": {
            "test_type": "multi_run_consistency",
            "model": "claude-3.5-sonnet",
            "framework": "civic_virtue", 
            "text_source": "Obama First Inaugural 2009",
            "total_runs": 5,
            "timestamp": datetime.now().isoformat()
        },
        "individual_runs": all_runs,
        "consistency_analysis": consistency_analysis
    }
    
    # Save results
    filepath = save_results(final_results)
    
    # Print summary
    print_summary(consistency_analysis)
    
    print(f"\n📄 Detailed results saved to: {filepath}")
    print(f"\n🎉 Multi-run analysis completed successfully!")

if __name__ == "__main__":
    main() 