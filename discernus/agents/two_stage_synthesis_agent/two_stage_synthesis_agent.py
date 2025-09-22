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
        """Validate that required inputs are available for synthesis."""
        # Trust upstream agents - just check existence, not content quality
        if not hasattr(run_context, 'statistical_artifacts') or not run_context.statistical_artifacts:
            self.logger.error("No statistical artifacts found in run_context")
            return False
        
        if not run_context.experiment_id:
            self.logger.error("No experiment_id found in run_context")
            return False
        
        if not run_context.framework_path:
            self.logger.error("No framework_path found in run_context")
            return False
        
        self.logger.info("Input validation passed: statistical results, experiment metadata, and framework available")
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
                max_tokens=8000   # Sufficient for comprehensive analysis
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
            
            # Load raw evidence extraction artifacts for Stage 2 curation and integration
            raw_evidence = self._load_raw_evidence_artifacts(run_context)
            
            if not raw_evidence:
                self.logger.warning("No curated evidence found - generating Stage 2 report with explanatory note")
                
                # Create a Stage 2 report that explicitly states no evidence was integrated
                timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
                no_evidence_report = f"""---
agent: {self.agent_name}
stage: stage2_no_evidence_integrated
timestamp: {timestamp}
model_used: {self.stage2_model}
evidence_included: false
synthesis_method: two_stage_fallback
---

# Research Synthesis Report

**Note on Evidence Integration:** No curated evidence was provided for this synthesis run. The following analysis is the complete data-driven report from Stage 1. No textual evidence has been integrated into this version of the report.

---

{stage1_report}
"""
                return no_evidence_report
            
            # Create the Stage 2 prompt with Stage 1 report and raw evidence (THIN: no parsing)
            stage2_prompt = self._create_stage2_prompt(stage1_report, raw_evidence)
            
            # Execute Stage 2 integration with Gemini Flash
            self.logger.info(f"Executing Stage 2 integration with {self.stage2_model}")
            
            response_tuple = self.llm_gateway.execute_call(
                model=self.stage2_model,
                prompt=stage2_prompt,
                temperature=0.2,  # Lower temperature for precise integration
                max_tokens=10000  # More tokens for enhanced report
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
        """Store Stage 1 report as artifact."""
        artifact_data = {
            "agent_name": self.agent_name,
            "stage": "stage1_data_driven_analysis",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model_used": self.stage1_model,
            "report_content": report,
            "evidence_included": False,
            "synthesis_method": "data_driven_only"
        }
        
        return self.storage.store_artifact(
            content=artifact_data,
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
            # Load framework content
            framework_content = ""
            if run_context.framework_path:
                framework_path = Path(run_context.framework_path)
                if framework_path.exists():
                    framework_content = framework_path.read_text(encoding='utf-8')
            
            # Load experiment content
            experiment_content = ""
            experiment_path = Path(run_context.experiment_id) / "experiment.md"
            if experiment_path.exists():
                experiment_content = experiment_path.read_text(encoding='utf-8')
            
            # Load corpus manifest
            corpus_manifest = ""
            if run_context.corpus_path:
                corpus_path = Path(run_context.corpus_path)
                if corpus_path.exists():
                    corpus_manifest = corpus_path.read_text(encoding='utf-8')
            
            return {
                "framework_content": framework_content,
                "experiment_content": experiment_content,
                "corpus_manifest": corpus_manifest,
                "statistical_results": run_context.statistical_results or {},
                "experiment_id": run_context.experiment_id,
                "metadata": run_context.metadata or {}
            }
            
        except Exception as e:
            self.logger.error(f"Failed to prepare Stage 1 context: {e}")
            return {}
    
    def _create_stage1_prompt(self, context: Dict[str, Any]) -> str:
        """Create the complete Stage 1 prompt with all context data."""
        
        # Read statistical results directly from artifacts
        statistical_summary = self._read_statistical_artifacts(context.get("run_context"))
        
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

Please generate a comprehensive framework-driven analysis report following the Stage 1 protocol outlined above."""

        return prompt
    
    def _read_statistical_artifacts(self, run_context: RunContext) -> str:
        """Read statistical analysis artifacts directly from storage."""
        if not run_context or not hasattr(run_context, 'statistical_artifacts'):
            return "No statistical artifacts available"
        
        try:
            statistical_content = []
            
            for artifact_hash in run_context.statistical_artifacts:
                try:
                    # Read artifact directly from storage
                    artifact_bytes = self.storage.get_artifact(artifact_hash)
                    if artifact_bytes:
                        artifact_data = json.loads(artifact_bytes.decode('utf-8'))
                        
                        # Extract the statistical analysis content
                        if 'statistical_analysis_content' in artifact_data:
                            statistical_content.append(artifact_data['statistical_analysis_content'])
                        
                except Exception as e:
                    self.logger.warning(f"Failed to read statistical artifact {artifact_hash}: {e}")
                    continue
            
            if statistical_content:
                return "\n\n---\n\n".join(statistical_content)
            else:
                return "No statistical analysis content found in artifacts"
                
        except Exception as e:
            self.logger.error(f"Failed to read statistical artifacts: {e}")
            return f"Error reading statistical artifacts: {str(e)}"
    
    def _load_raw_evidence_artifacts(self, run_context: RunContext) -> str:
        """Load ALL raw evidence extraction artifacts from analysis phase (THIN: direct from disk)."""
        try:
            raw_evidence_quotes = []
            
            # Look for evidence extraction artifacts from analysis phase
            if hasattr(run_context, 'analysis_artifacts') and run_context.analysis_artifacts:
                for artifact_hash in run_context.analysis_artifacts:
                    try:
                        # Load the artifact
                        artifact_bytes = self.storage.get_artifact(artifact_hash)
                        artifact_data = json.loads(artifact_bytes.decode('utf-8'))
                        
                        # Check if this is an evidence extraction artifact
                        if (isinstance(artifact_data, dict) and 
                            artifact_data.get('step') == 'evidence_extraction' and
                            'evidence_extraction' in artifact_data):
                            
                            # Extract the raw evidence content
                            evidence_content = artifact_data.get('evidence_extraction', '')
                            if evidence_content:
                                # Parse the JSON array from the evidence extraction
                                import re
                                json_match = re.search(r'```json\n(.*?)```', evidence_content, re.DOTALL)
                                if json_match:
                                    try:
                                        quotes = json.loads(json_match.group(1))
                                        if isinstance(quotes, list):
                                            for quote in quotes:
                                                raw_evidence_quotes.append({
                                                    'text': quote,
                                                    'document_index': artifact_data.get('document_index'),
                                                    'source_artifact': artifact_hash[:8]
                                                })
                                    except json.JSONDecodeError:
                                        self.logger.warning(f"Failed to parse evidence JSON from artifact {artifact_hash[:8]}")
                                        
                    except Exception as e:
                        self.logger.warning(f"Failed to load evidence artifact {artifact_hash[:8]}: {e}")
                        continue
            
            # Format all evidence for Stage 2 prompt
            if raw_evidence_quotes:
                evidence_text = "RAW EVIDENCE QUOTES FROM ANALYSIS PHASE:\n\n"
                for i, quote in enumerate(raw_evidence_quotes, 1):
                    evidence_text += f"{i}. Document {quote['document_index']}: \"{quote['text']}\"\n"
                    evidence_text += f"   (Source: {quote['source_artifact']})\n\n"
                
                self.logger.info(f"Loaded {len(raw_evidence_quotes)} raw evidence quotes for Stage 2 curation")
                return evidence_text
            else:
                self.logger.warning("No evidence extraction artifacts found in analysis phase")
                return ""
                
        except Exception as e:
            self.logger.error(f"Failed to load raw evidence artifacts: {e}")
            return ""
    
    def _prepare_curated_evidence(self, run_context: RunContext) -> str:
        """Prepare raw curated evidence from IntelligentEvidenceRetrievalAgent artifacts (THIN: no parsing)."""
        try:
            raw_evidence_content = []
            
            # Look for curated evidence artifacts from IntelligentEvidenceRetrievalAgent
            if hasattr(run_context, 'evidence_artifacts') and run_context.evidence_artifacts:
                for artifact_hash in run_context.evidence_artifacts:
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
    
    def _create_stage2_prompt(self, stage1_report: str, raw_evidence: str) -> str:
        """Create the complete Stage 2 prompt with Stage 1 report and raw evidence (THIN: no parsing)."""
        
        # Create the complete Stage 2 prompt with raw evidence
        prompt = f"""{self.stage2_prompt}

**STAGE 1 REPORT TO ENHANCE:**
{stage1_report}

**RAW EVIDENCE FOR CURATION AND INTEGRATION:**
{raw_evidence if raw_evidence else "No evidence available"}

Please enhance the Stage 1 report by strategically integrating the curated evidence quotes throughout the document, following the Stage 2 protocol outlined above. Preserve all analytical claims and conclusions from Stage 1 while bringing them to life with supporting evidence."""

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
            
            # Store raw evidence as appendix (THIN: no formatting/parsing)
            artifact_data = {
                "agent_name": self.agent_name,
                "stage": "evidence_appendix",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "raw_evidence_content": raw_curated_evidence,
                "evidence_content_length": len(raw_curated_evidence),
                "synthesis_method": "two_stage_with_appendix"
            }
            
            appendix_hash = self.storage.store_artifact(
                content=artifact_data,
                artifact_type="evidence_appendix",
                experiment_id="evidence_appendix"
            )
            
            self.logger.info(f"Evidence appendix created with raw content ({len(raw_curated_evidence)} characters)")
            return appendix_hash
            
        except Exception as e:
            self.logger.error(f"Failed to create evidence appendix: {e}")
            return None
    
