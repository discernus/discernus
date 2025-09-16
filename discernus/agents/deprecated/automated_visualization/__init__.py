"""
AutomatedVisualizationAgent - v8.0 Function Generation
======================================================

Automatically generates Python functions that create publication-ready visualizations
using THIN-compliant delimiter extraction.

THIN Architecture:
- LLM handles semantic understanding of visualization requirements
- Simple regex extraction using proprietary delimiters  
- No complex parsing - raw content in, clean functions out
- Framework-agnostic approach works with any v8.0 specification
"""

from .agent import AutomatedVisualizationAgent

__all__ = ["AutomatedVisualizationAgent"]
