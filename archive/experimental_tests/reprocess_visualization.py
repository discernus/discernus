#!/usr/bin/env python3

import sys
sys.path.append('.')

from narrative_gravity_elliptical import NarrativeGravityWellsElliptical, load_analysis_data
import json

def reprocess_visualization(json_file):
    """Reprocess an existing analysis result to generate a new visualization."""
    print(f"🔄 Reprocessing visualization from: {json_file}")
    
    # Load existing analysis data
    try:
        data = load_analysis_data(json_file)
        print(f"✅ Loaded analysis data successfully")
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return False
    
    # Create visualizer and generate new visualization
    try:
        visualizer = NarrativeGravityWellsElliptical()
        output_path = visualizer.create_visualization(data)
        print(f"🖼️  New visualization: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Error creating visualization: {e}")
        return False

def main():
    # Use the existing JSON file
    json_file = "model_output/2025_06_04_210021_anthropic_claude_4.0_sonnet_second_inaugural_address_of_donald_j_trump.json"
    
    success = reprocess_visualization(json_file)
    
    if success:
        print(f"\n🎉 Visualization reprocessed successfully!")
        print(f"📝 No API calls were made - just layout adjustment")
    else:
        print(f"\n❌ Failed to reprocess visualization")

if __name__ == "__main__":
    main() 