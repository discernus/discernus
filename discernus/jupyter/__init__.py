"""
Jupyter integration module for Discernus DCS.

This module provides natural integration with Jupyter notebooks through:
- Pandas accessor for DataFrame.dcs operations
- IPython magic commands for framework discovery
- Interactive widgets for visual framework building
"""

from .pandas_accessor import DCSAccessor, DCSVisualization, DCSFrameworkError

__all__ = ['DCSAccessor', 'DCSVisualization', 'DCSFrameworkError'] 