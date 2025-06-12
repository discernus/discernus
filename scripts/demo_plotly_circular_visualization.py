#!/usr/bin/env python3
"""
Demo Plotly Circular Visualization
=================================

This script demonstrates the Plotly-based circular visualization system
using the actual Civic Virtue framework configuration from the frameworks directory.
This validates that the visualization pipeline is working correctly with real framework data.

The visualization is saved as an HTML file in analysis_results/plotly_demo/.
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Ensure src is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from narrative_gravity.visualization.plotly_circular import PlotlyCircularVisualizer
from framework_loader import load_framework_config, extract_wells_config, print_framework_summary

# --- CONFIG ---
OUTPUT_DIR = 'analysis_results/plotly_demo/'
FRAMEWORK_NAME = 'civic_virtue'


def create_sample_data():
    """Create sample civic virtue analysis data using the actual framework configuration."""
    
    # Load actual Civic Virtue framework configuration
    print("📋 Loading Civic Virtue framework configuration...")
    framework_config = load_framework_config(FRAMEWORK_NAME)
    print_framework_summary(framework_config)
    
    # Extract wells configuration
    wells_config = extract_wells_config(framework_config)
    print(f"\n✅ Loaded {len(wells_config)} wells from framework configuration")
    
    # Sample analysis scenarios using actual well names from framework
    scenarios = {
        'hopeful_speech': {
            'title': 'Hopeful Presidential Address (Demo)',
            'scores': {
                'Dignity': 0.9,
                'Truth': 0.7,
                'Justice': 0.8,
                'Hope': 0.8,
                'Pragmatism': 0.6,
                'Tribalism': 0.1,
                'Manipulation': 0.2,
                'Resentment': 0.1,
                'Fantasy': 0.2,
                'Fear': 0.1
            }
        },
        'divisive_rhetoric': {
            'title': 'Divisive Political Rhetoric (Demo)',
            'scores': {
                'Dignity': 0.1,
                'Truth': 0.2,
                'Justice': 0.2,
                'Hope': 0.2,
                'Pragmatism': 0.3,
                'Tribalism': 0.9,
                'Manipulation': 0.8,
                'Resentment': 0.7,
                'Fantasy': 0.6,
                'Fear': 0.8
            }
        },
        'balanced_analysis': {
            'title': 'Balanced Policy Discussion (Demo)',
            'scores': {
                'Dignity': 0.7,
                'Truth': 0.8,
                'Justice': 0.7,
                'Hope': 0.6,
                'Pragmatism': 0.9,
                'Tribalism': 0.2,
                'Manipulation': 0.1,
                'Resentment': 0.2,
                'Fantasy': 0.1,
                'Fear': 0.2
            }
        }
    }
    
    return wells_config, scenarios


def main():
    """Run the Plotly circular visualization demonstration."""
    print("🎨 Plotly Circular Visualization Demo (Real Framework Config)")
    print("=" * 60)
    
    # Create output directory
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"📁 Output directory: {output_dir}")
    
    # Get sample data using real framework config
    wells_config, scenarios = create_sample_data()
    
    # Initialize visualizer
    visualizer = PlotlyCircularVisualizer()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Generate individual visualizations
    print("\n🖼️  Generating individual visualizations...")
    for scenario_name, scenario_data in scenarios.items():
        output_html = output_dir / f"demo_{scenario_name}_{timestamp}.html"
        
        fig = visualizer.plot(
            wells=wells_config,
            narrative_scores=scenario_data['scores'],
            narrative_label=scenario_data['title'],
            title=f"Civic Virtue Demo: {scenario_data['title']}",
            output_html=str(output_html),
            show=False
        )
        
        print(f"  ✅ {scenario_name}: {output_html}")
    
    # Generate comparison visualization
    print("\n🔄 Generating comparison visualization...")
    analyses = []
    for scenario_name, scenario_data in scenarios.items():
        analyses.append({
            'title': scenario_data['title'],
            'wells': wells_config,
            'scores': scenario_data['scores']
        })
    
    comparison_html = output_dir / f"demo_comparison_{timestamp}.html"
    comparison_fig = visualizer.create_comparison(
        analyses=analyses,
        title="Civic Virtue Framework Comparison (Demo)",
        output_html=str(comparison_html)
    )
    print(f"  ✅ Comparison: {comparison_html}")
    
    print("\n🎉 Demo completed successfully!")
    print(f"\n📋 Generated files:")
    for file in output_dir.glob(f"*{timestamp}*"):
        print(f"  • {file}")
    
    print(f"\n💡 Open any HTML file in your browser to view the interactive visualizations")
    print(f"🎯 This demonstrates the Plotly circular visualization pipeline with REAL framework configuration!")


if __name__ == '__main__':
    main() 