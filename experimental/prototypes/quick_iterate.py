#!/usr/bin/env python3
"""
Quick Iteration Script for Discernus Visualization Engine
=======================================================

Interactive script for rapid visualization development.
Allows quick theme switching and instant visualization generation.
"""

import time
import os
import sys
from pathlib import Path
import pandas as pd

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from discernus_visualization_engine import create_visualization_engine
from discernus_coordinate_visualizer import DiscernusCoordinateVisualizer

def load_sample_data():
    """Load consistent sample data for iteration."""
    return pd.DataFrame({
        'text_id': ['climate_article', 'political_speech', 'healthcare_debate'],
        'framework': ['moral_foundations', 'moral_foundations', 'moral_foundations'],
        'model': ['gpt-4-turbo', 'gpt-4-turbo', 'gpt-4-turbo'],
        'api_cost': [0.002, 0.003, 0.002],
        'well_care': [0.85, 0.45, 0.90],
        'well_fairness': [0.70, 0.80, 0.75],
        'well_loyalty': [0.30, 0.85, 0.40],
        'well_authority': [0.25, 0.75, 0.30],
        'well_sanctity': [0.20, 0.60, 0.35]
    })

def get_sample_anchors():
    """Get consistent anchor configuration."""
    return {
        'Care': {'angle': 0, 'type': 'integrative', 'weight': 1.0},
        'Fairness': {'angle': 72, 'type': 'integrative', 'weight': 1.0},
        'Loyalty': {'angle': 144, 'type': 'binding', 'weight': 1.0},
        'Authority': {'angle': 216, 'type': 'binding', 'weight': 1.0},
        'Sanctity': {'angle': 288, 'type': 'binding', 'weight': 1.0}
    }

def get_sample_scores():
    """Get sample axis scores."""
    return {'Care': 0.8, 'Fairness': 0.6, 'Loyalty': 0.4, 'Authority': 0.3, 'Sanctity': 0.2}

def generate_quick_viz(theme='academic'):
    """Generate visualization quickly with comprehensive system."""
    print(f"🔄 Generating comprehensive visualizations with {theme} theme...")
    
    # Load data
    df = load_sample_data()
    
    # Create engine
    engine = create_visualization_engine(theme=theme)
    
    # Generate comprehensive visualizations
    structured_results = {'structured_data': df}
    statistical_results = {'hypothesis_testing': {'foundation_independence': {'status': 'supported'}}}
    reliability_results = {'reliability_metrics': {'model_consistency': {'total_models': 3}}}
    
    viz_results = engine.generate_comprehensive_visualizations(
        structured_results, statistical_results, reliability_results
    )
    
    print(f"✅ Generated {len(engine.generated_files)} comprehensive visualization files")
    return engine.generated_files

def generate_quick_coordinate(theme='academic', custom_title=None):
    """Generate single coordinate plot quickly."""
    print(f"🗺️ Generating coordinate plot with {theme} theme...")
    
    # Create coordinate visualizer
    coord_viz = DiscernusCoordinateVisualizer(theme=theme)
    
    # Get sample data
    anchors = get_sample_anchors()
    scores = get_sample_scores()
    
    # Generate plot
    title = custom_title or f'Quick Iteration - {theme.title()} Theme'
    fig = coord_viz.plot_coordinate_system(
        anchors=anchors,
        axis_scores=scores,
        title=title,
        output_html='iteration_output/quick_coordinate.html',
        show=False
    )
    
    print("✅ Generated coordinate plot")
    return 'iteration_output/quick_coordinate.html'

def compare_themes():
    """Generate visualizations for all themes for comparison."""
    print("🎨 Generating theme comparison...")
    
    themes = ['academic', 'presentation', 'publication']
    generated_files = {}
    
    for theme in themes:
        print(f"  📊 Generating {theme} theme...")
        
        # Create theme-specific directory
        theme_dir = f'iteration_output/theme_{theme}'
        os.makedirs(theme_dir, exist_ok=True)
        
        # Generate coordinate plot
        coord_viz = DiscernusCoordinateVisualizer(theme=theme)
        anchors = get_sample_anchors()
        scores = get_sample_scores()
        
        coord_file = f'{theme_dir}/coordinate_comparison.html'
        fig = coord_viz.plot_coordinate_system(
            anchors=anchors,
            axis_scores=scores,
            title=f'Theme Comparison - {theme.title()}',
            output_html=coord_file,
            show=False
        )
        
        generated_files[theme] = coord_file
    
    print("✅ Theme comparison complete!")
    print("📂 Files generated:")
    for theme, file_path in generated_files.items():
        print(f"   {theme}: {file_path}")
    
    return generated_files

def show_menu():
    """Display the interactive menu."""
    print("\n" + "="*60)
    print("🚀 DISCERNUS VISUALIZATION ENGINE - RAPID ITERATION")
    print("="*60)
    print("1. Quick comprehensive visualization (all plots)")
    print("2. Quick coordinate plot only")
    print("3. Compare all themes")
    print("4. Custom coordinate plot")
    print("5. Show generated files")
    print("6. Clear iteration output")
    print("7. Help")
    print("q. Quit")
    print("="*60)

