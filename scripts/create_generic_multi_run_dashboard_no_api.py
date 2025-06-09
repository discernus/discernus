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
from src.narrative_gravity.engine import NarrativeGravityWellsElliptical
from src.api_clients.direct_api_client import DirectAPIClient

# Add statistical logging import
from src.utils.statistical_logger import logger, JobData, RunData
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
    visualizer = NarrativeGravityWellsElliptical()
    
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
    
    # Create the elliptical subplot (left) - slightly shifted right
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
                visualizer = NarrativeGravityWellsElliptical()
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