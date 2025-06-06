#!/usr/bin/env python3
"""
Create Obama Elliptical + Enhanced Bar Chart Dashboard V5
Fixed sizing and proportions with better layout
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime
import textwrap

# Import the elliptical visualization system
import sys
sys.path.append('.')
from narrative_gravity_elliptical import NarrativeGravityWellsElliptical
from src.api_clients.direct_api_client import DirectAPIClient

def extract_scores_from_raw_response(raw_response):
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

def extract_analysis_from_raw_response(raw_response):
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

def load_and_process_data():
    """Load the multi-run data and calculate mean scores and narrative centers"""
    results_file = "test_results/obama_multi_run_civic_virtue_20250606_142731.json"
    
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
    
    return mean_scores, well_stats, narrative_stats, all_analyses, data

def generate_composite_summary(all_analyses):
    """Generate a concise composite summary from all individual analyses"""
    
    print("🤖 Generating composite summary...")
    
    # Combine all analyses
    combined_text = "\n\n".join([f"Run {i+1}: {analysis}" for i, analysis in enumerate(all_analyses) if analysis])
    
    prompt = f"""Based on these 5 separate analyses of Obama's inaugural speech, create a concise composite summary that synthesizes the key findings. 

Individual Analyses:
{combined_text}

Please provide a brief composite summary (2-3 sentences maximum) that captures the most consistent themes across all analyses regarding Obama's narrative gravity profile."""

    try:
        api_client = DirectAPIClient()
        result, cost = api_client.analyze_text(
            text=prompt,
            framework="civic_virtue",
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

def generate_takeaways(mean_scores, well_stats, narrative_stats):
    """Generate concise takeaways and discussion of results"""
    
    print("🤖 Generating takeaways discussion...")
    
    # Create a summary of the statistical results
    integrative_avg = np.mean([well_stats[well]['mean'] for well in ['Dignity', 'Truth', 'Hope', 'Justice', 'Pragmatism'] if well in well_stats])
    disintegrative_avg = np.mean([well_stats[well]['mean'] for well in ['Tribalism', 'Manipulation', 'Fantasy', 'Resentment', 'Fear'] if well in well_stats])
    
    stats_summary = f"""Statistical Results Summary:
- 5 consecutive runs with Claude 3.5 Sonnet
- Integrative wells average: {integrative_avg:.3f}
- Disintegrative wells average: {disintegrative_avg:.3f}
- Narrative center: ({narrative_stats['x']['mean']:.3f}±{narrative_stats['x']['std']:.3f}, {narrative_stats['y']['mean']:.3f}±{narrative_stats['y']['std']:.3f})
- Most consistent wells: {', '.join([well for well, stats in well_stats.items() if stats['std'] < 0.01])}"""

    prompt = f"""Based on this multi-run analysis of Obama's inaugural speech using the civic virtue framework, provide 3-4 key takeaways.

{stats_summary}

Please provide:
1. What the consistency across runs reveals
2. What Obama's civic virtue profile shows
3. The significance of the narrative center position
4. One key implication

Keep response under 120 words total."""

    try:
        api_client = DirectAPIClient()
        result, cost = api_client.analyze_text(
            text=prompt,
            framework="civic_virtue",
            model_name="claude-3.5-sonnet"
        )
        
        if result and 'error' not in result:
            # Extract the analysis text
            if isinstance(result, dict):
                return result.get('analysis', result.get('raw_response', 'Takeaways generation failed.'))
            else:
                return str(result)
        else:
            return "Unable to generate takeaways discussion."
            
    except Exception as e:
        print(f"Error generating takeaways: {e}")
        return "Error generating takeaways discussion."

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

def create_dashboard_visualization():
    """Create the properly sized dashboard with charts and LLM-generated insights"""
    
    print("🔄 Loading multi-run data...")
    data_result = load_and_process_data()
    if not data_result:
        return
    
    mean_scores, well_stats, narrative_stats, all_analyses, raw_data = data_result
    
    print("🎨 Creating dashboard visualization...")
    
    # Create better proportioned figure (20x12 instead of 20x14)
    fig = plt.figure(figsize=(20, 12))
    
    # Use GridSpec for better control
    from matplotlib.gridspec import GridSpec
    gs = GridSpec(5, 2, figure=fig, height_ratios=[0.5, 2, 2, 0.3, 1.2], hspace=0.3, wspace=0.2)
    
    # Create the elliptical subplot (left) - larger size
    print("   📊 Generating elliptical visualization...")
    ax1 = fig.add_subplot(gs[1:3, 0])
    
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
        ax1.set_title('Civic Virtue Elliptical Map\nMean Scores Across 5 Runs', 
                      fontsize=16, fontweight='bold', pad=20)
        
        # Ensure equal aspect ratio for ellipse
        ax1.set_aspect('equal')
        ax1.set_xlim(-1.2, 1.2)
        ax1.set_ylim(-1.2, 1.2)
        
    except Exception as e:
        print(f"   ⚠️ Error creating elliptical plot: {e}")
    
    # Create the enhanced bar chart (right) - larger size
    print("   📊 Generating enhanced bar chart...")
    ax2 = fig.add_subplot(gs[1:3, 1])
    
    # Categorize wells
    integrative_wells = ['Dignity', 'Truth', 'Hope', 'Justice', 'Pragmatism']
    disintegrative_wells = ['Tribalism', 'Manipulation', 'Fantasy', 'Resentment', 'Fear']
    
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
    ax2.axvline(x=len(integrative_wells) + 0.25, color='gray', linestyle='--', alpha=0.5)
    
    # Generate LLM content for bottom panels
    print("   🤖 Generating composite summary...")
    composite_summary = generate_composite_summary(all_analyses)
    
    print("   🤖 Generating takeaways discussion...")
    takeaways = generate_takeaways(mean_scores, well_stats, narrative_stats)
    
    # Add bottom panels with LLM-generated content - better sized
    print("   📝 Adding summary and takeaways panels...")
    
    # Left bottom panel - Composite Summary
    ax3 = fig.add_subplot(gs[4, 0])
    ax3.axis('off')
    
    # Better text formatting
    ax3.text(0.02, 0.95, "COMPOSITE SUMMARY", 
             fontsize=14, fontweight='bold', color='darkblue',
             transform=ax3.transAxes, va='top')
    
    # Wrap text better and use smaller font
    wrapped_summary = textwrap.fill(composite_summary, width=60)
    ax3.text(0.02, 0.75, wrapped_summary, 
             fontsize=11, transform=ax3.transAxes, 
             va='top', wrap=True, color='black')
    
    # Add border
    for spine in ax3.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(2)
        spine.set_edgecolor('blue')
    
    # Right bottom panel - Takeaways
    ax4 = fig.add_subplot(gs[4, 1])
    ax4.axis('off')
    
    # Better text formatting
    ax4.text(0.02, 0.95, "KEY TAKEAWAYS & DISCUSSION", 
             fontsize=14, fontweight='bold', color='darkgreen',
             transform=ax4.transAxes, va='top')
    
    # Wrap text better and use smaller font
    wrapped_takeaways = textwrap.fill(takeaways, width=60)
    ax4.text(0.02, 0.75, wrapped_takeaways, 
             fontsize=11, transform=ax4.transAxes, 
             va='top', wrap=True, color='black')
    
    # Add border
    for spine in ax4.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(2)
        spine.set_edgecolor('green')
    
    # Add main title at the top
    fig.suptitle('Obama Inaugural Speech - Multi-Run Civic Virtue Analysis Dashboard\nClaude 3.5 Sonnet (5 runs)', 
                 fontsize=18, fontweight='bold', y=0.95)
    
    return fig

def main():
    """Generate the properly sized dashboard visualization"""
    print("🎨 Creating Obama Multi-Run Analysis Dashboard V5...")
    
    fig = create_dashboard_visualization()
    if not fig:
        return
    
    # Save the visualization
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test_results/obama_dashboard_v5_{timestamp}.png"
    
    fig.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    
    print(f"✅ Dashboard V5 saved: {filename}")
    print(f"📊 Features: Fixed sizing and proportions")
    print(f"🎯 Improvements: Better layout, larger charts, concise text")

if __name__ == "__main__":
    main() 