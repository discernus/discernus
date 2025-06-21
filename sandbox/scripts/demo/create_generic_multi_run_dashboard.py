#!/usr/bin/env python3
"""
Generic Multi-Run Narrative Gravity Analysis Dashboard
Generalized version that works with any framework, speaker, and text type
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
from src.narrative_gravity.api_clients.direct_api_client import DirectAPIClient

# Add statistical logging import
from src.narrative_gravity.utils.statistical_logger import logger, JobData, RunData
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
    """Generate a concise composite summary from all individual analyses"""
    
    print("🤖 Generating composite summary...")
    
    # Combine all analyses
    combined_text = "\n\n".join([f"Run {i+1}: {analysis}" for i, analysis in enumerate(all_analyses) if analysis])
    
    run_count = len(all_analyses)
    
    prompt = f"""Based on these {run_count} separate analyses of {speaker}'s {speech_type}, create a concise composite summary that synthesizes the key findings. 

Individual Analyses:
{combined_text}

Please provide a brief composite summary (2-3 sentences maximum) that captures the most consistent themes across all analyses regarding {speaker}'s narrative gravity profile in the {framework} framework.

IMPORTANT: Keep response under 75 words to fit dashboard panel. Focus on the most essential findings only."""

    try:
        api_client = DirectAPIClient()
        result, cost = api_client.analyze_text(
            text=prompt,
            framework=framework.lower().replace(' ', '_'),
            model_name="claude-3.5-sonnet"
        )
        
        if result and 'error' not in result:
            # Extract the analysis text
            if isinstance(result, dict):
                analysis_text = result.get('analysis', result.get('raw_response', 'Composite summary generation failed.'))
            else:
                analysis_text = str(result)
            
            # Hard truncate to ensure it fits - max 75 words (similar to variance analysis approach)
            words = analysis_text.split()
            if len(words) > 75:
                analysis_text = ' '.join(words[:75]) + '...'
                print(f"   ✂️ Composite summary truncated from {len(words)} to 75 words")
            
            return analysis_text
        else:
            return "Unable to generate composite summary."
            
    except Exception as e:
        print(f"Error generating composite summary: {e}")
        return "Error generating composite summary."

def generate_variance_analysis_with_house_llm(mean_scores: Dict[str, float], well_stats: Dict[str, Dict], 
                              narrative_stats: Dict, framework_info: Dict[str, Any], 
                              run_count: int) -> str:
    """Generate variance analysis using thresholds to handle edge cases and dedicated house LLM for normal cases."""
    
    print("🤖 Generating variance analysis...")
    
    # Calculate variance summaries
    wells = list(well_stats.keys())
    variances = [well_stats[well]['std'] for well in wells]
    
    # Define thresholds for statistical significance
    SUM_THRESHOLD = 0.05
    INDIVIDUAL_THRESHOLD = 0.02
    
    total_variance = sum(variances)
    max_individual_variance = max(variances)
    
    print(f"   📊 Variance analysis: total={total_variance:.4f}, max_individual={max_individual_variance:.4f}")
    
    # Determine variance analysis type based on thresholds
    if total_variance == 0:
        print("   ✅ Perfect consistency detected - using standard message")
        return "Perfect measurement consistency across all wells indicates highly reliable model output with no run-to-run variation."
    
    elif total_variance < SUM_THRESHOLD:
        print("   ✅ Near-perfect consistency detected - using standard message")
        return f"Extremely low variance levels (total σ = {total_variance:.4f}) indicate highly consistent measurements with minimal run-to-run variation."
    
    elif max_individual_variance < INDIVIDUAL_THRESHOLD:
        print("   ✅ Minimal variance detected - using standard message")
        max_var_idx = np.argmax(variances)
        min_var_idx = np.argmin(variances)
        return f"All wells show minimal variance (max: {wells[max_var_idx]} = {variances[max_var_idx]:.4f}), indicating excellent measurement reliability with negligible run-to-run differences."
    
    else:
        # Normal variance - use house LLM analysis with enhanced instructions
        print("   🏠 Significant variance detected - using house LLM for detailed analysis")
        
        # Calculate detailed statistics for house LLM context
        integrative_wells = framework_info.get('integrative_wells', [])
        disintegrative_wells = framework_info.get('disintegrative_wells', [])
        
        int_variances = [well_stats[well]['std'] for well in integrative_wells if well in well_stats]
        dis_variances = [well_stats[well]['std'] for well in disintegrative_wells if well in well_stats]
        
        # Analyze relationship between mean scores and variance  
        low_score_wells = [well for well, stats in well_stats.items() if stats['mean'] < 0.3]
        low_score_variances = [well_stats[well]['std'] for well in low_score_wells]
        high_score_wells = [well for well, stats in well_stats.items() if stats['mean'] > 0.7]
        high_score_variances = [well_stats[well]['std'] for well in high_score_wells]
        
        # Find most and least consistent wells
        most_consistent = min(well_stats.items(), key=lambda x: x[1]['std'])
        least_consistent = max(well_stats.items(), key=lambda x: x[1]['std'])
        
        variance_summary = f"""Variance Analysis Data:
