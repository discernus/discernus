#!/usr/bin/env python3
"""
NotebookInterpretationAgent - v8.0 Academic Results Interpretation
================================================================

THIN-compliant agent for generating academic results interpretation sections.
Maintains token limit compliance (<1000 tokens) while producing peer-review quality content.

THIN Architecture Principles:
- External YAML prompt templates (intelligence externalized)
- Minimal coordination logic (<150 lines)
- LLM handles all domain knowledge and academic interpretation
- Complete audit logging for provenance
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional

from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry
from discernus.core.audit_logger import AuditLogger


class NotebookInterpretationAgent:
    """
    THIN-compliant agent for generating academic results interpretation sections.
    
    Follows v8.0 architecture principles:
    - External YAML prompts for intelligence externalization
    - Token-limit compliance (<1000 tokens output)
    - Complete audit logging for academic provenance
    - Framework-agnostic operation
    """
    
    def __init__(self, model: str = "vertex_ai/gemini-2.5-flash", audit_logger: Optional[AuditLogger] = None):
        """Initialize interpretation generation agent."""
        self.model = model
        self.audit_logger = audit_logger or AuditLogger()
        self.agent_name = "NotebookInterpretationAgent"
        
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
    
    def generate_interpretation(self, 
                              framework_name: str,
                              experiment_name: str,
                              document_count: int,
                              statistical_summary: str,
                              key_findings: str) -> str:
        """
        Generate academic results interpretation section for research notebook.
        
        Args:
            framework_name: Name of the analytical framework
            experiment_name: Name of the experiment
            document_count: Number of documents analyzed
            statistical_summary: Summary of statistical results
            key_findings: Key findings from analysis
            
        Returns:
            Academic interpretation section (<1000 tokens)
            
        Raises:
            Exception: On generation failure
        """
        try:
            # Log interpretation generation start
            self.audit_logger.log_agent_event(
                agent_name=self.agent_name,
                event_type="INTERPRETATION_GENERATION_START",
                data={
                    "framework_name": framework_name,
                    "experiment_name": experiment_name,
                    "document_count": document_count
                }
            )
            
            # Format prompt with results context
            formatted_prompt = self.prompt_template.format(
                framework_name=framework_name,
                experiment_name=experiment_name,
                document_count=document_count,
                statistical_summary=statistical_summary[:1500],  # Limit for token management
                key_findings=key_findings[:1000]  # Limit for token management
            )
            
            # Generate interpretation using LLM
            interpretation_content, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=formatted_prompt,
                system_prompt="You are an expert academic researcher interpreting statistical results for computational social science papers."
            )
            
            # Validate token limit compliance
            estimated_tokens = len(interpretation_content.split()) * 1.3  # Rough token estimation
            if estimated_tokens > 1000:
                self.audit_logger.log_agent_event(
                    agent_name=self.agent_name,
                    event_type="TOKEN_LIMIT_WARNING",
                    data={"estimated_tokens": estimated_tokens, "limit": 1000}
                )
            
            # Log successful generation
            self.audit_logger.log_agent_event(
                agent_name=self.agent_name,
                event_type="INTERPRETATION_GENERATION_SUCCESS",
                data={
                    "content_length": len(interpretation_content),
                    "estimated_tokens": estimated_tokens,
                    "llm_metadata": metadata
                }
            )
            
            return interpretation_content
            
        except Exception as e:
            # Log generation failure
            self.audit_logger.log_agent_event(
                agent_name=self.agent_name,
                event_type="INTERPRETATION_GENERATION_FAILURE",
                data={"error": str(e), "framework_name": framework_name}
            )
            raise Exception(f"Interpretation generation failed: {str(e)}")
