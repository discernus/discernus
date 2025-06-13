#!/usr/bin/env python3
"""
Generic Multi-Run Narrative Gravity Analysis Dashboard - NO API VERSION
========================================================================

Testing/offline version that works with any framework, speaker, and text type
WITHOUT making API calls for summary generation. Uses the centralized 
visualization system for consistent professional outputs.

This script is identical to the main dashboard except:
- No LLM API calls for summary generation (uses simple templates)
- Designed for testing and offline analysis scenarios
- All visualizations use the centralized Plotly-based system
"""

import json
import numpy as np
from pathlib import Path
from datetime import datetime
import textwrap
import re
from typing import Dict, List, Optional, Tuple, Any

# Import the centralized visualization system
import sys
sys.path.append('.')
from src.narrative_gravity.visualization import create_visualization_engine
from src.narrative_gravity.engine_circular import NarrativeGravityWellsCircular

# NOTE: This version avoids API dependencies for testing
import time

def extract_scores_from_raw_response(raw_response: str) -> Dict[str, float]:
    """Extract scores from the raw JSON response"""
    try:
        lines = raw_response.strip().split('\n')
        json_lines = []
        in_json = False
        brace_count = 0
        
        for line in lines:
            if line.strip().startswith('{') and not in_json:
                in_json = True
                brace_count = 1
                json_lines.append(line)
            elif in_json:
                json_lines.append(line)
                brace_count += line.count('{') - line.count('}')
                if brace_count == 0:
                    break
        
        if json_lines:
            json_str = '\n'.join(json_lines)
            parsed = json.loads(json_str)
            return parsed.get('scores', {})
    except:
        pass
    return {}

def extract_analysis_from_raw_response(raw_response: str) -> str:
    """Extract the analysis text from the raw JSON response"""
    try:
        lines = raw_response.strip().split('\n')
        json_lines = []
        in_json = False
        brace_count = 0
        
        for line in lines:
            if line.strip().startswith('{') and not in_json:
                in_json = True
                brace_count = 1
                json_lines.append(line)
            elif in_json:
                json_lines.append(line)
                brace_count += line.count('{') - line.count('}')
                if brace_count == 0:
                    break
        
        if json_lines:
            json_str = '\n'.join(json_lines)
            parsed = json.loads(json_str)
            return parsed.get('analysis', '')
    except:
        pass
    return ""

def parse_filename_metadata(results_file: str) -> Dict[str, str]:
    """Extract metadata from filename using common patterns"""
    filename = Path(results_file).stem
    metadata = {}
    
    # Common patterns to extract speaker, framework, year, etc.
    patterns = [
        r'([a-zA-Z]+)_(\d{4})_([a-zA-Z_]+)_(\d{8}_\d{6})',  # speaker_year_framework_timestamp
        r'([a-zA-Z]+)_multi_run_([a-zA-Z_]+)_(\d{8}_\d{6})', # speaker_multi_run_framework_timestamp
        r'([a-zA-Z]+)_([a-zA-Z_]+)_(\d{4})', # speaker_framework_year
    ]
    
    for pattern in patterns:
        match = re.search(pattern, filename, re.IGNORECASE)
        if match:
            groups = match.groups()
            if len(groups) >= 3:
                metadata['speaker'] = groups[0].title()
                if groups[1].isdigit():  # year in second position
                    metadata['year'] = groups[1]
                    metadata['framework'] = groups[2].replace('_', ' ').title()
                else:  # framework in second position
                    metadata['framework'] = groups[1].replace('_', ' ').title()
                    if len(groups) > 2 and groups[2].isdigit():
                        metadata['year'] = groups[2]
            break
    
    return metadata

def detect_framework_structure(all_scores: List[Dict[str, float]]) -> Dict[str, Any]:
    """Auto-detect framework structure from score data"""
    if not all_scores:
        return {}
    
    # Get all unique wells
    all_wells = sorted(set().union(*all_scores))
    
    # Framework detection heuristics
    framework_info = {
        'wells': all_wells,
        'total_wells': len(all_wells),
        'framework_type': 'unknown'
    }
    
    # Common framework patterns
    civic_virtue_wells = {'dignity', 'truth', 'hope', 'justice', 'pragmatism', 
                         'tribalism', 'manipulation', 'fantasy', 'resentment', 'fear'}
    
    if civic_virtue_wells.issubset({w.lower() for w in all_wells}):
        framework_info['framework_type'] = 'civic_virtue'
        framework_info['integrative_wells'] = ['Dignity', 'Truth', 'Hope', 'Justice', 'Pragmatism']
        framework_info['disintegrative_wells'] = ['Tribalism', 'Manipulation', 'Fantasy', 'Resentment', 'Fear']
    else:
        # Generic categorization - assume first half integrative, second half disintegrative
        mid_point = len(all_wells) // 2
        framework_info['integrative_wells'] = all_wells[:mid_point + len(all_wells) % 2]
        framework_info['disintegrative_wells'] = all_wells[mid_point + len(all_wells) % 2:]
    
    return framework_info

