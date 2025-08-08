#!/usr/bin/env python3
"""
THIN Declarative Mathematical Synthesis Pipeline - Production Version
===================================================================

Integrates with Discernus infrastructure:
- LocalArtifactStorage for content-addressable data
- AuditLogger for complete provenance
- MathToolkit for reliable mathematical operations

4-Agent Architecture:
1. AnalysisPlanner: LLM generates JSON analysis plans
2. MathToolkit: Pre-built, tested mathematical functions
3. EvidenceCurator: txtai-based RAG for scalable evidence retrieval
4. RAGEnhancedInterpreter: Single intelligent interpreter with multi-audience sections

Key Innovation: Declarative mathematical specification eliminates code generation errors.
"""

import logging
import json
import time
import pandas as pd
import hashlib

import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from io import BytesIO

# Import main codebase infrastructure
import sys
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# MinIO client removed - using LocalArtifactStorage via compatibility wrapper
from discernus.core.audit_logger import AuditLogger

# Import THIN synthesis agents
from ..raw_data_analysis_planner.agent import RawDataAnalysisPlanner, RawDataAnalysisPlanRequest
from ..derived_metrics_analysis_planner.agent import DerivedMetricsAnalysisPlanner, DerivedMetricsAnalysisPlanRequest
from ..evidence_curator.agent import EvidenceCurator, EvidenceCurationRequest
from ...txtai_evidence_curator.agent import TxtaiEvidenceCurator, TxtaiCurationRequest
from ..results_interpreter.rag_enhanced_interpreter import RAGEnhancedResultsInterpreter, RAGInterpretationRequest
from ..results_interpreter.thin_interpreter import ThinResultsInterpreterAgent
from ...classification_agent.agent import ClassificationAgent, ClassificationRequest, ClassificationResponse
# GroundingEvidenceGenerator removed - functionality integrated into RAG interpreter per Epic #280
from ...evidence_indexer_agent.agent import EvidenceIndexerAgent, IndexingRequest, IndexingResponse
from ...evidence_quality_measurement.agent import EvidenceQualityMeasurementAgent, QualityMeasurementRequest, QualityMeasurementResponse

# Import MathToolkit for reliable mathematical operations
from discernus.core.math_toolkit import execute_analysis_plan, execute_analysis_plan_thin

@dataclass
class ProductionPipelineRequest:
    """Production pipeline request using artifact hashes instead of file paths."""
    framework_spec: str
    scores_artifact_hash: str  # LocalArtifactStorage hash for scores CSV
    evidence_artifact_hash: str  # LocalArtifactStorage hash for evidence CSV
    experiment_context: Optional[str] = None
    max_evidence_per_finding: int = 3
    min_confidence_threshold: float = 0.7
    interpretation_focus: str = "comprehensive"
    
    # Provenance context (Issue #208 fix)
    framework_hash: Optional[str] = None
    corpus_hash: Optional[str] = None
    framework_name: Optional[str] = None
    corpus_manifest: Optional[Dict[str, Any]] = None

@dataclass
class ProductionPipelineResponse:
    """Complete pipeline response with all outputs and metadata."""
    # Final outputs
    narrative_report: str
    executive_summary: str
    key_findings: list
    
    # Intermediate artifacts (as hashes for provenance)
    analysis_plan_hash: str
    statistical_results_hash: str
    curated_evidence_hash: str
    grounding_evidence_hash: str
    dual_purpose_report_hash: str
    
    # Pipeline metadata
    success: bool
    total_execution_time: float
    stage_timings: Dict[str, float]
    stage_success: Dict[str, bool]
    
    # Quality metrics
    word_count: int
    evidence_integration_summary: str
    statistical_summary: str
    
    # Error information (if any)
    error_message: str = ""

