#!/usr/bin/env python3
"""
ExperimentCoherenceAgent

Simple validation agent that checks experiment artifacts against Discernus specifications
and provides clear, actionable error messages with suggested fixes.

THIN approach: Uses LLM intelligence to validate instead of complex rule-based validation.
Follows THIN architecture with externalized YAML prompts.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

from discernus.core.base_agent import BaseAgent
from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry


@dataclass
class ValidationIssue:
    """Represents a validation issue with clear description and fix."""
    category: str
    description: str
    impact: str
    fix: str
    affected_files: Optional[List[str]] = None


@dataclass
class ValidationResult:
    """Result of experiment validation."""
    success: bool
    issues: List[ValidationIssue]
    suggestions: List[str]


class ExperimentCoherenceAgent(BaseAgent):
    """
    Validates experiment artifacts against Discernus specifications.
    
    Provides clear, actionable error messages without dialog complexity.
    Follows THIN architecture with externalized YAML prompts.
    """
    
    def __init__(self, model: str = "vertex_ai/gemini-2.5-flash"):
        super().__init__("ExperimentCoherenceAgent")
        self.model = model
        model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(model_registry)
        
        # Load externalized YAML prompt template
        self.prompt_template = self._load_prompt_template()
        
    def validate_experiment(self, experiment_path: Path) -> ValidationResult:
        """
        Validate experiment artifacts against specifications.
        
        Args:
            experiment_path: Path to experiment directory
            
        Returns:
            ValidationResult with issues and suggestions
        """
        try:
            # Load experiment artifacts
            experiment_spec = self._load_experiment_spec(experiment_path)
            framework_spec = self._load_framework_spec(experiment_path, experiment_spec)
            corpus_manifest = self._load_corpus_manifest(experiment_path, experiment_spec)
            
            # Create validation prompt
            validation_prompt = self._create_validation_prompt(
                experiment_spec, framework_spec, corpus_manifest
            )
            
            # Get LLM validation
            response, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=validation_prompt,
                system_prompt="You are a validation expert for the Discernus research platform."
            )
            
            # Parse validation result
            return self._parse_validation_response(response)
            
        except Exception as e:
            # Return validation failure for any loading errors
            return ValidationResult(
                success=False,
                issues=[ValidationIssue(
                    category="loading_error",
                    description=f"Failed to load experiment artifacts: {str(e)}",
                    impact="Cannot validate experiment setup",
                    fix="Check experiment directory structure and file permissions"
                )],
                suggestions=["Ensure experiment.md, framework.md, and corpus/ directory exist"]
            )
    
    def _load_experiment_spec(self, experiment_path: Path) -> Dict:
        """Load and parse experiment specification."""
        experiment_file = experiment_path / "experiment.md"
        if not experiment_file.exists():
            raise FileNotFoundError(f"experiment.md not found in {experiment_path}")
            
        with open(experiment_file, 'r') as f:
            content = f.read()
            
        # Extract YAML frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                return yaml.safe_load(parts[1])
            else:
                raise ValueError("Invalid experiment.md format (missing YAML frontmatter)")
        else:
            raise ValueError("experiment.md missing YAML frontmatter")
    
    def _load_framework_spec(self, experiment_path: Path, experiment_spec: Dict) -> str:
        """Load framework specification."""
        framework_file = experiment_path / experiment_spec.get('framework', 'framework.md')
        if not framework_file.exists():
            raise FileNotFoundError(f"Framework file not found: {framework_file}")
            
        with open(framework_file, 'r') as f:
            return f.read()
    
    def _load_corpus_manifest(self, experiment_path: Path, experiment_spec: Dict) -> Dict:
        """Load corpus manifest."""
        corpus_path = experiment_path / experiment_spec.get('corpus_path', 'corpus')
        corpus_manifest_file = corpus_path / "corpus.md"
        
        if not corpus_manifest_file.exists():
            raise FileNotFoundError(f"corpus.md not found in {corpus_path}")
            
        with open(corpus_manifest_file, 'r') as f:
            content = f.read()
            
        # Extract JSON manifest
        if '```json' in content:
            json_start = content.find('```json') + 7
            json_end = content.find('```', json_start)
            if json_end != -1:
                json_content = content[json_start:json_end].strip()
                return json.loads(json_content)
            else:
                raise ValueError("Invalid corpus.md format (malformed JSON block)")
        else:
            raise ValueError("corpus.md missing JSON manifest")
    
    def _create_validation_prompt(self, experiment_spec: Dict, framework_spec: str, corpus_manifest: Dict) -> str:
        """Create validation prompt using externalized YAML template."""
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        return self.prompt_template.format(
            current_date=current_date,
            experiment_spec=json.dumps(experiment_spec, indent=2),
            framework_spec=framework_spec[:2000] + "..." if len(framework_spec) > 2000 else framework_spec,
            corpus_manifest=json.dumps(corpus_manifest, indent=2)
        )
    
    def _parse_validation_response(self, response: str) -> ValidationResult:
        """Parse LLM validation response into structured result."""
        try:
            # Extract JSON from response
            if '```json' in response:
                json_start = response.find('```json') + 7
                json_end = response.find('```', json_start)
                if json_end != -1:
                    json_content = response[json_start:json_end].strip()
                    data = json.loads(json_content)
                else:
                    data = json.loads(response)
            else:
                data = json.loads(response)
            
            # Convert to ValidationResult
            issues = []
            for issue_data in data.get('issues', []):
                issues.append(ValidationIssue(
                    category=issue_data.get('category', 'unknown'),
                    description=issue_data.get('description', 'Unknown issue'),
                    impact=issue_data.get('impact', 'Unknown impact'),
                    fix=issue_data.get('fix', 'No fix provided'),
                    affected_files=issue_data.get('affected_files', [])
                ))
            
            return ValidationResult(
                success=data.get('success', False),
                issues=issues,
                suggestions=data.get('suggestions', [])
            )
            
        except Exception as e:
            # Return validation failure for parsing errors
            return ValidationResult(
                success=False,
                issues=[ValidationIssue(
                    category="parsing_error",
                    description=f"Failed to parse validation response: {str(e)}",
                    impact="Cannot determine validation status",
                    fix="Check validation agent configuration"
                )],
                suggestions=["Contact system administrator if issue persists"]
            ) 