#!/usr/bin/env python3
"""
Synthetic Narratives Analysis Job
Runs all synthetic narrative texts through Claude using the established analysis system,
then generates a multi-comparative visualization.
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# Add project root to path
sys.path.append('.')

from src.api_clients.direct_api_client import DirectAPIClient
from src.narrative_gravity.engine_circular import NarrativeGravityWellsCircular

def load_synthetic_narratives() -> Dict[str, str]:
    """Load all synthetic narrative texts"""
    narratives = {}
    base_path = Path("corpus/raw_sources/synthetic_narratives")
    
    # Define the files and their friendly names
    files = {
        "right_center_positive_stewardship.txt": "Right-Center Positive (Stewardship)",
        "left_center_negative_manifesto.txt": "Left-Center Negative (Manifesto)",
        "left_center_positive_renewal.txt": "Left-Center Positive (Renewal)",
        "right_center_negative_takeback.txt": "Right-Center Negative (Takeback)"
    }
    
    for filename, friendly_name in files.items():
        file_path = base_path / filename
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                narratives[friendly_name] = content
                print(f"✅ Loaded: {friendly_name}")
        except Exception as e:
            print(f"❌ Failed to load {filename}: {e}")
    
    return narratives

def run_single_analysis(client: DirectAPIClient, text: str, narrative_name: str) -> Dict[str, Any]:
    """Run a single civic virtue analysis on a narrative"""
    print(f"\n🔄 Analyzing: {narrative_name}")
    start_time = time.time()
    
    try:
        # Use civic virtue framework with Claude 3.5 Sonnet
        result, cost = client.analyze_text(text, "civic_virtue", "claude-3.5-sonnet")
        duration = time.time() - start_time
        
        # Extract scores if available
        scores = result.get('scores', {})
        
        analysis_data = {
            "narrative_name": narrative_name,
            "success": True,
            "model": "claude-3.5-sonnet",
            "framework": "civic_virtue",
            "result": result,
            "scores": scores,
            "cost": cost,
            "duration": duration,
            "timestamp": datetime.now().isoformat(),
            "text_preview": text[:200] + "..." if len(text) > 200 else text
        }
        
        print(f"✅ Analysis completed - Duration: {duration:.1f}s, Cost: ${cost:.4f}")
        
        # Show key metrics for this analysis
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
        print(f"❌ Analysis failed: {e}")
        return {
            "narrative_name": narrative_name,
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

def create_comparative_visualization(analysis_results: List[Dict[str, Any]]) -> str:
    """Create comparative visualization using the established system"""
    print("\n🎨 Creating comparative visualization...")
    
    # Filter successful analyses
    successful_analyses = [r for r in analysis_results if r.get('success', False) and r.get('scores')]
    
    if len(successful_analyses) < 2:
        print("❌ Need at least 2 successful analyses for comparison")
        return None
    
    # Format data for the established visualization system
    formatted_analyses = []
    
    for analysis in successful_analyses:
        # Create wells list from scores
        wells_list = []
        for well_name, score in analysis['scores'].items():
            wells_list.append({
                'name': well_name,
                'score': score
            })
        
        # Format for comparative visualization
        formatted_analysis = {
            'metadata': {
                'title': analysis['narrative_name'],
                'model_name': 'Claude 3.5 Sonnet',
                'model_version': 'claude-3.5-sonnet',
                'summary': f"Analysis of {analysis['narrative_name']} synthetic narrative",
                'timestamp': analysis['timestamp'],
                'framework': 'civic_virtue',
                'cost': analysis['cost'],
                'duration': analysis['duration']
            },
            'wells': wells_list
        }
        formatted_analyses.append(formatted_analysis)
    
    # Initialize the circular coordinate visualizer
    visualizer = NarrativeGravityWellsCircular()
    
    # Create comparative visualization
    output_path = visualizer.create_comparative_visualization(
        formatted_analyses, 
        output_path="synthetic_narratives_comparative_analysis.png"
    )
    
    print(f"✅ Comparative visualization created: {output_path}")
    return output_path

def save_analysis_results(analysis_results: List[Dict[str, Any]], output_path: str = "synthetic_narratives_analysis_results.json"):
    """Save all analysis results to JSON file"""
    
    # Calculate summary statistics
    successful_analyses = [r for r in analysis_results if r.get('success', False)]
    total_cost = sum(r.get('cost', 0) for r in successful_analyses)
    total_duration = sum(r.get('duration', 0) for r in successful_analyses)
    
    summary_data = {
        "job_metadata": {
            "job_name": "Synthetic Narratives Civic Virtue Analysis",
            "timestamp": datetime.now().isoformat(),
            "framework": "civic_virtue", 
            "model": "claude-3.5-sonnet",
            "total_narratives": len(analysis_results),
            "successful_analyses": len(successful_analyses),
            "total_cost": total_cost,
            "total_duration": total_duration,
            "success_rate": len(successful_analyses) / len(analysis_results) if analysis_results else 0
        },
        "individual_analyses": analysis_results
    }
    
    with open(output_path, 'w') as f:
        json.dump(summary_data, f, indent=2)
    
    print(f"📊 Analysis results saved: {output_path}")
    return output_path

def main():
    """Main execution function"""
    print("🧪 Synthetic Narratives Analysis Job")
    print("=" * 50)
    print("🤖 Model: Claude 3.5 Sonnet")
    print("📊 Framework: Civic Virtue")
    print("📄 Target: 4 Synthetic Narrative Texts")
    print()
    
    # Initialize client
    try:
        client = DirectAPIClient()
        print("✅ DirectAPIClient initialized")
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        return
    
    # Load synthetic narratives
    print("\n📚 Loading synthetic narratives...")
    narratives = load_synthetic_narratives()
    
    if not narratives:
        print("❌ No narratives loaded")
        return
    
    print(f"✅ Loaded {len(narratives)} narratives")
    
    # Run analyses
    print("\n🔄 Running analyses...")
    analysis_results = []
    
    for narrative_name, text in narratives.items():
        result = run_single_analysis(client, text, narrative_name)
        analysis_results.append(result)
        
        # Brief pause between analyses
        time.sleep(1)
    
    # Print summary
    successful_analyses = [r for r in analysis_results if r.get('success', False)]
    total_cost = sum(r.get('cost', 0) for r in successful_analyses)
    
    print(f"\n📊 Analysis Summary:")
    print(f"   ✅ Successful: {len(successful_analyses)}/{len(analysis_results)}")
    print(f"   💰 Total cost: ${total_cost:.4f}")
    print(f"   📊 Framework: Civic Virtue")
    
    # Save results
    results_file = save_analysis_results(analysis_results)
    
    # Create comparative visualization
    if len(successful_analyses) >= 2:
        viz_file = create_comparative_visualization(analysis_results)
        print(f"\n🖼️ Files generated:")
        print(f"   📊 Analysis data: {results_file}")
        print(f"   🎨 Visualization: {viz_file}")
    else:
        print("\n⚠️ Not enough successful analyses for comparative visualization")
    
    print("\n✅ Synthetic narratives analysis job complete!")

if __name__ == "__main__":
    main() 