# Narrative Gravity Wells - Circular Coordinate System Engine
# Version 2.0.0 - Plotly-based Interactive Visualization

import json
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union
import argparse

from .visualization.plotly_circular import PlotlyCircularVisualizer

class NarrativeGravityWellsCircular:
    """
    Narrative Gravity Wells analyzer and visualizer using circular coordinate system.
    
    Version 2.0.0 implements Plotly-based interactive visualization while preserving
    analytical sophistication through enhanced algorithms.
    
    Three-Dimensional Architecture:
    1. Positional Arrangement (Visual Rhetoric): Framework developers control well positioning
    2. Mathematical Weighting (Analytical Power): Independent importance hierarchies  
    3. Algorithmic Enhancement (Technical Sophistication): Validated enhancement algorithms
    """
    
    def __init__(self, config_dir: str = "config"):
        self.circle_radius = 1.0
        self.config_dir = config_dir
        self.well_definitions = {}
        self.type_to_color = {
            'integrative': '#2E7D32',  # Dark green
            'disintegrative': '#C62828'  # Dark red
        }
        
        # Load configuration or use defaults for backward compatibility
        try:
            self._load_framework_config()
        except (FileNotFoundError, KeyError) as e:
            print(f"⚠️  Using default configuration (config not found: {e})")
            self._load_default_config()
        
        # Initialize visualizer
        self.visualizer = PlotlyCircularVisualizer(
            circle_radius=self.circle_radius,
            type_to_color=self.type_to_color
        )

    def _load_framework_config(self):
        """Load framework configuration from config directory."""
        config_path = Path(self.config_dir) / "framework_config.json"
        with open(config_path) as f:
            config = json.load(f)
            self.well_definitions = config.get('wells', {})
            self.type_to_color = config.get('type_to_color', self.type_to_color)

    def _load_default_config(self):
        """Load default configuration for backward compatibility."""
        self.well_definitions = {
            'hope': {'angle': 0, 'type': 'integrative', 'weight': 1.0},
            'justice': {'angle': 72, 'type': 'integrative', 'weight': 0.8},
            'truth': {'angle': 144, 'type': 'integrative', 'weight': 0.8},
            'fear': {'angle': 216, 'type': 'disintegrative', 'weight': 0.6},
            'manipulation': {'angle': 288, 'type': 'disintegrative', 'weight': 0.6}
        }

    def circle_point(self, angle_deg: float) -> Tuple[float, float]:
        """Convert angle in degrees to (x, y) coordinates on unit circle."""
        angle_rad = np.deg2rad(angle_deg)
        x = self.circle_radius * np.cos(angle_rad)
        y = self.circle_radius * np.sin(angle_rad)
        return x, y

    def calculate_narrative_position(self, well_scores: Dict[str, float]) -> Tuple[float, float]:
        """Calculate narrative position based on well scores."""
        weighted_x, weighted_y, total_weight = 0.0, 0.0, 0.0
        
        for well_name, score in well_scores.items():
            if well_name in self.well_definitions:
                angle = self.well_definitions[well_name]['angle']
                weight = abs(self.well_definitions[well_name].get('weight', 1.0))
                x, y = self.circle_point(angle)
                force = score * weight
                weighted_x += x * force
                weighted_y += y * force
                total_weight += force
                
        if total_weight > 0:
            return weighted_x / total_weight, weighted_y / total_weight
        return 0.0, 0.0

    def create_visualization(self, data: Dict, output_path: str = None) -> str:
        """Generate complete circular coordinate visualization from analysis data."""
        # Convert well definitions to format expected by visualizer
        wells = {
            name: {
                'angle': info['angle'],
                'type': info['type'],
                'weight': info.get('weight', 1.0)
            }
            for name, info in self.well_definitions.items()
        }
        
        # Extract scores if provided in data
        narrative_scores = {}
        if 'wells' in data:
            for well in data['wells']:
                if 'name' in well and 'score' in well:
                    narrative_scores[well['name']] = well['score']
        
        # Get title from metadata if available
        title = data.get('metadata', {}).get('title', 'Circular Coordinate Analysis')
        
        # Create visualization
        fig = self.visualizer.plot(
            wells=wells,
            narrative_scores=narrative_scores if narrative_scores else None,
            title=title,
            output_html=output_path.replace('.png', '.html') if output_path else None,
            output_png=output_path if output_path else None,
            show=output_path is None
        )
        
        return output_path if output_path else "displayed"

    def create_comparative_visualization(self, analyses: List[Dict], output_path: str = None) -> str:
        """Create comparison visualization for multiple analyses."""
        formatted_analyses = []
        
        for analysis in analyses:
            # Convert well definitions to format expected by visualizer
            wells = {
                name: {
                    'angle': info['angle'],
                    'type': info['type'],
                    'weight': info.get('weight', 1.0)
                }
                for name, info in self.well_definitions.items()
            }
            
            # Extract scores
            scores = {}
            if 'wells' in analysis:
                for well in analysis['wells']:
                    if 'name' in well and 'score' in well:
                        scores[well['name']] = well['score']
            
            formatted_analyses.append({
                'title': analysis.get('metadata', {}).get('title', 'Analysis'),
                'wells': wells,
                'scores': scores
            })
        
        # Create comparison visualization
        self.visualizer.create_comparison(
            analyses=formatted_analyses,
            title='Comparative Analysis',
            output_html=output_path.replace('.png', '.html') if output_path else None,
            output_png=output_path if output_path else None
        )
        
        return output_path if output_path else "displayed"


def main():
    """CLI interface for circular coordinate system visualization."""
    print("🎯 Circular Coordinate System Engine v2.0.0")
    print("🔄 Enhanced algorithms with Plotly visualization")
    print("🌐 Interactive and publication-ready outputs")
    
    # Parse arguments
    parser = argparse.ArgumentParser(description='Circular Coordinate System Visualization')
    parser.add_argument('--config', default='config', help='Path to config directory')
    parser.add_argument('--output', help='Path to output file')
    args = parser.parse_args()
    
    # Basic test
    engine = NarrativeGravityWellsCircular(config_dir=args.config)
    test_data = {
        'metadata': {'title': 'Test Visualization'},
        'wells': [
            {'name': 'hope', 'score': 0.9},
            {'name': 'justice', 'score': 0.7},
            {'name': 'truth', 'score': 0.5},
            {'name': 'fear', 'score': 0.2},
            {'name': 'manipulation', 'score': 0.1}
        ]
    }
    
    output_path = args.output
    if not output_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"circular_test_{timestamp}.html"
    
    result = engine.create_visualization(test_data, output_path)
    print(f"✅ Visualization created: {result}")
    
    return test_data, result


if __name__ == "__main__":
    results, viz_path = main() 