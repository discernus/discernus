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

from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry
from discernus.core.audit_logger import AuditLogger
from discernus.core.parsing_utils import parse_llm_json_response


@dataclass
class ValidationIssue:
    """Represents a validation issue with clear description and fix."""
    category: str
    description: str
    impact: str
    fix: str
    priority: str = "BLOCKING"  # BLOCKING, QUALITY, SUGGESTION
    affected_files: Optional[List[str]] = None


@dataclass
class ValidationResult:
    """Result of experiment validation."""
    success: bool
    issues: List[ValidationIssue]
    suggestions: List[str]
    
    def has_blocking_issues(self) -> bool:
        """Check if any issues are blocking."""
        return any(issue.priority == "BLOCKING" for issue in self.issues)
    
    def get_issues_by_priority(self, priority: str) -> List[ValidationIssue]:
        """Get issues filtered by priority level."""
        return [issue for issue in self.issues if issue.priority == priority]


class ExperimentCoherenceAgent:
    """
    Validates experiment artifacts against Discernus specifications.
    
    Provides clear, actionable error messages without dialog complexity.
    Follows THIN architecture with externalized YAML prompts.
    """
    
    def __init__(self, 
                 model: str = "vertex_ai/gemini-2.5-pro",
                 audit_logger: Optional[AuditLogger] = None):
        self.model = model
        self.agent_name = "ExperimentCoherenceAgent"
        
        # Store audit logger (optional)
        self.audit_logger = audit_logger
        
        model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(model_registry)
        
        # Load externalized YAML prompt template
        self.prompt_template = self._load_prompt_template()
        
        # Log initialization (if audit logger available)
        if self.audit_logger:
            self.audit_logger.log_agent_event(
                self.agent_name,
                "initialization",
                {
                    "model": model,
                    "architecture": "mece_trinity_validation",
                    "capabilities": ["framework_validation", "experiment_validation", "corpus_validation", "trinity_coherence"]
                }
            )
    
    def _load_prompt_template(self) -> str:
        """Load externalized YAML prompt template."""
        import os
        import sys
        
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
        
    def validate_experiment(self, experiment_path: Path) -> ValidationResult:
        """
        Validate experiment artifacts against specifications.
        
        Args:
            experiment_path: Path to experiment directory
            
        Returns:
            ValidationResult with issues and suggestions
        """
        # Log validation start
        if self.audit_logger:
            self.audit_logger.log_agent_event(
                self.agent_name,
                "validation_start",
                {
                    "experiment_path": str(experiment_path),
                    "validation_type": "mece_trinity_coherence"
                }
            )
        
        try:
            # Load experiment artifacts
            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "loading_artifacts",
                    {"status": "starting"}
                )
            
            experiment_spec = self._load_experiment_spec(experiment_path)
            framework_spec = self._load_framework_spec(experiment_path, experiment_spec)
            corpus_manifest = self._load_corpus_manifest(experiment_path, experiment_spec)
            
            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "artifacts_loaded",
                    {
                        "experiment_name": experiment_spec.get("name", "unknown"),
                        "framework_path": experiment_spec.get("framework", "unknown"),
                        "corpus_path": experiment_spec.get("corpus_path", "unknown")
                    }
                )
            
            # Create validation prompt
            validation_prompt = self._create_validation_prompt(
                experiment_spec, framework_spec, corpus_manifest
            )
            
            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "llm_validation_prompt",
                    {"prompt": validation_prompt}
                )
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "llm_validation_start",
                    {"model": self.model}
                )
            
            # Add statistical prerequisite validation
            statistical_issues = self._validate_statistical_prerequisites(experiment_path, experiment_spec, corpus_manifest)
            
            # Get LLM validation
            response, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=validation_prompt,
                system_prompt="You are a validation expert for the Discernus research platform."
            )

            # Check if the LLM call was successful
            if not metadata.get("success", False):
                error_msg = metadata.get("error", "Unknown LLM call failure")
                if self.audit_logger:
                    self.audit_logger.log_error("llm_validation_failure", error_msg, {"agent": self.agent_name})
                return ValidationResult(
                    success=False,
                    issues=[ValidationIssue(
                        category="llm_call_failure",
                        description=f"LLM validation call failed: {error_msg}",
                        impact="Validation cannot be completed",
                        fix="Check LLM gateway configuration and model availability",
                        priority="BLOCKING",
                        affected_files=[]
                    )],
                    suggestions=["Verify LLM model availability and authentication"]
                )

            # Check if response is empty
            if not response or not response.strip():
                error_msg = "LLM returned empty response"
                if self.audit_logger:
                    self.audit_logger.log_error("llm_validation_empty_response", error_msg, {"agent": self.agent_name})
                return ValidationResult(
                    success=False,
                    issues=[ValidationIssue(
                        category="llm_empty_response",
                        description=f"LLM validation returned empty response: {error_msg}",
                        impact="Validation cannot be completed",
                        fix="Check LLM prompt and model configuration",
                        priority="BLOCKING",
                        affected_files=[]
                    )],
                    suggestions=["Review validation prompt template and model settings"]
                )

            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "llm_validation_response",
                    {"response": response}
                )
            
            # Parse validation result
            result = self._parse_validation_response(response)
            
            # Combine LLM validation issues with statistical prerequisite issues
            all_issues = statistical_issues + result.issues
            blocking_statistical_issues = [issue for issue in statistical_issues if issue.priority == "BLOCKING"]
            combined_result = ValidationResult(
                success=result.success and len(blocking_statistical_issues) == 0,
                issues=all_issues,
                suggestions=result.suggestions
            )
            
            # Log validation completion
            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "validation_complete",
                    {
                        "success": combined_result.success,
                        "issues_count": len(combined_result.issues),
                        "statistical_issues_count": len(statistical_issues),
                        "blocking_statistical_issues": len(blocking_statistical_issues)
                    }
                )
            
            return combined_result
            
        except Exception as e:
            # Log validation error
            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "validation_error",
                    {
                        "error": str(e),
                        "error_type": type(e).__name__,
                        "experiment_path": str(experiment_path)
                    }
                )
            
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
    
    def _validate_statistical_prerequisites(self, experiment_path: Path, experiment_spec: Dict, corpus_manifest: Dict) -> List[ValidationIssue]:
        """
        Validate statistical prerequisites for academically valid results.
        
        Args:
            experiment_path: Path to experiment directory
            experiment_spec: Experiment specification
            corpus_manifest: Corpus manifest data
            
        Returns:
            List of validation issues related to statistical prerequisites
        """
        issues = []
        
        # Sample size validation
        file_manifest = corpus_manifest.get('file_manifest', [])
        corpus_size = len(file_manifest)
        
        if corpus_size < 3:
            issues.append(ValidationIssue(
                category="statistical_validity",
                description=f"Insufficient corpus size: {corpus_size} documents",
                impact="Will produce perfect correlations and invalid statistical analysis",
                fix=f"Add {3 - corpus_size} more documents to corpus directory",
                priority="BLOCKING",
                affected_files=[str(experiment_path / experiment_spec.get('corpus_path', 'corpus'))]
            ))
        elif corpus_size < 5:
            issues.append(ValidationIssue(
                category="statistical_validity",
                description=f"Minimal corpus size: {corpus_size} documents",
                impact="Statistical power will be limited, results may be unstable",
                fix="Consider adding more documents for robust statistical analysis",
                priority="QUALITY",
                affected_files=[str(experiment_path / experiment_spec.get('corpus_path', 'corpus'))]
            ))
        
        # Framework complexity validation
        framework_path = experiment_path / experiment_spec.get('framework', 'framework.md')
        if framework_path.exists():
            try:
                with open(framework_path, 'r') as f:
                    framework_content = f.read()
                
                # Count expected dimensions (rough heuristic)
                dimension_indicators = ['score', 'dimension', 'axis', 'index']
                dimension_count = sum(framework_content.lower().count(indicator) for indicator in dimension_indicators)
                
                # If we have many expected dimensions but small corpus, warn about coverage
                if dimension_count > 10 and corpus_size < 10:
                    issues.append(ValidationIssue(
                        category="framework_coverage",
                        description=f"Complex framework ({dimension_count} dimension indicators) with small corpus ({corpus_size} documents)",
                        impact="Many framework dimensions may not be detectable, leading to calculation failures",
                        fix="Either simplify framework or expand corpus to ensure dimension coverage",
                        priority="QUALITY",
                        affected_files=[str(framework_path), str(experiment_path / experiment_spec.get('corpus_path', 'corpus'))]
                    ))
            except Exception as e:
                issues.append(ValidationIssue(
                    category="framework_analysis",
                    description=f"Could not analyze framework complexity: {str(e)}",
                    impact="Cannot predict framework dimension coverage",
                    fix="Ensure framework file is readable and well-formed",
                    priority="SUGGESTION",
                    affected_files=[str(framework_path)]
                                ))
            
            return issues
    
    def _request_llm_reformat(self, malformed_response: str) -> ValidationResult:
        """
        THIN Approach: Use LLM intelligence to reformat malformed JSON instead of complex parsing.
        
        This demonstrates THIN principles: when parsing fails, ask the LLM to fix it
        rather than writing complex extraction logic.
        """
        reformat_prompt = f"""
        The following response contains validation results but is not properly formatted JSON.
        Please reformat it as clean JSON matching this structure:
        
        {{
            "success": true/false,
            "issues": [
                {{
                    "category": "category_name",
                    "description": "issue description", 
                    "impact": "impact description",
                    "fix": "fix description",
                    "priority": "BLOCKING|QUALITY|SUGGESTION",
                    "affected_files": ["file1", "file2"]
                }}
            ],
            "suggestions": ["suggestion1", "suggestion2"]
        }}
        
        Original response to reformat:
        {malformed_response}
        
        Return only clean JSON, no markdown formatting or extra text.
        """
        
        try:
            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "llm_reformat_request",
                    {"reason": "malformed_json", "original_length": len(malformed_response)}
                )
            
            reformatted_response, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=reformat_prompt,
                system_prompt="You are a JSON formatting assistant. Return only clean JSON."
            )

            # Check if the LLM call was successful
            if not metadata.get("success", False):
                raise ValueError(f"LLM reformatting call failed: {metadata.get('error', 'Unknown error')}")

            # Check if response is empty
            if not reformatted_response or not reformatted_response.strip():
                raise ValueError("LLM returned empty response during reformatting")

            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "llm_reformat_response_received",
                    {"response_preview": reformatted_response[:200], "model": self.model}
                )
            
            # Try parsing the reformatted response
            data = json.loads(reformatted_response)
            
            # Convert to ValidationResult
            issues = []
            for issue_data in data.get('issues', []):
                issues.append(ValidationIssue(
                    category=issue_data.get('category', 'unknown'),
                    description=issue_data.get('description', 'Reformatted validation issue'),
                    impact=issue_data.get('impact', 'Unknown impact'),
                    fix=issue_data.get('fix', 'No fix provided'),
                    priority=issue_data.get('priority', 'SUGGESTION'),
                    affected_files=issue_data.get('affected_files', [])
                ))
            
            return ValidationResult(
                success=data.get('success', False),
                issues=issues,
                suggestions=data.get('suggestions', [])
            )
            
        except Exception as reformat_error:
            # Final fallback: return a validation failure
            return ValidationResult(
                success=False,
                issues=[ValidationIssue(
                    category="llm_response_error",
                    description=f"Could not parse or reformat LLM response: {str(reformat_error)}",
                    impact="Validation cannot be completed",
                    fix="Check LLM response format and prompt clarity",
                    priority="BLOCKING",
                    affected_files=[]
                )],
                suggestions=["Review prompt template for JSON format requirements"]
            )

    def _create_validation_prompt(self, experiment_spec: Dict, framework_spec: str, corpus_manifest: Dict) -> str:
        """Create validation prompt using externalized YAML template."""
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        return self.prompt_template.format(
            current_date=current_date,
            experiment_spec=json.dumps(experiment_spec, indent=2),
            framework_spec=framework_spec,
            corpus_manifest=json.dumps(corpus_manifest, indent=2)
        )
    
    def _parse_validation_response(self, response: str) -> ValidationResult:
        """
        Parse LLM validation response using THIN principles.
        
        THIN Approach: Trust LLM intelligence with simple parsing and graceful fallbacks.
        Avoid complex JSON extraction - let the LLM return clean JSON.
        """
        try:
            # THIN: Robust JSON parsing with markdown fallbacks
            data = parse_llm_json_response(
                response=response,
                llm_gateway=self.llm_gateway,
                model=self.model,
                audit_logger=self.audit_logger
            )
            
            # Convert to ValidationResult with LLM intelligence
            issues = []
            for issue_data in data.get('issues', []):
                issues.append(ValidationIssue(
                    category=issue_data.get('category', 'unknown'),
                    description=issue_data.get('description', 'Unknown issue'),
                    impact=issue_data.get('impact', 'Unknown impact'),
                    fix=issue_data.get('fix', 'No fix provided'),
                    priority=issue_data.get('priority', 'BLOCKING'),
                    affected_files=issue_data.get('affected_files', [])
                ))
            
            return ValidationResult(
                success=data.get('success', False),
                issues=issues,
                suggestions=data.get('suggestions', [])
            )
            
        except ValueError as parse_error:
            # The robust parser already tried all fallbacks including LLM reformatting
            if self.audit_logger:
                self.audit_logger.log_error(
                    "parsing_failed_all_fallbacks",
                    str(parse_error),
                    {
                        "agent": self.agent_name,
                        "response_preview": response[:500] if response else "EMPTY_RESPONSE",
                        "response_length": len(response) if response else 0,
                        "details": "Failed to parse response even after LLM reformatting fallbacks."
                    }
                )
            
            # Final fallback: return parsing error
            return ValidationResult(
                success=False,
                issues=[ValidationIssue(
                    category="llm_response_error",
                    description=f"Could not parse or reformat LLM response: {str(parse_error)}",
                    impact="Validation cannot be completed",
                    fix="Check LLM response format and prompt clarity",
                    priority="BLOCKING",
                    affected_files=[]
                )],
                suggestions=["Review prompt template for JSON format requirements"]
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