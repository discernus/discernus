#!/usr/bin/env python3

import sys
sys.path.append('.')

from narrative_gravity_elliptical import NarrativeGravityWellsElliptical, load_analysis_data
import json

def test_comparative_with_existing_data():
    """Test comparative visualization with existing analysis data."""
    print("🧪 Testing comparative visualization with existing data...")
    
    # Use the existing JSON file (we only have one, so we'll duplicate it for testing)
    json_file = "model_output/2025_06_04_210021_anthropic_claude_4.0_sonnet_second_inaugural_address_of_donald_j_trump.json"
    
    try:
        # Load the existing analysis
        data1 = load_analysis_data(json_file)
        print(f"✅ Loaded first analysis: {data1['metadata']['title']}")
        
        # Create a slightly modified version for comparison testing
        data2 = json.loads(json.dumps(data1))  # Deep copy
        data2['metadata']['title'] = "Modified Test Analysis (for comparison)"
        data2['metadata']['model_name'] = "Test Model"
        
        # Modify some scores to show a difference
        if 'wells' in data2:
            for well in data2['wells']:
                if well['name'] == 'Dignity':
                    well['score'] = max(0.1, well['score'] + 0.3)  # Increase Dignity
                elif well['name'] == 'Tribalism':
                    well['score'] = max(0.1, well['score'] - 0.2)  # Decrease Tribalism
        
        print(f"✅ Created modified second analysis for comparison")
        
        # Test comparative visualization
        visualizer = NarrativeGravityWellsElliptical()
        output_path = visualizer.create_comparative_visualization([data1, data2])
        
        print(f"🖼️  Comparative visualization: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error in comparative visualization test: {e}")
        return False

def main():
    success = test_comparative_with_existing_data()
    
    if success:
        print(f"\n🎉 Comparative visualization test successful!")
        print(f"📝 No API calls were made - used existing data")
        print(f"🔍 Ready to test with real LLM comparative analysis")
    else:
        print(f"\n❌ Comparative visualization test failed")
        print(f"⚠️  Need to fix issues before running LLM comparisons")

if __name__ == "__main__":
    main() 