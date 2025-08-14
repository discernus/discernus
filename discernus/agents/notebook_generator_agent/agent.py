"""
Notebook Generator Agent for Epic 401 - Direct Framework Handoff
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional

from discernus.gateway.llm_gateway import LLMGateway
from discernus.core.audit_logger import AuditLogger


class NotebookGenerationResult:
    def __init__(self, success: bool, notebook_path=None, error_message=None, metadata=None):
        self.success = success
        self.notebook_path = notebook_path
        self.error_message = error_message
        self.metadata = metadata or {}


class NotebookGeneratorAgent:
    def __init__(self, audit_logger: AuditLogger, model: str = "vertex_ai/gemini-2.5-pro"):
        self.audit_logger = audit_logger
        self.model = model
        self.llm_gateway = LLMGateway()
    
    def generate_derived_metrics_notebook(self, scores_data, evidence_data, framework_content, experiment_config, output_path):
        """Generate notebook using direct framework handoff - no parsing!"""
        try:
            # Prepare complete input for LLM (direct framework handoff)
            llm_input = self._prepare_llm_input(scores_data, evidence_data, framework_content, experiment_config)
            
            # Generate notebook using LLM
            notebook_content = self._generate_notebook_with_llm(llm_input)
            
            # Save notebook
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                f.write(notebook_content)
            
            # Return success
            metadata = {
                "approach": "direct_framework_handoff",
                "framework_size_bytes": len(framework_content.encode('utf-8'))
            }
            
            return NotebookGenerationResult(
                success=True,
                notebook_path=str(output_path),
                metadata=metadata
            )
            
        except Exception as e:
            return NotebookGenerationResult(
                success=False,
                error_message=str(e)
            )
    
    def _prepare_llm_input(self, scores_data, evidence_data, framework_content, experiment_config):
        """Direct framework handoff - no parsing, just send complete framework to LLM"""
        framework_name = experiment_config.get("framework", "Unknown Framework")
        experiment_name = experiment_config.get("name", "Unknown Experiment")
        
        llm_input = f"""
# Framework Analysis Request

## Framework Content
{framework_content}

## Experiment Context
- **Framework**: {framework_name}
- **Experiment**: {experiment_name}

## Instructions
Generate an executable Python notebook that calculates derived metrics based on this framework.
"""
        return llm_input
    
    def _generate_notebook_with_llm(self, llm_input):
        """Generate notebook using LLM"""
        # Mock implementation for testing
        return f"""# Generated Notebook
# Framework: {llm_input[:100]}...
print("Notebook generated successfully!")
"""
