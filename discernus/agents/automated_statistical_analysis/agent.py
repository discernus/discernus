#!/usr/bin/env python3
"""
AutomatedStatisticalAnalysisAgent - v8.0 Function Generation
============================================================

Automatically generates Python statistical analysis functions from experiment 
specifications and framework requirements using THIN-compliant delimiter extraction.

THIN Architecture:
- LLM handles semantic understanding of statistical requirements
- Simple regex extraction using proprietary delimiters  
- No complex parsing - raw content in, clean functions out
- Framework-agnostic approach works with any v8.0 specification

Statistical Focus:
- ANOVA for group comparisons
- Correlation matrices for dimension relationships
- Reliability analysis (Cronbach's alpha)
- Descriptive statistics
- Hypothesis testing functions
- Effect size calculations
"""

import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime, timezone

from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry
from discernus.core.thin_output_extraction import ThinOutputExtractor
from discernus.core.audit_logger import AuditLogger


class AutomatedStatisticalAnalysisAgent:
    """
    Generates Python statistical analysis functions from experiment and framework descriptions.
    
    THIN Approach:
    1. Read raw experiment and framework content (no parsing)
    2. Pass to LLM with statistical analysis generation prompt
    3. Extract clean functions using proprietary delimiters
    4. Validate and save to transactional workspace
    """
    
    def __init__(self, 
                 model: str = "vertex_ai/gemini-2.5-flash",
                 audit_logger: AuditLogger = None):
        """
        Initialize automated statistical analysis agent.
        
        Args:
            model: LLM model for function generation
            audit_logger: Audit logger for transaction tracking
        """
        self.model = model
        self.agent_name = "AutomatedStatisticalAnalysisAgent"
        self.audit_logger = audit_logger
        
        # Initialize LLM gateway
        model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(model_registry)
        
        # Initialize THIN output extractor
        self.extractor = ThinOutputExtractor()
    
    def generate_functions(self, workspace_path: Path) -> Dict[str, Any]:
        """
        Generate statistical analysis functions from experiment and framework specifications.
        
        Args:
            workspace_path: Transactional workspace for reading inputs and writing outputs
            
        Returns:
            Generation result with function details
            
        Raises:
            Exception: On function generation failure
        """
        self._log_event("STATISTICAL_GENERATION_START", {
            "workspace": str(workspace_path),
            "model": self.model
        })
        
        try:
            # Read raw content from workspace
            framework_content = (workspace_path / "framework_content.md").read_text()
            experiment_spec = json.loads((workspace_path / "experiment_spec.json").read_text())
            
            self._log_event("INPUTS_LOADED", {
                "framework_size": len(framework_content),
                "experiment_name": experiment_spec.get("name", "unknown"),
                "questions_count": len(experiment_spec.get("questions", []))
            })
            
            # Generate statistical analysis functions using LLM
            generated_functions = self._generate_statistical_functions(
                framework_content, 
                experiment_spec
            )
            
            # Extract clean functions using THIN delimiter approach
            extracted_functions = self.extractor.extract_code_blocks(generated_functions)
            
            if not extracted_functions:
                # Debug: Log the raw response to understand why extraction failed
                self._log_event("EXTRACTION_DEBUG", {
                    "raw_response_length": len(generated_functions),
                    "raw_response_preview": generated_functions[:1000],
                    "delimiter_start_found": "<<<DISCERNUS_FUNCTION_START>>>" in generated_functions,
                    "delimiter_end_found": "<<<DISCERNUS_FUNCTION_END>>>" in generated_functions
                })
                
                # Try fallback: create a simple descriptive statistics function
                self._log_event("FALLBACK_GENERATION", {"reason": "LLM did not use delimiters"})
                extracted_functions = [self._create_fallback_statistical_function()]
            
            # Combine all functions into single module
            function_module = self._create_statistical_module(extracted_functions, experiment_spec)
            
            # Save to workspace
            output_file = workspace_path / "automatedstatisticalanalysisagent_functions.py"
            output_file.write_text(function_module)
            
            self._log_event("STATISTICAL_GENERATION_SUCCESS", {
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
            self._log_event("STATISTICAL_GENERATION_FAILED", {
                "error": str(e),
                "workspace": str(workspace_path)
            })
            raise
    
    def _generate_statistical_functions(self, framework_content: str, experiment_spec: Dict[str, Any]) -> str:
        """Generate statistical analysis functions using LLM with THIN delimiter output."""
        
        questions = experiment_spec.get("questions", [])
        questions_text = "\n".join([f"- {q}" for q in questions]) if questions else "- No specific research questions provided"
        
        # Load external prompt template
        prompt_template = self._load_prompt_template()
        
        # Format prompt with experiment data
        prompt = prompt_template.format(
            framework_content=framework_content,
            experiment_name=experiment_spec.get('name', 'Unknown'),
            experiment_description=experiment_spec.get('description', 'No description'),
            research_questions=questions_text
        )

        try:
            response_text, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=prompt,
                system_prompt="You are an expert statistician generating comprehensive Python statistical analysis functions for academic research.",
                temperature=0.1,
                max_tokens=6000
            )
            
            return response_text
            
        except Exception as e:
            self._log_event("LLM_STATISTICAL_GENERATION_FAILED", {"error": str(e)})
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
    
    def _create_statistical_module(self, functions: List[str], experiment_spec: Dict[str, Any]) -> str:
        """Create complete Python module with all generated statistical functions."""
        header = f'''"""
Automated Statistical Analysis Functions
========================================

Generated by AutomatedStatisticalAnalysisAgent for experiment: {experiment_spec.get('name', 'Unknown')}
Description: {experiment_spec.get('description', 'No description')}
Generated: {datetime.now(timezone.utc).isoformat()}

This module contains automatically generated statistical analysis functions
for comprehensive data analysis including ANOVA, correlations, reliability,
and hypothesis testing as appropriate for the research questions.
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
from typing import Dict, Any, Optional, List, Tuple
import warnings

# Suppress common statistical warnings for cleaner output
warnings.filterwarnings('ignore', category=RuntimeWarning)


'''
        
        # Combine all functions
        all_functions = '\n\n'.join(functions)
        
        # Add utility function for running all analyses
        footer = '''

def run_complete_statistical_analysis(data: pd.DataFrame, alpha: float = 0.05) -> Dict[str, Any]:
    """
    Run complete statistical analysis suite on the dataset.
    
    Args:
        data: pandas DataFrame with dimension scores
        alpha: Significance level for hypothesis tests (default: 0.05)
        
    Returns:
        Dictionary with all statistical analysis results
    """
    results = {
        'analysis_metadata': {
            'timestamp': pd.Timestamp.now().isoformat(),
            'sample_size': len(data),
            'alpha_level': alpha,
            'variables_analyzed': list(data.select_dtypes(include=[np.number]).columns)
        }
    }
    
    # Get all analysis functions from this module
    import inspect
    current_module = inspect.getmodule(inspect.currentframe())
    
    for name, obj in inspect.getmembers(current_module):
        if (inspect.isfunction(obj) and 
            name.startswith(('calculate_', 'perform_', 'test_')) and 
            name != 'run_complete_statistical_analysis'):
            try:
                # Pass alpha parameter to functions that might need it
                if 'alpha' in inspect.signature(obj).parameters:
                    results[name] = obj(data, alpha=alpha)
                else:
                    results[name] = obj(data)
            except Exception as e:
                results[name] = {'error': f'Analysis failed: {str(e)}'}
                
    return results


def generate_statistical_summary_report(analysis_results: Dict[str, Any]) -> str:
    """
    Generate a human-readable summary report from statistical analysis results.
    
    Args:
        analysis_results: Results from run_complete_statistical_analysis()
        
    Returns:
        String containing formatted statistical report
    """
    report_lines = []
    report_lines.append("STATISTICAL ANALYSIS SUMMARY REPORT")
    report_lines.append("=" * 50)
    
    metadata = analysis_results.get('analysis_metadata', {})
    report_lines.append(f"Analysis Timestamp: {metadata.get('timestamp', 'Unknown')}")
    report_lines.append(f"Sample Size: {metadata.get('sample_size', 'Unknown')}")
    report_lines.append(f"Alpha Level: {metadata.get('alpha_level', 'Unknown')}")
    report_lines.append(f"Variables: {len(metadata.get('variables_analyzed', []))}")
    report_lines.append("")
    
    # Summarize key findings
    for analysis_name, result in analysis_results.items():
        if analysis_name != 'analysis_metadata' and isinstance(result, dict):
            if 'error' not in result:
                report_lines.append(f"{analysis_name.replace('_', ' ').title()}:")
                
                # Extract key statistics based on analysis type
                if 'p_value' in result:
                    p_val = result['p_value']
                    significance = "significant" if p_val < metadata.get('alpha_level', 0.05) else "not significant"
                    report_lines.append(f"  - p-value: {p_val:.4f} ({significance})")
                
                if 'effect_size' in result:
                    report_lines.append(f"  - Effect size: {result['effect_size']:.4f}")
                
                if 'correlation_matrix' in result:
                    report_lines.append(f"  - Correlation matrix generated with {len(result['correlation_matrix'])} variables")
                
                if 'cronbach_alpha' in result:
                    alpha_val = result['cronbach_alpha']
                    reliability = "excellent" if alpha_val > 0.9 else "good" if alpha_val > 0.8 else "acceptable" if alpha_val > 0.7 else "questionable"
                    report_lines.append(f"  - Cronbach's α: {alpha_val:.3f} ({reliability})")
                
                report_lines.append("")
            else:
                report_lines.append(f"{analysis_name}: ERROR - {result['error']}")
                report_lines.append("")
    
    return "\\n".join(report_lines)
'''
        
        return header + all_functions + footer
    
    def _create_fallback_statistical_function(self) -> str:
        """Create a fallback statistical function when LLM extraction fails."""
        return '''def calculate_basic_statistics(data, **kwargs):
    """
    Calculate basic descriptive statistics for all numeric columns.
    
    Args:
        data: pandas DataFrame with dimension scores
        **kwargs: Additional parameters
        
    Returns:
        dict: Basic statistics for each numeric column
    """
    import pandas as pd
    import numpy as np
    
    try:
        if data.empty:
            return None
            
        results = {}
        numeric_columns = data.select_dtypes(include=[np.number]).columns
        
        for col in numeric_columns:
            results[col] = {
                'mean': float(data[col].mean()) if not data[col].isna().all() else None,
                'std': float(data[col].std()) if not data[col].isna().all() else None,
                'count': int(data[col].count()),
                'missing': int(data[col].isna().sum())
            }
        
        return results
        
    except Exception as e:
        return {'error': f'Statistical calculation failed: {str(e)}'}'''
    
    def _log_event(self, event_type: str, details: Dict[str, Any]) -> None:
        """Log agent event to audit logger."""
        if self.audit_logger:
            self.audit_logger.log_agent_event(
                self.agent_name,
                event_type,
                details
            )
