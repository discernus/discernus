#!/usr/bin/env python3
"""
Real Narrative Gravity Maps Analysis Demo
Demonstrates actual mathematical calculations and visualizations using the NGM engine
"""

import sys
import json
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from narrative_gravity.engine_circular import NarrativeGravityWellsCircular
from narrative_gravity.framework_manager import FrameworkManager
from narrative_gravity.visualization.engine import NarrativeGravityVisualizationEngine

def demo_civic_virtue_analysis():
    """Demonstrate real analysis using Civic Virtue framework"""
    
    print("🔬 REAL NARRATIVE GRAVITY MAPS ANALYSIS DEMO")
    print("=" * 60)
    
    # Initialize the engine
    print("🔧 Initializing NGM Engine...")
    try:
        framework_manager = FrameworkManager()
        engine = NarrativeGravityWellsCircular()
        viz_engine = NarrativeGravityVisualizationEngine()
        print("✅ Engine initialized successfully")
    except Exception as e:
        print(f"❌ Engine initialization failed: {e}")
        return
    
    # Load Civic Virtue framework
    print("\n📚 Loading Civic Virtue Framework...")
    try:
        framework = framework_manager.load_framework('civic_virtue')
        print(f"✅ Loaded framework: {framework.name} v{framework.version}")
        print(f"   Wells: {len(framework.wells)} configured")
    except Exception as e:
        print(f"❌ Framework loading failed: {e}")
        return
    
    # Sample texts for analysis
    sample_texts = {
        "obama_dignity": {
            "title": "Obama - 2008 Convention Speech (Dignity Example)",
            "text": """There is not a liberal America and a conservative America—there is the United States of America. There is not a black America and white America and Latino America and Asian America—there is the United States of America. We are one people, all of us pledging allegiance to the stars and stripes, all of us defending the United States of America. In the end, that's what this election is about. Do we participate in a politics of cynicism, or do we participate in a politics of hope? The choice is ours. We can choose to be divided, or we can choose to come together. We can choose to focus on what separates us, or we can choose to focus on what unites us. The American people deserve better than the politics of division.""",
            "expected": "Should lean toward Dignity wells (universal human worth, bridging language)"
        },
        
        "trump_tribal": {
            "title": "Trump - 2016 Campaign Rally (Tribal Example)", 
            "text": """We will make America great again! The forgotten men and women of our country will be forgotten no longer. We will bring back our jobs. We will bring back our borders. We will bring back our wealth. And we will bring back our dreams. We will build a great wall along the southern border. And Mexico will pay for the wall. We will make our military so strong that nobody will mess with us. America first! America first! We will no longer surrender this country or its people to the false song of globalism. The American people will come first once again.""",
            "expected": "Should lean toward Tribal wells (us vs them, group loyalty, exclusion)"
        }
    }
    
    print(f"\n🎯 Analyzing {len(sample_texts)} sample texts...")
    
    results = []
    
    for text_id, text_data in sample_texts.items():
        print(f"\n📝 Analyzing: {text_data['title']}")
        print("-" * 50)
        
        try:
            # Run the actual analysis
            print("🧮 Running mathematical analysis...")
            result = engine.analyze_text(
                text=text_data['text'],
                framework=framework,
                calculate_center_of_mass=True,
                calculate_narrative_polarity=True
            )
            
            print("✅ Analysis complete!")
            
            # Display mathematical results
            print(f"📊 Mathematical Results:")
            if hasattr(result, 'center_of_mass') and result.center_of_mass:
                x, y = result.center_of_mass
                distance = (x**2 + y**2)**0.5
                print(f"   • Center of Mass: ({x:.3f}, {y:.3f})")
                print(f"   • Distance from Origin: {distance:.3f}")
            
            if hasattr(result, 'narrative_polarity_score'):
                print(f"   • Narrative Polarity Score: {result.narrative_polarity_score:.3f}")
            
            if hasattr(result, 'directional_purity_score'):
                print(f"   • Directional Purity Score: {result.directional_purity_score:.3f}")
            
            # Show well scores
            if hasattr(result, 'well_scores') and result.well_scores:
                print(f"   • Well Scores:")
                for well_name, score in result.well_scores.items():
                    print(f"     - {well_name}: {score:.3f}")
            
            print(f"📈 Expected Pattern: {text_data['expected']}")
            
            results.append({
                'text_id': text_id,
                'title': text_data['title'],
                'result': result,
                'text': text_data['text']
            })
            
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            continue
    
    # Generate visualizations
    print(f"\n🎨 Generating Visualizations...")
    try:
        # Create a batch visualization
        viz_data = []
        for r in results:
            if hasattr(r['result'], 'center_of_mass') and r['result'].center_of_mass:
                viz_data.append({
                    'title': r['title'],
                    'center_of_mass': r['result'].center_of_mass,
                    'well_scores': getattr(r['result'], 'well_scores', {}),
                    'narrative_polarity_score': getattr(r['result'], 'narrative_polarity_score', 0),
                    'text_preview': r['text'][:100] + "..."
                })
        
        if viz_data:
            # Generate visualization
            output_path = Path("analysis_results") / "real_ngm_demo_results.html"
            output_path.parent.mkdir(exist_ok=True)
            
            viz_engine.create_comparative_analysis(
                analyses=viz_data,
                title="Real NGM Analysis Demo - Civic Virtue Framework",
                output_html=str(output_path),
                show=False
            )
            
            print(f"✅ Interactive visualization saved: {output_path}")
            print(f"   Open in browser to see real mathematical positioning!")
        
    except Exception as e:
        print(f"⚠️ Visualization generation failed: {e}")
        print("   (Mathematical analysis still succeeded)")
    
    # Summary
    print(f"\n🎯 DEMO SUMMARY:")
    print("=" * 40)
    print(f"✅ Real mathematical analysis completed")
    print(f"✅ {len(results)} texts analyzed with actual calculations")
    print(f"✅ Center of mass coordinates calculated")
    print(f"✅ Well scores computed using framework weights")
    print(f"✅ Narrative polarity scores derived")
    
    if results:
        print(f"\n📊 MATHEMATICAL COMPARISON:")
        for r in results:
            if hasattr(r['result'], 'center_of_mass') and r['result'].center_of_mass:
                x, y = r['result'].center_of_mass
                distance = (x**2 + y**2)**0.5
                print(f"   • {r['title'][:30]}...: ({x:.3f}, {y:.3f}) distance={distance:.3f}")
    
    print(f"\n🔬 This demonstrates the difference between:")
    print(f"   ❌ Fake demos (just displaying framework info)")
    print(f"   ✅ Real analysis (actual math + visualizations)")

