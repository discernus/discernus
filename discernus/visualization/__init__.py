"""
Advanced DCS Visualization Module
================================

This module provides enhanced visualization capabilities for the Discernus Coordinate System,
implementing the advanced visualization types specified in Framework Specification v3.2.

Core Visualization Classes:
- AdvancedDCSVisualizer: Enhanced circular plots with theoretical weighting
- TemporalAnalysisVisualizer: Time-series DCS plotting capabilities  
- CompetitiveDynamicsVisualizer: Competition relationship visualization
- TheoreticalWeightingVisualizer: Theoretical weighting heatmaps
- FrameworkComparisonVisualizer: Multi-framework comparison tools
"""

from .advanced_plotly_dcs import AdvancedDCSVisualizer
from .theoretical_weighting_viz import TheoreticalWeightingVisualizer
from .dcs_plots import (
    plot_dcs_framework,
    plot_coordinate_space,
    plot_competitive_dynamics,
    plot_temporal_evolution,
    setup_publication_style,
    extract_framework_anchors,
    calculate_signature_coordinates
)

__all__ = [
    'AdvancedDCSVisualizer',
    'TheoreticalWeightingVisualizer',
    'plot_dcs_framework',
    'plot_coordinate_space', 
    'plot_competitive_dynamics',
    'plot_temporal_evolution',
    'setup_publication_style',
    'extract_framework_anchors',
    'calculate_signature_coordinates'
]

"""
Discernus Visualization Module

Provides distinctive identity with seamless academic compliance.
"""

from .discernus_typography import setup_style, TYPOGRAPHY_PROFILES

# Simple interface for immediate use
def discernus_style():
    """Apply distinctive Discernus identity styling"""
    setup_style('discernus')

def nature_style():
    """Apply Nature journal compliance styling"""
    setup_style('nature')

def science_style():
    """Apply Science journal compliance styling"""
    setup_style('science')

# Export key functions  
__all__.extend(['setup_style', 'discernus_style', 'nature_style', 'science_style', 'TYPOGRAPHY_PROFILES']) 