def show_help():
    """Show help information."""
    print("\n📖 HELP - Rapid Iteration Workflow:")
    print("="*50)
    print("🎯 Purpose: Iterate on visualizations without production pipeline overhead")
    print()
    print("📋 Workflow:")
    print("1. Choose option 1 or 2 to generate initial visualizations")
    print("2. Open generated HTML files in your browser")
    print("3. Make changes to code (themes, math, styling)")
    print("4. Re-run generation (same option)")
    print("5. Refresh browser to see changes")
    print()
    print("⚡ Speed Tips:")
    print("• Use option 2 for fastest iteration (coordinate plots only)")
    print("• Use option 3 to compare themes side-by-side")
    print("• Keep browser tab open and refresh after each generation")
    print("• Use option 4 for custom experiments")
    print()
    print("📁 Files saved to: iteration_output/")
    print("🔄 Edit discernus_*.py files to modify visualization behavior")

def show_generated_files():
    """Show currently generated files."""
    output_dir = Path('iteration_output')
    
    if not output_dir.exists():
        print("📁 No iteration output directory found")
        return
    
    html_files = list(output_dir.glob('*.html'))
    subdirs = [d for d in output_dir.iterdir() if d.is_dir()]
    
    print(f"\n📂 Generated Files in {output_dir}:")
    print("-" * 40)
    
    if html_files:
        print("📊 HTML Files:")
        for file in sorted(html_files):
            size = file.stat().st_size / 1024  # KB
            print(f"   {file.name} ({size:.1f} KB)")
    
    if subdirs:
        print("\n📁 Subdirectories:")
        for subdir in sorted(subdirs):
            subdir_files = list(subdir.glob('*.html'))
            print(f"   {subdir.name}/ ({len(subdir_files)} files)")
    
    if not html_files and not subdirs:
        print("   No files generated yet")

def clear_output():
    """Clear iteration output directory."""
    import shutil
    
    output_dir = Path('iteration_output')
    if output_dir.exists():
        response = input("⚠️  Clear all files in iteration_output/? (y/N): ").strip().lower()
        if response == 'y':
            shutil.rmtree(output_dir)
            print("✅ Iteration output cleared")
        else:
            print("❌ Cancelled")
    else:
        print("📁 No iteration output directory to clear")

def custom_coordinate_plot():
    """Generate custom coordinate plot with user parameters."""
    print("\n🎨 Custom Coordinate Plot Generator")
    print("-" * 40)
    
    try:
        # Get theme
        theme = input("Theme (academic/presentation/publication) [academic]: ").strip() or 'academic'
        if theme not in ['academic', 'presentation', 'publication']:
            print("❌ Invalid theme, using 'academic'")
            theme = 'academic'
        
        # Get custom title
        title = input("Custom title [Quick Custom Plot]: ").strip() or 'Quick Custom Plot'
        
        # Get figure size
        size_input = input("Figure size (600/800/1000) [800]: ").strip()
        figure_size = 800
        if size_input in ['600', '800', '1000']:
            figure_size = int(size_input)
        
        # Create custom visualizer
        coord_viz = DiscernusCoordinateVisualizer(
            theme=theme,
            figure_size=figure_size
        )
        
        # Generate plot
        anchors = get_sample_anchors()
        scores = get_sample_scores()
        
        output_file = 'iteration_output/custom_coordinate.html'
        fig = coord_viz.plot_coordinate_system(
            anchors=anchors,
            axis_scores=scores,
            title=title,
            output_html=output_file,
            show=False
        )
        
        print(f"✅ Custom coordinate plot generated: {output_file}")
        
    except KeyboardInterrupt:
        print("\n❌ Cancelled")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main interactive loop."""
    print("🗺️ Discernus Visualization Engine - Rapid Iteration")
    print("Setting up environment...")
    
    # Ensure output directory exists
    os.makedirs('iteration_output', exist_ok=True)
    
    while True:
        try:
            show_menu()
            choice = input("\nEnter your choice: ").strip().lower()
            
            if choice == 'q':
                print("👋 Goodbye! Happy iterating!")
                break
            
            elif choice == '1':
                theme = input("Theme (academic/presentation/publication) [academic]: ").strip() or 'academic'
                if theme not in ['academic', 'presentation', 'publication']:
                    print("❌ Invalid theme, using 'academic'")
                    theme = 'academic'
                
                files = generate_quick_viz(theme)
                print(f"📂 Open files in iteration_output/")
                
            elif choice == '2':
                theme = input("Theme (academic/presentation/publication) [academic]: ").strip() or 'academic'
                if theme not in ['academic', 'presentation', 'publication']:
                    print("❌ Invalid theme, using 'academic'")
                    theme = 'academic'
                
                file_path = generate_quick_coordinate(theme)
                print(f"📂 Open: {file_path}")
                
            elif choice == '3':
                compare_themes()
                
            elif choice == '4':
                custom_coordinate_plot()
                
            elif choice == '5':
                show_generated_files()
                
            elif choice == '6':
                clear_output()
                
            elif choice == '7':
                show_help()
                
            else:
                print("❌ Invalid choice. Please try again.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Happy iterating!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Please try again or press Ctrl+C to quit.")

if __name__ == '__main__':
    main() 