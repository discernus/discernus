"""
Notebook Generation Module

Handles automatic generation of Stage 6 analysis notebooks from templates.
Core production code for the experiment → notebook handoff.
"""

from .notebook_generator import generate_stage6_notebook
from .template_selector import select_template_pattern, get_template_info, validate_template_compatibility

__all__ = [
    'generate_stage6_notebook', 
    'select_template_pattern', 
    'get_template_info', 
    'validate_template_compatibility'
] 