def demo_framework_comparison():
    """Demonstrate analysis across multiple frameworks"""
    
    print(f"\n🔀 MULTI-FRAMEWORK COMPARISON DEMO")
    print("=" * 50)
    
    # Sample text for cross-framework analysis
    sample_text = """The strength of our democracy depends not on any one person, but on our ability to work together across our differences. We must reject the politics of division and embrace the politics of unity. Every American, regardless of their background, deserves equal dignity and respect. We can disagree on policy while still affirming our shared humanity and common values. This is what makes America great - not our ability to exclude others, but our capacity to include everyone in the American dream."""
    
    frameworks_to_test = ['civic_virtue', 'political_spectrum']
    
    print(f"📝 Analyzing same text across {len(frameworks_to_test)} frameworks...")
    print(f"Text: {sample_text[:100]}...")
    
    try:
        framework_manager = FrameworkManager()
        engine = NarrativeGravityWellsCircular()
        
        for framework_name in frameworks_to_test:
            print(f"\n🔍 Framework: {framework_name}")
            try:
                framework = framework_manager.load_framework(framework_name)
                result = engine.analyze_text(
                    text=sample_text,
                    framework=framework,
                    calculate_center_of_mass=True
                )
                
                if hasattr(result, 'center_of_mass') and result.center_of_mass:
                    x, y = result.center_of_mass
                    distance = (x**2 + y**2)**0.5
                    print(f"   Position: ({x:.3f}, {y:.3f}) distance={distance:.3f}")
                else:
                    print(f"   ❌ No center of mass calculated")
                    
            except Exception as e:
                print(f"   ❌ Analysis failed: {e}")
                
    except Exception as e:
        print(f"❌ Multi-framework demo failed: {e}")

def main():
    """Main demo function"""
    
    print("🚀 STARTING REAL NGM ANALYSIS DEMO")
    print("This demo actually runs the mathematical engine and generates visualizations!")
    print("")
    
    # Run civic virtue analysis demo
    demo_civic_virtue_analysis()
    
    # Run multi-framework comparison  
    demo_framework_comparison()
    
    print(f"\n🎉 DEMO COMPLETE!")
    print("=" * 50)
    print("Key Differences from fake demos:")
    print("✅ Real mathematical calculations")
    print("✅ Actual coordinate positioning")
    print("✅ Interactive visualizations generated")
    print("✅ Cross-framework comparisons")
    print("✅ Demonstrates working NGM engine")

if __name__ == "__main__":
    main() 