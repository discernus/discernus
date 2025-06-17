#!/usr/bin/env python3
"""
Demo script for the Three Wells Political Discourse Framework
Demonstrates analysis of contemporary political texts using independent wells approach
"""

import json
import os
import sys
from pathlib import Path

def load_framework():
    """Load the Three Wells Political framework configuration"""
    framework_path = Path("frameworks/three_wells_political/framework.json")
    
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
    """Demonstrate analysis of sample contemporary political texts"""
    
    # Sample texts representing each theoretical position
    sample_texts = {
        "obama_2008_unity": {
            "title": "Barack Obama - 2008 Convention Speech",
            "excerpt": "There is not a liberal America and a conservative America—there is the United States of America. There is not a black America and white America and Latino America and Asian America—there is the United States of America. We are one people, all of us pledging allegiance to the stars and stripes, all of us defending the United States of America. In the end, that's what this election is about. Do we participate in a politics of cynicism, or do we participate in a politics of hope?",
            "expected_well": "pluralist_individual_dignity_theory",
            "analysis_notes": "Emphasis on shared humanity, unity across differences, universal American identity transcending group categories"
        },
        
        "ocasio_cortez_intersectional": {
            "title": "Alexandria Ocasio-Cortez - Congressional Speech on Climate Justice",
            "excerpt": "When we talk about climate, we have to talk about it through the lens of what work pays and what work doesn't. We have to talk about it through the lens of housing and how that's wrapped up in health care. And we have to talk about it through the lens of race and class and how the frontline communities that are impacted by climate change are black and brown communities. These are communities that have been historically red-lined, that have been disinvested from. And so when we're not centering those communities, we're not actually talking about climate change.",
            "expected_well": "intersectionality_theory",
            "analysis_notes": "Multiple identity analysis, systemic oppression focus, marginalized community emphasis, structural inequality lens"
        },
        
        "trump_2016_tribal": {
            "title": "Donald Trump - 2016 Convention Speech",
            "excerpt": "The American People will come first once again. My plan will begin with safety at home – which means safe neighborhoods, secure borders, and protection from terrorism. There can be no prosperity without law and order. On the economy, I will outline reforms to add millions of new jobs and trillions in new wealth. America has lost nearly-one third of its manufacturing jobs since 1997, following the enactment of disastrous trade deals supported by Bill and Hillary Clinton. Remember, it was Bill Clinton who signed NAFTA, one of the worst economic deals ever made by our country.",
            "expected_well": "tribal_domination_theory", 
            "analysis_notes": "America First rhetoric, us-versus-them framing, group preference for Americans, exclusionary economic nationalism"
        }
    }
    
    return sample_texts

def simulate_analysis(framework, sample_texts):
    """Simulate how the framework would analyze the sample texts"""
    
    print("\n" + "="*80)
    print("THREE WELLS POLITICAL DISCOURSE ANALYSIS SIMULATION")
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
        print(f"   • Emergence Period: {historical_notes.get('emergence_period', 'N/A')}")
        print(f"   • Transition From: {historical_notes.get('transition_from', 'N/A')}")
        print(f"   • Key Insight: {historical_notes.get('key_insight', 'N/A')}")

def show_comparison_to_historical(framework):
    """Show comparison to historical 20th century framework"""
    
    print("\n🔄 Evolution of Political Gravitational Wells:")
    print("-" * 50)
    
    print("20th Century Triangle (1900-1989):")
    print("   • Classical Liberalism → Individual rights, market economics")
    print("   • Communism → Class-based analysis, collective ownership") 
    print("   • Fascism → State supremacy, organic nationalism")
    print("   Focus: Economic/state organization")
    
    print("\n21st Century Triangle (2010-present):")
    for well_id, well_config in framework['wells'].items():
        name = well_config['name']
        focus = well_config['core_principles'][0]
        print(f"   • {name} → {focus}")
    print("   Focus: Identity/dignity/belonging")
    
    print(f"\nTransition Period: {framework['historical_notes']['transition_period']}")
    print(f"Key Change: {framework['historical_notes']['gravitational_evolution']}")

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
    
    print("Three Wells Political Discourse Framework Demo")
    print("=" * 55)
    
    # Load framework
    framework = load_framework()
    if not framework:
        return
    
    # Show framework overview
    show_framework_overview(framework)
    
    # Show comparison to historical framework
    show_comparison_to_historical(framework)
    
    # Show metrics
    show_metrics(framework)
    
    # Load and analyze sample texts
    sample_texts = analyze_sample_texts()
    simulate_analysis(framework, sample_texts)
    
    print("\n" + "="*80)
    print("✅ DEMONSTRATION COMPLETE")
    print("="*80)
    print("\nThis framework demonstrates contemporary political discourse analysis through")
    print("three independent gravitational wells that transcend traditional left-right categories.")
    print("\nKey Features:")
    print("• Independent wells representing competing theories about human nature and social organization")
    print("• Evolution from 20th century economic/state focus to 21st century identity/dignity focus")
    print("• Rich theoretical foundations with comprehensive language cues and recognition patterns")
    print("• Framework-specific metrics for contemporary political analysis")
    print("• Explains cross-cutting coalitions and seemingly contradictory political phenomena")

if __name__ == "__main__":
    main() 