def load_and_process_data(results_file: str) -> Optional[Tuple]:
    """Load the multi-run data and calculate mean scores and narrative centers"""
    try:
        with open(results_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Results file not found: {results_file}")
        return None
    
    # Extract scores and analyses from all runs
    all_scores = []
    all_analyses = []
    narrative_centers = []
    
    # Initialize visualizer to calculate narrative centers
    visualizer = NarrativeGravityWellsCircular()
    
    for run in data['individual_runs']:
        if run['success']:
            # Handle both raw_response format and direct result format
            if 'raw_response' in run['result']:
                raw_response = run['result']['raw_response']
                scores = extract_scores_from_raw_response(raw_response)
                analysis = extract_analysis_from_raw_response(raw_response)
            else:
                # Direct format - scores and analysis are directly in result
                scores = run['result'].get('scores', {})
                analysis = run['result'].get('analysis', '')
            
            if scores:
                all_scores.append(scores)
                all_analyses.append(analysis)
                
                # Calculate narrative center for this run
                narrative_x, narrative_y = visualizer.calculate_narrative_position(scores)
                narrative_centers.append({'x': narrative_x, 'y': narrative_y})
    
    if not all_scores:
        print("❌ No scores found")
        return None
    
    # Auto-detect framework structure
    framework_info = detect_framework_structure(all_scores)
    
    # Calculate mean scores and statistics
    wells = sorted(set().union(*all_scores))
    mean_scores = {}
    well_stats = {}
    
    for well in wells:
        values = [scores.get(well, 0) for scores in all_scores]
        mean_scores[well] = np.mean(values)
        well_stats[well] = {
            'mean': np.mean(values),
            'std': np.std(values),
            'variance': np.var(values),
            'values': values
        }
    
    # Calculate narrative center statistics
    narrative_x_values = [center['x'] for center in narrative_centers]
    narrative_y_values = [center['y'] for center in narrative_centers]
    
    narrative_stats = {
        'x': {
            'mean': np.mean(narrative_x_values),
            'std': np.std(narrative_x_values),
            'values': narrative_x_values
        },
        'y': {
            'mean': np.mean(narrative_y_values),
            'std': np.std(narrative_y_values),
            'values': narrative_y_values
        }
    }
    
    return mean_scores, well_stats, narrative_stats, all_analyses, data, framework_info

def generate_composite_summary(all_analyses: List[str], speaker: str, speech_type: str, framework: str) -> str:
    """Generate composite summary - NO API VERSION for testing"""
    # Return simple placeholder instead of calling LLM
    return f"Meta-analysis reveals consistent {framework.lower()} narrative patterns across all {len(all_analyses)} runs. Strong gravitational pulls toward specific wells demonstrate clear rhetorical strategy throughout {speaker}'s {speech_type}."

def generate_variance_analysis_with_house_llm(mean_scores: Dict[str, float], well_stats: Dict[str, Dict], 
                              narrative_stats: Dict, framework_info: Dict[str, Any], 
                              run_count: int) -> str:
    """Generate variance analysis - NO API VERSION for testing"""
    # Calculate variance stats
    wells = list(well_stats.keys())
    variances = [well_stats[well]['std'] for well in wells]
    total_variance = sum(variances)
    max_individual_variance = max(variances) if variances else 0
    
    # Generate simple analysis based on variance patterns
    if total_variance == 0:
        return "Perfect consistency detected across all runs with zero variance in scoring patterns."
    elif total_variance < 0.05:
        return "Near-perfect consistency with minimal variance detected. Analysis demonstrates remarkable scoring stability across multiple runs."
    elif max_individual_variance < 0.02:
        return f"Low variance analysis shows consistent patterns across {run_count} runs. Total variance of {total_variance:.3f} indicates stable measurement with minor fluctuations in scoring."
    else:
        # Find wells with highest variance for detailed analysis
        high_variance_wells = [well for well in wells if well_stats[well]['std'] > 0.1]
        
        analysis_parts = [
            f"Variance analysis across {run_count} runs reveals systematic patterns.",
            f"Total variance: {total_variance:.3f}, maximum individual variance: {max_individual_variance:.3f}."
        ]
        
        if high_variance_wells:
            analysis_parts.append(f"Elevated variance detected in: {', '.join(high_variance_wells)}.")
        
        analysis_parts.append("Statistical examination demonstrates methodological consistency while capturing natural measurement variation in complex narrative analysis.")
        
        return " ".join(analysis_parts)

def create_analysis_data_for_visualization(mean_scores: Dict[str, float], framework_info: Dict[str, Any], metadata: Dict[str, str]) -> Dict:
    """Create data structure for centralized visualization system (NO API VERSION)."""
    
    # Convert mean scores to wells format expected by visualization engine
    wells = {}
    for well_name, score in mean_scores.items():
        # Assign angle based on well position (evenly distribute)
        well_index = list(mean_scores.keys()).index(well_name)
        angle = (well_index * 360 / len(mean_scores)) % 360
        
        # Determine well type from framework info
        well_type = 'integrative'
        if well_name in framework_info.get('disintegrative_wells', []):
            well_type = 'disintegrative'
        elif well_name in framework_info.get('integrative_wells', []):
            well_type = 'integrative'
        
        wells[well_name] = {
            'angle': angle,
            'type': well_type,
            'weight': 1.0
        }
    
    return {
        'title': f"{metadata.get('speaker', 'Unknown')} - {metadata.get('framework', 'Analysis')} (NO API)",
        'wells': wells,
        'scores': mean_scores,
        'metadata': metadata
    }

def create_dashboard(results_file: str, speaker: str = None, year: str = None, 
                    speech_type: str = None, framework: str = None) -> Optional[str]:
    """Create a generalized multi-run analysis dashboard"""
    
    start_time = time.time()
    
    print("🔄 Loading multi-run data...")
    data_result = load_and_process_data(results_file)
    if not data_result:
        return None
    
    mean_scores, well_stats, narrative_stats, all_analyses, raw_data, framework_info = data_result
    
    # Auto-extract metadata from filename if not provided
    filename_metadata = parse_filename_metadata(results_file)
    
    # Use provided parameters or fallback to auto-detection or defaults
    speaker = speaker or filename_metadata.get('speaker', 'Unknown Speaker')
    year = year or filename_metadata.get('year', 'Unknown Year')
    speech_type = speech_type or 'Speech'
    framework = framework or filename_metadata.get('framework') or framework_info.get('framework_type', 'Unknown Framework').title()
    
    # Get run count and model info from data
    run_count = raw_data.get('test_metadata', {}).get('total_runs', len(raw_data.get('individual_runs', [])))
    model_name = raw_data.get('test_metadata', {}).get('model', 'Claude 3.5 Sonnet').title()
    
    print(f"🎨 Creating NO API dashboard for {speaker} {year} {speech_type} ({framework})...")
    
    # Create centralized visualization using new engine (NO API VERSION)
    print("   📊 Generating centralized visualization...")
    
    try:
        # Create visualization engine with presentation theme for dashboard
        engine = create_visualization_engine(theme='presentation')
        
        # Prepare analysis data for visualization
        metadata = {
            'speaker': speaker,
            'year': year, 
            'framework': framework,
            'speech_type': speech_type
        }
        
        analysis_data = create_analysis_data_for_visualization(mean_scores, framework_info, metadata)
        
        # Create single analysis visualization
        viz_fig = engine.create_single_analysis(
            wells=analysis_data['wells'],
            scores=analysis_data['scores'],
            title=f'{framework} Analysis (NO API)\n{speaker} {year} ({run_count} runs)',
            include_center=True,
            show_variance=True,
            variance_data=narrative_stats if narrative_stats else None
        )
        
        # Save the visualization as HTML and PNG
        output_path = Path(results_file).parent / f"no_api_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        viz_fig.write_html(f"{output_path}.html")
        viz_fig.write_image(f"{output_path}.png", width=800, height=800, scale=2)
        
        print(f"   ✅ NO API Interactive visualization saved: {output_path}.html")
        print(f"   ✅ NO API Static visualization saved: {output_path}.png")
        
        # NO API VERSION: Summary generation without LLM calls
        print("   📝 Generating simple summaries (no API)...")
        composite_summary = generate_composite_summary(all_analyses, speaker, speech_type, framework)
        variance_analysis = generate_variance_analysis_with_house_llm(mean_scores, well_stats, narrative_stats, framework_info, run_count)
        
        print(f"   ✅ Composite Summary: {composite_summary[:50]}...")
        print(f"   ✅ Variance Analysis: {variance_analysis[:50]}...")
        print("   📊 Professional NO API dashboard completed!")
        
        # Return the HTML path for display
        return f"{output_path}.html"
        
    except Exception as e:
        print(f"   ⚠️ Error creating centralized visualization: {e}")
        return None
    

def main():
    """Main function to demonstrate NO API dashboard usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate Multi-Run Narrative Gravity Analysis Dashboard (NO API VERSION)')
    parser.add_argument('results_file', help='Path to the multi-run results JSON file')
    parser.add_argument('--speaker', help='Speaker name (auto-detected if not provided)')
    parser.add_argument('--year', help='Year of speech (auto-detected if not provided)')
    parser.add_argument('--speech-type', help='Type of speech (default: Speech)')
    parser.add_argument('--framework', help='Analysis framework (auto-detected if not provided)')
    
    args = parser.parse_args()
    
    print("🎨 Creating NO API Multi-Run Analysis Dashboard...")
    print("   (Testing version with centralized visualization system)")
    
    dashboard_path = create_dashboard(
        results_file=args.results_file,
        speaker=args.speaker,
        year=args.year,
        speech_type=args.speech_type,
        framework=args.framework
    )
    
    if dashboard_path:
        print(f"✅ NO API Dashboard created: {dashboard_path}")
        print(f"📊 Features: Centralized visualization, no API calls, professional theming")
        print(f"🎯 Perfect for testing and offline analysis")
    else:
        print("❌ Failed to create NO API dashboard")

if __name__ == "__main__":
    main()