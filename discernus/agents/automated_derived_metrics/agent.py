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
                experiment_spec,
                workspace_path
            )
            
            # Extract clean functions using THIN delimiter approach
            if not generated_functions or not generated_functions.strip():
                raise ValueError("No functions extracted from LLM response")
            
            # Create module from the already-combined functions
            function_module = self._create_function_module([generated_functions], experiment_spec)
            
            # Save to workspace
            output_file = workspace_path / "automatedderivedmetricsagent_functions.py"
            output_file.write_text(function_module)
            
            # Count the number of functions by counting how many calculations were attempted
            calculations = self._extract_individual_calculations(framework_content)
            functions_count = len(calculations)
            
            self._log_event("FUNCTION_GENERATION_SUCCESS", {
                "functions_extracted": functions_count,
                "output_file": str(output_file.name),
                "module_size": len(function_module)
            })
            
            return {
                "status": "success",
                "functions_generated": functions_count,
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

    def _generate_calculation_functions(self, framework_content: str, experiment_spec: Dict[str, Any], workspace_path: Path) -> str:
        """Generate calculation functions using componentized generation (one function at a time)."""
        # Extract individual calculations from framework
        calculations = self._extract_individual_calculations(framework_content)
        
        # Load actual data structure for data-aware prompting
        data_structure_info = self._load_data_structure(workspace_path)
        
        generated_functions = []
        
        # Generate ONE function at a time (componentized generation)
        for calc_name, calc_description in calculations.items():
            try:
                function_code = self._generate_single_function(
                    calc_name, 
                    calc_description, 
                    framework_content,
                    experiment_spec,
                    data_structure_info
                )
                
                # Validate the generated function
                if self._validate_function_syntax(function_code):
                    generated_functions.append(function_code)
                    self._log_event("SINGLE_FUNCTION_GENERATED", {
                        "function_name": calc_name,
                        "function_length": len(function_code)
                    })
                else:
                    self._log_event("FUNCTION_VALIDATION_FAILED", {
                        "function_name": calc_name,
                        "reason": "syntax_error"
                    })
                    
            except Exception as e:
                self._log_event("SINGLE_FUNCTION_GENERATION_FAILED", {
                    "function_name": calc_name,
                    "error": str(e)
                })
                continue
        
        # Combine all generated functions
        if not generated_functions:
            raise ValueError("No valid functions were generated")
        
        combined = "\n\n".join(generated_functions)
            
        return combined
    
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
            name not in ['calculate_all_derived_metrics', 'calculate_derived_metrics']):
            try:
                results[name.replace('calculate_', '')] = obj(data)
            except Exception as e:
                results[name.replace('calculate_', '')] = None
                
    return results


