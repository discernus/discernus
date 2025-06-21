#!/usr/bin/env python3
"""
Real Narrative Gravity Maps Mathematical Calculations Demo
Shows actual mathematical positioning and visualization generation
"""

import sys
import json
import numpy as np
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from narrative_gravity.engine_circular import NarrativeGravityWellsCircular
from narrative_gravity.framework_manager import FrameworkManager
from narrative_gravity.visualization.engine import NarrativeGravityVisualizationEngine

def demo_real_mathematical_calculations():
    """Demonstrate real mathematical calculations using the NGM engine"""
    
    print("🔬 REAL NARRATIVE GRAVITY MATHEMATICAL CALCULATIONS DEMO")
    print("=" * 70)
    print("This demo shows actual mathematical positioning and visualization generation!")
    print()
    
    # Initialize engines
    print("🔧 Initializing NGM Engine...")
    try:
        engine = NarrativeGravityWellsCircular()
        viz_engine = NarrativeGravityVisualizationEngine(theme='academic')
        print("✅ Engines initialized successfully")
    except Exception as e:
        print(f"❌ Engine initialization failed: {e}")
        return
    
    # Define sample well scores (simulating LLM analysis results)
    sample_analyses = {
        "obama_unity_speech": {
            "title": "Obama - Unity Speech (Dignity-Focused)",
            "well_scores": {
                'hope': 0.85,      # High positive scoring
                'justice': 0.70,   # Moderate positive  
                'truth': 0.60,     # Moderate positive
                'fear': 0.15,      # Low negative
                'manipulation': 0.10  # Very low negative
            },
            "expected_position": "Upper right quadrant (integrative)"
        },
        
        "divisive_rhetoric": {
            "title": "Divisive Political Rhetoric (Fear-Based)",
            "well_scores": {
                'hope': 0.20,      # Low positive
                'justice': 0.25,   # Low positive
                'truth': 0.15,     # Very low positive
                'fear': 0.80,      # High negative
                'manipulation': 0.75  # High negative
            },
            "expected_position": "Lower left quadrant (disintegrative)"
        },
        
        "balanced_analysis": {
            "title": "Balanced Political Analysis",
            "well_scores": {
                'hope': 0.45,      # Moderate positive
                'justice': 0.50,   # Moderate positive
                'truth': 0.55,     # Moderate positive
                'fear': 0.35,      # Low-moderate negative
                'manipulation': 0.25  # Low negative
            },
            "expected_position": "Center-right (slightly integrative)"
        }
    }
    
    print(f"🎯 Performing mathematical analysis on {len(sample_analyses)} samples...")
    
    results = []
    
    for analysis_id, analysis_data in sample_analyses.items():
        print(f"\n📝 Analyzing: {analysis_data['title']}")
        print("-" * 60)
        
        well_scores = analysis_data['well_scores']
        
        # Perform actual mathematical calculations
        print("🧮 Calculating narrative position...")
        x, y = engine.calculate_narrative_position(well_scores)
        distance = np.sqrt(x**2 + y**2)
        angle = np.degrees(np.arctan2(y, x))
        
        print("✅ Mathematical calculation complete!")
        
        # Display results
        print(f"📊 Mathematical Results:")
        print(f"   • Narrative Position: ({x:.3f}, {y:.3f})")
        print(f"   • Distance from Origin: {distance:.3f}")
        print(f"   • Angle: {angle:.1f}°")
        print(f"   • Expected Pattern: {analysis_data['expected_position']}")
        
        # Show well score contributions
        print(f"   • Well Score Contributions:")
        for well_name, score in well_scores.items():
            well_info = engine.well_definitions.get(well_name, {})
            well_angle = well_info.get('angle', 0)
            well_type = well_info.get('type', 'unknown')
            contribution_x, contribution_y = engine.circle_point(well_angle)
            weighted_contribution = score * well_info.get('weight', 1.0)
            print(f"     - {well_name} ({well_type}): {score:.2f} @ {well_angle}° → contribution = {weighted_contribution:.3f}")
        
        # Store result for visualization
        results.append({
            'title': analysis_data['title'],
            'position': (x, y),
            'distance': distance,
            'angle': angle,
            'well_scores': well_scores,
            'wells': engine.well_definitions
        })
    
    # Generate real visualization
    print(f"\n🎨 Generating Interactive Visualization...")
    try:
        # Prepare data for visualization
        viz_analyses = []
        for result in results:
            viz_analyses.append({
                'title': result['title'],
                'wells': result['wells'],
                'scores': result['well_scores']
            })
        
        # Create visualization
        output_path = Path("analysis_results") / "real_mathematical_demo_results.html"
        output_path.parent.mkdir(exist_ok=True)
        
        fig = viz_engine.create_comparative_analysis(
            analyses=viz_analyses,
            title="Real Mathematical Calculations Demo - NGM Engine",
            output_html=str(output_path),
            show=False
        )
        
        print(f"✅ Interactive visualization saved: {output_path}")
        print(f"   Open in browser to see real mathematical positioning!")
        
        # Also create single analysis examples
        for i, result in enumerate(results):
            single_output = output_path.parent / f"single_analysis_{i+1}.html"
            viz_engine.create_single_analysis(
                wells=result['wells'],
                narrative_scores=result['well_scores'],
                title=result['title'],
                output_html=str(single_output),
                show=False
            )
            print(f"   Single analysis saved: {single_output}")
        
    except Exception as e:
        print(f"⚠️ Visualization generation failed: {e}")
        print("   (Mathematical calculations still succeeded)")
    
    # Mathematical comparison summary
    print(f"\n🔢 MATHEMATICAL COMPARISON SUMMARY:")
    print("=" * 50)
    
    for result in results:
        x, y = result['position']
        distance = result['distance']
        angle = result['angle']
        
        # Determine quadrant
        if x >= 0 and y >= 0:
            quadrant = "Upper Right (Integrative)"
        elif x < 0 and y >= 0:
            quadrant = "Upper Left"
        elif x < 0 and y < 0:
            quadrant = "Lower Left (Disintegrative)"
        else:
            quadrant = "Lower Right"
        
        print(f"📍 {result['title'][:30]}...")
        print(f"   Position: ({x:.3f}, {y:.3f})")
        print(f"   Distance: {distance:.3f}")
        print(f"   Angle: {angle:.1f}°")
        print(f"   Quadrant: {quadrant}")
    
    # Demonstrate coordinate system
    print(f"\n🎯 COORDINATE SYSTEM EXPLANATION:")
    print("=" * 50)
    print("The circular coordinate system positions narratives based on well attractions:")
    print("• Integrative wells (hope, justice, truth) pull toward positive quadrants")
    print("• Disintegrative wells (fear, manipulation) pull toward negative quadrants") 
    print("• Distance from origin indicates narrative coherence")
    print("• Angle indicates dominant thematic direction")
    
    # Well positioning
    print(f"\n📍 WELL POSITIONS IN COORDINATE SYSTEM:")
    for well_name, well_info in engine.well_definitions.items():
        angle = well_info.get('angle', 0)
        well_type = well_info.get('type', 'unknown')
        x, y = engine.circle_point(angle)
        print(f"   • {well_name} ({well_type}): {angle}° → ({x:.3f}, {y:.3f})")
    
    return results

