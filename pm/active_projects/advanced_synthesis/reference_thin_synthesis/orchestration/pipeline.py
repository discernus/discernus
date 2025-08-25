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
from ...deprecated.txtai_evidence_curator.agent import TxtaiEvidenceCurator, TxtaiCurationRequest
from ...comprehensive_knowledge_curator.agent import ComprehensiveKnowledgeCurator, ComprehensiveIndexRequest, KnowledgeQuery
from ...sequential_synthesis.agent import SequentialSynthesisAgent, SynthesisRequest, SynthesisResponse
from ...reliability_analysis_agent import ReliabilityAnalysisAgent
from ....core.math_toolkit import execute_analysis_plan_thin
from ....core.statistical_formatter import StatisticalResultsFormatter
from ....gateway.llm_gateway import LLMGateway
from ....gateway.model_registry import ModelRegistry


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
    
    # Cost information
    total_cost_usd: float = 0.0
    total_tokens: int = 0
    
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
        self.llm_gateway = LLMGateway(ModelRegistry())

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
            gasket_schema = self._extract_gasket_schema(request.framework_spec)
            statistical_results_raw, sample_size = self._run_statistical_analysis(request, gasket_schema)
            
            # Step 1.5: Validate statistical health
            self.logger.info("🔍 Validating statistical health...")
            self._validate_statistical_health(statistical_results_raw, sample_size)
            
            statistical_results_hash = self._store_artifact_with_metadata(
                json.dumps(statistical_results_raw, default=self._json_serializer), 
                "statistical_results",
                "statistical_analysis",
                dependencies=[request.scores_artifact_hash]
            )

            # Use the new formatter to prepare stats for the LLM
            formatter = StatisticalResultsFormatter(statistical_results_raw)
            statistical_results_formatted = formatter.format_all()

            # Optional: add confidence summary if available in raw scores
            try:
                # Attempt to extract a confidence summary from the original scores
                # The raw analysis JSON is not directly accessible here; rely on cached CSV-derived data not available.
                # As a compromise, pass through any existing confidence summary if MathToolkit adds it in future.
                pass
            except Exception:
                pass

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
            
            total_time = time.time() - start_time
            
            # Ensure all costs are flushed to the cost log before generating the report
            time.sleep(0.1)  # Small delay to ensure file I/O is complete
            
            provenance_metadata = {
                'run_id': request.scores_artifact_hash[:16] if request.scores_artifact_hash else 'unknown',
                'framework_hash': request.framework_hash,
                'corpus_hash': request.corpus_hash,
                'scores_hash': request.scores_artifact_hash,
                'execution_time': total_time
            }
            
            # Get real cost data from audit logger
            session_costs = self.audit_logger.get_session_costs() if self.audit_logger else {}
            cost_metadata = {
                'total_cost': session_costs.get('total_cost_usd', 0.0),
                'total_tokens': session_costs.get('total_tokens', 0),
                'models': session_costs.get('models', {}),
                'agents': session_costs.get('agents', {})
            }
            
            # Extract experiment name from framework or use fallback
            experiment_name = self._extract_experiment_name(request)
            
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
                error_message="",
                total_cost_usd=cost_metadata.get('total_cost', 0.0),
                total_tokens=cost_metadata.get('total_tokens', 0)
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
                error_message=str(e),
                total_cost_usd=0.0,
                total_tokens=0
            )

    def _extract_gasket_schema(self, framework_spec: str) -> Dict[str, Any]:
        """
        Extracts the gasket_schema from the framework specification using proprietary markers.
        
        Args:
            framework_spec: The framework specification content.
            
        Returns:
            The gasket_schema dictionary.
            
        Raises:
            ValueError: If the gasket_schema is not found or is invalid.
        """
        # 🎯 V8.0 SYNTHESIS BYPASS: Skip gasket extraction for v8.0 frameworks
        if ('v8.0' in str(framework_spec) or 'cff_v8' in str(framework_spec) or 
            'version: 8.0' in str(framework_spec) or 'Version 8.0' in str(framework_spec)):
            print("🎯 V8.0 BYPASS: Skipping gasket schema extraction for v8.0 framework")
            return {"version": "8.0", "target_keys": [], "bypass": True}
            
        try:
            start_marker = "<GASKET_SCHEMA_START>"
            end_marker = "<GASKET_SCHEMA_END>"
            
            start_pos = framework_spec.find(start_marker)
            if start_pos == -1:
                raise ValueError("Gasket schema start marker not found in framework.")
                
            end_pos = framework_spec.find(end_marker, start_pos)
            if end_pos == -1:
                raise ValueError("Gasket schema end marker not found in framework.")
                
            # Extract content between markers and parse as JSON
            gasket_content = framework_spec[start_pos + len(start_marker):end_pos].strip()
            gasket_data = json.loads(gasket_content)
            
            # The gasket_schema is the top-level object
            if "gasket_schema" in gasket_data:
                return gasket_data["gasket_schema"]
            else:
                raise ValueError("gasket_schema key not found in the extracted content.")

        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse gasket_schema JSON: {e}")
            raise ValueError(f"Invalid gasket_schema JSON: {e}")
        except Exception as e:
            self.logger.error(f"Failed to extract gasket_schema: {e}")
            raise ValueError(f"Could not extract gasket_schema: {e}")

    def _extract_dimensions_from_gasket_schema(self, gasket_schema: Dict[str, Any]) -> List[str]:
        """
        Extracts the list of target keys from the gasket schema.
        
        Args:
            gasket_schema: The framework's gasket_schema.
            
        Returns:
            A list of score columns.
            
        Raises:
            ValueError: If the gasket_schema is invalid.
        """
        if not gasket_schema or 'target_keys' not in gasket_schema:
            raise ValueError("Invalid or missing gasket_schema with target_keys")
        
        self.logger.info(f"✅ Extracted {len(gasket_schema['target_keys'])} target keys from gasket_schema")
        return gasket_schema['target_keys']

    def _run_statistical_analysis(self, request: ProductionPipelineRequest, gasket_schema: Dict[str, Any]) -> tuple[Dict[str, Any], int]:
        """Helper to run the statistical analysis using MathToolkit."""
        combined_data = self.artifact_client.get_artifact(request.scores_artifact_hash)
        raw_analysis_data = combined_data.decode('utf-8')

        # THIN Principle: Dynamically discover score columns from the gasket_schema contract
        score_columns = self._extract_dimensions_from_gasket_schema(gasket_schema)
        
        # Sample-size aware statistical planning - check the data structure first
        try:
            # Try to determine sample size from the raw data
            raw_text = combined_data.decode('utf-8')
            if raw_text.startswith('[') or raw_text.startswith('{'):
                # JSON format - count top-level objects
                import json
                data_obj = json.loads(raw_text)
                if isinstance(data_obj, list):
                    sample_size = len(data_obj)
                elif isinstance(data_obj, dict) and 'documents' in data_obj:
                    sample_size = len(data_obj['documents'])
                else:
                    sample_size = 1  # Single document object
            else:
                # Try CSV format
                df_preview = pd.read_csv(BytesIO(combined_data))
                sample_size = len(df_preview)
        except Exception as e:
            self.logger.warning(f"Could not determine sample size, defaulting to 4: {e}")
            sample_size = 4  # Conservative fallback
        
        self.logger.info(f"📊 Sample size detected: N={sample_size}, adapting statistical analysis plan...")
        
        # Intelligent statistical planning based on sample size constraints
        analysis_tasks = {
            "descriptives": {"tool": "calculate_descriptive_stats", "parameters": {"columns": score_columns}}
        }
        
        if sample_size >= 10:
            # Sufficient for correlation analysis
            analysis_tasks["correlations"] = {"tool": "calculate_pearson_correlation", "parameters": {"columns": score_columns, "min_columns": 2}}
            self.logger.info("✅ Sample size adequate for correlation analysis")
        else:
            self.logger.info(f"⚠️ Sample size N={sample_size} insufficient for reliable correlation analysis (N≥10 recommended)")
            
        if sample_size >= 4:
            # Can calculate derived metrics for case studies
            analysis_tasks["derived_metrics"] = {"tool": "calculate_derived_metrics", "parameters": {"input_columns": score_columns}}
            
        analysis_plan = {"tasks": analysis_tasks}
        
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

        statistical_results = execute_analysis_plan_thin(
            raw_analysis_data=raw_analysis_data,
            analysis_plan_input=analysis_plan,
            llm_gateway=self.llm_gateway,
            model=self.analysis_model or self.synthesis_model,
            corpus_manifest=request.corpus_manifest,
            framework_calculation_spec=framework_calculation_spec,
        )
        
        return statistical_results, sample_size
    
    def _validate_statistical_health(self, statistical_results: Dict[str, Any], sample_size: int) -> None:
        """
        Validate statistical calculation health to detect data quality issues.
        
        Checks for:
        - High calculation failure rates (>50% failure rate fails experiment)
        - Perfect correlations indicating insufficient data
        - Statistical impossibilities or extreme values
        
        Args:
            statistical_results: Raw statistical results from MathToolkit
            sample_size: Number of documents in the analysis for context-aware validation
            
        Raises:
            Exception: If statistical health validation fails
        """
        try:
            # Initialize reliability analysis agent with Pro model for validation
            # Note: Statistical health validation requires higher intelligence than Flash Lite
            # TODO: Accept validation_model parameter from orchestrator
            reliability_agent = ReliabilityAnalysisAgent(
                model="vertex_ai/gemini-2.5-pro",  
                audit_logger=self.audit_logger
            )
            
            # Convert statistical results to JSON string for LLM analysis
            statistical_json = json.dumps(statistical_results, indent=2, default=self._json_serializer)
            
            # Validate statistical health with sample size context
            health_result = reliability_agent.validate_statistical_health(
                statistical_results=statistical_json,
                sample_size=sample_size,  # Pass sample size for context-aware validation
                analysis_type="case_study" if sample_size < 10 else "statistical"
            )
            
            # Log validation results
            self.audit_logger.log_agent_event(
                "ProductionThinSynthesisPipeline",
                "statistical_health_validation",
                {
                    "validation_passed": health_result.validation_passed,
                    "calculation_failures_count": len(health_result.calculation_failures),
                    "perfect_correlations_count": len(health_result.perfect_correlations),
                    "sample_size_assessment": health_result.sample_size_assessment,
                    "recommended_action": health_result.recommended_action
                }
            )
            
            # Handle validation results based on recommended action
            if health_result.recommended_action == "FAIL_EXPERIMENT":
                error_msg = (
                    f"Statistical health validation failed: {health_result.error_message or 'Critical statistical issues detected'}\n"
                    f"Calculation failures: {', '.join(health_result.calculation_failures) if health_result.calculation_failures else 'None'}\n"
                    f"Perfect correlations: {', '.join(health_result.perfect_correlations) if health_result.perfect_correlations else 'None'}\n"
                    f"Sample size: {health_result.sample_size_assessment}\n"
                    f"Statistical warnings: {'; '.join(health_result.statistical_warnings) if health_result.statistical_warnings else 'None'}"
                )
                self.logger.error(f"❌ {error_msg}")
                raise Exception(error_msg)
            
            elif health_result.recommended_action == "WARN_RESEARCHER":
                warning_msg = "Statistical health concerns detected but proceeding"
                if health_result.calculation_failures:
                    self.logger.warning(f"⚠️ Calculation failures: {', '.join(health_result.calculation_failures)}")
                if health_result.perfect_correlations:
                    self.logger.warning(f"⚠️ Perfect correlations detected: {', '.join(health_result.perfect_correlations)}")
                if health_result.statistical_warnings:
                    self.logger.warning(f"⚠️ Statistical warnings: {'; '.join(health_result.statistical_warnings)}")
                self.logger.warning(f"⚠️ Sample size assessment: {health_result.sample_size_assessment}")
                self.logger.info("✅ Statistical health validation passed with warnings")
            
            elif health_result.recommended_action == "PROCEED":
                self.logger.info("✅ Statistical health validation passed")
                if health_result.statistical_warnings:
                    self.logger.info(f"ℹ️ Minor statistical notes: {'; '.join(health_result.statistical_warnings)}")
            
        except Exception as e:
            # Always log the telemetry event for failures so telemetry system can track them
            self.audit_logger.log_agent_event(
                "ProductionThinSynthesisPipeline",
                "statistical_health_validation",
                {
                    "validation_passed": False,
                    "calculation_failures_count": 0,
                    "perfect_correlations_count": 0,
                    "sample_size_assessment": "unknown",
                    "recommended_action": "SYSTEM_ERROR",
                    "error_message": str(e)
                }
            )
            
            if "Statistical health validation failed" in str(e):
                # Re-raise validation failures
                raise
            else:
                # Log unexpected validation errors but don't fail the experiment
                error_msg = f"Statistical health validation system error: {str(e)}"
                self.logger.warning(f"⚠️ {error_msg}")
                self.audit_logger.log_error("statistical_health_validation_error", error_msg, {"stage": "synthesis_pipeline"})
                self.logger.warning("⚠️ Proceeding without statistical health validation due to system error")
        
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
    
    def _extract_experiment_name(self, request: ProductionPipelineRequest) -> str:
        """Extract experiment name from request context or framework."""
        try:
            # Try to get from framework specification first
            lines = request.framework_spec.split('\n')
            for line in lines:
                if 'experiment' in line.lower() and ('title' in line.lower() or 'name' in line.lower()):
                    # Extract after colon or similar
                    if ':' in line:
                        return line.split(':', 1)[1].strip()
            
            # Fallback: use a descriptive name based on framework
            framework_name = self._extract_framework_name(request.framework_spec)
            return f"{framework_name} Analysis Study"
        except:
            pass
        return 'Computational Discourse Analysis Study'
        
    def _build_rag_index(self, request: ProductionPipelineRequest):
        """Helper to build the RAG index with required artifacts for the ComprehensiveKnowledgeCurator."""
        
        # Artifacts to be indexed by the curator.
        # Note: Index evidence-only data for lookup; context (framework, corpus, stats) is passed directly.
        artifacts_to_index = {}
        if request.evidence_artifact_hash:
            artifacts_to_index['evidence'] = self.artifact_client.get_artifact(request.evidence_artifact_hash)
        
        if not artifacts_to_index:
            self.logger.warning("No evidence artifacts provided to build RAG index. Synthesis may be impaired.")
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