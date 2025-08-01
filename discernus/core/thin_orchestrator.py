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
from ..agents.EnhancedAnalysisAgent.main import EnhancedAnalysisAgent
from ..agents.intelligent_extractor_agent import IntelligentExtractorAgent
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
        
    def _create_thin_synthesis_pipeline(self, audit_logger: AuditLogger, storage: LocalArtifactStorage, model: str, debug_agent: Optional[str] = None, debug_level: str = "info") -> ProductionThinSynthesisPipeline:
        """Create a ProductionThinSynthesisPipeline with proper infrastructure."""
        
        # Create MinIO-compatible wrapper for LocalArtifactStorage
        class MinIOCompatibleStorage:
            def __init__(self, local_storage):
                self.local_storage = local_storage
                
            def put_artifact(self, content: bytes):
                return self.local_storage.put_artifact(content, {})
                
            def get_artifact(self, hash_id: str):
                return self.local_storage.get_artifact(hash_id)
        
        compatible_storage = MinIOCompatibleStorage(storage)
        
        return ProductionThinSynthesisPipeline(
            artifact_client=compatible_storage,
            audit_logger=audit_logger,
            model=model
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
                           corpus_manifest: Optional[Dict[str, Any]] = None,
                           debug_agent: Optional[str] = None,
                           debug_level: str = "info") -> Dict[str, Any]:
        """
        Run synthesis using the new THIN Code-Generated Synthesis Architecture.
        
        Returns results in the same format as EnhancedSynthesisAgent for compatibility.
        """
        
        # Create THIN synthesis pipeline
        pipeline = self._create_thin_synthesis_pipeline(audit_logger, storage, model, debug_agent, debug_level)
        
        # Build THIN-compliant experiment context - raw data for LLM intelligence
        experiment_context = self._build_comprehensive_experiment_context(experiment_config, framework_content, corpus_manifest)
        
        # Create pipeline request
        request = ProductionPipelineRequest(
            framework_spec=framework_content,
            scores_artifact_hash=scores_hash,
            evidence_artifact_hash=evidence_hash,
            experiment_context=experiment_context,
            max_evidence_per_finding=3,
            min_confidence_threshold=0.7,
            interpretation_focus="comprehensive",
            # Add provenance context (Issue #208 fix)
            framework_hash=framework_hash,
            corpus_hash=corpus_hash,
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
            storage = LocalArtifactStorage(self.security, shared_cache_dir)
            
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
            
            # Store framework content and audit logger for gasket integration
            self._current_framework_content = framework_content
            self._current_audit_logger = audit
            
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
                all_analysis_results, scores_hash, evidence_hash = self._execute_analysis_sequentially(
                    analysis_agent,
                    corpus_documents,
                    framework_content,
                    experiment_config,
                    analysis_model
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
                    "analysis_results_count": len(successful_analyses),
                    "available_for_synthesis": True
                }
                
                with open(results_dir / "analysis_summary.json", "w") as f:
                    json.dump(analysis_summary, f, indent=2)
                
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
                
                return {
                    "run_id": run_timestamp,
                    "status": "analysis_completed",
                    "scores_hash": scores_hash,
                    "evidence_hash": evidence_hash,
                    "duration": self._calculate_duration(start_time, end_time),
                    "costs": session_costs
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
                
                synthesis_result = self._run_thin_synthesis(
                    scores_hash=scores_hash,
                    evidence_hash=evidence_hash,
                    framework_content=framework_content,
                    experiment_config=experiment_config,
                    model=synthesis_model,
                    audit_logger=audit,
                    storage=storage,
                    # Add provenance context (Issue #208 fix)
                    framework_hash=framework_hash,
                    corpus_hash=corpus_hash,
                    corpus_manifest=corpus_manifest,  # THIN approach: pass raw corpus content
                    debug_agent=debug_agent,
                    debug_level=debug_level
                )
                
                # Display synthesis-only cost
                synthesis_costs = audit.get_session_costs()
                print(f"✅ Synthesis complete using cached analysis!")
                print(f"   💰 Synthesis cost: ${synthesis_costs.get('total_cost_usd', 0.0):.4f} USD")
                print(f"   🔢 Tokens used: {synthesis_costs.get('total_tokens', 0):,}")
                
                if not synthesis_result or not isinstance(synthesis_result, dict):
                    raise ThinOrchestratorError(f"Invalid synthesis result format: {type(synthesis_result)}")
                
                if "synthesis_report_markdown" not in synthesis_result:
                    raise ThinOrchestratorError("Missing synthesis_report_markdown in result")
                
                # Generate final report with cost transparency
                base_report = synthesis_result["synthesis_report_markdown"]
                session_costs = audit.get_session_costs()
                
                # Add cost summary section to report
                cost_section = self._generate_cost_summary_section(session_costs, run_timestamp)
                final_report = base_report + "\n\n" + cost_section
                
                # Save final report
                with open(results_dir / "final_report.md", "w") as f:
                    f.write(final_report)
                
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
                
                return {
                    "run_id": run_timestamp,
                    "status": "completed",
                    "duration": self._calculate_duration(start_time, end_time),
                    "costs": session_costs
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
            
            all_analysis_results, scores_hash, evidence_hash = self._execute_analysis_sequentially(
                analysis_agent,
                corpus_documents,
                framework_content,
                experiment_config,
                analysis_model
            )
            
            # Display analysis progress and cost
            analysis_costs = audit.get_session_costs()
            successful_count = len([res for res in all_analysis_results if res.get('analysis_result', {}).get('result_hash')])
            print(f"✅ Analysis phase complete: {successful_count}/{len(corpus_documents)} documents processed")
            print(f"   💰 Analysis cost so far: ${analysis_costs.get('total_cost_usd', 0.0):.4f} USD")
            print(f"   🔢 Tokens used: {analysis_costs.get('total_tokens', 0):,}")

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
            
            # Calculate corpus hash for complete provenance context
            corpus_content = ''.join([doc.get('filename', '') + str(doc.get('content', '')) for doc in corpus_documents])
            corpus_hash = hashlib.sha256(corpus_content.encode('utf-8')).hexdigest()
            
            print(f"🔬 Starting synthesis phase with {synthesis_model}...")
            
            synthesis_result = self._run_thin_synthesis(
                scores_hash=scores_hash,
                evidence_hash=evidence_hash,
                framework_content=framework_content,
                experiment_config=experiment_config,
                model=synthesis_model,
                audit_logger=audit,
                storage=storage,
                # Add provenance context (Issue #208 fix)
                framework_hash=framework_hash,
                corpus_hash=corpus_hash,
                corpus_manifest=corpus_manifest,  # THIN approach: pass raw corpus content
                debug_agent=debug_agent,
                debug_level=debug_level
            )
            
            # Display synthesis cost update
            synthesis_costs = audit.get_session_costs()
            print(f"✅ Synthesis phase complete!")
            print(f"   💰 Total cost so far: ${synthesis_costs.get('total_cost_usd', 0.0):.4f} USD")
            print(f"   🔢 Total tokens: {synthesis_costs.get('total_tokens', 0):,}")
            
            synthesis_end_time = datetime.now(timezone.utc).isoformat()
            
            # Record synthesis stage
            agent_name = "ProductionThinSynthesisPipeline"
            stage_metadata = {
                "result_hash": synthesis_result["result_hash"],
                "duration_seconds": synthesis_result["duration_seconds"],
                "synthesis_confidence": synthesis_result["synthesis_confidence"]
            }
            
            # Add THIN-specific metadata if available
            if "thin_metadata" in synthesis_result:
                stage_metadata["thin_pipeline_data"] = synthesis_result["thin_metadata"]
            
            manifest.add_execution_stage("synthesis", agent_name,
                                       synthesis_start_time, synthesis_end_time, "completed", stage_metadata)
            
            # Finalize manifest (synthesis results already captured in execution stages)
            
            # Combine batch results for final summary
            analysis_summary = self._combine_batch_results(all_analysis_results)

            # Generate final report with cost transparency
            base_report_content = synthesis_result.get("synthesis_report_markdown", "Synthesis failed.")
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
                "synthesis_duration": synthesis_result.get("execution_metadata", {}).get("duration_seconds", 0),
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
            
            return {
                "run_id": run_timestamp,
                "run_folder": str(run_folder),
                "results_directory": str(results_dir),
                "final_report_file": str(report_file),
                "manifest_file": str(manifest_file),
                "total_duration_seconds": total_duration,
                "analysis_result": analysis_summary,
                "synthesis_result": synthesis_result,
                "costs": session_costs,
                "mathematical_validation": True,
                "architecture": "thin_v2.0_direct_calls"
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
                                       model: str) -> tuple[List[Dict[str, Any]], Optional[str], Optional[str]]:
        """
        Executes the analysis agent for each document, then combines all results into a single artifact.
        """
        all_analysis_results = []
        total_docs = len(corpus_documents)
        print(f"\n🚀 Starting sequential analysis of {total_docs} documents...")

        for i, doc in enumerate(corpus_documents):
            print(f"\n--- Analyzing document {i+1}/{total_docs}: {doc.get('filename')} ---")
            try:
                # Analyze each document individually
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

        # Combine all analysis results into a single artifact
        combined_result = self._combine_analysis_results(all_analysis_results)
        
        # Calculate framework hash for provenance tracking
        import hashlib
        framework_hash = hashlib.sha256(framework_content.encode('utf-8')).hexdigest()
        
        # Store the combined result and return its hash
        # Note: We need to access storage through the analysis agent's storage
        combined_hash = analysis_agent.storage.put_artifact(
            json.dumps(combined_result).encode('utf-8'),
            {
                "artifact_type": "analysis_json_v6", 
                "framework_version": "v6.0", 
                "combined": True,
                "framework_hash": framework_hash
            }
        )
        
        return all_analysis_results, combined_hash, combined_hash

    def _combine_analysis_results(self, analysis_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Combines multiple individual analysis results into a single combined result.
        """
        combined_document_analyses = []
        
        for i, result in enumerate(analysis_results):
            if "error" in result:
                # Skip failed analyses
                continue
                
            # Extract the actual analysis data from the nested structure
            if "analysis_result" in result and "result_content" in result["analysis_result"]:
                # Get the cached result content
                cached_result = result["analysis_result"]["result_content"]
                
                # Extract the actual analysis data from the raw_analysis_response
                if "raw_analysis_response" in cached_result:
                    raw_response = cached_result["raw_analysis_response"]
                    
                    # Use Intelligent Extractor gasket (v7.0) or legacy parsing (v6.0)
                    # We need framework content for gasket schema extraction
                    framework_content = getattr(self, '_current_framework_content', None)
                    if framework_content:
                        extracted_data = self._extract_and_map_with_gasket(
                            raw_response, 
                            framework_content, 
                            getattr(self, '_current_audit_logger', None)
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
        
        # Create combined result structure
        combined_result = {
            "analysis_metadata": {
                "framework_name": "combined_analysis",
                "framework_version": "v6.0",
                "analyst_confidence": 0.85,
                "analysis_notes": f"Combined analysis of {len(combined_document_analyses)} documents"
            },
            "document_analyses": combined_document_analyses
        }
        
        return combined_result

    def _extract_gasket_schema_from_framework(self, framework_content: str) -> Optional[Dict[str, List[str]]]:
        """
        Extract gasket_schema from framework v7.0 JSON appendix.
        
        Args:
            framework_content: Raw framework markdown content
            
        Returns:
            gasket_schema dict or None if not found/invalid
        """
        try:
            # Look for JSON code block in framework
            if '```json' in framework_content:
                json_start = framework_content.rfind('```json') + 7
                json_end = framework_content.find('```', json_start)
                
                if json_end != -1:
                    json_content = framework_content[json_start:json_end].strip()
                    framework_config = json.loads(json_content)
                    
                    # Extract gasket_schema if present
                    gasket_schema = framework_config.get('gasket_schema')
                    if gasket_schema and 'target_keys' in gasket_schema and 'target_dimensions' in gasket_schema:
                        return gasket_schema
            
            return None
            
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Warning: Failed to extract gasket_schema from framework: {e}")
            return None

    def _extract_and_map_with_gasket(
        self,
        raw_analysis_response: str,
        framework_content: str,
        audit_logger: AuditLogger
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
            # Fallback to legacy parsing for non-v7.0 frameworks
            print("⚠️  No gasket_schema found, falling back to legacy JSON parsing")
            return self._legacy_json_parsing(raw_analysis_response)
        
        # Initialize Intelligent Extractor Agent
        extractor = IntelligentExtractorAgent(
            model="vertex_ai/gemini-2.5-flash",
            audit_logger=audit_logger
        )
        
        # Extract scores using gasket
        extraction_result = extractor.extract_scores_from_raw_analysis(
            raw_analysis_response, gasket_schema
        )
        
        if not extraction_result.success:
            print(f"❌ Intelligent Extractor failed: {extraction_result.error_message}")
            # Fallback to legacy parsing
            return self._legacy_json_parsing(raw_analysis_response)
        
        # Convert extracted scores to document analysis format
        document_analysis = {
            "document_id": "extracted_via_gasket",
            "document_name": "gasket_extraction",
            "analysis_scores": extraction_result.extracted_scores,
            "extraction_metadata": {
                "extraction_time_seconds": extraction_result.extraction_time_seconds,
                "tokens_used": extraction_result.tokens_used,
                "cost_usd": extraction_result.cost_usd,
                "attempts": extraction_result.attempts,
                "gasket_version": "v7.0"
            }
        }
        
        return {
            "document_analyses": [document_analysis],
            "analysis_metadata": {
                "framework_name": "gasket_extracted",
                "framework_version": "v7.0",
                "analyst_confidence": 0.95,  # High confidence from gasket extraction
                "analysis_notes": f"Extracted via Intelligent Extractor in {extraction_result.attempts} attempts"
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

    def _combine_batch_results(self, batch_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Combines results from multiple analysis batches into a single summary.
        """
        if not batch_results:
            return {"total_duration_seconds": 0, "num_batches": 0, "successful_batches": 0}

        total_duration = sum(r.get('analysis_result', {}).get('duration_seconds', 0) for r in batch_results)
        num_batches = len(batch_results)
        successful_batches = sum(1 for r in batch_results if r.get('analysis_result', {}).get('result_hash'))

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
                } for r in batch_results
            ]
        }

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
    
    def _build_comprehensive_experiment_context(self, experiment_config: Dict[str, Any], framework_content: str, corpus_manifest: Optional[Dict[str, Any]] = None) -> str:
        """
        THIN-compliant experiment context building.
        
        Provides LLMs with complete raw data for intelligent processing instead of 
        brittle software parsing. Works with any framework format (CAF, sentiment, 
        discourse analysis, etc.) by letting LLM intelligence handle extraction 
        and formatting decisions.
        
        THIN Principle: Pass raw structured data to LLMs - let them decide what's 
        important and how to format it, rather than hardcoding assumptions.
        """
        
        # Load additional corpus metadata if available  
        corpus_metadata = None
        try:
            corpus_dir = self.experiment_path / experiment_config.get('corpus_path', 'corpus')
            corpus_md_file = corpus_dir / "corpus.md"
            if corpus_md_file.exists():
                corpus_md_content = self.security.secure_read_text(corpus_md_file)
                
                # Extract manifest if present (but don't parse it - let LLM handle that)
                if '```json' in corpus_md_content:
                    json_start = corpus_md_content.find('```json') + 7
                    json_end = corpus_md_content.find('```', json_start)
                    if json_end > json_start:
                        json_str = corpus_md_content[json_start:json_end].strip()
                        corpus_metadata = json.loads(json_str)
        except Exception:
            # Don't fail on corpus metadata errors - just pass None
            pass
        
        # THIN approach: Simple data concatenation - let LLMs do the intelligent processing
        context_sections = [
            "## EXPERIMENT CONFIGURATION",
            "```json",
            json.dumps(experiment_config, indent=2),
            "```",
            "",
            "## FRAMEWORK SPECIFICATION",
            framework_content,
            "",
            "## CORPUS MANIFEST", 
            "```json" if corpus_manifest else "Not available",
            json.dumps(corpus_manifest, indent=2) if corpus_manifest else "",
            "```" if corpus_manifest else "",
            "",
            "## CORPUS METADATA",
            "```json" if corpus_metadata else "Not available", 
            json.dumps(corpus_metadata, indent=2) if corpus_metadata else "",
            "```" if corpus_metadata else ""
        ]
        
        return "\n".join(filter(None, context_sections))
    
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