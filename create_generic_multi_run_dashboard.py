#!/usr/bin/env python3
"""
Generic Multi-Run Narrative Gravity Analysis Dashboard
Generalized version that works with any framework, speaker, and text type
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime
import textwrap
import re
from typing import Dict, List, Optional, Tuple, Any

# Import the elliptical visualization system
import sys
sys.path.append('.')
from narrative_gravity_elliptical import NarrativeGravityWellsElliptical
from src.api_clients.direct_api_client import DirectAPIClient

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
    visualizer = NarrativeGravityWellsElliptical()
    
    for run in data['individual_runs']:
        if run['success']:
            raw_response = run['result']['raw_response']
            scores = extract_scores_from_raw_response(raw_response)
            analysis = extract_analysis_from_raw_response(raw_response)
            
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

Please provide a brief composite summary (2-3 sentences maximum) that captures the most consistent themes across all analyses regarding {speaker}'s narrative gravity profile in the {framework} framework."""

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
                return result.get('analysis', result.get('raw_response', 'Composite summary generation failed.'))
            else:
                return str(result)
        else:
            return "Unable to generate composite summary."
            
    except Exception as e:
        print(f"Error generating composite summary: {e}")
        return "Error generating composite summary."

def generate_variance_analysis(mean_scores: Dict[str, float], well_stats: Dict[str, Dict], 
                             narrative_stats: Dict, framework_info: Dict[str, Any], 
                             run_count: int) -> str:
    """Generate variance analysis focused purely on variance patterns"""
    
    print("🤖 Generating variance analysis...")
    
    # Get framework-specific wells
    integrative_wells = framework_info.get('integrative_wells', [])
    disintegrative_wells = framework_info.get('disintegrative_wells', [])
    
    # Get variance data for each category
    int_variances = [well_stats[well]['std'] for well in integrative_wells if well in well_stats]
    dis_variances = [well_stats[well]['std'] for well in disintegrative_wells if well in well_stats]
    
    # Calculate overall statistics
    all_variances = int_variances + dis_variances
    mean_variance = np.mean(all_variances)
    max_variance = np.max(all_variances)
    min_variance = np.min(all_variances)
    
    # Find most and least consistent wells
    most_consistent = min(well_stats.items(), key=lambda x: x[1]['std'])
    least_consistent = max(well_stats.items(), key=lambda x: x[1]['std'])
    
    # Count wells with very low variance (< 0.01)
    highly_consistent_count = sum(1 for well, stats in well_stats.items() if stats['std'] < 0.01)
    
    # Analyze relationship between mean scores and variance
    low_score_wells = [well for well, stats in well_stats.items() if stats['mean'] < 0.3]
    low_score_variances = [well_stats[well]['std'] for well in low_score_wells]
    high_score_wells = [well for well, stats in well_stats.items() if stats['mean'] > 0.7]
    high_score_variances = [well_stats[well]['std'] for well in high_score_wells]
    
    total_wells = len(well_stats)
    
    variance_summary = f"""Variance Analysis Data:
- {run_count} consecutive runs with Claude 3.5 Sonnet
- Overall variance range: {min_variance:.4f} to {max_variance:.4f}
- Mean variance across all wells: {mean_variance:.4f}
- Highly consistent wells (σ < 0.01): {highly_consistent_count}/{total_wells}
- Most consistent: {most_consistent[0]} (σ = {most_consistent[1]['std']:.4f})
- Least consistent: {least_consistent[0]} (σ = {least_consistent[1]['std']:.4f})"""

    if int_variances and dis_variances:
        variance_summary += f"""
- Integrative wells avg variance: {np.mean(int_variances):.4f}
- Disintegrative wells avg variance: {np.mean(dis_variances):.4f}"""
    
    if low_score_variances:
        variance_summary += f"""
- Low-score wells avg variance: {np.mean(low_score_variances):.4f}"""
    
    if high_score_variances:
        variance_summary += f"""
- High-score wells avg variance: {np.mean(high_score_variances):.4f}"""

    prompt = f"""You are analyzing ONLY variance patterns in this {run_count}-run analysis. Discuss exclusively variance - no content analysis.

{variance_summary}

Focus ONLY on:
1. Which wells have highest/lowest variance and specific numbers
2. Whether lower-scoring wells show higher variance due to fewer textual incidents in the source text
3. Category-specific variance comparison if applicable
4. What variance patterns indicate about measurement reliability
5. Whether these variance levels are acceptable for conclusions

Be technical and statistical. Mention the relationship between score magnitude and variance explicitly. Under 100 words, variance analysis only."""

    try:
        api_client = DirectAPIClient()
        result, cost = api_client.analyze_text(
            text=prompt,
            framework=framework_info.get('framework_type', 'unknown'),
            model_name="claude-3.5-sonnet"
        )
        
        if result and 'error' not in result:
            # Extract the analysis text
            if isinstance(result, dict):
                return result.get('analysis', result.get('raw_response', 'Variance analysis generation failed.'))
            else:
                return str(result)
        else:
            return "Unable to generate variance analysis."
            
    except Exception as e:
        print(f"Error generating variance analysis: {e}")
        return "Error generating variance analysis."

