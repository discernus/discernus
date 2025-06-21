"""
Academic Tool Integration Module - Priority 3 Infrastructure

This module provides academic research tool integration, data export pipelines,
and automated documentation generation for publication-ready research workflows.

Components:
- Data export pipeline for academic formats (CSV, R, Stata, JSON)
- AI-generated analysis templates (Jupyter, R, Stata)
- Academic documentation generators (methodology papers, replication packages)
- Cross-tool workflow orchestration for seamless academic integration
"""

from .data_export import AcademicDataExporter, ReplicationPackageBuilder
from .analysis_templates import JupyterTemplateGenerator, RScriptGenerator, StataIntegration
from .documentation import MethodologyPaperGenerator, StatisticalReportFormatter

__all__ = [
    'AcademicDataExporter',
    'ReplicationPackageBuilder', 
    'JupyterTemplateGenerator',
    'RScriptGenerator',
    'StataIntegration',
    'MethodologyPaperGenerator',
    'StatisticalReportFormatter'
] 