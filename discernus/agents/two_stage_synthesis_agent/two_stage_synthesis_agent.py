#!/usr/bin/env python3
"""
Two-Stage Synthesis Agent for Discernus
=======================================

Implements two-stage synthesis to prevent hallucination and ensure data-driven reports:

Stage 1: Data-Driven Analysis
- Input: Statistical results, experiment metadata, framework
- Process: Generate coherent analysis anchored in statistical findings
- Output: Complete research report without evidence quotes
- Goal: Establish all analytical claims based solely on data

Stage 2: Evidence Integration  
- Input: Stage 1 report + curated evidence from IntelligentEvidenceRetrievalAgent
- Process: Enhance report with supporting quotes, create evidence appendix
- Output: Final report with integrated evidence and complete audit trail
- Goal: Support existing claims with evidence, no new analytical claims

Anti-Hallucination Architecture:
- Stage separation prevents evidence from influencing analytical conclusions
- Stage 2 is strictly additive (quotes + appendix), no new analysis
- All claims must originate from Stage 1 statistical analysis
- Evidence serves only to illustrate pre-established findings
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

from discernus.core.standard_agent import StandardAgent
from discernus.core.agent_result import AgentResult
from discernus.core.run_context import RunContext
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.audit_logger import AuditLogger
from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway
from discernus.gateway.model_registry import ModelRegistry
import yaml


class TwoStageSynthesisAgent(StandardAgent):
    """
    Two-stage synthesis agent that prevents hallucination through architectural separation.
    
    The agent ensures all analytical claims originate from statistical data before any
    evidence integration, maintaining strict separation between analysis and illustration.
    """
    
    def __init__(self, 
                 security: ExperimentSecurityBoundary,
                 storage: LocalArtifactStorage,
                 audit: AuditLogger,
                 config: Optional[Dict[str, Any]] = None):
        """
        Initialize the TwoStageSynthesisAgent.
        
        Args:
            security: Security boundary for experiment access
            storage: Artifact storage interface
            audit: Audit logging interface
            config: Optional agent configuration
        """
        super().__init__(security, storage, audit, config)
        self.agent_name = "TwoStageSynthesisAgent"
        self.logger = logging.getLogger(__name__)
        
        # Initialize enhanced LLM gateway for tool calling
        model_registry = ModelRegistry()
        self.llm_gateway = EnhancedLLMGateway(model_registry)
        
        # Stage configuration
        self.stage1_model = "vertex_ai/gemini-2.5-pro"  # Pro for analytical depth
        self.stage2_model = "vertex_ai/gemini-2.5-flash"  # Flash for evidence integration
        
        # Load externalized prompts
        self.stage1_prompt = self._load_prompt_template("stage1_prompt.yaml")
        self.stage2_prompt = self._load_prompt_template("stage2_prompt.yaml")
        
        self.logger.info(f"Initialized {self.agent_name} with two-stage architecture and externalized prompts")
    
    def _load_prompt_template(self, filename: str) -> str:
        """Load a prompt template from the YAML file."""
        prompt_path = Path(__file__).parent / filename
        if not prompt_path.exists():
            error_msg = f"TwoStageSynthesisAgent prompt file not found at {prompt_path}"
            self.audit.log_agent_event(self.agent_name, "prompt_error", {"error": error_msg})
            raise FileNotFoundError(error_msg)
        
        with open(prompt_path, 'r') as f:
            yaml_content = f.read()
        prompt_data = yaml.safe_load(yaml_content)
        return prompt_data['template']
    
    def get_capabilities(self) -> List[str]:
        """Return list of agent capabilities."""
        return [
            "two_stage_synthesis",
            "anti_hallucination_architecture", 
            "data_driven_analysis",
            "evidence_integration",
            "evidence_appendix_generation",
            "analytical_claim_validation",
            "statistical_anchoring",
            "externalized_prompts",
            "tool_calling"
        ]
    
    def execute(self, run_context: RunContext, **kwargs) -> AgentResult:
        """
        Execute two-stage synthesis process.
        
        Args:
            run_context: The RunContext containing all experiment data
            **kwargs: Additional execution parameters
            
        Returns:
            AgentResult with final synthesis report and evidence appendix
        """
        try:
            self.logger.info("TwoStageSynthesisAgent starting two-stage execution")
            self.logger.info(f"Run context type: {type(run_context).__name__}")
            self.logger.info(f"Storage object: {type(self.storage).__name__}")
            self.logger.info(f"Storage available: {self.storage is not None}")
            
            self.logger.info("About to call log_execution_start...")
            self.log_execution_start(**kwargs)
            self.logger.info("log_execution_start completed successfully")
            
            # Validate inputs
            self.logger.info("Starting input validation...")
            try:
                validation_result = self._validate_inputs(run_context)
                self.logger.info(f"Input validation result: {validation_result}")
                if not validation_result:
                    self.logger.error("Input validation failed - returning early")
                    return AgentResult(
                        success=False,
                        artifacts=[],
                        metadata={"agent_name": self.agent_name, "error": "Input validation failed"},
                        error_message="Required inputs missing for synthesis"
                    )
                self.logger.info("Input validation passed - proceeding with synthesis")
            except Exception as e:
                self.logger.error(f"Exception during input validation: {e}")
                self.logger.error(f"Exception type: {type(e).__name__}")
                import traceback
                self.logger.error(f"Traceback: {traceback.format_exc()}")
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": f"Input validation exception: {e}"},
                    error_message=f"Input validation failed with exception: {e}"
                )
            
            # Stage 1: Data-Driven Analysis (no evidence)
            self.logger.info("Stage 1: Generating data-driven analysis...")
            stage1_report = self._execute_stage1_analysis(run_context)
            
            if not stage1_report:
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "Stage 1 analysis failed"},
                    error_message="Failed to generate data-driven analysis"
                )
            
            # Store Stage 1 report
            stage1_artifact = self._store_stage1_report(stage1_report)
            
            # Stage 2: Evidence Integration
            self.logger.info("Stage 2: Integrating curated evidence...")
            final_report = self._execute_stage2_integration(run_context, stage1_report)
            
            if not final_report:
                return AgentResult(
                    success=False,
                    artifacts=[stage1_artifact],
                    metadata={"agent_name": self.agent_name, "error": "Stage 2 integration failed"},
                    error_message="Failed to integrate evidence into report"
                )
            
            # Store final report with evidence
            final_artifact = self._store_final_report(final_report)
            
            # Create evidence appendix
            appendix_artifact = self._create_evidence_appendix(run_context, final_report)
            
            artifacts = [stage1_artifact, final_artifact]
            if appendix_artifact:
                artifacts.append(appendix_artifact)
            
            self.logger.info(f"Two-stage synthesis completed: {len(artifacts)} artifacts created")
            
            return AgentResult(
                success=True,
                artifacts=artifacts,
                metadata={
                    "agent_name": self.agent_name,
                    "stage1_model": self.stage1_model,
                    "stage2_model": self.stage2_model,
                    "synthesis_method": "two_stage_anti_hallucination",
                    "evidence_integration": True,
                    "appendix_created": appendix_artifact is not None
                }
            )
            
        except Exception as e:
            self.logger.error(f"TwoStageSynthesisAgent failed with exception: {e}")
            self.logger.error(f"Exception type: {type(e).__name__}")
            self.logger.error(f"Exception details: {str(e)}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            return AgentResult(
                success=False,
                artifacts=[],
                metadata={"agent_name": self.agent_name, "error": str(e), "error_type": type(e).__name__},
                error_message=f"Two-stage synthesis failed: {e}"
            )
    
    def _validate_inputs(self, run_context: RunContext) -> bool:
        """Strict contract enforcement: ALL required input assets must be present or fail hard."""
        
        self.logger.info("Starting _validate_inputs method")
        
        # Required Asset 1: Statistical analysis artifacts
        self.logger.info("Looking for statistical_analysis artifacts...")
        statistical_artifacts = self.storage.find_artifacts_by_metadata(artifact_type="statistical_analysis")
        self.logger.info(f"statistical_artifacts result: {statistical_artifacts}")
        
        # Defensive programming: Handle None return from storage
        if statistical_artifacts is None:
            self.logger.error("CRITICAL: find_artifacts_by_metadata returned None for statistical_analysis")
            return False
        
        if not statistical_artifacts:
            self.logger.error("CONTRACT VIOLATION: No statistical_analysis artifacts found via CAS discovery")
            return False
        self.logger.info(f"✓ Statistical analysis: Found {len(statistical_artifacts)} artifacts")
        
        # Required Asset 2: Curated evidence artifacts  
        evidence_artifacts = self.storage.find_artifacts_by_metadata(artifact_type="curated_evidence")
        
        # Defensive programming: Handle None return from storage
        if evidence_artifacts is None:
            self.logger.error("CRITICAL: find_artifacts_by_metadata returned None for curated_evidence")
            return False
        
        if not evidence_artifacts:
            self.logger.error("CONTRACT VIOLATION: No curated_evidence artifacts found via CAS discovery")
            return False
        self.logger.info(f"✓ Curated evidence: Found {len(evidence_artifacts)} artifacts")
        
        # Required Asset 3: Framework artifacts
        framework_artifacts = self.storage.find_artifacts_by_metadata(artifact_type="framework")
        
        # Defensive programming: Handle None return from storage
        if framework_artifacts is None:
            self.logger.error("CRITICAL: find_artifacts_by_metadata returned None for framework")
            return False
        
        if not framework_artifacts:
            self.logger.error("CONTRACT VIOLATION: No framework artifacts found via CAS discovery")
            return False
        self.logger.info(f"✓ Framework: Found {len(framework_artifacts)} artifacts")
        
        # Required Asset 4: Experiment spec artifacts
        experiment_artifacts = self.storage.find_artifacts_by_metadata(artifact_type="experiment_spec")
        
        # Defensive programming: Handle None return from storage
        if experiment_artifacts is None:
            self.logger.error("CRITICAL: find_artifacts_by_metadata returned None for experiment_spec")
            return False
        
        if not experiment_artifacts:
            self.logger.error("CONTRACT VIOLATION: No experiment_spec artifacts found via CAS discovery")
            return False
        self.logger.info(f"✓ Experiment spec: Found {len(experiment_artifacts)} artifacts")
        
        # Required Asset 5: Corpus manifest artifacts
        corpus_artifacts = self.storage.find_artifacts_by_metadata(artifact_type="corpus_manifest")
        
        # Defensive programming: Handle None return from storage
        if corpus_artifacts is None:
            self.logger.error("CRITICAL: find_artifacts_by_metadata returned None for corpus_manifest")
            return False
        
        if not corpus_artifacts:
            self.logger.error("CONTRACT VIOLATION: No corpus_manifest artifacts found via CAS discovery")
            return False
        self.logger.info(f"✓ Corpus manifest: Found {len(corpus_artifacts)} artifacts")
        
        self.logger.info("CONTRACT FULFILLED: All required input assets present - proceeding with synthesis")
        return True
    
    def _execute_stage1_analysis(self, run_context: RunContext) -> Optional[str]:
        """
        Execute Stage 1: Data-driven analysis without evidence quotes.
        
        Args:
            run_context: The RunContext containing statistical results
            
        Returns:
            Stage 1 report text or None if failed
        """
        try:
            self.logger.info("Starting Stage 1: Framework-driven data analysis")
            
            # Prepare the context for Stage 1 analysis
            self.logger.info("Preparing Stage 1 context...")
            stage1_context = self._prepare_stage1_context(run_context)
            self.logger.info(f"Stage 1 context prepared: {len(stage1_context)} keys")
            
            # Create the Stage 1 prompt with all necessary data
            self.logger.info("Creating Stage 1 prompt...")
            stage1_prompt = self._create_stage1_prompt(stage1_context)
            self.logger.info(f"Stage 1 prompt created: {len(stage1_prompt)} characters")
            
            # Execute Stage 1 analysis with Gemini Pro
            self.logger.info(f"Executing Stage 1 analysis with {self.stage1_model}")
            self.logger.info(f"Prompt length: {len(stage1_prompt)} characters")
            
            response_tuple = self.llm_gateway.execute_call(
                model=self.stage1_model,
                prompt=stage1_prompt,
                temperature=0.3  # Lower temperature for analytical consistency
            )
            
            self.logger.info(f"LLM call completed, response type: {type(response_tuple)}")
            if response_tuple:
                self.logger.info(f"Response length: {len(str(response_tuple))}")
            else:
                self.logger.error("LLM call returned None or empty response")
            
            # Extract content from tuple response
            response, metadata = response_tuple
            
            # Log LLM interaction with cost data
            if metadata and 'usage' in metadata:
                usage_data = metadata['usage']
                self.audit.log_llm_interaction(
                    model=self.stage1_model,
                    prompt=stage1_prompt,
                    response=response,
                    agent_name=self.agent_name,
                    interaction_type="stage1_analysis",
                    metadata={
                        "prompt_tokens": usage_data.get('prompt_tokens', 0),
                        "completion_tokens": usage_data.get('completion_tokens', 0),
                        "total_tokens": usage_data.get('total_tokens', 0),
                        "response_cost_usd": usage_data.get('response_cost_usd', 0.0),
                        "step": "stage1_analysis",
                        "temperature": 0.3
                    }
                )
            
            if not response or not response.strip():
                self.logger.error("Stage 1 analysis returned empty response")
                return None
            
            self.logger.info(f"Stage 1 analysis completed: {len(response)} characters")
            
            # Log successful execution
            self.audit.log_agent_event(
                self.agent_name, 
                "stage1_completed",
                {
                    "model_used": self.stage1_model,
                    "response_length": len(response),
                    "temperature": 0.3
                }
            )
            
            return response
            
        except Exception as e:
            self.logger.error(f"Stage 1 analysis failed: {e}")
            self.audit.log_agent_event(
                self.agent_name,
                "stage1_failed", 
                {"error": str(e)}
            )
            return None
    
    def _execute_stage2_integration(self, run_context: RunContext, stage1_report: str) -> Optional[str]:
        """
        Execute Stage 2: Evidence integration with curated quotes.
        
        Args:
            run_context: The RunContext containing curated evidence
            stage1_report: The Stage 1 report to enhance with evidence
            
        Returns:
            Final report with integrated evidence or None if failed
        """
        try:
            self.logger.info("Starting Stage 2: Evidence integration")
            
            # Load curated evidence from IntelligentEvidenceRetrievalAgent for Stage 2 integration
            # Contract validation ensures evidence exists, so this should never be empty
            raw_evidence = self._prepare_curated_evidence(run_context)
            
            # Get corpus manifest for document name mapping
            corpus_manifest_hash = run_context.metadata.get("corpus_manifest_hash")
            corpus_manifest = ""
            if corpus_manifest_hash:
                corpus_manifest = self.storage.get_artifact(corpus_manifest_hash).decode('utf-8')
            
            # Create the Stage 2 prompt with Stage 1 report, raw evidence, and corpus manifest (THIN: no parsing)
            stage2_prompt = self._create_stage2_prompt(stage1_report, raw_evidence, corpus_manifest)
            
            # Execute Stage 2 integration with Gemini Flash
            self.logger.info(f"Executing Stage 2 integration with {self.stage2_model}")
            
            response_tuple = self.llm_gateway.execute_call(
                model=self.stage2_model,
                prompt=stage2_prompt,
                temperature=0.2  # Lower temperature for precise integration
            )
            
            # Extract content from tuple response
            response, metadata = response_tuple
            
            # Log LLM interaction with cost data
            if metadata and 'usage' in metadata:
                usage_data = metadata['usage']
                self.audit.log_llm_interaction(
                    model=self.stage2_model,
                    prompt=stage2_prompt,
                    response=response,
                    agent_name=self.agent_name,
                    interaction_type="stage2_integration",
                    metadata={
                        "prompt_tokens": usage_data.get('prompt_tokens', 0),
                        "completion_tokens": usage_data.get('completion_tokens', 0),
                        "total_tokens": usage_data.get('total_tokens', 0),
                        "response_cost_usd": usage_data.get('response_cost_usd', 0.0),
                        "step": "stage2_integration",
                        "temperature": 0.2
                    }
                )
            
            if not response or not response.strip():
                self.logger.error("Stage 2 integration returned empty response")
                return stage1_report  # Fallback to Stage 1 report
            
            self.logger.info(f"Stage 2 integration completed: {len(response)} characters")
            
            # Log successful execution
            self.audit.log_agent_event(
                self.agent_name,
                "stage2_completed",
                {
                    "model_used": self.stage2_model,
                    "response_length": len(response),
                    "evidence_content_length": len(raw_evidence),
                    "temperature": 0.2
                }
            )
            
            return response
            
        except Exception as e:
            self.logger.error(f"Stage 2 integration failed: {e}")
            self.audit.log_agent_event(
                self.agent_name,
                "stage2_failed",
                {"error": str(e)}
            )
            # Return Stage 1 report as fallback
            return stage1_report
    
    def _store_stage1_report(self, report: str) -> str:
        """Store Stage 1 report as raw markdown content."""
        # Store the report directly without redundant YAML frontmatter
        # The report already contains the proper header from the Stage 1 prompt
        return self.storage.store_artifact(
            content=report,
            artifact_type="stage1_synthesis_report",
            experiment_id="stage1_analysis"
        )
    
    def _store_final_report(self, report: str) -> str:
        """Store final report as raw markdown content."""
        # Store the report directly without redundant YAML frontmatter
        # The report already contains the proper header from the Stage 1 prompt
        return self.storage.store_artifact(
            content=report,
            artifact_type="final_synthesis_report",
            experiment_id="final_report"
        )
    
    def _prepare_stage1_context(self, run_context: RunContext) -> Dict[str, Any]:
        """Prepare all necessary context data for Stage 1 analysis."""
        try:
            # CAS Discovery: Load framework content
            framework_artifacts = self.storage.find_artifacts_by_metadata(artifact_type="framework")
            if not framework_artifacts:
                raise ValueError("No framework artifacts found via CAS discovery")
            framework_content = self.storage.get_artifact(framework_artifacts[0]).decode('utf-8')
            
            # CAS Discovery: Load experiment content
            experiment_artifacts = self.storage.find_artifacts_by_metadata(artifact_type="experiment_spec")
            if experiment_artifacts:
                experiment_content = self.storage.get_artifact(experiment_artifacts[0]).decode('utf-8')
            else:
                experiment_content = ""
            
            # CAS Discovery: Load corpus manifest
            corpus_artifacts = self.storage.find_artifacts_by_metadata(artifact_type="corpus_manifest")
            if corpus_artifacts:
                corpus_manifest = self.storage.get_artifact(corpus_artifacts[0]).decode('utf-8')
            else:
                corpus_manifest = ""
            
            # Extract additional metadata for the prompt
            run_id = run_context.experiment_id
            completion_date = datetime.now(timezone.utc).isoformat()
            
            # Extract framework and corpus filenames from artifact metadata
            framework_metadata = self.storage.get_artifact_metadata(framework_artifacts[0])
            corpus_metadata = self.storage.get_artifact_metadata(corpus_artifacts[0]) if corpus_artifacts else {}
            
            framework_filename = framework_metadata.get("original_filename", "framework.md")
            corpus_filename = corpus_metadata.get("original_filename", "corpus.md")
            
            # Count corpus documents via CAS discovery
            corpus_document_artifacts = self.storage.find_artifacts_by_metadata(artifact_type="corpus_document")
            if corpus_document_artifacts is None:
                self.logger.error("CRITICAL: find_artifacts_by_metadata returned None for corpus_document")
                document_count = 0
            else:
                document_count = len(corpus_document_artifacts)
            
            return {
                "framework_content": framework_content,
                "experiment_content": experiment_content,
                "corpus_manifest": corpus_manifest,
                "statistical_results": {},  # Statistical results are read from artifacts
                "experiment_id": run_context.experiment_id,
                "run_id": run_id,
                "completion_date": completion_date,
                "framework_filename": framework_filename,
                "corpus_filename": corpus_filename,
                "document_count": document_count,
                "run_context": run_context  # Add run_context so _read_statistical_artifacts can access it
            }
            
        except Exception as e:
            self.logger.error(f"Failed to prepare Stage 1 context: {e}")
            return {}
    
    def _create_stage1_prompt(self, context: Dict[str, Any]) -> str:
        """Create the complete Stage 1 prompt with all context data."""
        
        # Read statistical results directly from artifacts
        statistical_summary = self._read_statistical_artifacts(context.get("run_context"))
        
        # Generate dynamic models used summary
        models_summary = self._generate_models_summary(context.get("run_context"))
        
        # Create the complete prompt by combining template with context
        # Replace template variables in the prompt
        prompt = self.stage1_prompt.replace('[experiment_name]', context.get('experiment_id', 'Unknown'))
        prompt = prompt.replace('[completion_date]', context.get('completion_date', 'Unknown'))
        # Extract framework name from framework content
        framework_content = context.get('framework_content', '')
        framework_name = 'Unknown Framework'
        if framework_content:
            # Try to extract framework name from the first line or title
            lines = framework_content.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('# '):
                    framework_name = line[2:].strip()
                    break
        prompt = prompt.replace('[Use the actual framework name from the framework content]', framework_name)
        prompt = prompt.replace('[corpus_filename]', context.get('corpus_filename', 'Unknown'))
        prompt = prompt.replace('[document_count]', str(context.get('document_count', 'Unknown')))
        prompt = prompt.replace('[models_used_summary]', models_summary)
        
        # Add the context data
        prompt += f"""

