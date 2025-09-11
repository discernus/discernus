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
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry
from discernus.core.audit_logger import AuditLogger
import json
from discernus.core.validation import ValidationIssue, ValidationResult


class ExperimentCoherenceAgent:
    """
    Validates experiment artifacts against Discernus specifications.
    
    Provides clear, actionable error messages without dialog complexity.
    Follows THIN architecture with externalized YAML prompts.
    """
    
    def __init__(self, 
                 model: str = "vertex_ai/gemini-2.5-pro",
                 audit_logger: Optional[AuditLogger] = None,
                 specification_references: Optional[Dict[str, str]] = None):
        self.model = model
        self.agent_name = "ExperimentCoherenceAgent"
        
        # Store audit logger (optional)
        self.audit_logger = audit_logger
        self.specification_references = specification_references or {}
        
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
    
    def _find_and_load_framework(self, experiment_path: Path) -> str:
        """Find and load framework file using format-agnostic discovery."""
        # Common framework filenames to check
        framework_candidates = [
            "framework.md",
            "caf_v10.md", "cff_v10.md", "pdaf_v10.md", "chf_v10.md", "ecf_v10.md",
            "framework_v10.md",
            # Versioned framework files
            "caf_v10_0_1.md", "caf_v10_0_2.md", "caf_v10_0_3.md",
            "cff_v10_0_1.md", "cff_v10_0_2.md", "cff_v10_0_3.md", 
            "pdaf_v10_0_1.md", "pdaf_v10_0_2.md", "pdaf_v10_0_3.md",
            "chf_v10_0_1.md", "chf_v10_0_2.md", "chf_v10_0_3.md",
            "ecf_v10_0_1.md", "ecf_v10_0_2.md", "ecf_v10_0_3.md"
        ]
        
        for filename in framework_candidates:
            framework_file = experiment_path / filename
            if framework_file.exists():
                return framework_file.read_text(encoding='utf-8')
        
        # If no standard files found, raise error
        raise ValueError(f"No framework file found in {experiment_path}. Expected one of: {', '.join(framework_candidates)}")
    
    def _find_and_load_corpus(self, experiment_path: Path) -> str:
        """Find and load corpus manifest file using format-agnostic discovery."""
        # Common corpus manifest filenames to check
        corpus_candidates = [
            "corpus.md",
            "corpus_manifest.md",
            "corpus_v8.md"
        ]
        
        for filename in corpus_candidates:
            corpus_file = experiment_path / filename
            if corpus_file.exists():
                return corpus_file.read_text(encoding='utf-8')
        
        # If no standard files found, raise error
        raise ValueError(f"No corpus manifest found in {experiment_path}. Expected one of: {', '.join(corpus_candidates)}")
    
    def _load_current_specifications(self) -> str:
        """Load current specifications from docs/specifications/ for compliance validation."""
        # Find project root (go up from agent directory)
        current_dir = Path(__file__).parent
        project_root = None
        
        # Search up to 5 levels for project root
        for _ in range(5):
            if (current_dir / "docs" / "specifications").exists():
                project_root = current_dir
                break
            current_dir = current_dir.parent
        
        if not project_root:
            raise ValueError("Could not find project root with docs/specifications directory")
        
        specs_dir = project_root / "docs" / "specifications"
        specifications = []
        
        # Load all current specifications
        for spec_file in ["EXPERIMENT_SPECIFICATION.md", "FRAMEWORK_SPECIFICATION.md", "CORPUS_SPECIFICATION.md"]:
            spec_path = specs_dir / spec_file
            if spec_path.exists():
                content = spec_path.read_text(encoding='utf-8')
                specifications.append(f"=== {spec_file} ===\n{content}")
        
        return "\n\n".join(specifications)
    
    def _validate_corpus_yaml_syntax(self, corpus_manifest: str) -> ValidationResult:
        """
        Validate YAML syntax in corpus manifest before LLM processing.
        
        Args:
            corpus_manifest: Raw corpus manifest content
            
        Returns:
            ValidationResult with YAML syntax issues if any
        """
        try:
            # Extract YAML block from corpus manifest
            if '## Document Manifest' in corpus_manifest:
                _, yaml_block = corpus_manifest.split('## Document Manifest', 1)
                if '```yaml' in yaml_block:
                    yaml_start = yaml_block.find('```yaml') + 7
                    yaml_end = yaml_block.rfind('```')
                    if yaml_end > yaml_start:
                        yaml_content = yaml_block[yaml_start:yaml_end].strip()
                        # Test YAML parsing
                        yaml.safe_load(yaml_content)
                        return ValidationResult(success=True, issues=[], suggestions=[])
                    else:
                        return ValidationResult(
                            success=False,
                            issues=[ValidationIssue(
                                category="yaml_syntax",
                                description="Corpus manifest YAML block is not properly closed",
                                impact="Experiment cannot parse corpus metadata",
                                fix="Ensure YAML block ends with ``` delimiter",
                                priority="BLOCKING",
                                affected_files=["corpus.md"]
                            )],
                            suggestions=[]
                        )
                else:
                    return ValidationResult(
                        success=False,
                        issues=[ValidationIssue(
                            category="yaml_syntax",
                            description="Corpus manifest missing YAML code block",
                            impact="Experiment cannot parse corpus metadata",
                            fix="Add ```yaml ... ``` block in Document Manifest section",
                            priority="BLOCKING",
                            affected_files=["corpus.md"]
                        )],
                        suggestions=[]
                    )
            else:
                return ValidationResult(
                    success=False,
                    issues=[ValidationIssue(
                        category="yaml_syntax",
                        description="Corpus manifest missing '## Document Manifest' section",
                        impact="Experiment cannot parse corpus metadata",
                        fix="Add '## Document Manifest' section with YAML metadata",
                        priority="BLOCKING",
                        affected_files=["corpus.md"]
                    )],
                    suggestions=[]
                )
        except yaml.YAMLError as e:
            return ValidationResult(
                success=False,
                issues=[ValidationIssue(
                    category="yaml_syntax",
                    description=f"Invalid YAML syntax in corpus manifest: {str(e)}",
                    impact="Experiment cannot parse corpus metadata",
                    fix="Fix YAML syntax errors - check for unclosed blocks, invalid characters, or malformed structure",
                    priority="BLOCKING",
                    affected_files=["corpus.md"]
                )],
                suggestions=[]
            )
        except Exception as e:
            return ValidationResult(
                success=False,
                issues=[ValidationIssue(
                    category="yaml_syntax",
                    description=f"Error parsing corpus manifest: {str(e)}",
                    impact="Experiment cannot parse corpus metadata",
                    fix="Check corpus manifest format and structure",
                    priority="BLOCKING",
                    affected_files=["corpus.md"]
                )],
                suggestions=[]
            )
        
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
            # Load raw experiment content (format agnostic)
            experiment_spec_content = self._load_artifact(experiment_path, "experiment.md")
            
            # Find and load framework and corpus files (format agnostic discovery)
            framework_spec = self._find_and_load_framework(experiment_path)
            corpus_manifest = self._find_and_load_corpus(experiment_path)
            
            # Pre-validate YAML syntax in corpus manifest
            yaml_validation_result = self._validate_corpus_yaml_syntax(corpus_manifest)
            if not yaml_validation_result.success:
                return yaml_validation_result

            # Load current specifications for compliance validation
            specification_references = self._load_specification_references()

            # Assemble the prompt with raw content (let LLM handle parsing)
            prompt = self._create_validation_prompt(
                experiment_spec=experiment_spec_content,
                framework_spec=framework_spec,
                corpus_manifest=corpus_manifest,
                specification_references=specification_references
            )
            
            # Call LLM for validation
            raw_response, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=prompt,
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
            if not raw_response or not raw_response.strip():
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
                    {"response": raw_response}
                )
            
            # Parse validation result
            result = self._parse_validation_response(raw_response)
            
            # Use LLM validation results only (THIN approach - let LLM handle statistical validation)
            all_issues = result.issues
            combined_result = ValidationResult(
                success=result.success,
                issues=all_issues,
                suggestions=result.suggestions,
                llm_metadata=metadata
            )
            
            # Log validation completion
            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "validation_complete",
                    {
                        "success": combined_result.success,
                        "issues_count": len(combined_result.issues)
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
    
    def _load_artifact(self, experiment_path: Path, filename: str) -> str:
        """Load a single artifact (experiment.md, framework.md, corpus.md) from the experiment directory."""
        artifact_path = experiment_path / filename
        if not artifact_path.exists():
            raise FileNotFoundError(f"{filename} not found in {experiment_path}")
            
        with open(artifact_path, 'r') as f:
            return f.read()

    def _extract_paths_from_experiment(self, experiment_spec: Dict, experiment_path: Path) -> Tuple[str, str]:
        """Extract framework and corpus file paths from the experiment specification."""
        framework_path = experiment_spec.get('components', {}).get('framework')
        corpus_path = experiment_spec.get('components', {}).get('corpus')

        if not framework_path:
            raise ValueError("Framework path not found in experiment.md `components` section.")
        if not corpus_path:
            raise ValueError("Corpus path not found in experiment.md `components` section.")

        # Ensure framework_path is a file
        if not (experiment_path / framework_path).is_file():
            raise FileNotFoundError(f"Framework file not found: {experiment_path / framework_path}")

        # For v10, corpus path points to a file, not a directory
        if not (experiment_path / corpus_path).is_file():
            raise FileNotFoundError(f"Corpus manifest file not found: {experiment_path / corpus_path}")

        return framework_path, corpus_path
    
    def _validate_statistical_prerequisites(self, experiment_path: Path, experiment_spec: Dict, corpus_manifest: Dict) -> List[ValidationIssue]:
        """
        Validate statistical prerequisites for academically valid results.
        
        Args:
            experiment_path: Path to experiment directory
            experiment_spec: Experiment specification
            corpus_manifest: Parsed corpus manifest dictionary
            
        Returns:
            List of validation issues related to statistical prerequisites
        """
        issues = []
        
        # THIN approach: Let the LLM handle corpus parsing and validation
        # This method now just provides basic file accessibility checks
        
        # Check if corpus directory exists and has text files
        # Note: corpus.md is at project root, but text files are in corpus/ directory
        corpus_dir = experiment_path / "corpus"
        if corpus_dir.exists():
            corpus_files = list(corpus_dir.glob("*.txt"))
            corpus_size = len(corpus_files)
            
            if corpus_size < 3:
                issues.append(ValidationIssue(
                    category="statistical_validity",
                    description=f"Insufficient corpus size: {corpus_size} text files found",
                    impact="Will produce perfect correlations and invalid statistical analysis",
                    fix=f"Add {3 - corpus_size} more text files to corpus directory",
                    priority="BLOCKING",
                    affected_files=[str(corpus_dir)]
                ))
            elif corpus_size < 5:
                issues.append(ValidationIssue(
                    category="statistical_validity",
                    description=f"Minimal corpus size: {corpus_size} text files found",
                    impact="Statistical power will be limited, results may be unstable",
                    fix="Consider adding more text files for robust statistical analysis",
                    priority="QUALITY",
                    affected_files=[str(corpus_dir)]
                ))
        else:
            issues.append(ValidationIssue(
                category="corpus_accessibility",
                description=f"Corpus directory not found: {corpus_dir}",
                impact="Cannot access corpus files for analysis",
                fix="Ensure corpus directory exists and contains text files",
                priority="BLOCKING",
                affected_files=[str(corpus_dir)]
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

    def _create_validation_prompt(self, experiment_spec: Dict, framework_spec: str, corpus_manifest: Dict, specification_references: Dict[str, str]) -> str:
        """Create validation prompt using externalized YAML template."""
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Extract capabilities registry from specification references
        capabilities_registry = specification_references.get("capabilities", "Capabilities registry not available")
        
        return self.prompt_template.format(
            current_date=current_date,
            experiment_spec=json.dumps(experiment_spec, indent=2),
            framework_spec=framework_spec,
            corpus_manifest=json.dumps(corpus_manifest, indent=2),
            specification_references=json.dumps(specification_references, indent=2),
            capabilities_registry=capabilities_registry
        )
    
    def _parse_validation_response(self, response: str) -> ValidationResult:
        """
        Parse LLM validation response using THIN principles.
        
        THIN Approach: Trust LLM intelligence with simple parsing and graceful fallbacks.
        Avoid complex JSON extraction - let the LLM return clean JSON.
        """
        try:
            # THIN: Simple JSON parsing
            data = json.loads(response)
            
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

    def _load_specification_references(self) -> Dict[str, str]:
        """Load the latest specification reference documents."""
        try:
            # Find the project root by looking for docs/specifications
            current_dir = Path(__file__).parent
            project_root = current_dir
            while project_root != project_root.parent:
                if (project_root / "docs" / "specifications").exists():
                    break
                project_root = project_root.parent
            
            if project_root == project_root.parent:
                raise FileNotFoundError("Could not find project root with docs/specifications")
            
            specs_dir = project_root / "docs" / "specifications"
            
            # Load specification files (assume latest version)
            specifications = {}
            
            spec_files = {
                "corpus": "CORPUS_SPECIFICATION.md",
                "experiment": "EXPERIMENT_SPECIFICATION.md", 
                "framework": "FRAMEWORK_SPECIFICATION.md"
            }
            
            # Load capabilities registry
            capabilities_path = project_root / "discernus" / "core" / "presets" / "core_capabilities.yaml"
            if capabilities_path.exists():
                with open(capabilities_path, 'r', encoding='utf-8') as f:
                    capabilities_content = f.read()
                specifications["capabilities"] = capabilities_content
            
            for spec_type, filename in spec_files.items():
                spec_path = specs_dir / filename
                if spec_path.exists():
                    with open(spec_path, 'r') as f:
                        specifications[spec_type] = f.read()
                else:
                    specifications[spec_type] = f"# {spec_type.title()} Specification\n\nSpecification file not found: {filename}"
            
            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "specification_references_loaded",
                    {
                        "specs_loaded": list(specifications.keys()),
                        "specs_dir": str(specs_dir)
                    }
                )
            
            return specifications
            
        except Exception as e:
            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "specification_references_failed",
                    {"error": str(e)}
                )
            
            # Return empty specs if loading fails
            return {
                "corpus": "# Corpus Specification\n\nCould not load specification reference",
                "experiment": "# Experiment Specification\n\nCould not load specification reference",
                "framework": "# Framework Specification\n\nCould not load specification reference"
            } 