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
            
            # THIN approach: Save raw LLM response directly as Python module
            # No parsing - let the LLM generate complete, valid Python code
            function_module = generated_functions
            
            # Save to workspace
            output_file = workspace_path / "automatedderivedmetricsagent_functions.py"
            output_file.write_text(function_module)
            
            # Count functions by analyzing the generated code (simple heuristic)
            # Count function definitions in the generated code
            functions_count = function_module.count('def ')
            
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
        """Generate calculation functions using direct LLM generation (THIN approach)."""
        # Load actual data structure for data-aware prompting
        data_structure_info = self._load_data_structure(workspace_path)
        
        # Load the prompt template
        prompt_template = self._load_prompt_template()
        
        # Prepare the prompt with actual framework content
        prompt = prompt_template.format(
            framework_content=framework_content,
            experiment_name=experiment_spec.get('name', 'Unknown'),
            experiment_description=experiment_spec.get('description', 'No description'),
            data_columns=data_structure_info.get('columns', 'No data structure info'),
            sample_data=data_structure_info.get('sample_data', 'No sample data')
        )
        
        # Generate functions using LLM
        self._log_event("LLM_GENERATION_START", {
            "prompt_length": len(prompt),
            "framework_size": len(framework_content)
        })
        
        try:
            # Temporarily disable structured output to test basic functionality
            response, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=prompt,
                temperature=0.1
            )
            
            if not response:
                raise ValueError("LLM returned empty response")
            
            # Handle structured output response
            if isinstance(response, dict):
                # Try different possible field names for the code
                code_field = None
                if 'code' in response:
                    code_field = 'code'
                elif 'python_module' in response:
                    code_field = 'python_module'
                elif 'python_code' in response:
                    code_field = 'python_code'
                elif 'content' in response:
                    code_field = 'content'
                
                if code_field:
                    # Structured output response - extract the code directly
                    extracted_code = response[code_field]
                    language = response.get('language', 'python')
                    
                    self._log_event("LLM_GENERATION_SUCCESS", {
                        "response_type": "structured_output",
                        "language": language,
                        "code_field": code_field,
                        "code_length": len(extracted_code)
                    })
                    
                    return extracted_code
            elif isinstance(response, list) and len(response) > 0:
                # Handle array response format
                first_item = response[0]
                if isinstance(first_item, dict) and 'content' in first_item:
                    extracted_code = first_item['content']
                    
                    self._log_event("LLM_GENERATION_SUCCESS", {
                        "response_type": "structured_output_array",
                        "array_length": len(response),
                        "code_length": len(extracted_code)
                    })
                    
                    return extracted_code
            else:
                # Fallback to parsing for non-structured output
                print("⚠️ Warning: Non-structured response, falling back to parsing")
                
                # Debug: Check for problematic strings
                if 'metric_name_1' in str(response):
                    print(f"🔍 DEBUG: LLM response contains 'metric_name_1'")
                    print(f"🔍 DEBUG: Response preview: {str(response)[:500]}")
                
                # Extract code using ThinOutputExtractor
                code_blocks = self.extractor.extract_code_blocks(str(response))
                
                if not code_blocks:
                    # Fallback: try to extract from markdown code blocks
                    import re
                    markdown_blocks = re.findall(r'```python\n(.*?)\n```', str(response), re.DOTALL)
                    if markdown_blocks:
                        code_blocks = markdown_blocks
                    else:
                        # Last resort: return the raw response and hope for the best
                        print("⚠️ Warning: No code blocks found, using raw response")
                        code_blocks = [str(response)]
                
                # Use the first (and typically only) code block
                extracted_code = code_blocks[0] if code_blocks else str(response)
                
                self._log_event("LLM_GENERATION_SUCCESS", {
                    "response_type": "parsed_output",
                    "response_length": len(str(response)),
                    "extracted_length": len(extracted_code),
                    "code_blocks_found": len(code_blocks)
                })
                
                return extracted_code
        
        except Exception as e:
            self._log_event("LLM_GENERATION_FAILED", {
                "error": str(e)
            })
            raise ValueError(f"Failed to generate derived metrics functions: {e}")
    
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
        # THIN approach: Let the LLM handle parsing, don't hardcode framework-specific logic
        # This method should be removed in favor of direct LLM generation
        # For now, return empty dict to force LLM-based generation
        return {}
    
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
            # Log what we're generating
            print(f"🔧 Generating derived metrics function: {calc_name}")
            
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
            
            # THIN approach: Show the LLM the actual raw data structure
            columns_info = []
            sample_data = "Sample analysis result structure (as it will appear in the DataFrame):\n"
            
            if analysis_data and len(analysis_data) > 0:
                first_result = analysis_data[0]
                
                # Show the complete raw structure - let the LLM figure out how to access it
                sample_data += json.dumps(first_result, indent=2)[:1500]
                if len(json.dumps(first_result, indent=2)) > 1500:
                    sample_data += "\n... (truncated)"
                
                # Provide minimal guidance about common patterns
                columns_info.append("Data structure analysis:")
                columns_info.append("- Look for 'raw_analysis_response' containing JSON strings")
                columns_info.append("- Parse JSON to find 'document_analyses' array")
                columns_info.append("- Extract 'dimensional_scores' from each document analysis")
                columns_info.append("- Work with the actual nested structure you find")
            else:
                columns_info.append("No analysis data available")
                sample_data = "No sample data available"
            
            return {
                'columns': '\n'.join(columns_info),
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
