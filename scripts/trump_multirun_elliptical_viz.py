#!/usr/bin/env python3
"""
Trump Multi-Run Analysis - Elliptical Visualization

Uses the established NarrativeGravityWellsElliptical system to generate 
a proper elliptical visualization of the Trump analysis results.
"""

import numpy as np
from src.narrative_gravity.engine import NarrativeGravityWellsElliptical
from datetime import datetime
import json

def create_trump_elliptical_visualization():
    """Create elliptical visualization using the established system."""
    
    print("🔄 Processing Trump multi-run data...")
    
    # Raw scores from the 5 Trump analysis runs (from PostgreSQL)
    trump_scores = [
        {"Fear": 0.7, "Hope": 0.5, "Truth": 0.3, "Dignity": 0.2, "Fantasy": 0.8, "Justice": 0.4, "Tribalism": 0.8, "Pragmatism": 0.3, "Resentment": 0.6, "Manipulation": 0.7},
        {"Fear": 0.7, "Hope": 0.5, "Truth": 0.3, "Dignity": 0.2, "Fantasy": 0.8, "Justice": 0.4, "Tribalism": 0.8, "Pragmatism": 0.3, "Resentment": 0.6, "Manipulation": 0.7},
        {"Fear": 0.7, "Hope": 0.5, "Truth": 0.3, "Dignity": 0.2, "Fantasy": 0.8, "Justice": 0.4, "Tribalism": 0.8, "Pragmatism": 0.3, "Resentment": 0.6, "Manipulation": 0.7},
        {"Fear": 0.7, "Hope": 0.5, "Truth": 0.3, "Dignity": 0.2, "Fantasy": 0.8, "Justice": 0.4, "Tribalism": 0.8, "Pragmatism": 0.3, "Resentment": 0.6, "Manipulation": 0.7},
        {"Fear": 0.8, "Hope": 0.6, "Truth": 0.3, "Dignity": 0.2, "Fantasy": 0.8, "Justice": 0.3, "Tribalism": 0.8, "Pragmatism": 0.2, "Resentment": 0.7, "Manipulation": 0.7}
    ]
    
    # Calculate average scores
    well_names = ["Dignity", "Truth", "Justice", "Hope", "Pragmatism", "Tribalism", "Manipulation", "Resentment", "Fantasy", "Fear"]
    average_scores = {}
    
    for well in well_names:
        scores = [run[well] for run in trump_scores]
        average_scores[well] = np.mean(scores)
    
    print("Multi-Run Average Scores:")
    for well, score in average_scores.items():
        print(f"  {well}: {score:.3f}")
    
    # Create the properly formatted data structure for the established system
    wells_list = []
    for well_name, score in average_scores.items():
        wells_list.append({
            'name': well_name,
            'score': score
        })
    
    # Create the analysis data structure expected by the visualization system
    analysis_data = {
        'metadata': {
            'title': 'Trump Joint Session Address - Multi-Run Average (5 runs)',
            'model_name': 'Claude 3.5 Sonnet',
            'model_version': 'claude-3.5-sonnet',
            'summary': 'Multi-run analysis of Trump Joint Session Address using Civic Virtue framework',
            'timestamp': datetime.now().isoformat(),
            'job_id': 'trump_trump_gpt4o_gpt_4o_20250606_221319',
            'framework': 'civic_virtue',
            'run_count': 5
        },
        'wells': wells_list
    }
    
    print("🎨 Creating elliptical visualization...")
    
    # Initialize the established elliptical visualizer
    visualizer = NarrativeGravityWellsElliptical()
    
    # Create the visualization using the established system
    output_path = visualizer.create_visualization(analysis_data, 
                                                 output_path="trump_joint_session_multirun_civic_virtue.png")
    
    print(f"✅ Visualization created: {output_path}")
    
    # Also save the processed data for reference
    with open("trump_multirun_average_data.json", "w") as f:
        json.dump({
            "job_id": "trump_trump_gpt4o_gpt_4o_20250606_221319",
            "speaker": "Donald Trump",
            "speech_type": "Joint Session Address", 
            "framework": "civic_virtue",
            "model": "claude-3.5-sonnet",
            "total_runs": 5,
            "raw_scores": trump_scores,
            "average_scores": average_scores,
            "analysis_data": analysis_data
        }, f, indent=2)
    
    print("📊 Analysis data saved: trump_multirun_average_data.json")
    
    return output_path

if __name__ == "__main__":
    output_path = create_trump_elliptical_visualization()
    print(f"\n🖼️  Trump elliptical visualization complete: {output_path}") 