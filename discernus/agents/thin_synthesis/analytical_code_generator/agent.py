#!/usr/bin/env python3
"""
AnalyticalCodeGenerator Agent

This agent receives framework specifications and generates Python code
that performs appropriate statistical analysis using pandas, numpy, scipy.

Key Design Principles:
- Framework-agnostic: Adapts to any analytical framework
- Code generation only: No direct statistical computation
- Template-based: Uses proven statistical patterns
- Deterministic output: Generates executable Python code
"""

import json
import logging
import re
from typing import Dict, Any, Optional
from dataclasses import dataclass

# Import LLM gateway from main codebase
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../..'))
from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry

@dataclass
class CodeGenerationRequest:
    """Request structure for code generation."""
    framework_spec: str
    scores_csv_structure: str
    evidence_csv_structure: str
    experiment_context: Optional[str] = None

@dataclass 
class CodeGenerationResponse:
    """Response structure containing generated code."""
    analysis_code: str
    code_explanation: str
    required_libraries: list
    expected_outputs: Dict[str, str]
    success: bool
    error_message: Optional[str] = None

class AnalyticalCodeGenerator:
    """
    Generates Python analysis code based on framework specifications.
    
    This agent leverages LLM intelligence to understand analytical frameworks
    and generate appropriate statistical code, while keeping the actual
    computation deterministic through pandas/scipy.
    """
    
    def __init__(self, model: str = "vertex_ai/gemini-2.5-flash"):
        """
        Initialize the AnalyticalCodeGenerator.
        
        Args:
            model: LLM model to use for code generation
        """
        self.model = model
        self.model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(self.model_registry)
        self.logger = logging.getLogger(__name__)
        
    def generate_analysis_code(self, request: CodeGenerationRequest) -> CodeGenerationResponse:
        """
        Generate Python analysis code based on framework specification.
        
        Args:
            request: CodeGenerationRequest containing framework and data specs
            
        Returns:
            CodeGenerationResponse with generated code and metadata
        """
        try:
            # Construct the code generation prompt
            prompt = self._build_code_generation_prompt(request)
            
            # Call LLM to generate code
            response_content, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=prompt,
                system_prompt="You are an expert data scientist and Python programmer.",
                temperature=0.1,  # Low temperature for consistent code generation
                max_tokens=4000
            )
            
            if not response_content or not metadata.get('success'):
                return CodeGenerationResponse(
                    analysis_code="",
                    code_explanation="",
                    required_libraries=[],
                    expected_outputs={},
                    success=False,
                    error_message=metadata.get('error', 'Empty response from LLM')
                )
            
            # Parse the LLM response
            return self._parse_llm_response(response_content)
            
        except Exception as e:
            self.logger.error(f"Code generation failed: {str(e)}")
            return CodeGenerationResponse(
                analysis_code="",
                code_explanation="",
                required_libraries=[],
                expected_outputs={},
                success=False,
                error_message=str(e)
            )
    
    def _build_code_generation_prompt(self, request: CodeGenerationRequest) -> str:
        """Build the prompt for LLM code generation."""
        
        prompt = f"""You are an expert data scientist and Python programmer. Your task is to generate Python analysis code that performs statistical analysis based on a research framework specification.

FRAMEWORK SPECIFICATION:
{request.framework_spec}

SCORES CSV STRUCTURE:
{request.scores_csv_structure}

EVIDENCE CSV STRUCTURE:  
{request.evidence_csv_structure}

EXPERIMENT CONTEXT:
{request.experiment_context or "Not provided"}

TASK: Generate Python code that:

1. **Loads and validates the CSV data** using pandas
2. **Performs framework-appropriate statistical analysis** including:
   - Descriptive statistics for all relevant dimensions
   - Reliability assessment (Cronbach's alpha where applicable)
   - Correlation analysis between related measures
   - Hypothesis testing based on framework requirements
   - Effect size calculations
   - Any framework-specific analytical approaches

3. **Outputs structured results** as JSON containing:
   - descriptive_stats: Summary statistics for each dimension
   - reliability_metrics: Internal consistency measures
   - correlations: Correlation matrices and key relationships
   - hypothesis_tests: Statistical test results with p-values
   - effect_sizes: Practical significance measures
   - sample_characteristics: Dataset metadata and quality metrics

REQUIREMENTS:
- Use only standard libraries: pandas, numpy, scipy.stats, json
- Include comprehensive error handling
- Add clear comments explaining each analytical step
- Generate code that is framework-agnostic but analytically appropriate
- Ensure all statistical calculations are mathematically sound
- Output results as structured JSON for downstream processing

RESPONSE FORMAT:
Provide your response as a JSON object with these fields:
- "analysis_code": The complete Python code as a string
- "code_explanation": Brief explanation of the analytical approach
- "required_libraries": List of required Python libraries
- "expected_outputs": Dictionary describing the output JSON structure

Generate the code now:"""

        return prompt
    
    def _parse_llm_response(self, response_content: str) -> CodeGenerationResponse:
        """Parse the LLM response into structured format."""
        
        try:
            # THIN Principle: Work WITH LLM behavior, not against it
            # LLMs almost always wrap JSON in markdown code blocks - expect this as the norm
            
            # Use regex to robustly extract JSON from any markdown code block variation
            # Handles: ```json\n{...}\n```, ```\n{...}\n```, ``` json\n{...}\n```, etc.
            code_block_pattern = r'```\s*(?:json)?\s*\n?(.*?)\n?```'
            match = re.search(code_block_pattern, response_content.strip(), re.DOTALL)
            
            if match:
                content = match.group(1).strip()
            else:
                # Fallback: try raw content (for cases without code blocks)
                content = response_content.strip()
            
            # Parse the cleaned JSON content
            parsed = json.loads(content)
            
            return CodeGenerationResponse(
                analysis_code=parsed.get('analysis_code', ''),
                code_explanation=parsed.get('code_explanation', ''),
                required_libraries=parsed.get('required_libraries', []),
                expected_outputs=parsed.get('expected_outputs', {}),
                success=True
            )
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse LLM response as JSON: {str(e)}")
            self.logger.warning("LLM may have ignored JSON format instructions - attempting raw Python extraction")
            
            # Last resort: Extract raw Python code (when LLM completely ignores JSON format)
            python_code_pattern = r'```python\s*\n(.*?)\n```'
            match = re.search(python_code_pattern, response_content, re.DOTALL)
            
            if match:
                extracted_code = match.group(1).strip()
                self.logger.info("Successfully extracted raw Python code from markdown block")
                return CodeGenerationResponse(
                    analysis_code=extracted_code,
                    code_explanation="Extracted raw Python code - LLM ignored JSON format",
                    required_libraries=["pandas", "numpy", "scipy", "statistics", "json"],
                    expected_outputs={"note": "Extracted from raw Python fallback"},
                    success=True
                )
            
            # Complete failure - return error
            return CodeGenerationResponse(
                analysis_code="",
                code_explanation="",
                required_libraries=[],
                expected_outputs={},
                success=False,
                error_message=f"Failed to parse response: {str(e)}"
            )
    
    def validate_generated_code(self, code: str) -> Dict[str, Any]:
        """
        Validate generated code for basic syntax and security.
        
        Args:
            code: Python code to validate
            
        Returns:
            Dictionary with validation results
        """
        validation_result = {
            "syntax_valid": False,
            "security_safe": False,
            "issues": []
        }
        
        # Basic syntax validation
        try:
            compile(code, '<string>', 'exec')
            validation_result["syntax_valid"] = True
        except SyntaxError as e:
            validation_result["issues"].append(f"Syntax error: {str(e)}")
        
        # Basic security checks
        dangerous_patterns = [
            'import os', 'import subprocess', 'import sys', '__import__',
            'exec(', 'eval(', 'open(', 'file(', 'input(', 'raw_input('
        ]
        
        security_safe = True
        for pattern in dangerous_patterns:
            if pattern in code:
                validation_result["issues"].append(f"Potentially unsafe pattern: {pattern}")
                security_safe = False
        
        validation_result["security_safe"] = security_safe
        
        return validation_result 