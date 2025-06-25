# Discernus Coordinate System Engine
# Version 2.0.0 - Plotly-based Interactive Visualization

import json
import yaml
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union, Any
import argparse

from .visualization.plotly_circular import PlotlyCircularVisualizer
from .utils.algorithm_config_loader import AlgorithmConfigLoader, AlgorithmConfig

class DiscernusCoordinateEngine:
    """
    Discernus Coordinate System analyzer and visualizer with configurable algorithms.
    
    Version 3.0 implements configurable algorithm parameters for research flexibility:
    - Configurable Dominance Amplification: Customizable threshold and multiplier
    - Configurable Adaptive Scaling: Adjustable scaling factors and sensitivity
    - LLM-Mathematical Integration: Documented prompting-amplification pipeline
    - Academic Transparency: Algorithm parameters explicitly reportable
    
    Three-Dimensional Architecture:
    1. Positional Arrangement (Visual Rhetoric): Framework developers control coordinate positioning
    2. Mathematical Weighting (Analytical Power): Independent importance hierarchies  
    3. Algorithmic Enhancement (Technical Sophistication): Configurable enhancement algorithms
    
    Features:
    - YAML-only framework loading (JSON deprecated)
    - Backward-compatible defaults for existing frameworks
    - Comprehensive algorithm parameter validation
    - Academic reporting support
    """
    
    def __init__(self, config_dir: str = "config", framework_path: str = None):
        self.circle_radius = 1.0
        self.config_dir = config_dir
        self.framework_path = framework_path
        self.well_definitions = {}
        self.framework_data = {}  # Store framework data for algorithm config loading
        self.type_to_color = {
            'integrative': '#2E7D32',  # Dark green
            'disintegrative': '#C62828',  # Dark red
            'individualizing': '#1976D2',  # Blue
            'binding': '#388E3C',  # Green
            'individualizing_violation': '#D32F2F',  # Red
            'binding_violation': '#F57C00',  # Orange
            'liberty_based': '#9C27B0'  # Purple
        }
        
        # Load framework configuration - YAML only (JSON deprecated)
        try:
            if framework_path:
                self._load_yaml_framework(framework_path)
            else:
                raise FileNotFoundError("No framework_path provided. JSON config deprecated - use YAML frameworks.")
        except (FileNotFoundError, KeyError) as e:
            print(f"⚠️  Using default configuration: {e}")
            self._load_default_config()
        
        # Load algorithm configuration
        self.algorithm_config_loader = AlgorithmConfigLoader()
        try:
            if framework_path and self.framework_data:
                self.algorithm_config = self.algorithm_config_loader.load_from_framework_data(
                    self.framework_data, framework_path
                )
            else:
                self.algorithm_config = self.algorithm_config_loader.get_default_config()
        except Exception as e:
            print(f"⚠️  Error loading algorithm config: {e}")
            print("⚠️  Using default algorithm configuration")
            self.algorithm_config = self.algorithm_config_loader.get_default_config()
        
        # Initialize visualizer
        self.visualizer = PlotlyCircularVisualizer(
            circle_radius=self.circle_radius,
            type_to_color=self.type_to_color
        )

    def _load_yaml_framework(self, framework_path: str):
        """Load framework configuration from YAML framework file."""
        try:
            with open(framework_path, 'r', encoding='utf-8') as f:
                framework_data = yaml.safe_load(f)
            
            # Store framework data for algorithm configuration loading
            self.framework_data = framework_data
            self.well_definitions = {}
            
            # Try Framework Specification v3.1 axes format first
            if 'axes' in framework_data:
                axes = framework_data['axes']
                for axis_name, axis_info in axes.items():
                    # Extract integrative pole
                    if 'integrative' in axis_info:
                        integrative = axis_info['integrative']
                        well_name = integrative['name']
                        self.well_definitions[well_name] = {
                            'angle': integrative.get('angle', 0),
                            'type': integrative.get('type', 'integrative'),
                            'weight': abs(integrative.get('weight', 1.0)),
                            'description': integrative.get('description', '')
                        }
                    
                    # Extract disintegrative pole
                    if 'disintegrative' in axis_info:
                        disintegrative = axis_info['disintegrative']
                        well_name = disintegrative['name']
                        self.well_definitions[well_name] = {
                            'angle': disintegrative.get('angle', 180),
                            'type': disintegrative.get('type', 'disintegrative'),
                            'weight': abs(disintegrative.get('weight', 1.0)),
                            'description': disintegrative.get('description', '')
                        }
                
                # Update colors from axis_type_colors if provided
                if 'axis_type_colors' in framework_data:
                    framework_colors = framework_data['axis_type_colors']
                    self.type_to_color.update(framework_colors)
                    
            # Try anchors-based format (alternative v3.1 format)
            elif 'anchors' in framework_data:
                anchors = framework_data['anchors']
                for anchor_name, anchor_info in anchors.items():
                    self.well_definitions[anchor_name] = {
                        'angle': anchor_info.get('angle', 0),
                        'type': anchor_info.get('type', 'anchor'),
                        'weight': abs(anchor_info.get('weight', 1.0)),
                        'description': anchor_info.get('description', '')
                    }
                
                # Update colors from anchor_type_colors if provided
                if 'anchor_type_colors' in framework_data:
                    framework_colors = framework_data['anchor_type_colors']
                    self.type_to_color.update(framework_colors)
                    
            # Fall back to dipoles format (legacy)
            elif 'dipoles' in framework_data:
                dipoles = framework_data.get('dipoles', [])
                
                for dipole in dipoles:
                    # Add positive pole
                    if 'positive' in dipole:
                        positive = dipole['positive']
                        self.well_definitions[positive['name']] = {
                            'angle': positive.get('angle', 0),
                            'type': positive.get('type', 'positive'),
                            'weight': abs(positive.get('weight', 1.0)),
                            'description': positive.get('description', '')
                        }
                    
                    # Add negative pole  
                    if 'negative' in dipole:
                        negative = dipole['negative']
                        self.well_definitions[negative['name']] = {
                            'angle': negative.get('angle', 180),
                            'type': negative.get('type', 'negative'),
                            'weight': abs(negative.get('weight', 1.0)),
                            'description': negative.get('description', '')
                        }
                
                # Update colors from well_type_colors if provided
                if 'well_type_colors' in framework_data:
                    framework_colors = framework_data['well_type_colors']
                    self.type_to_color.update(framework_colors)
                
            print(f"✅ Loaded {len(self.well_definitions)} wells from YAML framework: {framework_path}")
            
        except Exception as e:
            raise FileNotFoundError(f"Failed to load YAML framework {framework_path}: {e}")



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
        # Convert numpy types to Python native types for database compatibility
        return float(x), float(y)

    def apply_dominance_amplification(self, score: float) -> float:
        """
        Apply configurable dominance amplification for high scores.
        Uses algorithm configuration parameters for threshold and multiplier.
        """
        if not self.algorithm_config.dominance_amplification.enabled:
            return score
            
        threshold = self.algorithm_config.dominance_amplification.threshold
        multiplier = self.algorithm_config.dominance_amplification.multiplier
        
        if score > threshold:
            return score * multiplier
        return score
    
    def calculate_adaptive_scaling(self, well_scores: Dict[str, float]) -> float:
        """
        Calculate configurable adaptive scaling factor for optimal boundary utilization.
        Uses algorithm configuration parameters for scaling factors and sensitivity.
        """
        if not self.algorithm_config.adaptive_scaling.enabled:
            return 0.8  # Simple default when disabled
            
        if not well_scores:
            return self.algorithm_config.adaptive_scaling.base_scaling
        
        # Get configuration parameters
        base_scaling = self.algorithm_config.adaptive_scaling.base_scaling
        max_scaling = self.algorithm_config.adaptive_scaling.max_scaling
        variance_factor = self.algorithm_config.adaptive_scaling.variance_factor
        mean_factor = self.algorithm_config.adaptive_scaling.mean_factor
        
        # Calculate narrative strength based on score variance
        scores = list(well_scores.values())
        max_score = max(scores)
        min_score = min(scores)
        score_variance = max_score - min_score
        mean_score = float(np.mean(scores))  # Convert numpy type to Python float
        
        # Adaptive scaling based on narrative characteristics using configurable parameters
        # High variance + high mean = strong narrative = higher scaling
        # Low variance + low mean = weak narrative = lower scaling
        variance_boost = min(score_variance * variance_factor, (max_scaling - base_scaling) * 0.6)
        mean_boost = min(mean_score * mean_factor, (max_scaling - base_scaling) * 0.4)
        
        adaptive_scale = base_scaling + variance_boost + mean_boost
        return min(adaptive_scale, max_scaling)
    
    def calculate_narrative_position(self, well_scores: Dict[str, float], return_detailed_results: bool = False) -> Union[Tuple[float, float], Dict[str, Any]]:
        """
        Calculate narrative position using configurable algorithms with support for academic transparency.
        
        Args:
            well_scores: Dictionary mapping well names to raw scores (0.0-1.0)
            return_detailed_results: If True, returns detailed breakdown for chart output options
            
        Returns:
            If return_detailed_results=False: Tuple of (x, y) coordinates (backward compatibility)
            If return_detailed_results=True: Dictionary with raw/enhanced scores and coordinates
        """
        if not well_scores:
            if return_detailed_results:
                return {
                    'raw_scores': {},
                    'enhanced_scores': {},
                    'raw_coordinates': (0.0, 0.0),
                    'enhanced_coordinates': (0.0, 0.0),
                    'algorithm_config': self.get_algorithm_config_info(),
                    'scaling_factor': 0.8,
                    'amplification_applied': False
                }
            return 0.0, 0.0
        
        # Store raw scores for academic transparency
        raw_scores = well_scores.copy()
        
        # Apply enhanced algorithms to well scores
        enhanced_scores = {}
        for well_name, score in well_scores.items():
            if well_name in self.well_definitions:
                # Apply dominance amplification
                enhanced_score = self.apply_dominance_amplification(score)
                enhanced_scores[well_name] = enhanced_score
        
        # Calculate adaptive scaling factor using enhanced scores
        adaptive_scale = self.calculate_adaptive_scaling(enhanced_scores)
        
        # Helper function to calculate coordinates from scores
        def calculate_coordinates_from_scores(scores: Dict[str, float], scale_factor: float) -> Tuple[float, float]:
            weighted_x, weighted_y, total_weight = 0.0, 0.0, 0.0
            
            for well_name, score in scores.items():
                if well_name in self.well_definitions:
                    angle = self.well_definitions[well_name]['angle']
                    weight = abs(self.well_definitions[well_name].get('weight', 1.0))
                    x, y = self.circle_point(angle)
                    force = score * weight
                    weighted_x += x * force
                    weighted_y += y * force
                    total_weight += force
            
            if total_weight > 0:
                # Calculate base position
                base_x = weighted_x / total_weight
                base_y = weighted_y / total_weight
                
                # Apply scaling to optimize boundary utilization
                final_x = base_x * scale_factor
                final_y = base_y * scale_factor
                
                # Convert to Python native types for database compatibility
                return float(final_x), float(final_y)
            
            return 0.0, 0.0
        
        # Calculate coordinates for both raw and enhanced scores
        raw_coordinates = calculate_coordinates_from_scores(raw_scores, adaptive_scale)
        enhanced_coordinates = calculate_coordinates_from_scores(enhanced_scores, adaptive_scale)
        
        # Check if amplification was actually applied
        amplification_applied = any(
            enhanced_scores.get(name, 0) != raw_scores.get(name, 0) 
            for name in raw_scores.keys()
        )
        
        if return_detailed_results:
            return {
                'raw_scores': raw_scores,
                'enhanced_scores': enhanced_scores,
                'raw_coordinates': raw_coordinates,
                'enhanced_coordinates': enhanced_coordinates,
                'algorithm_config': self.get_algorithm_config_info(),
                'scaling_factor': adaptive_scale,
                'amplification_applied': amplification_applied,
                'threshold_exceeded_count': len([s for s in raw_scores.values() if s > self.algorithm_config.dominance_amplification.threshold])
            }
        
        # Return enhanced coordinates for backward compatibility
        return enhanced_coordinates

    def create_visualization(self, data: Dict, output_path: str = None, 
                            chart_output_mode: str = "enhanced_only", layout: str = "side_by_side") -> str:
        """
        Generate complete circular coordinate visualization with configurable chart output modes.
        
        Args:
            data: Analysis data containing wells and scores
            output_path: Output file path (optional)
            chart_output_mode: "raw_only", "enhanced_only", "both_comparison"
            layout: "side_by_side", "overlay" (for both_comparison mode)
        """
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
        
        # Generate detailed results for chart mode support
        if narrative_scores and chart_output_mode != "enhanced_only":
            # Get detailed results with both raw and enhanced coordinates
            detailed_results = self.calculate_narrative_position(narrative_scores, return_detailed_results=True)
            
            # Use new chart mode visualization
            fig = self.visualizer.plot_with_chart_modes(
                wells=wells,
                detailed_results=detailed_results,
                chart_output_mode=chart_output_mode,
                layout=layout,
                title=title,
                output_html=output_path.replace('.png', '.html') if output_path else None,
                output_png=output_path if output_path else None,
                show=output_path is None
            )
        else:
            # Fall back to standard visualization for backward compatibility
            fig = self.visualizer.plot(
                wells=wells,
                narrative_scores=narrative_scores if narrative_scores else None,
                title=title,
                output_html=output_path.replace('.png', '.html') if output_path else None,
                output_png=output_path if output_path else None,
                show=output_path is None
            )
        
        return output_path if output_path else "displayed"
    
    def create_academic_transparency_visualization(self, data: Dict, output_path: str = None) -> str:
        """
        Create visualization specifically designed for academic transparency with both raw and enhanced results.
        
        This is a convenience method that always uses "both_comparison" mode with "side_by_side" layout
        for maximum academic transparency and peer review support.
        """
        return self.create_visualization(
            data=data,
            output_path=output_path,
            chart_output_mode="both_comparison",
            layout="side_by_side"
        )

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

    def get_algorithm_config_info(self) -> Dict[str, Any]:
        """
        Get algorithm configuration information for logging and academic reporting.
        
        Returns:
            Dictionary containing algorithm configuration details
        """
        return {
            'algorithm_config_version': '3.0',
            'dominance_amplification': {
                'enabled': self.algorithm_config.dominance_amplification.enabled,
                'threshold': self.algorithm_config.dominance_amplification.threshold,
                'multiplier': self.algorithm_config.dominance_amplification.multiplier,
                'rationale': self.algorithm_config.dominance_amplification.rationale
            },
            'adaptive_scaling': {
                'enabled': self.algorithm_config.adaptive_scaling.enabled,
                'base_scaling': self.algorithm_config.adaptive_scaling.base_scaling,
                'max_scaling': self.algorithm_config.adaptive_scaling.max_scaling,
                'variance_factor': self.algorithm_config.adaptive_scaling.variance_factor,
                'mean_factor': self.algorithm_config.adaptive_scaling.mean_factor,
                'methodology': self.algorithm_config.adaptive_scaling.methodology
            },
            'prompting_integration': {
                'dominance_instruction': self.algorithm_config.prompting_integration.dominance_instruction,
                'amplification_purpose': self.algorithm_config.prompting_integration.amplification_purpose,
                'methodology_reference': self.algorithm_config.prompting_integration.methodology_reference
            }
        }


