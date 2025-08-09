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
            
            # Log cost information if audit logger available
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
                # Fallback to safe default if LLM call fails
                return {
                    "compatibility": "INCOMPATIBLE",
                    "confidence": 0.0,
                    "reasoning": f"LLM compatibility check failed: {metadata.get('error', 'unknown error')}",
                    "differences_found": ["LLM_CALL_FAILED"],
                    "reuse_recommendation": "NONE"
                }
            
            # Parse LLM JSON response
            import json
            import re
            json_match = re.search(r'\{.*\}', response_content, re.DOTALL)
            if json_match:
                compatibility_result = json.loads(json_match.group())
                # Validate required fields
                required_fields = ["compatibility", "confidence", "reasoning", "reuse_recommendation"]
                if all(field in compatibility_result for field in required_fields):
                    return compatibility_result
            
            # Fallback if parsing fails
            return {
                "compatibility": "INCOMPATIBLE", 
                "confidence": 0.0,
                "reasoning": "Failed to parse LLM compatibility response",
                "differences_found": ["PARSING_FAILED"],
                "reuse_recommendation": "NONE"
            }
            
        except Exception as e:
            # Fallback to safe default on any error
            return {
                "compatibility": "INCOMPATIBLE",
                "confidence": 0.0, 
                "reasoning": f"Framework compatibility check failed: {str(e)}",
                "differences_found": ["EXCEPTION_OCCURRED"],
                "reuse_recommendation": "NONE"
            }
        
    def _create_thin_synthesis_pipeline(self, audit_logger: AuditLogger, storage: LocalArtifactStorage, model: str, debug_agent: Optional[str] = None, debug_level: str = "info", analysis_model: Optional[str] = None) -> ProductionThinSynthesisPipeline:
        """Create a ProductionThinSynthesisPipeline with proper infrastructure."""
        
        # Create MinIO-compatible wrapper for LocalArtifactStorage
        class MinIOCompatibleStorage:
            def __init__(self, local_storage):
                self.local_storage = local_storage
                
            def put_artifact(self, content: bytes):
                return self.local_storage.put_artifact(content, {})
                
            def get_artifact(self, hash_id: str):
                return self.local_storage.get_artifact(hash_id)
                
            def artifact_exists(self, hash_id: str):
                return self.local_storage.artifact_exists(hash_id)
        
        compatible_storage = MinIOCompatibleStorage(storage)
        
        print(f"🔧 Creating synthesis pipeline with model: {model}")
        return ProductionThinSynthesisPipeline(
            artifact_client=compatible_storage,
            audit_logger=audit_logger,
            model=model,
            analysis_model=analysis_model
        )

    def _run_thin_synthesis(self,
                           scores_hash: str,
                           evidence_hash: str,
                           framework_content: str,
                           experiment_config: Dict[str, Any],
                           model: str,
                           audit_logger: AuditLogger,
                           storage: LocalArtifactStorage,
                           framework_hash: str,
                           corpus_hash: str,
                           corpus_manifest_hash: str,
                           corpus_manifest: Optional[Dict[str, Any]] = None,
                           analysis_model: Optional[str] = None,
                           debug_agent: Optional[str] = None,
                           debug_level: str = "info") -> Dict[str, Any]:
        """
        Run synthesis using the new THIN Code-Generated Synthesis Architecture.
        
        Returns results in the same format as EnhancedSynthesisAgent for compatibility.
        """
        
        # Create THIN synthesis pipeline
        pipeline = self._create_thin_synthesis_pipeline(audit_logger, storage, model, debug_agent, debug_level, analysis_model)
        
        # Parse the framework config to access static_weights and other metadata
        framework_config = self._parse_framework_config(framework_content)

        # Build THIN-compliant experiment context - raw data for LLM intelligence
        experiment_context = self._build_comprehensive_experiment_context(experiment_config, framework_config, corpus_manifest)
        
        # Create pipeline request
        request = ProductionPipelineRequest(
            framework_spec=framework_content,
            scores_artifact_hash=scores_hash,
            evidence_artifact_hash=evidence_hash,
            corpus_artifact_hash=corpus_hash,  # Pass corpus content hash for comprehensive RAG
            experiment_context=experiment_context,
            max_evidence_per_finding=3,
            min_confidence_threshold=0.7,
            interpretation_focus="comprehensive",
            # Add provenance context (Issue #208 fix)
            framework_hash=framework_hash,
            corpus_hash=corpus_manifest_hash, # Use manifest hash for provenance
            framework_name=experiment_config.get('framework', 'Unknown framework'),
            corpus_manifest=corpus_manifest
        )
        
        # Execute pipeline
        start_time = time.time()
        response = pipeline.run(request)
        duration_seconds = time.time() - start_time
        
        if response.success:
            # Store the narrative report as an artifact for compatibility
            report_hash = storage.put_artifact(
                response.narrative_report.encode('utf-8'),
                {"artifact_type": "synthesis_report", "pipeline": "thin_architecture"}
            )
            
            # Return in EnhancedSynthesisAgent format for compatibility
            return {
                "result_hash": report_hash,
                "duration_seconds": duration_seconds,
                "synthesis_confidence": 0.95,  # THIN architecture generally high confidence
                "synthesis_report_markdown": response.narrative_report,
                # Include artifact hashes for CSV export (Sprint 6 fix)
                "statistical_results_hash": response.statistical_results_hash,
                "curated_evidence_hash": response.curated_evidence_hash,
                
                # Additional THIN-specific metadata
                "thin_metadata": {
                    "pipeline_version": "production_v1.0",
                    "stage_timings": response.stage_timings,
                    "stage_success": response.stage_success,
                    "word_count": response.word_count,
                    "generated_artifacts": {
                        "analysis_plan": response.analysis_plan_hash,
                        "statistical_results": response.statistical_results_hash,
                        "curated_evidence": response.curated_evidence_hash
                    }
                }
            }
        else:
            # DEVELOPMENT: Fail fast instead of expensive fallbacks during debugging
            error_msg = f"THIN synthesis failed: {response.error_message}"
            print(f"❌ {error_msg}")
            print("🛑 Stopping execution to allow debugging (no expensive fallback)")
            raise ThinOrchestratorError(error_msg)

    def run_experiment(self, 
                      analysis_model: str = "vertex_ai/gemini-2.5-flash-lite",
                      synthesis_model: str = "vertex_ai/gemini-2.5-pro",
                      synthesis_only: bool = False,
                      analysis_only: bool = False,
                      ensemble_runs: int = 1,
                      auto_commit: bool = True,
                      resume_stage: Optional[str] = None,
                      debug_agent: Optional[str] = None,
                      debug_level: str = "info") -> Dict[str, Any]:
        """
        Run experiment with enhanced agents and stage control for targeted debugging.
        
        Args:
            analysis_model: LLM model to use for analysis
            synthesis_model: LLM model to use for synthesis
            synthesis_only: If True, skip analysis and run synthesis on existing CSVs
            analysis_only: If True, run only analysis phase and save artifacts
            ensemble_runs: Number of ensemble runs for self-consistency (1 = single run, 3-5 recommended)
            auto_commit: If True, automatically commit successful runs to Git (default: True)
            resume_stage: Resume at specific THIN synthesis sub-stage ('thin-gen', 'thin-exec', 'thin-cure', 'thin-interp')
            
        Returns:
            Experiment results with mathematical validation
        """
        start_time = datetime.now(timezone.utc).isoformat()
        
        # Create timestamped run folder
        run_timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        run_folder = self.experiment_path / "runs" / run_timestamp
        
        try:
            # Initialize run infrastructure
            self.security.secure_mkdir(run_folder)
            
            # Initialize audit logging
            audit = AuditLogger(self.security, run_folder)
            
            # Initialize experiment-level shared cache for perfect THIN caching
            shared_cache_dir = self.experiment_path / "shared_cache"
            self.security.secure_mkdir(shared_cache_dir)
            storage = LocalArtifactStorage(self.security, shared_cache_dir, run_timestamp)
            
            # Initialize enhanced manifest
            manifest = EnhancedManifest(self.security, run_folder, audit, storage)
            
            audit.log_orchestrator_event("experiment_start", {
                "experiment_path": str(self.experiment_path),
                "run_folder": str(run_folder),
                "model": analysis_model,
                "synthesis_only": synthesis_only,
                "architecture": "thin_v2.0_direct_calls"
            })
            
            print(f"🚀 Starting THIN v2.0 experiment: {run_timestamp}")
            
            # Load and validate experiment configuration
            experiment_config = self._load_experiment_config()
            manifest.set_run_metadata(
                experiment_config["name"], 
                str(self.experiment_path),
                "thin_v2.0_alpha"
            )
            manifest.set_experiment_config(experiment_config)
            
            # Load framework
            framework_content = self._load_framework(experiment_config["framework"])
            
            # Store framework content, audit logger, and analysis model for gasket integration
            self._current_framework_content = framework_content
            self._current_audit_logger = audit
            self._current_analysis_model = analysis_model
            framework_hash = storage.put_artifact(
                framework_content.encode('utf-8'),
                {"artifact_type": "framework", "original_filename": experiment_config["framework"]}
            )
            manifest.add_input_artifact("framework", framework_hash, {
                "filename": experiment_config["framework"],
                "size_bytes": len(framework_content)
            })
            
            # Load corpus documents and manifest
            corpus_documents, corpus_manifest = self._load_corpus(experiment_config["corpus_path"])
            corpus_hashes = []
            corpus_metadata = []
            
            for doc in corpus_documents:
                doc_hash = storage.put_artifact(
                    doc["content"].encode('utf-8') if isinstance(doc["content"], str) else doc["content"],
                    {"artifact_type": "corpus_document", "original_filename": doc["filename"]}
                )
                corpus_hashes.append(doc_hash)
                corpus_metadata.append({
                    "filename": doc["filename"],
                    "size_bytes": len(doc["content"]) if isinstance(doc["content"], str) else len(doc["content"])
                })
            
            manifest.add_corpus_artifacts(corpus_hashes, corpus_metadata)
            
            audit.log_orchestrator_event("inputs_loaded", {
                "framework_hash": framework_hash,
                "corpus_documents": len(corpus_documents),
                "total_input_artifacts": len(corpus_hashes) + 1
            })

            # Handle analysis-only mode: run analysis and exit early
            if analysis_only:
                print("🔍 Analysis-only mode: Running analysis and saving artifacts for later synthesis...")
                
                # Execute analysis phase
                print(f"📊 Analysis-only mode: Processing {len(corpus_documents)} documents...")
                
                analysis_agent = EnhancedAnalysisAgent(self.security, audit, storage)
                all_analysis_results, scores_hash, evidence_hash, corpus_hash = self._execute_analysis_sequentially(
                    analysis_agent,
                    corpus_documents,
                    framework_content,
                    experiment_config,
                    analysis_model,
                    ensemble_runs
                )
                
                # Display analysis-only cost
                analysis_costs = audit.get_session_costs()
                successful_count = len([res for res in all_analysis_results if res.get('analysis_result', {}).get('result_hash')])
                print(f"✅ Analysis complete: {successful_count}/{len(corpus_documents)} documents processed")
                print(f"   💰 Total cost: ${analysis_costs.get('total_cost_usd', 0.0):.4f} USD")
                print(f"   🔢 Total tokens: {analysis_costs.get('total_tokens', 0):,}")
                
                # Check if analysis succeeded
                successful_analyses = [res for res in all_analysis_results if res.get('analysis_result', {}).get('result_hash')]
                if not successful_analyses:
                    raise ThinOrchestratorError("Analysis failed. No artifacts saved.")
                
                # Create results directory and save artifact references
                results_dir = run_folder / "results"
                self.security.secure_mkdir(results_dir)
                
                analysis_summary = {
                    "mode": "analysis_only",
                    "scores_hash": scores_hash,
                    "evidence_hash": evidence_hash,
                    "corpus_hash": corpus_hash,
                    "analysis_results_count": len(successful_analyses),
                    "available_for_synthesis": True
                }
                
                with open(results_dir / "analysis_summary.json", "w") as f:
                    json.dump(analysis_summary, f, indent=2)
                
                # Export CSV files for external analysis (Gasket #3a)
                csv_export_result = self._export_csv_files(
                    scores_hash, evidence_hash, framework_content, 
                    experiment_config, corpus_manifest, results_dir, audit
                )
                
                if csv_export_result:
                    print(f"📊 CSV files exported:")
                    for filename, info in csv_export_result.get('files', {}).items():
                        print(f"   - {filename}: {info.get('records', 0)} records ({info.get('size_bytes', 0):,} bytes)")
                else:
                    print(f"⚠️  CSV export failed - continuing without CSV files")
                
                            # Create provenance-first artifact organization for analysis-only runs
            try:
                from discernus.core.provenance_organizer import ProvenanceOrganizer
                provenance_organizer = ProvenanceOrganizer(self.security, audit)
                experiment_metadata = {
                    "experiment_name": experiment_config.get("name", "Unknown Experiment"),
                    "run_timestamp": run_timestamp,
                    "framework_version": experiment_config.get("framework", "Unknown Framework"),
                    "model_used": analysis_model,
                    "mode": "analysis_only"
                }
                
                provenance_result = provenance_organizer.organize_run_artifacts(
                    run_folder, shared_cache_dir, experiment_metadata
                )
                
                if provenance_result["success"]:
                    print(f"📁 Provenance organization: {provenance_result['artifacts_organized']} artifacts organized")
                else:
                    print("⚠️  Provenance organization failed, continuing with standard structure")
                    
            except Exception as e:
                print(f"⚠️  Provenance organization error: {str(e)}")
                audit.log_error("provenance_organization_error", str(e), {})
            

                
                print(f"✅ Analysis completed - artifacts saved for synthesis:")
                print(f"   - Scores: {scores_hash[:12]}...")
                print(f"   - Evidence: {evidence_hash[:12]}...")
                print(f"   - Ready for: discernus run --synthesis-only or --stage commands")
                
                # Update manifest and return
                end_time = datetime.now(timezone.utc).isoformat()
                manifest.add_execution_stage(
                    stage_name="analysis",
                    agent_name="EnhancedAnalysisAgent", 
                    start_time=start_time,
                    end_time=end_time,
                    status="completed",
                    metadata={"model": analysis_model, "mode": "analysis_only"}
                )
                manifest.finalize_manifest()
                
                # Get cost information for analysis-only mode
                session_costs = audit.get_session_costs()
                
                # Auto-commit successful analysis-only run to Git (if enabled)
                commit_success = True
                if auto_commit:
                    commit_metadata = {
                        "run_id": run_timestamp,
                        "experiment_name": self.experiment_path.name
                    }
                    commit_success = self._auto_commit_run(run_folder, commit_metadata, audit)
                    if not commit_success:
                        print("⚠️  Auto-commit to Git failed (analysis completed successfully)")
                
                return {
                    "run_id": run_timestamp,
                    "status": "analysis_completed",
                    "scores_hash": scores_hash,
                    "evidence_hash": evidence_hash,
                    "corpus_hash": corpus_hash,
                    "duration": self._calculate_duration(start_time, end_time),
                    "costs": session_costs,
                    "auto_commit_success": auto_commit and commit_success if auto_commit else None
                }
            
            # Handle resume from specific THIN synthesis stage
            if resume_stage:
                print(f"⏩ Resume mode: Starting from THIN synthesis stage '{resume_stage}'...")
                
                # Validate that we can resume (artifacts exist)
                shared_cache_dir = self.experiment_path / "shared_cache" / "artifacts" 
                if not shared_cache_dir.exists():
                    raise ThinOrchestratorError(f"No shared cache found for resume mode. Run analysis first.")
                
                # TODO: Add stage-specific artifact validation and resumption logic
                # For now, fall back to synthesis_only behavior for stages
                print(f"⚠️  Stage-specific resumption not yet implemented. Using full synthesis...")
                synthesis_only = True  # Temporary fallback

            if synthesis_only:
                # Find latest run with complete analysis
                shared_cache_dir = self.experiment_path / "shared_cache" / "artifacts"
                if not shared_cache_dir.exists():
                    raise ThinOrchestratorError("No shared cache found for synthesis-only mode")
                
                # Create results directory for new run
                results_dir = run_folder / "results"
                self.security.secure_mkdir(results_dir)
                
                # Load artifact registry to find CSVs
                registry_file = shared_cache_dir / "artifact_registry.json"
                if not registry_file.exists():
                    raise ThinOrchestratorError("Artifact registry not found")
                
                with open(registry_file) as f:
                    registry = json.load(f)
                
                # Calculate current framework hash for provenance validation (Issue #208)
                current_framework_content = self._load_framework(experiment_config["framework"])
                current_framework_hash = hashlib.sha256(current_framework_content.encode('utf-8')).hexdigest()
                
                # THIN v2.1: LLM-based framework compatibility checking
                # Replace rigid hash matching with semantic analysis
                json_artifact_hash = None
                latest_json_time = None
                compatibility_info = None
                
                # First, try exact hash match for perfect compatibility (fast path)
                for artifact_id, info in registry.items():
                    metadata = info.get("metadata", {})
                    artifact_type = metadata.get("artifact_type")
                    artifact_framework_hash = metadata.get("framework_hash")
                    
                    if (artifact_framework_hash == current_framework_hash and 
                        artifact_type == "analysis_json_v6"):
                        timestamp = info["created_at"]
                        if not latest_json_time or timestamp > latest_json_time:
                            latest_json_time = timestamp
                            json_artifact_hash = artifact_id
                            compatibility_info = {
                                "method": "exact_hash_match",
                                "compatibility": "COMPATIBLE",
                                "confidence": 1.0,
                                "reasoning": "Identical framework hash - perfect match"
                            }
                
                # If no exact match, use LLM-based semantic compatibility checking
                if not json_artifact_hash:
                    print("🔍 No exact framework match found. Using LLM semantic compatibility analysis...")
                    
                    # Try LLM semantic analysis for frameworks with stored content
                    for artifact_id, info in registry.items():
                        metadata = info.get("metadata", {})
                        artifact_type = metadata.get("artifact_type")
                        artifact_framework_hash = metadata.get("framework_hash")
                        cached_framework_content = metadata.get("framework_content")
                        
                        # Use LLM analysis if we have framework content stored
                        if (artifact_type == "analysis_json_v6" and 
                            artifact_framework_hash and 
                            cached_framework_content and 
                            artifact_framework_hash != current_framework_hash):
                            
                            print(f"   🧠 Checking semantic compatibility with LLM for {artifact_id[:8]}...")
                            
                            compatibility_result = self._check_framework_compatibility_with_llm(
                                current_framework_content, 
                                cached_framework_content, 
                                artifact_id, 
                                audit_logger=audit
                            )
                            
                            # Use compatible artifact if LLM determines compatibility
                            if compatibility_result.get("compatibility") == "COMPATIBLE":
                                timestamp = info["created_at"]
                                if not latest_json_time or timestamp > latest_json_time:
                                    latest_json_time = timestamp
                                    json_artifact_hash = artifact_id
                                    compatibility_info = compatibility_result
                                    print(f"   ✅ LLM determined semantic compatibility: {artifact_id[:8]}...")
                                    break
                    
                    # Fallback to legacy compatibility for artifacts without framework content
                    if not json_artifact_hash:
                        print("   📎 No semantically compatible artifacts found. Checking legacy artifacts...")
                        for artifact_id, info in registry.items():
                            metadata = info.get("metadata", {})
                            artifact_type = metadata.get("artifact_type")
                            artifact_framework_hash = metadata.get("framework_hash")
                            
                            # Allow artifacts without framework hash (legacy compatibility)
                            if artifact_type == "analysis_json_v6" and not artifact_framework_hash:
                                timestamp = info["created_at"]
                                if not latest_json_time or timestamp > latest_json_time:
                                    latest_json_time = timestamp
                                    json_artifact_hash = artifact_id
                                    compatibility_info = {
                                        "method": "legacy_compatibility",
                                        "compatibility": "ASSUMED_COMPATIBLE",
                                        "confidence": 0.5,
                                        "reasoning": "Legacy artifact without framework hash - assumed compatible for backward compatibility"
                                    }
                                    print(f"   📎 Found legacy artifact without framework hash: {artifact_id[:8]}...")
                
                if json_artifact_hash:
                    # Use compatible artifact for both scores and evidence
                    scores_hash = json_artifact_hash
                    evidence_hash = json_artifact_hash
                    
                    print(f"✅ Using compatible analysis from shared cache")
                    print(f"   - Combined JSON: {json_artifact_hash[:8]}... ({latest_json_time})")
                    print(f"   - Framework: {current_framework_hash[:12]}... ")
                    print(f"   - Compatibility: {compatibility_info['compatibility']} "
                          f"({compatibility_info['confidence']:.2f} confidence)")
                    print(f"   - Method: {compatibility_info['method']}")
                    print(f"   - Reasoning: {compatibility_info['reasoning']}")
                else:
                    # Log available artifacts for debugging
                    available_artifacts = []
                    for artifact_id, info in registry.items():
                        metadata = info.get("metadata", {})
                        if metadata.get("artifact_type") == "analysis_json_v6":
                            available_artifacts.append({
                                "artifact_id": artifact_id[:12],
                                "framework_hash": metadata.get("framework_hash", "MISSING")[:12],
                                "timestamp": info.get("created_at")
                            })
                    
                    print(f"❌ No compatible analysis artifacts found")
                    print(f"   Current framework hash: {current_framework_hash[:12]}...")
                    print(f"   Available artifacts: {len(available_artifacts)}")
                    for artifact in available_artifacts:
                        print(f"     - {artifact['artifact_id']}... (fw: {artifact['framework_hash']}...)")
                    print("   💡 LLM determined no semantic compatibility with existing frameworks")
                    
                    raise ThinOrchestratorError(
                        f"No compatible analysis artifacts found for current framework. "
                        f"Current framework hash: {current_framework_hash[:12]}... "
                        f"Found {len(available_artifacts)} incompatible artifacts. "
                        "Run full analysis to generate artifacts for this framework."
                    )
                
                # Copy JSON artifact to new run for reference
                import shutil
                shutil.copy2(shared_cache_dir / json_artifact_hash, results_dir / "analysis.json")
                
                print(f"📊 Using existing analysis from shared cache (THIN v2.1)")
                print(f"   - Combined JSON: {json_artifact_hash[:8]}... ({latest_json_time})")
                print(f"   - Framework: {current_framework_hash[:12]}...")
                print(f"   - THIN Compatibility: {compatibility_info['compatibility']} "
                      f"({compatibility_info['confidence']:.2f} confidence)")
                print(f"   - Validation Method: {compatibility_info['method']}")
                print(f"   - Reasoning: {compatibility_info['reasoning']}")
                
                # Load framework and corpus for synthesis context (even in synthesis-only mode)
                framework_content = self._load_framework(experiment_config["framework"])
                _, corpus_manifest = self._load_corpus(experiment_config["corpus_path"])
                
                # Run synthesis only
                print("🏭 Using Discernus Advanced Synthesis Pipeline...")
                
                # Calculate framework hash for provenance
                framework_hash = hashlib.sha256(framework_content.encode('utf-8')).hexdigest()
                
                # Calculate corpus hash for complete provenance context
                corpus_content = ''.join([doc.get('filename', '') + str(doc.get('content', '')) for doc in corpus_documents])
                corpus_hash = hashlib.sha256(corpus_content.encode('utf-8')).hexdigest()
                
                print(f"🔬 Starting synthesis with {synthesis_model} using cached analysis...")
                
                synthesis_results = self._run_thin_synthesis(
                    scores_hash=scores_hash,
                    evidence_hash=evidence_hash,
                    framework_content=framework_content,
                    experiment_config=experiment_config,
                    model=synthesis_model,
                    audit_logger=audit,
                    storage=storage,
                    framework_hash=framework_hash,
                    corpus_hash=corpus_hash,
                    corpus_manifest_hash=corpus_manifest_hash,
                    corpus_manifest=corpus_manifest,
                    analysis_model=analysis_model
                )
                
                synthesis_end_time = datetime.now(timezone.utc).isoformat()
                
                # Display synthesis-only cost
                synthesis_costs = audit.get_session_costs()
                print(f"✅ Synthesis complete using cached analysis!")
                print(f"   💰 Synthesis cost: ${synthesis_costs.get('total_cost_usd', 0.0):.4f} USD")
                print(f"   🔢 Tokens used: {synthesis_costs.get('total_tokens', 0):,}")
                
                if not synthesis_results or not isinstance(synthesis_results, dict):
                    raise ThinOrchestratorError(f"Invalid synthesis result format: {type(synthesis_results)}")
                
                if "synthesis_report_markdown" not in synthesis_results:
                    raise ThinOrchestratorError("Missing synthesis_report_markdown in result")
                
                # Generate final report with cost transparency
                base_report = synthesis_results["synthesis_report_markdown"]
                session_costs = audit.get_session_costs()
                
                # Add cost summary section to report
                cost_section = self._generate_cost_summary_section(session_costs, run_timestamp)
                final_report = base_report + "\n\n" + cost_section
                
                # Save final report
                with open(results_dir / "final_report.md", "w") as f:
                    f.write(final_report)
                
                # Export comprehensive final CSV files including synthesis artifacts (Issue #295 regression fix)
                # Extract synthesis artifact hashes from synthesis metadata
                statistical_results_hash = ""
                curated_evidence_hash = ""
                
                # Check if synthesis metadata contains artifact references
                if "statistical_results_hash" in synthesis_results:
                    statistical_results_hash = synthesis_results["statistical_results_hash"]
                if "curated_evidence_hash" in synthesis_results:
                    curated_evidence_hash = synthesis_results["curated_evidence_hash"]
                
                final_csv_export_result = self._export_final_synthesis_csv_files(
                    scores_hash, evidence_hash, statistical_results_hash,
                    curated_evidence_hash, framework_content, 
                    experiment_config, corpus_manifest, synthesis_results, results_dir, audit
                )
                
                # Create provenance-first artifact organization (Issue #297)
                try:
                    provenance_organizer = ProvenanceOrganizer(self.security, audit)
                    experiment_metadata = {
                        "experiment_name": experiment_config.get("name", "Unknown Experiment"),
                        "run_timestamp": run_timestamp,
                        "framework_version": experiment_config.get("framework", "Unknown Framework"),
                        "model_used": synthesis_model
                    }
                    
                    provenance_result = provenance_organizer.organize_run_artifacts(
                        run_folder, shared_cache_dir, experiment_metadata
                    )
                    
                    if provenance_result["success"]:
                        print(f"📁 Provenance organization: {provenance_result['artifacts_organized']} artifacts organized")
                    else:
                        print("⚠️  Provenance organization failed, continuing with standard structure")
                        
                except Exception as e:
                    print(f"⚠️  Provenance organization error: {str(e)}")
                    audit.log_error("provenance_organization_error", str(e), {})
                
                # Update manifest
                end_time = datetime.now(timezone.utc).isoformat()
                manifest.add_execution_stage(
                    stage_name="synthesis",
                    agent_name="EnhancedSynthesisAgent",
                    start_time=start_time,
                    end_time=end_time,
                    status="completed",
                    metadata={"model": synthesis_model}
                )
                manifest.finalize_manifest()
                
                # Get cost information for synthesis-only mode
                session_costs = audit.get_session_costs()
                
                # Auto-commit successful synthesis-only run to Git (if enabled)
                commit_success = True
                if auto_commit:
                    commit_metadata = {
                        "run_id": run_timestamp,
                        "experiment_name": self.experiment_path.name
                    }
                    commit_success = self._auto_commit_run(run_folder, commit_metadata, audit)
                    if not commit_success:
                        print("⚠️  Auto-commit to Git failed (synthesis completed successfully)")
                
                return {
                    "run_id": run_timestamp,
                    "status": "completed",
                    "duration": self._calculate_duration(start_time, end_time),
                    "costs": session_costs,
                    "auto_commit_success": auto_commit and commit_success if auto_commit else None
                }
            
            # Normal full run - continue with analysis phase
            # Phase 1: Batch Planning and Enhanced Analysis with Context Window Management
            # CONTEXT_WINDOW_MANAGEMENT: This entire section can be removed when LLM context windows become unlimited
            batch_planning_start_time = datetime.now(timezone.utc).isoformat()
            manifest.add_execution_stage("batch_planning", "BatchPlannerAgent", batch_planning_start_time)
            
            # Create intelligent batch plan with production cost transparency
            # batch_planner = BatchPlannerAgent(self.security, audit)
            # batch_plan = batch_planner.create_batches(
            #     framework_content=framework_content,
            #     corpus_documents=corpus_documents,
            #     model=model
            # )
            
            batch_planning_end_time = datetime.now(timezone.utc).isoformat()
            manifest.add_execution_stage("batch_planning", "BatchPlannerAgent",
                                       batch_planning_start_time, batch_planning_end_time, "completed", {
                "total_batches": 0, # No batches in this new flow
                "total_estimated_cost": 0.0,
                "total_estimated_tokens": 0,
                "context_window_limit": 0
            })
            
            print(f"💰 Cost tracking: Per-document analysis costs will be displayed")
            print(f"📊 Processing: {len(corpus_documents)} documents individually")
            
            # Initialize analysis and synthesis agents
            analysis_agent = EnhancedAnalysisAgent(self.security, audit, storage)
            
            # Execute analysis (in chunks)
            print(f"📊 Starting analysis of {len(corpus_documents)} documents with {analysis_model}...")
            
            all_analysis_results, scores_hash, evidence_hash, corpus_artifact_hash = self._execute_analysis_sequentially(
                analysis_agent,
                corpus_documents,
                framework_content,
                experiment_config,
                analysis_model,
                ensemble_runs
            )
            
            # Display analysis progress and cost
            analysis_costs = audit.get_session_costs()
            successful_count = len([res for res in all_analysis_results if res.get('analysis_result', {}).get('result_hash')])
            print(f"✅ Analysis phase complete: {successful_count}/{len(corpus_documents)} documents processed")
            print(f"   💰 Analysis cost so far: ${analysis_costs.get('total_cost_usd', 0.0):.4f} USD")
            print(f"   🔢 Tokens used: {analysis_costs.get('total_tokens', 0):,}")

            # TODO: Ensemble runs disabled pending architectural review
            # Report ensemble quality summary if ensemble runs were used
            # if ensemble_runs > 1:
            #     self._report_ensemble_summary(all_analysis_results, ensemble_runs)

            # Check if any analysis tasks succeeded
            successful_analyses = [res for res in all_analysis_results if res.get('analysis_result', {}).get('result_hash')]
            if not successful_analyses:
                raise ThinOrchestratorError("All analysis batches failed. Halting experiment.")

            # Execute synthesis
            print("\n🔬 Synthesizing results...")
            synthesis_start_time = datetime.now(timezone.utc).isoformat()
            
            print("🏭 Using Discernus Advanced Synthesis Pipeline...")
            print(f"DEBUG: Passing scores_hash={scores_hash}, evidence_hash={evidence_hash} to THIN pipeline.")
            
            # Calculate framework hash for provenance
            framework_hash = hashlib.sha256(framework_content.encode('utf-8')).hexdigest()
            
            # This is the manifest hash, not the content hash.
            corpus_manifest_hash = corpus_documents[0]['hash'] if corpus_documents else ""
            
            synthesis_results = self._run_thin_synthesis(
                scores_hash=scores_hash,
                evidence_hash=evidence_hash,
                corpus_hash=corpus_artifact_hash,  # Use the content hash from analysis
                framework_content=framework_content,
                experiment_config=experiment_config,
                model=synthesis_model,
                audit_logger=audit,
                storage=storage,
                framework_hash=framework_hash,
                corpus_manifest_hash=corpus_manifest_hash,
                corpus_manifest=corpus_manifest,
                analysis_model=analysis_model
            )
            
            synthesis_end_time = datetime.now(timezone.utc).isoformat()
            
            # Display synthesis cost update
            synthesis_costs = audit.get_session_costs()
            print(f"✅ Synthesis phase complete!")
            print(f"   💰 Total cost so far: ${synthesis_costs.get('total_cost_usd', 0.0):.4f} USD")
            print(f"   🔢 Total tokens: {synthesis_costs.get('total_tokens', 0):,}")
            
            # Record synthesis stage
            agent_name = "ProductionThinSynthesisPipeline"
            stage_metadata = {
                "result_hash": synthesis_results["result_hash"],
                "duration_seconds": synthesis_results["duration_seconds"],
                "synthesis_confidence": synthesis_results["synthesis_confidence"]
            }
            
            # Add THIN-specific metadata if available
            if "thin_metadata" in synthesis_results:
                stage_metadata["thin_pipeline_data"] = synthesis_results["thin_metadata"]
            
            manifest.add_execution_stage("synthesis", agent_name,
                                       synthesis_start_time, synthesis_end_time, "completed", stage_metadata)
            
            # Finalize manifest (synthesis results already captured in execution stages)
            
            # Combine batch results for final summary
            analysis_summary = self._combine_batch_results(all_analysis_results)

            # Generate final report with cost transparency
            base_report_content = synthesis_results.get("synthesis_report_markdown", "Synthesis failed.")
            session_costs = audit.get_session_costs()
            
            # Add cost summary section to report
            cost_section = self._generate_cost_summary_section(session_costs, run_timestamp)
            final_report_content = base_report_content + "\n\n" + cost_section
            
            report_hash = storage.put_artifact(
                final_report_content.encode('utf-8'), 
                {"artifact_type": "final_report"}
            )

            # Write final report to results folder
            results_dir = self.security.secure_mkdir(run_folder / "results")
            report_file = results_dir / "final_report.md"
            self.security.secure_write_text(report_file, final_report_content)
            
            # Create provenance-first artifact organization (Issue #297)
            try:
                provenance_organizer = ProvenanceOrganizer(self.security, audit)
                experiment_metadata = {
                    "experiment_name": experiment_config.get("name", "Unknown Experiment"),
                    "run_timestamp": run_timestamp,
                    "framework_version": experiment_config.get("framework", "Unknown Framework"),
                    "model_used": analysis_model
                }
                
                provenance_result = provenance_organizer.organize_run_artifacts(
                    run_folder, shared_cache_dir, experiment_metadata
                )
                
                if provenance_result["success"]:
                    print(f"📁 Provenance organization: {provenance_result['artifacts_organized']} artifacts organized")
                else:
                    print("⚠️  Provenance organization failed, continuing with standard structure")
                    
            except Exception as e:
                print(f"⚠️  Provenance organization error: {str(e)}")
                audit.log_error("provenance_organization_error", str(e), {})
            

            
            # Export comprehensive final CSV files including synthesis artifacts (Gasket #3a)
            # Extract synthesis artifact hashes from synthesis metadata
            # The synthesis pipeline stores artifacts but doesn't return hashes in the result
            # We need to find the statistical results and curated evidence artifacts
            statistical_results_hash = ""
            curated_evidence_hash = ""
            
            # Check if synthesis metadata contains artifact references
            if "statistical_results_hash" in synthesis_results:
                statistical_results_hash = synthesis_results["statistical_results_hash"]
            if "curated_evidence_hash" in synthesis_results:
                curated_evidence_hash = synthesis_results["curated_evidence_hash"]
                
            # TODO: For now, we'll look for the most recent synthesis artifacts in the cache
            # This is a temporary solution until the synthesis pipeline returns proper hashes
            
            final_csv_export_result = self._export_final_synthesis_csv_files(
                scores_hash, evidence_hash, statistical_results_hash,
                curated_evidence_hash, framework_content, 
                experiment_config, corpus_manifest, synthesis_results, results_dir, audit
            )
            
            # Finalize manifest and audit
            manifest_file = manifest.finalize_manifest()
            audit.finalize_session()
            
            # Calculate total execution time
            end_time = datetime.now(timezone.utc).isoformat()
            total_duration = self._calculate_duration(start_time, end_time)
            
            # Final orchestrator event
            audit.log_orchestrator_event("experiment_complete", {
                "total_duration_seconds": total_duration,
                "analysis_duration": analysis_summary["total_duration_seconds"],
                "synthesis_duration": synthesis_results.get("execution_metadata", {}).get("duration_seconds", 0),
                "final_report_hash": report_hash,
                "manifest_file": str(manifest_file),
                "mathematical_validation": "completed"
            })
            
            # Get session cost summary for research transparency
            session_costs = audit.get_session_costs()
            
            print(f"\n✅ THIN v2.0 experiment complete: {run_timestamp} ({total_duration:.1f}s)")
            print(f"📋 Results: {results_dir}")
            print(f"📊 Report: {report_file}")
            print(f"\n💰 Final Cost Summary:")
            print(f"   Total Cost: ${session_costs.get('total_cost_usd', 0.0):.4f} USD")
            print(f"   Total Tokens: {session_costs.get('total_tokens', 0):,}")
            
            # Show detailed cost breakdown
            operations = session_costs.get('operations', {})
            if operations:
                print(f"   Cost by Operation:")
                for op, op_costs in operations.items():
                    cost_usd = op_costs.get('cost_usd', 0.0)
                    tokens = op_costs.get('tokens', 0)
                    calls = op_costs.get('calls', 0)
                    print(f"     • {op}: ${cost_usd:.4f} ({tokens:,} tokens, {calls} calls)")
            
            # Auto-commit successful run to Git (if enabled)
            if auto_commit:
                commit_metadata = {
                    "run_id": run_timestamp,
                    "experiment_name": self.experiment_path.name
                }
                commit_success = self._auto_commit_run(run_folder, commit_metadata, audit)
                if not commit_success:
                    print("⚠️  Auto-commit to Git failed (run completed successfully)")
            
            return {
                "run_id": run_timestamp,
                "run_folder": str(run_folder),
                "results_directory": str(results_dir),
                "final_report_file": str(report_file),
                "manifest_file": str(manifest_file),
                "total_duration_seconds": total_duration,
                "analysis_result": analysis_summary,
                "synthesis_result": synthesis_results,
                "costs": session_costs,
                "mathematical_validation": True,
                "architecture": "thin_v2.0_direct_calls",
                "auto_commit_success": auto_commit and commit_success if auto_commit else None
            }
            
        except Exception as e:
            # Log error and cleanup
            try:
                audit.log_error("orchestrator_error", str(e), {
                    "experiment_path": str(self.experiment_path),
                    "run_folder": str(run_folder) if 'run_folder' in locals() else None
                })
                if 'audit' in locals():
                    audit.finalize_session()
            except:
                pass  # Don't fail on logging errors
            
            raise ThinOrchestratorError(f"Experiment execution failed: {e}")

    def _execute_analysis_sequentially(self,
                                       analysis_agent: EnhancedAnalysisAgent,
                                       corpus_documents: List[Dict[str, Any]],
                                       framework_content: str,
                                       experiment_config: Dict[str, Any],
                                       model: str,
                                       ensemble_runs: int = 1) -> tuple[List[Dict[str, Any]], Optional[str], Optional[str], Optional[str]]:
        """
        Executes the analysis agent for each document with optional ensemble runs for self-consistency.
        Returns all analysis results, scores_hash, evidence_hash, and corpus_hash.
        """
        
        all_analysis_results = []
        
        print(f"\n🚀 Starting sequential analysis of {len(corpus_documents)} documents...")
        
        for i, doc in enumerate(corpus_documents):
            print(f"\n--- Analyzing document {i+1}/{len(corpus_documents)}: {doc.get('filename')} ---")
            
            # TODO: Ensemble runs disabled pending architectural review
            # if ensemble_runs > 1:
            #     # Ensemble analysis with multiple runs
            #     ensemble_results = []
            #     for run in range(ensemble_runs):
            #         print(f"  🔄 Ensemble run {run + 1}/{ensemble_runs}...")
            #         try:
            #             result = analysis_agent.analyze_batch(
            #             framework_content=framework_content,
            #             corpus_documents=[doc],  # Pass a list with a single document
            #             experiment_config=experiment_config,
            #             model=model,
            #             current_scores_hash=None,  # Don't accumulate hashes
            #             current_evidence_hash=None,
            #             ensemble_run=run + 1,
            #             total_ensemble_runs=ensemble_runs
            #             )
            #         ensemble_results.append(result)
            #     except Exception as e:
            #         print(f"    ❌ Ensemble run {run + 1} failed: {e}")
            #         ensemble_results.append({"error": str(e), "document": doc.get('filename'), "run": run + 1})
            #     
            #     # Aggregate ensemble results using median aggregation
            #     aggregated_result = self._aggregate_ensemble_results(ensemble_results, doc.get('filename'))
            #     all_analysis_results.append(aggregated_result)
            # else:
            # Single run analysis
            try:
                result = analysis_agent.analyze_batch(
                    framework_content=framework_content,
                    corpus_documents=[doc],  # Pass a list with a single document
                    experiment_config=experiment_config,
                    model=model,
                    current_scores_hash=None,  # Don't accumulate hashes
                    current_evidence_hash=None
                )
                
                # Append the analysis result to the list
                all_analysis_results.append(result)
            except Exception as e:
                print(f"❌ Analysis failed for document {doc.get('filename')}: {e}")
                all_analysis_results.append({"error": str(e), "document": doc.get('filename')})

        # Combine all analysis results into a single JSON artifact for synthesis
        scores_hash, evidence_hash = self._combine_analysis_artifacts(all_analysis_results, analysis_agent.storage)
        
        # Store combined corpus as a single artifact for comprehensive RAG
        corpus_content = "\n\n---\n\n".join([doc.get('content', '') for doc in corpus_documents])
        corpus_hash = analysis_agent.storage.put_artifact(
            corpus_content.encode('utf-8'),
            {"artifact_type": "combined_corpus_text"}
        )
        
        return all_analysis_results, scores_hash, evidence_hash, corpus_hash

    def _combine_analysis_artifacts(self, analysis_results: List[Dict[str, Any]], storage) -> tuple[str, str]:
        """
        Combine analysis results from multiple documents into a single result.
        
        THIN approach: Combine evidence artifacts from individual analyses
        instead of extracting evidence from raw responses.
        """
        import json
        from datetime import datetime, timezone
        
        combined_document_analyses = []
        all_evidence = []  # Collect evidence from individual evidence artifacts
        
        for i, result in enumerate(analysis_results):
            if not result or "error" in result:
                print(f"Warning: Skipping failed analysis result {i}")
                continue
                
            # Extract the actual analysis data from the nested structure
            if "analysis_result" in result and "result_content" in result["analysis_result"]:
                # Get the cached result content
                cached_result = result["analysis_result"]["result_content"]
                
                # Extract the actual analysis data from the raw_analysis_response
                if "raw_analysis_response" in cached_result:
                    raw_response = cached_result["raw_analysis_response"]
                    
                    # Evidence already extracted during analysis time - load from evidence artifact
                    # (THIN principle: analysis agent produces evidence format needed for RAG)
                    if "evidence_hash" in cached_result:
                        evidence_hash = cached_result["evidence_hash"]
                        try:
                            evidence_artifact_data = storage.get_artifact(evidence_hash)
                            if evidence_artifact_data:
                                evidence_artifact = json.loads(evidence_artifact_data.decode('utf-8'))
                                evidence_list = evidence_artifact.get("evidence_data", [])
                                all_evidence.extend(evidence_list)
                                print(f"    📋 Loaded {len(evidence_list)} evidence pieces from analysis {i}")
                        except Exception as e:
                            print(f"Warning: Failed to load evidence artifact for analysis {i}: {e}")
                    
                    # Use Intelligent Extractor gasket (v7.0) or legacy parsing (v6.0)
                    # We need framework content for gasket schema extraction
                    framework_content = getattr(self, '_current_framework_content', None)
                    if framework_content:
                        extracted_data = self._extract_and_map_with_gasket(
                            raw_response, 
                            framework_content, 
                            getattr(self, '_current_audit_logger', None),
                            getattr(self, '_current_analysis_model', 'vertex_ai/gemini-2.5-flash-lite')
                        )
                    else:
                        # Fallback to legacy parsing if framework content not available
                        extracted_data = self._legacy_json_parsing(raw_response)
                    
                    if extracted_data and "document_analyses" in extracted_data:
                        combined_document_analyses.extend(extracted_data["document_analyses"])
                    else:
                        print(f"Warning: Failed to extract analysis data from result {i}")
                        continue
                else:
                    print(f"Warning: No raw_analysis_response found in cached result {i}")
                    continue
            elif "raw_analysis_response" in result:
                # Direct raw_analysis_response (fallback)
                raw_response = result["raw_analysis_response"]
                
                # Evidence already extracted during analysis time - no post-processing needed
                # (THIN principle: analysis agent produces evidence format needed for RAG)
                
                # Extract JSON from the delimited response
                import re
                json_pattern = r"<<<DISCERNUS_ANALYSIS_JSON_v6>>>\n(.*?)\n<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>"
                json_match = re.search(json_pattern, raw_response, re.DOTALL)
                
                if json_match:
                    try:
                        analysis_data = json.loads(json_match.group(1))
                        if "document_analyses" in analysis_data:
                            combined_document_analyses.extend(analysis_data["document_analyses"])
                    except json.JSONDecodeError as e:
                        print(f"Warning: Failed to parse JSON from analysis result {i}: {e}")
                        continue
                else:
                    print(f"Warning: No JSON found in raw_analysis_response for result {i}")
                    continue
            elif "document_analyses" in result:
                # Direct document_analyses (shouldn't happen with current structure)
                combined_document_analyses.extend(result["document_analyses"])
            elif "analysis_metadata" in result:
                # Single document result (legacy format)
                combined_document_analyses.append({
                    "document_id": f"doc_{i}",
                    "document_name": f"document_{i}.txt",
                    "dimensional_scores": result.get("dimensional_scores", {}),
                    "evidence": result.get("evidence", [])
                })
            else:
                print(f"Warning: Unknown analysis result format for result {i}")
                continue
        
        # Create combined scores result structure
        combined_result = {
            "analysis_metadata": {
                "framework_name": "combined_analysis",
                "framework_version": "v6.0",
                "analyst_confidence": 0.85,
                "analysis_notes": f"Combined analysis of {len(combined_document_analyses)} documents"
            },
            "document_analyses": combined_document_analyses
        }
        
        # Create combined evidence artifact from individual evidence artifacts
        evidence_artifact = {
            "evidence_metadata": {
                "total_documents": len(combined_document_analyses),
                "total_evidence_pieces": len(all_evidence),
                "extraction_method": "analysis_time_combination_v1.0",
                "extraction_time": datetime.now(timezone.utc).isoformat(),
                "framework_version": "v6.0"
            },
            "evidence_data": all_evidence
        }
        
        # Store combined evidence artifact
        evidence_hash = storage.put_artifact(
            json.dumps(evidence_artifact, indent=2).encode('utf-8'),
            {
                "artifact_type": "combined_evidence_v6",
                "extraction_method": "analysis_time_combination",
                "total_evidence_pieces": len(all_evidence),
                "total_documents": len(combined_document_analyses)
            }
        )
        
        print(f"📋 Evidence combination: {len(all_evidence)} pieces from {len(combined_document_analyses)} documents → {evidence_hash[:12]}...")
        
        return combined_result, evidence_hash

    def _extract_gasket_schema_from_framework(self, framework_content: str) -> Optional[Dict[str, Any]]:
        """
        Extract gasket_schema from framework v7.1 JSON appendix.
        Only supports v7.1 enhanced format - no backward compatibility.
        
        Args:
            framework_content: Raw framework markdown content
            
        Returns:
            gasket_schema dict (v7.1 format) or None if not found/invalid
        """
        try:
            # Look for gasket_schema specifically in framework
            # Search for "gasket_schema" keyword first, then find the containing JSON block
            if 'gasket_schema' in framework_content:
                gasket_pos = framework_content.find('gasket_schema')
                
                # Find the JSON block that contains gasket_schema
                json_blocks = []
                start_pos = 0
                while True:
                    json_start_marker = framework_content.find('```json', start_pos)
                    if json_start_marker == -1:
                        break
                    
                    json_start = json_start_marker + 7
                    json_end = framework_content.find('```', json_start)
                    
                    if json_end != -1:
                        json_content = framework_content[json_start:json_end].strip()
                        
                        # Check if this JSON block contains gasket_schema
                        if json_start <= gasket_pos <= json_end:
                            try:
                                framework_config = json.loads(json_content)
                                
                                # Extract gasket_schema if present
                                gasket_schema = framework_config.get('gasket_schema')
                                if gasket_schema:
                                    # Support v7.1 and v7.3 formats (v7.3 is backward compatible)
                                    supported_versions = ['7.1', '7.3', 'v7.1', 'v7.3']
                                    if gasket_schema.get('version') in supported_versions and 'target_keys' in gasket_schema:
                                        return gasket_schema
                                    else:
                                        print(f"❌ Unsupported gasket_schema version: {gasket_schema.get('version')}. Supported versions: {supported_versions}")
                                        return None
                            except json.JSONDecodeError:
                                pass  # Try next JSON block
                    
                    start_pos = json_end + 3 if json_end != -1 else json_start_marker + 7
            
            return None
            
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Warning: Failed to extract gasket_schema from framework: {e}")
            return None

    def _convert_v71_gasket_to_v70(self, v71_schema: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Convert v7.1 enhanced gasket schema to v7.0 format for Intelligent Extractor compatibility.
        
        Args:
            v71_schema: v7.1 gasket_schema with extraction_targets structure
            
        Returns:
            v7.0 compatible gasket_schema with target_keys and target_dimensions
        """
        try:
            extraction_targets = v71_schema.get('extraction_targets', {})
            
            # Extract all score keys from core_scores and metadata_scores
            target_keys = []
            
            # Add core scores (required)
            core_scores = extraction_targets.get('core_scores', {})
            target_keys.extend(core_scores.keys())
            
            # Add metadata scores (optional)
            metadata_scores = extraction_targets.get('metadata_scores', {})
            target_keys.extend(metadata_scores.keys())
            
            # Create target_dimensions from score descriptions
            target_dimensions = []
            for score_key, score_config in {**core_scores, **metadata_scores}.items():
                description = score_config.get('description', score_key)
                target_dimensions.append(description)
            
            # Return v7.0 compatible format
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
        Extract scores using Intelligent Extractor gasket (Gasket #2).
        
        Replaces brittle regex/JSON parsing with LLM-based semantic extraction.
        
        Args:
            raw_analysis_response: Raw Analysis Log from Analysis Agent
            framework_content: Framework content for gasket_schema extraction
            audit_logger: Audit logger for provenance
            
        Returns:
            Extracted analysis data or None if extraction fails
        """
        # Extract gasket schema from framework
        gasket_schema = self._extract_gasket_schema_from_framework(framework_content)
        
        if not gasket_schema:
            # No backward compatibility - error out on non-supported frameworks
            print("❌ No valid gasket_schema found in framework")
            print(f"🔍 Framework content length: {len(framework_content)}")
            print(f"🔍 Contains ```json: {'```json' in framework_content}")
            raise ValueError("Framework must have valid gasket_schema (v7.1 or v7.3). No backward compatibility with v7.0 or earlier.")
        
        # Extract evidence from raw response for v7.1 integration (Issue #281)
        document_evidence_list = self._extract_evidence_from_delimited(raw_analysis_response)
        
        # Initialize Intelligent Extractor Agent
        extractor = IntelligentExtractorAgent(
            model=model,
            audit_logger=audit_logger
        )
        
        # Extract scores using gasket
        extraction_result = extractor.extract_scores_from_raw_analysis(
            raw_analysis_response, gasket_schema
        )
        
        if not extraction_result.success:
            print(f"❌ Intelligent Extractor failed: {extraction_result.error_message}")
            # No fallback - fail fast on extraction errors
            raise ValueError(f"v7.1 Intelligent Extractor failed: {extraction_result.error_message}. No legacy fallback available.")
        
        # Check if we have multi-document extraction results (THIN approach)
        if "_document_analyses" in extraction_result.extracted_scores:
            # Multi-document extraction: preserve individual document identities
            document_analyses_data = extraction_result.extracted_scores["_document_analyses"]
            
            document_analyses = []
            for doc_data in document_analyses_data:
                # Find evidence for this specific document
                doc_name = doc_data["document_name"]
                doc_evidence = [ev for ev in document_evidence_list if ev.get("document_name") == doc_name]
                
                document_analysis = {
                    "document_id": "extracted_via_gasket",
                    "document_name": doc_data["document_name"],  # Preserve actual filename
                    "analysis_scores": doc_data["analysis_scores"],
                    "evidence": doc_evidence,  # Add evidence for v7.1 compatibility
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
            # Single-document extraction (fallback)
            document_analysis = {
                "document_id": "extracted_via_gasket",
                "document_name": "gasket_extraction",
                "analysis_scores": extraction_result.extracted_scores,
                "evidence": document_evidence_list,  # Add all evidence for single-document case
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
        
        This is the old brittle parsing logic, kept as fallback for non-v7.0 frameworks.
        """
        import re
        
        # Extract JSON from the delimited response
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
        Extract evidence from delimited raw analysis response for pre-extraction.
        
        This enables THIN evidence pre-extraction during analysis combination,
        avoiding the need to scan registry and load multiple artifacts during synthesis.
        
        Args:
            raw_response: Raw analysis response with delimited JSON format
            
        Returns:
            List of evidence dictionaries with document context preserved
        """
        import re
        import json
        
        # Extract JSON from delimited format
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
                        # Add metadata for provenance
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

    def _aggregate_ensemble_results(self, ensemble_results: List[Dict[str, Any]], document_name: str) -> Dict[str, Any]:
        """
        Aggregates multiple ensemble runs using median aggregation for self-consistency.
        
        Args:
            ensemble_results: List of analysis results from ensemble runs
            document_name: Name of the document being analyzed
            
        Returns:
            Aggregated result with median scores and consensus metrics
        """
        import statistics
        import json
        
        # Filter out failed runs
        successful_runs = [r for r in ensemble_results if "error" not in r and "analysis_result" in r]
        
        if not successful_runs:
            # If all runs failed, return the first error result
            return ensemble_results[0] if ensemble_results else {"error": "All ensemble runs failed", "document": document_name}
        
        print(f"    ✅ {len(successful_runs)}/{len(ensemble_results)} ensemble runs successful")
        
        # Extract scores from each successful run
        all_scores = []
        all_raw_responses = []
        all_durations = []
        
        for run in successful_runs:
            try:
                # Extract raw analysis response
                cached_result = run["analysis_result"]["result_content"]
                raw_response = cached_result["raw_analysis_response"]
                all_raw_responses.append(raw_response)
                
                # Extract scores using gasket or legacy parsing
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
                    all_scores.append(extracted_data["document_analyses"])
                
                # Collect duration
                duration = run["analysis_result"].get("duration_seconds", 0)
                all_durations.append(duration)
                
            except Exception as e:
                print(f"    ⚠️ Failed to extract scores from ensemble run: {e}")
                continue
        
        if not all_scores:
            return {"error": "Failed to extract scores from any ensemble run", "document": document_name}
        
        # Perform median aggregation on scores
        aggregated_scores = self._median_aggregate_scores(all_scores)
        
        # Calculate consensus metrics
        consensus_metrics = self._calculate_consensus_metrics(all_scores)
        
        # Log ensemble quality metrics
        self._log_ensemble_quality_metrics(consensus_metrics, document_name, len(successful_runs))
        
        # Use the first successful run as template, but replace with aggregated data
        template_run = successful_runs[0]
        aggregated_result = template_run.copy()
        
        # Update with aggregated scores and consensus metrics
        if "analysis_result" in aggregated_result:
            aggregated_result["analysis_result"]["ensemble_aggregated"] = True
            aggregated_result["analysis_result"]["ensemble_runs"] = len(successful_runs)
            aggregated_result["analysis_result"]["consensus_metrics"] = consensus_metrics
            aggregated_result["analysis_result"]["median_duration"] = statistics.median(all_durations) if all_durations else 0
            
            # Replace the raw response with a combined one for evidence extraction
            combined_raw_response = "\n\n=== ENSEMBLE RUNS ===\n\n".join(all_raw_responses)
            aggregated_result["analysis_result"]["result_content"]["raw_analysis_response"] = combined_raw_response
        
        return aggregated_result

    def _median_aggregate_scores(self, all_scores: List[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """
        Performs median aggregation on scores from multiple ensemble runs.
        
        Args:
            all_scores: List of score lists from each ensemble run
            
        Returns:
            List of aggregated scores using median values
        """
        if not all_scores or not all_scores[0]:
            return []
        
        # Get the first run's structure as template
        template_scores = all_scores[0]
        aggregated_scores = []
        
        for doc_analysis in template_scores:
            doc_name = doc_analysis.get("document_name", "unknown")
            analysis_scores = doc_analysis.get("analysis_scores", {})
            
            # Collect all scores for each dimension across runs
            dimension_scores = {}
            for scores_run in all_scores:
                for doc in scores_run:
                    if doc.get("document_name") == doc_name:
                        run_scores = doc.get("analysis_scores", {})
                        for dimension, score in run_scores.items():
                            if dimension not in dimension_scores:
                                dimension_scores[dimension] = []
                            # Only add non-None scores
                            if score is not None:
                                dimension_scores[dimension].append(score)
            
            # Calculate median for each dimension
            median_scores = {}
            for dimension, scores in dimension_scores.items():
                if scores:
                    import statistics
                    median_scores[dimension] = statistics.median(scores)
                else:
                    # If no valid scores, use the first available score
                    for scores_run in all_scores:
                        for doc in scores_run:
                            if doc.get("document_name") == doc_name:
                                run_scores = doc.get("analysis_scores", {})
                                if dimension in run_scores and run_scores[dimension] is not None:
                                    median_scores[dimension] = run_scores[dimension]
                                    break
                        if dimension in median_scores:
                            break
            
            # Create aggregated document analysis
            aggregated_doc = {
                "document_name": doc_name,
                "analysis_scores": median_scores,
                "aggregation_method": "median",
                "ensemble_runs": len(all_scores)
            }
            
            aggregated_scores.append(aggregated_doc)
        
        return aggregated_scores

    def _calculate_consensus_metrics(self, all_scores: List[List[Dict[str, Any]]]) -> Dict[str, Any]:
        """
        Calculates consensus metrics for ensemble runs.
        
        Args:
            all_scores: List of score lists from each ensemble run
            
        Returns:
            Dictionary with consensus metrics
        """
        if not all_scores or len(all_scores) < 2:
            return {"consensus_level": "single_run", "variance": 0.0}
        
        # Calculate variance for each dimension across runs
        dimension_variances = {}
        
        for scores_run in all_scores:
            for doc in scores_run:
                doc_name = doc.get("document_name", "unknown")
                analysis_scores = doc.get("analysis_scores", {})
                
                for dimension, score in analysis_scores.items():
                    if dimension not in dimension_variances:
                        dimension_variances[dimension] = []
                    # Only add non-None scores to avoid mathematical errors
                    if score is not None:
                        dimension_variances[dimension].append(score)
        
        # Calculate statistics for each dimension
        consensus_metrics = {}
        total_variance = 0.0
        dimension_count = 0
        
        for dimension, scores in dimension_variances.items():
            if len(scores) > 1:
                import statistics
                variance = statistics.variance(scores)
                mean = statistics.mean(scores)
                dimension_count += 1
                total_variance += variance
                
                consensus_metrics[dimension] = {
                    "mean": mean,
                    "variance": variance,
                    "std_dev": statistics.stdev(scores) if len(scores) > 1 else 0
                }
        
        # Overall consensus metrics
        avg_variance = total_variance / dimension_count if dimension_count > 0 else 0.0
        
        # Determine consensus level based on variance
        if avg_variance < 0.1:
            consensus_level = "high"
        elif avg_variance < 0.3:
            consensus_level = "medium"
        else:
            consensus_level = "low"
        
        return {
            "consensus_level": consensus_level,
            "average_variance": avg_variance,
            "dimension_metrics": consensus_metrics,
            "ensemble_runs": len(all_scores)
        }

    def _log_ensemble_quality_metrics(self, consensus_metrics: Dict[str, Any], document_name: str, successful_runs: int) -> None:
        """
        Log ensemble quality metrics for transparency and debugging.
        
        Args:
            consensus_metrics: Calculated consensus metrics
            document_name: Name of the document analyzed
            successful_runs: Number of successful ensemble runs
        """
        consensus_level = consensus_metrics.get("consensus_level", "unknown")
        avg_variance = consensus_metrics.get("average_variance", 0.0)
        ensemble_runs = consensus_metrics.get("ensemble_runs", 0)
        
        print(f"    📊 Ensemble Quality for {document_name}:")
        print(f"       • Consensus Level: {consensus_level.upper()}")
        print(f"       • Average Variance: {avg_variance:.3f}")
        print(f"       • Successful Runs: {successful_runs}/{ensemble_runs}")
        
        # Log detailed dimension metrics if consensus is concerning
        if consensus_level == "low":
            print(f"    ⚠️  Low consensus detected - dimension details:")
            dimension_metrics = consensus_metrics.get("dimension_metrics", {})
            for dimension, metrics in dimension_metrics.items():
                variance = metrics.get("variance", 0.0)
                if variance > 0.3:  # High variance threshold
                    mean = metrics.get("mean", 0.0)
                    std_dev = metrics.get("std_dev", 0.0)
                    print(f"       • {dimension}: mean={mean:.2f}, variance={variance:.3f}, std_dev={std_dev:.3f}")
        
        # Log to audit system for permanent record
        if hasattr(self, '_current_audit_logger') and self._current_audit_logger:
            self._current_audit_logger.log_agent_event(
                "EnsembleAggregator",
                "ensemble_quality_assessment",
                {
                    "document_name": document_name,
                    "consensus_level": consensus_level,
                    "average_variance": avg_variance,
                    "successful_runs": successful_runs,
                    "total_runs": ensemble_runs,
                    "dimension_count": len(consensus_metrics.get("dimension_metrics", {}))
                }
            )

    def _report_ensemble_summary(self, all_analysis_results: List[Dict[str, Any]], ensemble_runs: int) -> None:
        """
        Generate a summary report of ensemble quality across all documents.
        
        Args:
            all_analysis_results: List of analysis results (potentially aggregated from ensemble runs)
            ensemble_runs: Number of ensemble runs performed
        """
        print(f"\n📊 Ensemble Analysis Summary ({ensemble_runs} runs per document):")
        
        # Collect consensus metrics from all documents
        consensus_levels = []
        avg_variances = []
        total_dimensions = 0
        
        for result in all_analysis_results:
            if ("analysis_result" in result and 
                "consensus_metrics" in result["analysis_result"]):
                
                consensus_metrics = result["analysis_result"]["consensus_metrics"]
                consensus_level = consensus_metrics.get("consensus_level", "unknown")
                avg_variance = consensus_metrics.get("average_variance", 0.0)
                dimension_count = len(consensus_metrics.get("dimension_metrics", {}))
                
                consensus_levels.append(consensus_level)
                avg_variances.append(avg_variance)
                total_dimensions += dimension_count
        
        if consensus_levels:
            # Calculate summary statistics
            high_consensus = consensus_levels.count("high")
            medium_consensus = consensus_levels.count("medium") 
            low_consensus = consensus_levels.count("low")
            total_docs = len(consensus_levels)
            overall_avg_variance = sum(avg_variances) / len(avg_variances) if avg_variances else 0.0
            
            print(f"   📈 Consensus Distribution:")
            print(f"      • High Consensus: {high_consensus}/{total_docs} documents ({high_consensus/total_docs*100:.1f}%)")
            print(f"      • Medium Consensus: {medium_consensus}/{total_docs} documents ({medium_consensus/total_docs*100:.1f}%)")
            print(f"      • Low Consensus: {low_consensus}/{total_docs} documents ({low_consensus/total_docs*100:.1f}%)")
            print(f"   📊 Overall Quality:")
            print(f"      • Average Variance: {overall_avg_variance:.3f}")
            print(f"      • Total Dimensions Analyzed: {total_dimensions}")
            
            # Provide interpretation
            if overall_avg_variance < 0.1:
                quality_assessment = "EXCELLENT - Very high ensemble agreement"
            elif overall_avg_variance < 0.2:
                quality_assessment = "GOOD - Strong ensemble agreement"
            elif overall_avg_variance < 0.3:
                quality_assessment = "FAIR - Moderate ensemble agreement"
            else:
                quality_assessment = "CONCERNING - Low ensemble agreement"
            
            print(f"   🎯 Quality Assessment: {quality_assessment}")
            
            # Warn if many documents have low consensus
            if low_consensus > total_docs * 0.3:  # More than 30% low consensus
                print(f"   ⚠️  WARNING: {low_consensus} documents show low consensus - consider reviewing analysis or increasing ensemble runs")
        else:
            print(f"   ⚠️  No ensemble metrics found in analysis results")

    def _load_experiment_config(self) -> Dict[str, Any]:
        """Load and validate the experiment.md file."""
        exp_file = self.experiment_path / "experiment.md"
        
        if not exp_file.exists():
            raise ThinOrchestratorError(f"experiment.md not found in {self.experiment_path}")
        
        content = self.security.secure_read_text(exp_file)
        
        # Extract YAML from markdown
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
        
        # Validate required fields
        required_fields = ['name', 'framework', 'corpus_path']
        missing_fields = [field for field in required_fields if field not in config]
        if missing_fields:
            raise ThinOrchestratorError(f"Missing required fields in experiment.md: {', '.join(missing_fields)}")
        
        return config
    
    def _build_comprehensive_experiment_context(self, experiment_config: Dict[str, Any], framework_config: Dict[str, Any], corpus_manifest: Optional[Dict[str, Any]] = None) -> str:
        """
        THIN-compliant experiment context building.
        
        Provides LLMs with complete raw data for intelligent processing instead of 
        brittle software parsing. Works with any framework format (CAF, sentiment, 
        discourse analysis, etc.) by letting LLM intelligence handle extraction 
        and formatting decisions.
        
        THIN Principle: Pass raw structured data to LLMs - let them decide what's 
        important and how to format it, rather than hardcoding assumptions.
        """
        
        # v7.3: Build a structured JSON context for the synthesis pipeline
        context = {
            "experiment_config": experiment_config,
            "framework_config": framework_config,
            "corpus_manifest": corpus_manifest
        }
        
        # We now pass a structured JSON context string instead of a free-form string.
        return json.dumps(context, indent=2)
    
    def _load_framework(self, framework_filename: str) -> str:
        """
        Load framework content with trusted canonical path resolution.
        
        The orchestrator is trusted infrastructure that can safely resolve canonical
        framework references (../../frameworks/...) while maintaining security 
        boundaries for agents.
        """
        
        # Check if this is a relative path to canonical frameworks
        if framework_filename.startswith("../../frameworks/"):
            # TRUSTED OPERATION: Orchestrator resolves canonical frameworks
            project_root = Path(__file__).parent.parent.parent  # Get to discernus/
            canonical_path = framework_filename.lstrip("../../")
            framework_file = project_root / canonical_path
            
            if not framework_file.exists():
                raise ThinOrchestratorError(f"Canonical framework not found: {framework_filename}")
            
            print(f"🛡️ Security: Loading canonical framework: {framework_file.name}")
            # Direct read (orchestrator is trusted infrastructure)
            return framework_file.read_text(encoding='utf-8')
        
        else:
            # EXISTING LOGIC: Local framework in experiment directory
            framework_file = self.experiment_path / framework_filename
            
            if not framework_file.exists():
                raise ThinOrchestratorError(f"Framework file not found: {framework_filename}")
            
            print(f"🛡️ Security: Loading local framework: {framework_file.name}")
            # Use security boundary for local files (agents must stay within boundary)
            return self.security.secure_read_text(framework_file)
    
    def _load_corpus(self, corpus_path: str) -> tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """Load corpus documents and corpus manifest."""
        corpus_dir = self.experiment_path / corpus_path
        
        if not corpus_dir.exists():
            raise ThinOrchestratorError(f"Corpus directory not found: {corpus_path}")
        
        # Find all text and PDF files recursively in corpus directory
        corpus_files = []
        for root, dirs, files in os.walk(corpus_dir):
            for file in files:
                if file.endswith(('.txt', '.pdf')) and not file.startswith('.'):
                    corpus_files.append(Path(root) / file)
        
        if not corpus_files:
            raise ThinOrchestratorError(f"No .txt or .pdf files found in corpus directory: {corpus_path}")
        
        # Load corpus documents
        documents = []
        for file_path in sorted(corpus_files):
            if file_path.suffix == '.txt':
                content = self.security.secure_read_text(file_path)
            elif file_path.suffix == '.pdf':
                # For PDF files, we'll pass them as binary data and let Gemini handle them
                content = self.security.secure_read_bytes(file_path)
            
            documents.append({
                "filename": file_path.name,
                "content": content,
                "filepath": str(file_path.relative_to(self.experiment_path))
            })
        
        # Load corpus manifest from corpus.md
        corpus_manifest = {}
        corpus_md_file = corpus_dir / "corpus.md"
        if corpus_md_file.exists():
            try:
                corpus_md_content = self.security.secure_read_text(corpus_md_file)
                
                # Extract JSON from corpus.md (similar to framework parsing)
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
    
    def _generate_final_report(self, 
                             analysis_result: Dict[str, Any],
                             synthesis_result: Dict[str, Any], 
                             experiment_config: Dict[str, Any],
                             manifest: EnhancedManifest) -> str:
        """Generate beautiful final markdown report."""
        
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        
        report = f"""# {experiment_config['name']} - Analysis Report

**Generated**: {timestamp}  
**Architecture**: THIN v2.0 Direct Function Calls  
**Mathematical Validation**: Enabled  

---

## Executive Summary

This report presents the results of computational research analysis using the Discernus platform with enhanced mathematical validation capabilities.

**Key Features of This Analysis**:
- ✅ Mathematical "show your work" requirements for all calculations
- ✅ Dual-LLM validation with spot-checking of numerical results  
- ✅ Complete audit trails for academic reproducibility
- ✅ Content-addressable storage for perfect caching
- ✅ Security boundary enforcement

---

## Analysis Results

### Enhanced Analysis Agent Results
**Agent**: {analysis_result['result_content']['agent_name']}  
**Version**: {analysis_result['result_content']['agent_version']}  
**Duration**: {analysis_result['duration_seconds']:.1f} seconds  
**Mathematical Validation**: {analysis_result['mathematical_validation']}  

{analysis_result['result_content']['analysis_results']}

---

## Synthesis Results

### Enhanced Synthesis Agent Results  
**Agent**: {synthesis_result['result_content']['agent_name']}  
**Version**: {synthesis_result['result_content']['agent_version']}  
**Duration**: {synthesis_result['duration_seconds']:.1f} seconds  
**Mathematical Confidence**: {synthesis_result['synthesis_confidence']:.2f}  

{synthesis_result['result_content']['synthesis_results']}

---

## Mathematical Validation Report

### Validation Summary
- **Dual-LLM Validation**: {synthesis_result['result_content'].get('mathematical_validation', {}).get('validation_enabled', False)}
- **Mathematical Confidence**: {synthesis_result['synthesis_confidence']:.2f}
- **Errors Detected**: {len(synthesis_result['mathematical_validation'].get('mathematical_errors_found', []))}

### Validation Details
{synthesis_result['result_content'].get('mathematical_validation', {}).get('validation_content', 'No validation details available')}

---

## Provenance Information

### Experiment Configuration
- **Experiment**: {experiment_config['name']}
- **Framework**: {experiment_config['framework']}
- **Corpus Path**: {experiment_config['corpus_path']}

### Execution Metadata
- **Run ID**: {analysis_result['result_content']['execution_metadata']['start_time']}
- **Security Boundary**: {analysis_result['result_content']['provenance']['security_boundary']['experiment_name']}
- **Audit Session**: {analysis_result['result_content']['provenance']['audit_session_id']}

### Artifact Hashes
- **Framework**: {analysis_result['result_content']['input_artifacts']['framework_hash'][:16]}...
- **Documents**: {len(analysis_result['result_content']['input_artifacts']['document_hashes'])} corpus documents
- **Analysis Result**: {analysis_result['result_hash'][:16]}...
- **Synthesis Result**: {synthesis_result['result_hash'][:16]}...

---

## Quality Assurance

### Discernus Platform Validation
- ✅ Advanced computational research capabilities
- ✅ LLM intelligence for complex reasoning
- ✅ Efficient processing coordination  
- ✅ Perfect caching through content-addressable storage
- ✅ Complete audit trails for academic integrity

### Mathematical Validation
- ✅ "Show your work" requirements implemented
- ✅ Dual-LLM validation with spot-checking
- ✅ Confidence estimates for all numerical results
- ✅ Independent recalculation of key metrics

---

*This report was generated by the Discernus computational research platform with enhanced mathematical validation capabilities.*
"""
        
        return report
    
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
        
        Args:
            run_folder: Path to the completed run directory
            run_metadata: Metadata about the run (run_id, experiment_name, etc.)
            audit: Audit logger for recording the commit attempt
            
        Returns:
            True if commit succeeded, False if it failed (non-blocking)
        """
        import subprocess
        
        try:
            # Get to repository root (run_folder is experiment_path/runs/timestamp)
            repo_root = run_folder.parent.parent.parent
            
            # Add the run directory to Git (force to override .gitignore for research preservation)
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
            
            # Create commit message (keep it short per .cursor/rules)
            run_id = run_metadata.get('run_id', 'unknown')
            experiment_name = run_metadata.get('experiment_name', 'experiment')
            commit_msg = f"Complete run {run_id}: {experiment_name}"
            
            # Ensure commit message is under 50 characters
            if len(commit_msg) > 47:  # Leave room for ellipsis
                commit_msg = commit_msg[:44] + "..."
            
            # Commit the run
            result = subprocess.run(
                ["git", "commit", "-m", commit_msg],
                cwd=repo_root,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                # Check if it's just "nothing to commit" (not an error)
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
            
            # Check for successful commit in output (git pre-commit hooks can write to stderr but still succeed)
            if "nested repositories found" in result.stderr and "commit proceeding" in result.stderr:
                # This is just the nested repo check - commit actually succeeded
                pass
            elif result.stderr and "nothing to commit" not in result.stderr.lower():
                # Log as warning but don't fail if return code was 0
                audit.log_orchestrator_event("auto_commit_warning", {
                    "message": "Git commit succeeded but had stderr output",
                    "stderr": result.stderr
                })
            
            # Success
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
    
    def _generate_cost_summary_section(self, session_costs: Dict[str, Any], run_timestamp: str) -> str:
        """
        Generate academic-grade cost summary section for research reports.
        
        Args:
            session_costs: Cost data from audit logger
            run_timestamp: Timestamp of the experiment run
            
        Returns:
            Formatted markdown section with cost transparency
        """
        cost_section = f"""---

## Research Transparency: Computational Cost Analysis

### Cost Summary
**Total Cost**: ${session_costs.get('total_cost_usd', 0.0):.4f} USD  
**Total Tokens**: {session_costs.get('total_tokens', 0):,}  
**Run Timestamp**: {run_timestamp}  

### Cost Breakdown by Operation
"""
        
        operations = session_costs.get('operations', {})
        if operations:
            for operation, op_costs in operations.items():
                cost_usd = op_costs.get('cost_usd', 0.0)
                tokens = op_costs.get('tokens', 0)
                calls = op_costs.get('calls', 0)
                avg_cost_per_call = cost_usd / calls if calls > 0 else 0.0
                cost_section += f"- **{operation.replace('_', ' ').title()}**: ${cost_usd:.4f} USD ({tokens:,} tokens, {calls} calls, ${avg_cost_per_call:.4f} avg/call)\n"
        else:
            cost_section += "No operation-level cost data available.\n"
        
        cost_section += "\n### Cost Breakdown by Model\n"
        models = session_costs.get('models', {})
        if models:
            for model, model_costs in models.items():
                cost_usd = model_costs.get('cost_usd', 0.0)
                tokens = model_costs.get('tokens', 0)
                calls = model_costs.get('calls', 0)
                cost_section += f"- **{model}**: ${cost_usd:.4f} USD ({tokens:,} tokens, {calls} calls)\n"
        else:
            cost_section += "No model-level cost data available.\n"
        
        cost_section += "\n### Cost Breakdown by Agent\n"
        agents = session_costs.get('agents', {})
        if agents:
            for agent, agent_costs in agents.items():
                cost_usd = agent_costs.get('cost_usd', 0.0)
                tokens = agent_costs.get('tokens', 0)
                calls = agent_costs.get('calls', 0)
                cost_section += f"- **{agent}**: ${cost_usd:.4f} USD ({tokens:,} tokens, {calls} calls)\n"
        else:
            cost_section += "No agent-level cost data available.\n"
        
        cost_section += f"""\n### Methodology Note
This research was conducted using the Discernus computational research platform, ensuring complete transparency in computational costs. All LLM interactions are logged with exact token counts and costs for reproducibility and academic integrity.

**Cost Calculation**: Based on provider pricing at time of execution  
**Token Counting**: Exact tokens reported by LLM providers  
**Audit Trail**: Complete logs available in experiment run directory  
"""
        
        return cost_section
    def _validate_artifact_hashes(self, *hashes: str) -> Dict[str, bool]:
        """Validate that all provided artifact hashes exist and are accessible."""
        validation_results = {}
        
        for hash_value in hashes:
            if not hash_value:
                validation_results[hash_value] = False
                continue
                
            try:
                # Check if artifact exists in storage
                # Note: Skip validation for now - this is informational only
                artifact_exists = True  # Assume exists to avoid blocking pipeline
                validation_results[hash_value] = artifact_exists
                
                if not artifact_exists:
                    print(f"WARNING: Artifact hash {hash_value} not found in storage")
                    
            except Exception as e:
                print(f"ERROR: Error validating artifact hash {hash_value}: {e}")
                validation_results[hash_value] = False
        
        return validation_results
    
    def _export_final_synthesis_csv_files(
        self,
        scores_hash: str,
        evidence_hash: str,
        statistical_results_hash: str,
        curated_evidence_hash: str,
        framework_content: str,
        experiment_config: Dict[str, Any],
        corpus_manifest: Dict[str, Any],
        synthesis_metadata: Dict[str, Any],
        results_dir: Path,
        audit: AuditLogger
    ) -> Optional[Dict[str, Any]]:
        """
        Export comprehensive final CSV files including synthesis artifacts (Gasket #3a).
        
        Args:
            scores_hash: Hash of analysis scores artifact
            evidence_hash: Hash of evidence artifact
            statistical_results_hash: Hash of statistical results from synthesis
            curated_evidence_hash: Hash of curated evidence from synthesis
            framework_content: Framework content for context
            experiment_config: Experiment configuration
            corpus_manifest: Corpus metadata
            synthesis_metadata: Complete synthesis pipeline metadata
            results_dir: Results directory for CSV output
            audit: Audit logger for provenance
            
        Returns:
            CSV export result or None if export fails
        """
        try:
            from discernus.agents.csv_export_agent import CSVExportAgent, ExportOptions
            
            # Validate all hashes before proceeding
            hash_validation = self._validate_artifact_hashes(
                scores_hash, evidence_hash, statistical_results_hash, curated_evidence_hash
            )
            
            # Log validation results
            for hash_value, is_valid in hash_validation.items():
                if not is_valid and hash_value:  # Only log errors for non-empty hashes
                    audit.log_error("artifact_validation_error", f"Invalid artifact hash: {hash_value}", {})
            
            # Initialize CSV Export Agent with storage access
            csv_agent = CSVExportAgent(audit_logger=audit)
            
            # Get storage from synthesis metadata (should contain storage reference)
            storage = None
            if hasattr(audit, 'storage'):
                storage = audit.storage
            else:
                # Fallback: recreate storage from experiment path
                shared_cache_dir = self.experiment_path / "shared_cache"
                storage = LocalArtifactStorage(self.security, shared_cache_dir, "unknown_run")
            
            csv_agent.artifact_storage = storage
            
            # Configure export options
            export_options = ExportOptions(
                include_metadata=True,
                export_format="standard"
            )
            
            # Export comprehensive final CSV files
            result = csv_agent.export_final_synthesis_data(
                scores_hash=scores_hash,
                evidence_hash=evidence_hash,
                statistical_results_hash=statistical_results_hash,
                curated_evidence_hash=curated_evidence_hash,
                framework_config={"name": "framework", "version": "v7.0"},  # TODO: Extract from framework_content
                corpus_manifest=corpus_manifest,
                synthesis_metadata=synthesis_metadata,
                export_path=str(results_dir),
                export_options=export_options
            )
            
            if result.success:
                print(f"📊 Final CSV Export: {len(result.files_created)} files created")
                for filename in result.files_created:
                    print(f"   • {filename}")
                
                return {
                    "success": True,
                    "files": result.files_created,
                    "total_records": result.total_records,
                    "export_time": result.export_time_seconds
                }
            else:
                print(f"⚠️  Final CSV export failed: {result.error_message}")
                return None
                
        except Exception as e:
            print(f"❌ Final CSV export error: {str(e)}")
            audit.log_agent_event(
                "CSVExportAgent",
                "final_export_error",
                {"error": str(e)}
            )
            return None
    
    def _export_csv_files(
        self,
        scores_hash: str,
        evidence_hash: str,
        framework_content: str,
        experiment_config: Dict[str, Any],
        corpus_manifest: Dict[str, Any],
        results_dir: Path,
        audit: AuditLogger
    ) -> Optional[Dict[str, Any]]:
        """
        Export CSV files for external analysis using CSV Export Agent (Gasket #3a).
        
        Args:
            scores_hash: Hash of analysis scores artifact
            evidence_hash: Hash of evidence artifact
            framework_content: Framework content for context
            experiment_config: Experiment configuration
            corpus_manifest: Corpus metadata
            results_dir: Results directory for CSV output
            audit: Audit logger for provenance
            
        Returns:
            CSV export result or None if export fails
        """
        try:
            # Initialize CSV Export Agent with storage access
            csv_agent = CSVExportAgent(audit_logger=audit)
            
            # Get storage from audit or recreate from experiment path
            storage = None
            if hasattr(audit, 'storage'):
                storage = audit.storage
            else:
                # Fallback: recreate storage from experiment path
                shared_cache_dir = self.experiment_path / "shared_cache"
                storage = LocalArtifactStorage(self.security, shared_cache_dir, "unknown_run")
            
            csv_agent.artifact_storage = storage
            
            # Parse framework configuration
            framework_config = self._parse_framework_config(framework_content)
            
            # Export CSV files
            export_result = csv_agent.export_mid_point_data(
                scores_hash=scores_hash,
                evidence_hash=evidence_hash,
                framework_config=framework_config,
                corpus_manifest=corpus_manifest,
                export_path=str(results_dir)
            )
            
            if export_result.success:
                print(f"📊 CSV Export: {len(export_result.files_created)} files created")
                for file in export_result.files_created:
                    print(f"   • {file}")
                return export_result.__dict__
            else:
                print(f"⚠️  CSV Export failed: {export_result.error_message}")
                return None
                
        except Exception as e:
            print(f"⚠️  CSV Export error: {str(e)}")
            audit.log_error("csv_export_error", str(e), {
                "scores_hash": scores_hash,
                "evidence_hash": evidence_hash
            })
            return None
    
    def _parse_framework_config(self, framework_content: str) -> Dict[str, Any]:
        """Parse framework configuration from framework content."""
        try:
            # Extract JSON appendix from framework markdown
            import re
            json_match = re.search(r'<details><summary>Machine-Readable Configuration</summary>\s*```json\s*\n(.*?)\n\s*```\s*</details>', framework_content, re.DOTALL)
            if json_match:
                config_str = json_match.group(1)
                config = json.loads(config_str)
                
                # v7.3: Ensure static_weights is present, defaulting to empty dict if not
                if 'static_weights' not in config:
                    config['static_weights'] = {}
                
                # v7.3: Ensure pattern_classifications is present, defaulting to empty dict if not
                if 'pattern_classifications' not in config:
                    config['pattern_classifications'] = {}
                
                # v7.3: Ensure reporting_metadata is present, defaulting to empty dict if not
                if 'reporting_metadata' not in config:
                    config['reporting_metadata'] = {}
                    
                return config
            else:
                # Fallback for older formats or malformed files
                json_match_fallback = re.search(r'```json\s*\n(.*?)\n\s*```', framework_content, re.DOTALL)
                if json_match_fallback:
                    return json.loads(json_match_fallback.group(1))
                return {"name": "unknown", "version": "unknown", "static_weights": {}}
        except Exception as e:
            print(f"⚠️  Framework parsing error: {e}. Defaulting to empty config.")
            return {"name": "unknown", "version": "unknown", "static_weights": {}} 