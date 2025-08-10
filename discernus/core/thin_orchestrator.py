#!/usr/bin/env python3
"""
THIN Orchestrator v2.0 for Discernus
====================================

THIN v2.0 orchestrator implementing direct function calls instead of Redis coordination.
Coordinates the simplified 2-agent pipeline: Enhanced Analysis → Enhanced Synthesis

Key THIN v2.0 principles:
- Direct Python function calls (no Redis coordination)
- LLM intelligence for complex reasoning
- Minimal software coordination
- Perfect caching through content-addressable storage
- Complete audit trails for academic integrity
"""

import json
import os
import time
import yaml
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
import hashlib # Added for framework hash calculation

from .security_boundary import ExperimentSecurityBoundary, SecurityError
from .audit_logger import AuditLogger
from .local_artifact_storage import LocalArtifactStorage
from .enhanced_manifest import EnhancedManifest
from .provenance_organizer import ProvenanceOrganizer
from ..agents.EnhancedAnalysisAgent.main import EnhancedAnalysisAgent
from ..agents.intelligent_extractor_agent import IntelligentExtractorAgent
from ..agents.csv_export_agent import CSVExportAgent, ExportOptions
from ..gateway.llm_gateway import LLMGateway
from ..gateway.model_registry import ModelRegistry

# Import THIN Synthesis Pipeline for enhanced synthesis
from ..agents.thin_synthesis.orchestration.pipeline import (
    ProductionThinSynthesisPipeline, 
    ProductionPipelineRequest,
    ProductionPipelineResponse
)


class ThinOrchestratorError(Exception):
    """THIN orchestrator specific exceptions"""
    pass