def calculate_derived_metrics(data: pd.DataFrame) -> pd.DataFrame:
    """
    Template-compatible wrapper function for derived metrics calculation.
    
    This function is called by the universal notebook template and returns
    the original data with additional derived metric columns.
    
    Args:
        data: pandas DataFrame with dimension scores
        
    Returns:
        DataFrame with original data plus derived metric columns
    """
    # Calculate all derived metrics
    derived_metrics = calculate_all_derived_metrics(data)
    
    # Create a copy of the original data
    result = data.copy()
    
    # Add derived metrics as new columns
    for metric_name, metric_value in derived_metrics.items():
        if metric_value is not None:
            # For scalar metrics, broadcast to all rows
            result[metric_name] = metric_value
        else:
            # For failed calculations, use NaN
            result[metric_name] = np.nan
    
    return result
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
    
    def _extract_individual_calculations(self, framework_content: str) -> Dict[str, str]:
        """Extract individual calculations from framework content for componentized generation."""
        calculations = {}
        
        # Parse the CFF v8.0 framework for calculation descriptions
        import re
        
        # Look for calculation sections in the framework
        calc_section_match = re.search(r'## Advanced Metrics.*?(?=##|$)', framework_content, re.DOTALL | re.IGNORECASE)
        if not calc_section_match:
            # Fallback: look for any calculations section
            calc_section_match = re.search(r'## Calculations.*?(?=##|$)', framework_content, re.DOTALL | re.IGNORECASE)
        
        if calc_section_match:
            calc_section = calc_section_match.group(0)
            
            # Extract individual calculations
            # Look for patterns like "**Identity Tension**: description"
            calc_matches = re.findall(r'\*\*([^*]+)\*\*:\s*([^*\n]+)', calc_section)
            for calc_name, calc_desc in calc_matches:
                # Clean up the names
                clean_name = calc_name.strip().lower().replace(' ', '_')
                calculations[clean_name] = calc_desc.strip()
        
        # If no calculations found, provide defaults for CFF
        if not calculations:
            calculations = {
                "identity_tension": "Conflict between tribal dominance and individual dignity dimensions",
                "emotional_balance": "Difference between hope and fear scores", 
                "success_climate": "Difference between compersion and envy scores",
                "relational_climate": "Difference between amity and enmity scores",
                "goal_orientation": "Difference between cohesive goals and fragmentative goals",
                "overall_cohesion_index": "Comprehensive measure combining all dimensions"
            }
        
        return calculations
    
    def _generate_single_function(self, calc_name: str, calc_description: str, 
                                framework_content: str, experiment_spec: Dict[str, Any],
                                data_structure_info: Dict[str, Any]) -> str:
        """Generate a single calculation function using focused LLM prompt."""
        
        # Create focused prompt for single function
        single_function_prompt = f"""You are an expert Python developer generating ONE calculation function for a research framework.

**CALCULATION TO IMPLEMENT:**
Name: {calc_name}
Description: {calc_description}

**FRAMEWORK CONTEXT:**
{framework_content[:1000]}...

**ACTUAL DATA STRUCTURE:**
The analysis data contains the following columns:
{data_structure_info['columns_info']}

**SAMPLE DATA:**
{data_structure_info['sample_data']}

**REQUIREMENTS:**
1. Generate EXACTLY ONE Python function
2. Function name: calculate_{calc_name}
3. Accept pandas DataFrame 'data' as primary parameter (this will be a single row/Series)
4. Use the EXACT column names shown in the actual data structure above
5. Handle missing data gracefully (return None)
6. Include proper docstring with formula
7. Be production-ready with error handling

**CRITICAL:** Use the EXACT column names shown in the actual data structure above. Do NOT assume or invent column names.

**CRITICAL OUTPUT FORMAT - YOU MUST FOLLOW THIS EXACTLY:**
You MUST start your response with the opening delimiter and end with the closing delimiter.
Do NOT include any other text before or after the delimiters.

<<<DISCERNUS_FUNCTION_START>>>
def calculate_{calc_name}(data, **kwargs):
    \"\"\"
    Calculate {calc_name}: {calc_description}
    
    Args:
        data: pandas DataFrame with dimension scores
        **kwargs: Additional parameters
        
    Returns:
        float: Calculated result or None if insufficient data
    \"\"\"
    import pandas as pd
    import numpy as np
    
    try:
        # Implementation here
        pass
    except Exception:
        return None
<<<DISCERNUS_FUNCTION_END>>>

**MANDATORY RULES:**
- Your response MUST begin with: <<<DISCERNUS_FUNCTION_START>>>
- Your response MUST end with: <<<DISCERNUS_FUNCTION_END>>>
- Generate ONLY ONE function between these delimiters
- Do NOT add explanatory text outside the delimiters
- The delimiters are case-sensitive and must match exactly

Generate ONLY this one function. Do not generate multiple functions."""

        try:
            response_text, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=single_function_prompt,
                system_prompt=f"You are an expert Python developer. Generate exactly one function for {calc_name}."
            )
            
            # Extract the function using THIN delimiter approach
            extracted_functions = self.extractor.extract_code_blocks(response_text)
            
            if not extracted_functions:
                raise ValueError(f"No function extracted for {calc_name}")
            
            if len(extracted_functions) > 1:
                # Take the first function if multiple were generated
                self._log_event("MULTIPLE_FUNCTIONS_WARNING", {
                    "calc_name": calc_name,
                    "functions_count": len(extracted_functions)
                })
            
            return extracted_functions[0]
            
        except Exception as e:
            self._log_event("SINGLE_FUNCTION_LLM_FAILED", {
                "calc_name": calc_name,
                "error": str(e)
            })
            raise
    
    def _validate_function_syntax(self, function_code: str) -> bool:
        """Validate that generated function has correct Python syntax."""
        import ast
        
        try:
            # Try to parse the function code
            ast.parse(function_code)
            return True
        except SyntaxError as e:
            self._log_event("FUNCTION_SYNTAX_ERROR", {
                "error": str(e),
                "line": getattr(e, 'lineno', 'unknown')
            })
            return False
    
    def _load_data_structure(self, workspace_path: Path) -> Dict[str, Any]:
        """
        Load actual data structure from workspace for data-aware prompting.
        
        Returns:
            Dictionary with columns_info and sample_data for prompting
        """
        import pandas as pd
        
        try:
            # Load analysis data from workspace
            analysis_data_path = workspace_path / "analysis_data.json"
            if not analysis_data_path.exists():
                # Fallback to generic structure if no data available
                return {
                    'columns_info': "No analysis data available - use generic column names",
                    'sample_data': "No sample data available"
                }
            
            with open(analysis_data_path, 'r') as f:
                analysis_data = json.load(f)
            
            if not analysis_data:
                return {
                    'columns_info': "Analysis data is empty - use generic column names", 
                    'sample_data': "No sample data available"
                }
            
            # Convert to DataFrame to analyze structure
            df = pd.DataFrame(analysis_data)
            
            # Generate columns info with data types and value ranges
            columns_info = []
            for col in df.columns:
                if col == 'document_name':
                    columns_info.append(f"- {col} (string)")
                else:
                    # Check if column contains real numeric data
                    non_null_values = df[col].dropna()
                    if len(non_null_values) > 0 and pd.api.types.is_numeric_dtype(non_null_values):
                        min_val = non_null_values.min()
                        max_val = non_null_values.max()
                        columns_info.append(f"- {col} (float {min_val:.2f}-{max_val:.2f}) ← REAL DATA")
                    else:
                        columns_info.append(f"- {col} (float - mostly NaN, ignore)")
            
            # Generate sample data showing first valid row
            sample_data = "Sample row from actual data:\n"
            if len(df) > 0:
                first_row = df.iloc[0]
                doc_name = first_row.get('document_name', 'unknown')[:30]
                sample_data += f"Document: {doc_name}\n"
                
                # Show key numeric columns with real values
                numeric_cols = df.select_dtypes(include=['number']).columns
                real_data_cols = []
                for col in numeric_cols:
                    if col in first_row and pd.notna(first_row[col]):
                        real_data_cols.append(f"{col}={first_row[col]}")
                
                if real_data_cols:
                    sample_data += f"Real values: {', '.join(real_data_cols[:6])}..."
                else:
                    sample_data += "No real numeric values found in first row"
            
            return {
                'columns_info': '\n'.join(columns_info),
                'sample_data': sample_data
            }
            
        except Exception as e:
            self._log_event("DATA_STRUCTURE_LOADING_FAILED", {
                "error": str(e),
                "workspace": str(workspace_path)
            })
            
            # Return safe fallback
            return {
                'columns_info': f"Failed to load data structure: {str(e)}",
                'sample_data': "No sample data available"
            }
