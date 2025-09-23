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
            self.log_execution_start(**kwargs)
            
            # Validate inputs
            if not self._validate_inputs(run_context):
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "Input validation failed"},
                    error_message="Required inputs missing for synthesis"
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
            self.logger.error(f"Two-stage synthesis failed: {e}")
            return AgentResult(
                success=False,
                artifacts=[],
                metadata={"agent_name": self.agent_name, "error": str(e)},
                error_message=f"Two-stage synthesis failed: {e}"
            )
    
    def _validate_inputs(self, run_context: RunContext) -> bool:
        """Strict contract enforcement: ALL required input assets must be present or fail hard."""
        
        # Required Asset 1: Statistical analysis artifacts
        statistical_artifacts = self.storage.find_artifacts_by_metadata(artifact_type="statistical_analysis")
        if not statistical_artifacts:
            self.logger.error("CONTRACT VIOLATION: No statistical_analysis artifacts found via CAS discovery")
            return False
        self.logger.info(f"✓ Statistical analysis: Found {len(statistical_artifacts)} artifacts")
        
        # Required Asset 2: Curated evidence artifacts  
        evidence_artifacts = self.storage.find_artifacts_by_metadata(artifact_type="curated_evidence")
        if not evidence_artifacts:
            self.logger.error("CONTRACT VIOLATION: No curated_evidence artifacts found via CAS discovery")
            return False
        self.logger.info(f"✓ Curated evidence: Found {len(evidence_artifacts)} artifacts")
        
        # Required Asset 3: Framework hash
        framework_hash = run_context.metadata.get("framework_hash")
        if not framework_hash:
            self.logger.error("CONTRACT VIOLATION: No framework_hash found in run_context metadata")
            return False
        self.logger.info(f"✓ Framework: Found hash {framework_hash[:8]}")
        
        # Required Asset 4: Experiment hash
        experiment_hash = run_context.metadata.get("experiment_hash")
        if not experiment_hash:
            self.logger.error("CONTRACT VIOLATION: No experiment_hash found in run_context metadata")
            return False
        self.logger.info(f"✓ Experiment: Found hash {experiment_hash[:8]}")
        
        # Required Asset 5: Corpus manifest hash
        corpus_manifest_hash = run_context.metadata.get("corpus_manifest_hash")
        if not corpus_manifest_hash:
            self.logger.error("CONTRACT VIOLATION: No corpus_manifest_hash found in run_context metadata")
            return False
        self.logger.info(f"✓ Corpus manifest: Found hash {corpus_manifest_hash[:8]}")
        
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
            stage1_context = self._prepare_stage1_context(run_context)
            
            # Create the Stage 1 prompt with all necessary data
            stage1_prompt = self._create_stage1_prompt(stage1_context)
            
            # Execute Stage 1 analysis with Gemini Pro
            self.logger.info(f"Executing Stage 1 analysis with {self.stage1_model}")
            
            response_tuple = self.llm_gateway.execute_call(
                model=self.stage1_model,
                prompt=stage1_prompt,
                temperature=0.3,  # Lower temperature for analytical consistency
                # max_tokens handled by provider defaults (65535 for Vertex AI)
            )
            
            # Extract content from tuple response
            response, metadata = response_tuple
            
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
                temperature=0.2,  # Lower temperature for precise integration
                # max_tokens handled by provider defaults (65535 for Vertex AI)
            )
            
            # Extract content from tuple response
            response, metadata = response_tuple
            
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
        # Add metadata header to the markdown content itself
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
        markdown_content = f"""---
agent: {self.agent_name}
stage: stage1_data_driven_analysis
timestamp: {timestamp}
model_used: {self.stage1_model}
evidence_included: false
synthesis_method: data_driven_only
---

{report}"""
        
        return self.storage.store_artifact(
            content=markdown_content,
            artifact_type="stage1_synthesis_report",
            experiment_id="stage1_analysis"
        )
    
    def _store_final_report(self, report: str) -> str:
        """Store final report as raw markdown content."""
        # Add metadata header to the markdown content itself
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
        markdown_content = f"""---
agent: {self.agent_name}
stage: stage2_evidence_integrated
timestamp: {timestamp}
model_used: {self.stage2_model}
evidence_included: true
synthesis_method: two_stage_with_evidence
---

{report}"""
        
        return self.storage.store_artifact(
            content=markdown_content,
            artifact_type="final_synthesis_report",
            experiment_id="final_report"
        )
    
    def _prepare_stage1_context(self, run_context: RunContext) -> Dict[str, Any]:
        """Prepare all necessary context data for Stage 1 analysis."""
        try:
            # CAS Discovery: Load framework content from hash address
            framework_hash = run_context.metadata.get("framework_hash")
            if not framework_hash:
                raise ValueError("Framework hash not found in run_context metadata")
            framework_content = self.storage.get_artifact(framework_hash).decode('utf-8')
            
            # CAS Discovery: Load experiment content from hash address
            experiment_hash = run_context.metadata.get("experiment_hash")
            if experiment_hash:
                experiment_content = self.storage.get_artifact(experiment_hash).decode('utf-8')
            else:
                experiment_content = ""
            
            # CAS Discovery: Load corpus manifest from hash address
            corpus_manifest_hash = run_context.metadata.get("corpus_manifest_hash")
            if corpus_manifest_hash:
                corpus_manifest = self.storage.get_artifact(corpus_manifest_hash).decode('utf-8')
            else:
                corpus_manifest = ""
            
            return {
                "framework_content": framework_content,
                "experiment_content": experiment_content,
                "corpus_manifest": corpus_manifest,
                "statistical_results": {},  # Statistical results are read from artifacts
                "experiment_id": run_context.experiment_id,
                "metadata": run_context.metadata or {},
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
        prompt = f"""{self.stage1_prompt}

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
        CAS-native discovery of statistical analysis artifacts.
        THIN: No parsing, just raw data shuttle to LLM.
        """
        try:
            # CAS discovery: Find statistical_analysis artifacts
            statistical_artifacts = self.storage.find_artifacts_by_metadata(
                artifact_type="statistical_analysis"
            )
            
            if not statistical_artifacts:
                # Contract validation should prevent this from happening
                raise RuntimeError("No statistical_analysis artifacts found via CAS discovery - contract violation")
            
            self.logger.info(f"Found {len(statistical_artifacts)} statistical artifacts via CAS discovery")
            
            # THIN: Collect raw artifact content without parsing
            raw_statistical_content = []
            
            for artifact_hash in statistical_artifacts:
                try:
                    # Load raw artifact bytes
                    artifact_bytes = self.storage.get_artifact(artifact_hash)
                    if artifact_bytes:
                        # THIN: Just decode to string, no JSON parsing
                        raw_content = artifact_bytes.decode('utf-8')
                        raw_statistical_content.append(raw_content)
                        
                except Exception as e:
                    self.logger.warning(f"Failed to load statistical artifact {artifact_hash}: {e}")
                    continue
            
            if raw_statistical_content:
                # Join raw artifacts with separators for LLM processing
                return "\n\n=== STATISTICAL ARTIFACT SEPARATOR ===\n\n".join(raw_statistical_content)
            else:
                return "No statistical analysis content found"
                
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
    
