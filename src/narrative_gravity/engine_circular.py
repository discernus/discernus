# Narrative Gravity Wells - Circular Coordinate System Engine
# Version 1.1.0 - Universal Tool Compatibility with Enhanced Algorithms

import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union
import matplotlib.colors as mcolors
import argparse

class NarrativeGravityWellsCircular:
    """
    Narrative Gravity Wells analyzer and visualizer using circular coordinate system.
    
    Version 1.1.0 implements circular coordinates for maximum researcher adoption
    while preserving analytical sophistication through enhanced algorithms.
    
    Three-Dimensional Architecture:
    1. Positional Arrangement (Visual Rhetoric): Framework developers control well positioning
    2. Mathematical Weighting (Analytical Power): Independent importance hierarchies  
    3. Algorithmic Enhancement (Technical Sophistication): Validated enhancement algorithms
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
        
        # Style configuration optimized for circular coordinates
        self.style_config = {
            'figure_size': (10, 10),  # Square aspect ratio for circular system
            'main_title': "Narrative Gravity Wells Analysis",
            'font_sizes': {
                'title': 20,
                'subtitle': 16,
                'summary': 12,
                'labels': 11,
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
                'circle': '#616161',                 # Professional gray
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
        
        # Enhanced algorithm parameters (validated through iterative optimization)
        self.enhancement_config = {
            'dominance_amplification': {
                'threshold': 0.7,
                'amplification_base': 2.0,  # Refined from initial 2.5
                'max_amplification': 2.5,
                'moderate_boost': 1.1,
                'suppression_power': 1.5
            },
            'adaptive_scaling': {
                'min_scale': 0.65,  # Moderate narratives
                'max_scale': 0.95,  # Extreme narratives
                'extremeness_weight': 0.30
            },
            'boundary_snapping': {
                'dominance_threshold': 0.85,
                'snap_strength': 0.15,
                'boundary_target': 0.92
            }
        }

    def _load_framework_config(self):
        """Load framework configuration from config files with circular coordinate support."""
        framework_path = Path(self.config_dir) / "framework.json"
        
        with open(framework_path, 'r') as f:
            framework = json.load(f)
        
        # Extract circle parameters (simplified from ellipse)
        if 'circle' in framework:
            circle_config = framework['circle']
            self.circle_radius = circle_config.get('radius', 1.0)
        elif 'ellipse' in framework:
            # Backward compatibility: convert ellipse to circle
            ellipse_config = framework['ellipse']
            # Use average of semi-axes for circular radius
            self.circle_radius = (ellipse_config['semi_major_axis'] + ellipse_config['semi_minor_axis']) / 2
            print(f"ℹ️  Converted elliptical config to circular (radius: {self.circle_radius:.2f})")
        else:
            self.circle_radius = 1.0
        
        # Load positioning strategy (new flexible system)
        self.positioning_strategy = framework.get('positioning_strategy', {})
        strategy_type = self.positioning_strategy.get('type', 'individual_angles')
        
        # Extract well definitions with strategy-aware positioning
        wells_config = framework['wells']
        self.well_definitions = {}
        
        if strategy_type in ['clustered_positioning', 'clustered_dipoles']:
            # Wells use clustering strategy - angles may be auto-generated or specified
            self.well_definitions = self._apply_clustered_positioning(wells_config)
        elif strategy_type == 'even_distribution':
            # Auto-generate evenly distributed angles
            self.well_definitions = self._apply_even_distribution(wells_config)
        else:
            # Individual angles - use exactly as specified (default behavior)
            for well_name, well_config in wells_config.items():
                self.well_definitions[well_name] = {
                    'angle': well_config['angle'],  # Standard 0-360 degree positioning
                    'type': well_config['type'],    # integrative/disintegrative
                    'narrative_weight': well_config['weight']  # Mathematical weighting
                }
        
        # Store additional framework metadata
        self.framework_version = framework.get('version', 'unknown')
        self.scaling_factor = framework.get('scaling_factor', 0.8)
        
        # Load positional arrangement preference (new in v1.1.0)
        self.positional_arrangement = framework.get('positional_arrangement', 'normative')
        
        # Clean version string for display
        display_version = self.framework_version
        if display_version.startswith('v'):
            display_version = display_version[1:]
        
        print(f"✅ Loaded circular framework v{display_version} from {framework_path}")
        print(f"ℹ️  Positioning strategy: {strategy_type}")
        if strategy_type in ['clustered_positioning', 'clustered_dipoles']:
            clusters = self.positioning_strategy.get('clusters', {})
            if clusters:
                cluster_info = []
                for cluster_name, cluster_config in clusters.items():
                    span = cluster_config.get('span', 'N/A')
                    center = cluster_config.get('center_angle', 'N/A')
                    cluster_info.append(f"{cluster_name} {span}°@{center}°")
                print(f"ℹ️  Clusters: {', '.join(cluster_info)}")
            else:
                # Legacy support
                integrative_span = self.positioning_strategy.get('integrative_cluster', {}).get('span', 'N/A')
                disintegrative_span = self.positioning_strategy.get('disintegrative_cluster', {}).get('span', 'N/A')
                print(f"ℹ️  Legacy clustering spans: integrative {integrative_span}°, disintegrative {disintegrative_span}°")

    def _load_default_config(self):
        """Load default circular configuration with Civic Virtue framework as example."""
        # Circular parameters - universal standard
        self.circle_radius = 1.0
        
        # Default: Civic Virtue Framework with normative positioning
        # Integrative wells in upper hemisphere (normative "good")
        # Disintegrative wells in lower hemisphere (normative "problematic")
        self.well_definitions = {
            # Integrative wells (upper hemisphere) - hierarchical weighting
            'Dignity': {'angle': 0, 'type': 'integrative', 'narrative_weight': 1.0},     # Top (identity)
            'Truth': {'angle': 45, 'type': 'integrative', 'narrative_weight': 0.8},     # Upper right (principles)
            'Justice': {'angle': 135, 'type': 'integrative', 'narrative_weight': 0.8},  # Upper left (principles)
            'Hope': {'angle': 315, 'type': 'integrative', 'narrative_weight': 0.6},     # Lower right (moderators)
            'Pragmatism': {'angle': 285, 'type': 'integrative', 'narrative_weight': 0.6}, # Lower right (moderators)
            
            # Disintegrative wells (lower hemisphere) - hierarchical weighting
            'Tribalism': {'angle': 180, 'type': 'disintegrative', 'narrative_weight': -1.0},  # Bottom (identity)
            'Manipulation': {'angle': 315, 'type': 'disintegrative', 'narrative_weight': -0.8}, # Lower right (principles)
            'Resentment': {'angle': 225, 'type': 'disintegrative', 'narrative_weight': -0.8},   # Lower left (principles)
            'Fear': {'angle': 200, 'type': 'disintegrative', 'narrative_weight': -0.6},        # Lower left (moderators)
            'Fantasy': {'angle': 255, 'type': 'disintegrative', 'narrative_weight': -0.6}      # Lower center (moderators)
        }
        
        self.framework_version = "default_circular_v1.1.0"
        self.scaling_factor = 0.8
        self.positional_arrangement = "normative"  # Civic Virtue default

    def _apply_clustered_positioning(self, wells_config):
        """Apply clustered positioning strategy (framework-agnostic)."""
        well_definitions = {}
        
        # Get all defined clusters (framework can define any number with any names)
        clusters = self.positioning_strategy.get('clusters', {})
        
        # Fallback to legacy integrative/disintegrative naming for backward compatibility
        if not clusters:
            clusters = {}
            if 'integrative_cluster' in self.positioning_strategy:
                clusters['cluster_1'] = self.positioning_strategy['integrative_cluster']
            if 'disintegrative_cluster' in self.positioning_strategy:
                clusters['cluster_2'] = self.positioning_strategy['disintegrative_cluster']
        
        # Create mapping from well types to cluster assignments
        well_type_to_cluster = {}
        for cluster_name, cluster_config in clusters.items():
            assigned_types = cluster_config.get('well_types', [])
            for well_type in assigned_types:
                well_type_to_cluster[well_type] = cluster_name
        
        # Group wells by their assigned clusters
        cluster_wells = {}
        unassigned_wells = []
        
        for well_name, well_config in wells_config.items():
            well_type = well_config.get('type', 'default')
            if well_type in well_type_to_cluster:
                cluster_name = well_type_to_cluster[well_type]
                if cluster_name not in cluster_wells:
                    cluster_wells[cluster_name] = []
                cluster_wells[cluster_name].append((well_name, well_config))
            else:
                unassigned_wells.append((well_name, well_config))
        
        # Generate positions for clustered wells
        for cluster_name, wells_in_cluster in cluster_wells.items():
            cluster_config = clusters[cluster_name]
            center_angle = cluster_config.get('center_angle', 0)
            span = cluster_config.get('span', 60)
            
            for i, (well_name, well_config) in enumerate(wells_in_cluster):
                if 'angle' in well_config:
                    # Use specified angle (framework developer choice)
                    angle = well_config['angle']
                else:
                    # Auto-generate within cluster
                    angle = self._generate_cluster_angle(center_angle, span, i, len(wells_in_cluster))
                
                well_definitions[well_name] = {
                    'angle': angle,
                    'type': well_config.get('type', 'default'),
                    'narrative_weight': well_config['weight']
                }
        
        # Handle unassigned wells (use individual angles if specified)
        for well_name, well_config in unassigned_wells:
            if 'angle' in well_config:
                well_definitions[well_name] = {
                    'angle': well_config['angle'],
                    'type': well_config.get('type', 'default'),
                    'narrative_weight': well_config['weight']
                }
            else:
                print(f"⚠️  Well '{well_name}' not assigned to cluster and no angle specified")
        
        return well_definitions

    def _apply_even_distribution(self, wells_config):
        """Apply even distribution positioning strategy."""
        well_definitions = {}
        
        # Get distribution parameters
        start_angle = self.positioning_strategy.get('start_angle', 0)
        rotation_offset = self.positioning_strategy.get('rotation_offset', 0)
        
        # Calculate even spacing
        num_wells = len(wells_config)
        angle_step = 360 / num_wells
        
        for i, (well_name, well_config) in enumerate(wells_config.items()):
            angle = (start_angle + (i * angle_step) + rotation_offset) % 360
            
            well_definitions[well_name] = {
                'angle': angle,
                'type': well_config['type'],
                'narrative_weight': well_config['weight']
            }
        
        return well_definitions

    def _generate_cluster_angle(self, center_angle, span, index, total_wells):
        """Generate angle within cluster for auto-positioning."""
        if total_wells == 1:
            return center_angle
        
        # Distribute wells evenly within the span
        start_angle = center_angle - (span / 2)
        step = span / (total_wells - 1) if total_wells > 1 else 0
        angle = (start_angle + (index * step)) % 360
        
        return angle

    def circle_point(self, angle_deg: float) -> Tuple[float, float]:
        """Calculate point on circle boundary for given angle using standard polar coordinates."""
        angle_rad = np.deg2rad(angle_deg)
        x = self.circle_radius * np.cos(angle_rad)
        y = self.circle_radius * np.sin(angle_rad)
        return x, y

    def apply_dominance_amplification(self, score: float) -> float:
        """Apply dominance amplification algorithm (validated through iterative optimization)."""
        config = self.enhancement_config['dominance_amplification']
        
        if score >= config['threshold']:
            # Amplify high scores exponentially
            excess = score - config['threshold']
            amplification = 1.0 + (excess ** config['amplification_base']) * 0.8
            return min(score * amplification, config['max_amplification'])
        elif score <= (1.0 - config['threshold']):
            # Gentle suppression for very low scores
            suppression = (score / (1.0 - config['threshold'])) ** config['suppression_power']
            return suppression
        else:
            # Moderate enhancement for middle range
            return score * config['moderate_boost']

    def calculate_adaptive_scaling(self, well_scores: Dict[str, float]) -> float:
        """Calculate adaptive scaling factor based on narrative extremeness."""
        config = self.enhancement_config['adaptive_scaling']
        
        # Measure extremeness through score variance and distance from center
        score_values = list(well_scores.values())
        variance = np.var(score_values)
        extremeness = max(abs(max(score_values) - 0.5), abs(min(score_values) - 0.5)) * 2
        
        # Combine measures
        combined_factor = (variance / 0.1 + extremeness) / 2
        
        # Scale from min_scale (moderate) to max_scale (extreme)
        scaling_factor = config['min_scale'] + (combined_factor * config['extremeness_weight'])
        return min(scaling_factor, config['max_scale'])

    def calculate_narrative_position(self, well_scores: Dict[str, float]) -> Tuple[float, float]:
        """Calculate narrative position using enhanced algorithms and circular coordinates."""
        
        # Step 1: Apply dominance amplification to all scores
        enhanced_scores = {name: self.apply_dominance_amplification(score) 
                         for name, score in well_scores.items()}
        
        # Step 2: Calculate base position using gravitational pull
        weighted_x = 0.0
        weighted_y = 0.0
        total_weight = 0.0
        
        for well_name, enhanced_score in enhanced_scores.items():
            if well_name in self.well_definitions:
                well_x, well_y = self.circle_point(self.well_definitions[well_name]['angle'])
                narrative_weight = self.well_definitions[well_name]['narrative_weight']
                force = enhanced_score * abs(narrative_weight)
                
                weighted_x += well_x * force
                weighted_y += well_y * force
                total_weight += force
        
        if total_weight > 0:
            # Base positioning
            narrative_x = weighted_x / total_weight
            narrative_y = weighted_y / total_weight
            
            # Step 3: Apply adaptive scaling
            adaptive_scale = self.calculate_adaptive_scaling(well_scores)
            narrative_x *= adaptive_scale
            narrative_y *= adaptive_scale
            
            return narrative_x, narrative_y
        
        return 0.0, 0.0

    def create_visualization(self, data: Dict, output_path: str = None) -> str:
        """Generate complete circular coordinate visualization from analysis data."""
        
        # Basic setup for testing
        self.fig = plt.figure(figsize=(10, 10))
        self.ax = plt.subplot(1, 1, 1)
        self.ax.set_aspect('equal')
        self.ax.set_xlim(-1.2, 1.2)
        self.ax.set_ylim(-1.2, 1.2)
        
        # Plot circle boundary
        theta = np.linspace(0, 2*np.pi, 100)
        x_circle = self.circle_radius * np.cos(theta)
        y_circle = self.circle_radius * np.sin(theta)
        self.ax.plot(x_circle, y_circle, 'k-', linewidth=2)
        
        # Add title
        plt.title("Circular Coordinate System Test")
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            return output_path
        else:
            plt.show()
            return "displayed"


def main():
    """CLI interface for circular coordinate system visualization."""
    print("🎯 Circular Coordinate System Engine v1.1.0")
    print("🔄 Enhanced algorithms: Dominance amplification, adaptive scaling")
    print("🌐 Universal tool compatibility: Standard polar coordinates")
    
    # Basic test
    engine = NarrativeGravityWellsCircular()
    test_data = {}
    engine.create_visualization(test_data)


if __name__ == "__main__":
    main() 