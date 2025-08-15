#!/usr/bin/env python3
"""
AutomatedDerivedMetricsAgent - v8.0 Function Generation
======================================================

Automatically generates Python calculation functions from natural language 
framework specifications using THIN-compliant delimiter extraction.

THIN Architecture:
- LLM handles semantic understanding of calculation requirements
- Simple regex extraction using proprietary delimiters  
- No complex parsing - raw content in, clean functions out
- Framework-agnostic approach works with any v8.0 specification

Success Criteria:
- 95%+ function generation success rate
- 99%+ mathematical accuracy in generated calculations
- Clean, executable Python functions with proper error handling
"""

import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime, timezone

from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry
from discernus.core.thin_output_extraction import ThinOutputExtractor
from discernus.core.audit_logger import AuditLogger


class AutomatedDerivedMetricsAgent:
    """
    Generates Python calculation functions from natural language framework descriptions.
    
    THIN Approach:
    1. Read raw framework content (no parsing)
    2. Pass to LLM with calculation generation prompt
    3. Extract clean functions using proprietary delimiters
    4. Validate and save to transactional workspace
    """
    
    def __init__(self, 
                 model: str = "vertex_ai/gemini-2.5-flash",
                 audit_logger: AuditLogger = None):
        """
        Initialize automated derived metrics agent.
        
        Args:
            model: LLM model for function generation
            audit_logger: Audit logger for transaction tracking
        """
        self.model = model
        self.agent_name = "AutomatedDerivedMetricsAgent"
        self.audit_logger = audit_logger
        
        # Initialize LLM gateway
        model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(model_registry)
        
        # Initialize THIN output extractor
        self.extractor = ThinOutputExtractor()
    
    def generate_functions(self, workspace_path: Path) -> Dict[str, Any]:
        """
        Generate derived metrics functions from framework specifications.
        
        Args:
            workspace_path: Transactional workspace for reading inputs and writing outputs
            
        Returns:
            Generation result with function details
            
        Raises:
            Exception: On function generation failure
        """
        self._log_event("FUNCTION_GENERATION_START", {
            "workspace": str(workspace_path),
            "model": self.model
        })
        
        try:
            # Read raw framework content from workspace
            framework_content = (workspace_path / "framework_content.md").read_text()
            experiment_spec = json.loads((workspace_path / "experiment_spec.json").read_text())
            
            self._log_event("INPUTS_LOADED", {
                "framework_size": len(framework_content),
                "experiment_name": experiment_spec.get("name", "unknown")
            })
            
            # Generate calculation functions using LLM
            generated_functions = self._generate_calculation_functions(
                framework_content, 
                experiment_spec
            )
            
            # Extract clean functions using THIN delimiter approach
            extracted_functions = self.extractor.extract_code_blocks(generated_functions)
            
            if not extracted_functions:
                raise ValueError("No functions extracted from LLM response")
            
            # Combine all functions into single module
            function_module = self._create_function_module(extracted_functions, experiment_spec)
            
            # Save to workspace
            output_file = workspace_path / "automatedderivedmetricsagent_functions.py"
            output_file.write_text(function_module)
            
            self._log_event("FUNCTION_GENERATION_SUCCESS", {
                "functions_extracted": len(extracted_functions),
                "output_file": str(output_file.name),
                "module_size": len(function_module)
            })
            
            return {
                "status": "success",
                "functions_generated": len(extracted_functions),
                "output_file": str(output_file.name),
                "module_size": len(function_module)
            }
            
        except Exception as e:
            self._log_event("FUNCTION_GENERATION_FAILED", {
                "error": str(e),
                "workspace": str(workspace_path)
            })
            raise
    
    def _load_prompt_template(self) -> str:
        """Load external YAML prompt template following THIN architecture."""
        import os
        import yaml
        
        # Find prompt.yaml in agent directory
        agent_dir = os.path.dirname(__file__)
        prompt_path = os.path.join(agent_dir, 'prompt.yaml')
        
        if not os.path.exists(prompt_path):
            raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
        
        # Load prompt template
        with open(prompt_path, 'r') as f:
            prompt_content = f.read()
            prompt_data = yaml.safe_load(prompt_content)
        
        if 'template' not in prompt_data:
            raise ValueError(f"Prompt file missing 'template' key: {prompt_path}")
        
        return prompt_data['template']

    def _generate_calculation_functions(self, framework_content: str, experiment_spec: Dict[str, Any]) -> str:
        """Generate calculation functions using LLM with THIN delimiter output."""
        # Load external prompt template
        prompt_template = self._load_prompt_template()
        
        # Format prompt with experiment data
        prompt = prompt_template.format(
            framework_content=framework_content,
            experiment_name=experiment_spec.get('name', 'Unknown'),
            experiment_description=experiment_spec.get('description', 'No description')
        )

        try:
            response_text, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=prompt,
                system_prompt="You are an expert Python developer generating calculation functions for research frameworks.",
                temperature=0.1,
                max_tokens=4000
            )
            
            return response_text
            
        except Exception as e:
            self._log_event("LLM_GENERATION_FAILED", {"error": str(e)})
            raise
    
    def _create_function_module(self, functions: List[str], experiment_spec: Dict[str, Any]) -> str:
        """Create complete Python module with all generated functions."""
        header = f'''"""
Automated Derived Metrics Functions
===================================

Generated by AutomatedDerivedMetricsAgent for experiment: {experiment_spec.get('name', 'Unknown')}
Description: {experiment_spec.get('description', 'No description')}
Generated: {datetime.now(timezone.utc).isoformat()}

This module contains automatically generated calculation functions for derived metrics
as specified in the framework's natural language descriptions.
"""

import pandas as pd
import numpy as np
from typing import Optional, Dict, Any


'''
        
        # Combine all functions
        all_functions = '\n\n'.join(functions)
        
        # Add utility function for getting all calculations
        footer = '''

def calculate_all_derived_metrics(data: pd.DataFrame) -> Dict[str, Optional[float]]:
    """
    Calculate all derived metrics for the given dataset.
    
    Args:
        data: pandas DataFrame with dimension scores
        
    Returns:
        Dictionary mapping metric names to calculated values
    """
    results = {}
    
    # Get all calculation functions from this module
    import inspect
    current_module = inspect.getmodule(inspect.currentframe())
    
    for name, obj in inspect.getmembers(current_module):
        if (inspect.isfunction(obj) and 
            name.startswith('calculate_') and 
            name != 'calculate_all_derived_metrics'):
            try:
                results[name.replace('calculate_', '')] = obj(data)
            except Exception as e:
                results[name.replace('calculate_', '')] = None
                
    return results
'''
        
        return header + all_functions + footer
    
    def _log_event(self, event_type: str, details: Dict[str, Any]) -> None:
        """Log agent event to audit logger."""
        if self.audit_logger:
            self.audit_logger.log_agent_event(
                self.agent_name,
                event_type,
                details
            )