class ProductionThinSynthesisPipeline:
    """
    Production version of THIN Code-Generated Synthesis Pipeline.
    
    Integrates with Discernus infrastructure for robust, scalable synthesis.
    """
    
    def __init__(self,
                 artifact_client,  # LocalArtifactStorage compatibility wrapper
                 audit_logger: AuditLogger,
                 model: str,
                 analysis_model: Optional[str] = None,
                 debug_agent: Optional[str] = None,
                 debug_level: str = "info"):
        """
        Initialize production pipeline with infrastructure dependencies.
        
        Args:
            artifact_client: LocalArtifactStorage compatibility wrapper for content-addressable storage
            audit_logger: Audit logger for complete provenance
            model: LLM model for all agents
        """
        self.artifact_client = artifact_client
        self.audit_logger = audit_logger
        self.model = model
        self.analysis_model = analysis_model
        self.debug_agent = debug_agent
        self.debug_level = debug_level
        
        # Initialize agents with infrastructure (THIN architecture)
        self.raw_data_planner = RawDataAnalysisPlanner(model=model, audit_logger=audit_logger)
        self.derived_metrics_planner = DerivedMetricsAnalysisPlanner(model=model, audit_logger=audit_logger)
        self.evidence_indexer = EvidenceIndexerAgent(model=model, audit_logger=audit_logger)
        self.evidence_curator = EvidenceCurator(model=model, audit_logger=audit_logger)
        self.txtai_curator = TxtaiEvidenceCurator(model=model, audit_logger=audit_logger)  # Used by RAG interpreter
        self.rag_interpreter = RAGEnhancedResultsInterpreter(model=model, audit_logger=audit_logger)
        self.thin_interpreter = ThinResultsInterpreterAgent(model=model, audit_logger=audit_logger)
        self.classification_agent = ClassificationAgent()
        self.quality_measurement_agent = EvidenceQualityMeasurementAgent(model=model, audit_logger=audit_logger)
        # grounding_evidence_generator removed - functionality integrated into RAG interpreter
        
        # Set up logging
        self.logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        
        self.audit_logger.log_agent_event(
            "ProductionThinSynthesisPipeline",
            "initialization",
            {
                "model": model,
                "architecture": "declarative_mathematical_specification",
                "math_toolkit_enabled": True
            }
        )
        
        self.logger.info("🏭 Production THIN Synthesis Pipeline initialized")
        self.logger.info(f"🔧 Synthesis pipeline using model: {model}")

    def _store_artifact_with_metadata(self, content: str, artifact_type: str, 
                                    stage: str, dependencies: List[str] = None) -> str:
        """Store artifact with comprehensive provenance metadata."""
        content_bytes = content.encode('utf-8')
        metadata = {
            "artifact_type": artifact_type,
            "stage": stage,
            "timestamp": datetime.utcnow().isoformat(),
            "dependencies": json.dumps(dependencies or []),
            "content_hash": hashlib.sha256(content_bytes).hexdigest(),
            "size_bytes": str(len(content_bytes)),
            "pipeline_version": "v2.0",
            "agent_versions": json.dumps({
                "analysis_planner": "v1.0",
                "results_interpreter": "v1.0", 
                "evidence_curator": "v1.0"
            })
        }
        
        # Store content with metadata using LocalArtifactStorage capabilities
        hash_id = hashlib.sha256(content_bytes).hexdigest()
        
        # Check if already exists (cache hit)
        if self.artifact_client.artifact_exists(hash_id):
            self.logger.debug(f"Artifact cache hit: {hash_id}")
            return hash_id
        
        # Store artifact with metadata using the artifact client interface
        try:
            if hasattr(self.artifact_client, 'client') and hasattr(self.artifact_client, 'bucket'):
                # Direct LocalArtifactStorage client - store with metadata
                self.artifact_client.client.put_object(
                    bucket_name=self.artifact_client.bucket,
                    object_name=hash_id,
                    data=BytesIO(content_bytes),
                    length=len(content_bytes),
                    metadata=metadata
                )
                self.logger.debug(f"Stored artifact with LocalArtifactStorage metadata: {hash_id}")
            elif hasattr(self.artifact_client, 'local_storage'):
                # LocalArtifactStorage compatibility wrapper - call underlying storage with metadata
                hash_result = self.artifact_client.local_storage.put_artifact(content_bytes, metadata)
                if hash_result != hash_id:
                    self.logger.warning(f"Hash mismatch: expected {hash_id}, got {hash_result}")
                self.logger.debug(f"Stored artifact with LocalStorage metadata: {hash_id}")
            else:
                # Unknown client type - use standard put_artifact method (no metadata)
                hash_result = self.artifact_client.put_artifact(content_bytes)
                if hash_result != hash_id:
                    self.logger.warning(f"Hash mismatch: expected {hash_id}, got {hash_result}")
                self.logger.warning(f"Stored artifact without metadata (unknown client type): {hash_id}")
        except Exception as e:
            # Fallback: use standard put_artifact method (no metadata)
            self.logger.warning(f"Metadata storage failed, using standard storage: {e}")
            self.artifact_client.put_artifact(content_bytes)
        
        self.logger.info(f"Stored {artifact_type} artifact: {hash_id} ({stage}, {len(content_bytes)} bytes)")
        
        # Log artifact creation for provenance
        self.audit_logger.log_agent_event(
            "ProductionThinSynthesisPipeline",
            "artifact_created",
            {
                "artifact_hash": hash_id,
                "artifact_type": artifact_type,
                "stage": stage,
                "size_bytes": len(content_bytes),
                "dependencies": dependencies or []
            }
        )
        
        return hash_id

    def run(self, request: ProductionPipelineRequest) -> ProductionPipelineResponse:
        """
        Execute the complete 4-agent synthesis pipeline with full infrastructure.
        
        Args:
            request: ProductionPipelineRequest with artifact hashes
            
        Returns:
            ProductionPipelineResponse with complete synthesis results
        """
        start_time = time.time()
        stage_timings = {}
        stage_success = {}
        
        # Initialize artifact hash variables at method level for accessibility
        plan_hash = ""
        results_hash = ""
        evidence_hash = ""
        
        # Initialize response variables at method level for accessibility
        plan_response = None
        exec_response = None
        curation_response = None
        
        # Log pipeline start
        self.audit_logger.log_agent_event(
            "ProductionThinSynthesisPipeline",
            "pipeline_start",
            {
                "framework_spec_preview": request.framework_spec[:200] + "..." if len(request.framework_spec) > 200 else request.framework_spec,
                "scores_artifact": request.scores_artifact_hash,
                "evidence_artifact": request.evidence_artifact_hash,
                "experiment_context": request.experiment_context,
                # Add provenance context logging (Issue #208 fix)
                "framework_hash": request.framework_hash[:12] + "..." if request.framework_hash else "MISSING",
                "corpus_hash": request.corpus_hash[:12] + "..." if request.corpus_hash else "MISSING",
                "framework_name": request.framework_name,
                "provenance_validated": bool(request.framework_hash and request.corpus_hash)
            }
        )
        
        # Log provenance context for debugging
        if request.framework_hash and request.corpus_hash:
            self.logger.info(f"🔍 Synthesis provenance validated:")
            self.logger.info(f"   - Framework: {request.framework_name} ({request.framework_hash[:12]}...)")
            self.logger.info(f"   - Corpus: {request.corpus_hash[:12]}...")
            self.logger.info(f"   - Scores artifact: {request.scores_artifact_hash[:12]}...")
            self.logger.info(f"   - Evidence artifact: {request.evidence_artifact_hash[:12]}...")
        else:
            self.logger.warning("⚠️  Missing provenance context - synthesis agents operating blind!")
        
        try:
            self.logger.info("🚀 Starting Production THIN Synthesis Pipeline")
            
            # Stage 1: Generate Analysis Plan
            self.logger.info("📝 Stage 1: Generating analysis plan...")
            stage_start = time.time()
            
            plan_response = self._stage_1_generate_analysis_plan(request)
            
            stage_timings['analysis_planning'] = time.time() - stage_start
            stage_success['analysis_planning'] = plan_response.success
            
            if not plan_response.success:
                return self._create_error_response(
                    "Analysis planning failed", 
                    plan_response.error_message,
                    stage_timings, 
                    stage_success,
                    time.time() - start_time
                )
            
            # Stage 2: Execute Analysis Plan
            self.logger.info("⚙️  Stage 2: Executing analysis plan...")
            stage_start = time.time()
            
            exec_response = self._stage_2_execute_analysis_plan(plan_response, request)
            
            stage_timings['analysis_execution'] = time.time() - stage_start
            stage_success['analysis_execution'] = len(exec_response.get('errors', [])) == 0
            
            if len(exec_response.get('errors', [])) > 0:
                return self._create_error_response(
                    "Analysis execution failed",
                    "; ".join(exec_response['errors']),
                    stage_timings,
                    stage_success,
                    time.time() - start_time
                )
            
            # Stage 2.5: Generate Intelligent Evidence Index
            self.logger.info("📇 Stage 2.5: Generating intelligent evidence index...")
            stage_start = time.time()
            
            index_response = self._stage_2_5_generate_evidence_index(request)
            
            stage_timings['evidence_indexing'] = time.time() - stage_start
            stage_success['evidence_indexing'] = index_response.success
            
            if not index_response.success:
                return self._create_error_response(
                    "Evidence indexing failed",
                    index_response.error_message,
                    stage_timings,
                    stage_success,
                    time.time() - start_time
                )
            
            # Stage 3 & 4 REMOVED: Redundant evidence processing eliminated per Epic #280 Milestone 1.1
            # Evidence processing now handled directly by Stage 5 RAG interpreter for THIN architecture
            
            # Stage 5: Evidence-Enhanced Results Interpretation (THIN Architecture)
            self.logger.info("📖 Stage 5: Evidence-enhanced results interpretation...")
            stage_start = time.time()
            
            stage_response = self._stage_5_interpret_results(exec_response, request)
            
            stage_timings['results_interpretation'] = time.time() - stage_start
            stage_success['results_interpretation'] = stage_response.success
            
            if not stage_response.success:
                return self._create_error_response(
                    "Results interpretation failed",
                    stage_response.error_message,
                    stage_timings,
                    stage_success,
                    time.time() - start_time
                )
            
            # Extract the actual interpretation response and dual-purpose response
            interpretation_response = stage_response.response
            dual_purpose_response = stage_response.dual_purpose_response
            
            # Stage 6: Evidence Quality Measurement (Epic #354)
            self.logger.info("📊 Stage 6: Evidence quality measurement...")
            stage_start = time.time()
            
            quality_response = self._stage_6_measure_evidence_quality(
                request, exec_response, interpretation_response
            )
            
            stage_timings['quality_measurement'] = time.time() - stage_start
            stage_success['quality_measurement'] = quality_response.success
            
            if not quality_response.success:
                self.logger.warning(f"Quality measurement failed: {quality_response.error_message}")
                # Continue with synthesis even if quality measurement fails
            
            # Store intermediate artifacts with comprehensive metadata
            plan_hash = self._store_artifact_with_metadata(
                content=json.dumps(plan_response.analysis_plan),
                artifact_type="analysis_plan",
                stage="raw_data_analysis",
                dependencies=[request.scores_artifact_hash]
            )
            
            # Defensive JSON serialization for exec_response
            def make_json_safe(obj):
                if isinstance(obj, (str, int, float, bool, type(None))):
                    return obj
                elif isinstance(obj, (list, tuple)):
                    return [make_json_safe(item) for item in obj]
                elif isinstance(obj, dict):
                    return {str(k): make_json_safe(v) for k, v in obj.items()}
                else:
                    return str(obj)
            
            # Store the combined two-stage results with comprehensive metadata
            safe_exec_response = make_json_safe(exec_response)
            results_hash = self._store_artifact_with_metadata(
                content=json.dumps(safe_exec_response),
                artifact_type="statistical_results",
                stage="mathematical_analysis",
                dependencies=[plan_hash, request.scores_artifact_hash]
            )
            # Evidence artifact storage removed per Epic #280 Milestone 1.1
            # Evidence processing unified in Stage 5 RAG interpreter for THIN architecture
            evidence_hash = ""  # No longer needed - evidence handled directly by RAG interpreter
            grounding_hash = ""  # Stage 4 eliminated
            
            # Success! Create complete response
            total_time = time.time() - start_time
            
            self.logger.info(f"✅ Pipeline completed successfully in {total_time:.2f} seconds")
            
            # Log pipeline completion
            self.audit_logger.log_agent_event(
                "ProductionThinSynthesisPipeline",
                "pipeline_complete",
                {
                    "total_time": total_time,
                    "stage_timings": stage_timings,
                    "analysis_plan_hash": plan_hash,
                    "statistical_results_hash": results_hash,
                    "curated_evidence_hash": evidence_hash,
                    "word_count": interpretation_response.word_count
                }
            )
            
            # Store dual-purpose report artifact
            dual_purpose_hash = self._store_artifact_with_metadata(
                content=dual_purpose_response.report_content if dual_purpose_response.success else "Dual-purpose report generation failed",
                artifact_type="dual_purpose_report",
                stage="dual_purpose_report_generation",
                dependencies=[results_hash, evidence_hash, grounding_hash]
            )
            
            return ProductionPipelineResponse(
                # Final outputs
                narrative_report=interpretation_response.narrative_report,
                executive_summary=interpretation_response.executive_summary,
                key_findings=interpretation_response.key_findings,
                
                # Intermediate artifacts
                analysis_plan_hash=plan_hash,
                statistical_results_hash=results_hash,
                curated_evidence_hash=evidence_hash,
                grounding_evidence_hash=grounding_hash,
                
                # Pipeline metadata
                success=True,
                total_execution_time=total_time,
                stage_timings=stage_timings,
                stage_success=stage_success,
                
                # Quality metrics
                word_count=interpretation_response.word_count,
                evidence_integration_summary=interpretation_response.evidence_integration_summary,
                statistical_summary=interpretation_response.statistical_summary,
                dual_purpose_report_hash=dual_purpose_hash
            )
            
        except Exception as e:
            total_time = time.time() - start_time
            self.logger.error(f"Pipeline failed with exception: {str(e)}")
            
            # Log pipeline failure
            self.audit_logger.log_agent_event(
                "ProductionThinSynthesisPipeline",
                "pipeline_failed",
                {
                    "total_time": total_time,
                    "error": str(e),
                    "stage_timings": stage_timings,
                    "stage_success": stage_success
                }
            )
            
            return self._create_error_response(
                "Pipeline execution failed",
                str(e),
                stage_timings,
                stage_success,
                total_time
            )

    def _stage_1_generate_analysis_plan(self, request: ProductionPipelineRequest):
        """Stage 1: Generate two-stage analysis plan using declarative mathematical specification."""
        
        # THIN approach: Pass raw analysis data directly to both planners
        # Let LLMs handle all data interpretation and structure understanding
        scores_data_bytes = self.artifact_client.get_artifact(request.scores_artifact_hash)
        
        # Ground the planner by providing the actual available columns.
        from discernus.core.math_toolkit import _json_scores_to_dataframe_thin
        scores_df = _json_scores_to_dataframe_thin(json.loads(scores_data_bytes.decode('utf-8')))
        available_columns = scores_df.columns.tolist()

        raw_analysis_data = scores_data_bytes.decode('utf-8')
        
        self.logger.info(f"THIN approach: Passing raw analysis data ({len(raw_analysis_data)} chars) to two-stage planners")
        
        # Create enhanced data summary with column discovery (THIN principle)
        # Parse the raw data to discover available columns for the LLM
        try:
            # Create column summary for LLM discovery
            metadata_columns = [col for col in available_columns if col not in 
                              [c for c in available_columns if c.endswith(('_score', '_salience', '_confidence'))] 
                              and col != 'aid']
            score_columns = [col for col in available_columns if col.endswith('_score')]
            salience_columns = [col for col in available_columns if col.endswith('_salience')]
            confidence_columns = [col for col in available_columns if col.endswith('_confidence')]
            
            column_summary = f"""
Raw Analysis Data:
- Data size: {len(raw_analysis_data)} characters
- Data type: JSON analysis results
- Source: Analysis artifact {request.scores_artifact_hash[:12]}...
- DataFrame shape: {scores_df.shape[0]} rows, {scores_df.shape[1]} columns

Available Columns (COMPLETE LIST - use ONLY these):
{available_columns}

Column Categories (discovered from actual data):
- Document identifier: ['aid']
- Metadata/Grouping variables: {metadata_columns}
- Dimensional scores: {score_columns}
- Salience weights: {salience_columns}
- Confidence ratings: {confidence_columns}

CRITICAL: Use ONLY the exact column names listed above. Any column not in this list does NOT exist in the data.
"""
        except Exception as e:
            # Fallback to simple summary if parsing fails
            column_summary = f"""
Raw Analysis Data:
- Data size: {len(raw_analysis_data)} characters
- Data type: JSON analysis results
- Source: Analysis artifact {request.scores_artifact_hash[:12]}...
- Note: LLM will interpret structure and content directly
- Warning: Column discovery failed - use raw data to identify available columns
"""
        
        try:
            # Extract research questions from experiment context
            research_questions = self._extract_research_questions(request.experiment_context)
            
            # Stage 1A: Generate raw data collection plan
            self.logger.info("📊 Stage 1A: Generating raw data collection plan...")
            
            raw_data_request = RawDataAnalysisPlanRequest(
                experiment_context=request.experiment_context or "",
                framework_spec=request.framework_spec,
                corpus_manifest="",  # Will be populated from experiment context
                research_questions=research_questions,
                available_columns=available_columns
            )
            
            # Log raw data planning start
            self.audit_logger.log_agent_event(
                "RawDataAnalysisPlanner",
                "raw_data_planning_start",
                {
                    "framework_spec_length": len(request.framework_spec),
                    "research_questions_count": len(research_questions),
                    "approach": "thin_stage_1_raw_data"
                }
            )
            
            raw_data_response = self.raw_data_planner.generate_raw_data_plan(raw_data_request)
            
            if not raw_data_response.success:
                raise Exception(f"Raw data planning failed: {raw_data_response.error_message}")
            
            # Stage 1B: Generate derived metrics analysis plan
            self.logger.info("🧮 Stage 1B: Generating derived metrics analysis plan...")
            
            derived_metrics_request = DerivedMetricsAnalysisPlanRequest(
                experiment_context=request.experiment_context or "",
                framework_spec=request.framework_spec,
                corpus_manifest="",  # Will be populated from experiment context
                research_questions=research_questions,
                raw_data_summary=column_summary
            )
            
            # Log derived metrics planning start
            self.audit_logger.log_agent_event(
                "DerivedMetricsAnalysisPlanner",
                "derived_metrics_planning_start",
                {
                    "framework_spec_length": len(request.framework_spec),
                    "research_questions_count": len(research_questions),
                    "raw_data_summary_length": len(column_summary),
                    "approach": "thin_stage_2_derived_metrics"
                }
            )
            
            derived_metrics_response = self.derived_metrics_planner.generate_derived_metrics_plan(derived_metrics_request)
            
            if not derived_metrics_response.success:
                raise Exception(f"Derived metrics planning failed: {derived_metrics_response.error_message}")
            
            # THIN: Combine both raw LLM responses for downstream processing
            combined_plan = {
                "stage_1_raw_data": raw_data_response.raw_llm_response or raw_data_response.analysis_plan,  # THIN: Prefer raw response
                "stage_2_derived_metrics": derived_metrics_response.raw_llm_response or derived_metrics_response.analysis_plan,  # THIN: Prefer raw response
                "combined_summary": f"Two-stage THIN analysis plan: {len(raw_data_response.raw_llm_response or '')} + {len(derived_metrics_response.raw_llm_response or '')} chars of raw LLM responses"
            }
            
            # Debug logging for generated plans (THIN approach)
            if self.debug_agent == "analysis-plan" and self.debug_level in ["debug", "verbose"]:
                self.logger.info(f"Raw data plan response: {len(raw_data_response.raw_llm_response or '')} chars")
                self.logger.info(f"Derived metrics plan response: {len(derived_metrics_response.raw_llm_response or '')} chars")
                if raw_data_response.raw_llm_response:
                    self.logger.info(f"Raw data plan preview: {raw_data_response.raw_llm_response[:500]}...")
                if derived_metrics_response.raw_llm_response:
                    self.logger.info(f"Derived metrics plan preview: {derived_metrics_response.raw_llm_response[:500]}...")
            
            # Create a unified response object for compatibility
            class CombinedPlanResponse:
                def __init__(self, combined_plan):
                    self.analysis_plan = combined_plan
                    self.success = True
                    self.error_message = None
                    self.raw_llm_response = f"Combined plan: {combined_plan['combined_summary']}"
            
            return CombinedPlanResponse(combined_plan)
            
        except Exception as e:
            self.logger.error(f"Analysis planning failed: {str(e)}")
            return type('ErrorResponse', (), {
                'success': False,
                'error_message': str(e),
                'analysis_plan': None,
                'raw_llm_response': None
            })()
    
    def _extract_research_questions(self, experiment_context: str) -> list:
        """
        Extract research questions from experiment context.
        
        Args:
            experiment_context: The experiment context string
            
        Returns:
            List of research questions
        """
        if not experiment_context:
            return []
        
        # Simple extraction - look for lines that start with numbers or bullet points
        questions = []
        lines = experiment_context.split('\n')
        
        for line in lines:
            line = line.strip()
            # Look for numbered questions (e.g., "1. What is...")
            if line and (line[0].isdigit() and '. ' in line[:10]):
                question = line.split('. ', 1)[1] if '. ' in line else line
                questions.append(question)
            # Look for bullet points (e.g., "- What is...")
            elif line.startswith('- ') or line.startswith('* '):
                question = line[2:] if len(line) > 2 else line
                questions.append(question)
            # Look for "Research Question:" patterns
            elif 'research question' in line.lower() and ':' in line:
                question = line.split(':', 1)[1].strip()
                if question:
                    questions.append(question)
        
        return questions

    def _stage_2_execute_analysis_plan(self, plan_response, request: ProductionPipelineRequest):
        """Stage 2: Execute two-stage analysis plan using MathToolkit (THIN approach)."""
        
        # THIN approach: Pass raw analysis data directly to MathToolkit
        # Let MathToolkit handle all data parsing and DataFrame creation
        combined_data = self.artifact_client.get_artifact(request.scores_artifact_hash)
        raw_analysis_data = combined_data.decode('utf-8')
        
        self.logger.info(f"THIN approach: Passing raw analysis data ({len(raw_analysis_data)} chars) to MathToolkit")
        
        try:
            # Validate plan response
            if not plan_response.success:
                raise Exception(f"Analysis plan generation failed: {plan_response.error_message}")
            
            if not plan_response.analysis_plan:
                raise Exception("No analysis plan generated")
            
            # THIN: Extract raw LLM responses for direct execution
            combined_plan = plan_response.analysis_plan
            raw_data_plan = combined_plan.get("stage_1_raw_data", {})
            derived_metrics_plan = combined_plan.get("stage_2_derived_metrics", {})
            
            self.logger.info(f"Executing THIN two-stage plan: {len(str(raw_data_plan))} + {len(str(derived_metrics_plan))} chars of raw LLM responses")
            
            # Log execution start
            self.audit_logger.log_agent_event(
                "MathToolkit",
                "thin_two_stage_analysis_execution_start",
                {
                    "raw_data_plan_size": len(str(raw_data_plan)),
                    "derived_metrics_plan_size": len(str(derived_metrics_plan)),
                    "raw_data_size": len(raw_analysis_data),
                    "approach": "fully_thin_execution"
                }
            )
            
            # THIN: Extract framework calculation_spec for authoritative formulas
            framework_calculation_spec = None
            try:
                import json
                import re
                # Extract JSON appendix from framework
                json_pattern = r"```json\n(.*?)\n```"
                json_match = re.search(json_pattern, request.framework_spec, re.DOTALL)
                if json_match:
                    framework_config = json.loads(json_match.group(1))
                    framework_calculation_spec = framework_config.get("calculation_spec")
                    if framework_calculation_spec:
                        self.logger.info(f"THIN: Using framework calculation_spec with {len(framework_calculation_spec.get('formulas', {}))} authoritative formulas")
                    else:
                        self.logger.warning("THIN: No calculation_spec found in framework - falling back to LLM-generated formulas")
            except Exception as e:
                self.logger.warning(f"THIN: Failed to extract framework calculation_spec: {e} - falling back to LLM-generated formulas")
            
            # Execute Stage 1: Raw data collection (THIN: Pass raw LLM response)
            stage_1_results = {}
            if raw_data_plan:  # THIN: Always try to execute if plan exists
                self.logger.info("📊 Executing Stage 1: Raw data collection (THIN)...")
                stage_1_results = execute_analysis_plan_thin(raw_analysis_data, raw_data_plan, request.corpus_manifest, framework_calculation_spec)
            
            # Execute Stage 2: Derived metrics and statistical analysis (THIN: Pass raw LLM response)
            self.logger.info("🧮 Executing Stage 2: Derived metrics and statistical analysis (THIN)...")
            stage_2_results = execute_analysis_plan_thin(raw_analysis_data, derived_metrics_plan, request.corpus_manifest, framework_calculation_spec)
            
            # Combine results from both stages
            combined_results = {
                "stage_1_raw_data": stage_1_results,
                "stage_2_derived_metrics": stage_2_results,
                "combined_summary": f"Two-stage execution: {len(stage_1_results.get('results', {}))} raw data results + {len(stage_2_results.get('results', {}))} derived metrics results"
            }
            
            # Debug logging for execution results
            if self.debug_agent == "math-toolkit" and self.debug_level in ["debug", "verbose"]:
                self.logger.info(f"Stage 1 success: {len(stage_1_results.get('errors', [])) == 0}")
                self.logger.info(f"Stage 1 errors: {stage_1_results.get('errors', [])}")
                self.logger.info(f"Stage 1 tasks completed: {len(stage_1_results.get('results', {}))}")
                self.logger.info(f"Stage 2 success: {len(stage_2_results.get('errors', [])) == 0}")
                self.logger.info(f"Stage 2 errors: {stage_2_results.get('errors', [])}")
                self.logger.info(f"Stage 2 tasks completed: {len(stage_2_results.get('results', {})) if stage_2_results else 0}")
            
            # Log execution completion
            self.audit_logger.log_agent_event(
                "MathToolkit",
                "two_stage_analysis_execution_complete",
                {
                    "stage_1_success": len(stage_1_results.get('errors', [])) == 0,
                    "stage_1_errors_count": len(stage_1_results.get('errors', [])),
                    "stage_1_tasks_completed": len(stage_1_results.get('results', {})),
                    "stage_2_success": len(stage_2_results.get('errors', [])) == 0,
                    "stage_2_errors_count": len(stage_2_results.get('errors', [])),
                    "stage_2_tasks_completed": len(stage_2_results.get('results', {}))
                }
            )
            
            return combined_results
            
        except Exception as e:
            self.logger.error(f"Two-stage analysis execution failed: {str(e)}")
            raise

    def _stage_2_5_generate_evidence_index(self, request: ProductionPipelineRequest) -> IndexingResponse:
        """Stage 2.5: Generate intelligent evidence index for RAG-based retrieval."""
        try:
            # Retrieve evidence data
            evidence_data = self.artifact_client.get_artifact(request.evidence_artifact_hash)
            
            # Create indexing request
            indexing_request = IndexingRequest(
                evidence_data=evidence_data,
                model=self.model
            )
            
            # Generate the intelligent index
            self.logger.info(f"📇 Generating intelligent evidence index from {len(evidence_data)} bytes of evidence data")
            index_response = self.evidence_indexer.generate_index(indexing_request)
            
            if index_response.success:
                # Store the intelligent index as an artifact
                index_hash = self._store_artifact_with_metadata(
                    index_response.intelligent_index.decode('utf-8'),
                    "intelligent_evidence_index",
                    {
                        "original_evidence_hash": request.evidence_artifact_hash,
                        "index_size_bytes": len(index_response.intelligent_index),
                        "compression_ratio": len(index_response.intelligent_index) / len(evidence_data)
                    }
                )
                
                self.logger.info(f"📇 Intelligent evidence index generated successfully: {index_hash[:12]}...")
                
                # Add the index hash to the response for downstream stages
                index_response.index_artifact_hash = index_hash
                
            return index_response
            
        except Exception as e:
            self.logger.error(f"Evidence indexing failed: {str(e)}")
            return IndexingResponse(
                intelligent_index=b"",
                success=False,
                error_message=str(e)
            )

    def _stage_3_curate_evidence(self, exec_response, request: ProductionPipelineRequest, index_response: IndexingResponse = None):
        """Stage 3: Curate evidence based on statistical results."""
        
        # Retrieve evidence data for curation using THIN pre-extracted evidence artifact
        # This replaces the old registry scanning approach with direct artifact access
        combined_data = self.artifact_client.get_artifact(request.evidence_artifact_hash)
        self.logger.info(f"Using pre-extracted evidence artifact: {request.evidence_artifact_hash[:12]}...")
        
        # Extract results from the two-stage structure
        # Use derived metrics results (Stage 2) for evidence curation
        stage_2_results = exec_response.get('stage_2_derived_metrics', {})
        
        # Create curation request. Note that scores_data is now passed from the request.
        curation_request = EvidenceCurationRequest(
            statistical_results=stage_2_results,  # Pass the full stage_2_results with results key
            evidence_data=combined_data,
            framework_spec=request.framework_spec,
            scores_data=self.artifact_client.get_artifact(request.scores_artifact_hash)
        )
        
        # Get intelligent index data for RAG-based curation
        intelligent_index_data = None
        if index_response and index_response.success and index_response.index_artifact_hash:
            intelligent_index_data = self.artifact_client.get_artifact(index_response.index_artifact_hash)
        
        # Log evidence curation start
        self.audit_logger.log_agent_event(
            "EvidenceCurator",
            "evidence_curation_start",
            {
                "available_evidence_count": 57,  # Known from JSON structure
                "statistical_results_keys": list(stage_2_results.get('results', {}).keys()) if stage_2_results.get('results') else "no_results",
                "max_evidence_per_finding": request.max_evidence_per_finding,
                "stage_2_results_used": True,
                "intelligent_index_available": intelligent_index_data is not None
            }
        )
        
        curation_response = self.evidence_curator.curate_evidence(curation_request, intelligent_index_data)
        
        # Debug logging for evidence curation
        if self.debug_agent == "evidence-curator" and self.debug_level in ["debug", "verbose"]:
            self.logger.info(f"Evidence curation success: {curation_response.success}")
            self.logger.info(f"Evidence curation error: {curation_response.error_message or 'None'}")
            self.logger.info(f"Raw LLM curation length: {len(curation_response.raw_llm_curation) if curation_response.raw_llm_curation else 0}")
            if curation_response.raw_llm_curation:
                self.logger.info(f"Raw LLM curation preview: {curation_response.raw_llm_curation[:200]}...")
        
        return curation_response
    
    # Stage 3 & 4 methods removed per Epic #280 Milestone 1.1
    # Evidence processing unified in Stage 5 RAG interpreter for THIN architecture

    def _stage_5_interpret_results(self, exec_response, request: ProductionPipelineRequest):
        """Stage 5: Generate final narrative interpretation with grounding evidence."""
        
        # Extract results from the two-stage structure
        # Use derived metrics results (Stage 2) for interpretation
        stage_2_results = exec_response.get('stage_2_derived_metrics', {})
        statistical_results = stage_2_results.get('results', {})
        
        # Debug logging for results interpreter (THIN architecture)
        if self.debug_agent in ['results-interpreter', None] and self.debug_level in ['debug', 'verbose']:
            self.logger.info(f"📖 DEBUG: Evidence-enhanced results interpreter input:")
            self.logger.info(f"   - Statistical results keys: {list(statistical_results.keys()) if statistical_results else 'NO DATA'}")
            self.logger.info(f"   - Evidence artifact hash: {request.evidence_artifact_hash}")
            if statistical_results:
                for key, value in statistical_results.items():
                    if isinstance(value, dict):
                        self.logger.info(f"   - {key}: {list(value.keys()) if value else 'EMPTY'}")
                    else:
                        self.logger.info(f"   - {key}: {type(value).__name__}")
        
        # Build provenance metadata for report headers
        from datetime import datetime, timezone
        
        # Generate timestamps
        execution_time_utc = datetime.now(timezone.utc)
        execution_time_local = datetime.now()
        
        # Use provided framework name or extract from spec
        framework_name = request.framework_name or "Unknown Framework"
        framework_version = "v6.0"  # Default for current architecture
        
        if not request.framework_name and request.framework_spec:
            lines = request.framework_spec.split('\n')[:15]  # Check first 15 lines
            for line in lines:
                line_lower = line.lower()
                if any(keyword in line_lower for keyword in ['framework', 'assessment', 'analysis']):
                    if '#' in line or '**' in line:
                        framework_name = line.strip('# *').strip()
                        # Try to extract version
                        if 'v' in line_lower and any(char.isdigit() for char in line):
                            import re
                            version_match = re.search(r'v\d+\.\d+', line_lower)
                            if version_match:
                                framework_version = version_match.group()
                        break
        
        # Generate a more meaningful run ID
        run_hash = hash(f"{request.scores_artifact_hash}_{execution_time_utc.isoformat()}")
        run_id = f"{execution_time_utc.strftime('%Y%m%dT%H%M%SZ')}_{abs(run_hash)%100000:05d}"
        
        # Collect errors and warnings from the execution pipeline
        notable_errors = []
        warnings = []
        quality_alerts = []
        
        # Check for statistical execution errors
        if exec_response.get('stage_2_derived_metrics', {}).get('errors'):
            for error in exec_response['stage_2_derived_metrics']['errors'][:3]:  # Top 3 errors
                if 'not found in DataFrame' in error:
                    notable_errors.append(f"Missing data column: {error.split(':')[0] if ':' in error else error}")
                elif 'ANOVA failed' in error:
                    notable_errors.append(f"Statistical test failed: {error.split(':')[-1].strip() if ':' in error else error}")
                else:
                    notable_errors.append(error)
        
        # Check for derived metrics calculation issues
        stage_2_results = exec_response.get('stage_2_derived_metrics', {})
        if stage_2_results:
            for task_name, task_result in stage_2_results.items():
                if isinstance(task_result, dict) and task_result.get('type') == 'derived_metrics_calculation':
                    if not task_result.get('success', True):
                        failed_calcs = task_result.get('failed_calculations', [])
                        for failed_calc in failed_calcs[:2]:  # Top 2 failed calculations
                            notable_errors.append(f"Derived metric calculation failed: {failed_calc.get('metric', 'unknown')} - {failed_calc.get('error', 'unknown error')}")
                    elif task_result.get('success_rate', 1.0) < 1.0:
                        warnings.append(f"Partial derived metrics success: {task_result.get('success_rate', 0):.1%} of calculations succeeded")
        
        # Evidence curation status will be checked by RAG interpreter during synthesis
        # No pre-checking needed in THIN architecture - let LLM handle evidence intelligently
        
        # Check statistical results for issues
        stage_2_results = exec_response.get('stage_2_derived_metrics', {})
        if stage_2_results.get('results'):
            successful_tasks = len([r for r in stage_2_results['results'].values() if not r.get('error')])
            total_tasks = len(stage_2_results['results'])
            if successful_tasks < total_tasks:
                warnings.append(f"Statistical analysis: {successful_tasks}/{total_tasks} tasks completed successfully")
        
        # v7.3: Extract reporting_metadata from experiment context
        reporting_metadata = {}
        try:
            if request.experiment_context:
                experiment_context = json.loads(request.experiment_context)
                framework_config = experiment_context.get("framework_config", {})
                reporting_metadata = framework_config.get("reporting_metadata", {})
        except (json.JSONDecodeError, AttributeError):
            # Fallback to empty metadata if parsing fails
            reporting_metadata = {}
        
        # Open the synthesis aperture: Use rich analysis evidence instead of empty statistical curation
        analysis_evidence_data = self.artifact_client.get_artifact(request.evidence_artifact_hash)
        
        # Ensure txtai curator is initialized with evidence for RAG-enhanced synthesis
        if not self.txtai_curator.index_built:
            self.logger.info("🔍 Initializing txtai curator for RAG-enhanced synthesis...")
            if self.txtai_curator._build_evidence_index(analysis_evidence_data):
                self.logger.info("✅ txtai index built successfully for synthesis")
            else:
                self.logger.warning("⚠️  txtai index build failed - falling back to traditional synthesis")
        
        # Log interpretation start
        self.audit_logger.log_agent_event(
            "RAGEnhancedResultsInterpreter",
            "interpretation_start",
            {
                "statistical_results_count": len(statistical_results),
                "txtai_available": getattr(self.txtai_curator, 'index_built', False),
                "framework_name": framework_name,
                "run_id": run_id
            }
        )
        
        # Build request for current interpreter(s)
        rag_request = RAGInterpretationRequest(
            statistical_results=statistical_results,
            framework_spec=request.framework_spec,
            experiment_context=request.experiment_context,
            txtai_curator=self.txtai_curator if getattr(self.txtai_curator, 'index_built', False) else None,
            
            # Provenance metadata
            run_id=run_id,
            models_used={
                "synthesis": self.model,
                "analysis": self.analysis_model or "unknown"
            },
            execution_timestamp_utc=execution_time_utc.strftime('%Y-%m-%d %H:%M:%S UTC'),
            execution_timestamp_local=execution_time_local.strftime('%Y-%m-%d %H:%M:%S %Z'),
            framework_name=framework_name,
            framework_version=framework_version,
            corpus_info=self._safe_extract_corpus_info(request.experiment_context),
            cost_data=self._safe_get_cost_data()
        )
        
        # Feature flag to switch to THIN interpreter
        # Default to THIN interpreter; allow opting out
        use_thin = os.environ.get("DISCERNUS_USE_THIN_INTERPRETER", "true").lower() in ("1", "true", "yes")
        if use_thin:
            # Adapt request to thin agent (statistical_results, framework_spec, experiment_context, txtai_curator)
            class ThinReq:
                def __init__(self, rr):
                    self.statistical_results = rr.statistical_results
                    self.framework_spec = rr.framework_spec
                    self.experiment_context = rr.experiment_context
                    self.txtai_curator = rr.txtai_curator
            thin_req = ThinReq(rag_request)
            thin_resp = self.thin_interpreter.interpret_results(thin_req)
            class ThinCompat:
                def __init__(self, r):
                    self.success = r.success
                    self.narrative_report = r.full_report
                    self.executive_summary = r.scanner_section
                    self.error_message = r.error_message
                    self.scanner_section = r.scanner_section
                    self.collaborator_section = r.collaborator_section
                    self.transparency_section = r.transparency_section
                    self.word_count = r.word_count
                    self.evidence_queries_used = r.evidence_queries_used
                    self.statistical_results = {}
                    self.report_content = r.full_report
                    self.key_findings = []
                    self.evidence_integration_summary = {}
                    self.statistical_summary = {}
            interpretation_response = ThinCompat(thin_resp)
        else:
            # Generate RAG-enhanced interpretation (replaces both stage 5 and 6)
            rag_response = self.rag_interpreter.interpret_results(rag_request)
            class CompatibilityResponse:
                def __init__(self, rag_response):
                    self.success = rag_response.success
                    self.narrative_report = rag_response.full_report
                    self.executive_summary = rag_response.scanner_section
                    self.error_message = rag_response.error_message or ""
                    self.scanner_section = rag_response.scanner_section
                    self.collaborator_section = rag_response.collaborator_section
                    self.transparency_section = rag_response.transparency_section
                    self.word_count = rag_response.word_count
                    self.evidence_queries_used = rag_response.evidence_queries_used
                    self.statistical_results = {}
                    self.report_content = rag_response.full_report
                    self.key_findings = []
                    self.evidence_integration_summary = {}
                    self.statistical_summary = {}
            interpretation_response = CompatibilityResponse(rag_response)
        dual_purpose_response = interpretation_response  # Same object, different interface
        
        # Return a success response object so the main method can continue with artifact creation
        class StageResponse:
            def __init__(self, success, response, dual_purpose_response):
                self.success = success
                self.response = response
                self.dual_purpose_response = dual_purpose_response
                self.error_message = ""
        
        return StageResponse(True, interpretation_response, dual_purpose_response)

    # Stage 6 removed - RAG-enhanced interpreter now handles all report generation in stage 5
    
    def _safe_get_cost_data(self):
        """Safely get cost data that can be JSON serialized."""
        try:
            if self.audit_logger and hasattr(self.audit_logger, 'get_session_costs'):
                cost_data = self.audit_logger.get_session_costs()
                # Ensure all values are JSON serializable
                if isinstance(cost_data, dict):
                    safe_cost_data = {}
                    for key, value in cost_data.items():
                        try:
                            import json
                            json.dumps(value)  # Test if serializable
                            safe_cost_data[key] = value
                        except (TypeError, ValueError):
                            safe_cost_data[key] = str(value)  # Convert to string if not serializable
                    return safe_cost_data
            return {}
        except Exception as e:
            self.logger.warning(f"Failed to get cost data: {e}")
            return {}
    
    def _safe_extract_corpus_info(self, experiment_context):
        """Safely extract corpus info that can be JSON serialized."""
        try:
            corpus_info = self._extract_corpus_info(experiment_context)
            # Ensure all values are JSON serializable
            if isinstance(corpus_info, dict):
                safe_corpus_info = {}
                for key, value in corpus_info.items():
                    try:
                        import json
                        json.dumps(value)  # Test if serializable
                        safe_corpus_info[key] = value
                    except (TypeError, ValueError):
                        safe_corpus_info[key] = str(value)  # Convert to string if not serializable
                return safe_corpus_info
            return corpus_info or {}
        except Exception as e:
            self.logger.warning(f"Failed to extract corpus info: {e}")
            return {}

    # THIN REFACTORING: Removed ~150 lines of THICK DataFrame parsing logic
    # All data parsing is now handled by individual agents (AnalysisPlanner, MathToolkit, etc.)
    # This eliminates the pipeline's framework intelligence and makes it truly THIN

    def _create_error_response(self, 
                             error_type: str, 
                             error_message: str,
                             stage_timings: Dict[str, float],
                             stage_success: Dict[str, bool],
                             total_time: float) -> ProductionPipelineResponse:
        """Create standardized error response."""
        
        return ProductionPipelineResponse(
            narrative_report="",
            executive_summary="",
            key_findings=[],
            analysis_plan_hash="",
            statistical_results_hash="",
            curated_evidence_hash="",
            grounding_evidence_hash="",
            dual_purpose_report_hash="",
            success=False,
            total_execution_time=total_time,
            stage_timings=stage_timings,
            stage_success=stage_success,
            word_count=0,
            evidence_integration_summary="",
            statistical_summary="",
            error_message=f"{error_type}: {error_message}"
        )
    
    def _stage_6_measure_evidence_quality(self, request: ProductionPipelineRequest, exec_response: Dict[str, Any], interpretation_response) -> QualityMeasurementResponse:
        """
        Stage 6: Evidence Quality Measurement (Epic #354)
        
        Implements comprehensive quality measurement:
        - REQ-EU-001: Evidence utilization rate measurement
        - REQ-EU-002: Interpretive claim coverage tracking
        - REQ-EU-003: Evidence-claim alignment scoring
        - REQ-EU-004: Evidence relevance ranking
        - REQ-EU-005: Evidence quality scoring framework
        """
        try:
            # Get available evidence data
            available_evidence_data = self.artifact_client.get_artifact(request.evidence_artifact_hash)
            if not available_evidence_data:
                return QualityMeasurementResponse(
                    success=False,
                    error_message="Failed to retrieve available evidence data"
                )
            
            # Get used evidence from interpretation response
            used_evidence_data = b'{"evidence_data": []}'  # Default empty
            if hasattr(interpretation_response, 'used_evidence') and interpretation_response.used_evidence:
                used_evidence_data = json.dumps({
                    'evidence_data': interpretation_response.used_evidence
                }).encode('utf-8')
            
            # Create quality measurement request
            quality_request = QualityMeasurementRequest(
                available_evidence_data=available_evidence_data,
                used_evidence_data=used_evidence_data,
                statistical_results=exec_response,
                synthesis_report=interpretation_response.narrative_report,
                framework_spec=request.framework_spec,
                experiment_context=request.experiment_context
            )
            
            # Execute quality measurement
            quality_response = self.quality_measurement_agent.measure_evidence_quality(quality_request)
            
            # Log quality metrics
            if quality_response.success and quality_response.metrics:
                metrics = quality_response.metrics
                self.logger.info(f"📊 Evidence Quality Metrics:")
                self.logger.info(f"   - Utilization Rate: {metrics.evidence_utilization_rate:.1%}")
                self.logger.info(f"   - Claim Coverage: {metrics.interpretive_claim_coverage:.1%}")
                self.logger.info(f"   - Alignment Score: {metrics.evidence_claim_alignment_score:.1%}")
                self.logger.info(f"   - Overall Quality: {metrics.overall_quality_score:.1%}")
                
                # Log recommendations
                if quality_response.recommendations:
                    self.logger.info(f"📋 Quality Recommendations:")
                    for rec in quality_response.recommendations:
                        self.logger.info(f"   - {rec}")
            
            return quality_response
            
        except Exception as e:
            self.logger.error(f"Quality measurement failed: {str(e)}")
            return QualityMeasurementResponse(
                success=False,
                error_message=str(e)
            )
    
    def _extract_corpus_info(self, experiment_context: Optional[str]) -> Dict[str, Any]:
        """Extract corpus information from experiment context in a framework-agnostic way."""
        default_corpus_info = {
            "document_count": "Unknown",
            "corpus_type": "Text Corpus", 
            "date_range": "Unknown"
        }
        
        if not experiment_context:
            return default_corpus_info
            
        try:
            context = json.loads(experiment_context)
            corpus_info = context.get("corpus_info", {})
            
            # Extract available corpus metadata
            extracted_info = {}
            extracted_info["document_count"] = str(corpus_info.get("document_count", "Unknown"))
            extracted_info["corpus_type"] = corpus_info.get("corpus_type", "Text Corpus")
            extracted_info["date_range"] = corpus_info.get("date_range", "Unknown")
            
            return extracted_info
            
        except (json.JSONDecodeError, AttributeError):
            return default_corpus_info 