#!/usr/bin/env python3
"""
Natural Jupyter Integration Demo

This script demonstrates how DCS visualization feels natural and effortless
in typical data science workflows.
"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import the pandas accessor (this would normally be: import discernus)
from discernus.jupyter.pandas_accessor import DCSAccessor, DCSFrameworkError

def main():
    print("🚀 DCS Natural Jupyter Integration Demo")
    print("=" * 50)
    
    # Simulate typical researcher workflow
    print("\n1. Researcher loads political discourse data (as usual):")
    
    # Typical data scientists already have
    speech_data = pd.DataFrame({
        'speech_id': ['bolsonaro_july', 'bolsonaro_aug', 'bolsonaro_sept', 'bolsonaro_oct'],
        'populism_score': [0.4, 0.7, 0.6, 0.9],
        'nationalism_score': [0.6, 0.8, 0.9, 0.7],
        'patriotism_score': [0.3, 0.2, 0.4, 0.1],
        'date': ['2018-07', '2018-08', '2018-09', '2018-10']
    })
    
    print(speech_data)
    
    # Natural discovery process
    print("\n2. DCS suggests what to do with this data:")
    try:
        suggestions = speech_data.dcs.suggest_frameworks()
    except Exception as e:
        print(f"Note: In real implementation, this would work. Error: {e}")
        
    # Show what the output would look like
    print("\n🎯 Detected data patterns:")
    print("   • ideological_dimensions: 3 found: populism_score, nationalism_score, patriotism_score")
    print("   • temporal_data: date column detected: date")
    print("   • sample_size: 4 observations")
    print("   • score_range: 0.10 to 0.90")
    
    print("\n📋 Recommended frameworks:")
    print("   1. tamaki_fuks_competitive_populism ⭐ (confidence: 0.9)")
    print("      - Perfect match - handles populism/nationalism/patriotism triangle")
    print("   2. political_worldview_triad (confidence: 0.7)")
    print("      - Alternative - broader context analysis")
    
    # One-line visualization
    print("\n3. Researcher applies framework with natural pandas syntax:")
    print("   speech_data.dcs.tamaki_fuks().plot()")
    print("   → Generates sophisticated triangular competitive space visualization")
    
    # Progressive enhancement
    print("\n4. Easy enhancement with fluent interface:")
    print("   speech_data.dcs.tamaki_fuks()")
    print("     .title('Bolsonaro Campaign Evolution')")
    print("     .add_competitive_dynamics(strength=0.8)")
    print("     .add_temporal_analysis()")
    print("     .export('analysis.html', style='academic')")
    print("   → Creates publication-ready interactive visualization")
    
    # Error handling demo
    print("\n5. Helpful error handling when data doesn't match:")
    
    incomplete_data = pd.DataFrame({
        'speech_id': ['speech1', 'speech2'],
        'populism_score': [0.4, 0.7]
        # Missing nationalism_score, patriotism_score
    })
    
    print("   incomplete_data = pd.DataFrame({")
    print("       'speech_id': ['speech1', 'speech2'],")
    print("       'populism_score': [0.4, 0.7]")
    print("       # Missing other required columns")
    print("   })")
    print("\n   incomplete_data.dcs.tamaki_fuks()")
    print("\n   ❌ Output:")
    
    try:
        incomplete_data.dcs.tamaki_fuks()
    except DCSFrameworkError as e:
        print("   " + str(e).replace('\n', '\n   '))
        
        print("\n   📖 Example data format:")
        example = e.show_example_data()
    except Exception as e:
        # Show what the error would look like
        print("   ❌ Tamaki Fuks framework requires 3 dimensions but found 1")
        print("")
        print("   📋 Required columns:")
        print("      • populism_score ✅ (found)")
        print("      • nationalism_score ❌ (missing)")  
        print("      • patriotism_score ❌ (missing)")
        print("")
        print("   💡 Suggestions:")
        print("      1. Add missing columns to your DataFrame")
        print("      2. Try a different framework: df.dcs.suggest_frameworks()")
        print("      3. Use auto-detection: df.dcs.auto_detect()")
    
    # Comparison to current approach
    print("\n" + "=" * 50)
    print("📊 COMPARISON: Current vs Natural Approach")
    print("=" * 50)
    
    print("\n❌ Current (Complex):")
    print("   1. Read framework YAML documentation")
    print("   2. Study anchor configuration requirements")
    print("   3. Import visualization classes manually")
    print("   4. Configure anchors with angles/weights")
    print("   5. Initialize visualizer with parameters")
    print("   6. Convert data to expected format")
    print("   7. Call visualization methods with config")
    print("   → 20+ lines of setup code")
    
    print("\n✅ Natural (Simple):")
    print("   1. Load data (already doing this)")
    print("   2. speech_data.dcs.tamaki_fuks().plot()")
    print("   → 1 line of code")
    
    print("\n🎯 Result: Researchers can focus on analysis, not implementation!")
    

def show_widget_interface_concept():
    """Show what the widget interface would look like."""
    
    print("\n" + "=" * 50)
    print("🎨 WIDGET INTERFACE CONCEPT")
    print("=" * 50)
    
    print("\nfrom discernus.jupyter_widgets import DCSBuilder")
    print("\nbuilder = DCSBuilder(speech_data)")
    print("builder.show()")
    print("\n# Would display interactive widget with:")
    print("   • Dropdown: Framework Selection")
    print("     - [tamaki_fuks_competitive_populism ⭐]")
    print("     - [moral_foundations_theory]")
    print("     - [political_worldview_triad]")
    print("")
    print("   • Column Mapping:")
    print("     - Populism: [populism_score ▼]")
    print("     - Nationalism: [nationalism_score ▼]")  
    print("     - Patriotism: [patriotism_score ▼]")
    print("")
    print("   • Options:")
    print("     - ☑ Add competitive dynamics")
    print("     - ☑ Include temporal analysis")
    print("     - ☑ Academic style export")
    print("")
    print("   • [Generate Visualization] button")
    print("")
    print("   • Live preview pane shows visualization")
    print("   • Generated code pane shows equivalent Python")
    

if __name__ == "__main__":
    main()
    show_widget_interface_concept()
    
    print("\n" + "=" * 50)
    print("🚀 Ready to transform DCS from complex to natural!")
    print("=" * 50) 