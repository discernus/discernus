"""
Elliptical Moral Gravity Wells Framework v2.0
Copyright (c) 2025 Jeff Whatcott
All rights reserved.

This module implements the Elliptical Moral Gravity Wells framework v2.0 for analyzing 
the moral forces driving political narratives. Based on the academic paper 
"Moral Gravity Wells: A Quantitative Framework for Discerning the Moral Forces 
Driving Political Narratives."

Version 2.0 enhancements include:
- Interactive LLM prompt system for multi-file comparative analysis
- Enhanced filename generation with content identification and vendor attribution  
- Professional visualization system with automatic text fitting
- Support for multiple AI models (GPT-4, Claude, Gemini, etc.)
- Modular configuration system for extensibility

The framework positions ten moral "gravity wells" on an elliptical boundary,
with integrative wells in the upper half and disintegrative wells in the lower half.
Narratives are positioned inside the ellipse based on gravitational pull from boundary wells.
"""

import matplotlib.pyplot as plt
import seaborn as sns
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
import matplotlib.colors as mcolors
import argparse

class MoralGravityWellsElliptical:
    """
    Elliptical Moral Gravity Wells analyzer and visualizer.
    
    This class implements the mathematical framework for positioning narratives
    within an elliptical coordinate system based on moral gravity wells.
    
    Version 2.0 adds modular configuration support while maintaining full 
    backward compatibility with existing JSON files and naming conventions.
    """
    
    def __init__(self, config_dir: str = "config"):
        self.fig = None
        self.ax = None
        self.config_dir = config_dir
        
        # Use pure matplotlib for reliable aspect ratio control
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
        
        # Load configuration or use defaults for backward compatibility
        try:
            self._load_framework_config()
        except (FileNotFoundError, KeyError) as e:
            print(f"⚠️  Using default configuration (config not found: {e})")
            self._load_default_config()
        
        # Style configuration remains the same
        self.style_config = {
            'figure_size': (10, 12.5),  # Larger size while maintaining 4:5 ratio (same as 8:10)
            'main_title': "Elliptical Moral Gravity Wells Analysis",
            'font_sizes': {
                'title': 20,      # Slightly larger for bigger figure
                'subtitle': 16,   # Slightly larger for bigger figure
                'summary': 12,    # Slightly larger for bigger figure
                'labels': 11,     # Slightly larger for bigger figure
                'coordinates': 9,
                'metrics': 11
            },
            'colors': {
                'wells_integrative': '#2E7D32',      # Deep green
                'wells_disintegrative': '#C62828',   # Deep red
                'wells_integrative_edge': '#1B5E20', # Darker green edge
                'wells_disintegrative_edge': '#B71C1C', # Darker red edge
                'scores': '#1976D2',                 # Professional blue
                'narrative': '#FF8F00',              # Vibrant orange
                'narrative_edge': '#E65100',         # Darker orange edge
                'ellipse': '#616161',                # Professional gray
                'text_primary': '#212121',           # Dark gray
                'text_secondary': '#757575',         # Medium gray
                'metrics_bg': '#F5F5F5',            # Light gray background
                'metrics_border': '#BDBDBD'          # Medium gray border
            },
            'marker_sizes': {
                'wells': 80,
                'scores': 60,
                'narrative': 300
            }
        }

    def _load_framework_config(self):
        """Load framework configuration from config files."""
        framework_path = Path(self.config_dir) / "framework.json"
        
        with open(framework_path, 'r') as f:
            framework = json.load(f)
        
        # Extract ellipse parameters
        ellipse_config = framework['ellipse']
        self.ellipse_a = ellipse_config['semi_major_axis']
        self.ellipse_b = ellipse_config['semi_minor_axis']
        
        # Extract well definitions
        wells_config = framework['wells']
        self.well_definitions = {}
        
        for well_name, well_config in wells_config.items():
            self.well_definitions[well_name] = {
                'angle': well_config['angle'],
                'type': well_config['type'],
                'moral_weight': well_config['weight']
            }
        
        # Store additional framework metadata
        self.framework_version = framework.get('version', 'unknown')
        self.scaling_factor = framework.get('scaling_factor', 0.8)
        
        # Clean version string for display (remove v prefix if present to avoid duplication)
        display_version = self.framework_version
        if display_version.startswith('v'):
            display_version = display_version[1:]
        
        print(f"✅ Loaded framework v{display_version} from {framework_path}")

    def _load_default_config(self):
        """Load default configuration for backward compatibility."""
        # Ellipse parameters - CORRECT orientation
        self.ellipse_a = 1.0  # Semi-major axis (VERTICAL)
        self.ellipse_b = 0.7  # Semi-minor axis (HORIZONTAL)
        
        # Well definitions with elliptical positioning (current values)
        self.well_definitions = {
            'Dignity': {'angle': 90, 'type': 'integrative', 'moral_weight': 1.0},
            'Justice': {'angle': 135, 'type': 'integrative', 'moral_weight': 0.8},
            'Truth': {'angle': 45, 'type': 'integrative', 'moral_weight': 0.8},
            'Pragmatism': {'angle': 160, 'type': 'integrative', 'moral_weight': 0.6},
            'Hope': {'angle': 20, 'type': 'integrative', 'moral_weight': 0.6},
            'Tribalism': {'angle': 270, 'type': 'disintegrative', 'moral_weight': -1.0},
            'Resentment': {'angle': 225, 'type': 'disintegrative', 'moral_weight': -0.8},
            'Manipulation': {'angle': 315, 'type': 'disintegrative', 'moral_weight': -0.8},
            'Fear': {'angle': 200, 'type': 'disintegrative', 'moral_weight': -0.6},
            'Fantasy': {'angle': 340, 'type': 'disintegrative', 'moral_weight': -0.6}
        }
        
        self.framework_version = "default"
        self.scaling_factor = 0.8

    def ellipse_point(self, angle_deg: float) -> Tuple[float, float]:
        """Calculate point on ellipse boundary for given angle."""
        angle_rad = np.deg2rad(angle_deg)
        x = self.ellipse_b * np.cos(angle_rad)  # Minor axis horizontal
        y = self.ellipse_a * np.sin(angle_rad)  # Major axis vertical
        return x, y

    def setup_figure(self) -> None:
        """Initialize the figure with clean layout."""
        # Create figure with tall proportions
        self.fig = plt.figure(figsize=self.style_config['figure_size'])
        self.fig.patch.set_facecolor('white')
        
        # Simple, clean subplot
        self.ax = plt.subplot(1, 1, 1)
        self.ax.set_facecolor('white')
        
        # CRITICAL: Set equal aspect ratio for proper ellipse display
        self.ax.set_aspect('equal')
        self.ax.set_xlim(-1.2, 1.2)
        self.ax.set_ylim(-1.4, 1.4)
        
        # Clean grid
        self.ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5, color='lightgray')
        self.ax.set_axisbelow(True)
        
        # Remove ticks for cleaner look
        self.ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
        for spine in self.ax.spines.values():
            spine.set_visible(False)

    def plot_ellipse_boundary(self) -> None:
        """Plot the elliptical boundary using parametric equations for guaranteed orientation."""
        # Create ellipse using parametric equations - this WORKS
        theta = np.linspace(0, 2*np.pi, 100)
        x_ellipse = self.ellipse_b * np.cos(theta)  # horizontal (smaller)
        y_ellipse = self.ellipse_a * np.sin(theta)  # vertical (larger)
        
        # Plot the ellipse boundary
        self.ax.plot(x_ellipse, y_ellipse, 
                    color=self.style_config['colors']['ellipse'],
                    linestyle='-', 
                    linewidth=3,
                    alpha=0.8)

    def add_titles(self, subtitle: str, model_name: str = None, model_version: str = None) -> None:
        """Add main title and subtitle with model information."""
        # Extract clean subtitle (remove existing parentheses)
        clean_subtitle = subtitle.split(' (')[0] if ' (' in subtitle else subtitle
        
        # Add model information if available
        if model_name and model_version:
            clean_subtitle += f" (analyzed by {model_name})"
        elif model_name:
            clean_subtitle += f" (analyzed by {model_name})"
        
        self.fig.text(0.5, 0.95, self.style_config['main_title'],
                     fontsize=self.style_config['font_sizes']['title'],
                     fontweight='bold',
                     horizontalalignment='center',
                     color=self.style_config['colors']['text_primary'])
        
        self.fig.text(0.5, 0.91, clean_subtitle,
                     fontsize=self.style_config['font_sizes']['subtitle'],
                     style='italic',
                     horizontalalignment='center',
                     color=self.style_config['colors']['text_secondary'])

    def plot_wells_and_scores(self, wells: List[Dict], include_scores: bool = True) -> Dict[str, float]:
        """Plot wells on ellipse boundary with clean styling."""
        well_scores = {}
        
        for well in wells:
            name = well['name']
            score = well['score']
            well_scores[name] = score
            
            current_well_angle = self.well_definitions[name]['angle'] # Get angle from loaded config
            x, y = self.ellipse_point(current_well_angle)
            
            # Choose colors based on well type
            well_type = self.well_definitions[name]['type']
            if well_type == 'integrative':
                well_color = self.style_config['colors']['wells_integrative']
                edge_color = self.style_config['colors']['wells_integrative_edge']
            else:
                well_color = self.style_config['colors']['wells_disintegrative']
                edge_color = self.style_config['colors']['wells_disintegrative_edge']
            
            # Plot well position
            self.ax.scatter(x, y, 
                          color=well_color,
                          s=self.style_config['marker_sizes']['wells'], 
                          zorder=4, alpha=0.9,
                          edgecolors=edge_color,
                          linewidth=2)
            
            # Add well labels with smart positioning
            # Check if the well is at the top (90 deg) or bottom (270 deg)
            if current_well_angle == 90 or current_well_angle == 270:
                # Center labels for top and bottom wells
                label_x = 0  # Force x-coordinate to exactly 0 for perfect centering
                label_y = y + (0.09 if current_well_angle == 90 else -0.09)
                ha = 'center'
                va = 'bottom' if current_well_angle == 90 else 'top'
            else:
                # Standard positioning for other wells
                label_offset = 0.09
                label_x = x + (label_offset if x >= 0 else -label_offset)
                label_y = y + (0.025 if y >= 0 else -0.025)
                ha = 'left' if x >= 0 else 'right'
                va = 'bottom' if y >= 0 else 'top'
            
            # Well labels
            self.ax.text(label_x, label_y, name, ha=ha, va=va, 
                        fontsize=self.style_config['font_sizes']['labels'], 
                        fontweight='bold',
                        color=self.style_config['colors']['text_primary'],
                        bbox=dict(boxstyle="round,pad=0.3", 
                                facecolor='white', 
                                alpha=0.9,
                                edgecolor=edge_color,
                                linewidth=1))
            
            if include_scores:
                # Plot score as inner point
                score_x = x * score * 0.8
                score_y = y * score * 0.8
                self.ax.scatter(score_x, score_y,
                              color=self.style_config['colors']['scores'],
                              s=self.style_config['marker_sizes']['scores'],
                              alpha=0.8, zorder=3,
                              edgecolors='white',
                              linewidth=1.5)
                
                # Draw line from center to score
                self.ax.plot([0, score_x], [0, score_y],
                           color=self.style_config['colors']['scores'],
                           linestyle='--', alpha=0.6, zorder=2,
                           linewidth=1.5)
        
        return well_scores

    def calculate_narrative_position(self, well_scores: Dict[str, float]) -> Tuple[float, float]:
        """Calculate narrative position inside ellipse based on gravitational pull from wells."""
        weighted_x = 0.0
        weighted_y = 0.0
        total_weight = 0.0
        
        for well_name, score in well_scores.items():
            if well_name in self.well_definitions:
                well_x, well_y = self.ellipse_point(self.well_definitions[well_name]['angle'])
                moral_weight = self.well_definitions[well_name]['moral_weight']
                force = score * abs(moral_weight)
                
                weighted_x += well_x * force
                weighted_y += well_y * force
                total_weight += force
        
        if total_weight > 0:
            narrative_x = weighted_x / total_weight
            narrative_y = weighted_y / total_weight
            
            # Ensure narrative stays inside ellipse
            scale_factor = 0.8
            narrative_x *= scale_factor
            narrative_y *= scale_factor
            
            return narrative_x, narrative_y
        
        return 0.0, 0.0

    def plot_narrative_position(self, well_scores: Dict[str, float]) -> Tuple[float, float]:
        """Calculate and plot the narrative position."""
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
                    "Moral Center",
                    ha='center', va='bottom',
                    color=self.style_config['colors']['text_primary'],
                    fontweight='bold', 
                    fontsize=self.style_config['font_sizes']['labels'],
                    bbox=dict(boxstyle="round,pad=0.4", 
                            facecolor='white', 
                            alpha=0.9,
                            edgecolor=self.style_config['colors']['narrative'],
                            linewidth=2))
        
        # Add coordinates
        self.ax.text(narrative_x, narrative_y - 0.12,
                    f"({narrative_x:.2f}, {narrative_y:.2f})",
                    ha='center', va='top',
                    color=self.style_config['colors']['text_secondary'],
                    fontsize=self.style_config['font_sizes']['coordinates'],
                    alpha=0.8)
        
        return narrative_x, narrative_y

    def generate_content_identifier(self, title: str) -> str:
        """Generate a clean content identifier from the analysis title."""
        # Remove the "(analyzed by...)" part
        clean_title = title.split(' (analyzed by')[0].strip()
        
        # Convert to filename-safe format
        content_id = clean_title.lower()
        content_id = content_id.replace(' ', '_')
        content_id = content_id.replace(':', '')
        content_id = content_id.replace('-', '_')
        content_id = content_id.replace(',', '')
        content_id = content_id.replace('.', '')
        content_id = content_id.replace('(', '')
        content_id = content_id.replace(')', '')
        content_id = content_id.replace('"', '')
        content_id = content_id.replace("'", '')
        
        # Limit length to keep filenames reasonable
        if len(content_id) > 50:
            content_id = content_id[:50]
        
        # Remove trailing underscores
        content_id = content_id.rstrip('_')
        
        return content_id

    def generate_model_filename_part(self, metadata: Dict) -> str:
        """Generate proper model part of filename from metadata."""
        model_name = metadata.get('model_name', 'unknown_model')
        model_version = metadata.get('model_version', '')
        
        # Clean and combine model name and version
        clean_name = model_name.lower().replace(' ', '_').replace('-', '_')
        clean_version = model_version.lower().replace(' ', '_').replace('-', '_')
        
        # Handle common patterns
        if 'chatgpt' in clean_name.lower():
            if 'gpt-4' in clean_version or 'gpt_4' in clean_version:
                return 'openai_gpt_4'
            elif 'gpt-3' in clean_version or 'gpt_3' in clean_version:
                return 'openai_gpt_3'
            else:
                return 'openai_chatgpt'
        elif 'gpt-4' in clean_name or 'gpt_4' in clean_name:
            return 'openai_gpt_4'
        elif 'claude' in clean_name:
            if clean_version:
                return f'anthropic_claude_{clean_version}'
            return 'anthropic_claude'
        elif 'gemini' in clean_name:
            if clean_version:
                return f'google_gemini_{clean_version}'
            return 'google_gemini'
        else:
            # Generic case - combine name and version if available
            if clean_version and clean_version not in clean_name:
                return f"{clean_name}_{clean_version}"
            return clean_name

    def add_visualization_metadata(self, analyses: List[Dict], output_path: str = None) -> None:
        """Add comprehensive metadata at the bottom of the visualization."""
        metadata_lines = []
        
        # Get current framework info
        framework_name = "unknown"
        framework_version = self.framework_version
        
        # Try to get framework name from config
        try:
            with open(Path(self.config_dir) / "dipoles.json", 'r') as f:
                dipoles_data = json.load(f)
                framework_name = dipoles_data.get('framework_name', 'unknown')
                display_name = dipoles_data.get('display_name', framework_name)
                if display_name and display_name != framework_name:
                    framework_name = display_name
        except:
            pass
        
        # Clean framework version for display
        display_version = framework_version
        if display_version.startswith('v'):
            display_version = display_version[1:]
        
        # Add creation timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        metadata_lines.append(f"Generated: {timestamp}")
        
        # Add framework info
        metadata_lines.append(f"Framework: {framework_name} v{display_version}")
        
        # Add file and model info for each analysis
        for i, analysis in enumerate(analyses):
            metadata = analysis.get('metadata', {})
            
            # Extract filename from metadata if available
            filename = metadata.get('filename', f'analysis_{i+1}.json')
            if filename.endswith('.json'):
                filename = filename[:-5]  # Remove .json extension for cleaner display
            
            # Get model info
            model_name = metadata.get('model_name', 'Unknown')
            model_version = metadata.get('model_version', '')
            model_info = f"{model_name} {model_version}".strip() if model_version else model_name
            
            # Create file info line
            file_line = f"File {i+1}: {filename} ({model_info})"
            metadata_lines.append(file_line)
        
        # Join all metadata lines
        metadata_text = " | ".join(metadata_lines)
        
        # Add metadata at the very bottom of the figure
        self.fig.text(0.5, 0.01, metadata_text,
                     fontsize=8,
                     color='#666666',
                     horizontalalignment='center',
                     verticalalignment='bottom',
                     style='italic',
                     bbox=dict(boxstyle="round,pad=0.3", 
                             facecolor='white', 
                             alpha=0.8,
                             edgecolor='lightgray',
                             linewidth=0.5))

    def create_visualization(self, data: Dict, output_path: str = None) -> str:
        """Generate complete visualization from analysis data."""
        
        # Normalize data to handle both old and new JSON formats
        normalized_data = normalize_analysis_data(data)
        
        # Ensure well angles match current framework configuration
        for well in normalized_data['wells']:
            well_name = well['name']
            if well_name in self.well_definitions:
                well['angle'] = self.well_definitions[well_name]['angle']
            else:
                print(f"⚠️  Unknown well '{well_name}' - using angle 0")
                well['angle'] = 0
        
        self.setup_figure()
        self.add_titles(normalized_data['metadata']['title'], 
                       normalized_data['metadata'].get('model_name'), 
                       normalized_data['metadata'].get('model_version'))
        self.plot_ellipse_boundary()
        
        # Plot wells and scores
        well_scores = self.plot_wells_and_scores(normalized_data['wells'])
        
        # Plot narrative position
        narrative_x, narrative_y = self.plot_narrative_position(well_scores)
        
        # Add metrics display
        metrics = self.calculate_elliptical_metrics(narrative_x, narrative_y, well_scores)
        self.add_metrics_display(metrics)
        
        # Add legend
        self.add_legend()
        
        # Add summary
        self.add_summary(normalized_data['metadata']['summary'])
        
        # Add comprehensive metadata at bottom
        self.add_visualization_metadata([normalized_data], output_path)
        
        # Finalize
        plt.tight_layout()
        
        if output_path is None:
            # Generate filename using improved model name generation and content identifier
            timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
            model_part = self.generate_model_filename_part(normalized_data['metadata'])
            content_part = self.generate_content_identifier(normalized_data['metadata']['title'])
            filename = f"{timestamp}_{model_part}_{content_part}.png"
            output_path = f"model_output/{filename}"
        
        # Create output directory if it doesn't exist
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.close()
        return output_path

    def calculate_elliptical_metrics(self, narrative_x: float, narrative_y: float, 
                                   well_scores: Dict[str, float]) -> Dict[str, float]:
        """Calculate enhanced metrics for elliptical positioning."""
        
        # Moral Elevation Score: Y-coordinate normalized by semi-major axis (vertical)
        moral_elevation = narrative_y / self.ellipse_a
        
        # Enhanced Moral Polarity: Distance from center normalized
        moral_polarity = np.sqrt(narrative_x**2 + narrative_y**2) / max(self.ellipse_a, self.ellipse_b)
        
        # Narrative Coherence: Consistency of pull direction
        integrative_pull = sum(score for name, score in well_scores.items() 
                              if self.well_definitions[name]['type'] == 'integrative')
        disintegrative_pull = sum(score for name, score in well_scores.items() 
                                 if self.well_definitions[name]['type'] == 'disintegrative')
        
        total_pull = integrative_pull + disintegrative_pull
        if total_pull > 0:
            coherence = abs(integrative_pull - disintegrative_pull) / total_pull
        else:
            coherence = 0.0
            
        # Directional Purity Score (DPS): Alignment with vertical moral axis
        dps = self.calculate_directional_purity_score(well_scores)
        
        return {
            'moral_elevation': moral_elevation,
            'moral_polarity': moral_polarity,
            'coherence': coherence,
            'directional_purity': dps
        }

    def calculate_directional_purity_score(self, well_scores: Dict[str, float]) -> float:
        """Calculate Directional Purity Score (DPS) as specified in the paper."""
        numerator = 0.0
        denominator = 0.0
        
        for well_name, score in well_scores.items():
            if well_name in self.well_definitions:
                well_x, well_y = self.ellipse_point(self.well_definitions[well_name]['angle'])
                moral_weight = self.well_definitions[well_name]['moral_weight']
                
                numerator += moral_weight * score * np.sign(well_y)
                denominator += abs(moral_weight) * score
        
        if denominator > 0:
            return numerator / denominator
        return 0.0

    def add_metrics_display(self, metrics: Dict[str, float]) -> None:
        """Add metrics display outside the chart area."""
        metrics_text = (f"Moral Elevation: {metrics['moral_elevation']:.3f}\n"
                       f"Moral Polarity: {metrics['moral_polarity']:.3f}\n"
                       f"Coherence: {metrics['coherence']:.3f}\n"
                       f"Directional Purity: {metrics['directional_purity']:.3f}")
        
        self.fig.text(0.02, 0.5, metrics_text,  # Moved to center-left
                     fontsize=self.style_config['font_sizes']['metrics'],
                     color=self.style_config['colors']['text_primary'],
                     fontweight='bold',
                     verticalalignment='center', # Align to center
                     horizontalalignment='left', # Align to left
                     bbox=dict(boxstyle="round,pad=0.5", 
                             facecolor=self.style_config['colors']['metrics_bg'], 
                             alpha=0.9,
                             edgecolor=self.style_config['colors']['metrics_border'],
                             linewidth=1.5))

    def add_legend(self) -> None:
        """Add legend with clear styling."""
        patches = [
            mpatches.Patch(color=self.style_config['colors']['wells_integrative'],
                         label='Integrative Wells'),
            mpatches.Patch(color=self.style_config['colors']['wells_disintegrative'],
                         label='Disintegrative Wells'),
            mpatches.Patch(color=self.style_config['colors']['scores'],
                         label='Well Scores'),
            mpatches.Patch(color=self.style_config['colors']['narrative'],
                         label='Moral Center')
        ]
        
        self.fig.legend(handles=patches, 
                       loc='lower center', 
                       bbox_to_anchor=(0.5, 0.025),  # Moved legend down to y=0.025
                       ncol=4,
                       fontsize=self.style_config['font_sizes']['labels'],
                       frameon=True,
                       facecolor='white',
                       edgecolor='gray',
                       framealpha=0.9)

    def add_summary(self, summary: str) -> None:
        """Add analysis summary below the legend with generous space to prevent truncation."""
        # Very generous parameters for 500 character limit
        max_lines = 5  # Allow 5 lines to be safe
        base_font_size = 11
        min_font_size = 10
        
        working_summary = summary.strip()
        
        # Only truncate if dramatically over 500 chars (should rarely happen with prompt limit)
        if len(working_summary) > 550:  # Very generous buffer
            sentences = working_summary.split('. ')
            truncated = ""
            
            for i, sentence in enumerate(sentences):
                if i == 0:
                    test_text = sentence
                else:
                    test_text = truncated + ". " + sentence
                
                if len(test_text) <= 520:  # Very generous
                    truncated = test_text
                else:
                    break
            
            if len(truncated) > 100:
                working_summary = truncated.rstrip() + "..."
            else:
                working_summary = working_summary[:517] + "..."
        
        # Very conservative font sizing - avoid reduction unless absolutely necessary
        font_size = base_font_size
        target_chars_per_line = 90  # Conservative line width for safety
        
        final_length = len(working_summary)
        if final_length > 480:  # Only for very long summaries
            font_size = max(min_font_size, base_font_size - 1)
            target_chars_per_line = 95
        
        # Wrap text generously
        wrapped_text = '\n'.join(wrap(working_summary, width=target_chars_per_line))
        lines = wrapped_text.split('\n')
        
        # Only truncate as absolute last resort
        if len(lines) > max_lines:
            # Try wider lines first
            wrapped_text = '\n'.join(wrap(working_summary, width=target_chars_per_line + 15))
            lines = wrapped_text.split('\n')
            
            if len(lines) > max_lines:
                # Very generous final truncation
                final_lines = lines[:max_lines-1]
                last_line = lines[max_lines-1]
                if len(last_line) > target_chars_per_line + 10:
                    last_line = last_line[:target_chars_per_line+7] + "..."
                final_lines.append(last_line)
                wrapped_text = '\n'.join(final_lines)
        
        # Position the summary
        self.fig.text(0.5, 0.06,  # Moved summary down to y=0.06
                     wrapped_text,
                     horizontalalignment='center',
                     verticalalignment='bottom',
                     fontsize=font_size,
                     color=self.style_config['colors']['text_primary'],
                     style='italic',
                     bbox=dict(boxstyle="round,pad=0.5",
                              facecolor='white', 
                              alpha=0.95,
                              edgecolor=self.style_config['colors']['text_secondary'], 
                              linewidth=1.5))

    def smart_truncate_comparative_titles(self, titles: List[str], max_length: int = 25) -> List[str]:
        """
        Smart truncation for comparative titles that preserves distinguishing information.
        
        For titles with common prefixes/suffixes, focuses on the unique parts.
        For very similar titles, uses intelligent abbreviation and person name extraction.
        """
        if len(titles) < 2:
            # Single title - use standard truncation
            return [title[:max_length-3] + "..." if len(title) > max_length else title for title in titles]
        
        # Clean titles first (remove "(analyzed by...)" parts)
        clean_titles = []
        for title in titles:
            clean_title = title.split(' (analyzed by')[0] if ' (analyzed by' in title else title
            clean_titles.append(clean_title)
        
        # Find common prefix
        if len(clean_titles) >= 2:
            # Find longest common prefix
            common_prefix = ""
            min_len = min(len(t) for t in clean_titles)
            for i in range(min_len):
                if all(title[i] == clean_titles[0][i] for title in clean_titles):
                    common_prefix += clean_titles[0][i]
                else:
                    break
            
            # Find longest common suffix  
            common_suffix = ""
            for i in range(1, min_len + 1):
                if all(title[-i] == clean_titles[0][-i] for title in clean_titles):
                    common_suffix = clean_titles[0][-i] + common_suffix
                else:
                    break
            
            # If we have a significant common prefix (more than 10 chars), focus on unique parts
            if len(common_prefix) > 10:
                unique_parts = []
                for title in clean_titles:
                    # Remove common prefix and suffix
                    unique_part = title[len(common_prefix):]
                    if common_suffix and unique_part.endswith(common_suffix):
                        unique_part = unique_part[:-len(common_suffix)]
                    
                    # Clean up the unique part
                    unique_part = unique_part.strip(" -_,")
                    
                    # Special handling for presidential speeches and similar patterns
                    if unique_part:
                        # Extract person names for inaugural addresses, speeches, etc.
                        words = unique_part.split()
                        if len(words) >= 2:
                            # Look for name patterns: "Donald J. Trump", "Abraham Lincoln", etc.
                            if any(word.endswith('.') for word in words[:3]):  # Middle initial pattern
                                # "Donald J. Trump" -> "D.J. Trump"
                                if len(words) >= 3:
                                    unique_part = f"{words[0][0]}.{words[1]} {words[2]}"
                                else:
                                    unique_part = f"{words[0][0]}. {words[1]}"
                            elif len(words) == 2 and all(word[0].isupper() for word in words):
                                # "Abraham Lincoln" -> "A. Lincoln" if too long
                                if len(unique_part) > max_length:
                                    unique_part = f"{words[0][0]}. {words[1]}"
                            elif len(words) > 2:
                                # Multiple words - try to abbreviate intelligently
                                unique_part = f"{words[0]} {words[-1]}"  # First and last word
                    
                    # If still too long, truncate but preserve the end (usually the name)
                    if len(unique_part) > max_length:
                        if len(unique_part.split()) > 1:
                            # Keep the last word (usually surname) and truncate the beginning
                            words = unique_part.split()
                            last_word = words[-1]
                            remaining_space = max_length - len(last_word) - 4  # "... "
                            if remaining_space > 0:
                                unique_part = f"...{unique_part[:remaining_space]} {last_word}"
                            else:
                                unique_part = f"...{last_word}"
                        else:
                            unique_part = unique_part[:max_length-3] + "..."
                    
                    # Add context clue if very short
                    if len(unique_part) < 8 and common_prefix:
                        # Add abbreviated prefix for context
                        prefix_words = common_prefix.strip().split()
                        if prefix_words:
                            # Abbreviate first word(s) for context
                            if "inaugural" in common_prefix.lower():
                                context = "Inaug:"
                            elif "speech" in common_prefix.lower():
                                context = "Speech:"
                            elif "address" in common_prefix.lower():
                                context = "Addr:"
                            else:
                                context = f"{prefix_words[0][:4]}:"
                            unique_part = f"{context} {unique_part}"
                    
                    unique_parts.append(unique_part if unique_part else title[:max_length-3] + "...")
                
                return unique_parts
        
        # Fallback: no significant common prefix, use standard smart truncation
        result = []
        for title in clean_titles:
            if len(title) <= max_length:
                result.append(title)
            else:
                # Try to preserve important words (names, key terms)
                words = title.split()
                if len(words) > 1:
                    # Keep first and last words if possible
                    first_word = words[0]
                    last_word = words[-1]
                    if len(first_word) + len(last_word) + 4 <= max_length:  # space for "... "
                        result.append(f"{first_word}...{last_word}")
                    else:
                        # Just truncate normally
                        result.append(title[:max_length-3] + "...")
                else:
                    result.append(title[:max_length-3] + "...")
        
        return result

    def create_comparative_visualization(self, analyses: List[Dict], output_path: str = None) -> str:
        """Create a comparative visualization of multiple analyses."""
        
        # Normalize all analysis data
        normalized_analyses = [normalize_analysis_data(data) for data in analyses]
        
        # Ensure all wells have current framework angles
        for analysis in normalized_analyses:
            for well in analysis['wells']:
                well_name = well['name']
                if well_name in self.well_definitions:
                    well['angle'] = self.well_definitions[well_name]['angle']
                else:
                    print(f"⚠️  Unknown well '{well_name}' - using angle 0")
                    well['angle'] = 0
        
        self.setup_figure()
        
        # Create title with multiple narratives
        titles = [data['metadata']['title'] for data in normalized_analyses]
        
        # Clean titles by removing any existing "(analyzed by...)" parts
        clean_titles = []
        for title in titles:
            clean_title = title.split(' (analyzed by')[0] if ' (analyzed by' in title else title
            clean_titles.append(clean_title)
        
        # Create subtitle with both narrative names
        comparative_subtitle = " vs. ".join(clean_titles[:2])  # Show first 2 titles
        if len(clean_titles) > 2:
            comparative_subtitle += f" (and {len(clean_titles) - 2} more)"
        
        # Use custom titles for comparative analysis
        self.fig.text(0.5, 0.95, "Moral Distance Analysis",
                     fontsize=self.style_config['font_sizes']['title'],
                     fontweight='bold',
                     horizontalalignment='center',
                     color=self.style_config['colors']['text_primary'])
        
        self.fig.text(0.5, 0.91, comparative_subtitle,
                     fontsize=self.style_config['font_sizes']['subtitle'],
                     style='italic',
                     horizontalalignment='center',
                     color=self.style_config['colors']['text_secondary'])
        
        self.plot_ellipse_boundary()
        
        # Plot wells (only once)
        self.plot_wells_only(normalized_analyses[0]['wells'])
        
        # Calculate positions for all narratives
        positions = []
        colors = plt.cm.Set1([i/len(normalized_analyses) for i in range(len(normalized_analyses))])
        
        # Get smart truncated titles for the chart labels
        chart_titles = self.smart_truncate_comparative_titles(titles, max_length=25)
        
        for i, data in enumerate(normalized_analyses):
            well_scores = {well['name']: well['score'] for well in data['wells']}
            x, y = self.calculate_narrative_position(well_scores)
            positions.append((x, y))
            
            # Plot each narrative with different color
            self.ax.scatter(x, y, 
                          s=self.style_config['marker_sizes']['narrative'],
                          c=[colors[i]], 
                          edgecolors='black',
                          linewidth=2,
                          alpha=0.9,
                          zorder=10)
            
            # Use the smart truncated title
            truncated_title = chart_titles[i]
            
            # Center the label over the moral center
            self.ax.text(x, y + 0.12,  # Position above the center
                        truncated_title,
                        ha='center', va='bottom',
                        fontsize=10,
                        fontweight='bold',
                        color=self.style_config['colors']['text_primary'],
                        bbox=dict(boxstyle="round,pad=0.3", 
                                facecolor=colors[i], 
                                alpha=0.8,
                                edgecolor='black',
                                linewidth=1))
        
        # Add dotted line between moral centers (if there are exactly 2)
        if len(positions) == 2:
            pos1, pos2 = positions
            self.ax.plot([pos1[0], pos2[0]], [pos1[1], pos2[1]], 
                        linestyle='--', 
                        color='gray',  # Make it gray and more subtle
                        linewidth=2,  # Make it thinner for a more subtle line
                        alpha=0.6,    # Make it more opaque for testing
                        zorder=15)    # Higher z-order to ensure it's on top
        
        # Add comparative metrics (but no legend since labels are on chart)
        self.add_comparative_metrics(positions, normalized_analyses)
        
        # Add comprehensive metadata at bottom (replacing model info box)
        self.add_visualization_metadata(normalized_analyses, output_path)
        
        plt.tight_layout()
        
        if output_path is None:
            timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
            filename = f"{timestamp}_comparative_analysis.png"
            output_path = f"model_output/{filename}"
        
        # Create output directory if it doesn't exist
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.close()
        return output_path

    def plot_wells_only(self, wells: List[Dict]) -> None:
        """Plot only the wells without scores for comparative visualization."""
        for well in wells:
            name = well['name']
            
            if name in self.well_definitions:
                current_well_angle = self.well_definitions[name]['angle'] # Get angle from loaded config
                x, y = self.ellipse_point(current_well_angle)
                
                # Choose colors based on well type
                well_type = self.well_definitions[name]['type']
                if well_type == 'integrative':
                    well_color = self.style_config['colors']['wells_integrative']
                    edge_color = self.style_config['colors']['wells_integrative_edge']
                else:
                    well_color = self.style_config['colors']['wells_disintegrative']
                    edge_color = self.style_config['colors']['wells_disintegrative_edge']
                
                # Plot well position
                self.ax.scatter(x, y, 
                              color=well_color,
                              s=self.style_config['marker_sizes']['wells'], 
                              zorder=4, alpha=0.9,
                              edgecolors=edge_color,
                              linewidth=2)
                
                # Add well labels with smart positioning
                # Check if the well is at the top (90 deg) or bottom (270 deg)
                if current_well_angle == 90 or current_well_angle == 270:
                    label_x = 0
                    label_y = y + (0.09 if current_well_angle == 90 else -0.09)
                    ha = 'center'
                    va = 'bottom' if current_well_angle == 90 else 'top'
                else:
                    label_offset = 0.09
                    label_x = x + (label_offset if x >= 0 else -label_offset)
                    label_y = y + (0.025 if y >= 0 else -0.025)
                    ha = 'left' if x >= 0 else 'right'
                    va = 'bottom' if y >= 0 else 'top'
                
                # Well labels
                self.ax.text(label_x, label_y, name, ha=ha, va=va, 
                            fontsize=self.style_config['font_sizes']['labels'], 
                            fontweight='bold',
                            color=self.style_config['colors']['text_primary'],
                            bbox=dict(boxstyle="round,pad=0.3", 
                                    facecolor='white', 
                                    alpha=0.9,
                                    edgecolor=edge_color,
                                    linewidth=1))

    def add_comparative_metrics(self, positions: List[Tuple[float, float]], analyses: List[Dict]) -> None:
        """Add comparative metrics and distance information."""
        if len(positions) < 2:
            return
            
        # Calculate elliptical distance
        distance = self.calculate_elliptical_distance(positions[0], positions[1])
        
        # Get key metrics from each analysis
        metrics_text = "Comparative Metrics:\n"
        titles = [analysis['metadata']['title'].split(' (')[0] for analysis in analyses]
        
        for i, analysis in enumerate(analyses):
            wells_dict = {well['name']: well['score'] for well in analysis['wells']}
            narrative_x, narrative_y = positions[i]
            metrics = self.calculate_elliptical_metrics(narrative_x, narrative_y, wells_dict)
            
            title_short = titles[i][:15] + "..." if len(titles[i]) > 15 else titles[i]
            metrics_text += f"\n{title_short}:\n"
            metrics_text += f"  Elevation: {metrics['moral_elevation']:.3f}\n"
            metrics_text += f"  Coherence: {metrics['coherence']:.3f}\n"
        
        metrics_text += f"\nElliptical Distance: {distance:.3f}"
        
        # Position metrics on the left side
        self.fig.text(0.02, 0.5, metrics_text,
                     fontsize=self.style_config['font_sizes']['metrics'] - 1,
                     color=self.style_config['colors']['text_primary'],
                     fontweight='bold',
                     verticalalignment='center',
                     bbox=dict(boxstyle="round,pad=0.5", 
                             facecolor='lightblue', 
                             alpha=0.9,
                             edgecolor='blue',
                             linewidth=1.5))

    def calculate_elliptical_distance(self, pos_a: Tuple[float, float], 
                                    pos_b: Tuple[float, float]) -> float:
        """Calculate distance between two narrative positions using elliptical geometry."""
        x_a, y_a = pos_a
        x_b, y_b = pos_b
        
        # Elliptical distance formula
        distance = np.sqrt(((x_a - x_b)**2) / (self.ellipse_b**2) + 
                          ((y_a - y_b)**2) / (self.ellipse_a**2))
        
        return distance

