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
3. EvidenceCurator: LLM selects evidence based on actual results
4. ResultsInterpreter: LLM synthesizes final narrative

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
from ..results_interpreter.agent import ResultsInterpreter, InterpretationRequest
from ..results_interpreter.dual_purpose_results_interpreter import DualPurposeResultsInterpreter, DualPurposeReportRequest, DualPurposeReportResponse
from ...classification_agent.agent import ClassificationAgent, ClassificationRequest, ClassificationResponse
from ...score_grounding.grounding_evidence_generator import GroundingEvidenceGenerator, GroundingEvidenceRequest

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
        
        # Initialize agents with infrastructure
        self.raw_data_planner = RawDataAnalysisPlanner(model=model, audit_logger=audit_logger)
        self.derived_metrics_planner = DerivedMetricsAnalysisPlanner(model=model, audit_logger=audit_logger)
        self.evidence_curator = EvidenceCurator(model=model, audit_logger=audit_logger)
        self.results_interpreter = ResultsInterpreter(model=model, audit_logger=audit_logger)
        self.dual_purpose_interpreter = DualPurposeResultsInterpreter(model=model, audit_logger=audit_logger)
        self.classification_agent = ClassificationAgent()
        self.grounding_evidence_generator = GroundingEvidenceGenerator(model=model, audit_logger=audit_logger)
        
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
            
            # Stage 3: Curate Evidence
            self.logger.info("🔍 Stage 3: Curating evidence...")
            
            # Debug output for evidence curator
            if self.debug_agent in ['evidence-curator', None] and self.debug_level in ['debug', 'verbose']:
                self.logger.info(f"🔍 DEBUG: Evidence curation input:")
                stage_2_results = exec_response.get('stage_2_derived_metrics', {})
                statistical_results = stage_2_results.get('results', {})
                self.logger.info(f"   - Statistical results keys: {list(statistical_results.keys()) if statistical_results else 'NO DATA'}")
                self.logger.info(f"   - Evidence artifact hash: {request.evidence_artifact_hash}")
                if statistical_results:
                    for key, value in statistical_results.items():
                        if isinstance(value, dict):
                            self.logger.info(f"   - {key}: {list(value.keys()) if value else 'EMPTY'}")
                        else:
                            self.logger.info(f"   - {key}: {type(value).__name__}")
            
            stage_start = time.time()
            
            curation_response = self._stage_3_curate_evidence(exec_response, request)
            
            stage_timings['evidence_curation'] = time.time() - stage_start
            stage_success['evidence_curation'] = curation_response.success
            
            if not curation_response.success:
                return self._create_error_response(
                    "Evidence curation failed",
                    curation_response.error_message,
                    stage_timings,
                    stage_success,
                    time.time() - start_time
                )
            
            # Stage 4: Generate Grounding Evidence
            self.logger.info("🔗 Stage 4: Generating grounding evidence...")
            stage_start = time.time()
            
            grounding_response = self._stage_4_generate_grounding_evidence(exec_response, request)
            
            stage_timings['grounding_evidence_generation'] = time.time() - stage_start
            stage_success['grounding_evidence_generation'] = grounding_response.success
            
            if not grounding_response.success:
                return self._create_error_response(
                    "Grounding evidence generation failed",
                    grounding_response.error_message,
                    stage_timings,
                    stage_success,
                    time.time() - start_time
                )
            
            # Stage 5: Interpret Results
            self.logger.info("📖 Stage 5: Interpreting results...")
            stage_start = time.time()
            
            stage_response = self._stage_5_interpret_results(
                exec_response, curation_response, grounding_response, request
            )
            
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
            evidence_hash = self._store_artifact_with_metadata(
                content=json.dumps(curation_response.to_json_serializable()),
                artifact_type="curated_evidence",
                stage="evidence_curation",
                dependencies=[results_hash, request.scores_artifact_hash]
            )
            
            # Store grounding evidence artifact
            grounding_hash = self._store_artifact_with_metadata(
                content=json.dumps(grounding_response.to_json_serializable()),
                artifact_type="grounding_evidence",
                stage="grounding_evidence_generation",
                dependencies=[results_hash, request.evidence_artifact_hash]
            )
            
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
                statistical_summary=interpretation_response.statistical_summary
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
        combined_data = self.artifact_client.get_artifact(request.scores_artifact_hash)
        
        # Convert raw bytes to string for LLM processing (THIN principle)
        raw_analysis_data = combined_data.decode('utf-8')
        
        self.logger.info(f"THIN approach: Passing raw analysis data ({len(raw_analysis_data)} chars) to two-stage planners")
        
        # Create enhanced data summary with column discovery (THIN principle)
        # Parse the raw data to discover available columns for the LLM
        try:
            import json
            import pandas as pd
            from discernus.core.math_toolkit import _json_scores_to_dataframe_thin
            
            # Parse the raw analysis data to get column information
            analysis_result = json.loads(raw_analysis_data)
            df = _json_scores_to_dataframe_thin(analysis_result)
            
            # Create column summary for LLM discovery
            available_columns = list(df.columns)
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
- DataFrame shape: {df.shape[0]} rows, {df.shape[1]} columns

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
                research_questions=research_questions
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

    def _stage_3_curate_evidence(self, exec_response, request: ProductionPipelineRequest):
        """Stage 3: Curate evidence based on statistical results."""
        
        # Retrieve evidence data for curation using THIN pre-extracted evidence artifact
        # This replaces the old registry scanning approach with direct artifact access
        combined_data = self.artifact_client.get_artifact(request.evidence_artifact_hash)
        self.logger.info(f"Using pre-extracted evidence artifact: {request.evidence_artifact_hash[:12]}...")
        
        # Extract results from the two-stage structure
        # Use derived metrics results (Stage 2) for evidence curation
        stage_2_results = exec_response.get('stage_2_derived_metrics', {})
        statistical_results = stage_2_results.get('results', {})
        
        # Create curation request with raw data - let LLM handle parsing
        curation_request = EvidenceCurationRequest(
            statistical_results=statistical_results,
            evidence_data=combined_data,
            framework_spec=request.framework_spec,
            max_evidence_per_finding=request.max_evidence_per_finding,
            min_confidence_threshold=request.min_confidence_threshold
        )
        
        # Log evidence curation start
        self.audit_logger.log_agent_event(
            "EvidenceCurator",
            "evidence_curation_start",
            {
                "available_evidence_count": 57,  # Known from JSON structure
                "statistical_results_keys": list(statistical_results.keys()) if isinstance(statistical_results, dict) else "non_dict_results",
                "max_evidence_per_finding": request.max_evidence_per_finding,
                "stage_2_results_used": True
            }
        )
        
        curation_response = self.evidence_curator.curate_evidence(curation_request)
        
        # Debug logging for evidence curation
        if self.debug_agent == "evidence-curator" and self.debug_level in ["debug", "verbose"]:
            self.logger.info(f"Evidence curation success: {curation_response.success}")
            self.logger.info(f"Evidence curation error: {curation_response.error_message or 'None'}")
            self.logger.info(f"Curated evidence count: {len(curation_response.curated_evidence) if curation_response.curated_evidence else 0}")
            if curation_response.curated_evidence:
                self.logger.info(f"Curated evidence types: {[evidence.evidence_type for evidence in curation_response.curated_evidence]}")
        
        return curation_response

    def _stage_4_generate_grounding_evidence(self, exec_response, request: ProductionPipelineRequest):
        """Stage 4: Generate grounding evidence for every numerical score."""
        
        # Retrieve evidence data for grounding generation
        evidence_data = self.artifact_client.get_artifact(request.evidence_artifact_hash)
        self.logger.info(f"Generating grounding evidence using evidence artifact: {request.evidence_artifact_hash[:12]}...")
        
        # Extract analysis scores from the execution response
        stage_2_results = exec_response.get('stage_2_derived_metrics', {})
        analysis_scores = stage_2_results.get('results', {})
        
        # Extract document name from experiment context or use default
        document_name = "unknown_document"
        if request.experiment_context:
            # Try to extract document name from experiment context
            import re
            doc_match = re.search(r'document[:\s]+([^\s,]+)', request.experiment_context, re.IGNORECASE)
            if doc_match:
                document_name = doc_match.group(1)
        
        # Create grounding evidence request
        grounding_request = GroundingEvidenceRequest(
            analysis_scores=analysis_scores,
            evidence_data=evidence_data,
            framework_spec=request.framework_spec,
            document_name=document_name,
            min_confidence_threshold=request.min_confidence_threshold
        )
        
        # Log grounding evidence generation start
        self.audit_logger.log_agent_event(
            "GroundingEvidenceGenerator",
            "grounding_generation_start",
            {
                "document_name": document_name,
                "analysis_scores_keys": list(analysis_scores.keys()) if isinstance(analysis_scores, dict) else "non_dict_scores",
                "evidence_artifact": request.evidence_artifact_hash[:12] + "...",
                "framework_spec_length": len(request.framework_spec)
            }
        )
        
        # Generate grounding evidence for all scores
        return self.grounding_evidence_generator.generate_grounding_evidence(grounding_request)

    def _stage_5_interpret_results(self, exec_response, curation_response, grounding_response, request: ProductionPipelineRequest):
        """Stage 5: Generate final narrative interpretation with grounding evidence."""
        
        # Extract results from the two-stage structure
        # Use derived metrics results (Stage 2) for interpretation
        stage_2_results = exec_response.get('stage_2_derived_metrics', {})
        statistical_results = stage_2_results.get('results', {})
        
        # Debug logging for results interpreter
        if self.debug_agent in ['results-interpreter', None] and self.debug_level in ['debug', 'verbose']:
            self.logger.info(f"📖 DEBUG: Results interpreter input:")
            self.logger.info(f"   - Statistical results keys: {list(statistical_results.keys()) if statistical_results else 'NO DATA'}")
            self.logger.info(f"   - Curated evidence keys: {list(curation_response.curated_evidence.keys()) if curation_response.curated_evidence else 'NO DATA'}")
            self.logger.info(f"   - Total evidence pieces: {sum(len(evidence_list) for evidence_list in curation_response.curated_evidence.values()) if curation_response.curated_evidence else 0}")
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
        
        # Check for evidence curation issues
        if not curation_response.success:
            notable_errors.append(f"Evidence curation failed: {curation_response.error_message}")
        elif curation_response.curated_evidence and len(curation_response.curated_evidence) == 0:
            warnings.append("No evidence was curated - this may indicate data quality issues")
        elif curation_response.curated_evidence:
            total_evidence = sum(len(evidence_list) for evidence_list in curation_response.curated_evidence.values())
            if total_evidence < 5:
                warnings.append(f"Limited evidence base (only {total_evidence} pieces of evidence curated for synthesis)")
        
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
        
        interpretation_request = InterpretationRequest(
            statistical_results=statistical_results,
            curated_evidence=curation_response.curated_evidence,
            framework_spec=request.framework_spec,
            experiment_context=request.experiment_context,
            footnote_registry=curation_response.footnote_registry,
            
            # Provenance metadata
            run_id=run_id,
            models_used={
                "synthesis": self.model,
                "analysis": self.analysis_model if self.analysis_model else "unknown"
            },
            execution_timestamp_utc=execution_time_utc.strftime('%Y-%m-%d %H:%M:%S UTC'),
            execution_timestamp_local=execution_time_local.strftime('%Y-%m-%d %H:%M:%S %Z'),
            framework_name=framework_name,
            framework_version=framework_version,
            corpus_info=self._extract_corpus_info(request.experiment_context),
            
            # Error and warning tracking
            notable_errors=notable_errors if notable_errors else None,
            warnings=warnings if warnings else None,
            quality_alerts=quality_alerts if quality_alerts else None,
            
            # v7.3: Framework reporting metadata
            reporting_metadata=reporting_metadata
        )
        
        # Log interpretation start
        self.audit_logger.log_agent_event(
            "ResultsInterpreter",
            "interpretation_start",
            {
                "curated_evidence_count": len(curation_response.curated_evidence),
                "interpretation_focus": request.interpretation_focus,
                "stage_2_results_used": True
            }
        )
        
        # Store the interpretation response for use in the main method
        interpretation_response = self.results_interpreter.interpret_results(interpretation_request)
        
        # Generate dual-purpose report for academic collaboration
        dual_purpose_response = self._stage_6_generate_dual_purpose_report(
            interpretation_response, curation_response, grounding_response, request
        )
        
        # Return a success response object so the main method can continue with artifact creation
        class StageResponse:
            def __init__(self, success, response, dual_purpose_response):
                self.success = success
                self.response = response
                self.dual_purpose_response = dual_purpose_response
                self.error_message = ""
        
        return StageResponse(True, interpretation_response, dual_purpose_response)

    def _stage_6_generate_dual_purpose_report(self, interpretation_response, curation_response, grounding_response, request: ProductionPipelineRequest):
        """Stage 6: Generate dual-purpose report for academic collaboration."""
        
        self.logger.info("📝 Stage 6: Generating dual-purpose report for academic collaboration...")
        
        try:
            # Extract data from previous stages
            statistical_results = interpretation_response.statistical_results if hasattr(interpretation_response, 'statistical_results') else {}
            scores_data = {}  # Will be populated from artifact if needed
            
            # Convert evidence data to JSON-serializable format
            if curation_response.success and hasattr(curation_response, 'to_json_serializable'):
                evidence_data = curation_response.to_json_serializable()
            else:
                evidence_data = {}
            
            # Extract experiment context for report metadata
            experiment_context = {}
            if request.experiment_context:
                try:
                    experiment_context = json.loads(request.experiment_context)
                except (json.JSONDecodeError, AttributeError):
                    experiment_context = {}
            
            # Extract experiment name and subtitle
            experiment_name = experiment_context.get('name', 'Computational Analysis')
            experiment_subtitle = experiment_context.get('description', 'Analysis using computational framework')
            if isinstance(experiment_subtitle, str) and len(experiment_subtitle) > 100:
                experiment_subtitle = experiment_subtitle[:97] + "..."
            
            # Extract corpus information
            corpus_info = self._extract_corpus_info(request.experiment_context)
            document_count = corpus_info.get('document_count', 0)
            corpus_type = corpus_info.get('corpus_type', 'Text Corpus')
            corpus_composition = corpus_info.get('corpus_composition', 'Unknown')
            
            # Generate timestamps
            execution_time_utc = datetime.now(timezone.utc)
            execution_time_local = datetime.now()
            
            # Extract framework information
            framework_name = request.framework_name or "Unknown Framework"
            framework_version = "v7.3"  # Default for current architecture
            
            # Generate run ID
            run_hash = hash(f"{request.scores_artifact_hash}_{execution_time_utc.isoformat()}")
            run_id = f"{execution_time_utc.strftime('%Y%m%dT%H%M%SZ')}_{abs(run_hash)%100000:05d}"
            
            # Extract real cost data from audit logger
            cost_data = self.audit_logger.get_session_costs()
            
            # Create dual-purpose report request with configurable options
            dual_purpose_request = DualPurposeReportRequest(
                        experiment_name=experiment_name,
                        experiment_subtitle=experiment_subtitle,
                        run_id=run_id,
                        execution_time_utc=execution_time_utc.strftime('%Y-%m-%d %H:%M:%S UTC'),
                        execution_time_local=execution_time_local.strftime('%Y-%m-%d %H:%M:%S %Z'),
                        analysis_model=self.analysis_model or "unknown",
                        synthesis_model=self.model,
                        framework_name=framework_name,
                        framework_version=framework_version,
                        document_count=document_count,
                        corpus_type=corpus_type,
                        corpus_composition=corpus_composition,
                        statistical_results=statistical_results,
                        evidence_data=evidence_data,
                        scores_data=scores_data,
                        run_directory=f"runs/{run_id}",
                        cost_data=cost_data,
                        # Configurable options for flexibility
                        template_path=None,  # Use default discovery
                        section_markers=None  # Use default markers
                    )
            
            # Generate dual-purpose report
            dual_purpose_response = self.dual_purpose_interpreter.generate_dual_purpose_report(dual_purpose_request)
            
            if dual_purpose_response.success:
                self.logger.info("✅ Dual-purpose report generated successfully")
                return dual_purpose_response
            else:
                self.logger.warning(f"⚠️ Dual-purpose report generation failed: {dual_purpose_response.error_message}")
                # Return a fallback response
                return DualPurposeReportResponse(
                    report_content="Dual-purpose report generation failed. Standard report available.",
                    scanner_section="",
                    collaborator_section="",
                    transparency_section="",
                    success=False,
                    error_message=dual_purpose_response.error_message
                )
                
        except Exception as e:
            self.logger.error(f"❌ Failed to generate dual-purpose report: {e}")
            return DualPurposeReportResponse(
                report_content="",
                scanner_section="",
                collaborator_section="",
                transparency_section="",
                success=False,
                error_message=str(e)
            )

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
            success=False,
            total_execution_time=total_time,
            stage_timings=stage_timings,
            stage_success=stage_success,
            word_count=0,
            evidence_integration_summary="",
            statistical_summary="",
            error_message=f"{error_type}: {error_message}"
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