**FRAMEWORK SPECIFICATION:**
{context.get('framework_content', 'Framework content not available')}

**EXPERIMENT CONFIGURATION:**
{context.get('experiment_content', 'Experiment content not available')}

**CORPUS MANIFEST:**
{context.get('corpus_manifest', 'Corpus manifest not available')}

**STATISTICAL ANALYSIS RESULTS:**
{statistical_summary}

**EXPERIMENT METADATA:**
Experiment ID: {context.get('experiment_id', 'Unknown')}
Analysis Completed: {context.get('metadata', {}).get('analysis_completed', 'Unknown')}
Models Used: {models_summary}

Please generate a comprehensive framework-driven analysis report following the Stage 1 protocol outlined above."""

        return prompt
    
    def _generate_models_summary(self, run_context: RunContext) -> str:
        """Generate a dynamic summary of models used across all pipeline stages."""
        try:
            # Get models from audit logs
            models_used = set()
            
            # Check audit logs for model usage
            if hasattr(self.audit, 'get_agent_events'):
                events = self.audit.get_agent_events()
                for event in events:
                    if 'model_used' in event.get('metadata', {}):
                        model = event['metadata']['model_used']
                        if model and model != 'Unknown':
                            models_used.add(model)
            
            # Add current synthesis models
            models_used.add(self.stage1_model)
            models_used.add(self.stage2_model)
            
            if models_used:
                # Format as readable list
                model_list = sorted(list(models_used))
                if len(model_list) == 1:
                    return model_list[0]
                elif len(model_list) == 2:
                    return f"{model_list[0]}, {model_list[1]}"
                else:
                    return f"{', '.join(model_list[:-1])}, and {model_list[-1]}"
            else:
                return f"Analysis: {self.stage1_model}, Synthesis: {self.stage2_model}"
                
        except Exception as e:
            self.logger.warning(f"Could not generate dynamic models summary: {e}")
            return f"Analysis: {self.stage1_model}, Synthesis: {self.stage2_model}"
    
    def _read_statistical_artifacts(self, run_context: RunContext) -> str:
        """
        CAS-native discovery of both baseline statistics and statistical analysis artifacts.
        THIN: No parsing, just raw data shuttle to LLM.
        
        Three-tier architecture integration:
        - Tier 1: baseline_statistics (pandas-computed foundational stats)
        - Tier 2: statistical_analysis (LLM experiment-specific analysis)
        - Tier 3: synthesis (this agent combines both for comprehensive reporting)
        """
        try:
            self.logger.info("Starting _read_statistical_artifacts...")
            all_statistical_content = []
            
            # CAS discovery: Find baseline_statistics artifacts (Tier 1)
            baseline_artifacts = self.storage.find_artifacts_by_metadata(
                artifact_type="baseline_statistics"
            )
            
            if baseline_artifacts:
                self.logger.info(f"Found {len(baseline_artifacts)} baseline statistics artifacts via CAS discovery")
                
                for artifact_hash in baseline_artifacts:
                    try:
                        artifact_bytes = self.storage.get_artifact(artifact_hash)
                        if artifact_bytes:
                            raw_content = artifact_bytes.decode('utf-8')
                            # Label baseline statistics for LLM context
                            labeled_content = f"=== BASELINE STATISTICS (TIER 1 - PANDAS COMPUTED) ===\n{raw_content}"
                            all_statistical_content.append(labeled_content)
                    except Exception as e:
                        self.logger.warning(f"Failed to load baseline statistics artifact {artifact_hash}: {e}")
                        continue
            else:
                self.logger.warning("No baseline_statistics artifacts found - synthesis may lack foundational data")
            
            # CAS discovery: Find statistical_analysis artifacts (Tier 2)
            statistical_artifacts = self.storage.find_artifacts_by_metadata(
                artifact_type="statistical_analysis"
            )
            
            if not statistical_artifacts:
                # Contract validation should prevent this from happening
                raise RuntimeError("No statistical_analysis artifacts found via CAS discovery - contract violation")
            
            self.logger.info(f"Found {len(statistical_artifacts)} statistical analysis artifacts via CAS discovery")
            
            for artifact_hash in statistical_artifacts:
                try:
                    artifact_bytes = self.storage.get_artifact(artifact_hash)
                    if artifact_bytes:
                        raw_content = artifact_bytes.decode('utf-8')
                        # Label statistical analysis for LLM context
                        labeled_content = f"=== STATISTICAL ANALYSIS (TIER 2 - LLM EXPERIMENT-SPECIFIC) ===\n{raw_content}"
                        all_statistical_content.append(labeled_content)
                except Exception as e:
                    self.logger.warning(f"Failed to load statistical analysis artifact {artifact_hash}: {e}")
                    continue
            
            if all_statistical_content:
                # Join all statistical artifacts with clear separators
                return "\n\n=== STATISTICAL ARTIFACT SEPARATOR ===\n\n".join(all_statistical_content)
            else:
                return "No statistical content found"
                
        except Exception as e:
            self.logger.error(f"Failed to discover statistical artifacts via CAS: {e}")
            return f"Error discovering statistical artifacts: {str(e)}"
    
    def _load_raw_evidence_artifacts(self, run_context: RunContext) -> str:
        """
        CAS-native discovery of curated evidence artifacts from Evidence Agent.
        THIN: No parsing, just raw data shuttle to LLM.
        Scalability: Uses curated evidence, not raw evidence extraction.
        """
        try:
            # CAS discovery: Find curated_evidence artifacts (from Evidence Agent, not Analysis Agent)
            evidence_artifacts = self.storage.find_artifacts_by_metadata(
                artifact_type="curated_evidence"
            )
            
            if not evidence_artifacts:
                # Contract validation should prevent this from happening
                raise RuntimeError("No curated_evidence artifacts found via CAS discovery - contract violation")
            
            self.logger.info(f"Found {len(evidence_artifacts)} evidence artifacts via CAS discovery")
            
            # THIN: Collect raw artifact content without parsing
            raw_evidence_content = []
            
            for artifact_hash in evidence_artifacts:
                try:
                    # Load raw artifact bytes
                    artifact_bytes = self.storage.get_artifact(artifact_hash)
                    if artifact_bytes:
                        # THIN: Just decode to string, no JSON parsing
                        raw_content = artifact_bytes.decode('utf-8')
                        raw_evidence_content.append(raw_content)
                        
                except Exception as e:
                    self.logger.warning(f"Failed to load evidence artifact {artifact_hash}: {e}")
                    continue
            
            if raw_evidence_content:
                # Join raw artifacts with separators for LLM processing
                return "\n\n=== EVIDENCE ARTIFACT SEPARATOR ===\n\n".join(raw_evidence_content)
            else:
                return "No evidence extraction content found"
                
        except Exception as e:
            self.logger.error(f"Failed to load raw evidence artifacts: {e}")
            return ""
    
    def _prepare_curated_evidence(self, run_context: RunContext) -> str:
        """Prepare raw curated evidence from IntelligentEvidenceRetrievalAgent artifacts via CAS discovery (THIN: no parsing)."""
        try:
            raw_evidence_content = []
            
            # CAS Discovery: Find curated evidence artifacts
            evidence_artifacts = self.storage.find_artifacts_by_metadata(artifact_type="curated_evidence")
            
            for artifact_hash in evidence_artifacts:
                try:
                    # Load the artifact
                    artifact_bytes = self.storage.get_artifact(artifact_hash)
                    artifact_data = json.loads(artifact_bytes.decode('utf-8'))
                    
                    # Check if this is a curated evidence artifact from IntelligentEvidenceRetrievalAgent
                    if (isinstance(artifact_data, dict) and 
                        artifact_data.get('agent_name') == 'IntelligentEvidenceRetrievalAgent' and
                        'curated_evidence' in artifact_data):
                        
                        # THIN: Get raw curation response without parsing
                        evidence_content = artifact_data.get('curated_evidence', {})
                        if isinstance(evidence_content, dict) and 'raw_curation_response' in evidence_content:
                            raw_response = evidence_content.get('raw_curation_response', '')
                            if raw_response:
                                raw_evidence_content.append(raw_response)
                                
                except Exception as e:
                    self.logger.warning(f"Failed to load evidence artifact {artifact_hash}: {e}")
                    continue
            
            # Join all raw evidence content
            combined_evidence = "\n\n--- EVIDENCE CURATION ---\n\n".join(raw_evidence_content)
            self.logger.info(f"Prepared raw curated evidence content ({len(combined_evidence)} characters)")
            return combined_evidence
            
        except Exception as e:
            self.logger.error(f"Failed to prepare curated evidence: {e}")
            return ""
    
    def _create_stage2_prompt(self, stage1_report: str, raw_evidence: str, corpus_manifest: str = "") -> str:
        """Create the complete Stage 2 prompt with Stage 1 report, raw evidence, and corpus manifest (THIN: no parsing)."""
        
        # Create the complete Stage 2 prompt with raw evidence and corpus manifest
        prompt = f"""{self.stage2_prompt}

