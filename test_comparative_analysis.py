#!/usr/bin/env python3

import sys
sys.path.append('.')

from src.api_clients.direct_api_client import DirectAPIClient
from narrative_gravity_elliptical import NarrativeGravityWellsElliptical
import json
import time

def run_comparative_analysis():
    """Run a comparative analysis between two different presidential speeches."""
    print("🆚 Running Comparative Analysis: Trump vs Biden Inaugurals")
    
    start_time = time.time()
    
    # Initialize client and analyzer
    client = DirectAPIClient()
    visualizer = NarrativeGravityWellsElliptical()
    
    # Files to analyze for comparison
    files = [
        "corpus/golden_set/presidential_speeches/txt/golden_trump_inaugural_01.txt",
        "corpus/golden_set/presidential_speeches/txt/golden_biden_inaugural_01.txt"
    ]
    
    analyses = []
    
    try:
        for i, text_file in enumerate(files):
            print(f"\n📖 Analyzing file {i+1}/2: {text_file}")
            
            # Read the text
            with open(text_file, 'r', encoding='utf-8') as f:
                text_content = f.read()
            
            print(f"📊 Text length: {len(text_content):,} characters")
            
            # Run analysis with GPT-4o
            result, cost = client.analyze_text(
                text=text_content,
                framework='civic_virtue',
                model_name='gpt-4o'
            )
            
            # Add cost to result
            result['cost'] = cost
            
            # Ensure we have the required metadata
            if 'metadata' not in result:
                result['metadata'] = {}
            
            # Add required metadata fields based on file
            if 'trump' in text_file:
                result['metadata']['title'] = "Donald J. Trump Inaugural Address 2017 (analyzed by GPT-4o)"
                speaker = "Trump"
            else:
                result['metadata']['title'] = "Joseph R. Biden Inaugural Address 2021 (analyzed by GPT-4o)"
                speaker = "Biden"
            
            result['metadata']['model_name'] = "GPT-4o"  
            result['metadata']['model_version'] = "gpt-4o"
            
            # Add analysis summary to metadata if available
            if 'analysis' in result and 'summary' not in result['metadata']:
                result['metadata']['summary'] = result['analysis']
            
            # Debug: Check the structure before adding
            print(f"🔍 Result structure for {speaker}: {list(result.keys())}")
            if 'scores' in result:
                print(f"   Scores: {list(result['scores'].keys())}")
            
            analyses.append(result)
            
            print(f"✅ {speaker} analysis complete - Cost: ${cost:.4f}")
            
            # Show civic virtue scores
            print(f"📊 {speaker} Civic Virtue Scores:")
            if 'wells' in result:
                for well in result['wells']:
                    print(f"  {well['name']}: {well['score']:.2f}")
        
        # Create comparative visualization
        print(f"\n🎨 Creating comparative visualization...")
        output_path = visualizer.create_comparative_visualization(analyses)
        
        # Calculate total costs and time
        total_cost = sum(analysis.get('cost', 0) for analysis in analyses)
        total_time = time.time() - start_time
        
        print(f"\n✅ Comparative Analysis Complete!")
        print(f"💰 Total Cost: ${total_cost:.4f}")
        print(f"⏱️  Total Time: {total_time:.1f} seconds")
        print(f"🖼️  Visualization: {output_path}")
        
        # Show narrative positions for comparison (using scores directly)
        print(f"\n📍 Narrative Positions:")
        for i, analysis in enumerate(analyses):
            speaker = "Trump" if i == 0 else "Biden"
            if 'scores' in analysis:
                well_scores = analysis['scores']
                x, y = visualizer.calculate_narrative_position(well_scores)
                metrics = visualizer.calculate_elliptical_metrics(x, y, well_scores)
                print(f"  {speaker}: ({x:.3f}, {y:.3f}) - Elevation: {metrics['narrative_elevation']:.3f}")
        
        # Calculate distance between positions (using scores directly)
        if len(analyses) == 2:
            well_scores_1 = analyses[0]['scores'] if 'scores' in analyses[0] else {}
            well_scores_2 = analyses[1]['scores'] if 'scores' in analyses[1] else {}
            
            if well_scores_1 and well_scores_2:
                pos1 = visualizer.calculate_narrative_position(well_scores_1)
                pos2 = visualizer.calculate_narrative_position(well_scores_2)
                
                distance = visualizer.calculate_elliptical_distance(pos1, pos2)
                print(f"🔍 Elliptical Distance: {distance:.3f}")
        
        print(f"\n🎉 Comparative analysis completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

def main():
    success = run_comparative_analysis()
    
    if not success:
        print(f"\n❌ Comparative analysis failed")

if __name__ == "__main__":
    main() 