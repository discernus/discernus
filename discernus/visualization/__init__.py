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

__all__ = [
    'AdvancedDCSVisualizer',
    'TheoreticalWeightingVisualizer'
] 