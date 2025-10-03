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
from datetime import datetime, timezone

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
        self.model = "vertex_ai/gemini-2.5-flash-lite"  # TEST: Flash Lite with reasoning=1
        
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

            # 1. Validate and extract necessary data from RunContext (always needed for file path population)
            validation_inputs = self._validate_and_extract_inputs(run_context)

            # 2. Check if LLM validation should be skipped
            skip_validation = run_context.metadata.get("skip_validation", False)
            
            if skip_validation:
                # Skip LLM validation but still populate file paths
                self.logger.info("Skipping LLM validation, but file paths have been populated")
                validation_result = ValidationResult(
                    success=True,
                    issues=[],
                    suggestions=[],
                    llm_metadata={"agent_name": self.agent_name, "validation_skipped": True}
                )
                artifact_hash = None  # No validation artifact when skipped
            else:
                # 3. Perform validation using LLM
                self.logger.info("Performing experiment validation...")
                validation_result = self._perform_validation(validation_inputs, run_context)

                # 4. Store validation results
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
            artifacts = [artifact_hash] if artifact_hash else []
            result = AgentResult(
                success=True,
                artifacts=artifacts,
                metadata={
                    "agent_name": self.agent_name,
                    "validation_success": validation_result.success,
                    "issues_count": len(validation_result.issues),
                    "blocking_issues": len([i for i in validation_result.issues if i.priority == "BLOCKING"]),
                    "validation_skipped": skip_validation
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

    def validate_experiment(self, experiment_path: Path) -> ValidationResult:
        """
        Standalone validation method for CLI validation command.
        
        Args:
            experiment_path: Path to experiment directory
            
        Returns:
            ValidationResult with issues and suggestions
        """
        self.logger.info(f"Starting standalone validation for experiment: {experiment_path}")
        
        try:
            # Load experiment content
            experiment_file = experiment_path / "experiment.md"
            if not experiment_file.exists():
                return ValidationResult(
                    success=False,
                    issues=[ValidationIssue(
                        category="missing_file",
                        description=f"experiment.md not found in {experiment_path}",
                        impact="Validation cannot be completed",
                        fix="Create experiment.md file in experiment directory",
                        priority="BLOCKING",
                        affected_files=["experiment.md"]
                    )],
                    suggestions=["Ensure experiment.md exists in the experiment directory"]
                )
            
            experiment_content = experiment_file.read_text(encoding='utf-8')
            
            # Find and load framework file
            framework_content = self._find_and_load_framework(experiment_path)
            
            # Find and load corpus manifest
            corpus_manifest_content = self._find_and_load_corpus(experiment_path)
            
            # Load specification references
            specification_references = self._load_specification_references()
            
            # Create validation inputs
            validation_inputs = {
                "experiment_content": experiment_content,
                "framework_content": framework_content,
                "corpus_manifest_content": corpus_manifest_content,
                "specification_references": specification_references,
                "corpus_directory_listing": self._get_corpus_directory_listing(experiment_path)
            }
            
            # Perform validation
            validation_result = self._perform_validation(validation_inputs)
            
            self.logger.info(f"Standalone validation completed: success={validation_result.success}")
            return validation_result
            
        except Exception as e:
            self.logger.error(f"Error in standalone validation: {e}")
            return ValidationResult(
                success=False,
                issues=[ValidationIssue(
                    category="validation_error",
                    description=f"Validation failed: {str(e)}",
                    impact="Validation cannot be completed",
                    fix="Check experiment structure and file accessibility",
                    priority="BLOCKING",
                    affected_files=[]
                )],
                suggestions=["Verify experiment directory structure and file permissions"]
            )

    def _find_and_load_framework(self, experiment_path: Path) -> str:
        """Find and load framework file using format-agnostic discovery."""
        # Look for any .md file that could be a framework
        framework_files = list(experiment_path.glob("*.md"))
        
        # Filter out known non-framework files
        excluded_files = {
            "experiment.md", "corpus.md", "corpus_manifest.md", 
            "README.md", "readme.md", "Readme.md"
        }
        
        framework_candidates = [
            f for f in framework_files 
            if f.name not in excluded_files
        ]
        
        if not framework_candidates:
            raise ValueError(f"No framework file found in {experiment_path}. Please add a framework file (any .md file except experiment.md, corpus.md, or README.md)")
        
        if len(framework_candidates) > 1:
            # If multiple potential frameworks, prefer common names
            preferred_names = ["framework.md", "framework_v10.md"]
            for preferred in preferred_names:
                for candidate in framework_candidates:
                    if candidate.name == preferred:
                        return candidate.read_text(encoding='utf-8')
        
        # Return the first (or only) framework file found
        return framework_candidates[0].read_text(encoding='utf-8')
    
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
    
    def _load_specification_references(self) -> Dict[str, str]:
        """Load current specifications from docs/specifications/ for compliance validation."""
        specs_dir = Path(__file__).parent.parent.parent.parent / "docs" / "specifications"
        references = {}
        
        if specs_dir.exists():
            for spec_file in specs_dir.glob("*.md"):
                try:
                    content = spec_file.read_text(encoding='utf-8')
                    references[spec_file.stem] = content
                except Exception as e:
                    self.logger.warning(f"Could not load specification {spec_file}: {e}")
        
        return references
    
    def _get_corpus_directory_listing(self, experiment_path: Path) -> List[str]:
        """Get listing of corpus directory for validation context."""
        corpus_dir = experiment_path / "corpus"
        if not corpus_dir.exists():
            return []
        
        try:
            return [str(f.relative_to(experiment_path)) for f in corpus_dir.rglob("*") if f.is_file()]
        except Exception as e:
            self.logger.warning(f"Could not list corpus directory: {e}")
            return []

    def _validate_and_extract_inputs(self, run_context: RunContext) -> Dict[str, Any]:
        """THIN: Read files from disk and pass directly to LLM. Let LLM handle parsing."""
        if not run_context:
            raise ValueError("RunContext is required.")

        experiment_dir = Path(run_context.experiment_dir)
        
        # THIN: Just read files and register in CAS - no parsing
        try:
            # 1. Read and register experiment.md
            experiment_file_path = experiment_dir / 'experiment.md'
            if not experiment_file_path.exists():
                raise ValueError(f"Experiment file not found: {experiment_file_path}")
            experiment_hash = self.storage.put_file(experiment_file_path, {"artifact_type": "experiment_spec"})
            experiment_content = experiment_file_path.read_text(encoding='utf-8')
            
            # 2. Read and register framework.md
            framework_path = experiment_dir / 'framework.md'
            if not framework_path.exists():
                raise ValueError(f"Framework file not found: {framework_path}")
            framework_hash = self.storage.put_file(framework_path, {"artifact_type": "framework"})
            framework_content = framework_path.read_text(encoding='utf-8')
            
            # 3. Read and register corpus.md
            corpus_path = experiment_dir / 'corpus.md'
            if not corpus_path.exists():
                raise ValueError(f"Corpus manifest file not found: {corpus_path}")
            corpus_manifest_hash = self.storage.put_file(corpus_path, {"artifact_type": "corpus_manifest"})
            corpus_manifest_content = corpus_path.read_text(encoding='utf-8')
            
            # 4. THIN: Just scan corpus directory and register all files - no parsing
            corpus_dir = experiment_dir / 'corpus'
            if not corpus_dir.exists():
                raise ValueError(f"Corpus directory not found: {corpus_dir}")
            
            corpus_document_hashes = []
            corpus_files = []
            
            # Simply register all .txt files in corpus directory
            for file_path in corpus_dir.glob("*.txt"):
                doc_hash = self.storage.put_file(file_path, {
                    "artifact_type": "corpus_document",
                    "filename": file_path.name
                })
                corpus_document_hashes.append(doc_hash)
                corpus_files.append(file_path.name)
            
            # Store CAS hashes in run_context metadata
            run_context.metadata["experiment_hash"] = experiment_hash
            run_context.metadata["framework_hash"] = framework_hash
            run_context.metadata["corpus_manifest_hash"] = corpus_manifest_hash
            run_context.metadata["corpus_document_hashes"] = corpus_document_hashes
            run_context.metadata["document_count"] = len(corpus_document_hashes)
            
            self.logger.info(f"THIN file registration complete - experiment: {experiment_hash[:8]}, "
                           f"framework: {framework_hash[:8]}, corpus_manifest: {corpus_manifest_hash[:8]}, "
                           f"corpus_docs: {len(corpus_document_hashes)}")
            
            # THIN: Pass raw content directly to LLM - let LLM handle all parsing
            return {
                "experiment_content": experiment_content,
                "framework_content": framework_content,
                "corpus_manifest_content": corpus_manifest_content,
                "corpus_directory_listing": sorted(corpus_files),
                "specification_references": self._load_specification_references()
            }
            
        except Exception as e:
            raise ValueError(f"Failed to read experiment files from {experiment_dir}: {e}")

    def _perform_validation(self, inputs: Dict[str, Any], run_context: RunContext) -> ValidationResult:
        """Perform validation using LLM."""
        try:
            # Pre-validate corpus YAML syntax and file accessibility
            # Get experiment path from run_context
            experiment_path = Path(run_context.experiment_dir)
            corpus_manifest = inputs['corpus_manifest_content']
            
            # 1. Validate corpus YAML syntax
            yaml_validation_result = self._validate_corpus_yaml_syntax(corpus_manifest)
            if not yaml_validation_result.success:
                return yaml_validation_result
            
            # 2. Validate corpus file accessibility
            corpus_accessibility_issues = self._validate_corpus_file_accessibility(experiment_path, corpus_manifest)
            if corpus_accessibility_issues:
                # Check if any are blocking issues
                blocking_issues = [issue for issue in corpus_accessibility_issues if issue.priority == "BLOCKING"]
                if blocking_issues:
                    return ValidationResult(
                        success=False,
                        issues=corpus_accessibility_issues,
                        suggestions=[]
                    )
                # If only quality issues, continue but include them in final result
                # (We'll combine them with LLM results later)
            
            # Create validation prompt
            prompt = self._create_validation_prompt(inputs)
            
            # Call LLM for validation (no structured output - THIN approach)
            raw_response, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=prompt,
                system_prompt="You are a validation expert for the Discernus research platform.",
                reasoning=1  # Enable reasoning parameter for Flash Lite
            )

            # Log LLM interaction with cost data
            if metadata and 'usage' in metadata:
                usage_data = metadata['usage']
                self.audit.log_llm_interaction(
                    model=self.model,
                    prompt=prompt,
                    response=str(raw_response),
                    agent_name=self.agent_name,
                    interaction_type="experiment_validation",
                    metadata={
                        "prompt_tokens": usage_data.get('prompt_tokens', 0),
                        "completion_tokens": usage_data.get('completion_tokens', 0),
                        "total_tokens": usage_data.get('total_tokens', 0),
                        "response_cost_usd": usage_data.get('response_cost_usd', 0.0),
                        "validation_type": "experiment_validation"
                    }
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

            # Parse validation result from markdown fences - THIN approach
            llm_validation_result = self._parse_validation_response(raw_response)
            
            # Combine LLM results with corpus accessibility issues
            all_issues = list(llm_validation_result.issues)
            if corpus_accessibility_issues:
                all_issues.extend(corpus_accessibility_issues)
            
            return ValidationResult(
                success=llm_validation_result.success,
                issues=all_issues,
                suggestions=llm_validation_result.suggestions,
                llm_metadata=llm_validation_result.llm_metadata
            )

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

    def _validate_corpus_file_accessibility(self, experiment_path: Path, corpus_manifest: str) -> List[ValidationIssue]:
        """
        Validate that files listed in corpus manifest actually exist in corpus directory.
        
        Args:
            experiment_path: Path to experiment directory
            corpus_manifest: Raw corpus manifest content
            
        Returns:
            List of validation issues related to file accessibility
        """
        issues = []
        
        try:
            # Extract document list from corpus manifest
            document_files = self._extract_document_files_from_manifest(corpus_manifest)
            
            if not document_files:
                issues.append(ValidationIssue(
                    category="corpus_accessibility",
                    description="No document files found in corpus manifest",
                    impact="Cannot access corpus files for analysis",
                    fix="Ensure corpus manifest lists actual document files",
                    priority="BLOCKING",
                    affected_files=["corpus.md"]
                ))
                return issues
            
            # Check corpus directory exists
            corpus_dir = experiment_path / "corpus"
            if not corpus_dir.exists():
                issues.append(ValidationIssue(
                    category="corpus_accessibility",
                    description=f"Corpus directory not found: {corpus_dir}",
                    impact="Cannot access corpus files for analysis",
                    fix="Ensure corpus directory exists and contains text files",
                    priority="BLOCKING",
                    affected_files=[str(corpus_dir)]
                ))
                return issues
            
            # Check each file listed in manifest
            missing_files = []
            actual_files = set(f.name for f in corpus_dir.glob("*.txt"))
            
            for doc_file in document_files:
                if doc_file not in actual_files:
                    missing_files.append(doc_file)
            
            if missing_files:
                issues.append(ValidationIssue(
                    category="corpus_accessibility",
                    description=f"Files listed in manifest not found in corpus directory: {', '.join(missing_files[:5])}{'...' if len(missing_files) > 5 else ''}",
                    impact="Cannot access specified corpus files for analysis",
                    fix=f"Ensure all files listed in corpus manifest exist in {corpus_dir} directory",
                    priority="BLOCKING",
                    affected_files=["corpus.md", str(corpus_dir)]
                ))
            
            # Check for files in directory not listed in manifest
            manifest_files = set(document_files)
            unlisted_files = actual_files - manifest_files
            
            if unlisted_files:
                issues.append(ValidationIssue(
                    category="corpus_coherence",
                    description=f"Files in corpus directory not listed in manifest: {', '.join(list(unlisted_files)[:5])}{'...' if len(unlisted_files) > 5 else ''}",
                    impact="Corpus manifest does not accurately reflect available files",
                    fix="Update corpus manifest to include all files in corpus directory or remove unlisted files",
                    priority="QUALITY",
                    affected_files=["corpus.md", str(corpus_dir)]
                ))
            
            # Validate document count consistency
            manifest_count = len(document_files)
            actual_count = len(actual_files)
            
            if manifest_count != actual_count:
                issues.append(ValidationIssue(
                    category="corpus_coherence",
                    description=f"Document count mismatch: manifest claims {manifest_count} documents, directory contains {actual_count}",
                    impact="Corpus manifest does not accurately reflect available files",
                    fix="Update corpus manifest to match actual files in directory",
                    priority="BLOCKING",
                    affected_files=["corpus.md", str(corpus_dir)]
                ))
            
        except Exception as e:
            issues.append(ValidationIssue(
                category="corpus_validation_error",
                description=f"Error validating corpus file accessibility: {str(e)}",
                impact="Cannot verify corpus file accessibility",
                fix="Check corpus manifest format and directory structure",
                priority="BLOCKING",
                affected_files=["corpus.md"]
            ))
        
        return issues
    
    def _extract_document_files_from_manifest(self, corpus_manifest: str) -> List[str]:
        """Extract list of document files from corpus manifest."""
        import re
        
        document_files = []
        
        # Look for file references in the manifest
        # Pattern: **filename.txt** or filename.txt
        file_patterns = [
            r'\*\*([^*]+\.txt)\*\*',  # **filename.txt**
            r'`([^`]+\.txt)`',        # `filename.txt`
        ]
        
        for pattern in file_patterns:
            matches = re.findall(pattern, corpus_manifest)
            document_files.extend(matches)
        
        # Remove duplicates and return
        return list(set(document_files))
    
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
            # Look for either "Document Manifest" or "Document Inventory" sections
            if '## Document Manifest' in corpus_manifest:
                _, yaml_block = corpus_manifest.split('## Document Manifest', 1)
            elif '## Document Inventory' in corpus_manifest:
                _, yaml_block = corpus_manifest.split('## Document Inventory', 1)
            else:
                yaml_block = ""
            
            if yaml_block and '```yaml' in yaml_block:
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
                        fix="Add ```yaml ... ``` block in Document Inventory section",
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

    def _parse_validation_response(self, response: str) -> ValidationResult:
        """
        Parse validation response from markdown fences - THIN approach.
        
        Expected format:
        ```validation
        SUCCESS: true/false
        
        ISSUES:
        - Category: issue_category
          Description: issue description
          Impact: impact description
          Fix: suggested fix
          Priority: BLOCKING/WARNING/INFO
          Files: file1, file2
        ```
        """
        try:
            # Extract content from markdown fences
            if "```validation" in response:
                start = response.find("```validation") + len("```validation")
                end = response.find("```", start)
                if end == -1:
                    end = len(response)
                content = response[start:end].strip()
            else:
                content = response.strip()
            
            # Parse success status
            success = "SUCCESS: true" in content or "SUCCESS:true" in content
            
            # Parse issues
            issues = []
            if "ISSUES:" in content:
                issues_section = content.split("ISSUES:")[1]
                if "SUGGESTIONS:" in issues_section:
                    issues_section = issues_section.split("SUGGESTIONS:")[0]
                
                # Split by issue markers
                issue_blocks = [block.strip() for block in issues_section.split("- Category:") if block.strip()]
                
                for block in issue_blocks:
                    if not block:
                        continue
                    
                    # Parse issue fields
                    lines = [line.strip() for line in block.split('\n') if line.strip()]
                    issue_data = {}
                    
                    for line in lines:
                        if line.startswith("Category:"):
                            issue_data['category'] = line.split("Category:")[1].strip()
                        elif line.startswith("Description:"):
                            issue_data['description'] = line.split("Description:")[1].strip()
                        elif line.startswith("Impact:"):
                            issue_data['impact'] = line.split("Impact:")[1].strip()
                        elif line.startswith("Fix:"):
                            issue_data['fix'] = line.split("Fix:")[1].strip()
                        elif line.startswith("Priority:"):
                            issue_data['priority'] = line.split("Priority:")[1].strip()
                        elif line.startswith("Files:"):
                            files_str = line.split("Files:")[1].strip()
                            issue_data['affected_files'] = [f.strip() for f in files_str.split(',') if f.strip()]
                    
                    # Create ValidationIssue if we have required fields
                    if 'category' in issue_data and 'description' in issue_data:
                        issues.append(ValidationIssue(
                            category=issue_data.get('category', 'unknown'),
                            description=issue_data.get('description', 'Unknown issue'),
                            impact=issue_data.get('impact', 'Unknown impact'),
                            fix=issue_data.get('fix', 'No fix provided'),
                            priority=issue_data.get('priority', 'BLOCKING'),
                            affected_files=issue_data.get('affected_files', [])
                        ))
            
            # Parse suggestions
            suggestions = []
            if "SUGGESTIONS:" in content:
                suggestions_section = content.split("SUGGESTIONS:")[1]
                suggestion_lines = [line.strip() for line in suggestions_section.split('\n') if line.strip() and line.startswith('-')]
                suggestions = [line[1:].strip() for line in suggestion_lines]
            
            return ValidationResult(
                success=success,
                issues=issues,
                suggestions=suggestions
            )
            
        except Exception as e:
            self.logger.error(f"Failed to parse validation response: {str(e)}")
            return ValidationResult(
                success=False,
                issues=[ValidationIssue(
                    category="parsing_error",
                    description=f"Could not parse validation response: {str(e)}",
                    impact="Validation cannot be completed",
                    fix="Check LLM response format",
                    priority="BLOCKING",
                    affected_files=[]
                )],
                suggestions=["Verify LLM response format"]
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
            corpus_directory_listing=json.dumps(inputs.get("corpus_directory_listing", []), indent=2),
            specification_references=json.dumps(inputs.get("specification_references", {}), indent=2),
            capabilities_registry=capabilities_registry
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
