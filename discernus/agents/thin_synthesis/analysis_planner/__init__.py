"""
AnalysisPlanner: LLM agent for generating declarative mathematical analysis plans.

This agent replaces the AnalyticalCodeGenerator by outputting structured JSON
specifications of what mathematical operations to perform, rather than generating
arbitrary Python code.
"""

from .agent import AnalysisPlanner

__all__ = ['AnalysisPlanner'] 