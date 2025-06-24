#!/usr/bin/env python3
"""
Discernus Visualization Iteration Lab
====================================

Rapid iteration environment for visualization development that enables:
- Hot-reload development of visualization features
- A/B testing of different mathematical approaches
- Theme switching and parameter tuning
- Direct integration with production data formats
- Fast feedback loops for both function and appearance

This lab uses the new cartographic terminology and provides a bridge
between experimental development and production integration.
"""

import sys
import json
import time
import importlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import plotly.graph_objects as go
from datetime import datetime

# Add project paths for imports
sys.path.append('/Volumes/dev/discernus/src')
sys.path.append('/Volumes/dev/discernus/experimental/prototypes')

# Import updated systems
from discernus_visualization_engine import DiscernusVisualizationEngine, create_discernus_visualization_engine
from discernus_themes import get_theme, list_themes


class VisualizationIterationLab:
    """
    Rapid iteration lab for visualization development.
    
    Features:
    - Live parameter tuning without code changes
    - A/B testing of mathematical approaches
    - Theme switching and comparison
    - Production data format compatibility
    - Hot-reload development workflow
    """
    
    def __init__(self, output_dir: str = "experimental/prototypes/iteration_output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create test configurations
        self.test_anchors = self._create_test_anchor_sets()
        self.test_signatures = self._create_test_signatures()
        
        # Track iterations
        self.iteration_count = 0
        self.results_log = []
        
        print("🧪 Discernus Visualization Iteration Lab Initialized")
        print(f"📁 Output directory: {self.output_dir}")
        
    def _create_test_anchor_sets(self) -> Dict[str, Dict]:
        """Create test anchor configurations for different framework types."""
        return {
            'civic_virtue_asfx': {
                # Axis-Set Framework (ASFx) - paired anchors
                'Hope': {'angle': 20, 'type': 'integrative', 'weight': 0.6},
                'Justice': {'angle': 90, 'type': 'integrative', 'weight': 0.8},
                'Truth': {'angle': 160, 'type': 'integrative', 'weight': 0.8},
                'Dignity': {'angle': 45, 'type': 'integrative', 'weight': 1.0},
                'Pragmatism': {'angle': 135, 'type': 'integrative', 'weight': 0.6},
                'Fear': {'angle': 200, 'type': 'disintegrative', 'weight': -0.6},
                'Resentment': {'angle': 270, 'type': 'disintegrative', 'weight': -0.8},
                'Manipulation': {'angle': 340, 'type': 'disintegrative', 'weight': -0.8},
                'Tribalism': {'angle': 225, 'type': 'disintegrative', 'weight': -1.0},
                'Fantasy': {'angle': 315, 'type': 'disintegrative', 'weight': -0.6}
            },
            'three_theories_asfa': {
                # Anchor-Set Framework (ASFa) - independent anchors
                'Intersectionality': {'angle': 120, 'type': 'progressive', 'weight': 1.0},
                'Tribal_Domination': {'angle': 240, 'type': 'conservative', 'weight': 1.0},
                'Pluralist_Dignity': {'angle': 0, 'type': 'virtue', 'weight': 1.0}
            },
            'minimal_test': {
                # Simple test case for mathematical validation
                'North': {'angle': 90, 'type': 'integrative', 'weight': 1.0},
                'South': {'angle': 270, 'type': 'disintegrative', 'weight': -1.0},
                'East': {'angle': 0, 'type': 'progressive', 'weight': 0.8},
                'West': {'angle': 180, 'type': 'conservative', 'weight': 0.8}
            }
        }
    
    def _create_test_signatures(self) -> Dict[str, Dict]:
        """Create test axis/anchor signatures for different scenarios."""
        return {
            'extreme_positive': {
                'Hope': 0.9, 'Justice': 0.8, 'Truth': 0.9, 'Dignity': 1.0, 'Pragmatism': 0.7,
                'Fear': 0.1, 'Resentment': 0.0, 'Manipulation': 0.1, 'Tribalism': 0.0, 'Fantasy': 0.2
            },
            'extreme_negative': {
                'Hope': 0.2, 'Justice': 0.1, 'Truth': 0.3, 'Dignity': 0.1, 'Pragmatism': 0.3,
                'Fear': 0.9, 'Resentment': 1.0, 'Manipulation': 0.8, 'Tribalism': 0.9, 'Fantasy': 0.7
            },
            'balanced_moderate': {
                'Hope': 0.5, 'Justice': 0.6, 'Truth': 0.5, 'Dignity': 0.6, 'Pragmatism': 0.4,
                'Fear': 0.4, 'Resentment': 0.3, 'Manipulation': 0.4, 'Tribalism': 0.3, 'Fantasy': 0.5
            },
            'single_dominant': {
                'Hope': 0.2, 'Justice': 0.9, 'Truth': 0.1, 'Dignity': 0.3, 'Pragmatism': 0.2,
                'Fear': 0.1, 'Resentment': 0.2, 'Manipulation': 0.1, 'Tribalism': 0.1, 'Fantasy': 0.1
            },
            'mixed_tension': {
                'Hope': 0.7, 'Justice': 0.8, 'Truth': 0.3, 'Dignity': 0.6, 'Pragmatism': 0.4,
                'Fear': 0.6, 'Resentment': 0.4, 'Manipulation': 0.7, 'Tribalism': 0.5, 'Fantasy': 0.3
            }
        }
    
    def rapid_theme_comparison(self, anchor_set: str = 'civic_virtue_asfx', 
                             signature: str = 'extreme_positive') -> Dict[str, str]:
        """
        Rapidly generate the same visualization across all themes.
        
        Args:
            anchor_set: Which anchor configuration to use
            signature: Which test signature to use
            
        Returns:
            Dictionary mapping theme names to output file paths
        """
        self.iteration_count += 1
        print(f"\n🎨 Theme Comparison Iteration #{self.iteration_count}")
        print(f"   Anchor Set: {anchor_set}")
        print(f"   Signature: {signature}")
        
        anchors = self.test_anchors[anchor_set]
        scores = self.test_signatures[signature]
        
        # Filter scores to only include anchors that exist in the anchor set
        filtered_scores = {k: v for k, v in scores.items() if k in anchors}
        
        theme_outputs = {}
        themes = list_themes()
        
        for theme_name in themes:
            print(f"   🎯 Generating {theme_name} theme...")
            
            # Create engine with theme
            engine = create_discernus_visualization_engine(theme=theme_name)
            
            # Generate visualization
            fig = engine.create_single_analysis(
                anchors=anchors,
                axis_scores=filtered_scores,
                title=f'{anchor_set.title()} - {signature.title()} ({theme_name.title()} Theme)',
                show=False
            )
            
            # Save output
            timestamp = datetime.now().strftime("%H%M%S")
            filename = f"theme_comparison_iter{self.iteration_count}_{theme_name}_{timestamp}.html"
            output_path = self.output_dir / filename
            
            fig.write_html(str(output_path))
            theme_outputs[theme_name] = str(output_path)
            
            print(f"      ✅ Saved: {filename}")
        
        # Log this iteration
        self.results_log.append({
            'iteration': self.iteration_count,
            'type': 'theme_comparison',
            'anchor_set': anchor_set,
            'signature': signature,
            'outputs': theme_outputs,
            'timestamp': datetime.now().isoformat()
        })
        
        print(f"✅ Theme comparison complete - {len(theme_outputs)} files generated")
        return theme_outputs
    
    def mathematical_approach_testing(self, approaches: List[str] = None) -> Dict[str, Any]:
        """
        Test different mathematical approaches for centroid calculation.
        
        Args:
            approaches: List of mathematical approaches to test
            
        Returns:
            Dictionary with results from each approach
        """
        if approaches is None:
            approaches = ['standard', 'exponential_weighting', 'adaptive_scaling', 'boundary_snapping']
        
        self.iteration_count += 1
        print(f"\n🧮 Mathematical Approach Testing Iteration #{self.iteration_count}")
        
        # Use extreme signatures to test mathematical differences
        test_cases = ['extreme_positive', 'extreme_negative', 'single_dominant']
        anchors = self.test_anchors['civic_virtue_asfx']
        
        results = {}
        
        for approach in approaches:
            print(f"   🔬 Testing {approach} approach...")
            approach_results = {}
            
            for test_case in test_cases:
                scores = self.test_signatures[test_case]
                filtered_scores = {k: v for k, v in scores.items() if k in anchors}
                
                # Calculate centroid with different mathematical approaches
                engine = create_discernus_visualization_engine(theme='academic')
                
                if approach == 'standard':
                    centroid = engine.calculate_centroid(anchors, filtered_scores)
                elif approach == 'exponential_weighting':
                    centroid = self._calculate_centroid_exponential(anchors, filtered_scores)
                elif approach == 'adaptive_scaling':
                    centroid = self._calculate_centroid_adaptive(anchors, filtered_scores)
                elif approach == 'boundary_snapping':
                    centroid = self._calculate_centroid_boundary_snap(anchors, filtered_scores)
                else:
                    centroid = engine.calculate_centroid(anchors, filtered_scores)
                
                approach_results[test_case] = {
                    'centroid': centroid,
                    'distance_from_center': (centroid[0]**2 + centroid[1]**2)**0.5,
                    'scores': filtered_scores
                }
            
            results[approach] = approach_results
            print(f"      ✅ {approach} complete")
        
        # Generate comparison visualization
        self._visualize_mathematical_comparison(results, anchors)
        
        return results
    
    def _calculate_centroid_exponential(self, anchors: Dict, scores: Dict, base: float = 2.5) -> Tuple[float, float]:
        """Calculate centroid with exponential weighting."""
        import numpy as np
        
        total_x = 0.0
        total_y = 0.0
        total_weight = 0.0
        
        for anchor_name, score in scores.items():
            if anchor_name in anchors:
                anchor = anchors[anchor_name]
                angle = anchor['angle']
                weight = abs(anchor.get('weight', 1.0))
                
                # Exponential weighting
                exp_score = score ** base if score >= 0.1 else 0.0
                
                # Convert angle to radians and calculate position
                angle_rad = np.radians(angle)
                x = np.cos(angle_rad)
                y = np.sin(angle_rad)
                
                # Weight the contribution
                weighted_score = exp_score * weight
                total_x += weighted_score * x
                total_y += weighted_score * y
                total_weight += weighted_score
        
        if total_weight > 0:
            centroid_x = total_x / total_weight
            centroid_y = total_y / total_weight
            
            # Enhanced scaling for exponential approach
            scaling_factor = 0.9
            return (centroid_x * scaling_factor, centroid_y * scaling_factor)
        
        return (0.0, 0.0)
    
    def _calculate_centroid_adaptive(self, anchors: Dict, scores: Dict) -> Tuple[float, float]:
        """Calculate centroid with adaptive scaling based on score distribution."""
        import numpy as np
        
        # Standard calculation first
        total_x = 0.0
        total_y = 0.0
        total_weight = 0.0
        
        for anchor_name, score in scores.items():
            if anchor_name in anchors:
                anchor = anchors[anchor_name]
                angle = anchor['angle']
                weight = abs(anchor.get('weight', 1.0))
                
                angle_rad = np.radians(angle)
                x = np.cos(angle_rad)
                y = np.sin(angle_rad)
                
                weighted_score = score * weight
                total_x += weighted_score * x
                total_y += weighted_score * y
                total_weight += weighted_score
        
        if total_weight > 0:
            centroid_x = total_x / total_weight
            centroid_y = total_y / total_weight
            
            # Adaptive scaling based on extremeness
            max_score = max(scores.values())
            score_variance = np.var(list(scores.values()))
            extremeness = max_score * score_variance
            
            # Scale from 0.6 (diffuse) to 0.95 (focused)
            scaling_factor = 0.6 + (0.35 * min(extremeness / 0.3, 1.0))
            
            return (centroid_x * scaling_factor, centroid_y * scaling_factor)
        
        return (0.0, 0.0)
    
    def _calculate_centroid_boundary_snap(self, anchors: Dict, scores: Dict, snap_threshold: float = 0.8) -> Tuple[float, float]:
        """Calculate centroid with boundary snapping for dominant anchors."""
        import numpy as np
        
        # Find dominant anchor
        max_score = max(scores.values())
        dominant_anchor = None
        
        if max_score >= snap_threshold:
            for anchor_name, score in scores.items():
                if score == max_score and anchor_name in anchors:
                    dominant_anchor = anchor_name
                    break
        
        # Standard calculation
        total_x = 0.0
        total_y = 0.0
        total_weight = 0.0
        
        for anchor_name, score in scores.items():
            if anchor_name in anchors:
                anchor = anchors[anchor_name]
                angle = anchor['angle']
                weight = abs(anchor.get('weight', 1.0))
                
                angle_rad = np.radians(angle)
                x = np.cos(angle_rad)
                y = np.sin(angle_rad)
                
                weighted_score = score * weight
                total_x += weighted_score * x
                total_y += weighted_score * y
                total_weight += weighted_score
        
        if total_weight > 0:
            centroid_x = total_x / total_weight
            centroid_y = total_y / total_weight
            
            # Apply boundary snapping if dominant anchor exists
            if dominant_anchor:
                dominant_anchor_data = anchors[dominant_anchor]
                angle_rad = np.radians(dominant_anchor_data['angle'])
                boundary_x = np.cos(angle_rad)
                boundary_y = np.sin(angle_rad)
                
                # Snap toward boundary
                boundary_proximity = (max_score - snap_threshold) / (1.0 - snap_threshold)
                snap_distance = 0.7 + (0.25 * boundary_proximity)
                
                # Blend calculated position with snapped position
                blend_factor = boundary_proximity * 0.6
                final_x = (1 - blend_factor) * centroid_x + blend_factor * boundary_x * snap_distance
                final_y = (1 - blend_factor) * centroid_y + blend_factor * boundary_y * snap_distance
                
                return (final_x, final_y)
            else:
                # Standard scaling
                return (centroid_x * 0.8, centroid_y * 0.8)
        
        return (0.0, 0.0)
    
    def _visualize_mathematical_comparison(self, results: Dict, anchors: Dict):
        """Create visualization comparing different mathematical approaches."""
        print("   📊 Generating mathematical comparison visualization...")
        
        # Create comparison figure
        fig = go.Figure()
        
        colors = {'standard': 'blue', 'exponential_weighting': 'red', 
                 'adaptive_scaling': 'green', 'boundary_snapping': 'orange'}
        
        # Plot anchor positions
        for anchor_name, anchor_data in anchors.items():
            angle_rad = np.radians(anchor_data['angle'])
            x = np.cos(angle_rad)
            y = np.sin(angle_rad)
            
            fig.add_trace(go.Scatter(
                x=[x], y=[y],
                mode='markers+text',
                text=[anchor_name],
                textposition='middle center',
                marker=dict(size=12, color='gray', symbol='circle'),
                name=anchor_name,
                showlegend=False
            ))
        
        # Plot centroids for each approach and test case
        for approach, approach_results in results.items():
            for test_case, test_data in approach_results.items():
                centroid = test_data['centroid']
                
                fig.add_trace(go.Scatter(
                    x=[centroid[0]], y=[centroid[1]],
                    mode='markers',
                    marker=dict(size=8, color=colors.get(approach, 'black')),
                    name=f'{approach}_{test_case}',
                    showlegend=True
                ))
        
        # Add unit circle
        circle_angles = np.linspace(0, 2*np.pi, 100)
        circle_x = np.cos(circle_angles)
        circle_y = np.sin(circle_angles)
        
        fig.add_trace(go.Scatter(
            x=circle_x, y=circle_y,
            mode='lines',
            line=dict(color='gray', dash='dash'),
            name='Coordinate Boundary',
            showlegend=False
        ))
        
        fig.update_layout(
            title='Mathematical Approach Comparison',
            xaxis=dict(range=[-1.2, 1.2], scaleanchor="y", scaleratio=1),
            yaxis=dict(range=[-1.2, 1.2]),
            width=800, height=800
        )
        
        # Save comparison
        timestamp = datetime.now().strftime("%H%M%S")
        filename = f"mathematical_comparison_iter{self.iteration_count}_{timestamp}.html"
        output_path = self.output_dir / filename
        
        fig.write_html(str(output_path))
        print(f"      ✅ Saved: {filename}")
    
    def hot_reload_development_session(self):
        """
        Interactive development session with hot-reload capabilities.
        """
        print("\n🔥 Hot Reload Development Session Started")
        print("   Commands:")
        print("     'themes' - Compare all themes")
        print("     'math' - Test mathematical approaches")  
        print("     'custom [anchor_set] [signature]' - Custom test")
        print("     'reload' - Reload visualization modules")
        print("     'quit' - Exit session")
        
        while True:
            try:
                command = input("\n🧪 Lab > ").strip().lower()
                
                if command == 'quit':
                    break
                elif command == 'themes':
                    self.rapid_theme_comparison()
                elif command == 'math':
                    self.mathematical_approach_testing()
                elif command == 'reload':
                    self._reload_modules()
                elif command.startswith('custom'):
                    parts = command.split()
                    anchor_set = parts[1] if len(parts) > 1 else 'civic_virtue_asfx'
                    signature = parts[2] if len(parts) > 2 else 'extreme_positive'
                    
                    if anchor_set in self.test_anchors and signature in self.test_signatures:
                        self.rapid_theme_comparison(anchor_set, signature)
                    else:
                        print(f"❌ Invalid anchor_set or signature")
                        print(f"   Available anchor sets: {list(self.test_anchors.keys())}")
                        print(f"   Available signatures: {list(self.test_signatures.keys())}")
                else:
                    print("❌ Unknown command")
                    
            except KeyboardInterrupt:
                print("\n🔴 Session interrupted")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
        
        print("\n✅ Hot Reload Development Session Ended")
        self._generate_session_summary()
    
    def _reload_modules(self):
        """Reload visualization modules for hot development."""
        try:
            import discernus_visualization_engine
            import discernus_themes
            
            importlib.reload(discernus_visualization_engine)
            importlib.reload(discernus_themes)
            
            print("🔄 Modules reloaded successfully")
        except Exception as e:
            print(f"❌ Reload failed: {e}")
    
    def _generate_session_summary(self):
        """Generate summary of the iteration session."""
        if not self.results_log:
            return
        
        summary_file = self.output_dir / f"session_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        summary = {
            'session_info': {
                'total_iterations': self.iteration_count,
                'session_duration': 'calculated_if_needed',
                'total_files_generated': sum(len(r.get('outputs', {})) for r in self.results_log)
            },
            'iterations': self.results_log,
            'test_configurations': {
                'anchor_sets': list(self.test_anchors.keys()),
                'signatures': list(self.test_signatures.keys()),
                'themes_available': list_themes()
            }
        }
        
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"📋 Session summary saved: {summary_file}")


if __name__ == '__main__':
    # Initialize the lab
    lab = VisualizationIterationLab()
    
    print("\n🧪 DISCERNUS VISUALIZATION ITERATION LAB")
    print("=" * 50)
    print("This lab enables rapid iteration on visualization development")
    print("with immediate feedback and production-compatible outputs.")
    print()
    
    # Quick demo
    print("📋 Running quick demo...")
    lab.rapid_theme_comparison('minimal_test', 'single_dominant')
    
    # Start interactive session
    lab.hot_reload_development_session() 