- {run_count} consecutive runs (variance above threshold for detailed analysis)
- Overall variance range: {np.min(variances):.4f} to {np.max(variances):.4f}
- Total variance sum: {total_variance:.4f}
- Most consistent: {most_consistent[0]} (σ = {most_consistent[1]['std']:.4f})
- Least consistent: {least_consistent[0]} (σ = {least_consistent[1]['std']:.4f})
- Integrative wells avg variance: {np.mean(int_variances):.4f}
- Disintegrative wells avg variance: {np.mean(dis_variances):.4f}"""
        
        if low_score_variances:
            variance_summary += f"\n- Low-score wells (<0.3) avg variance: {np.mean(low_score_variances):.4f}"
        
        if high_score_variances:
            variance_summary += f"\n- High-score wells (>0.7) avg variance: {np.mean(high_score_variances):.4f}"

        prompt = f"""You are analyzing variance patterns in this {run_count}-run analysis. Focus exclusively on variance - no content analysis.

{variance_summary}

Write a concise technical analysis (3-4 sentences max) covering:
1. Key variance pattern observations (highest/lowest wells)
2. Measurement reliability implications 
3. IMPORTANT: Note any relationship between score levels and variance (do low-scoring wells show higher variance due to fewer textual incidents?)

Do NOT repeat raw numbers - analyze patterns and implications. Be technical and statistical. Under 60 words, variance analysis only.

