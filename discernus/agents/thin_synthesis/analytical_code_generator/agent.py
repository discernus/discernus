#!/usr/bin/env python3
"""
AnalyticalCodeGenerator Agent - THIN Architecture

Generates Python code for statistical analysis using externalized YAML prompts.
Follows THIN principles: prompts externalized, minimal coordination logic only.
"""

import json
import logging
import re
import yaml
from pathlib import Path
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
    actual_scores_sample: Optional[Dict] = None
    actual_evidence_sample: Optional[list] = None
    available_columns: Optional[list] = None
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
    THIN Architecture: External YAML prompts, minimal coordination logic.
    """
    
    def __init__(self, model: str = "vertex_ai/gemini-2.5-flash"):
        """Initialize with model and load YAML template."""
        self.model = model
        self.model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(self.model_registry)
        self.logger = logging.getLogger(__name__)
        self.prompt_template = self._load_prompt_template()
        
    def _load_prompt_template(self) -> str:
        """Load the prompt template from YAML file."""
        prompt_file = Path(__file__).parent / "prompt.yaml"
        with open(prompt_file, 'r') as f:
            config = yaml.safe_load(f)
            return config['template']
        
    def generate_analysis_code(self, request: CodeGenerationRequest) -> CodeGenerationResponse:
        """Generate Python analysis code based on framework specification."""
        try:
            # Format the prompt template with request data
            prompt = self.prompt_template.format(
                framework_spec=request.framework_spec,
                scores_csv_structure=request.scores_csv_structure,
                evidence_csv_structure=request.evidence_csv_structure,
                experiment_context=request.experiment_context or "Not provided",
                actual_scores_sample=request.actual_scores_sample or "Not provided",
                actual_evidence_sample=request.actual_evidence_sample or "Not provided", 
                available_columns=request.available_columns or "Not provided"
            )
            
            # Call LLM to generate code
            response_content, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=prompt,
                system_prompt="You are an expert data scientist and Python programmer.",
                temperature=0.1,
                max_tokens=4000
            )

            if not response_content or not metadata.get('success'):
                return CodeGenerationResponse(
                    analysis_code="", code_explanation="", required_libraries=[],
                    expected_outputs={}, success=False,
                    error_message=metadata.get('error', 'Empty response from LLM')
                )
            
            return self._parse_llm_response(response_content)
            
        except Exception as e:
            self.logger.error(f"Code generation failed: {str(e)}")
            return CodeGenerationResponse(
                analysis_code="", code_explanation="", required_libraries=[],
                expected_outputs={}, success=False, error_message=str(e)
            )
    
    def _parse_llm_response(self, response_content: str) -> CodeGenerationResponse:
        """Parse the LLM response into structured format."""
        try:
            # Extract JSON from markdown code blocks  
            code_block_pattern = r'```\s*(?:json)?\s*\n?(.*?)\n?```'
            match = re.search(code_block_pattern, response_content.strip(), re.DOTALL)
            content = match.group(1).strip() if match else response_content.strip()
            
            parsed = json.loads(content)
            return CodeGenerationResponse(
                analysis_code=parsed.get('analysis_code', ''),
                code_explanation=parsed.get('code_explanation', ''),
                required_libraries=parsed.get('required_libraries', []),
                expected_outputs=parsed.get('expected_outputs', {}),
                success=True
            )
            
        except json.JSONDecodeError:
            # Fallback: Extract raw Python code
            python_match = re.search(r'```python\s*\n(.*?)\n```', response_content, re.DOTALL)
            if python_match:
                return CodeGenerationResponse(
                    analysis_code=python_match.group(1).strip(),
                    code_explanation="Extracted raw Python code",
                    required_libraries=["pandas", "numpy", "scipy", "json"],
                    expected_outputs={},
                    success=True
                )
            
            return CodeGenerationResponse(
                analysis_code="", code_explanation="", required_libraries=[],
                expected_outputs={}, success=False,
                error_message="Failed to parse LLM response"
            )

if __name__ == "__main__":
    # Test the agent
    agent = AnalyticalCodeGenerator()
    test_request = CodeGenerationRequest(
        framework_spec="Test framework", scores_csv_structure="aid,score",
        evidence_csv_structure="aid,quote", experiment_context="Test"
    )
    response = agent.generate_analysis_code(test_request)
    print(f"🧪 Test: Success={response.success}")
    if response.success:
        print(f"Generated {len(response.analysis_code)} chars, libs: {response.required_libraries}")
    else:
        print(f"Error: {response.error_message}") 