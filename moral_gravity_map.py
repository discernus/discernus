"""
Copyright (c) 2025 Jeff Whatcott
All rights reserved.

Moral Gravity Map Visualization Tool
This tool generates visualizations of moral gravity well analyses.
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import json
import sys
import os
import tempfile
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from textwrap import wrap
from pathlib import Path
import shutil

# Create a temporary directory for working files
TEMP_DIR = Path(tempfile.gettempdir()) / "moral_gravity_analysis"
TEMP_DIR.mkdir(exist_ok=True)

class MoralGravityMap:
    """Core class for generating moral gravity visualizations."""
    
    def __init__(self):
        self.fig = None
        self.ax = None
        self.style_config = {
            'figure_size': (12, 10),
            'main_title': "Moral Gravity Map",
            'font_sizes': {
                'title': 16,
                'subtitle': 12,
                'summary': 10
            },
            'colors': {
                'wells': 'gray',
                'scores': 'blue',
                'com': 'red'
            },
            'marker_sizes': {
                'wells': 50,
                'scores': 50,
                'com': 100
            }
        }

    def setup_figure(self) -> None:
        """Initialize the figure with consistent styling."""
        plt.style.use('default')
        self.fig = plt.figure(figsize=self.style_config['figure_size'])
        self.ax = plt.subplot2grid((8, 1), (0, 0), rowspan=6, projection='polar')
        self.fig.patch.set_facecolor('white')
        self.ax.set_facecolor('white')
        self.ax.spines['polar'].set_color('none')

    def add_titles(self, subtitle: str) -> None:
        """Add main title and subtitle with consistent styling."""
        self.fig.text(0.5, 0.92, self.style_config['main_title'],
                     fontsize=self.style_config['font_sizes']['title'],
                     fontweight='bold',
                     horizontalalignment='center')
        
        self.fig.text(0.5, 0.89, subtitle,
                     fontsize=self.style_config['font_sizes']['subtitle'],
                     style='italic',
                     horizontalalignment='center')

    def plot_base_elements(self, wells: List[Dict]) -> Tuple[List[float], List[float], List[str]]:
        """Plot the common elements (unit circle and well positions)."""
        # Plot unit circle
        circle = plt.Circle((0, 0), 1.0, transform=self.ax.transData._b,
                          fill=False, color=self.style_config['colors']['wells'],
                          linestyle=':', alpha=0.5)
        self.ax.add_artist(circle)
        
        # Convert well data
        angles_rad = [np.deg2rad(well['angle']) for well in wells]
        scores = [well['score'] for well in wells]
        names = [well['name'] for well in wells]
        
        # Plot well positions
        self.ax.scatter(angles_rad, [1]*len(wells),
                       color=self.style_config['colors']['wells'],
                       s=self.style_config['marker_sizes']['wells'], zorder=3)
        
        # Add well labels
        for name, angle in zip(names, angles_rad):
            ha = 'center' if name in ["Dignity", "Tribalism"] else \
                 'left' if -np.pi/2 <= angle <= np.pi/2 else 'right'
            
            label_radius = 1.25 if name == "Resentment" else 1.2
            self.ax.text(angle, label_radius, name, ha=ha, va='center', rotation=0)
        
        return angles_rad, scores, names

    def plot_single_analysis(self, data: Dict, include_scores: bool = True) -> None:
        """Plot a single analysis with scores and COM."""
        angles_rad, scores, _ = self.plot_base_elements(data['wells'])
        
        if include_scores:
            # Plot scores and connection lines
            for angle, score in zip(angles_rad, scores):
                self.ax.scatter(angle, score,
                              color=self.style_config['colors']['scores'],
                              s=self.style_config['marker_sizes']['scores'],
                              zorder=3)
                self.ax.plot([angle, angle], [0, score],
                           color=self.style_config['colors']['scores'],
                           linestyle='--', alpha=0.5, zorder=2)
        
        # Plot COM
        com_x = data['metrics']['com']['x']
        com_y = data['metrics']['com']['y']
        com_r = np.sqrt(com_x**2 + com_y**2)
        com_theta = np.arctan2(com_y, com_x)
        
        self.ax.scatter(com_theta, com_r,
                       s=self.style_config['marker_sizes']['com'],
                       color=self.style_config['colors']['com'], zorder=4)
        self.ax.text(com_theta, com_r + 0.1,
                    f"COM = ({com_x:.2f}, {com_y:.2f})",
                    ha='center', va='bottom',
                    color=self.style_config['colors']['com'])

    def plot_multiple_coms(self, analyses: List[Dict]) -> None:
        """Plot multiple COMs from different analyses."""
        if not analyses:
            return
        
        # Use first analysis for base elements
        self.plot_base_elements(analyses[0]['wells'])
        
        # Use tab20 colormap for distinct colors
        n_colors = len(analyses)
        self.com_colors = plt.cm.tab20(np.linspace(0, 1, 20))[:n_colors]
        self.analyses = analyses  # Store for legend creation
        
        # Group points by proximity
        points = []
        for analysis in analyses:
            com_x = analysis['metrics']['com']['x']
            com_y = analysis['metrics']['com']['y']
            com_r = np.sqrt(com_x**2 + com_y**2)
            com_theta = np.arctan2(com_y, com_x)
            points.append((com_r, com_theta, com_x, com_y))
        
        # Find groups of overlapping points
        THRESHOLD = 0.02  # Distance threshold for considering points as overlapping
        groups = []
        used = set()
        
        for i, (r1, theta1, x1, y1) in enumerate(points):
            if i in used:
                continue
            
            group = [(i, (r1, theta1, x1, y1))]
            used.add(i)
            
            for j, (r2, theta2, x2, y2) in enumerate(points):
                if j in used:
                    continue
                
                # Calculate Euclidean distance between points
                dist = np.sqrt((x1-x2)**2 + (y1-y2)**2)
                if dist < THRESHOLD:
                    group.append((j, (r2, theta2, x2, y2)))
                    used.add(j)
            
            groups.append(group)
        
        # Plot points with offset for overlapping ones
        for group in groups:
            if len(group) == 1:
                # Single point - plot normally
                idx, (r, theta, _, _) = group[0]
                self.ax.scatter(theta, r,
                              s=self.style_config['marker_sizes']['com'],
                              color=self.com_colors[idx],
                              alpha=0.7,  # Add some transparency
                              zorder=4)
            else:
                # Multiple overlapping points - arrange in a small circle
                center_r = np.mean([p[1][0] for p in group])
                center_theta = np.mean([p[1][1] for p in group])
                
                # Calculate offsets in a circle
                n_points = len(group)
                radius = 0.02  # Size of the arrangement circle
                for i, (idx, _) in enumerate(group):
                    angle = 2 * np.pi * i / n_points
                    offset_r = radius * np.cos(angle)
                    offset_theta = radius * np.sin(angle) / center_r  # Adjust for polar coordinates
                    
                    self.ax.scatter(center_theta + offset_theta, center_r + offset_r,
                                  s=self.style_config['marker_sizes']['com'],
                                  color=self.com_colors[idx],
                                  alpha=0.7,  # Add some transparency
                                  zorder=4)

    def add_legend(self, mode: str = 'single') -> None:
        """Add appropriate legend based on visualization mode."""
        legend_ax = plt.subplot2grid((8, 1), (6, 0))
        legend_ax.axis('off')
        
        if mode == 'single':
            patches = [
                mpatches.Patch(color=self.style_config['colors']['wells'],
                             label='Gravity Wells'),
                mpatches.Patch(color=self.style_config['colors']['scores'],
                             label='Narrative Scores'),
                mpatches.Patch(color=self.style_config['colors']['com'],
                             label='Center of Mass')
            ]
            legend_ax.legend(handles=patches, loc='center', ncol=len(patches),
                           bbox_to_anchor=(0.5, 0.8))
        else:  # multiple
            # Create patches for each model's COM only
            patches = []
            
            # Add a patch for each model
            for analysis, color in zip(self.analyses, self.com_colors):
                patches.append(mpatches.Patch(color=color,
                                           label=analysis['metadata']['model_name']))
            
            # Use 3 columns for legend when there are many models
            ncol = 3 if len(patches) > 6 else 2
            legend_ax.legend(handles=patches, loc='center', ncol=ncol,
                           bbox_to_anchor=(0.5, 1.0))

    def add_summary(self, summary: str) -> None:
        """Add analysis summary with consistent styling."""
        wrapped_text = '\n'.join(wrap(summary, width=100))
        self.fig.text(0.5, 0.12, wrapped_text,
                     horizontalalignment='center',
                     verticalalignment='center',
                     fontsize=self.style_config['font_sizes']['summary'],
                     style='italic',
                     bbox=dict(facecolor='white', alpha=0.9,
                              edgecolor='none', pad=5))

    def finalize_plot(self) -> None:
        """Apply final styling and adjustments."""
        self.ax.set_ylim(0, 1.4)
        self.ax.set_rticks([])
        self.ax.set_xticks([])
        self.ax.grid(False)
        plt.subplots_adjust(top=0.85, bottom=0.05, hspace=0)

    def save_plot(self, output_path: str) -> None:
        """Save the plot to file."""
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.close()

def create_output_directory(json_path: str, data: Dict, multi_analysis: bool = False) -> tuple[str, str]:
    """Create output directory structure and return paths."""
    base_dir = Path("model_output")
    base_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    
    if multi_analysis:
        subfolder_name = f"{timestamp}_multi_model_comparison"
        base_filename = "moral_gravity_comparison"
    else:
        model_name = data['metadata'].get('model_name', 'unknown_model')
        model_name = model_name.lower().replace(' ', '_')
        json_name = Path(json_path).stem
        base_filename = f"{json_name}_{model_name}"
        subfolder_name = f"{timestamp}_{model_name}_{json_name}"
    
    output_dir = base_dir / subfolder_name
    output_dir.mkdir(exist_ok=True)
    
    json_filename = f"{base_filename}.json"
    png_filename = f"{base_filename}.png"
    
    json_output_path = output_dir / json_filename
    png_output_path = output_dir / png_filename
    
    if not multi_analysis:
        # Copy input file to output directory
        shutil.copy2(json_path, json_output_path)
    else:
        # For multi-analysis, save the combined analysis to the output directory
        temp_json = TEMP_DIR / json_filename
        shutil.copy2(json_path, json_output_path)
    
    return str(json_output_path), str(png_output_path)

def load_analysis_data(json_path: str) -> Dict:
    """Load and validate the analysis data from a JSON file."""
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    required_keys = {'wells', 'metrics'}
    if not all(key in data for key in required_keys):
        raise ValueError(f"JSON must contain all required keys: {required_keys}")
    
    return data

def generate_single_visualization(data: Dict, json_path: str) -> None:
    """Generate a single analysis visualization."""
    json_output_path, png_output_path = create_output_directory(json_path, data)
    
    viz = MoralGravityMap()
    viz.setup_figure()
    viz.add_titles(data['metadata']['title'])
    viz.plot_single_analysis(data)
    viz.add_legend(mode='single')
    viz.add_summary(data['metadata']['summary'])
    viz.finalize_plot()
    viz.save_plot(png_output_path)
    
    print(f"\nOutput files saved to: {os.path.dirname(png_output_path)}")

def generate_multi_visualization(analyses: List[Dict], output_name: str = "comparison") -> None:
    """Generate a visualization with multiple COMs."""
    _, png_output_path = create_output_directory(output_name, analyses[0], multi_analysis=True)
    
    viz = MoralGravityMap()
    viz.setup_figure()
    viz.add_titles("Multi-Model Moral Gravity Analysis")
    viz.plot_multiple_coms(analyses)
    viz.add_legend(mode='multiple')
    viz.finalize_plot()
    viz.save_plot(png_output_path)
    
    print(f"\nComparison visualization saved to: {os.path.dirname(png_output_path)}")

def main():
    if len(sys.argv) > 1:
        json_path = sys.argv[1]
    else:
        json_path = 'sample_analysis.json'
    
    try:
        # If input file is in root directory, move it to temp directory
        original_path = None
        if not Path(json_path).parent.is_absolute():
            original_path = Path(json_path)
            temp_input = TEMP_DIR / Path(json_path).name
            shutil.copy2(json_path, temp_input)
            json_path = str(temp_input)
        
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        if isinstance(data, list):
            generate_multi_visualization(data, json_path)
        else:
            generate_single_visualization(data, json_path)
            
        # Clean up temporary files
        for file in TEMP_DIR.glob("*"):
            file.unlink()
        
        # Remove original file if it was in root directory
        if original_path and original_path.exists():
            original_path.unlink()
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 