**STAGE 1 REPORT TO ENHANCE:**
{stage1_report}

**RAW EVIDENCE FOR CURATION AND INTEGRATION:**
{raw_evidence if raw_evidence else "No evidence available"}

**CORPUS MANIFEST FOR DOCUMENT NAME MAPPING:**
{corpus_manifest if corpus_manifest else "No corpus manifest available"}

Please enhance the Stage 1 report by strategically integrating the curated evidence quotes throughout the document, following the Stage 2 protocol outlined above. Use the corpus manifest to map document indices (Document 1, Document 2, etc.) to actual document names. Preserve all analytical claims and conclusions from Stage 1 while bringing them to life with supporting evidence."""

        return prompt
    
    
    def _create_evidence_appendix(self, run_context: RunContext, final_report: str) -> Optional[str]:
        """Create evidence appendix with raw curated evidence (THIN: no parsing)."""
        try:
            self.logger.info("Creating evidence appendix")
            
            # Get raw curated evidence (THIN: no parsing)
            raw_curated_evidence = self._prepare_curated_evidence(run_context)
            
            if not raw_curated_evidence:
                self.logger.info("No curated evidence for appendix")
                return None
            
            # Create markdown content with metadata header
            timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
            markdown_content = f"""---
agent_name: {self.agent_name}
stage: evidence_appendix
timestamp: {timestamp}
evidence_content_length: {len(raw_curated_evidence)}
synthesis_method: two_stage_with_appendix
---

{raw_curated_evidence}"""
            
            # Store as markdown content
            content_bytes = markdown_content.encode('utf-8')
            appendix_hash = self.storage.put_artifact(
                content_bytes,
                {"artifact_type": "evidence_appendix", "experiment_id": "evidence_appendix"}
            )
            
            self.logger.info(f"Evidence appendix created with raw content ({len(raw_curated_evidence)} characters)")
            return appendix_hash
            
        except Exception as e:
            self.logger.error(f"Failed to create evidence appendix: {e}")
            return None
    
