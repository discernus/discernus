"""
Discernus Pipeline Package

Production pipeline code for experiment execution and Stage 6 notebook generation.
Moved from templates/ to proper Python package structure.
"""

from .notebook_generation import generate_stage6_notebook, select_template_pattern

__all__ = ['generate_stage6_notebook', 'select_template_pattern'] 