#!/usr/bin/env python3
"""
UniversalNotebookTemplate - v8.0 Jinja2 Template Engine
=======================================================

THIN-compliant template engine for deterministic notebook assembly.
Combines LLM-generated components with generated functions into complete notebooks.

THIN Architecture Principles:
- Minimal coordination logic (<150 lines)
- Deterministic assembly (no LLM calls in template engine)
- Complete data externalization (no embedded datasets)
- Content-addressable storage integration
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from jinja2 import Environment, FileSystemLoader, select_autoescape
from discernus.core.audit_logger import AuditLogger


@dataclass
class DataPath:
    """External data path reference for notebook template."""
    variable_name: str
    file_path: str
    description: str


class UniversalNotebookTemplate:
    """
    THIN-compliant Jinja2 template engine for notebook generation.
    
    Follows v8.0 architecture principles:
    - Deterministic assembly (no LLM intelligence in template)
    - Complete data externalization via content-addressable storage
    - SHA-256 integrity for all generated notebooks
    - Framework-agnostic operation
    """
    
    def __init__(self, audit_logger: Optional[AuditLogger] = None):
        """Initialize universal notebook template engine."""
        self.audit_logger = audit_logger or AuditLogger()
        self.agent_name = "UniversalNotebookTemplate"
        
        # Initialize Jinja2 environment
        template_dir = Path(__file__).parent / "notebook_templates"
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Load universal template
        self.template = self.jinja_env.get_template('universal_notebook_template.py.j2')
        
        # Log template initialization
        self.audit_logger.log_agent_event(
            agent_name=self.agent_name,
            event_type="TEMPLATE_ENGINE_INITIALIZED",
            data={"template_path": str(template_dir)}
        )
    
    def render_notebook(self,
                       experiment_name: str,
                       framework_name: str,
                       document_count: int,
                       analysis_model: str,
                       synthesis_model: str,
                       methodology_section: str,
                       interpretation_section: str,
                       discussion_section: str,
                       derived_metrics_functions: str,
                       statistical_analysis_functions: str,
                       evidence_integration_functions: str,
                       visualization_functions: str,
                       data_paths: List[DataPath]) -> str:
        """
        Render complete research notebook from components.
        
        Args:
            experiment_name: Name of the experiment
            framework_name: Name of the analytical framework
            document_count: Number of documents analyzed
            analysis_model: LLM model used for analysis
            synthesis_model: LLM model used for synthesis
            methodology_section: Generated methodology content
            interpretation_section: Generated interpretation content
            discussion_section: Generated discussion content
            derived_metrics_functions: Generated Python functions
            statistical_analysis_functions: Generated Python functions
            evidence_integration_functions: Generated Python functions
            visualization_functions: Generated Python functions
            data_paths: External data path references
            
        Returns:
            Complete executable notebook as Python string
            
        Raises:
            Exception: On template rendering failure
        """
        try:
            # Log notebook rendering start
            self.audit_logger.log_agent_event(
                agent_name=self.agent_name,
                event_type="NOTEBOOK_RENDERING_START",
                data={
                    "experiment_name": experiment_name,
                    "framework_name": framework_name,
                    "document_count": document_count,
                    "component_count": 4  # methodology, interpretation, discussion, functions
                }
            )
            
            # Prepare template context
            template_context = {
                "experiment_name": experiment_name,
                "framework_name": framework_name,
                "document_count": document_count,
                "analysis_model": analysis_model,
                "synthesis_model": synthesis_model,
                "generation_timestamp": datetime.now(timezone.utc).isoformat(),
                "methodology_section": self._format_section("METHODOLOGY", methodology_section),
                "interpretation_section": self._format_section("RESULTS INTERPRETATION", interpretation_section),
                "discussion_section": self._format_section("DISCUSSION", discussion_section),
                "derived_metrics_functions": derived_metrics_functions,
                "statistical_analysis_functions": statistical_analysis_functions,
                "evidence_integration_functions": evidence_integration_functions,
                "visualization_functions": visualization_functions,
                "data_paths": data_paths
            }
            
            # Render notebook using Jinja2 template
            notebook_content = self.template.render(**template_context)
            
            # Log successful rendering
            self.audit_logger.log_agent_event(
                agent_name=self.agent_name,
                event_type="NOTEBOOK_RENDERING_SUCCESS",
                data={
                    "notebook_length": len(notebook_content),
                    "template_context_keys": list(template_context.keys())
                }
            )
            
            return notebook_content
            
        except Exception as e:
            # Log rendering failure
            self.audit_logger.log_agent_event(
                agent_name=self.agent_name,
                event_type="NOTEBOOK_RENDERING_FAILURE",
                data={"error": str(e), "experiment_name": experiment_name}
            )
            raise Exception(f"Notebook rendering failed: {str(e)}")
    
    def _format_section(self, section_title: str, content: str) -> str:
        """Format section content with consistent headers."""
        return f"""# {section_title}
# ============================================================================

{content}

"""