class ThinOrchestrator:
    """
    THIN v2.0 orchestrator implementing direct function call coordination.
    
    Simplified 2-agent pipeline:
    1. Enhanced Analysis Agent (with mathematical validation)
    2. Enhanced Synthesis Agent (with mathematical spot-checking)
    
    Key features:
    - Direct function calls (no Redis)
    - Security boundary enforcement
    - Complete audit trails
    - Perfect caching for restart=resume
    - Enhanced mathematical validation
    """
    
    def __init__(self, experiment_path: Path):
        """
        Initialize THIN orchestrator for an experiment.
        
        Args:
            experiment_path: Path to experiment directory (containing experiment.md)
        """
        self.experiment_path = Path(experiment_path).resolve()
        
        # Initialize security boundary
        self.security = ExperimentSecurityBoundary(self.experiment_path)
        
        # Initialize LLM gateway for THIN-compliant framework validation
        self.model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(self.model_registry)
        
        print(f"🎯 THIN Orchestrator v2.0 initialized for: {self.security.experiment_name}")
    
    def _check_framework_compatibility_with_llm(self, current_framework: str, cached_framework: str, cached_artifact_id: str, audit_logger: Optional[AuditLogger] = None) -> Dict[str, Any]:
        """
        THIN-compliant framework compatibility check using LLM intelligence.
        
        Replaces rigid hash-based matching with semantic analysis.
        
        Args:
            current_framework: Current framework content
            cached_framework: Previously cached framework content
            cached_artifact_id: ID of cached artifact for logging
            
        Returns:
            Dict containing compatibility decision and reasoning
        """
        compatibility_prompt = f"""You are a research methodology expert evaluating framework compatibility for computational text analysis.

CURRENT FRAMEWORK:
{current_framework[:2000]}{'...' if len(current_framework) > 2000 else ''}

CACHED FRAMEWORK (from artifact {cached_artifact_id[:12]}...):
{cached_framework[:2000]}{'...' if len(cached_framework) > 2000 else ''}

TASK: Determine if analysis artifacts from the cached framework can be safely reused with the current framework.

EVALUATION CRITERIA:
- Same analytical dimensions (names and definitions)
- Same scoring methodology (scale, criteria)
- Same research intent and theoretical foundation
- Minor differences (formatting, typos, examples) should be COMPATIBLE
- Major differences (new dimensions, different scales, different theory) should be INCOMPATIBLE

RESPONSE FORMAT (JSON only):
{{
    "compatibility": "COMPATIBLE" | "INCOMPATIBLE" | "PARTIAL",
    "confidence": 0.0-1.0,
    "reasoning": "Brief explanation of decision",
    "differences_found": ["list", "of", "key", "differences"],
    "reuse_recommendation": "FULL" | "NONE" | "PARTIAL"
}}

Respond with only the JSON object."""

        try:
            response_content, metadata = self.llm_gateway.execute_call(
                model="vertex_ai/gemini-2.5-flash",
                prompt=compatibility_prompt,
                max_tokens=1000
            )
            
            if audit_logger and metadata.get('success') and 'usage' in metadata:
                usage = metadata['usage']
                audit_logger.log_cost(
                    operation="framework_validation",
                    model="vertex_ai/gemini-2.5-flash",
                    tokens_used=usage.get('total_tokens', 0),
                    cost_usd=usage.get('response_cost_usd', 0.0),
                    agent_name="ThinOrchestrator",
                    metadata={
                        "prompt_tokens": usage.get('prompt_tokens', 0),
                        "completion_tokens": usage.get('completion_tokens', 0),
                        "validation_type": "semantic_compatibility"
                    }
                )
            
            if not metadata.get('success'):
                return {
                    "compatibility": "INCOMPATIBLE",
                    "confidence": 0.0,
                    "reasoning": f"LLM compatibility check failed: {metadata.get('error', 'unknown error')}",
                    "differences_found": ["LLM_CALL_FAILED"],
                    "reuse_recommendation": "NONE"
                }
            
            import json
            import re
            json_match = re.search(r'\{.*\}', response_content, re.DOTALL)
            if json_match:
                compatibility_result = json.loads(json_match.group())
                required_fields = ["compatibility", "confidence", "reasoning", "reuse_recommendation"]
                if all(field in compatibility_result for field in required_fields):
                    return compatibility_result
            
            return {
                "compatibility": "INCOMPATIBLE", 
                "confidence": 0.0,
                "reasoning": "Failed to parse LLM compatibility response",
                "differences_found": ["PARSING_FAILED"],
                "reuse_recommendation": "NONE"
            }
            
        except Exception as e:
            return {
                "compatibility": "INCOMPATIBLE",
                "confidence": 0.0, 
                "reasoning": f"Framework compatibility check failed: {str(e)}",
                "differences_found": ["EXCEPTION_OCCURRED"],
                "reuse_recommendation": "NONE"
            }
        
    def _create_thin_synthesis_pipeline(self, model: str, audit: AuditLogger, storage: LocalArtifactStorage) -> "ProductionThinSynthesisPipeline":
        """Factory method to create the synthesis pipeline."""
        return ProductionThinSynthesisPipeline(
            artifact_client=storage,
            audit_logger=audit,
            model=model,
            analysis_model=self._current_analysis_model,
        )

    def _run_thin_synthesis(self,
                            pipeline: "ProductionThinSynthesisPipeline",
                            framework_content: str,
                           scores_hash: str,
                           evidence_hash: str,
                            corpus_hash: str,
                           experiment_config: Dict[str, Any],
                            corpus_manifest: Dict[str, Any],
                           framework_hash: str,
                            corpus_content_hash: str) -> "ProductionPipelineResponse":
        """Executes the THIN synthesis pipeline and returns the response."""
        request = ProductionPipelineRequest(
            framework_spec=framework_content,
            scores_artifact_hash=scores_hash,
            evidence_artifact_hash=evidence_hash,
            corpus_artifact_hash=corpus_content_hash,
            experiment_context=json.dumps(experiment_config.get("context", {})),
            framework_hash=framework_hash,
            corpus_hash=corpus_hash, # This is the manifest hash
            framework_name=experiment_config.get("name"),
            corpus_manifest=corpus_manifest,
        )
        return pipeline.run(request)

    def run_experiment(self, 
                      analysis_model: str = "vertex_ai/gemini-2.5-flash-lite",
                      synthesis_model: str = "vertex_ai/gemini-2.5-pro",
                      ensemble_runs: int = 1,
                      auto_commit: bool = True,
                      debug_agent: Optional[str] = None,
                      debug_level: str = "info") -> Dict[str, Any]:
        """
        Run experiment with a unified, linear pipeline to ensure complete provenance.
        
        Args:
            analysis_model: LLM model to use for analysis
            synthesis_model: LLM model to use for synthesis
            ensemble_runs: Number of ensemble runs for self-consistency (1 = single run)
            auto_commit: If True, automatically commit successful runs to Git (default: True)
            
        Returns:
            Experiment results with complete provenance and artifacts.
        """
        start_time = datetime.now(timezone.utc).isoformat()
        
        run_timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        run_folder = self.experiment_path / "runs" / run_timestamp
        
        try:
            # STAGE 0: SETUP
            # ==================================================================
            self.security.secure_mkdir(run_folder)
            audit = AuditLogger(self.security, run_folder)
            shared_cache_dir = self.experiment_path / "shared_cache"
            self.security.secure_mkdir(shared_cache_dir)
            storage = LocalArtifactStorage(self.security, shared_cache_dir, run_timestamp)
            manifest = EnhancedManifest(self.security, run_folder, audit, storage)
            
            audit.log_orchestrator_event("experiment_start", {
                "experiment_path": str(self.experiment_path),
                "run_folder": str(run_folder),
                "analysis_model": analysis_model,
                "synthesis_model": synthesis_model,
                "architecture": "thin_v2.1_unified"
            })
            
            print(f"🚀 Starting THIN v2.1 unified experiment: {run_timestamp}")

            # STAGE 1: LOAD INPUTS
            # ==================================================================
            experiment_config = self._load_experiment_config()
            manifest.set_run_metadata(
                experiment_config["name"], 
                str(self.experiment_path),
                "thin_v2.1_unified"
            )
            manifest.set_experiment_config(experiment_config)
            
            framework_content = self._load_framework(experiment_config["framework"])
            self._current_framework_content = framework_content
            self._current_audit_logger = audit
            self._current_analysis_model = analysis_model
            
            framework_hash = storage.put_artifact(
                framework_content.encode('utf-8'),
                {"artifact_type": "framework", "original_filename": experiment_config["framework"]}
            )
            manifest.add_input_artifact("framework", framework_hash, {"filename": experiment_config["framework"]})
            
            corpus_documents, corpus_manifest = self._load_corpus(experiment_config["corpus_path"])
            corpus_manifest['manifest_hash'] = hashlib.sha256(json.dumps(corpus_manifest).encode('utf-8')).hexdigest()
            print(f"DEBUG: corpus_documents loaded: {len(corpus_documents)} documents")
            print(f"DEBUG: corpus_manifest: {corpus_manifest}")
            corpus_hashes = [storage.put_artifact(doc["content"].encode('utf-8'), {"artifact_type": "corpus_document", "original_filename": doc["filename"]}) for doc in corpus_documents]
            manifest.add_corpus_artifacts(corpus_hashes, [{"filename": doc["filename"]} for doc in corpus_documents])
            
            audit.log_orchestrator_event("inputs_loaded", {"framework_hash": framework_hash, "corpus_documents": len(corpus_documents)})

            # STAGE 2: ANALYSIS
            print(f"📊 STAGE 2: ANALYSIS - Processing {len(corpus_documents)} documents...")
                analysis_agent = EnhancedAnalysisAgent(self.security, audit, storage)
                all_analysis_results, scores_hash, evidence_hash, corpus_hash = self._execute_analysis_sequentially(
                analysis_agent, corpus_documents, framework_content, experiment_config, analysis_model, ensemble_runs
            )
            
                analysis_costs = audit.get_session_costs()
                successful_count = len([res for res in all_analysis_results if res.get('analysis_result', {}).get('result_hash')])
            if not successful_count:
                raise ThinOrchestratorError("Analysis failed completely. No artifacts were generated.")

            print(f"✅ Analysis complete: {successful_count}/{len(corpus_documents)} processed. Cost: ${analysis_costs.get('total_cost_usd', 0.0):.4f}")
            manifest.add_execution_stage("analysis", "EnhancedAnalysisAgent", start_time, datetime.now(timezone.utc).isoformat(), "completed", {"model": analysis_model})

            # STAGE 3: SYNTHESIS
            print(f"🔬 STAGE 3: SYNTHESIS - Generating comprehensive report...")
            synthesis_start_time = datetime.now(timezone.utc).isoformat()
            
            synthesis_pipeline = self._create_thin_synthesis_pipeline(synthesis_model, audit, storage)
            synthesis_response = self._run_thin_synthesis(
                synthesis_pipeline, framework_content, scores_hash, evidence_hash,
                corpus_hash, experiment_config, corpus_manifest, framework_hash,
                corpus_content_hash=corpus_hash
            )

            if not synthesis_response.success:
                raise ThinOrchestratorError(f"THIN Synthesis failed: {synthesis_response.error_message}")

            print(f"✅ Synthesis complete: {synthesis_response.word_count} words generated.")
            manifest.add_execution_stage("synthesis", "ProductionThinSynthesisPipeline", synthesis_start_time, datetime.now(timezone.utc).isoformat(), "completed", {"model": synthesis_model, "report_hash": synthesis_response.dual_purpose_report_hash})

            # STAGE 4: FINALIZATION & EXPORT
            print("📦 STAGE 4: FINALIZATION - Exporting results and organizing provenance...")
                results_dir = run_folder / "results"
                self.security.secure_mkdir(results_dir)
                
            export_result = self._export_final_synthesis_csv_files(
                scores_hash,
                evidence_hash,
                synthesis_response.statistical_results_hash,
                framework_content,
                experiment_config,
                corpus_manifest,
                results_dir,
                audit
            )
            if not export_result.get('success'):
                 audit.log_error("csv_export_failed", export_result.get('error_message', 'Unknown error'), {})

                    provenance_organizer = ProvenanceOrganizer(self.security, audit)
            provenance_organizer.organize_run_artifacts(run_folder, shared_cache_dir, {"experiment_name": experiment_config.get("name"), "run_timestamp": run_timestamp})

            manifest.finalize_manifest()

            if auto_commit:
                self._auto_commit_run(run_folder, {"run_id": run_timestamp, "experiment_name": self.experiment_path.name}, audit)
            
                end_time = datetime.now(timezone.utc).isoformat()
                session_costs = audit.get_session_costs()
                
            print(f"🎉 Experiment run {run_timestamp} completed successfully!")
                return {
                    "run_id": run_timestamp,
                    "status": "completed",
                "final_report_hash": synthesis_response.dual_purpose_report_hash,
                    "duration": self._calculate_duration(start_time, end_time),
                    "costs": session_costs,
            }

        except (ThinOrchestratorError, SecurityError) as e:
            print(f"❌ Experiment failed: {str(e)}")
            if 'manifest' in locals():
                manifest.finalize_manifest()
            raise
        except Exception as e:
            print(f"💥 An unexpected error occurred: {str(e)}")
            if 'manifest' in locals():
                manifest.finalize_manifest()
            if 'audit' in locals():
                audit.log_error("unexpected_orchestrator_failure", str(e), {})
            raise ThinOrchestratorError(f"Unexpected orchestrator failure: {e}") from e

    def _export_final_synthesis_csv_files(self, scores_hash: str, evidence_hash: str, statistical_results_hash: str, framework_content: str, experiment_config: Dict[str, Any], corpus_manifest: Dict[str, Any], results_dir: Path, audit: AuditLogger) -> Dict[str, Any]:
        """Exports all final CSVs including scores, evidence, and statistical results."""
        try:
            csv_agent = CSVExportAgent(audit_logger=audit)
            csv_agent.artifact_storage = LocalArtifactStorage(self.security, self.experiment_path / "shared_cache", "export")
            
            framework_config = self._parse_framework_config(framework_content)

            export_options = ExportOptions(include_calculated_metrics=True, include_metadata=True)
            
            result = csv_agent.export_final_synthesis_data(
                scores_hash=scores_hash,
                evidence_hash=evidence_hash,
                statistical_results_hash=statistical_results_hash,
                curated_evidence_hash="",
                framework_config=framework_config,
                corpus_manifest=corpus_manifest,
                synthesis_metadata={},
                export_path=str(results_dir),
                export_options=export_options
            )
            
            if result.success:
                print(f"✅ CSV Export successful: {len(result.files_created)} files created in {results_dir}")
                audit.log_agent_event("CSVExportAgent", "export_final_synthesis_data", {"files": result.files_created})
                else:
                print(f"⚠️ CSV Export failed: {result.error_message}")
                audit.log_error("csv_export_failed", result.error_message, {})
                    
            return {"success": result.success, "files": result.files_created, "error_message": result.error_message}
            except Exception as e:
            print(f"💥 Unhandled error during final CSV export: {e}")
            audit.log_error("csv_export_unhandled_error", str(e), {})
            return {"success": False, "error_message": str(e)}

    def _execute_analysis_sequentially(self,
                                       analysis_agent: EnhancedAnalysisAgent,
                                       corpus_documents: List[Dict[str, Any]],
                                       framework_content: str,
                                       experiment_config: Dict[str, Any],
                                       model: str,
                                       ensemble_runs: int = 1) -> tuple[List[Dict[str, Any]], Optional[str], Optional[str], Optional[str]]:
        """
        Executes the analysis agent for each document.
        """
        all_analysis_results = []
        
        print(f"\n🚀 Starting sequential analysis of {len(corpus_documents)} documents...")
        
        for i, doc in enumerate(corpus_documents):
            print(f"\n--- Analyzing document {i+1}/{len(corpus_documents)}: {doc.get('filename')} ---")
            
            try:
                result = analysis_agent.analyze_batch(
                    framework_content=framework_content,
                    corpus_documents=[doc],
                    experiment_config=experiment_config,
                    model=model,
                    current_scores_hash=None,
                    current_evidence_hash=None
                )
                
                all_analysis_results.append(result)
            except Exception as e:
                print(f"❌ Analysis failed for document {doc.get('filename')}: {e}")
                all_analysis_results.append({"error": str(e), "document": doc.get('filename')})

        scores_hash, evidence_hash = self._combine_analysis_artifacts(all_analysis_results, analysis_agent.storage)
        
        corpus_content = "\n\n---\n\n".join([doc.get('content', '') for doc in corpus_documents])
        corpus_hash = analysis_agent.storage.put_artifact(
            corpus_content.encode('utf-8'),
            {"artifact_type": "combined_corpus_text"}
        )
        
        return all_analysis_results, scores_hash, evidence_hash, corpus_hash

    def _combine_analysis_artifacts(self, analysis_results: List[Dict[str, Any]], storage) -> tuple[str, str]:
        """
        Combine analysis results from multiple documents into a single result.
        """
        import json
        
        combined_document_analyses = []
        all_evidence = []
        
        for i, result in enumerate(analysis_results):
            if not result or "error" in result:
                continue
                
            if "analysis_result" in result and "result_content" in result["analysis_result"]:
                cached_result = result["analysis_result"]["result_content"]
                
                if "raw_analysis_response" in cached_result:
                    raw_response = cached_result["raw_analysis_response"]
                    
                    if "evidence_hash" in cached_result:
                        evidence_hash = cached_result["evidence_hash"]
                        try:
                            evidence_artifact_data = storage.get_artifact(evidence_hash)
                            if evidence_artifact_data:
                                evidence_artifact = json.loads(evidence_artifact_data.decode('utf-8'))
                                evidence_list = evidence_artifact.get("evidence_data", [])
                                all_evidence.extend(evidence_list)
                        except Exception as e:
                            print(f"Warning: Failed to load evidence artifact for analysis {i}: {e}")
                    
                    framework_content = getattr(self, '_current_framework_content', None)
                    if framework_content:
                        extracted_data = self._extract_and_map_with_gasket(
                            raw_response, 
                            framework_content, 
                            getattr(self, '_current_audit_logger', None),
                            getattr(self, '_current_analysis_model', 'vertex_ai/gemini-2.5-flash-lite')
                        )
                    else:
                        extracted_data = self._legacy_json_parsing(raw_response)
                    
                    if extracted_data and "document_analyses" in extracted_data:
                        combined_document_analyses.extend(extracted_data["document_analyses"])
        
        combined_result = {
            "analysis_metadata": {
                "framework_name": "combined_analysis", "framework_version": "v6.0", "analyst_confidence": 0.85,
                "analysis_notes": f"Combined analysis of {len(combined_document_analyses)} documents"
            },
            "document_analyses": combined_document_analyses
        }
        
        evidence_artifact = {
            "evidence_metadata": {
                "total_documents": len(combined_document_analyses), "total_evidence_pieces": len(all_evidence),
                "extraction_method": "analysis_time_combination_v1.0", "extraction_time": datetime.now(timezone.utc).isoformat(),
                "framework_version": "v6.0"
            },
            "evidence_data": all_evidence
        }
        
        evidence_hash = storage.put_artifact(
            json.dumps(evidence_artifact, indent=2).encode('utf-8'),
            {
                "artifact_type": "combined_evidence_v6", "extraction_method": "analysis_time_combination",
                "total_evidence_pieces": len(all_evidence), "total_documents": len(combined_document_analyses)
            }
        )
        
        combined_result_hash = storage.put_artifact(
            json.dumps(combined_result, indent=2).encode('utf-8'),
            {
                "artifact_type": "combined_analysis_v6", "total_documents": len(combined_document_analyses),
                "framework_version": "v6.0"
            }
        )
        
        return combined_result_hash, evidence_hash

    def _extract_gasket_schema_from_framework(self, framework_content: str) -> Optional[Dict[str, Any]]:
        """
        Extract gasket_schema from framework v7.1 JSON appendix.
        """
        try:
            if 'gasket_schema' in framework_content:
                gasket_pos = framework_content.find('gasket_schema')
                
                start_pos = 0
                while True:
                    json_start_marker = framework_content.find('```json', start_pos)
                    if json_start_marker == -1:
                        break
                    
                    json_start = json_start_marker + 7
                    json_end = framework_content.find('```', json_start)
                    
                    if json_end != -1:
                        json_content = framework_content[json_start:json_end].strip()
                        
                        if json_start <= gasket_pos <= json_end:
                            try:
                                framework_config = json.loads(json_content)
                                
                                gasket_schema = framework_config.get('gasket_schema')
                                if gasket_schema:
                                    supported_versions = ['7.1', '7.3', 'v7.1', 'v7.3']
                                    if gasket_schema.get('version') in supported_versions and 'target_keys' in gasket_schema:
                                        return gasket_schema
                                    else:
                                        print(f"❌ Unsupported gasket_schema version: {gasket_schema.get('version')}. Supported versions: {supported_versions}")
                                        return None
                            except json.JSONDecodeError:
                                pass
                    
                    start_pos = json_end + 3 if json_end != -1 else json_start_marker + 7
            
            return None
            
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Warning: Failed to extract gasket_schema from framework: {e}")
            return None

    def _convert_v71_gasket_to_v70(self, v71_schema: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Convert v7.1 enhanced gasket schema to v7.0 format.
        """
        try:
            extraction_targets = v71_schema.get('extraction_targets', {})
            
            target_keys = []
            
            core_scores = extraction_targets.get('core_scores', {})
            target_keys.extend(core_scores.keys())
            
            metadata_scores = extraction_targets.get('metadata_scores', {})
            target_keys.extend(metadata_scores.keys())
            
            target_dimensions = []
            for score_key, score_config in {**core_scores, **metadata_scores}.items():
                description = score_config.get('description', score_key)
                target_dimensions.append(description)
            
            v70_schema = {
                'target_keys': target_keys,
                'target_dimensions': target_dimensions,
                'version': '7.1_converted',
                'conversion_source': 'v7.1_enhanced'
            }
            
            print(f"✅ Converted v7.1 gasket schema: {len(target_keys)} target keys")
            return v70_schema
            
        except Exception as e:
            print(f"❌ Failed to convert v7.1 gasket schema: {e}")
            return None

    def _extract_and_map_with_gasket(
        self,
        raw_analysis_response: str,
        framework_content: str,
        audit_logger: AuditLogger,
        model: str = "vertex_ai/gemini-2.5-flash-lite"
    ) -> Optional[Dict[str, Any]]:
        """
        Extract scores using Intelligent Extractor gasket.
        """
        gasket_schema = self._extract_gasket_schema_from_framework(framework_content)
        
        if not gasket_schema:
            print("❌ No valid gasket_schema found in framework")
            print(f"🔍 Framework content length: {len(framework_content)}")
            print(f"🔍 Contains ```json: {'```json' in framework_content}")
            raise ValueError("Framework must have valid gasket_schema (v7.1 or v7.3). No backward compatibility with v7.0 or earlier.")
        
        document_evidence_list = self._extract_evidence_from_delimited(raw_analysis_response)
        
        extractor = IntelligentExtractorAgent(
            model=model,
            audit_logger=audit_logger
        )
        
        extraction_result = extractor.extract_scores_from_raw_analysis(
            raw_analysis_response, gasket_schema
        )
        
        if not extraction_result.success:
            print(f"❌ Intelligent Extractor failed: {extraction_result.error_message}")
            raise ValueError(f"v7.1 Intelligent Extractor failed: {extraction_result.error_message}. No legacy fallback available.")
        
        if "_document_analyses" in extraction_result.extracted_scores:
            document_analyses_data = extraction_result.extracted_scores["_document_analyses"]
            
            document_analyses = []
            for doc_data in document_analyses_data:
                doc_name = doc_data["document_name"]
                doc_evidence = [ev for ev in document_evidence_list if ev.get("document_name") == doc_name]
                
                document_analysis = {
                    "document_id": "extracted_via_gasket",
                    "document_name": doc_data["document_name"],
                    "analysis_scores": doc_data["analysis_scores"],
                    "evidence": doc_evidence,
                    "extraction_metadata": {
                        "extraction_time_seconds": extraction_result.extraction_time_seconds,
                        "tokens_used": extraction_result.tokens_used,
                        "cost_usd": extraction_result.cost_usd,
                        "attempts": extraction_result.attempts,
                        "gasket_version": "v7.1",
                        "document_identity_preserved": True
                    }
                }
                document_analyses.append(document_analysis)
            
            return {
                "document_analyses": document_analyses,
                "analysis_metadata": {
                    "framework_name": "gasket_extracted",
                    "framework_version": "v7.1",
                    "analyst_confidence": 0.95,
                    "analysis_notes": f"Extracted via Intelligent Extractor in {extraction_result.attempts} attempts, preserving {len(document_analyses)} document identities with evidence"
                }
            }
        else:
            document_analysis = {
                "document_id": "extracted_via_gasket",
                "document_name": "gasket_extraction",
                "analysis_scores": extraction_result.extracted_scores,
                "evidence": document_evidence_list,
                "extraction_metadata": {
                    "extraction_time_seconds": extraction_result.extraction_time_seconds,
                    "tokens_used": extraction_result.tokens_used,
                    "cost_usd": extraction_result.cost_usd,
                    "attempts": extraction_result.attempts,
                    "gasket_version": "v7.1"
                }
            }
            
            return {
                "document_analyses": [document_analysis],
                "analysis_metadata": {
                    "framework_name": "gasket_extracted",
                    "framework_version": "v7.1",
                    "analyst_confidence": 0.95,
                    "analysis_notes": f"Extracted via Intelligent Extractor in {extraction_result.attempts} attempts with evidence"
                }
            }

    def _legacy_json_parsing(self, raw_analysis_response: str) -> Optional[Dict[str, Any]]:
        """
        Legacy JSON parsing for backwards compatibility.
        """
        import re
        
        json_pattern = r"<<<DISCERNUS_ANALYSIS_JSON_v6>>>\n(.*?)\n<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>"
        json_match = re.search(json_pattern, raw_analysis_response, re.DOTALL)
        
        if json_match:
            try:
                analysis_data = json.loads(json_match.group(1))
                return analysis_data
            except json.JSONDecodeError as e:
                print(f"Warning: Failed to parse JSON from legacy format: {e}")
                return None
        else:
            print("Warning: No JSON found in legacy format")
            return None

    def _extract_evidence_from_delimited(self, raw_response: str) -> List[Dict[str, Any]]:
        """
        Extract evidence from delimited raw analysis response.
        """
        import re
        import json
        
        json_pattern = r'<<<DISCERNUS_ANALYSIS_JSON_v6>>>\s*({.*?})\s*<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>'
        json_match = re.search(json_pattern, raw_response, re.DOTALL)
        
        if not json_match:
            return []
        
        try:
            analysis_data = json.loads(json_match.group(1).strip())
            document_analyses = analysis_data.get('document_analyses', [])
            
            evidence_list = []
            for doc_analysis in document_analyses:
                doc_name = doc_analysis.get('document_name', 'unknown')
                evidence_items = doc_analysis.get('evidence', [])
                
                for evidence in evidence_items:
                    evidence_list.append({
                        "document_name": doc_name,
                        "dimension": evidence.get('dimension'),
                        "quote_text": evidence.get('quote_text'),
                        "confidence": evidence.get('confidence'),
                        "context_type": evidence.get('context_type'),
                        "extraction_method": "pre_extraction_v1.0",
                        "source_type": "raw_analysis_response"
                    })
            
            return evidence_list
        except json.JSONDecodeError as e:
            print(f"Warning: Failed to extract evidence from delimited format: {e}")
            return []

    def _combine_batch_results(self, all_analysis_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Combines results from multiple analysis batches into a single summary.
        """
        if not all_analysis_results:
            return {"total_duration_seconds": 0, "num_batches": 0, "successful_batches": 0}

        total_duration = sum(r.get('analysis_result', {}).get('duration_seconds', 0) for r in all_analysis_results)
        num_batches = len(all_analysis_results)
        successful_batches = sum(1 for r in all_analysis_results if r.get('analysis_result', {}).get('result_hash'))

        return {
            "total_duration_seconds": total_duration,
            "num_batches": num_batches,
            "successful_batches": successful_batches,
            "all_batches_successful": successful_batches == num_batches,
            "individual_batch_results": [
                {
                    "batch_id": r.get("analysis_result", {}).get("batch_id"),
                    "result_hash": r.get("analysis_result", {}).get("result_hash"),
                    "duration": r.get("analysis_result", {}).get("duration_seconds")
                } for r in all_analysis_results
            ]
        }

    def _load_experiment_config(self) -> Dict[str, Any]:
        """Load and validate the experiment.md file."""
        exp_file = self.experiment_path / "experiment.md"
        
        if not exp_file.exists():
            raise ThinOrchestratorError(f"experiment.md not found in {self.experiment_path}")
        
        content = self.security.secure_read_text(exp_file)
        
        if '---' in content:
            parts = content.split('---')
            if len(parts) >= 2:
                yaml_content = parts[1].strip()
            else:
                yaml_content = parts[0].strip()
        else:
            yaml_content = content
        
        try:
            config = yaml.safe_load(yaml_content)
        except yaml.YAMLError as e:
            raise ThinOrchestratorError(f"Invalid YAML in experiment.md: {e}")
        
        required_fields = ['name', 'framework', 'corpus_path']
        missing_fields = [field for field in required_fields if field not in config]
        if missing_fields:
            raise ThinOrchestratorError(f"Missing required fields in experiment.md: {', '.join(missing_fields)}")
        
        return config
    
    def _build_comprehensive_experiment_context(self, experiment_config: Dict[str, Any], framework_config: Dict[str, Any], corpus_manifest: Optional[Dict[str, Any]] = None) -> str:
        """
        THIN-compliant experiment context building.
        """
        
        context = {
            "experiment_config": experiment_config,
            "framework_config": framework_config,
            "corpus_manifest": corpus_manifest
        }
        
        return json.dumps(context, indent=2)
    
    def _load_framework(self, framework_filename: str) -> str:
        """
        Load framework content with trusted canonical path resolution.
        """
        
        if framework_filename.startswith("../../frameworks/"):
            project_root = Path(__file__).parent.parent.parent
            canonical_path = framework_filename.lstrip("../../")
            framework_file = project_root / canonical_path
            
            if not framework_file.exists():
                raise ThinOrchestratorError(f"Canonical framework not found: {framework_filename}")
            
            print(f"🛡️ Security: Loading canonical framework: {framework_file.name}")
            return framework_file.read_text(encoding='utf-8')
        
        else:
            framework_file = self.experiment_path / framework_filename
            
            if not framework_file.exists():
                raise ThinOrchestratorError(f"Framework file not found: {framework_filename}")
            
            print(f"🛡️ Security: Loading local framework: {framework_file.name}")
            return self.security.secure_read_text(framework_file)
    
    def _load_corpus(self, corpus_path: str) -> tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """Load corpus documents and corpus manifest."""
        corpus_dir = self.experiment_path / corpus_path
        
        if not corpus_dir.exists():
            raise ThinOrchestratorError(f"Corpus directory not found: {corpus_path}")
        
        corpus_files = []
        for root, dirs, files in os.walk(corpus_dir):
            for file in files:
                if file.endswith(('.txt', '.pdf')) and not file.startswith('.'):
                    corpus_files.append(Path(root) / file)
        
        if not corpus_files:
            raise ThinOrchestratorError(f"No .txt or .pdf files found in corpus directory: {corpus_path}")
        
        documents = []
        for file_path in sorted(corpus_files):
            if file_path.suffix == '.txt':
                content = self.security.secure_read_text(file_path)
            elif file_path.suffix == '.pdf':
                content = self.security.secure_read_bytes(file_path)
            
            documents.append({
                "filename": file_path.name,
                "content": content,
                "filepath": str(file_path.relative_to(self.experiment_path))
            })
        
        corpus_manifest = {}
        corpus_md_file = corpus_dir / "corpus.md"
        if corpus_md_file.exists():
            try:
                corpus_md_content = self.security.secure_read_text(corpus_md_file)
                
                if '```json' in corpus_md_content:
                    json_start = corpus_md_content.find('```json') + 7
                    json_end = corpus_md_content.find('```', json_start)
                    if json_end > json_start:
                        json_str = corpus_md_content[json_start:json_end].strip()
                        corpus_manifest = json.loads(json_str)
                        print(f"📄 Loaded corpus manifest with {len(corpus_manifest.get('file_manifest', []))} document metadata entries")
                    else:
                        print("⚠️ corpus.md found but no valid JSON block detected")
                else:
                    print("⚠️ corpus.md found but no JSON block detected")
            except Exception as e:
                print(f"⚠️ Failed to parse corpus.md: {e}")
                corpus_manifest = {}
        else:
            print("⚠️ No corpus.md found - synthesis will have limited metadata awareness")
        
        return documents, corpus_manifest
    
    def _calculate_duration(self, start: str, end: str) -> float:
        """Calculate duration between timestamps in seconds."""
        try:
            start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
            return (end_dt - start_dt).total_seconds()
        except Exception:
            return 0.0
    
    def _auto_commit_run(self, run_folder: Path, run_metadata: Dict[str, Any], audit: 'AuditLogger') -> bool:
        """
        Automatically commit completed research run to Git.
        """
        import subprocess
        
        try:
            repo_root = run_folder.parent.parent.parent
            
            result = subprocess.run(
                ["git", "add", "--force", str(run_folder.relative_to(repo_root))],
                cwd=repo_root,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                audit.log_error("auto_commit_add_failed", result.stderr, {
                    "run_folder": str(run_folder),
                    "git_add_stderr": result.stderr
                })
                return False
            
            run_id = run_metadata.get('run_id', 'unknown')
            experiment_name = run_metadata.get('experiment_name', 'experiment')
            commit_msg = f"Complete run {run_id}: {experiment_name}"
            
            if len(commit_msg) > 47:
                commit_msg = commit_msg[:44] + "..."
            
            result = subprocess.run(
                ["git", "commit", "-m", commit_msg],
                cwd=repo_root,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                if "nothing to commit" in result.stdout.lower() or "nothing to commit" in result.stderr.lower():
                    audit.log_orchestrator_event("auto_commit_nothing_to_commit", {
                        "message": "No new changes to commit"
                    })
                    return True
                
                audit.log_error("auto_commit_commit_failed", result.stderr, {
                    "run_folder": str(run_folder),
                    "commit_message": commit_msg,
                    "git_commit_stderr": result.stderr
                })
                return False
            
            if "nested repositories found" in result.stderr and "commit proceeding" in result.stderr:
                pass
            elif result.stderr and "nothing to commit" not in result.stderr.lower():
                audit.log_orchestrator_event("auto_commit_warning", {
                    "message": "Git commit succeeded but had stderr output",
                    "stderr": result.stderr
                })
            
            audit.log_orchestrator_event("auto_commit_success", {
                "run_id": run_id,
                "commit_message": commit_msg,
                "committed_path": str(run_folder.relative_to(repo_root))
            })
            
            print(f"📝 Auto-committed to Git: {commit_msg}")
            return True
            
        except subprocess.TimeoutExpired:
            audit.log_error("auto_commit_timeout", "Git command timed out", {
                "run_folder": str(run_folder)
            })
            return False
        except Exception as e:
            audit.log_error("auto_commit_error", str(e), {
                "run_folder": str(run_folder),
                "error_type": type(e).__name__
            })
            return False
    
    def _parse_framework_config(self, framework_content: str) -> Dict[str, Any]:
        """Parse framework configuration from framework content."""
        try:
            import re
            json_match = re.search(r'<details><summary>Machine-Readable Configuration</summary>\s*```json\s*\n(.*?)\n\s*```\s*</details>', framework_content, re.DOTALL)
            if json_match:
                config_str = json_match.group(1)
                config = json.loads(config_str)
                
                if 'static_weights' not in config:
                    config['static_weights'] = {}
                
                if 'pattern_classifications' not in config:
                    config['pattern_classifications'] = {}
                
                if 'reporting_metadata' not in config:
                    config['reporting_metadata'] = {}
                    
                return config
            else:
                json_match_fallback = re.search(r'```json\s*\n(.*?)\n\s*```', framework_content, re.DOTALL)
                if json_match_fallback:
                    return json.loads(json_match_fallback.group(1))
                return {"name": "unknown", "version": "unknown", "static_weights": {}}
        except Exception as e:
            print(f"⚠️  Framework parsing error: {e}. Defaulting to empty config.")
            return {"name": "unknown", "version": "unknown", "static_weights": {}} 
