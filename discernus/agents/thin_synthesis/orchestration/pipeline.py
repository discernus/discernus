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
import re

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
from ...comprehensive_knowledge_curator.agent import ComprehensiveKnowledgeCurator, ComprehensiveIndexRequest, KnowledgeQuery
from ...sequential_synthesis.agent import SequentialSynthesisAgent, SynthesisRequest, SynthesisResponse
from ....core.math_toolkit import execute_analysis_plan_thin
from ....core.statistical_formatter import StatisticalResultsFormatter


@dataclass
class ProductionPipelineRequest:
    """Production pipeline request using artifact hashes instead of file paths."""
    framework_spec: str
    scores_artifact_hash: str  # LocalArtifactStorage hash for scores CSV
    evidence_artifact_hash: str  # LocalArtifactStorage hash for evidence CSV
    corpus_artifact_hash: Optional[str] = None  # LocalArtifactStorage hash for combined corpus
    experiment_context: Optional[str] = None
    max_evidence_per_finding: int = 3
    min_confidence_threshold: float = 0.7
    interpretation_focus: str = "comprehensive"
    
    # Provenance context (Issue #208 fix)
    framework_hash: Optional[str] = None
    corpus_hash: Optional[str] = None # Hash of corpus manifest
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
    Production version of THIN Synthesis Pipeline (v2.0 Architecture).
    
    Integrates with Discernus infrastructure for robust, scalable synthesis using the SequentialSynthesisAgent.
    """
    
    def __init__(self,
                 artifact_client,  # LocalArtifactStorage compatibility wrapper
                 audit_logger: AuditLogger,
                 model: str,
                 analysis_model: Optional[str] = None,
                 debug_agent: Optional[str] = None,
                 debug_level: str = "info"):
        """
        Initialize production pipeline with v2.0 infrastructure dependencies.
        
        Args:
            artifact_client: LocalArtifactStorage compatibility wrapper for content-addressable storage
            audit_logger: Audit logger for complete provenance
            model: LLM model for synthesis agents
            analysis_model: LLM model for analysis agents
        """
        self.artifact_client = artifact_client
        self.audit_logger = audit_logger
        self.synthesis_model = model
        self.analysis_model = analysis_model
        
        # V2.0 architecture: Use SequentialSynthesisAgent and ComprehensiveKnowledgeCurator
        self.sequential_synthesis_agent = SequentialSynthesisAgent(model=model, audit_logger=audit_logger)
        self.knowledge_curator = ComprehensiveKnowledgeCurator(model=model, artifact_storage=self.artifact_client, audit_logger=audit_logger)

        # Debug configuration
        self.debug_agent = os.environ.get("DISCERNUS_DEBUG_AGENT")
        self.debug_level = os.environ.get("DISCERNUS_DEBUG_LEVEL", "info")
        
        # Set up logging
        self.logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        
        self.audit_logger.log_agent_event(
            "ProductionThinSynthesisPipeline",
            "initialization",
            {
                "model": model,
                "architecture": "sequential_synthesis_v2.0",
                "math_toolkit_enabled": True
            }
        )
        
        self.logger.info("🏭 Production THIN Synthesis Pipeline initialized (v2.0 Architecture)")
        self.logger.info(f"🔧 Synthesis pipeline using model: {model}")

    def run(self, request: ProductionPipelineRequest) -> ProductionPipelineResponse:
        """
        Execute the full synthesis pipeline using the Sequential Synthesis Agent v2.0.
        """
        start_time = time.time()
        self.logger.info(f"🔍 Synthesis provenance validated:")
        self.logger.info(f"   - Framework: {request.framework_name} ({request.framework_hash[:12] if request.framework_hash else '...'}...)")
        self.logger.info(f"   - Corpus: ({request.corpus_hash[:12] if request.corpus_hash else '...'}...)")
        self.logger.info(f"   - Scores artifact: {request.scores_artifact_hash[:12] if request.scores_artifact_hash else '...'}...")
        self.logger.info(f"   - Evidence artifact: {request.evidence_artifact_hash[:12] if request.evidence_artifact_hash else '...'}...")

        self.logger.info("🚀 Executing Sequential Synthesis Agent v2.0...")

        try:
            # Step 1: Run MathToolkit to get statistical results
            self.logger.info("📊 Running statistical analysis...")
            statistical_results_raw = self._run_statistical_analysis(request)
            
            statistical_results_hash = self._store_artifact_with_metadata(
                json.dumps(statistical_results_raw, default=self._json_serializer), 
                "statistical_results",
                "statistical_analysis",
                dependencies=[request.scores_artifact_hash]
            )

            # Use the new formatter to prepare stats for the LLM
            formatter = StatisticalResultsFormatter(statistical_results_raw)
            statistical_results_formatted = formatter.format_all()

            # Step 1.5: Export final CSVs with all statistical results
            self._export_final_csvs(request, statistical_results_hash, statistical_results_raw)

            # Step 2: Build the RAG index
            self.logger.info("📚 Building RAG lookup index...")
            self._build_rag_index(request)

            # Step 3: Execute Sequential Synthesis
            direct_context = {
                "experiment": json.loads(request.experiment_context) if request.experiment_context and request.experiment_context.strip() else {},
                "framework": request.framework_spec,
                "corpus": request.corpus_manifest,
                "statistics": statistical_results_formatted,
            }
            
            synthesis_request = SynthesisRequest(
                direct_context=direct_context,
                rag_curator=self.knowledge_curator
            )

            synthesis_response = self.sequential_synthesis_agent.synthesize_research(synthesis_request)
            
            self.audit_logger.log_agent_event("SequentialSynthesisAgent", "synthesis_complete", {"success": synthesis_response.success})
            
            if not synthesis_response.success:
                raise Exception(synthesis_response.error_message or "Sequential synthesis failed without an error message.")

            # Generate three-part academic report
            from discernus.core.report_generator import ThreePartReportGenerator
            
            provenance_metadata = {
                'run_id': request.scores_artifact_hash[:16] if request.scores_artifact_hash else 'unknown',
                'framework_hash': request.framework_hash,
                'corpus_hash': request.corpus_hash,
                'scores_hash': request.scores_artifact_hash
            }
            
            cost_metadata = {
                'total_cost': 0.0,  # TODO: Implement actual cost tracking
                'total_tokens': 0   # TODO: Implement actual token tracking
            }
            
            # Extract experiment name - use simple_test name for now
            # TODO: Fix upstream experiment context passing
            experiment_name = 'Democratic Discourse Cohesion Study'
            
            report_generator = ThreePartReportGenerator(
                experiment_name=experiment_name,
                framework_name=self._extract_framework_name(request.framework_spec),
                statistical_results=statistical_results_raw,
                provenance_metadata=provenance_metadata,
                cost_metadata=cost_metadata
            )
            
            # Generate complete three-part report
            complete_report = report_generator.generate_report(synthesis_response.final_report)
            
            final_report_hash = self._store_artifact_with_metadata(
                complete_report, "final_report", "synthesis", [statistical_results_hash]
            )
            
            total_time = time.time() - start_time
            self.logger.info(f"✅ Pipeline completed successfully in {total_time:.2f} seconds")
            
            # Construct a compatible ProductionPipelineResponse
            return ProductionPipelineResponse(
                success=True,
                narrative_report=complete_report,  # Now using three-part report
                executive_summary="See Part II of report.", 
                key_findings=[], # TODO: Extract from report
                analysis_plan_hash="", # No longer generated
                statistical_results_hash=statistical_results_hash,
                curated_evidence_hash="", # No longer generated as a separate artifact
                grounding_evidence_hash="", # No longer generated
                dual_purpose_report_hash=final_report_hash,
                total_execution_time=total_time,
                stage_timings={"synthesis": total_time},
                stage_success={"synthesis": True},
                word_count=len(complete_report.split()),
                evidence_integration_summary="Three-part academic report with deterministic statistical foundation",
                statistical_summary="Deterministic MathToolkit results (no LLM interpretation)",
                error_message=""
            )

        except Exception as e:
            self.logger.error(f"Sequential Synthesis Pipeline failed: {e}", exc_info=True)
            total_time = time.time() - start_time
            return ProductionPipelineResponse(
                success=False, 
                narrative_report="",
                executive_summary="",
                key_findings=[],
                analysis_plan_hash="",
                statistical_results_hash="",
                curated_evidence_hash="",
                grounding_evidence_hash="",
                dual_purpose_report_hash="",
                total_execution_time=total_time,
                stage_timings={"synthesis_failed": total_time},
                stage_success={"synthesis": False},
                word_count=0,
                evidence_integration_summary="",
                statistical_summary="",
                error_message=str(e)
            )

    def _export_final_csvs(self, request: ProductionPipelineRequest, statistical_results_hash: str, statistical_results_raw: Dict[str, Any]):
        """Helper to export final CSVs including derived metrics."""
        try:
            from discernus.agents.csv_export_agent import CSVExportAgent, ExportOptions
            self.logger.info("📊 Exporting final CSV results...")

            csv_agent = CSVExportAgent(audit_logger=self.audit_logger)
            # The CSV agent's _load_artifact_data method is robust enough to handle
            # the artifact_client from the pipeline directly.
            csv_agent.artifact_storage = self.artifact_client

            export_options = ExportOptions(
                include_calculated_metrics=True,
                include_metadata=True,
                export_format="standard"
            )

            # The CSV agent writes to a directory, so we create a temporary one.
            # The artifacts are stored in the content-addressable storage, not kept on disk.
            with tempfile.TemporaryDirectory() as temp_dir:
                # The CSV agent needs the raw *scores* data, not just the hash.
                # It re-loads artifacts internally, so we pass hashes.
                scores_data = self.artifact_client.get_artifact(request.scores_artifact_hash)
                
                # The agent's `export_final_synthesis_data` expects artifact hashes
                # and loads them itself. We pass the hashes it needs.
                csv_result = csv_agent.export_final_synthesis_data(
                    scores_hash=request.scores_artifact_hash,
                    evidence_hash=request.evidence_artifact_hash,
                    # We pass the raw results directly to avoid re-loading the artifact we just created.
                    # The CSV agent is designed to handle this.
                    statistical_results_hash=statistical_results_hash,
                    curated_evidence_hash="",  # Not generated in this pipeline
                    framework_config={"name": self._extract_framework_name(request.framework_spec), "version": "v7.3"},
                    corpus_manifest=request.corpus_manifest or {},
                    synthesis_metadata={
                        "pipeline_version": "v2.0",
                        # Pass the raw results directly to the export agent
                        "statistical_results_raw": statistical_results_raw,
                        "scores_data_raw": json.loads(scores_data.decode('utf-8'))
                    },
                    export_path=temp_dir,
                    export_options=export_options
                )

                if csv_result.success:
                    self.logger.info(f"✅ CSV export successful: {len(csv_result.files_created)} files created in temp dir.")
                    for filename in csv_result.files_created:
                        filepath = os.path.join(temp_dir, filename)
                        with open(filepath, 'r', encoding='utf-8') as f:
                            csv_content = f.read()
                            csv_hash = self._store_artifact_with_metadata(
                                csv_content, f"csv_export_{filename}", "export", [statistical_results_hash]
                            )
                            self.logger.info(f"-> Stored CSV artifact: {filename} ({len(csv_content)} bytes) -> {csv_hash}")
                else:
                    self.logger.warning(f"⚠️ CSV export failed: {csv_result.error_message}")

        except Exception as e:
            self.logger.error(f"❌ Unhandled error during CSV export: {str(e)}", exc_info=True)

    def _run_statistical_analysis(self, request: ProductionPipelineRequest) -> Dict[str, Any]:
        """Helper to run the statistical analysis using MathToolkit."""
        combined_data = self.artifact_client.get_artifact(request.scores_artifact_hash)
        raw_analysis_data = combined_data.decode('utf-8')

        # This will be replaced by an AnalysisPlanner agent in the future.
        # For now, we use a default plan with CFF dimensional score columns.
        score_columns = [
            "tribal_dominance_score", "individual_dignity_score", "fear_score", "hope_score",
            "envy_score", "compersion_score", "enmity_score", "amity_score", 
            "fragmentative_goals_score", "cohesive_goals_score"
        ]
        
        analysis_plan = {
            "tasks": {
                "descriptives": {"tool": "calculate_descriptive_stats", "parameters": {"columns": score_columns}},
                "correlations": {"tool": "calculate_pearson_correlation", "parameters": {"columns": score_columns, "min_columns": 2}},
                "derived_metrics": {"tool": "calculate_derived_metrics", "parameters": {"input_columns": score_columns}}
            }
        }
        
        framework_calculation_spec = None
        try:
            # Safely extract calculation_spec from framework appendix
            json_pattern = r"```json\s*(.*?)\s*```"
            json_match = re.search(json_pattern, request.framework_spec, re.DOTALL)
            if json_match:
                framework_config = json.loads(json_match.group(1))
                framework_calculation_spec = framework_config.get("calculation_spec")
        except Exception:
            self.logger.warning("Could not parse framework_calculation_spec from framework. Proceeding without it.")

        return execute_analysis_plan_thin(raw_analysis_data, analysis_plan, request.corpus_manifest, framework_calculation_spec)
        
    def _extract_framework_name(self, framework_spec: str) -> str:
        """Extract framework name from framework specification."""
        try:
            # Look for title in markdown format
            lines = framework_spec.split('\n')
            for line in lines:
                if line.startswith('# ') or line.startswith('## '):
                    return line.strip('#').strip()
            
            # Fallback: look for framework name in JSON metadata
            import re
            json_pattern = r"```json\s*(.*?)\s*```"
            json_match = re.search(json_pattern, framework_spec, re.DOTALL)
            if json_match:
                framework_config = json.loads(json_match.group(1))
                return framework_config.get('name', 'Unknown Framework')
        except:
            pass
        return 'Unknown Framework'
        
    def _build_rag_index(self, request: ProductionPipelineRequest):
        """Helper to build the RAG index with required artifacts for the ComprehensiveKnowledgeCurator."""
        
        # Artifacts to be indexed by the curator.
        # Note: We only index lookup-oriented data (evidence, corpus), not context data.
        artifacts_to_index = {}
        if request.corpus_artifact_hash:
            artifacts_to_index['corpus'] = self.artifact_client.get_artifact(request.corpus_artifact_hash)
        if request.evidence_artifact_hash:
            artifacts_to_index['evidence'] = self.artifact_client.get_artifact(request.evidence_artifact_hash)
        
        if not artifacts_to_index:
            self.logger.warning("No corpus or evidence artifacts provided to build RAG index. Synthesis may be impaired.")
            return

        index_request = ComprehensiveIndexRequest(
            run_id=request.scores_artifact_hash,
            experiment_context=request.experiment_context,
            framework_spec=request.framework_spec,
            experiment_artifacts=artifacts_to_index
        )
        self.knowledge_curator.build_comprehensive_index(index_request)

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
                "sequential_synthesis_agent": "v2.0",
                "comprehensive_knowledge_curator": "v2.0", 
                "math_toolkit": "v2.0"
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

    def _json_serializer(self, obj):
        """Custom JSON serializer for pandas/numpy data types."""
        import numpy as np
        import pandas as pd
        
        # Handle numpy data types
        if isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, pd.Series):
            return obj.to_dict()
        elif isinstance(obj, pd.DataFrame):
            return obj.to_dict('records')
        elif isinstance(obj, (pd.Timestamp, datetime)):
            return obj.isoformat()
        elif hasattr(obj, 'item'):  # Handle other numpy scalars
            return obj.item()
        
        # For unhandled types, return string representation as a fallback
        try:
                    return str(obj)
        except Exception:
            return f"<unserializable: {type(obj).__name__}>" 