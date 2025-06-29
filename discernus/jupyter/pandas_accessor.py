"""
DCS Pandas Accessor for Natural Jupyter Integration

This module implements the pandas accessor pattern to make DCS visualization
feel native to existing data science workflows.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
import warnings


@pd.api.extensions.register_dataframe_accessor("dcs")
class DCSAccessor:
    """
    Pandas accessor for DCS framework visualization.
    
    Usage:
        df.dcs.suggest_frameworks()
        df.dcs.tamaki_fuks().plot()
        df.dcs.auto_detect().show()
    """
    
    def __init__(self, pandas_obj):
        self._obj = pandas_obj
        self._detected_patterns = None
        
    def suggest_frameworks(self) -> Dict[str, Any]:
        """
        Analyze DataFrame structure and suggest appropriate DCS frameworks.
        
        Returns:
            Dict with suggested frameworks and confidence scores
        """
        patterns = self._analyze_data_patterns()
        suggestions = self._match_frameworks(patterns)
        
        print("🎯 Detected data patterns:")
        for pattern, details in patterns.items():
            print(f"   • {pattern}: {details}")
        
        print("\n📋 Recommended frameworks:")
        for i, (framework, info) in enumerate(suggestions.items(), 1):
            star = " ⭐" if info['confidence'] > 0.8 else ""
            print(f"   {i}. {framework}{star} (confidence: {info['confidence']:.1f})")
            print(f"      - {info['description']}")
        
        return suggestions
    
    def auto_detect(self):
        """
        Automatically detect the best framework for this data.
        
        Returns:
            DCSVisualization instance with intelligent defaults
        """
        patterns = self._analyze_data_patterns()
        best_framework = self._select_best_framework(patterns)
        
        if best_framework:
            return getattr(self, best_framework)()
        else:
            raise DCSFrameworkError(
                "Could not auto-detect appropriate framework for this data.\n"
                "Try: df.dcs.suggest_frameworks() for manual selection."
            )
    
    def tamaki_fuks(self, **kwargs):
        """
        Apply Tamaki & Fuks Competitive Populism framework.
        
        Args:
            **kwargs: Framework configuration options
            
        Returns:
            DCSVisualization configured for competitive populism analysis
        """
        required_cols = ['populism_score', 'nationalism_score', 'patriotism_score']
        self._validate_columns(required_cols, 'tamaki_fuks')
        
        from discernus.visualization.advanced_plotly_dcs import AdvancedDCSVisualizer
        
        # Configure anchors for Tamaki & Fuks framework
        anchors = {
            'populism': {'angle': 0, 'type': 'populist_ideology', 'weight': 1.0},
            'patriotism': {'angle': 120, 'type': 'state_ideology', 'weight': 1.0},
            'nationalism': {'angle': 240, 'type': 'nation_ideology', 'weight': 1.0}
        }
        
        # Create visualization wrapper
        return DCSVisualization(
            data=self._obj,
            framework='tamaki_fuks',
            anchors=anchors,
            visualizer=AdvancedDCSVisualizer(),
            **kwargs
        )
    
    def moral_foundations(self, **kwargs):
        """
        Apply Moral Foundations Theory framework.
        """
        required_cols = ['care', 'fairness', 'loyalty', 'authority', 'sanctity']
        self._validate_columns(required_cols, 'moral_foundations')
        
        # Implementation would follow similar pattern
        return DCSVisualization(
            data=self._obj,
            framework='moral_foundations',
            anchors=self._get_mft_anchors(),
            **kwargs
        )
    
    def political_worldview(self, **kwargs):
        """
        Apply Political Worldview Triad framework.
        """
        # Implementation for worldview framework
        pass
    
    def _analyze_data_patterns(self) -> Dict[str, Any]:
        """Analyze DataFrame to detect DCS-relevant patterns."""
        patterns = {}
        
        # Detect ideological dimensions
        ideological_cols = self._detect_ideological_columns()
        if ideological_cols:
            patterns['ideological_dimensions'] = f"{len(ideological_cols)} found: {', '.join(ideological_cols)}"
        
        # Detect temporal data
        temporal_cols = self._detect_temporal_columns()
        if temporal_cols:
            patterns['temporal_data'] = f"date column detected: {temporal_cols[0]}"
        
        # Detect sample size
        patterns['sample_size'] = f"{len(self._obj)} observations"
        
        # Detect score ranges
        numeric_cols = self._obj.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            score_range = (self._obj[numeric_cols].min().min(), self._obj[numeric_cols].max().max())
            patterns['score_range'] = f"{score_range[0]:.2f} to {score_range[1]:.2f}"
        
        return patterns
    
    def _detect_ideological_columns(self) -> List[str]:
        """Detect columns that appear to contain ideological scores."""
        ideological_keywords = [
            'populism', 'nationalism', 'patriotism',
            'care', 'fairness', 'loyalty', 'authority', 'sanctity',
            'liberal', 'conservative', 'progressive'
        ]
        
        detected = []
        for col in self._obj.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in ideological_keywords):
                detected.append(col)
        
        return detected
    
    def _detect_temporal_columns(self) -> List[str]:
        """Detect columns that contain temporal data."""
        temporal_keywords = ['date', 'time', 'timestamp', 'year', 'month']
        
        detected = []
        for col in self._obj.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in temporal_keywords):
                detected.append(col)
            # Also check if column contains datetime-like data
            elif pd.api.types.is_datetime64_any_dtype(self._obj[col]):
                detected.append(col)
        
        return detected
    
    def _match_frameworks(self, patterns: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Match detected patterns to appropriate frameworks."""
        suggestions = {}
        
        ideological_dims = patterns.get('ideological_dimensions', '')
        
        # Tamaki & Fuks framework matching
        if all(dim in ideological_dims.lower() for dim in ['populism', 'nationalism', 'patriotism']):
            suggestions['tamaki_fuks_competitive_populism'] = {
                'confidence': 0.95,
                'description': 'Perfect match - handles populism/nationalism/patriotism triangle',
                'supports_temporal': 'temporal_data' in patterns
            }
        
        # Moral Foundations Theory matching
        mft_dims = ['care', 'fairness', 'loyalty', 'authority', 'sanctity']
        if sum(dim in ideological_dims.lower() for dim in mft_dims) >= 3:
            confidence = sum(dim in ideological_dims.lower() for dim in mft_dims) / len(mft_dims)
            suggestions['moral_foundations_theory'] = {
                'confidence': confidence,
                'description': f'Good match - {int(confidence*5)} of 5 MFT dimensions detected'
            }
        
        return suggestions
    
    def _select_best_framework(self, patterns: Dict[str, Any]) -> Optional[str]:
        """Select the best framework based on detected patterns."""
        suggestions = self._match_frameworks(patterns)
        
        if not suggestions:
            return None
        
        # Return framework with highest confidence
        best = max(suggestions.items(), key=lambda x: x[1]['confidence'])
        return best[0].split('_')[0] + '_' + best[0].split('_')[1]  # Convert to method name
    
    def _validate_columns(self, required_cols: List[str], framework_name: str):
        """Validate that required columns exist for a framework."""
        missing_cols = [col for col in required_cols if col not in self._obj.columns]
        
        if missing_cols:
            available_cols = [col for col in required_cols if col in self._obj.columns]
            
            error_msg = f"❌ {framework_name.replace('_', ' ').title()} framework requires {len(required_cols)} dimensions but found {len(available_cols)}\n\n"
            
            error_msg += "📋 Required columns:\n"
            for col in required_cols:
                status = "✅" if col in self._obj.columns else "❌"
                found_text = "(found)" if col in self._obj.columns else "(missing)"
                error_msg += f"   • {col} {status} {found_text}\n"
            
            error_msg += "\n💡 Suggestions:\n"
            error_msg += "   1. Add missing columns to your DataFrame\n"
            error_msg += f"   2. Try a different framework: df.dcs.suggest_frameworks()\n"
            error_msg += "   3. Use auto-detection: df.dcs.auto_detect()\n"
            
            raise DCSFrameworkError(error_msg)


