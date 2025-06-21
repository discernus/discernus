#!/usr/bin/env python3
"""
Demo script for the Historical Ideological Triangle Framework
Demonstrates analysis of 20th century political texts using independent wells approach
"""

import json
import os
import sys
from pathlib import Path

def load_framework():
    """Load the Historical Ideological Triangle framework configuration"""
    framework_path = Path("frameworks/historical_ideological_triangle/framework.json")
    
    if not framework_path.exists():
        print(f"❌ Framework file not found: {framework_path}")
        return None
        
    try:
        with open(framework_path, 'r') as f:
            framework = json.load(f)
        print(f"✅ Loaded {framework['framework_meta']['name']} v{framework['framework_meta']['version']}")
        return framework
    except Exception as e:
        print(f"❌ Error loading framework: {e}")
        return None

def analyze_sample_texts():
    """Demonstrate analysis of sample historical texts"""
    
    # Sample texts representing each ideological position
    sample_texts = {
        "roosevelt_four_freedoms": {
            "title": "Franklin D. Roosevelt - Four Freedoms Speech (1941)",
            "excerpt": "In the future days, which we seek to make secure, we look forward to a world founded upon four essential human freedoms. The first is freedom of speech and expression—everywhere in the world. The second is freedom of every person to worship God in his own way—everywhere in the world. The third is freedom from want—which, translated into world terms, means economic understandings which will secure to every nation a healthy peacetime life for its inhabitants—everywhere in the world. The fourth is freedom from fear—which, translated into world terms, means a world-wide reduction of armaments to such a point and in such a thorough fashion that no nation will be in a position to commit an act of physical aggression against any neighbor—anywhere in the world.",
            "expected_well": "classical_liberalism",
            "analysis_notes": "Emphasis on individual freedoms, universal rights, international cooperation within liberal framework"
        },
        
        "stalin_constitution": {
            "title": "Stalin - Soviet Constitution Speech (1936)",
            "excerpt": "The draft of the new Constitution of the USSR proceeds from the fact that there are no longer any antagonistic classes in our society; that our society consists of two friendly classes—the workers and peasants; that these classes are in power; that the leading force of our society is the working class headed by the Communist Party. The draft Constitution proceeds from the fact that the nations of the USSR are equal in rights, that they have proved their equality and fraternal cooperation in the common struggle for the consolidation and development of the Soviet system.",
            "expected_well": "communism",
            "analysis_notes": "Class-based analysis, collective ownership, party leadership, international solidarity among Soviet nations"
        },
        
        "mussolini_doctrine": {
            "title": "Benito Mussolini - The Doctrine of Fascism (1932)",
            "excerpt": "Fascism conceives of the State as an absolute, in comparison with which all individuals or groups are relative, only to be conceived of in their relation to the State. For Fascism, the growth of empire, that is to say the expansion of the nation, is an essential manifestation of vitality, and its opposite a sign of decadence. Peoples which are rising, or rising again after a period of decadence, are always imperialist; any renunciation is a sign of decay and of death.",
            "expected_well": "fascism", 
            "analysis_notes": "State supremacy, organic nationalism, imperial expansion, rejection of individual rights"
        }
    }
    
    return sample_texts

def simulate_analysis(framework, sample_texts):
    """Simulate how the framework would analyze the sample texts"""
    
    print("\n" + "="*80)
    print("HISTORICAL IDEOLOGICAL TRIANGLE ANALYSIS SIMULATION")
    print("="*80)
    
    wells = framework['wells']
    
    for text_id, text_data in sample_texts.items():
        print(f"\n📝 Analyzing: {text_data['title']}")
        print("-" * 60)
        
        # Show the text excerpt
        print(f"Text Excerpt:")
        print(f'"{text_data["excerpt"][:200]}..."')
        
        # Show expected well
        expected_well = text_data['expected_well']
        well_name = wells[expected_well]['name']
        well_angle = wells[expected_well]['position']['angle_degrees']
        
        print(f"\n🎯 Expected Gravitational Well: {well_name} ({well_angle}°)")
        print(f"📊 Analysis Notes: {text_data['analysis_notes']}")
        
        # Show relevant language cues for the expected well
        print(f"\n🔍 Key Language Cues from {well_name}:")
        well_config = wells[expected_well]
        for category, cues in well_config['language_cues'].items():
            print(f"   • {category.replace('_', ' ').title()}: {', '.join(cues[:3])}...")
        
        print("\n" + "-" * 60)

def show_framework_overview(framework):
    """Display framework overview"""
    
    meta = framework['framework_meta']
    wells = framework['wells']
    
    print("="*80)
    print(f"FRAMEWORK: {meta['name']} v{meta['version']}")
    print("="*80)
    
    print(f"Description: {meta['description']}")
    print(f"Historical Period: {meta['historical_period']}")
    print(f"Framework Type: {framework['framework_type']}")
    print(f"Calculation Method: {framework['calculation_method']}")
    
    print(f"\n📍 Wells Configuration:")
    for well_id, well_config in wells.items():
        name = well_config['name']
        angle = well_config['position']['angle_degrees']
        coords = well_config['position']['coordinates']
        print(f"   • {name}: {angle}° → ({coords[0]:.3f}, {coords[1]:.3f})")
    
    historical_notes = framework.get('historical_notes', {})
    if historical_notes:
        print(f"\n📚 Historical Context:")
        print(f"   • Collapse Date: {historical_notes.get('collapse_date', 'N/A')}")
        print(f"   • Collapse Reason: {historical_notes.get('collapse_reason', 'N/A')}")
        print(f"   • Key Insight: {historical_notes.get('key_insight', 'N/A')}")

def show_metrics(framework):
    """Display framework-specific metrics"""
    
    metrics = framework.get('metrics', {})
    
    print("\n📊 Framework-Specific Metrics:")
    print("-" * 40)
    
    for metric_name, metric_config in metrics.items():
        print(f"\n• {metric_name.replace('_', ' ').title()}")
        print(f"  Description: {metric_config['description']}")
        if 'interpretation' in metric_config:
            print(f"  Interpretation: {metric_config['interpretation']}")

def main():
    """Main demonstration function"""
    
    print("Historical Ideological Triangle Framework Demo")
    print("=" * 50)
    
    # Load framework
    framework = load_framework()
    if not framework:
        return
    
    # Show framework overview
    show_framework_overview(framework)
    
    # Show metrics
    show_metrics(framework)
    
    # Load and analyze sample texts
    sample_texts = analyze_sample_texts()
    simulate_analysis(framework, sample_texts)
    
    print("\n" + "="*80)
    print("✅ DEMONSTRATION COMPLETE")
    print("="*80)
    print("\nThis framework demonstrates the independent wells approach for analyzing")
    print("20th century political discourse across three competing ideological systems.")
    print("\nKey Features:")
    print("• Independent wells (not dipole oppositions)")
    print("• Equal gravitational strength across all three frameworks")
    print("• Rich historical context and language cues")
    print("• Framework-specific metrics for ideological analysis")
    print("• Comprehensive prompt configuration for LLM analysis")

if __name__ == "__main__":
    main() 