class CustomEllipticalVisualizer(NarrativeGravityWellsElliptical):
    """Extended visualizer that can display narrative center variance"""
    
    def __init__(self, narrative_stats=None):
        super().__init__()
        self.narrative_stats = narrative_stats
    
    def plot_narrative_position_with_variance(self, well_scores: dict) -> tuple:
        """Calculate and plot the narrative position with variance information."""
        narrative_x, narrative_y = self.calculate_narrative_position(well_scores)
        
        # Plot narrative position with glow effect
        self.ax.scatter(narrative_x, narrative_y,
                       s=self.style_config['marker_sizes']['narrative'] * 1.3,
                       color='lightgray', 
                       zorder=4, alpha=0.4,
                       edgecolors='gray',
                       linewidth=1)
        
        self.ax.scatter(narrative_x, narrative_y,
                       s=self.style_config['marker_sizes']['narrative'],
                       color=self.style_config['colors']['narrative'], 
                       zorder=5, alpha=0.9,
                       edgecolors=self.style_config['colors']['narrative_edge'],
                       linewidth=3)
        
        # Add label
        self.ax.text(narrative_x, narrative_y + 0.12,
                    "Narrative Center",
                    ha='center', va='bottom',
                    color=self.style_config['colors']['text_primary'],
                    fontweight='bold', 
                    fontsize=self.style_config['font_sizes']['labels'],
                    bbox=dict(boxstyle="round,pad=0.4", 
                            facecolor='white', 
                            alpha=0.9,
                            edgecolor=self.style_config['colors']['narrative'],
                            linewidth=2))
        
        # Add coordinates with variance if available
        if self.narrative_stats:
            x_mean = self.narrative_stats['x']['mean']
            x_std = self.narrative_stats['x']['std']
            y_mean = self.narrative_stats['y']['mean']
            y_std = self.narrative_stats['y']['std']
            
            coord_text = f"({x_mean:.3f}±{x_std:.3f}, {y_mean:.3f}±{y_std:.3f})"
            self.ax.text(narrative_x, narrative_y - 0.12,
                        coord_text,
                        ha='center', va='top',
                        color=self.style_config['colors']['text_secondary'],
                        fontsize=self.style_config['font_sizes']['coordinates'],
                        fontweight='bold',
                        bbox=dict(boxstyle="round,pad=0.3", 
                                facecolor='lightyellow', 
                                alpha=0.8,
                                edgecolor='orange',
                                linewidth=1))
        else:
            # Fallback to regular coordinates
            self.ax.text(narrative_x, narrative_y - 0.12,
                        f"({narrative_x:.2f}, {narrative_y:.2f})",
                        ha='center', va='top',
                        color=self.style_config['colors']['text_secondary'],
                        fontsize=self.style_config['font_sizes']['coordinates'],
                        alpha=0.8)
        
        return narrative_x, narrative_y

def create_dashboard(results_file: str, speaker: str = None, year: str = None, 
                    speech_type: str = None, framework: str = None) -> Optional[plt.Figure]:
    """Create a generalized multi-run analysis dashboard"""
    
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
                  height_ratios=[0.5, 2, 2, 0.15, 0.9, 0.15, 0.2],
                  width_ratios=[0.4, 1.6, 2.2, 0.2],
                  hspace=0.2, wspace=0.15)
    
    # Create the elliptical subplot (left)
    print("   📊 Generating elliptical visualization...")
    ax1 = fig.add_subplot(gs[1:3, 1])
    
    # Create elliptical visualization
    try:
        visualizer = CustomEllipticalVisualizer(narrative_stats)
        
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
        
        # Create the elliptical components manually
        visualizer.plot_ellipse_boundary()
        well_scores = visualizer.plot_wells_and_scores(wells_list, include_scores=True)
        narrative_x, narrative_y = visualizer.plot_narrative_position_with_variance(well_scores)
        
        # Add title to this subplot
        ax1.set_title(f'{framework} Elliptical Map\nMean Scores Across {run_count} Runs', 
                      fontsize=16, fontweight='bold', pad=20)
        
        # Ensure equal aspect ratio for ellipse
        ax1.set_aspect('equal')
        ax1.set_xlim(-1.2, 1.2)
        ax1.set_ylim(-1.2, 1.2)
        
    except Exception as e:
        print(f"   ⚠️ Error creating elliptical plot: {e}")
    
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
    variance_analysis = generate_variance_analysis(mean_scores, well_stats, narrative_stats, framework_info, run_count)
    
    # Add narrative panels
    print("   📝 Adding summary and variance analysis panels...")
    
    # Left panel - Composite Summary (aligned with ellipse)
    ax3 = fig.add_subplot(gs[4, 1])
    ax3.axis('off')
    
    # Better text formatting
    ax3.text(0.02, 0.95, "COMPOSITE SUMMARY", 
             fontsize=14, fontweight='bold', color='darkblue',
             transform=ax3.transAxes, va='top')
    
    # Wrap text with expanded width
    wrapped_summary = textwrap.fill(composite_summary, width=66)
    ax3.text(0.02, 0.75, wrapped_summary, 
             fontsize=11, transform=ax3.transAxes, 
             va='top', wrap=True, color='black')
    
    # Add border
    for spine in ax3.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(2)
        spine.set_edgecolor('blue')
    
    # Right panel - Variance Analysis
    ax4 = fig.add_subplot(gs[4, 2])
    ax4.axis('off')
    
    # Better text formatting
    ax4.text(0.02, 0.95, "VARIANCE ANALYSIS", 
             fontsize=14, fontweight='bold', color='darkred',
             transform=ax4.transAxes, va='top')
    
    # Wrap text with appropriate width
    wrapped_variance = textwrap.fill(variance_analysis, width=85)
    ax4.text(0.02, 0.75, wrapped_variance, 
             fontsize=11, transform=ax4.transAxes, 
             va='top', wrap=True, color='black')
    
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
    
    return fig

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
        filename = f"test_results/generic_dashboard_{base_name}_{timestamp}.png"
    
    # Ensure output directory exists
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    
    fig.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    
    print(f"✅ Generic Dashboard saved: {filename}")
    print(f"📊 Features: Auto-detection, framework-agnostic, parameter-driven")

if __name__ == "__main__":
    main()