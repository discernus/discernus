#!/usr/bin/env python3

import sys
sys.path.append('.')

from src.api_clients.direct_api_client import DirectAPIClient
from narrative_gravity_elliptical import NarrativeGravityWellsElliptical
import json
import time

def main():
    print("🚀 Testing GPT-4o Trump Joint Address Analysis - Summary Position Fix...")
    
    start_time = time.time()
    
    # Initialize client and analyzer
    client = DirectAPIClient()
    visualizer = NarrativeGravityWellsElliptical()
    
    # File to analyze
    text_file = "corpus/golden_set/presidential_speeches/txt/golden_trump_joint_01.txt"
    
    try:
        # Read the text
        with open(text_file, 'r', encoding='utf-8') as f:
            text_content = f.read()
        
        print(f"📖 Analyzing: {text_file}")
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
        
        # Add required metadata fields
        result['metadata']['title'] = "Donald J. Trump Address to Joint Session of Congress March 4, 2025 (analyzed by GPT-4o)"
        result['metadata']['model_name'] = "GPT-4o"  
        result['metadata']['model_version'] = "gpt-4o"
        
        # Add analysis summary to metadata
        if 'analysis' in result and 'summary' not in result['metadata']:
            result['metadata']['summary'] = result['analysis']
        
        # Create complete visualization with metrics
        output_path = visualizer.create_visualization(result)
        
        # Display key results  
        print(f"\n✅ Analysis Complete!")
        print(f"🎯 Overall Score: {result.get('overall_score', 'N/A')}")
        print(f"💰 Cost: ${result.get('cost', 0):.4f}")
        print(f"⏱️  Time: {time.time() - start_time:.1f} seconds")
        print(f"🖼️  Visualization: {output_path}")
        
        # Show civic virtue scores
        print(f"\n📊 Civic Virtue Scores:")
        if 'wells' in result:
            for well in result['wells']:
                print(f"  {well['name']}: {well['score']:.2f}")
        
        # Show calculated metrics
        if 'metadata' in result and 'calculated_metrics' in result['metadata']:
            metrics = result['metadata']['calculated_metrics']
            print(f"\n🧮 Calculated Metrics:")
            print(f"  Narrative Elevation: {metrics.get('narrative_elevation', 'N/A'):.3f}")
            print(f"  Narrative Polarity: {metrics.get('narrative_polarity', 'N/A'):.3f}")
            print(f"  Coherence: {metrics.get('coherence', 'N/A'):.3f}")
            print(f"  Directional Purity: {metrics.get('directional_purity', 'N/A'):.3f}")
        
        # Show summary length
        summary = result.get('metadata', {}).get('summary', '')
        if summary:
            print(f"\n📝 Summary: {len(summary)} characters")
            print(f"   Preview: {summary[:100]}...")
        
        print(f"\n🎉 Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main() 