def load_analysis_data(json_path: str) -> Dict:
    """Load analysis data from JSON file."""
    with open(json_path, 'r') as f:
        return json.load(f)

def normalize_analysis_data(data: Dict) -> Dict:
    """
    Normalize analysis data to handle both old and new JSON formats.
    
    Old format: {'wells': [{'name': 'Dignity', 'angle': 90, 'score': 1.0}, ...]}
    New format: {'scores': {'Dignity': 1.0, 'Truth': 0.8, ...}}
    
    Always returns old format for backward compatibility with visualization code.
    """
    if 'scores' in data and 'wells' not in data:
        # New minimal format - convert to old format for backward compatibility
        wells = []
        scores = data['scores']
        
        # Note: angles and weights will be loaded from framework config during visualization
        # For now, we create wells entries without angles (they'll be populated later)
        for well_name, score in scores.items():
            wells.append({
                'name': well_name,
                'score': score,
                'angle': 0,  # Will be overridden by framework config
            })
        
        # Create normalized data structure
        normalized_data = data.copy()
        normalized_data['wells'] = wells
        
        return normalized_data
    
    elif 'wells' in data:
        # Old format - return as-is but ensure angles match current framework if available
        return data
    
    else:
        raise ValueError("Invalid JSON format: must contain either 'wells' or 'scores'")

