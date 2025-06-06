#!/usr/bin/env python3
"""
Create Obama Elliptical + Enhanced Bar Chart Visualization V3
Left: Elliptical visualization with mean scores + narrative center variance
Right: Enhanced integrative vs disintegrative bar chart (wells only)
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime

# Import the elliptical visualization system
import sys
sys.path.append('.')
from narrative_gravity_elliptical import NarrativeGravityWellsElliptical

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

def load_and_process_data():
    """Load the multi-run data and calculate mean scores and narrative centers"""
    results_file = "test_results/obama_multi_run_civic_virtue_20250606_142731.json"
    
    try:
        with open(results_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Results file not found: {results_file}")
        return None
    
    # Extract scores from all runs
    all_scores = []
    narrative_centers = []
    
    # Initialize visualizer to calculate narrative centers
    visualizer = NarrativeGravityWellsElliptical()
    
    for run in data['individual_runs']:
        if run['success']:
            raw_response = run['result']['raw_response']
            scores = extract_scores_from_raw_response(raw_response)
            if scores:
                all_scores.append(scores)
                
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
    
    return mean_scores, well_stats, narrative_stats, data

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

def create_combined_visualization():
    """Create the combined two-panel visualization with narrative center variance on ellipse"""
    
    print("🔄 Loading multi-run data...")
    data_result = load_and_process_data()
    if not data_result:
        return
    
    mean_scores, well_stats, narrative_stats, raw_data = data_result
    
    print("🎨 Creating combined visualization...")
    
    # Create the combined figure
    fig = plt.figure(figsize=(20, 10))
    
    # Create the elliptical subplot (left)
    print("   📊 Generating elliptical visualization with variance...")
    ax1 = plt.subplot(1, 2, 1)
    
    # Create elliptical visualization by formatting data properly for the visualizer
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
                      fontsize=14, fontweight='bold', pad=20)
        
        # Ensure equal aspect ratio for ellipse
        ax1.set_aspect('equal')
        ax1.set_xlim(-1.2, 1.2)
        ax1.set_ylim(-1.2, 1.2)
        
    except Exception as e:
        print(f"   ⚠️ Using simplified elliptical plot: {e}")
        # Fallback: create a simple scatter plot in elliptical format
        create_simple_elliptical_plot(ax1, mean_scores, well_stats)
    
    # Create the enhanced bar chart (right) - back to wells only
    print("   📊 Generating enhanced bar chart (wells only)...")
    ax2 = plt.subplot(1, 2, 2)
    
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
                 fontsize=10, fontweight='bold')
    
    # Add value labels for disintegrative wells
    for i, (bar, mean, std) in enumerate(zip(bars_dis, dis_means, dis_stds)):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + std + 0.02,
                 f'{mean:.3f}±{std:.3f}', ha='center', va='bottom', 
                 fontsize=10, fontweight='bold')
    
    # Customize the chart
    all_wells = integrative_wells + disintegrative_wells
    all_positions = list(x_int) + list(x_dis)
    
    ax2.set_xticks(all_positions)
    ax2.set_xticklabels(all_wells, rotation=45, ha='right', fontsize=11)
    ax2.set_ylabel('Score (0.0 - 1.0)', fontsize=12, fontweight='bold')
    ax2.set_title('Integrative vs Disintegrative Wells\nwith Confidence Intervals (±1 Standard Deviation)', 
                  fontsize=14, fontweight='bold', pad=20)
    ax2.legend(loc='upper left', fontsize=11)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 1.1)
    
    # Add dividing line between integrative and disintegrative
    ax2.axvline(x=len(integrative_wells) + 0.25, color='gray', linestyle='--', alpha=0.5)
    
    # Add main title
    fig.suptitle('Obama Inaugural Speech - Multi-Run Civic Virtue Analysis\nClaude 3.5 Sonnet (5 runs)', 
                 fontsize=16, fontweight='bold', y=0.95)
    
    # Adjust layout
    plt.tight_layout()
    plt.subplots_adjust(top=0.88)
    
    return fig

def create_simple_elliptical_plot(ax, mean_scores, well_stats):
    """Create a simplified elliptical-style plot as fallback"""
    
    # Define well positions (approximate elliptical arrangement)
    well_positions = {
        'Dignity': (0, 1),
        'Truth': (0.7, 0.7),
        'Hope': (0.9, 0.4),
        'Justice': (-0.7, 0.7),
        'Pragmatism': (-0.9, 0.4),
        'Tribalism': (0, -1),
        'Manipulation': (-0.7, -0.7),
        'Fantasy': (-0.9, -0.4),
        'Resentment': (0.7, -0.7),
        'Fear': (0.9, -0.4)
    }
    
    # Draw ellipse outline
    theta = np.linspace(0, 2*np.pi, 100)
    x_ellipse = np.cos(theta)
    y_ellipse = np.sin(theta)
    ax.plot(x_ellipse, y_ellipse, 'k--', alpha=0.3, linewidth=2)
    
    # Plot wells
    for well, score in mean_scores.items():
        if well in well_positions:
            x, y = well_positions[well]
            # Scale position by score for visual effect
            x_scaled = x * (0.3 + 0.7 * score)
            y_scaled = y * (0.3 + 0.7 * score)
            
            # Color by type
            color = '#2E8B57' if well in ['Dignity', 'Truth', 'Hope', 'Justice', 'Pragmatism'] else '#CD5C5C'
            
            # Plot point
            ax.scatter(x_scaled, y_scaled, s=500*score, c=color, alpha=0.7, edgecolor='black')
            
            # Add label
            ax.annotate(f'{well}\n{score:.3f}', (x_scaled, y_scaled), 
                       ha='center', va='center', fontsize=9, fontweight='bold')
    
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)

def main():
    """Generate the enhanced combined visualization"""
    print("🎨 Creating Obama Multi-Run Elliptical + Enhanced Bar Chart V3...")
    
    fig = create_combined_visualization()
    if not fig:
        return
    
    # Save the visualization
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test_results/obama_elliptical_enhanced_v3_{timestamp}.png"
    
    fig.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    
    print(f"✅ Enhanced V3 visualization saved: {filename}")
    print(f"📊 Left Panel: Elliptical map with mean scores + narrative center variance")
    print(f"📊 Right Panel: Enhanced bar chart (wells only)")
    print(f"🎯 Improved: Narrative center variance displayed on elliptical chart")

if __name__ == "__main__":
    main() 