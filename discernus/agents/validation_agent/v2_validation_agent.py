#!/usr/bin/env python3
"""
V2 Validation Agent

Validates experiment artifacts against Discernus specifications and provides
clear, actionable error messages with suggested fixes.

THIN approach: Uses LLM intelligence to validate instead of complex rule-based validation.
Follows V2 architecture with externalized YAML prompts and RunContext data handoffs.
"""

import json
import logging
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

from discernus.core.standard_agent import StandardAgent
from discernus.core.run_context import RunContext
from discernus.core.agent_result import AgentResult
from discernus.core.validation import ValidationIssue, ValidationResult
from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry


class V2ValidationAgent(StandardAgent):
    """
    V2 validation agent that checks experiment artifacts against Discernus specifications.
    
    Provides clear, actionable error messages without dialog complexity.
    Follows THIN architecture with externalized YAML prompts.
    """

    def __init__(self, security, storage, audit, config=None):
        """Initialize the V2 validation agent."""
        super().__init__(security, storage, audit, config)
        self.agent_name = "V2ValidationAgent"
        self.logger = logging.getLogger(__name__)
        
        # Initialize LLM gateway
        model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(model_registry)
        self.model = "vertex_ai/gemini-2.5-pro"  # Default model for validation
        
        # Load externalized YAML prompt template
        self.prompt_template = self._load_prompt_template()
        
        self.logger.info(f"Initialized {self.agent_name}")

    def get_capabilities(self) -> List[str]:
        """Return the capabilities of this validation agent."""
        return ["validation", "verification", "coherence_checking"]

    def _load_prompt_template(self) -> str:
        """Load externalized YAML prompt template."""
        agent_dir = Path(__file__).parent
        prompt_path = agent_dir / 'prompt.yaml'
        
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
        
        with open(prompt_path, 'r') as f:
            prompt_content = f.read()
            prompt_data = yaml.safe_load(prompt_content)
        
        if 'template' not in prompt_data:
            raise ValueError(f"Prompt file missing 'template' key: {prompt_path}")
        
        return prompt_data['template']

    def execute(self, run_context: RunContext, **kwargs) -> AgentResult:
        """
        V2 StandardAgent execute method.
        
        Args:
            run_context: The RunContext object containing all necessary data
            
        Returns:
            AgentResult containing validation results and artifact hash
        """
        self.logger.info(f"Starting {self.agent_name} validation for experiment_id: {run_context.experiment_id}")
        
        try:
            self.log_execution_start(run_context=run_context, **kwargs)

            # 1. Validate and extract necessary data from RunContext
            validation_inputs = self._validate_and_extract_inputs(run_context)

            # 2. Perform validation using LLM
            self.logger.info("Performing experiment validation...")
            validation_result = self._perform_validation(validation_inputs)

            # 3. Store validation results
            artifact_hash = self._store_validation_results(validation_result, run_context)

            # 4. Check if validation was successful
            if not validation_result.success:
                blocking_issues = [issue for issue in validation_result.issues if issue.priority == "BLOCKING"]
                if blocking_issues:
                    # Create detailed error message with actual issue descriptions
                    issue_details = []
                    for issue in blocking_issues:
                        issue_details.append(f"• {issue.description}")
                        if hasattr(issue, 'fix') and issue.fix:
                            issue_details.append(f"  Fix: {issue.fix}")
                    
                    error_msg = f"Validation failed with {len(blocking_issues)} blocking issue(s):\n" + "\n".join(issue_details)
                    self.logger.error(error_msg)
                    return AgentResult(
                        success=False,
                        artifacts=[],
                        metadata={"agent_name": self.agent_name, "error": error_msg},
                        error_message=error_msg
                    )

            # 5. Log completion and return success
            result = AgentResult(
                success=True,
                artifacts=[artifact_hash],
                metadata={
                    "agent_name": self.agent_name,
                    "validation_success": validation_result.success,
                    "issues_count": len(validation_result.issues),
                    "blocking_issues": len([i for i in validation_result.issues if i.priority == "BLOCKING"])
                }
            )
            self.log_execution_complete(result)
            return result

        except Exception as e:
            self.logger.error(f"Validation failed: {str(e)}")
            return AgentResult(
                success=False,
                artifacts=[],
                metadata={"agent_name": self.agent_name, "error": str(e)},
                error_message=str(e)
            )

    def _validate_and_extract_inputs(self, run_context: RunContext) -> Dict[str, Any]:
        """Validate RunContext and extract all necessary data for validation."""
        if not run_context:
            raise ValueError("RunContext is required.")

        inputs = {}
        
        # Required metadata fields
        required_metadata = ["framework_content", "corpus_manifest_content"]
        for meta_field in required_metadata:
            if meta_field not in run_context.metadata:
                raise ValueError(f"RunContext metadata is missing required field: {meta_field}")
            inputs[meta_field] = run_context.metadata[meta_field]

        # Load experiment content from the experiment directory
        # According to v10.0 spec, all files (experiment.md, framework, corpus) are in the same directory
        experiment_dir = Path(run_context.framework_path).parent
        experiment_file_path = experiment_dir / 'experiment.md'
        if experiment_file_path.exists():
            inputs['experiment_content'] = experiment_file_path.read_text(encoding='utf-8')
        else:
            raise ValueError(f"Experiment file not found: {experiment_file_path}")

        # Load current specifications for compliance validation
        inputs['specification_references'] = self._load_specification_references()

        return inputs

    def _perform_validation(self, inputs: Dict[str, Any]) -> ValidationResult:
        """Perform validation using LLM."""
        try:
            # Create validation prompt
            prompt = self._create_validation_prompt(inputs)
            
            # Use structured output for validation results
            response_schema = {
                "type": "object",
                "properties": {
                    "success": {
                        "type": "boolean",
                        "description": "Whether the experiment is valid"
                    },
                    "issues": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "category": {"type": "string"},
                                "description": {"type": "string"},
                                "impact": {"type": "string"},
                                "fix": {"type": "string"},
                                "priority": {"type": "string"},
                                "affected_files": {"type": "array", "items": {"type": "string"}}
                            },
                            "required": ["category", "description", "impact", "fix", "priority", "affected_files"]
                        },
                        "description": "List of validation issues found"
                    },
                    "suggestions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of general suggestions"
                    }
                },
                "required": ["success", "issues", "suggestions"]
            }
            
            # Call LLM for validation
            raw_response, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=prompt,
                system_prompt="You are a validation expert for the Discernus research platform.",
                response_schema=response_schema
            )

            # Check if the LLM call was successful
            if not metadata.get("success", False):
                error_msg = metadata.get("error", "Unknown LLM call failure")
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

            # Parse validation result
            if isinstance(raw_response, dict):
                issues = []
                for issue_data in raw_response.get('issues', []):
                    issues.append(ValidationIssue(
                        category=issue_data.get('category', 'unknown'),
                        description=issue_data.get('description', 'Unknown issue'),
                        impact=issue_data.get('impact', 'Unknown impact'),
                        fix=issue_data.get('fix', 'No fix provided'),
                        priority=issue_data.get('priority', 'BLOCKING'),
                        affected_files=issue_data.get('affected_files', [])
                    ))
                
                return ValidationResult(
                    success=raw_response.get('success', False),
                    issues=issues,
                    suggestions=raw_response.get('suggestions', [])
                )
            else:
                # Fallback parsing
                return self._parse_validation_response(str(raw_response))

        except Exception as e:
            self.logger.error(f"Validation failed: {str(e)}")
            return ValidationResult(
                success=False,
                issues=[ValidationIssue(
                    category="validation_error",
                    description=f"Validation failed: {str(e)}",
                    impact="Cannot determine validation status",
                    fix="Check validation agent configuration",
                    priority="BLOCKING",
                    affected_files=[]
                )],
                suggestions=["Contact system administrator if issue persists"]
            )

    def _create_validation_prompt(self, inputs: Dict[str, Any]) -> str:
        """Create validation prompt using externalized YAML template."""
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Extract capabilities registry from specification references
        capabilities_registry = inputs.get("specification_references", {}).get("capabilities", "Capabilities registry not available")
        
        return self.prompt_template.format(
            current_date=current_date,
            experiment_spec=json.dumps(inputs.get("experiment_content", ""), indent=2),
            framework_spec=inputs.get("framework_content", ""),
            corpus_manifest=json.dumps(inputs.get("corpus_manifest_content", ""), indent=2),
            specification_references=json.dumps(inputs.get("specification_references", {}), indent=2),
            capabilities_registry=capabilities_registry
        )

    def _parse_validation_response(self, response: str) -> ValidationResult:
        """Parse LLM validation response using THIN principles."""
        try:
            # Try to find JSON in the response (handle markdown code blocks)
            json_content = response.strip()
            
            # Look for JSON in markdown code blocks
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.rfind("```")
                if json_end > json_start:
                    json_content = response[json_start:json_end].strip()
            elif "```" in response:
                # Try to find any code block
                code_start = response.find("```") + 3
                code_end = response.rfind("```")
                if code_end > code_start:
                    json_content = response[code_start:code_end].strip()
            
            # Parse the JSON content
            data = json.loads(json_content)
            
            # Convert to ValidationResult
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
            
        except Exception as e:
            return ValidationResult(
                success=False,
                issues=[ValidationIssue(
                    category="llm_response_error",
                    description=f"Could not parse LLM response: {str(e)}",
                    impact="Validation cannot be completed",
                    fix="Check LLM response format and prompt clarity",
                    priority="BLOCKING",
                    affected_files=[]
                )],
                suggestions=["Review prompt template for JSON format requirements"]
            )

    def _store_validation_results(self, validation_result: ValidationResult, run_context: RunContext) -> str:
        """Store validation results as a structured artifact."""
        timestamp = datetime.now().isoformat()
        
        # Prepare artifact data
        artifact_data = {
            "validation_success": validation_result.success,
            "issues": [
                {
                    "category": issue.category,
                    "description": issue.description,
                    "impact": issue.impact,
                    "fix": issue.fix,
                    "priority": issue.priority,
                    "affected_files": issue.affected_files
                }
                for issue in validation_result.issues
            ],
            "suggestions": validation_result.suggestions,
            "metadata": {
                "agent": self.agent_name,
                "timestamp": timestamp,
                "experiment_id": run_context.experiment_id,
                "validation_type": "experiment_coherence"
            }
        }
        
        # Store as JSON artifact
        artifact_content = json.dumps(artifact_data, indent=2).encode('utf-8')
        artifact_hash = self.storage.put_artifact(
            content=artifact_content,
            metadata={
                "artifact_type": "validation_report",
                "agent": self.agent_name,
                "timestamp": timestamp,
                "experiment_id": run_context.experiment_id
            }
        )
        
        self.logger.info(f"Validation results stored as artifact: {artifact_hash}")
        return artifact_hash

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
            
            # Load specification files
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
            
            return specifications
            
        except Exception as e:
            self.logger.warning(f"Could not load specification references: {str(e)}")
            # Return empty specs if loading fails
            return {
                "corpus": "# Corpus Specification\n\nCould not load specification reference",
                "experiment": "# Experiment Specification\n\nCould not load specification reference",
                "framework": "# Framework Specification\n\nCould not load specification reference"
            }
