#!/usr/bin/env python3
"""
NotebookMethodologyAgent - v8.0 Academic Methodology Generation
==============================================================

THIN-compliant agent for generating academic methodology sections in research notebooks.
Maintains token limit compliance (<800 tokens) while producing peer-review quality content.

THIN Architecture Principles:
- External YAML prompt templates (intelligence externalized)
- Minimal coordination logic (<150 lines)
- LLM handles all domain knowledge and academic writing
- Complete audit logging for provenance
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional

from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry
from discernus.core.audit_logger import AuditLogger


class NotebookMethodologyAgent:
    """
    THIN-compliant agent for generating academic methodology sections.
    
    Follows v8.0 architecture principles:
    - External YAML prompts for intelligence externalization
    - Token-limit compliance (<800 tokens output)
    - Complete audit logging for academic provenance
    - Framework-agnostic operation
    """
    
    def __init__(self, model: str = "vertex_ai/gemini-2.5-flash", audit_logger: Optional[AuditLogger] = None):
        """Initialize methodology generation agent."""
        self.model = model
        self.audit_logger = audit_logger or AuditLogger()
        self.agent_name = "NotebookMethodologyAgent"
        
        # Initialize LLM gateway
        model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(model_registry)
        
        # Load external YAML prompt (THIN principle)
        self.prompt_template = self._load_yaml_prompt()
        
        # Log agent initialization
        self.audit_logger.log_agent_event(
            agent_name=self.agent_name,
            event_type="AGENT_INITIALIZED",
            data={"model": self.model}
        )
    
    def _load_yaml_prompt(self) -> str:
        """Load externalized YAML prompt template."""
        prompt_path = Path(__file__).parent / "prompt.yaml"
        with open(prompt_path, 'r') as f:
            prompt_data = yaml.safe_load(f)
        return prompt_data['template']
    
    def generate_methodology(self, 
                           framework_content: str,
                           experiment_name: str,
                           framework_name: str,
                           document_count: int,
                           analysis_model: str) -> str:
        """
        Generate academic methodology section for research notebook.
        
        Args:
            framework_content: Raw framework specification content
            experiment_name: Name of the experiment
            framework_name: Name of the analytical framework
            document_count: Number of documents analyzed
            analysis_model: LLM model used for analysis
            
        Returns:
            Academic methodology section (<800 tokens)
            
        Raises:
            Exception: On generation failure
        """
        try:
            # Log methodology generation start
            self.audit_logger.log_agent_event(
                agent_name=self.agent_name,
                event_type="METHODOLOGY_GENERATION_START",
                data={
                    "framework_name": framework_name,
                    "experiment_name": experiment_name,
                    "document_count": document_count,
                    "analysis_model": analysis_model
                }
            )
            
            # Format prompt with experiment context
            formatted_prompt = self.prompt_template.format(
                framework_name=framework_name,
                experiment_name=experiment_name,
                document_count=document_count,
                analysis_model=analysis_model,
                framework_content=framework_content[:2000]  # Limit framework content for token management
            )
            
            # Generate methodology using LLM
            methodology_content, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=formatted_prompt,
                system_prompt="You are an expert academic researcher writing methodology sections for computational social science papers."
            )
            
            # Validate token limit compliance
            estimated_tokens = len(methodology_content.split()) * 1.3  # Rough token estimation
            if estimated_tokens > 800:
                self.audit_logger.log_agent_event(
                    agent_name=self.agent_name,
                    event_type="TOKEN_LIMIT_WARNING",
                    data={"estimated_tokens": estimated_tokens, "limit": 800}
                )
            
            # Log successful generation
            self.audit_logger.log_agent_event(
                agent_name=self.agent_name,
                event_type="METHODOLOGY_GENERATION_SUCCESS",
                data={
                    "content_length": len(methodology_content),
                    "estimated_tokens": estimated_tokens,
                    "llm_metadata": metadata
                }
            )
            
            return methodology_content
            
        except Exception as e:
            # Log generation failure
            self.audit_logger.log_agent_event(
                agent_name=self.agent_name,
                event_type="METHODOLOGY_GENERATION_FAILURE",
                data={"error": str(e), "framework_name": framework_name}
            )
            raise Exception(f"Methodology generation failed: {str(e)}")