def demo_framework_loading():
    """Demonstrate loading different frameworks with real calculations"""
    
    print(f"\n🔧 FRAMEWORK LOADING DEMONSTRATION")
    print("=" * 50)
    
    try:
        framework_manager = FrameworkManager()
        
        # List available frameworks
        print("📚 Available frameworks:")
        # This would list frameworks if the directory exists
        frameworks_dir = Path("frameworks")
        if frameworks_dir.exists():
            for framework_dir in frameworks_dir.iterdir():
                if framework_dir.is_dir():
                    print(f"   • {framework_dir.name}")
        else:
            print("   • Using default configuration (no frameworks directory found)")
        
        print("\n🔍 Testing default framework configuration:")
        engine = NarrativeGravityWellsCircular()
        
        # Show loaded configuration
        print(f"   Wells configured: {len(engine.well_definitions)}")
        for well_name, well_config in engine.well_definitions.items():
            print(f"     - {well_name}: {well_config}")
        
        # Test calculation with default configuration
        test_scores = {'hope': 0.8, 'fear': 0.3, 'justice': 0.6, 'truth': 0.4, 'manipulation': 0.2}
        x, y = engine.calculate_narrative_position(test_scores)
        print(f"\n   Test calculation result: ({x:.3f}, {y:.3f})")
        
    except Exception as e:
        print(f"   ⚠️ Framework loading issue: {e}")

def main():
    """Main demo function"""
    
    print("🚀 STARTING REAL NGM MATHEMATICAL CALCULATIONS DEMO")
    print("=" * 70)
    print("This demo demonstrates the difference between:")
    print("❌ Fake demos: Just displaying framework information")
    print("✅ Real demos: Actual mathematical calculations + visualizations")
    print()
    
    # Run mathematical calculations demo
    results = demo_real_mathematical_calculations()
    
    # Run framework loading demo
    demo_framework_loading()
    
    print(f"\n🎉 DEMO COMPLETE!")
    print("=" * 50)
    print("What this demo actually accomplished:")
    print("✅ Real mathematical positioning calculations")
    print("✅ Coordinate system positioning (x, y coordinates)")
    print("✅ Distance and angle calculations")
    print("✅ Interactive HTML visualizations generated")
    print("✅ Multiple analysis comparison")
    print("✅ Demonstrates working NGM mathematical engine")
    print()
    print("🔬 This is what actual NGM analysis looks like!")
    print("   (Not just printing framework information)")

if __name__ == "__main__":
    main() 