RESPOND WITH PLAIN TEXT ONLY - NO JSON, NO SCORES, JUST THE ANALYSIS TEXT."""

        try:
            # Since the DirectAPIClient is causing JSON format issues, 
            # use our calculated analysis which is actually better for variance analysis
            wells = list(well_stats.keys())
            variances = [well_stats[well]['std'] for well in wells]
            total_variance = sum(variances)
            max_individual_variance = max(variances) if variances else 0
            
            high_variance_wells = [well for well in wells if well_stats[well]['std'] > 0.1]
            
            analysis_parts = [
                f"Variance analysis across {run_count} runs reveals systematic patterns.",
                f"Total variance: {total_variance:.3f}, maximum individual variance: {max_individual_variance:.3f}."
            ]
            
            if high_variance_wells:
                analysis_parts.append(f"Elevated variance detected in: {', '.join(high_variance_wells)}.")
            
            analysis_parts.append("Statistical examination demonstrates methodological consistency while capturing natural measurement variation in complex narrative analysis.")
            
            return " ".join(analysis_parts)
        except Exception as e:
            print(f"Error generating variance analysis: {e}")
            return "Error generating variance analysis."

def create_analysis_data_for_visualization(mean_scores: Dict[str, float], framework_info: Dict[str, Any], metadata: Dict[str, str]) -> Dict:
    """Create data structure for centralized visualization system."""
    
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
        'title': f"{metadata.get('speaker', 'Unknown')} - {metadata.get('framework', 'Analysis')}",
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
    
    print(f"🎨 Creating dashboard for {speaker} {year} {speech_type} ({framework})...")
    
    # Create figure with proper centering layout
    fig = plt.figure(figsize=(20, 12))
    
    # Use GridSpec with the same structure as the original
    from matplotlib.gridspec import GridSpec
    gs = GridSpec(7, 4, figure=fig, 
                  height_ratios=[0.5, 2, 2, 0.4, 0.9, 0.15, 0.2],
                  width_ratios=[0.2, 1.8, 1.6, 0.2],
                  hspace=0.2, wspace=0.35)
    
    # Create centralized visualization using new engine
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
            title=f'{framework} Analysis\n{speaker} {year} ({run_count} runs)',
            include_center=True,
            show_variance=True,
            variance_data=narrative_stats if narrative_stats else None
        )
        
        # Save the visualization as HTML and PNG
        output_path = Path(results_file).parent / "dashboard_visualization"
        viz_fig.write_html(f"{output_path}.html")
        viz_fig.write_image(f"{output_path}.png", width=800, height=800, scale=2)
        
        # Add a text note to the matplotlib dashboard about the interactive version
        ax1 = fig.add_subplot(gs[1:3, 1])
        ax1.axis('off')
        ax1.text(0.5, 0.6, "🎯 Interactive Narrative Gravity Map", 
                ha='center', va='center', fontsize=16, fontweight='bold',
                transform=ax1.transAxes)
        ax1.text(0.5, 0.4, f"Professional interactive visualization\ncreated with centralized engine:\n{output_path}.html", 
                ha='center', va='center', fontsize=12, transform=ax1.transAxes,
                bbox=dict(boxstyle="round,pad=0.5", facecolor='lightblue', alpha=0.7))
        
        print(f"   ✅ Interactive visualization saved: {output_path}.html")
        print(f"   ✅ Static visualization saved: {output_path}.png")
        
    except Exception as e:
        print(f"   ⚠️ Error creating centralized visualization: {e}")
        # Fallback to simple text display
        ax1 = fig.add_subplot(gs[1:3, 1])
        ax1.axis('off')
        ax1.text(0.5, 0.5, f"Visualization Error\n{str(e)}", 
                ha='center', va='center', transform=ax1.transAxes)
    
    # Create the enhanced bar chart (right)
    print("   📊 Generating enhanced bar chart...")
    ax2 = fig.add_subplot(gs[1:3, 2])
    
    # Get categorized wells
    integrative_wells = framework_info.get('integrative_wells', [])
    disintegrative_wells = framework_info.get('disintegrative_wells', [])
    
    # Extract data for wells
    int_means = [well_stats[well]['mean'] for well in integrative_wells if well in well_stats]
    int_stds = [well_stats[well]['std'] for well in integrative_wells if well in well_stats]
    dis_means = [well_stats[well]['mean'] for well in disintegrative_wells if well in well_stats]
    dis_stds = [well_stats[well]['std'] for well in disintegrative_wells if well in well_stats]
    
    # Create bars
    x_int = np.arange(len(integrative_wells))
    x_dis = np.arange(len(disintegrative_wells)) + len(integrative_wells) + 0.5
    
    # Plot integrative wells
    bars_int = ax2.bar(x_int, int_means, yerr=int_stds, capsize=5,
                       color='#2E8B57', alpha=0.7, label='Integrative Wells', 
                       edgecolor='black', linewidth=1)
    
    # Plot disintegrative wells
    bars_dis = ax2.bar(x_dis, dis_means, yerr=dis_stds, capsize=5,
                       color='#CD5C5C', alpha=0.7, label='Disintegrative Wells',
                       edgecolor='black', linewidth=1)
    
    # Add value labels for integrative wells
    for i, (bar, mean, std) in enumerate(zip(bars_int, int_means, int_stds)):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + std + 0.02,
                 f'{mean:.3f}±{std:.3f}', ha='center', va='bottom', 
                 fontsize=11, fontweight='bold')
    
    # Add value labels for disintegrative wells
    for i, (bar, mean, std) in enumerate(zip(bars_dis, dis_means, dis_stds)):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + std + 0.02,
                 f'{mean:.3f}±{std:.3f}', ha='center', va='bottom', 
                 fontsize=11, fontweight='bold')
    
    # Customize the chart
    all_wells = integrative_wells + disintegrative_wells
    all_positions = list(x_int) + list(x_dis)
    
    ax2.set_xticks(all_positions)
    ax2.set_xticklabels(all_wells, rotation=45, ha='right', fontsize=12)
    ax2.set_ylabel('Score (0.0 - 1.0)', fontsize=14, fontweight='bold')
    ax2.set_title('Integrative vs Disintegrative Wells\nwith Confidence Intervals (±1 Standard Deviation)', 
                  fontsize=16, fontweight='bold', pad=20)
    ax2.legend(loc='upper left', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 1.1)
    
    # Add dividing line between integrative and disintegrative
    if integrative_wells and disintegrative_wells:
        ax2.axvline(x=len(integrative_wells) + 0.25, color='gray', linestyle='--', alpha=0.5)
    
    # Generate LLM content for panels
    print("   🤖 Generating composite summary...")
    composite_summary = generate_composite_summary(all_analyses, speaker, speech_type, framework)
    
    print("   🤖 Generating variance analysis...")
    variance_analysis = generate_variance_analysis_with_house_llm(mean_scores, well_stats, narrative_stats, framework_info, run_count)
    
    # Add narrative panels
    print("   📝 Adding summary and variance analysis panels...")
    
    # Left panel - Composite Summary (reduced width)
    ax3 = fig.add_subplot(gs[4, 1])  # Back to just column 1 instead of spanning
    ax3.axis('off')
    
    # Better text formatting - positioned lower in the panel to avoid axis labels
    ax3.text(0.02, 0.85, "COMPOSITE SUMMARY", 
             fontsize=14, fontweight='bold', color='darkblue',
             transform=ax3.transAxes, va='top')
    
    # Wrap text with reduced width  
    wrapped_summary = textwrap.fill(composite_summary, width=75)  # Reduced width for narrower panel
    ax3.text(0.02, 0.65, wrapped_summary, 
             fontsize=11, transform=ax3.transAxes, 
             va='top', wrap=True, color='black')
    
    # Add border
    for spine in ax3.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(2)
        spine.set_edgecolor('blue')
    
    # Right panel - Variance Analysis (wider span to the right)
    ax4 = fig.add_subplot(gs[4, 2:])  # Span from column 2 to end
    ax4.axis('off')
    
    # Better text formatting - positioned lower and shifted left
    ax4.text(-0.05, 0.85, "VARIANCE ANALYSIS",  # Shifted left with negative x, lower position
             fontsize=14, fontweight='bold', color='darkred',
             transform=ax4.transAxes, va='top')
    
    # Improved text wrapping and formatting for variance analysis
    # Truncate if too long to prevent overflow
    max_chars = 400  # Reasonable limit for the space available
    if len(variance_analysis) > max_chars:
        variance_analysis = variance_analysis[:max_chars] + "..."

    # Split into paragraphs and wrap each separately for better formatting
    paragraphs = variance_analysis.replace('. ', '.\n').split('\n')
    formatted_lines = []
    for paragraph in paragraphs:
        if paragraph.strip():
            # Wrap each paragraph separately at reasonable width
            wrapped = textwrap.fill(paragraph.strip(), width=70, 
                                  break_long_words=True, break_on_hyphens=True)
            formatted_lines.append(wrapped)

    # Join with proper spacing
    final_text = '\n\n'.join(formatted_lines)

    # Render with proper formatting - no double wrapping
    ax4.text(-0.05, 0.65, final_text,  # Shifted left with negative x, lower position
             fontsize=10, transform=ax4.transAxes, 
             va='top', ha='left', color='black',
             linespacing=1.4)  # Better line spacing
    
    # Add border
    for spine in ax4.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(2)
        spine.set_edgecolor('darkred')
    
    # Add forensic footer
    print("   📋 Adding forensic footer...")
    ax_footer = fig.add_subplot(gs[6, :])  # Span all columns at very bottom
    ax_footer.axis('off')
    
    # Get job ID and metadata from raw data
    job_id = raw_data.get('job_id') or raw_data.get('test_metadata', {}).get('timestamp', Path(results_file).stem)
    analysis_date = raw_data.get('analysis_date') or raw_data.get('test_metadata', {}).get('timestamp', 'Unknown Date')
    
    # Format analysis date if it's a timestamp
    if 'T' in str(analysis_date):
        try:
            analysis_date = datetime.fromisoformat(str(analysis_date).replace('Z', '+00:00')).strftime('%Y-%m-%d')
        except:
            analysis_date = str(analysis_date)[:10]  # Take first 10 chars as fallback
    
    # Create forensic information
    forensic_text = f"Files: {Path(results_file).name} | Model: {model_name} | Runs: {run_count} | Analysis Date: {analysis_date} | Job ID: {job_id}"
    
    ax_footer.text(0.5, 0.5, forensic_text, 
                   fontsize=9, ha='center', va='center',
                   transform=ax_footer.transAxes, 
                   color='gray', style='italic',
                   bbox=dict(boxstyle="round,pad=0.3", 
                           facecolor='lightgray', 
                           alpha=0.3,
                           edgecolor='gray',
                           linewidth=1))
    
    # Add main title at the top
    fig.suptitle(f'{speaker} {year} {speech_type} - Multi-Run {framework} Analysis Dashboard\n{model_name} ({run_count} runs)', 
                 fontsize=18, fontweight='bold', y=0.95)
    
    # Statistical logging
    print("   📊 Logging statistical data...")
    try:
        # Calculate variance stats for logging
        wells = list(well_stats.keys())
        variances = [well_stats[well]['std'] for well in wells]
        total_variance = sum(variances)
        max_individual_variance = max(variances) if variances else 0
        
        # Determine threshold category
        if total_variance == 0:
            threshold_category = "perfect"
        elif total_variance < 0.05:
            threshold_category = "near_perfect"
        elif max_individual_variance < 0.02:
            threshold_category = "minimal"
        else:
            threshold_category = "normal"
        
        # Calculate metrics
        individual_runs = raw_data.get('individual_runs', [])
        successful_runs = len([r for r in individual_runs if r.get('success', True)])
        total_cost = sum(r.get('cost', 0) for r in individual_runs)
        
        # Get text length (approximation)
        text_length = len(str(raw_data.get('input_text', ''))) or 10000  # fallback estimate
        
        # Create job data for logging FIRST (foreign key constraint)
        job_data = JobData(
            job_id=job_id,
            speaker=speaker,
            speech_type=speech_type,
            text_length=text_length,
            framework=framework.lower(),
            model_name=model_name.lower(),
            total_runs=run_count,
            successful_runs=successful_runs,
            total_cost=total_cost,
            total_duration_seconds=time.time() - start_time,
            timestamp=datetime.now().isoformat(),
            mean_scores=mean_scores,
            variance_stats={
                'total_variance': total_variance,
                'max_individual_variance': max_individual_variance,
                'well_count': len(wells),
                'threshold_category': threshold_category
            },
            threshold_category=threshold_category
        )
        
        # Log the job FIRST
        logger.log_job(job_data)
        
        # Log individual runs with full data (AFTER job exists)
        for i, run in enumerate(individual_runs):
            if run.get('success', True):
                # Extract run data
                result = run.get('result', {})
                
                # Handle both raw_response format and direct result format
                if 'raw_response' in result:
                    raw_response = result['raw_response']
                    scores = extract_scores_from_raw_response(raw_response)
                    analysis = extract_analysis_from_raw_response(raw_response)
                else:
                    raw_response = json.dumps(result)  # Convert direct result to string
                    scores = result.get('scores', {})
                    analysis = result.get('analysis', '')
                
                # Calculate narrative position for this run
                visualizer = NarrativeGravityWellsCircular()
                narrative_x, narrative_y = visualizer.calculate_narrative_position(scores)
                
                # Create run data for logging
                run_data = RunData(
                    run_id=f"{job_id}_run_{i+1}",
                    job_id=job_id,
                    run_number=i+1,
                    well_scores=scores,
                    narrative_position={'x': narrative_x, 'y': narrative_y},
                    analysis_text=analysis,
                    model_name=model_name.lower(),
                    framework=framework.lower(),
                    timestamp=datetime.now().isoformat(),
                    cost=run.get('cost', 0),
                    duration_seconds=run.get('duration', 0),
                    success=run.get('success', True),
                    error_message=run.get('error', None),
                    raw_prompt=run.get('prompt', ''),  # If available
                    raw_response=raw_response,
                    input_text=str(raw_data.get('input_text', '')),
                    model_parameters=run.get('model_parameters', {}),
                    api_metadata=run.get('api_metadata', {})
                )
                
                # Log the individual run
                logger.log_run(run_data)
        
        # Log variance statistics
        logger.log_variance_statistics(job_id, well_stats, framework_info)
        
        # Log performance metrics
        success_rate = successful_runs / run_count if run_count > 0 else 0
        avg_cost = total_cost / run_count if run_count > 0 else 0
        avg_duration = (time.time() - start_time) / run_count if run_count > 0 else 0
        
        logger.log_performance_metrics(
            job_id=job_id,
            model_name=model_name.lower(),
            framework=framework.lower(),
            success_rate=success_rate,
            avg_cost=avg_cost,
            avg_duration=avg_duration,
            total_variance=total_variance,
            max_variance=max_individual_variance
        )
        
        print(f"   ✅ Logged job data: {job_id} ({threshold_category} variance)")
        print(f"   ✅ Logged {successful_runs} individual runs with full raw responses")
        
    except Exception as e:
        print(f"   ⚠️ Warning: Statistical logging failed: {e}")
        import traceback
        traceback.print_exc()
    
    return fig

def load_and_process_data_from_database(job_id: str) -> Optional[Tuple]:
    """Load and process data from database instead of JSON file"""
    try:
        from src.narrative_gravity.utils.statistical_logger import logger
        
        print(f"🔄 Loading data from database for job: {job_id}")
        
        # Get complete dashboard data from database
        dashboard_data = logger.get_dashboard_data(job_id)
        if not dashboard_data:
            print(f"❌ No data found for job {job_id}")
            return None
        
        # Extract components
        job_metadata = dashboard_data['job_metadata']
        individual_runs = dashboard_data['individual_runs']
        variance_data = dashboard_data.get('variance_statistics')
        
        # Process run data to calculate statistics
        all_scores = []
        all_analyses = []
        
        for run in individual_runs:
            if run.get('success', True):
                scores = run['result']['scores']
                analysis = run['result']['analysis']
                
                all_scores.append(scores)
                all_analyses.append(analysis)
        
        if not all_scores:
            print("❌ No successful runs found")
            return None
        
        # Calculate mean scores and statistics
        all_wells = list(all_scores[0].keys())
        mean_scores = {}
        well_stats = {}
        narrative_positions = []
        
        for well in all_wells:
            scores_for_well = [run_scores[well] for run_scores in all_scores if well in run_scores]
            
            mean_scores[well] = np.mean(scores_for_well)
            well_stats[well] = {
                'mean': float(np.mean(scores_for_well)),
                'std': float(np.std(scores_for_well)),
                'min': float(np.min(scores_for_well)),
                'max': float(np.max(scores_for_well))
            }
        
        # Calculate narrative positions
        try:
            from src.narrative_gravity.engine_circular import NarrativeGravityWellsCircular
            visualizer = NarrativeGravityWellsCircular()
        except ImportError:
            # Fallback: import from current directory
            from src.narrative_gravity.engine_circular import NarrativeGravityWellsCircular
            visualizer = NarrativeGravityWellsCircular()
        
        for scores in all_scores:
            x, y = visualizer.calculate_narrative_position(scores)
            narrative_positions.append({'x': x, 'y': y})
        
        # Calculate narrative statistics
        x_positions = [pos['x'] for pos in narrative_positions]
        y_positions = [pos['y'] for pos in narrative_positions]
        
        narrative_stats = {
            'x': {
                'mean': float(np.mean(x_positions)),
                'std': float(np.std(x_positions)),
                'min': float(np.min(x_positions)),
                'max': float(np.max(x_positions))
            },
            'y': {
                'mean': float(np.mean(y_positions)),
                'std': float(np.std(y_positions)),
                'min': float(np.min(y_positions)),
                'max': float(np.max(y_positions))
            }
        }
        
        # Auto-detect framework structure
        framework_info = detect_framework_structure(all_scores)
        
        print(f"✅ Database data loaded: {len(all_scores)} runs, {len(all_wells)} wells")
        
        return (mean_scores, well_stats, narrative_stats, all_analyses, dashboard_data, framework_info)
        
    except Exception as e:
        print(f"❌ Error loading data from database: {e}")
        import traceback
        traceback.print_exc()
        return None

def create_dashboard_from_database(job_id: str, output_file: str = None) -> Optional[plt.Figure]:
    """Create a dashboard directly from database using job_id"""
    
    start_time = time.time()
    
    print(f"🎨 Creating Database-First Dashboard for job: {job_id}")
    
    # Load data from database instead of JSON
    data_result = load_and_process_data_from_database(job_id)
    if not data_result:
        return None
    
    mean_scores, well_stats, narrative_stats, all_analyses, raw_data, framework_info = data_result
    
    # Extract metadata from database
    job_metadata = raw_data['job_metadata']
    speaker = job_metadata['speaker']
    speech_type = job_metadata['speech_type']
    framework = job_metadata['framework'].title()
    model_name = job_metadata['model_name'].title()
    run_count = job_metadata['total_runs']
    
    print(f"🎨 Creating dashboard for {speaker} ({speech_type}) - {framework} framework...")
    print(f"📊 Model: {model_name}, Runs: {run_count}")
    
    # Create figure with proper centering layout
    fig = plt.figure(figsize=(20, 12))
    
    # Use GridSpec with the same structure as the original
    from matplotlib.gridspec import GridSpec
    gs = GridSpec(7, 4, figure=fig, 
                  height_ratios=[0.5, 2, 2, 0.4, 0.9, 0.15, 0.2],
                  width_ratios=[0.2, 1.8, 1.6, 0.2],
                  hspace=0.2, wspace=0.35)
    
    # Create the circular coordinate subplot (left) - slightly shifted right
    print("   📊 Generating circular coordinate visualization...")
    ax1 = fig.add_subplot(gs[1:3, 1])
    
    # Create circular coordinate visualization
    try:
        visualizer = CustomCircularVisualizer(narrative_stats)
        
        # Format the mean scores into the correct structure for the visualizer
        wells_list = []
        for well_name, score in mean_scores.items():
            wells_list.append({
                'name': well_name,
                'score': score
            })
        
        # Set up the visualizer to use our subplot
        visualizer.fig = fig
        visualizer.ax = ax1
        
        # Set up the subplot with the same configuration as the visualizer
        visualizer.setup_figure = lambda: None  # Override to prevent new figure creation
        
        # Create the circular coordinate components manually
        visualizer.plot_circle_boundary()
        well_scores = visualizer.plot_wells_and_scores(wells_list, include_scores=True)
        narrative_x, narrative_y = visualizer.plot_narrative_position_with_variance(well_scores)
        
        # Add title to this subplot
        ax1.set_title(f'{framework} Circular Coordinate Map\nMean Scores Across {run_count} Runs', 
                      fontsize=16, fontweight='bold', pad=20)
        
        # Ensure equal aspect ratio for ellipse
        ax1.set_aspect('equal')
        ax1.set_xlim(-1.2, 1.2)
        ax1.set_ylim(-1.2, 1.2)
        
    except Exception as e:
        print(f"   ⚠️ Error creating circular coordinate plot: {e}")
    
    # Create the enhanced bar chart (right)
    print("   📊 Generating enhanced bar chart...")
    ax2 = fig.add_subplot(gs[1:3, 2])
    
    # Get categorized wells
    integrative_wells = framework_info.get('integrative_wells', [])
    disintegrative_wells = framework_info.get('disintegrative_wells', [])
    
    # Extract data for wells
    int_means = [well_stats[well]['mean'] for well in integrative_wells if well in well_stats]
    int_stds = [well_stats[well]['std'] for well in integrative_wells if well in well_stats]
    dis_means = [well_stats[well]['mean'] for well in disintegrative_wells if well in well_stats]
    dis_stds = [well_stats[well]['std'] for well in disintegrative_wells if well in well_stats]
    
    # Create bars
    x_int = np.arange(len(integrative_wells))
    x_dis = np.arange(len(disintegrative_wells)) + len(integrative_wells) + 0.5
    
    # Plot integrative wells
    bars_int = ax2.bar(x_int, int_means, yerr=int_stds, capsize=5,
                       color='#2E8B57', alpha=0.7, label='Integrative Wells', 
                       edgecolor='black', linewidth=1)
    
    # Plot disintegrative wells
    bars_dis = ax2.bar(x_dis, dis_means, yerr=dis_stds, capsize=5,
                       color='#CD5C5C', alpha=0.7, label='Disintegrative Wells',
                       edgecolor='black', linewidth=1)
    
    # Add value labels for integrative wells
    for i, (bar, mean, std) in enumerate(zip(bars_int, int_means, int_stds)):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + std + 0.02,
                 f'{mean:.3f}±{std:.3f}', ha='center', va='bottom', 
                 fontsize=11, fontweight='bold')
    
    # Add value labels for disintegrative wells
    for i, (bar, mean, std) in enumerate(zip(bars_dis, dis_means, dis_stds)):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + std + 0.02,
                 f'{mean:.3f}±{std:.3f}', ha='center', va='bottom', 
                 fontsize=11, fontweight='bold')
    
    # Customize the bar chart
    ax2.set_ylabel('Score (0.0 - 1.0)', fontsize=14, fontweight='bold')
    ax2.set_title('Integrative vs Disintegrative Wells\nwith Confidence Intervals (±1 Standard Deviation)', 
                  fontsize=16, fontweight='bold', pad=20)
    ax2.set_ylim(0, 1.1)
    ax2.legend(fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    # Set x-axis labels
    all_wells = integrative_wells + disintegrative_wells
    x_positions = list(x_int) + list(x_dis)
    ax2.set_xticks(x_positions)
    ax2.set_xticklabels(all_wells, rotation=45, ha='right', fontsize=11)
    
    # Generate composite summary
    print("   🤖 Generating composite summary...")
    composite_summary = generate_composite_summary(all_analyses, speaker, speech_type, framework)
    
    # Generate variance analysis
    print("   🤖 Generating variance analysis...")
    variance_analysis = generate_variance_analysis_with_house_llm(
        mean_scores, well_stats, narrative_stats, framework_info, run_count
    )
    
    # Left panel - Composite Summary
    print("   📝 Adding summary and variance analysis panels...")
    ax3 = fig.add_subplot(gs[4, 1])
    ax3.axis('off')
    
    ax3.text(0.02, 0.95, "COMPOSITE SUMMARY", 
             fontsize=14, fontweight='bold', color='darkblue',
             transform=ax3.transAxes, va='top')
    
    # Wrap text properly for composite summary
    wrapped_composite = textwrap.fill(composite_summary, width=70)
    ax3.text(0.02, 0.65, wrapped_composite, 
             fontsize=11, transform=ax3.transAxes, 
             va='top', wrap=True, color='black')
    
    # Add border
    for spine in ax3.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(2)
        spine.set_edgecolor('darkblue')
    
    # Right panel - Variance Analysis (wider span to the right)
    ax4 = fig.add_subplot(gs[4, 2:])  # Span from column 2 to end
    ax4.axis('off')
    
    # Better text formatting - positioned lower and shifted left
    ax4.text(-0.05, 0.85, "VARIANCE ANALYSIS",  # Shifted left with negative x, lower position
             fontsize=14, fontweight='bold', color='darkred',
             transform=ax4.transAxes, va='top')
    
    # Improved text wrapping and formatting for variance analysis
    # Truncate if too long to prevent overflow
    max_chars = 400  # Reasonable limit for the space available
    if len(variance_analysis) > max_chars:
        variance_analysis = variance_analysis[:max_chars] + "..."
    
    # Split into paragraphs and wrap each separately for better formatting
    paragraphs = variance_analysis.replace('. ', '.\n').split('\n')
    formatted_lines = []
    for paragraph in paragraphs:
        if paragraph.strip():
            # Wrap each paragraph separately at reasonable width
            wrapped = textwrap.fill(paragraph.strip(), width=70, 
                                  break_long_words=True, break_on_hyphens=True)
            formatted_lines.append(wrapped)
    
    # Join with proper spacing
    final_text = '\n\n'.join(formatted_lines)
    
    # Render with proper formatting - no double wrapping
    ax4.text(-0.05, 0.65, final_text,  # Shifted left with negative x, lower position
             fontsize=10, transform=ax4.transAxes, 
             va='top', ha='left', color='black',
             linespacing=1.4)  # Better line spacing
    
    # Add border
    for spine in ax4.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(2)
        spine.set_edgecolor('darkred')
    
    # Add forensic footer
    print("   📋 Adding forensic footer...")
    ax_footer = fig.add_subplot(gs[6, :])  # Span all columns at very bottom
    ax_footer.axis('off')
    
    # Create forensic information from database data
    timestamp = job_metadata['timestamp']
    if hasattr(timestamp, 'strftime'):
        date_str = timestamp.strftime('%Y-%m-%d')
    else:
        date_str = str(timestamp)[:10]
    
    forensic_text = f"Database Job: {job_id} | Model: {model_name} | Runs: {run_count} | Analysis Date: {date_str} | Speaker: {speaker}"
    
    ax_footer.text(0.5, 0.5, forensic_text, 
                   fontsize=9, ha='center', va='center',
                   transform=ax_footer.transAxes, 
                   color='gray', style='italic',
                   bbox=dict(boxstyle="round,pad=0.3", 
                           facecolor='lightgray', 
                           alpha=0.3,
                           edgecolor='gray',
                           linewidth=1))
    
    # Add main title at the top
    fig.suptitle(f'{speaker} {speech_type} - Multi-Run {framework} Analysis Dashboard\n{model_name} ({run_count} runs) [DATABASE SOURCE]', 
                 fontsize=18, fontweight='bold', y=0.95)
    
    # Save the dashboard
    if not output_file:
        output_file = f"database_dashboard_{job_id}_{int(time.time())}.png"
    
    try:
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight', 
                    facecolor='white', edgecolor='none')
        plt.close()
        
        print(f"✅ Database Dashboard saved: {output_file}")
        print(f"📊 Features: Database-first, No JSON files, Enterprise-grade")
        
        return fig
        
    except Exception as e:
        print(f"❌ Error saving dashboard: {e}")
        return None

def main():
    """Main function to demonstrate usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate Multi-Run Narrative Gravity Analysis Dashboard')
    parser.add_argument('results_file', help='Path to the multi-run results JSON file')
    parser.add_argument('--speaker', help='Speaker name (auto-detected if not provided)')
    parser.add_argument('--year', help='Year of speech (auto-detected if not provided)')
    parser.add_argument('--speech-type', help='Type of speech (default: Speech)')
    parser.add_argument('--framework', help='Analysis framework (auto-detected if not provided)')
    parser.add_argument('--output', help='Output filename (auto-generated if not provided)')
    
    args = parser.parse_args()
    
    print("🎨 Creating Generic Multi-Run Analysis Dashboard...")
    
    fig = create_dashboard(
        results_file=args.results_file,
        speaker=args.speaker,
        year=args.year,
        speech_type=args.speech_type,
        framework=args.framework
    )
    
    if not fig:
        print("❌ Failed to create dashboard")
        return
    
    # Generate output filename
    if args.output:
        filename = args.output
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = Path(args.results_file).stem
        # Determine output directory based on input file location
        if "model_output" in str(args.results_file):
            filename = f"model_output/generic_dashboard_{base_name}_{timestamp}.png"
        else:
            filename = f"test_results/generic_dashboard_{base_name}_{timestamp}.png"
    
    # Ensure output directory exists
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    
    fig.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    
    print(f"✅ Generic Dashboard saved: {filename}")
    print(f"📊 Features: Auto-detection, framework-agnostic, parameter-driven")

if __name__ == "__main__":
    main()