def main():
    """CLI interface for configurable coordinate system visualization."""
    print("🎯 Discernus Coordinate System Engine v3.0")
    print("⚙️  Configurable algorithms: Dominance amplification + adaptive scaling")
    print("📚 Academic transparency: Algorithm parameters explicitly reportable")
    print("🌐 Interactive and publication-ready outputs")
    
    # Parse arguments
    parser = argparse.ArgumentParser(description='Configurable Coordinate System Visualization')
    parser.add_argument('--framework', help='Path to YAML framework file')
    parser.add_argument('--output', help='Path to output file')
    parser.add_argument('--show-config', action='store_true', help='Show algorithm configuration')
    args = parser.parse_args()
    
    # Initialize engine
    try:
        if args.framework:
            engine = DiscernusCoordinateEngine(framework_path=args.framework)
        else:
            print("ℹ️  No framework specified, using default configuration")
            engine = DiscernusCoordinateEngine()
    except Exception as e:
        print(f"❌ Error initializing engine: {e}")
        return None, None
    
    # Show algorithm configuration if requested
    if args.show_config:
        print("\n📋 Algorithm Configuration:")
        config_info = engine.get_algorithm_config_info()
        for section, params in config_info.items():
            if section == 'algorithm_config_version':
                print(f"  Version: {params}")
            else:
                print(f"  {section.replace('_', ' ').title()}:")
                for key, value in params.items():
                    print(f"    {key}: {value}")
        print()
    
    # Basic test with realistic data
    test_data = {
        'metadata': {'title': 'Configurable Algorithm Test'},
        'wells': [
            {'name': 'hope', 'score': 0.9},  # High score - should get amplification if threshold <= 0.9
            {'name': 'justice', 'score': 0.7},  # At default threshold
            {'name': 'truth', 'score': 0.5},
            {'name': 'fear', 'score': 0.2},
            {'name': 'manipulation', 'score': 0.1}
        ]
    }
    
    # Test configurable algorithms
    print("🧪 Testing configurable algorithms:")
    
    # Test dominance amplification
    original_score = 0.8
    amplified_score = engine.apply_dominance_amplification(original_score)
    if amplified_score != original_score:
        print(f"  ✅ Dominance amplification: {original_score} → {amplified_score:.3f}")
    else:
        print(f"  ℹ️  Dominance amplification: {original_score} (no change - below threshold or disabled)")
    
    # Test adaptive scaling
    test_scores = {'hope': 0.9, 'justice': 0.7, 'fear': 0.2}
    scaling_factor = engine.calculate_adaptive_scaling(test_scores)
    print(f"  ✅ Adaptive scaling factor: {scaling_factor:.3f}")
    
    # Create visualization
    output_path = args.output
    if not output_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"configurable_test_{timestamp}.html"
    
    result = engine.create_visualization(test_data, output_path)
    print(f"✅ Visualization created: {result}")
    
    # Report algorithm configuration for academic transparency
    print("\n📊 Algorithm Configuration for Academic Reporting:")
    config_info = engine.get_algorithm_config_info()
    dom_config = config_info['dominance_amplification']
    scale_config = config_info['adaptive_scaling']
    
    print(f"  Dominance amplification: {'enabled' if dom_config['enabled'] else 'disabled'}")
    if dom_config['enabled']:
        print(f"    Threshold: {dom_config['threshold']} (scores above this receive amplification)")
        print(f"    Multiplier: {dom_config['multiplier']} (amplification factor)")
    
    print(f"  Adaptive scaling: {'enabled' if scale_config['enabled'] else 'disabled'}")
    if scale_config['enabled']:
        print(f"    Base scaling: {scale_config['base_scaling']} (minimum coordinate scaling)")
        print(f"    Max scaling: {scale_config['max_scaling']} (maximum coordinate scaling)")
    
    return test_data, result


if __name__ == "__main__":
    results, viz_path = main() 