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

from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway
from discernus.gateway.model_registry import ModelRegistry
from discernus.core.deprecated.thin_output_extraction import ThinOutputExtractor
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
        self.llm_gateway = EnhancedLLMGateway(model_registry)
        
        # Initialize THIN output extractor
        self.extractor = ThinOutputExtractor()
    
    def generate_functions(self, workspace_path: Path, pre_assembled_prompt: str = None) -> Dict[str, Any]:
        """Generate statistical analysis functions from framework and experiment specifications.
        
        Args:
            workspace_path: Transactional workspace for reading inputs and writing outputs
            pre_assembled_prompt: Optional pre-assembled prompt from StatisticalAnalysisPromptAssembler
            
        Returns:
            Generation result with function details
            
        Raises:
            Exception: On function generation failure
        """
        self._log_event("STATISTICAL_GENERATION_START", {
            "workspace": str(workspace_path),
            "model": self.model,
            "using_pre_assembled_prompt": pre_assembled_prompt is not None
        })
        
        try:
            # Always read experiment_spec for module creation
            experiment_spec = json.loads((workspace_path / "experiment_spec.json").read_text())
            
            if pre_assembled_prompt:
                # Use the pre-assembled prompt from the assembler
                self._log_event("USING_PRE_ASSEMBLED_PROMPT", {
                    "prompt_length": len(pre_assembled_prompt)
                })
                
                # Generate functions using the pre-assembled prompt
                generated_functions = self._generate_functions_with_prompt(pre_assembled_prompt)
            else:
                # Fall back to the original approach (for backward compatibility)
                self._log_event("USING_LEGACY_PROMPT_GENERATION", {})
                
                # Read raw content from workspace
                framework_content = (workspace_path / "framework_content.md").read_text()
                
                self._log_event("INPUTS_LOADED", {
                    "framework_size": len(framework_content),
                    "experiment_name": experiment_spec.get("name", "unknown"),
                    "questions_count": len(experiment_spec.get("questions", []))
                })
                
                # Generate statistical analysis functions using LLM
                generated_functions = self._generate_statistical_functions(
                    framework_content, 
                    experiment_spec,
                    workspace_path
                )
            
            # THIN approach: Extract Python code from LLM response
            function_module = generated_functions
            
            # Use the same robust extraction for string responses
            if isinstance(function_module, str):
                function_module = self._extract_python_code_robustly(function_module)
            
            # Save to workspace
            output_file = workspace_path / "automatedstatisticalanalysisagent_functions.py"
            output_file.write_text(function_module)
            print(f"🔍 Written {len(function_module)} chars to {output_file.name}")
            
            # Count functions by analyzing the generated code (simple heuristic)
            # Count function definitions in the generated code
            functions_count = function_module.count('def ')
            
            self._log_event("STATISTICAL_GENERATION_SUCCESS", {
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
            self._log_event("STATISTICAL_GENERATION_FAILED", {
                "error": str(e),
                "workspace": str(workspace_path)
            })
            raise
    
    def _load_data_structure(self, workspace_path: Path) -> Dict[str, Any]:
        """
        Load actual data structure from workspace for data-aware prompting.
        
        Returns:
            Dictionary with columns_info and sample_data for prompting
        """
        import pandas as pd
        import json
        
        try:
            # Look for analysis data in the workspace - try multiple possible locations
            possible_paths = [
                workspace_path / "analysis_data.json",
                workspace_path / "individual_analysis_results.json",
                workspace_path / "raw_analysis_data.json"
            ]
            
            analysis_data_path = None
            for path in possible_paths:
                if path.exists():
                    analysis_data_path = path
                    break
            
            if not analysis_data_path:
                # Fallback to generic structure if no data available
                return {
                    'columns_info': "No analysis data available - use generic column names ending with _raw, _salience, _confidence",
                    'sample_data': "No sample data available"
                }
            
            with open(analysis_data_path, 'r') as f:
                analysis_data = json.load(f)
            
            if not analysis_data:
                return {
                    'columns_info': "Analysis data is empty - use generic column names ending with _raw, _salience, _confidence", 
                    'sample_data': "No sample data available"
                }
            
            # Convert to DataFrame to analyze structure - handle different data formats
            if isinstance(analysis_data, list) and len(analysis_data) > 0:
                # Handle list of individual analysis results
                sample_result = analysis_data[0]
                if 'raw_analysis_response' in sample_result:
                    # Extract JSON from delimited response to understand structure
                    raw_response = sample_result['raw_analysis_response']
                    start_marker = '<<<DISCERNUS_ANALYSIS_JSON_v6>>>'
                    end_marker = '<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>'
                    
                    start_idx = raw_response.find(start_marker)
                    end_idx = raw_response.find(end_marker)
                    
                    if start_idx != -1 and end_idx != -1:
                        json_content = raw_response[start_idx + len(start_marker):end_idx].strip()
                        parsed_data = json.loads(json_content)
                        
                        # Extract column structure from document analyses
                        if 'document_analyses' in parsed_data and len(parsed_data['document_analyses']) > 0:
                            doc_analysis = parsed_data['document_analyses'][0]
                            columns_info = ["- document_name (string)"]
                            sample_values = []
                            
                            for dimension, scores in doc_analysis.get('dimensional_scores', {}).items():
                                columns_info.append(f"- {dimension}_raw (float 0.0-1.0) ← ACTUAL COLUMN NAME")
                                columns_info.append(f"- {dimension}_salience (float 0.0-1.0) ← ACTUAL COLUMN NAME") 
                                columns_info.append(f"- {dimension}_confidence (float 0.0-1.0) ← ACTUAL COLUMN NAME")
                                
                                # Add sample values
                                sample_values.extend([
                                    f"{dimension}_raw={scores.get('raw_score', 0.0)}",
                                    f"{dimension}_salience={scores.get('salience', 0.0)}",
                                    f"{dimension}_confidence={scores.get('confidence', 0.0)}"
                                ])
                            
                            return {
                                'columns_info': '\n'.join(columns_info),
                                'sample_data': f"Sample row from actual data:\nDocument: {doc_analysis.get('document_name', 'unknown')[:30]}\nReal values: {', '.join(sample_values[:6])}..."
                            }
            
            # Fallback: try to convert directly to DataFrame
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
                        columns_info.append(f"- {col} (float {min_val:.2f}-{max_val:.2f}) ← ACTUAL COLUMN NAME")
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
            
            # Return safe fallback with correct column naming pattern
            return {
                'columns_info': f"Failed to load data structure: {str(e)}\nUse column names ending with _raw, _salience, _confidence (NOT _score)",
                'sample_data': "No sample data available"
            }

    def _generate_statistical_functions(self, framework_content: str, experiment_spec: Dict[str, Any], workspace_path: Path) -> str:
        """Generate statistical analysis functions using componentized generation approach."""
        # Load actual data structure for data-aware prompting
        data_structure_info = self._load_data_structure(workspace_path)
        
        # Extract individual statistical analyses needed
        statistical_analyses = self._extract_statistical_analyses(framework_content, experiment_spec)
        
        generated_functions = []
        for analysis_name, analysis_description in statistical_analyses.items():
            try:
                function_code = self._generate_single_statistical_function(
                    analysis_name, analysis_description, framework_content, experiment_spec, data_structure_info
                )
                generated_functions.append(function_code)
                
            except Exception as e:
                print(f"❌ Failed to generate {analysis_name}: {str(e)}")
                self._log_event("SINGLE_STATISTICAL_FUNCTION_LLM_FAILED", {
                    "analysis_name": analysis_name,
                    "error": str(e)
                })
                continue
        
        if not generated_functions:
            raise ValueError("No valid statistical functions were generated")
        
        combined = "\n\n".join(generated_functions)
            
        return combined
    
    def _extract_python_code_robustly(self, response) -> str:
        """
        Robustly extract Python code from any LLM response structure.
        No more guessing key names - this finds Python code anywhere!
        """
        def looks_like_python_code(text):
            """Check if a string looks like Python code."""
            if not isinstance(text, str) or len(text) < 50:
                return False
            # Look for Python keywords and structure
            python_indicators = ['import pandas', 'import numpy', 'def ', 'import ', 'pd.DataFrame', 'return ']
            return sum(indicator in text for indicator in python_indicators) >= 2
        
        # Strategy 1: If it's a string, check if it's already Python code
        if isinstance(response, str):
            if looks_like_python_code(response):
                return response
            # Try parsing as JSON first
            try:
                response = json.loads(response)
            except json.JSONDecodeError:
                return response  # Return as-is if not JSON
        
        # Strategy 2: If it's a dict, find the longest Python code string
        if isinstance(response, dict):
            candidate_code = None
            max_length = 0
            found_key = None
            
            # First, try all values directly
            for key, value in response.items():
                if isinstance(value, str) and looks_like_python_code(value):
                    if len(value) > max_length:
                        candidate_code = value
                        found_key = key
                        max_length = len(value)
            
            if candidate_code:
                print(f"🔍 Auto-detected Python code in key '{found_key}' (length: {len(candidate_code)})")
                return candidate_code
            
            # Strategy 3: Try nested structures (JSON arrays, etc.)
            for key, value in response.items():
                if isinstance(value, str):
                    try:
                        nested_data = json.loads(value)
                        if isinstance(nested_data, list) and len(nested_data) > 0:
                            # Special handling for function arrays (like python_module)
                            if key == "python_module" or all(isinstance(item, dict) and ("code" in item or "content" in item) for item in nested_data):
                                # This is a function array - combine all function codes
                                combined_code = []
                                combined_code.append("import pandas as pd")
                                combined_code.append("import numpy as np")
                                combined_code.append("import scipy.stats as stats")
                                combined_code.append("from typing import Dict, Any, Optional, List, Tuple")
                                combined_code.append("import warnings")
                                combined_code.append("")
                                
                                for item in nested_data:
                                    if isinstance(item, dict):
                                        # Try both "code" and "content" fields
                                        function_code = item.get("code") or item.get("content")
                                        if function_code and looks_like_python_code(function_code):
                                            combined_code.append(function_code)
                                            combined_code.append("")
                                
                                combined_python = "\n".join(combined_code)
                                print(f"🔍 Combined {len(nested_data)} functions from {key} into Python module")
                                return combined_python
                            
                            # Original nested handling
                            for item in nested_data:
                                if isinstance(item, dict):
                                    for nested_key, nested_value in item.items():
                                        if looks_like_python_code(nested_value):
                                            print(f"🔍 Found Python code in nested: {key}[0].{nested_key}")
                                            return nested_value
                    except json.JSONDecodeError:
                        continue
        
        # Strategy 4: If it's a list, check all items
        if isinstance(response, list):
            for i, item in enumerate(response):
                if isinstance(item, str) and looks_like_python_code(item):
                    print(f"🔍 Found Python code in list item {i}")
                    return item
                elif isinstance(item, dict):
                    for key, value in item.items():
                        if isinstance(value, str) and looks_like_python_code(value):
                            print(f"🔍 Found Python code in list[{i}].{key}")
                            return value
        
        # Fallback: return string representation
        print("⚠️ No Python code detected - returning string representation")
        return str(response)

    def _generate_functions_with_prompt(self, pre_assembled_prompt: str) -> str:
        """Generate statistical analysis functions using a pre-assembled prompt.
        
        Args:
            pre_assembled_prompt: The complete prompt assembled by StatisticalAnalysisPromptAssembler
            
        Returns:
            Generated function code as a string
        """
        try:
            # Log what we're generating
            print("🔧 Generating statistical analysis functions...")
            
            # Use structured output for Vertex AI
            response_schema = {
                "type": "object",
                "properties": {
                    "language": {
                        "type": "string",
                        "description": "The programming language of the generated code."
                    },
                    "code": {
                        "type": "string", 
                        "description": "The complete, executable Python code string."
                    }
                },
                "required": ["language", "code"]
            }
            
            response, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=pre_assembled_prompt,
                temperature=0.1,
                response_schema=response_schema
            )
            
            if not response:
                raise ValueError("LLM returned empty response")
            
            # Use robust extraction - no more guessing key names!
            extracted_code = self._extract_python_code_robustly(response)
            
            if extracted_code and isinstance(extracted_code, str) and len(extracted_code) > 100:
                return extracted_code
            
            # Old fallback code for reference (should rarely be reached now)
            if isinstance(response, dict):
                # Check for different possible field names
                if 'code' in response:
                    extracted_code = response['code']
                    language = response.get('language', 'python')
                elif 'module_code' in response:
                    print(f"🔍 Found module_code in response")
                    extracted_code = response['module_code']
                    language = response.get('language', 'python')
                elif 'python_module' in response:
                    extracted_code = response['python_module']
                    language = response.get('language', 'python')
                elif 'module_content' in response:
                    print(f"🔍 Found module_content in response")
                    extracted_code = response['module_content']
                    language = response.get('language', 'python')
                elif 'module' in response:
                    print(f"🔍 Found module in response")
                    extracted_code = response['module']
                    language = response.get('language', 'python')
                elif 'statistical_functions_module' in response:
                    print(f"🔍 Found statistical_functions_module in response")
                    extracted_code = response['statistical_functions_module']
                    language = response.get('language', 'python')
                elif 'python_code' in response:
                    print(f"🔍 Found python_code in response")
                    extracted_code = response['python_code']
                    language = response.get('language', 'python')
                else:
                    # Fallback for non-structured responses
                    print("⚠️ Warning: Structured output failed, using raw response")
                    print(f"🔍 Response keys: {list(response.keys()) if isinstance(response, dict) else 'Not a dict'}")
                    print(f"🔍 Response type: {type(response)}")
                    
                    # Try to extract Python code from complex JSON structures
                    if isinstance(response, dict):
                        # Look for nested JSON content that might contain actual Python code
                        for key, value in response.items():
                            if isinstance(value, str):
                                try:
                                    # Try parsing as JSON array
                                    import json
                                    parsed = json.loads(value)
                                    if isinstance(parsed, list) and len(parsed) > 0:
                                        if isinstance(parsed[0], dict) and 'content' in parsed[0]:
                                            extracted_code = parsed[0]['content']
                                            print(f"🔍 Extracted Python code from nested JSON structure (length: {len(extracted_code)})")
                                            language = 'python'
                                            break
                                except (json.JSONDecodeError, KeyError, IndexError):
                                    continue
                        else:
                            # If no nested structure found, fallback to string conversion
                            extracted_code = str(response)
                            language = 'python'
                    else:
                        extracted_code = str(response)
                        language = 'python'
                
                self._log_event("PROMPT_BASED_GENERATION_SUCCESS", {
                    "response_type": "structured_output",
                    "language": language,
                    "code_length": len(extracted_code)
                })
                
                return extracted_code
            else:
                # Fallback for non-structured responses
                print("⚠️ Warning: Structured output failed, using raw response")
                self._log_event("PROMPT_BASED_GENERATION_SUCCESS", {
                    "response_type": "raw_output",
                    "response_length": len(str(response))
                })
                
                return str(response)
            
        except Exception as e:
            self._log_event("PROMPT_BASED_GENERATION_FAILED", {
                "error": str(e)
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


def perform_statistical_analysis(data: pd.DataFrame) -> Dict[str, Any]:
    """
    Template-compatible wrapper function for statistical analysis.
    
    This function is called by the universal notebook template and performs
    comprehensive statistical analysis on the provided dataset.
    
    Args:
        data: pandas DataFrame with dimension scores and derived metrics
        
    Returns:
        Dictionary containing all statistical analysis results
    """
    return run_complete_statistical_analysis(data)


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
    
    def _extract_statistical_analyses(self, framework_content: str, experiment_spec: Dict[str, Any]) -> Dict[str, str]:
        """Extract individual statistical analyses needed for componentized generation."""
        analyses = {}
        
        # Standard statistical analyses for any framework
        analyses["descriptive_statistics"] = "Generate descriptive statistics (mean, median, std, etc.) for all numeric dimensions"
        analyses["correlation_analysis"] = "Generate correlation matrix and significance tests between all dimensions"
        
        # Framework-appropriate reliability/validation analysis (LLM-determined)
        validation_type = self._determine_framework_validation_type(framework_content)
        if validation_type == "oppositional_validation":
            analyses["oppositional_validation"] = "Generate oppositional construct validation including negative correlation checks, discriminant validity tests, and convergent validity assessment for opposing dimension pairs"
        else:
            analyses["reliability_analysis"] = "Generate Cronbach's alpha and other reliability measures for dimension consistency"
        
        # Framework-specific analyses based on content
        if "tension" in framework_content.lower():
            analyses["tension_analysis"] = "Generate statistical analysis for tension-based metrics and relationships"
        
        if "cohesion" in framework_content.lower() or "cohesive" in framework_content.lower():
            analyses["cohesion_analysis"] = "Generate statistical analysis for cohesion metrics and patterns"
        
        # Research question-specific analyses
        questions = experiment_spec.get("questions", [])
        if questions:
            analyses["hypothesis_testing"] = "Generate hypothesis testing functions based on research questions"
        
        return analyses
    
    def _determine_framework_validation_type(self, framework_content: str) -> str:
        """
        Use LLM to determine appropriate validation approach for the framework.
        
        Args:
            framework_content: The complete framework markdown content
            
        Returns:
            str: Either "oppositional_validation" or "reliability_analysis"
        """
        # Truncate framework content to avoid token limits while preserving key sections
        framework_excerpt = framework_content[:3000]
        if len(framework_content) > 3000:
            framework_excerpt += "\n\n[Content truncated for analysis]"
        
        classification_prompt = f"""Analyze this research framework to determine the appropriate statistical validation approach.

FRAMEWORK TO ANALYZE:
{framework_excerpt}

TASK: Determine if this framework measures opposing constructs or unidimensional constructs.

OPPOSING CONSTRUCTS are dimensions designed to be conceptually opposite (like Dimension A vs Dimension B, or positive vs negative variants of the same concept). These should be negatively correlated and require oppositional construct validation.

UNIDIMENSIONAL CONSTRUCTS are dimensions that should correlate positively with each other and can be validated using traditional reliability measures like Cronbach's Alpha.

ANALYSIS CRITERIA:
- Look for explicit opposing pairs (A vs B, A ↔ B)
- Check if dimensions are described as conceptual opposites
- Consider whether negative correlations would validate the framework design
- Assess if dimensions measure competing or complementary concepts

RESPOND WITH EXACTLY ONE WORD:
- "OPPOSITIONAL" if this framework measures opposing constructs
- "UNIDIMENSIONAL" if this framework measures constructs that should correlate positively

RESPONSE:"""

        try:
            response_text, _ = self.llm_gateway.execute_call(
                model=self.model,
                prompt=classification_prompt,
                system_prompt="You are an expert psychometrician analyzing research frameworks for appropriate validation methods."
            )
            
            response = response_text.strip().upper()
            
            # Log the classification decision
            self._log_event("FRAMEWORK_CLASSIFICATION", {
                "classification": response,
                "framework_length": len(framework_content)
            })
            
            return "oppositional_validation" if "OPPOSITIONAL" in response else "reliability_analysis"
            
        except Exception as e:
            # Fallback to reliability analysis if LLM call fails
            self._log_event("FRAMEWORK_CLASSIFICATION_ERROR", {
                "error": str(e),
                "fallback": "reliability_analysis"
            })
            return "reliability_analysis"
    
    def _generate_single_statistical_function(self, analysis_name: str, analysis_description: str, 
                                            framework_content: str, experiment_spec: Dict[str, Any], 
                                            data_structure_info: Dict[str, Any]) -> str:
        """Generate a single statistical analysis function using LLM with THIN delimiters."""
        
        # Create focused prompt for single function
        questions = experiment_spec.get("questions", [])
        questions_text = "\n".join([f"- {q}" for q in questions]) if questions else "- No specific research questions provided"
        
        single_function_prompt = f"""You are an expert statistician generating ONE statistical analysis function for academic research.

**STATISTICAL ANALYSIS TO IMPLEMENT:**
Name: {analysis_name}
Description: {analysis_description}

**RESEARCH CONTEXT:**
Experiment: {experiment_spec.get('name', 'Unknown')}
Description: {experiment_spec.get('description', 'No description')}
Research Questions:
{questions_text}

**FRAMEWORK CONTEXT:**
{framework_content[:1500]}...

**ACTUAL DATA STRUCTURE:**
The analysis data contains the following columns:
{data_structure_info['columns_info']}

**SAMPLE DATA:**
{data_structure_info['sample_data']}

**CRITICAL:** Use the EXACT column names shown in the actual data structure above. Do NOT assume or invent column names.

**REQUIREMENTS:**
1. Generate EXACTLY ONE Python function
2. Function name: {analysis_name.replace(' ', '_').lower()}
3. Accept pandas DataFrame 'data' as primary parameter
4. Use scientific libraries: pandas, numpy, scipy.stats, pingouin
5. Handle missing data gracefully (return None or appropriate message)
6. Include proper docstring with statistical methodology
7. Return structured results (dict format)
8. Be production-ready with comprehensive error handling

**OUTPUT FORMAT:**
Wrap the function in proprietary delimiters:

<<<DISCERNUS_FUNCTION_START>>>
def {analysis_name.replace(' ', '_').lower()}(data, **kwargs):
    \"\"\"
    {analysis_description}
    
    Args:
        data: pandas DataFrame with dimension scores
        **kwargs: Additional statistical parameters
        
    Returns:
        dict: Statistical results with significance tests
    \"\"\"
    import pandas as pd
    import numpy as np
    from scipy import stats
    import pingouin as pg
    
    try:
        # Your statistical analysis implementation here
        # Return structured results
        return {{'results': 'implementation_here'}}
        
    except Exception as e:
        return {{'error': f'Statistical analysis failed: {{str(e)}}'}}
<<<DISCERNUS_FUNCTION_END>>>

Generate the complete function now:"""

        try:
            # Log what we're generating
            print(f"🔧 Generating statistical function: {analysis_name}")
            
            # Call LLM without problematic parameters
            response_text, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=single_function_prompt,
                system_prompt=f"You are an expert statistician. Generate exactly one function for {analysis_name}."
            )
            
            # Extract the function using THIN delimiter approach
            extracted_functions = self.extractor.extract_code_blocks(response_text)
            
            if not extracted_functions:
                raise ValueError(f"No function extracted for {analysis_name}")
            
            if len(extracted_functions) > 1:
                # Take the first function if multiple were generated
                self._log_event("MULTIPLE_STATISTICAL_FUNCTIONS_WARNING", {
                    "analysis_name": analysis_name,
                    "functions_count": len(extracted_functions)
                })
            
            return extracted_functions[0]
            
        except Exception as e:
            self._log_event("SINGLE_STATISTICAL_FUNCTION_LLM_FAILED", {
                "analysis_name": analysis_name,
                "error": str(e)
            })
            raise
