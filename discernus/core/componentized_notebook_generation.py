#!/usr/bin/env python3
"""
ComponentizedNotebookGeneration - v8.0 Token-Limit Compliant Orchestrator
=========================================================================

THIN-compliant orchestrator for generating notebook components within token limits.
Coordinates specialized agents to produce academic-quality notebook sections.

THIN Architecture Principles:
- Minimal coordination logic (<150 lines)
- External YAML prompts for all LLM interactions
- Token-limit compliance through componentized generation
- Complete audit logging for academic provenance
"""

from pathlib import Path
from typing import Dict, Any, Optional, List

from discernus.core.audit_logger import AuditLogger
from discernus.core.universal_notebook_template import UniversalNotebookTemplate, DataPath
from discernus.agents.notebook_methodology_agent import NotebookMethodologyAgent
from discernus.agents.notebook_interpretation_agent import NotebookInterpretationAgent
from discernus.agents.notebook_discussion_agent import NotebookDiscussionAgent


class ComponentizedNotebookGeneration:
    """
    THIN-compliant orchestrator for componentized notebook generation.
    
    Follows v8.0 architecture principles:
    - Token-limit compliance through specialized agents
    - Complete data externalization (no embedded datasets)
    - Deterministic assembly of LLM-generated components
    - Framework-agnostic operation
    """
    
    def __init__(self, 
                 analysis_model: str = "vertex_ai/gemini-2.5-flash",
                 synthesis_model: str = "vertex_ai/gemini-2.5-pro",
                 audit_logger: Optional[AuditLogger] = None):
        """Initialize componentized notebook generation orchestrator."""
        self.analysis_model = analysis_model
        self.synthesis_model = synthesis_model
        self.audit_logger = audit_logger or AuditLogger()
        self.agent_name = "ComponentizedNotebookGeneration"
        
        # Initialize specialized agents
        self.methodology_agent = NotebookMethodologyAgent(model=analysis_model, audit_logger=audit_logger)
        self.interpretation_agent = NotebookInterpretationAgent(model=analysis_model, audit_logger=audit_logger)
        self.discussion_agent = NotebookDiscussionAgent(model=analysis_model, audit_logger=audit_logger)
        
        # Initialize template engine
        self.template_engine = UniversalNotebookTemplate(audit_logger=audit_logger)
        
        # Log orchestrator initialization
        self.audit_logger.log_agent_event(
            agent_name=self.agent_name,
            event_type="ORCHESTRATOR_INITIALIZED",
            data={
                "analysis_model": analysis_model,
                "synthesis_model": synthesis_model,
                "agent_count": 3
            }
        )
    
    def generate_complete_notebook(self,
                                 experiment_name: str,
                                 framework_name: str,
                                 framework_content: str,
                                 document_count: int,
                                 generated_functions: Dict[str, str],
                                 data_paths: List[DataPath],
                                 statistical_summary: str = "",
                                 key_findings: str = "",
                                 research_context: str = "") -> str:
        """
        Generate complete research notebook using componentized approach.
        
        Args:
            experiment_name: Name of the experiment
            framework_name: Name of the analytical framework
            framework_content: Raw framework specification content
            document_count: Number of documents analyzed
            generated_functions: Dictionary of generated Python functions
            data_paths: External data path references
            statistical_summary: Summary of statistical results
            key_findings: Key findings from analysis
            research_context: Broader research context
            
        Returns:
            Complete executable notebook as Python string
            
        Raises:
            Exception: On generation failure
        """
        try:
            # Log notebook generation start
            self.audit_logger.log_agent_event(
                agent_name=self.agent_name,
                event_type="NOTEBOOK_GENERATION_START",
                data={
                    "experiment_name": experiment_name,
                    "framework_name": framework_name,
                    "document_count": document_count
                }
            )
            
            # Generate methodology section (<800 tokens)
            methodology_section = self.methodology_agent.generate_methodology(
                framework_content=framework_content,
                experiment_name=experiment_name,
                framework_name=framework_name,
                document_count=document_count,
                analysis_model=self.analysis_model
            )
            
            # Generate interpretation section (<1000 tokens)
            interpretation_section = self.interpretation_agent.generate_interpretation(
                framework_name=framework_name,
                experiment_name=experiment_name,
                document_count=document_count,
                statistical_summary=statistical_summary,
                key_findings=key_findings
            )
            
            # Generate discussion section (<800 tokens)
            discussion_section = self.discussion_agent.generate_discussion(
                framework_name=framework_name,
                experiment_name=experiment_name,
                document_count=document_count,
                key_interpretations=interpretation_section[:1000],  # Use generated interpretation as input
                research_context=research_context
            )
            
            # Render complete notebook using template engine
            complete_notebook = self.template_engine.render_notebook(
                experiment_name=experiment_name,
                framework_name=framework_name,
                document_count=document_count,
                analysis_model=self.analysis_model,
                synthesis_model=self.synthesis_model,
                methodology_section=methodology_section,
                interpretation_section=interpretation_section,
                discussion_section=discussion_section,
                derived_metrics_functions=generated_functions.get('derived_metrics', ''),
                statistical_analysis_functions=generated_functions.get('statistical_analysis', ''),
                evidence_integration_functions=generated_functions.get('evidence_integration', ''),
                visualization_functions=generated_functions.get('visualization', ''),
                data_paths=data_paths
            )
            
            # Log successful generation
            self.audit_logger.log_agent_event(
                agent_name=self.agent_name,
                event_type="NOTEBOOK_GENERATION_SUCCESS",
                data={
                    "notebook_length": len(complete_notebook),
                    "sections_generated": 3,  # methodology, interpretation, discussion
                    "functions_integrated": len(generated_functions)
                }
            )
            
            return complete_notebook
            
        except Exception as e:
            # Log generation failure
            self.audit_logger.log_agent_event(
                agent_name=self.agent_name,
                event_type="NOTEBOOK_GENERATION_FAILURE",
                data={"error": str(e), "experiment_name": experiment_name}
            )
            raise Exception(f"Componentized notebook generation failed: {str(e)}")