def main():
    """Main function for generating elliptical moral gravity visualizations."""
    parser = argparse.ArgumentParser(
        description='Generate elliptical moral gravity visualizations from JSON analysis files'
    )
    parser.add_argument('json_files', nargs='+',
                      help='Path(s) to JSON analysis files (for comparative analysis, provide multiple files)')
    parser.add_argument('--output', '-o', type=str,
                      help='Output path for the generated image (optional)')
    
    args = parser.parse_args()
    
    visualizer = MoralGravityWellsElliptical()
    
    try:
        if len(args.json_files) == 1:
            # Single analysis visualization
            print(f"Generating single analysis visualization from: {args.json_files[0]}")
            analysis_data = load_analysis_data(args.json_files[0])
            output_path = visualizer.create_visualization(analysis_data, args.output)
            print(f"Single analysis visualization saved to: {output_path}")
        else:
            # Comparative analysis visualization
            print(f"Generating comparative analysis visualization from {len(args.json_files)} files:")
            analyses = []
            for json_file in args.json_files:
                print(f"  - {json_file}")
                analyses.append(load_analysis_data(json_file))
            
            output_path = visualizer.create_comparative_visualization(analyses, args.output)
            print(f"Comparative analysis visualization saved to: {output_path}")
    
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format - {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 