class DCSVisualization:
    """
    Wrapper class for DCS visualization with fluent interface.
    """
    
    def __init__(self, data, framework, anchors, visualizer=None, **kwargs):
        self.data = data
        self.framework = framework
        self.anchors = anchors
        self.visualizer = visualizer
        self.config = kwargs
        self._title = None
        self._competitive_dynamics = False
        self._temporal_analysis = False
        
    def title(self, title: str):
        """Set visualization title."""
        self._title = title
        return self
    
    def add_competitive_dynamics(self, strength: float = 0.8):
        """Add competitive dynamics analysis."""
        self._competitive_dynamics = True
        self.config['competition_strength'] = strength
        return self
    
    def add_temporal_analysis(self):
        """Add temporal evolution analysis."""
        self._temporal_analysis = True
        return self
    
    def highlight_trends(self):
        """Highlight trends in the visualization."""
        self.config['highlight_trends'] = True
        return self
    
    def add_velocity_vectors(self):
        """Add velocity vectors showing temporal progression."""
        self.config['velocity_vectors'] = True
        return self
    
    def emphasize_temporal_progression(self):
        """Emphasize temporal progression in visualization."""
        self.config['temporal_emphasis'] = True
        return self
    
    def configure_anchors(self, config):
        """Configure anchor positioning and properties."""
        self.config['anchor_config'] = config
        return self
    
    def custom_layout(self, **kwargs):
        """Apply custom layout configuration."""
        self.config.update(kwargs)
        return self
    
    def plot(self):
        """Generate the DCS visualization."""
        if not self.visualizer:
            raise DCSFrameworkError("No visualizer configured")
        
        # Convert DataFrame to the format expected by visualizer
        signature_scores = self._extract_signature_scores()
        
        # Generate appropriate visualization based on framework
        if self.framework == 'tamaki_fuks':
            if self._temporal_analysis and self._has_temporal_data():
                return self._create_temporal_visualization(signature_scores)
            elif self._competitive_dynamics:
                return self._create_competitive_visualization(signature_scores)
            else:
                return self._create_basic_visualization(signature_scores)
        
        return None
    
    def show(self):
        """Display the visualization."""
        fig = self.plot()
        if fig:
            fig.show()
        return None  # Don't return self to avoid auto-display in Jupyter
    
    def export(self, filename: str, style: str = 'academic', dpi: int = 300):
        """Export visualization to file."""
        fig = self.plot()
        if fig:
            if filename.endswith('.html'):
                fig.write_html(filename)
            elif filename.endswith('.png'):
                fig.write_image(filename, width=1200, height=800, scale=dpi/100)
            elif filename.endswith('.pdf'):
                fig.write_image(filename, format='pdf', width=1200, height=800)
        return self
    
    def _extract_signature_scores(self) -> Dict[str, float]:
        """Extract signature scores from DataFrame."""
        if self.framework == 'tamaki_fuks':
            # Take the mean of scores if multiple rows
            scores = {}
            for anchor in ['populism', 'nationalism', 'patriotism']:
                col_name = f"{anchor}_score"
                if col_name in self.data.columns:
                    scores[anchor] = self.data[col_name].mean()
            return scores
        return {}
    
    def _has_temporal_data(self) -> bool:
        """Check if data contains temporal information."""
        temporal_cols = ['date', 'time', 'timestamp', 'year', 'month']
        return any(col in self.data.columns for col in temporal_cols)
    
    def _create_basic_visualization(self, signature_scores):
        """Create basic DCS visualization."""
        return self.visualizer.plot(
            anchors=self.anchors,
            signature_scores=signature_scores,
            title=self._title or f"{self.framework.replace('_', ' ').title()} Analysis"
        )
    
    def _create_competitive_visualization(self, signature_scores):
        """Create competitive dynamics visualization."""
        competition_config = {
            'competition_pairs': [
                {'anchors': ['populism', 'patriotism'], 'strength': self.config.get('competition_strength', 0.8)},
                {'anchors': ['populism', 'nationalism'], 'strength': 0.6},
                {'anchors': ['patriotism', 'nationalism'], 'strength': 0.4}
            ]
        }
        
        return self.visualizer.plot_competitive_dynamics(
            anchors=self.anchors,
            competition_config=competition_config,
            signature_scores=signature_scores,
            title=self._title or "Competitive Dynamics Analysis"
        )
    
    def _create_temporal_visualization(self, signature_scores):
        """Create temporal evolution visualization."""
        # Convert DataFrame rows to temporal data format
        temporal_data = []
        for idx, row in self.data.iterrows():
            temporal_data.append({
                'timestamp': str(idx),
                'signature_scores': {
                    'populism': row.get('populism_score', 0),
                    'nationalism': row.get('nationalism_score', 0),
                    'patriotism': row.get('patriotism_score', 0)
                }
            })
        
        return self.visualizer.plot_temporal_evolution(
            anchors=self.anchors,
            temporal_data=temporal_data,
            title=self._title or "Temporal Evolution Analysis"
        )


class DCSFrameworkError(Exception):
    """Custom exception for DCS framework errors."""
    
    def show_example_data(self):
        """Show example data format for the framework."""
        example = pd.DataFrame({
            'speech_id': ['speech_1', 'speech_2', 'speech_3'],
            'populism_score': [0.6, 0.8, 0.4],
            'nationalism_score': [0.7, 0.5, 0.9],
            'patriotism_score': [0.3, 0.6, 0.2],
            'date': ['2018-07', '2018-08', '2018-09']
        })
        
        print("\n📖 Example data format:")
        print(example.to_string(index=False))
        print("\nThen use: df.dcs.tamaki_fuks().plot()")
        
        return example 