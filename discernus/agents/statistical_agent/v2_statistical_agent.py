#!/usr/bin/env python3
"""
V2 Statistical Agent - Atomic Processing Implementation
=====================================================

This agent processes atomic score and derived metrics artifacts from the AnalysisAgent
and performs comprehensive statistical analysis.

THIN Principles:
- Each document's scores are processed individually
- LLM handles all statistical intelligence
- Agent only adapts interfaces, no business logic
- Atomic artifacts for downstream consumption
"""

import json
import logging
import yaml
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.agent_result import AgentResult
from discernus.core.run_context import RunContext
from discernus.core.standard_agent import StandardAgent
from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway
from discernus.gateway.model_registry import get_model_registry


class V2StatisticalAgent(StandardAgent):
    """
    V2 Statistical Agent for atomic processing of score artifacts.
    
    This agent processes individual score and derived metrics artifacts
    from the AnalysisAgent and performs comprehensive statistical analysis.
    """
    
    def __init__(self, 
                 security: ExperimentSecurityBoundary,
                 storage: LocalArtifactStorage,
                 audit: AuditLogger):
        """
        Initialize the V2 Statistical Agent.
        
        Args:
            security: Security boundary for file operations
            storage: Content-addressable artifact storage
            audit: Audit logger for comprehensive event tracking
        """
        super().__init__(security, storage, audit)
        self.agent_name = "V2StatisticalAgent"
        self.logger = logging.getLogger(__name__)
        
        # Initialize LLM gateway
        self.gateway = EnhancedLLMGateway(get_model_registry())
        
        self.logger.info(f"Initialized {self.agent_name}")
    
    def _load_prompt_template(self) -> str:
        """Load the statistical analysis prompt template from YAML file."""
        prompt_path = Path(__file__).parent / "prompt.yaml"
        if not prompt_path.exists():
            error_msg = f"StatisticalAgent prompt file not found at {prompt_path}"
            self.audit.log_agent_event(self.agent_name, "prompt_error", {"error": error_msg})
            raise FileNotFoundError(error_msg)
        
        with open(prompt_path, 'r') as f:
            yaml_content = f.read()
        prompt_data = yaml.safe_load(yaml_content)
        return prompt_data['template']
    
    def get_capabilities(self) -> Dict[str, Any]:
        """
        Get agent capabilities and metadata.
        
        Returns:
            Dictionary describing agent capabilities
        """
        return {
            "agent_name": self.agent_name,
            "agent_type": "V2StatisticalAgent",
            "capabilities": [
                "statistical_analysis",
                "atomic_score_processing"
            ],
            "input_types": ["score_extraction_artifacts", "derived_metrics_artifacts"],
            "output_types": ["statistical_analysis"],
            "models_used": ["vertex_ai/gemini-2.5-pro", "vertex_ai/gemini-2.5-flash-lite"]
        }
    
    def execute(self, run_context: RunContext) -> AgentResult:
        """
        Execute statistical analysis on atomic score artifacts.
        
        Args:
            run_context: Run context containing analysis artifacts and metadata
            
        Returns:
            AgentResult with statistical analysis artifacts
        """
        try:
            # CAS Discovery approach - corpus documents loaded by orchestrator
            
            # Store run context for access in other methods
            self._current_run_context = {
                'experiment_id': run_context.experiment_id,
                'metadata': run_context.metadata
            }
            
            self.logger.info("Starting V2 Statistical Agent execution")
            self.audit.log_agent_event(self.agent_name, "execution_started", {
                "run_context_type": type(run_context).__name__
            })
            
            # Validate run context
            if not run_context:
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "run_context is required"},
                    error_message="run_context is required"
                )
            
            # REMOVED: Framework file reading - now handled by CAS discovery in _step1_statistical_analysis
            
            # CAS-native discovery: Find score_extraction artifacts
            score_artifacts = self.storage.find_artifacts_by_metadata(artifact_type="score_extraction")
            self.logger.info(f"Discovered {len(score_artifacts)} score_extraction artifacts via CAS")
            
            # Contract validation: Check expected count using CAS-discovered corpus documents
            corpus_document_hashes = run_context.metadata.get("corpus_document_hashes", [])
            expected_count = len(corpus_document_hashes)
            if len(score_artifacts) != expected_count:
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "contract_violation"},
                    error_message=f"Contract violation: Expected {expected_count} score_extraction artifacts for {expected_count} corpus documents, found {len(score_artifacts)}"
                )
            
            # Process atomic score artifacts
            raw_artifacts = self._collect_atomic_scores(score_artifacts)
            if not raw_artifacts:
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "no artifacts found"},
                    error_message="No artifacts found in analysis artifacts"
                )
            
            # Generate batch ID
            batch_id = f"stats_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
            
            # Step 1: Statistical Analysis with CAS discovery
            statistical_analysis_content = self._step1_statistical_analysis(raw_artifacts, batch_id)
            if not statistical_analysis_content:
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={"agent_name": self.agent_name, "error": "statistical analysis failed"},
                    error_message="Statistical analysis failed"
                )
            
            # THIN: Store raw LLM response directly, no parsing
            statistical_artifact_data = {
                "analysis_id": f"stats_{batch_id}",
                "step": "statistical_analysis",
                "model_used": "vertex_ai/gemini-2.5-pro",
                "statistical_analysis": statistical_analysis_content.strip(),  # Ensure leading/trailing whitespace is removed
                "documents_processed": len(raw_artifacts),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            statistical_content_bytes = json.dumps(statistical_artifact_data, indent=2).encode('utf-8')
            statistical_artifact_hash = self.storage.put_artifact(
                statistical_content_bytes,
                {"artifact_type": "statistical_analysis", "batch_id": batch_id}
            )
            # REMOVED: run_context.statistical_artifacts - replaced with CAS discovery
            run_context.statistical_results = statistical_analysis_content.strip()  # THIN: Raw LLM response
            
            
            # Create artifacts list with proper hashes
            artifacts = [
                {
                    "type": "statistical_analysis",
                    "content": statistical_artifact_data,
                    "metadata": {
                        "artifact_type": "statistical_analysis",
                        "phase": "statistical",
                        "batch_id": batch_id,
                        "timestamp": datetime.now().isoformat(),
                        "agent_name": self.agent_name,
                        "artifact_hash": statistical_artifact_hash
                    }
                }
            ]
            
            self.audit.log_agent_event(self.agent_name, "execution_completed", {
                "batch_id": batch_id,
                "artifacts_created": len(artifacts),
                "documents_processed": len(raw_artifacts)
            })
            
            return AgentResult(
                success=True,
                artifacts=artifacts,
                metadata={
                    "agent_name": self.agent_name,
                    "batch_id": batch_id,
                    "documents_processed": len(raw_artifacts),
                    "artifacts_created": len(artifacts)
                }
            )
            
        except Exception as e:
            self.logger.error(f"V2StatisticalAgent execution failed: {e}")
            self.audit.log_agent_event(self.agent_name, "execution_failed", {
                "error": str(e)
            })
            return AgentResult(
                success=False,
                artifacts=[],
                metadata={"agent_name": self.agent_name, "error": str(e)},
                error_message=f"V2StatisticalAgent execution failed: {str(e)}"
            )
    
    def _collect_atomic_scores(self, score_artifacts: List[str]) -> List[str]:
        """
        Collect raw score_extraction artifacts for LLM processing.
        THIN: No parsing, no validation - just raw data shuttle.
        
        Args:
            score_artifacts: List of score_extraction artifact hashes from CAS discovery
            
        Returns:
            List of raw artifact content strings for LLM processing
        """
        self.logger.info(f"Collecting {len(score_artifacts)} raw score_extraction artifacts")
        raw_artifacts = []
        
        for artifact_hash in score_artifacts:
            try:
                # Load raw artifact bytes
                artifact_bytes = self.storage.get_artifact(artifact_hash)
                if not artifact_bytes:
                    self.logger.warning(f"Could not load artifact {artifact_hash}")
                    continue
                
                # THIN: Just decode to string, no parsing or validation
                artifact_content = artifact_bytes.decode('utf-8')
                raw_artifacts.append(artifact_content)
                
            except Exception as e:
                self.logger.warning(f"Error loading artifact {artifact_hash}: {e}")
                continue
        
        return raw_artifacts
    
    
    def _step1_statistical_analysis(self, raw_artifacts: List[str], batch_id: str) -> Optional[str]:
        """
        Step 1: Perform statistical analysis using CAS discovery for source materials.
        
        Args:
            raw_artifacts: List of raw artifact data from analysis phase
            batch_id: Batch identifier
            
        Returns:
            Complete LLM response with statistical results, or None if failed
        """
        try:
            # Load the externalized prompt template
            prompt_template = self._load_prompt_template()
            self.logger.info(f"Loaded prompt template, length: {len(prompt_template)}")
            
            # CAS Discovery: Get source materials from hash addresses
            run_context = getattr(self, '_current_run_context', {})
            metadata = run_context.get('metadata', {})
            
            # Get framework from CAS
            framework_hash = metadata.get('framework_hash')
            if not framework_hash:
                raise ValueError("Framework hash not found in run_context metadata")
            framework_content = self.storage.get_artifact(framework_hash).decode('utf-8')
            
            # Get corpus manifest from CAS
            corpus_manifest_hash = metadata.get('corpus_manifest_hash')
            if not corpus_manifest_hash:
                raise ValueError("Corpus manifest hash not found in run_context metadata")
            corpus_manifest_content = self.storage.get_artifact(corpus_manifest_hash).decode('utf-8')
            
            # Get experiment context
            experiment_id = run_context.get('experiment_id', 'unknown')
            
            # THIN: Pass raw artifact strings directly to LLM
            # Join all raw artifacts with separators for LLM processing
            raw_data_block = "\n\n=== ARTIFACT SEPARATOR ===\n\n".join(raw_artifacts)
            
            # Prepare the prompt with raw data
            prompt = prompt_template.format(
                framework_content=framework_content,
                experiment_name=experiment_id,
                experiment_description=f"Statistical analysis of {experiment_id} corpus using the Cohesive Flourishing Framework",
                research_questions="How do rhetorical strategies in this corpus manifest through the Cohesive Flourishing Framework dimensions?",
                experiment_content=framework_content,
                data_columns="dimensional_scores, derived_metrics, evidence",
                sample_data=raw_data_block,
                corpus_manifest=corpus_manifest_content
            )

            self.audit.log_agent_event(self.agent_name, "step1_started", {
                "batch_id": batch_id,
                "step": "statistical_analysis",
                "model": "vertex_ai/gemini-2.5-pro",
                "artifacts_count": len(raw_artifacts)
            })
            
            # Call LLM
            response = self.gateway.execute_call(
                model="vertex_ai/gemini-2.5-pro",
                prompt=prompt,
                # No response_schema for THIN agent
            )
            
            if isinstance(response, tuple):
                content, metadata = response
            else:
                content = response.get('content', '')
                metadata = response.get('metadata', {})
            
            self.logger.info(f"LLM response length: {len(content)}")
            self.logger.info(f"LLM response preview: {content[:200]}...")
            
            # THIN: Return raw LLM response directly, no parsing
            if content and content.strip():
                self.audit.log_agent_event(self.agent_name, "step1_completed", {
                    "batch_id": batch_id,
                    "step": "statistical_analysis",
                    "response_length": len(content)
                })
                return content.strip()
            else:
                self.logger.error("Statistical analysis returned empty response")
                return None
                
        except Exception as e:
            self.logger.error(f"Step 1 failed: {e}")
            return None
    
    
    # REMOVED: _read_framework_file - replaced with CAS discovery in _step1_statistical_analysis