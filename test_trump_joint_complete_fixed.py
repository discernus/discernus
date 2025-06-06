#!/usr/bin/env python3
"""
Complete Analysis Test: Trump Joint Address 
Full end-to-end test with scores, metrics, and visualization (FIXED VERSION)
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.api_clients.direct_api_client import DirectAPIClient
from narrative_gravity_elliptical import NarrativeGravityWellsElliptical

def load_trump_joint_text():
    """Load the Trump joint address txt file"""
    trump_file = Path("corpus/golden_set/presidential_speeches/txt/golden_trump_joint_01.txt")
    
    if not trump_file.exists():
        raise FileNotFoundError(f"Trump joint address file not found: {trump_file}")
    
    with open(trump_file, 'r', encoding='utf-8') as f:
        text = f.read().strip()
    
    print(f"📄 Loaded: {trump_file.name}")
    print(f"📏 Length: {len(text):,} characters")
    print(f"📝 Preview: {text[:200]}...")
    
    return text, trump_file.name

def run_complete_analysis():
    """Run complete civic virtue analysis with visualization"""
    
    print("🧪 Complete Analysis Test: Trump Joint Address (FIXED)")
    print("=" * 60)
    print("🤖 Model: GPT-4o")
    print("📊 Framework: Civic Virtue")
    print("📄 File: Trump Joint Address")
    print("🎯 Output: Scores + Metrics + Visualization + LLM Summary")
    print()
    
    # Initialize components
    try:
        client = DirectAPIClient()
        visualizer = NarrativeGravityWellsElliptical()
        print("✅ Components initialized")
    except Exception as e:
        print(f"❌ Failed to initialize components: {e}")
        return
    
    # Load text
    try:
        text, filename = load_trump_joint_text()
        print("✅ Text loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load text: {e}")
        return
    
    print()
    
    # Step 1: Run LLM analysis
    print("🔄 Step 1: Running civic virtue analysis...")
    start_time = time.time()
    
    try:
        result, cost = client.analyze_text(text, "civic_virtue", "gpt-4o")
        
        analysis_time = time.time() - start_time
        
        print(f"✅ LLM analysis completed in {analysis_time:.1f} seconds")
        print(f"💰 Cost: ${cost:.4f}")
        
        if 'scores' not in result:
            raise ValueError("No scores returned from analysis")
            
        scores = result['scores']
        print(f"✅ Received {len(scores)} civic virtue scores")
        
        # Extract the LLM's detailed analysis summary
        llm_analysis = result.get('analysis', '')
        if llm_analysis:
            print(f"✅ Received detailed LLM analysis ({len(llm_analysis)} characters)")
        else:
            print("⚠️ No detailed analysis summary received")
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return
    
    # Step 2: Calculate advanced metrics
    print("\n🔄 Step 2: Calculating advanced metrics...")
    
    try:
        # Calculate narrative position
        narrative_x, narrative_y = visualizer.calculate_narrative_position(scores)
        
        # Calculate enhanced metrics
        calculated_metrics = visualizer.calculate_elliptical_metrics(narrative_x, narrative_y, scores)
        
        print(f"✅ Calculated metrics:")
        print(f"   📍 Narrative Position: ({narrative_x:.3f}, {narrative_y:.3f})")
        print(f"   📈 Narrative Elevation: {calculated_metrics['narrative_elevation']:.3f}")
        print(f"   🎯 Narrative Polarity: {calculated_metrics['narrative_polarity']:.3f}")
        print(f"   🧭 Coherence: {calculated_metrics['coherence']:.3f}")
        print(f"   ⚖️ Directional Purity: {calculated_metrics['directional_purity']:.3f}")
        
    except Exception as e:
        print(f"❌ Metrics calculation failed: {e}")
        return
    
    # Step 3: Create complete data structure
    print("\n🔄 Step 3: Building complete data structure...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    complete_data = {
        'metadata': {
            'title': 'Donald J. Trump Address to Joint Session of Congress March 4, 2025',
            'filename': filename,
            'model_name': 'GPT-4o',
            'model_version': '4o',
            'framework_name': 'civic_virtue',
            'framework_version': 'v2025.06.04',
            'analysis_timestamp': datetime.now().isoformat(),
            'summary': llm_analysis  # Use the actual LLM analysis as summary for visualization
        },
        'scores': scores,
        'calculated_metrics': calculated_metrics,
        'analysis_details': {
            'character_count': len(text),
            'word_count': len(text.split()),
            'analysis_duration_seconds': analysis_time,
            'cost_usd': cost,
            'narrative_position': {
                'x': narrative_x,
                'y': narrative_y
            }
        },
        'raw_analysis': llm_analysis
    }
    
    print("✅ Complete data structure built")
    
    # Step 4: Generate visualization
    print("\n🔄 Step 4: Generating visualization...")
    
    try:
        # Create the visualization data in the expected format
        visualization_data = {
            'metadata': complete_data['metadata'],
            'wells': [
                {
                    'name': well_name,
                    'score': score,
                    'angle': visualizer.well_definitions[well_name]['angle']
                }
                for well_name, score in scores.items()
                if well_name in visualizer.well_definitions
            ]
        }
        
        # Generate visualization with LLM summary
        viz_path = visualizer.create_visualization(visualization_data)
        
        print(f"✅ Visualization created: {viz_path}")
        print(f"✅ LLM summary included in visualization")
        
    except Exception as e:
        print(f"❌ Visualization generation failed: {e}")
        viz_path = None
    
    # Step 5: Save complete results
    print("\n🔄 Step 5: Saving results...")
    
    try:
        # Save JSON results
        json_filename = f"trump_joint_complete_analysis_fixed_{timestamp}.json"
        
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(complete_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Complete analysis saved: {json_filename}")
        
    except Exception as e:
        print(f"❌ Failed to save results: {e}")
    
    # Step 6: Display results summary
    print("\n" + "=" * 60)
    print("📊 COMPLETE ANALYSIS RESULTS")
    print("=" * 60)
    
    # LLM Summary
    if llm_analysis:
        print(f"\n📝 LLM ANALYSIS SUMMARY:")
        print(f"   {llm_analysis[:300]}..." if len(llm_analysis) > 300 else f"   {llm_analysis}")
    
    # Scores breakdown
    print("\n🏛️ CIVIC VIRTUE SCORES:")
    
    positive_wells = ['Dignity', 'Truth', 'Hope', 'Justice', 'Pragmatism']
    negative_wells = ['Tribalism', 'Manipulation', 'Fantasy', 'Resentment', 'Fear']
    
    print("\n✨ Positive Wells (Integrative):")
    positive_total = 0
    for well in positive_wells:
        if well in scores:
            score = scores[well]
            positive_total += score
            print(f"   {well:12}: {score:.2f}")
    
    print("\n⚠️ Negative Wells (Disintegrative):")
    negative_total = 0
    for well in negative_wells:
        if well in scores:
            score = scores[well]
            negative_total += score
            print(f"   {well:12}: {score:.2f}")
    
    overall_score = positive_total - negative_total
    print(f"\n📈 AGGREGATE SCORES:")
    print(f"   Positive Total:  {positive_total:.2f}")
    print(f"   Negative Total:  {negative_total:.2f}")
    print(f"   Overall Score:   {overall_score:.2f}")
    
    # Advanced metrics
    print(f"\n🔬 ADVANCED METRICS:")
    print(f"   Narrative Elevation: {calculated_metrics['narrative_elevation']:.3f}")
    print(f"   Narrative Polarity:  {calculated_metrics['narrative_polarity']:.3f}")
    print(f"   Coherence:          {calculated_metrics['coherence']:.3f}")
    print(f"   Directional Purity: {calculated_metrics['directional_purity']:.3f}")
    
    # Technical details
    print(f"\n⚙️ TECHNICAL DETAILS:")
    print(f"   Text Length:        {len(text):,} characters")
    print(f"   Analysis Time:      {analysis_time:.1f} seconds")
    print(f"   Cost:              ${cost:.4f}")
    print(f"   JSON Output:       {json_filename}")
    if viz_path:
        print(f"   Visualization:     {viz_path}")
    
    print(f"\n🎉 Complete analysis with LLM summary finished successfully!")

if __name__ == "__main__":
    run_complete_analysis() 