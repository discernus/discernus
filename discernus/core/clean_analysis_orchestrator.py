#!/usr/bin/env python3
"""
Clean Analysis Orchestrator - THIN Architecture
===============================================

Focused orchestrator for analysis + synthesis without notebook generation cruft.
Addresses the architectural mismatch where we don't produce notebooks but the
current orchestrator is designed for notebook generation.

Architecture:
1. Load specs (experiment.md, framework, corpus)
2. Run analysis (using AnalysisAgent)
3. Run coherence validation (ExperimentCoherenceAgent)
4. Generate statistical analysis (StatisticalAgent - THIN v2.0)
5. Run synthesis (UnifiedSynthesisAgent)
6. Copy results with publication readiness (CRIT-001/002/003)

THIN Principles:
- Direct function calls (no complex orchestration)
- Minimal dependencies
- Clean separation of concerns
- Focus on what we actually need
"""

import os
# Disable huggingface tokenizers parallelism warning before any imports
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import yaml
import json
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd
import pickle
from .logging_config import setup_logging, get_logger, log_experiment_start, log_experiment_complete, log_experiment_failure
from .security_boundary import ExperimentSecurityBoundary, SecurityError
from .audit_logger import AuditLogger
from .local_artifact_storage import LocalArtifactStorage
from .enhanced_manifest import EnhancedManifest
from ..agents.experiment_coherence_agent import ExperimentCoherenceAgent
from ..agents.analysis_agent.main import AnalysisAgent
from ..gateway.llm_gateway_enhanced import EnhancedLLMGateway
from ..gateway.model_registry import ModelRegistry
from ..agents.statistical_agent.main import StatisticalAgent
# TxtaiEvidenceCurator removed from mainline; use RAGIndexManager instead
from ..agents.unified_synthesis_agent import UnifiedSynthesisAgent
# CSVExportAgent DEPRECATED - StatisticalAgent produces CSV via tool calls
from ..gateway.llm_gateway import LLMGateway
from ..gateway.model_registry import ModelRegistry
from .unified_cache_manager import ValidationCacheManager, StatisticalAnalysisCacheManager, AnalysisCacheManager
from .rag_index_manager import RAGIndexManager
from .provenance_organizer import ProvenanceOrganizer
from .directory_structure_reorganizer import reorganize_directory_structure
from .evidence_matching_wrapper import EvidenceMatchingWrapper
from txtai.embeddings import Embeddings
# QA agents temporarily disabled
# from ..agents.revision_agent.agent import RevisionAgent
from ..agents.evidence_retriever_agent import EvidenceRetrieverAgent

from ..core.logging_config import setup_logging_for_run
import logging
# FactCheckerAgent removed in OSS cleanup; all references excised


class CleanAnalysisError(Exception):
    """Clean analysis orchestrator specific exceptions."""
    pass


class CleanAnalysisOrchestrator:
    """
    Clean orchestrator focused on analysis and synthesis only.
    No notebook generation, no complex agent chains, just what we need.
    """
    
    def __init__(self, experiment_path: Path, progress_manager=None, 
                 analysis_model: str = "vertex_ai/gemini-2.5-flash",
                 synthesis_model: str = "vertex_ai/gemini-2.5-pro", 
                 validation_model: str = "vertex_ai/gemini-2.5-pro",
                 derived_metrics_model: str = "vertex_ai/gemini-2.5-flash-lite",
                 dry_run: bool = False,
                 skip_validation: bool = False,
                 analysis_only: bool = False,
                 statistical_prep: bool = False,
                 skip_synthesis: bool = False,
                 resume_from_stats: bool = False,
                 auto_commit: bool = True,
                 verbosity: str = "normal"):
        """Initialize clean analysis orchestrator."""
        self.experiment_path = Path(experiment_path).resolve()

        # Store mode parameters
        self.analysis_model = analysis_model
        self.synthesis_model = synthesis_model
        self.validation_model = validation_model
        self.derived_metrics_model = derived_metrics_model
        self.dry_run = dry_run
        self.skip_validation = skip_validation
        self.analysis_only = analysis_only
        self.statistical_prep = statistical_prep
        self.skip_synthesis = skip_synthesis
        self.resume_from_stats = resume_from_stats
        self.auto_commit = auto_commit
        self.verbosity = verbosity

        # Initialize core components
        self.security = ExperimentSecurityBoundary(self.experiment_path)

        # Set up logging to capture output to a file within the run folder
        self.log_file = setup_logging_for_run(self.experiment_path)
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Orchestrator initialized. Logging to {self.log_file}")

        # Progress manager for UI feedback
        self.progress_manager = progress_manager
        
        # Initialize model registry and LLM gateway for Show Your Work agents
        self.model_registry = ModelRegistry()
        self.llm_gateway = EnhancedLLMGateway(self.model_registry)

        # Testing and development mode flags
        self.test_mode = False
        self.mock_llm_calls = False
        self.performance_monitoring = True

        # Initialize performance monitoring
        self.performance_metrics = {
            "start_time": datetime.now(timezone.utc),
            "phase_timings": {},
            "cache_hits": 0,
            "cache_misses": 0
        }

        self.logger.info(f"Clean orchestrator initialized for: {self.security.experiment_name}")
        # Use the same security boundary instance to avoid duplicate initialization messages
        self.security_boundary = self.security
        self.artifact_storage = None
        self.manifest = None
        self.rag_index = None # Add instance variable for the RAG index

    def enable_test_mode(self, mock_llm: bool = True, performance_monitoring: bool = False):
        """Enable test mode for development and testing."""
        self.test_mode = True
        self.mock_llm_calls = mock_llm
        self.performance_monitoring = performance_monitoring
        self.logger.info("Test mode enabled")
    
    def disable_test_mode(self):
        """Disable test mode."""
        self.test_mode = False
        self.mock_llm_calls = False
        self.performance_monitoring = True
        self.logger.info("Test mode disabled")
    
    def get_test_configuration(self) -> Dict[str, Any]:
        """Get current test configuration for validation."""
        return {
            "test_mode": self.test_mode,
            "mock_llm_calls": self.mock_llm_calls,
            "performance_monitoring": self.performance_monitoring,
            "experiment_path": str(self.experiment_path),
            "security_boundary": str(self.security.experiment_name)
        }
    
    def run_experiment(self) -> Dict[str, Any]:
        """
        Run experiment based on mode:
        - Standard: analysis + synthesis + results
        - Statistical Prep: analysis + derived metrics + CSV export
        - Analysis Only: analysis + CSV export
        """
        
        run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        start_time = datetime.now(timezone.utc)
        
        try:
            self._log_progress("🔧 DEBUG: Starting run_experiment method")
            # Initialize infrastructure
            audit_logger = self._initialize_infrastructure(run_id)
            
            # Track experiment timing and audit logger for log summary
            self._experiment_start_time = start_time
            self._current_audit_logger = audit_logger
            
            log_experiment_start(self.security.experiment_name, run_id)
            self._log_progress("🔧 DEBUG: Infrastructure initialized")
            
            # Handle resume from statistical preparation
            self._log_progress(f"🔍 Checking resume flag: {self.resume_from_stats} (type: {type(self.resume_from_stats)})")
            if self.resume_from_stats:
                self._log_progress("🔄 Resume mode: Loading existing statistical preparation results...")
                self._log_progress(f"🔄 Resume flag is set: {self.resume_from_stats}")
                self._log_progress("🔄 About to call _resume_from_statistical_prep...")
                try:
                    result = self._resume_from_statistical_prep(audit_logger, run_id, start_time)
                    self._log_progress("🔄 _resume_from_statistical_prep completed successfully")
                    return result
                except Exception as e:
                    self._log_progress(f"❌ Resume function failed: {e}")
                    import traceback
                    self._log_progress(f"❌ Traceback: {traceback.format_exc()}")
                    raise
            else:
                self._log_progress("🔄 Resume flag is False, proceeding with normal flow...")

            self._log_progress("🔧 DEBUG: Entering main pipeline execution")
            self._log_status("🔧 DEBUG: About to start main pipeline")
            self._log_progress("🚀 Starting clean analysis pipeline...")
            
            # Phase 1: Load specifications
            self._log_progress("📋 Loading specifications...")
            if self.progress_manager:
                self.progress_manager.update_main_progress("Load specifications")
            phase_start = datetime.now(timezone.utc)
            try:
                self.config = self._load_specs()
                self._log_status("Specifications loaded")
                
                # Debug: Check config structure
                self._log_progress(f"🔧 DEBUG: Config type: {type(self.config)}")
                self._log_progress(f"🔧 DEBUG: Config keys: {list(self.config.keys()) if isinstance(self.config, dict) else 'Not a dict'}")
                if isinstance(self.config, dict) and 'hypotheses' in self.config:
                    self._log_progress(f"🔧 DEBUG: Hypotheses type: {type(self.config['hypotheses'])}")
                    if isinstance(self.config['hypotheses'], list) and len(self.config['hypotheses']) > 0:
                        self._log_progress(f"🔧 DEBUG: First hypothesis type: {type(self.config['hypotheses'][0])}")
                        if isinstance(self.config['hypotheses'][0], dict):
                            self._log_progress(f"🔧 DEBUG: First hypothesis keys: {list(self.config['hypotheses'][0].keys())}")
                
                self._log_phase_timing("specifications_loading", phase_start)
            except Exception as e:
                self._log_progress(f"❌ Failed to load specifications: {str(e)}")
                raise CleanAnalysisError(f"Specification loading failed: {str(e)}")
            
            # Phase 2: Validation (unless skipped)
            if not self.skip_validation:
                phase_start = datetime.now(timezone.utc)
                self._run_coherence_validation(self.validation_model, audit_logger)
                self._log_status("Experiment coherence validated")
                self._log_phase_timing("coherence_validation", phase_start)
            
            # Phase 3: Validate corpus files
            phase_start = datetime.now(timezone.utc)
            try:
                missing_files = self._validate_corpus_files_exist()
                if missing_files:
                    error_msg = f"Corpus validation failed. Missing files: {', '.join(missing_files)}"
                    raise CleanAnalysisError(error_msg)
                self._log_status("Corpus files validated")
                self._log_phase_timing("corpus_validation", phase_start)
            except Exception as e:
                self._log_progress(f"❌ Corpus validation failed: {str(e)}")
                raise CleanAnalysisError(f"Corpus validation failed: {str(e)}")
            
            # Phase 4: Run analysis
            if self.progress_manager:
                self.progress_manager.update_main_progress("Analysis")
            phase_start = datetime.now(timezone.utc)
            try:
                analysis_results = self._run_analysis_phase(self.analysis_model, audit_logger)
                
                # Store analysis results for synthesis access
                self._analysis_results = analysis_results
                
                self._log_status(f"Analysis completed: {len(analysis_results)} documents processed")
                self._log_phase_timing("analysis_phase", phase_start)
                
                # Mode-specific handling after analysis
                if self.analysis_only:
                    # Analysis-only mode: Complete analysis and exit (no CSV export)
                    self._log_progress("📊 Analysis-only mode: Analysis complete, no CSV export")
                    run_dir = self.experiment_path / "runs" / run_id
                    results_dir = run_dir / "results"
                    results_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Create provenance organization
                    self._create_provenance_organization(run_id, audit_logger)
                    
                    # Reorganize directory structure
                    self._reorganize_directory_structure(run_id, audit_logger)
                    
                    # Auto-commit to Git (if enabled)
                    if self.auto_commit:
                        self._auto_commit_run(run_id, audit_logger)
                    
                    # Finalize manifest
                    if self.manifest:
                        try:
                            self.manifest.finalize_manifest()
                        except Exception as e:
                            self._log_progress(f"⚠️ Manifest finalization failed: {str(e)}")
                    
                    duration = (datetime.now(timezone.utc) - start_time).total_seconds()
                    
                    # Log partial completion for analysis-only mode
                    from .logging_config import get_logger
                    logger = get_logger(__name__)
                    logger.info(f"Analysis-only completed (partial pipeline): {self.security.experiment_name}")
                    
                    return {
                        "run_id": run_id,
                        "results_directory": str(results_dir),
                        "analysis_documents": len(analysis_results),
                        "status": "completed_analysis_only",
                        "mode": "analysis_only",
                        "pipeline_status": "partial_completion",
                        "completed_phases": ["validation", "analysis"],
                        "remaining_phases": ["derived_metrics", "evidence_retrieval", "synthesis"],
                        "duration_seconds": duration,
                        "performance_metrics": self._get_performance_summary(),
                        "costs": audit_logger.get_session_costs() if audit_logger else {"total_cost_usd": 0.0}
                    }
                elif self.statistical_prep:
                    # Statistical preparation mode: Run derived metrics + CSV export
                    self._log_progress("📊 Statistical Preparation Mode")
                    self._log_progress("   This mode runs analysis + derived metrics + CSV export")
                    self._log_progress("   Perfect for external statistical analysis workflows")
                    self._log_progress("   Outputs: scores.csv, evidence.csv, metadata.csv")
                    self._log_progress("   Use 'discernus resume' later to complete synthesis if needed")
                    self._log_progress("📊 Running derived metrics and CSV export...")
                    # Continue to derived metrics phase below
                else:
                    # Standard mode: Build RAG index for synthesis
                    phase_start = datetime.now(timezone.utc)
                    try:
                        self._build_and_cache_rag_index(audit_logger)
                        self._log_status("RAG index built and cached successfully")
                        self._log_phase_timing("rag_index_cache", phase_start)
                    except Exception as e:
                        # RAG caching failure is not fatal - we can still build it later
                        self._log_progress(f"⚠️ RAG index caching failed, will build during synthesis: {str(e)}")
                
            except Exception as e:
                self._log_progress(f"❌ Analysis phase failed: {str(e)}")
                raise CleanAnalysisError(f"Analysis phase failed: {str(e)}")
            
            # THIN: Derived metrics are already produced by AnalysisAgent tool calls
            # No extraction phase needed - just log that they're available in artifacts
            if self.progress_manager:
                self.progress_manager.update_main_progress("Derived metrics")
            self._log_progress("📊 THIN: Derived metrics available in AnalysisAgent artifacts")
            derived_metrics_results = {"status": "available_in_artifacts", "message": "Derived metrics produced by AnalysisAgent tool calls"}
            
            # Statistical preparation mode: Copy StatisticalAgent CSV outputs and exit
            if self.statistical_prep:
                self._log_progress("📊 Statistical preparation mode: Copying CSV files from StatisticalAgent...")
                results_dir = self._copy_statistical_artifacts_to_results(run_id)
                
                # Set resume capability in manifest
                if self.manifest:
                    # Collect artifact hashes needed for resume
                    resume_artifacts = []
                    if hasattr(self, '_analysis_results') and self._analysis_results:
                        for result in self._analysis_results:
                            if 'analysis_hash' in result:
                                resume_artifacts.append(result['analysis_hash'])
                    if hasattr(self, '_derived_metrics_results') and self._derived_metrics_results:
                        if 'derived_metrics_hash' in self._derived_metrics_results:
                            resume_artifacts.append(self._derived_metrics_results['derived_metrics_hash'])
                    
                    self.manifest.set_resume_capability(
                        can_resume=True,
                        statistical_prep_completed=True,
                        resume_artifacts=resume_artifacts,
                        resume_metadata={
                            "analysis_documents": len(analysis_results),
                            "derived_metrics_completed": True,
                            "csv_export_completed": True,
                            "resume_timestamp": datetime.now(timezone.utc).isoformat()
                        }
                    )
                    
                    # Create provenance organization
                    self._create_provenance_organization(run_id, audit_logger)
                    
                    # Reorganize directory structure
                    self._reorganize_directory_structure(run_id, audit_logger)
                    
                    # Auto-commit to Git (if enabled)
                    self._log_progress(f"📝 Auto-commit flag: {self.auto_commit}")
                    if self.auto_commit:
                        self._auto_commit_run(run_id, audit_logger)
                    else:
                        self._log_progress("📝 Auto-commit disabled, skipping Git commit")
                    
                    # Finalize manifest
                    if self.manifest:
                        try:
                            self.manifest.finalize_manifest()
                        except Exception as e:
                            self._log_progress(f"⚠️ Manifest finalization failed: {str(e)}")
                    
                    duration = (datetime.now(timezone.utc) - start_time).total_seconds()
                    
                    # User-friendly completion message
                    self._log_progress("✅ Statistical Preparation Complete!")
                    self._log_progress(f"   📁 Results saved to: {results_dir}")
                    self._log_progress("   📊 Generated files:")
                    self._log_progress("      • scores.csv - Analysis scores and derived metrics")
                    self._log_progress("      • evidence.csv - Supporting quotes and evidence")
                    self._log_progress("      • metadata.csv - Document and run metadata")
                    self._log_progress("   🔄 To complete synthesis later, run:")
                    self._log_progress(f"      discernus resume {self.experiment_path}")
                    self._log_progress("   💡 Perfect for external statistical analysis workflows!")
                    
                    # Log partial completion for statistical prep mode
                    from .logging_config import get_logger
                    logger = get_logger(__name__)
                    logger.info(f"Statistical preparation completed (partial pipeline): {self.security.experiment_name}")
                    
                    return {
                        "run_id": run_id,
                        "results_directory": str(results_dir),
                        "analysis_documents": len(analysis_results),
                        "status": "completed_statistical_prep",
                        "mode": "statistical_prep",
                        "pipeline_status": "partial_completion",
                        "completed_phases": ["validation", "analysis", "derived_metrics", "csv_export"],
                        "remaining_phases": ["evidence_retrieval", "synthesis"],
                        "duration_seconds": duration,
                        "performance_metrics": self._get_performance_summary(),
                        "costs": audit_logger.get_session_costs() if audit_logger else {"total_cost_usd": 0.0}
                    }
            
            # Phase 6: Generate statistics
            phase_start = datetime.now(timezone.utc)
            try:
                statistical_results = self._run_statistical_analysis_phase(self.derived_metrics_model, audit_logger, analysis_results, derived_metrics_results)
                self._log_status("Statistical analysis completed")
                self._log_phase_timing("statistical_analysis", phase_start)
            except Exception as e:
                self._log_progress(f"❌ Statistical analysis phase failed: {str(e)}")
                raise CleanAnalysisError(f"Statistical analysis phase failed: {str(e)}")
            
            # Skip synthesis mode: Export results and exit after statistical analysis
            if self.skip_synthesis:
                self._log_progress("📊 Skip synthesis mode: Exporting results without synthesis...")
                # Create results directory with statistical results
                run_dir = self.experiment_path / "runs" / run_id
                results_dir = run_dir / "results"
                results_dir.mkdir(parents=True, exist_ok=True)
                
                # Save statistical results
                if statistical_results.get('stats_hash'):
                    metadata_dir = results_dir / "metadata"
                    metadata_dir.mkdir(exist_ok=True)
                    stats_content = self.artifact_storage.get_artifact(statistical_results['stats_hash'])
                    stats_file = metadata_dir / "statistical_results.json"
                    with open(stats_file, 'wb') as f:
                        f.write(stats_content)
                
                # Create basic results summary
                results_summary = {
                    "run_id": run_id,
                    "mode": "skip_synthesis",
                    "analysis_documents": len(analysis_results),
                    "statistical_analysis_completed": True,
                    "synthesis_skipped": True,
                    "duration_seconds": (datetime.now(timezone.utc) - start_time).total_seconds(),
                    "performance_metrics": self._get_performance_summary(),
                    "costs": audit_logger.get_session_costs() if audit_logger else {"total_cost_usd": 0.0}
                }
                
                # Save results summary
                summary_file = metadata_dir / "experiment_summary.json"
                with open(summary_file, 'w', encoding='utf-8') as f:
                    json.dump(results_summary, f, indent=2)
                
                # Create provenance organization
                self._create_provenance_organization(run_id, audit_logger)
                
                # Finalize manifest
                if self.manifest:
                    try:
                        self.manifest.finalize_manifest()
                    except Exception as e:
                        self._log_progress(f"⚠️ Manifest finalization failed: {str(e)}")
                
                duration = (datetime.now(timezone.utc) - start_time).total_seconds()
                log_experiment_complete(self.security.experiment_name, run_id, duration)
                
                return {
                    "run_id": run_id,
                    "results_directory": str(results_dir),
                    "analysis_documents": len(analysis_results),
                    "status": "completed_skip_synthesis",
                    "mode": "skip_synthesis",
                    "duration_seconds": duration,
                    "performance_metrics": self._get_performance_summary(),
                    "costs": audit_logger.get_session_costs() if audit_logger else {"total_cost_usd": 0.0}
                }
            
            # Phase 7: Corpus index building (DISABLED - not needed without QA agents)
            self._log_progress("📝 Skipping corpus index building (QA agents disabled)")
            self._corpus_index_service = None

            # Phase 7.5: Validate Index Readiness (GATE)
            self._log_progress("🔍 Validating readiness before proceeding...")
            
            # RAG index validation removed - EvidenceRetrieverAgent builds its own evidence wrapper
            # No separate RAG index needed for evidence retrieval phase
            
            # Corpus index service validation skipped (QA agents disabled)
            
            # Corpus index service testing skipped (QA agents disabled)
            self._log_progress("✅ Ready to proceed to evidence retrieval")

            # Phase 8: Run evidence retrieval to curate supporting quotes
            phase_start = datetime.now(timezone.utc)
            self._log_progress("🔍 Phase 8: Evidence Retrieval - Analyzing statistical findings and curating supporting quotes...")
            
            # Corpus index service debug removed (QA agents disabled)
            
            try:
                # Use Flash for evidence retrieval planning (cost optimization)
                evidence_model = "vertex_ai/gemini-2.5-flash"
                evidence_results = self._run_evidence_retrieval_phase(evidence_model, audit_logger, statistical_results, run_id)
                self._log_status("Evidence retrieval completed")
                self._log_phase_timing("evidence_retrieval_phase", phase_start)
                
                # Validate that evidence retrieval actually succeeded
                if not evidence_results or evidence_results.get('status') in ['failed', 'error', 'no_evidence_available']:
                    raise CleanAnalysisError(f"Evidence retrieval failed with status: {evidence_results.get('status', 'unknown')}")
                
                # THIN: CSV files are generated by StatisticalAgent via tool calls
                # No direct CSV generation needed in orchestrator
                self._log_progress("📊 THIN: CSV files available from StatisticalAgent tool calls")
                    
            except Exception as e:
                # Evidence retrieval failure is FATAL - no fallback, no continuing
                self._log_progress(f"❌ FATAL: Evidence retrieval phase failed: {str(e)}")
                raise CleanAnalysisError(f"Evidence retrieval phase failed: {str(e)}")

            # Phase 9: RAG index already built in Phase 7
            self._log_progress("✅ RAG index already built in Phase 7")

            # Phase 10: Run synthesis with RAG integration and curated evidence
            if self.progress_manager:
                self.progress_manager.update_main_progress("Synthesis")
            phase_start = datetime.now(timezone.utc)
            self._log_progress("📝 Phase 10: Synthesis - Generating comprehensive research report...")
            
            # Corpus index service debug removed (QA agents disabled)
            
            try:
                synthesis_results = self._run_synthesis(self.synthesis_model, self.analysis_model, audit_logger, statistical_results, evidence_results, run_id)
                self._log_status("Synthesis completed")
                self._log_phase_timing("synthesis_phase", phase_start)
                
                # Extract assets from synthesis results
                self._log_progress(f"🔧 DEBUG: Synthesis results keys: {list(synthesis_results.keys())}")
                assets = synthesis_results.get("assets", {})
                self._log_progress(f"🔧 DEBUG: Assets keys: {list(assets.keys())}")
                self._log_progress(f"🔧 DEBUG: report_hash in assets: {'report_hash' in assets}")
            except Exception as e:
                # A failure in synthesis is a fatal error for the experiment.
                self._log_progress(f"❌ FATAL: Synthesis phase failed: {str(e)}")
                raise CleanAnalysisError(f"Synthesis phase failed with a fatal error: {str(e)}") from e

            # Phase 11: Fact-checking validation (REMOVED - system deprecated)
            self._log_progress("📝 Fact-checking system removed - skipping validation phase")

            # Phase 12: Create outputs with publication readiness
            self._log_status("🔧 DEBUG: About to execute Phase 12 - Outputs creation")
            if self.progress_manager:
                self.progress_manager.update_main_progress("Outputs creation")
            phase_start = datetime.now(timezone.utc)
            try:
                self._log_status("🔧 DEBUG: Calling _create_clean_outputs_directory")
                outputs_dir = self._create_clean_outputs_directory(run_id, statistical_results, assets)
                self._log_status(f"Outputs created: {outputs_dir}")
                self._log_phase_timing("outputs_creation", phase_start)
                self._log_status("🔧 DEBUG: Phase 12 completed successfully")
            except Exception as e:
                import traceback
                error_msg = f"⚠️ Outputs creation failed, attempting basic outputs: {str(e)}"
                traceback_msg = f"🔧 DEBUG: Full traceback: {traceback.format_exc()}"
                self._log_progress(error_msg)
                self._log_progress(traceback_msg)
                print(error_msg)
                print(traceback_msg)
                # Create basic outputs directory
                outputs_dir = self._create_basic_outputs_directory(run_id)
            
            # Phase 13: Create provenance organization
            if self.progress_manager:
                self.progress_manager.update_main_progress("Provenance organization")
            phase_start = datetime.now(timezone.utc)
            self._create_provenance_organization(run_id, audit_logger)
            self._log_phase_timing("provenance_organization", phase_start)
            
            # Phase 14: Reorganize directory structure
            if self.progress_manager:
                self.progress_manager.update_main_progress("Directory reorganization")
            phase_start = datetime.now(timezone.utc)
            self._reorganize_directory_structure(run_id, audit_logger)
            self._log_phase_timing("directory_reorganization", phase_start)
            
            # Phase 15: Auto-commit to Git (if enabled)
            if self.auto_commit:
                if self.progress_manager:
                    self.progress_manager.update_main_progress("Git commit")
                phase_start = datetime.now(timezone.utc)
                self._auto_commit_run(run_id, audit_logger)
                self._log_phase_timing("git_commit", phase_start)
            
            duration = (datetime.now(timezone.utc) - start_time).total_seconds()
            log_experiment_complete(self.security.experiment_name, run_id, duration)
            
            # Get performance summary
            performance_summary = self._get_performance_summary()
            
            # Get session costs from audit logger
            session_costs = audit_logger.get_session_costs() if audit_logger else {"total_cost_usd": 0.0}
            
            # Log final performance summary including cache metrics
            self._log_final_performance_summary()

            # Phase 16: CSV export moved to Phase 8.5 (after evidence retrieval)

            # Finalize manifest if it exists
            if self.manifest:
                try:
                    self.manifest.finalize_manifest()
                except Exception as e:
                    self._log_progress(f"⚠️ Manifest finalization failed: {str(e)}")

            return {
                "run_id": run_id,
                "results_directory": str(outputs_dir),
                "analysis_documents": len(analysis_results),
                "status": "completed",
                "warnings": self._get_warnings(),
                "duration_seconds": duration,
                "performance_metrics": performance_summary,
                "costs": session_costs,
                "cache_performance": self._generate_cache_performance_report()
            }
            
        except Exception as e:
            log_experiment_failure(self.security.experiment_name, run_id, "experiment_execution", str(e))
            self._log_progress(f"❌ Experiment failed: {str(e)}")
            raise CleanAnalysisError(f"Experiment failed: {str(e)}")
    
    def _initialize_infrastructure(self, run_id: str) -> AuditLogger:
        """Initialize infrastructure components matching legacy pattern."""
        try:
            # Setup logging (matching legacy pattern)
            self._log_progress("🔧 Setting up logging...")
            run_folder = Path(self.experiment_path) / "session" / run_id
            run_folder.mkdir(parents=True, exist_ok=True)
            setup_logging(Path(self.experiment_path), run_folder)
            
            # Initialize audit logger (matching legacy pattern)
            self._log_progress("🔧 Initializing audit logger...")
            audit_logger = AuditLogger(
                security_boundary=self.security,
                run_folder=run_folder
            )
            
            # Initialize artifact storage - USE SHARED CACHE for perfect caching (matching legacy)
            self._log_progress("🔧 Initializing artifact storage...")
            shared_cache_dir = self.experiment_path / "shared_cache"
            self.security.secure_mkdir(shared_cache_dir)
            self.artifact_storage = LocalArtifactStorage(
                security_boundary=self.security,
                run_folder=shared_cache_dir,
                run_name=run_id
            )
            
            # Clean up orphaned registry entries to prevent warnings
            cleanup_stats = self.artifact_storage.cleanup_orphaned_entries(quiet=True)
            if cleanup_stats['orphaned_removed'] > 0:
                self._log_progress(f"🧹 Cleaned up {cleanup_stats['orphaned_removed']} orphaned cache entries")
            
            # Verify caching is working
            self._verify_caching_performance()
            
            # Initialize manifest (matching legacy pattern)
            self._log_progress("🔧 Initializing manifest...")
            self.manifest = EnhancedManifest(
                security_boundary=self.security,
                run_folder=run_folder,
                audit_logger=audit_logger,
                artifact_storage=self.artifact_storage
            )
            
            # Set run mode information in manifest
            self.manifest.set_run_mode(
                analysis_only=self.analysis_only,
                statistical_prep=self.statistical_prep,
                skip_synthesis=self.skip_synthesis,
                resume_from_stats=self.resume_from_stats,
                dry_run=self.dry_run
            )
            
            # Initialize LLM Gateway (matching legacy pattern)
            self._log_progress("🔧 Initializing LLM Gateway...")
            # Use the already initialized EnhancedLLMGateway for Show Your Work
            if not hasattr(self, 'llm_gateway'):
                from ..gateway.llm_gateway import LLMGateway
                from ..gateway.model_registry import ModelRegistry
                self.llm_gateway = LLMGateway(ModelRegistry())
            
            # Performance monitoring already initialized in constructor
            
            self._log_progress("✅ Infrastructure initialization completed")
            return audit_logger
            
        except Exception as e:
            self._log_progress(f"❌ Infrastructure initialization failed: {str(e)}")
            raise CleanAnalysisError(f"Infrastructure initialization failed: {str(e)}") from e
    
    def _verify_caching_performance(self):
        """Verify that caching is working optimally."""
        try:
            # Test cache performance with a simple operation
            test_key = "cache_test_key"
            test_data = {"test": "data", "timestamp": datetime.now(timezone.utc).isoformat()}
            
            # Store test data (encode as JSON bytes)
            test_data_bytes = json.dumps(test_data).encode('utf-8')
            self.artifact_storage.put_artifact(test_data_bytes, {"artifact_type": "cache_test", "test_key": test_key})
            
            # Retrieve test data by finding the artifact with the test_key metadata
            retrieved_data = None
            for artifact_hash, artifact_info in self.artifact_storage.registry.items():
                self._log_progress(f"🔧 DEBUG: artifact_info type: {type(artifact_info)}")
                self._log_progress(f"🔧 DEBUG: artifact_info: {artifact_info}")
                if isinstance(artifact_info, dict):
                    metadata = artifact_info.get("metadata", {})
                    if metadata.get("test_key") == test_key:
                        artifact_bytes = self.artifact_storage.get_artifact(artifact_hash)
                        retrieved_data = json.loads(artifact_bytes.decode('utf-8'))
                        break
            
            if retrieved_data and retrieved_data.get("test") == "data":
                self._log_progress("✅ Cache performance verified - storage and retrieval working")
            else:
                self._log_progress("⚠️ Cache performance issue detected - data corruption possible")
                
        except Exception as e:
            self._log_progress(f"⚠️ Cache performance verification failed: {str(e)}")
    
    def _log_phase_timing(self, phase_name: str, start_time: datetime):
        """Log timing for each phase for performance monitoring."""
        duration = (datetime.now(timezone.utc) - start_time).total_seconds()
        self.performance_metrics["phase_timings"][phase_name] = duration
        self._log_progress(f"⏱️ {phase_name} completed in {duration:.2f} seconds")
    
    def _generate_cache_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive cache performance report."""
        total_requests = self.performance_metrics["cache_hits"] + self.performance_metrics["cache_misses"]
        
        if total_requests == 0:
            return {
                "cache_performance": "No cache requests made",
                "hit_rate": 0.0,
                "total_requests": 0,
                "cache_hits": 0,
                "cache_misses": 0
            }
        
        hit_rate = (self.performance_metrics["cache_hits"] / total_requests) * 100
        
        return {
            "cache_performance": f"Cache hit rate: {hit_rate:.1f}%",
            "hit_rate": hit_rate,
            "total_requests": total_requests,
            "cache_hits": self.performance_metrics["cache_hits"],
            "cache_misses": self.performance_metrics["cache_misses"],
            "efficiency": "High" if hit_rate >= 80 else "Medium" if hit_rate >= 50 else "Low"
        }
    
    def _log_cache_performance_summary(self):
        """Log cache performance summary to progress output."""
        if self.performance_monitoring:
            cache_report = self._generate_cache_performance_report()
            self._log_progress(f"📊 Cache Performance: {cache_report['cache_performance']}")
            self._log_progress(f"   Hits: {cache_report['cache_hits']}, Misses: {cache_report['cache_misses']}")
            self._log_progress(f"   Efficiency: {cache_report['efficiency']}")
    
    def _log_final_performance_summary(self):
        """Log final performance summary including cache metrics."""
        if self.performance_monitoring:
            total_duration = (datetime.now(timezone.utc) - self.performance_metrics["start_time"]).total_seconds()
            
            self._log_progress("=" * 60)
            self._log_progress("📈 FINAL PERFORMANCE SUMMARY")
            self._log_progress("=" * 60)
            self._log_progress(f"⏱️ Total Duration: {total_duration:.2f}s")
            
            # Log phase timings
            if self.performance_metrics["phase_timings"]:
                self._log_progress("📋 Phase Breakdown:")
                for phase, duration in self.performance_metrics["phase_timings"].items():
                    self._log_progress(f"   {phase}: {duration:.2f}s")
            
            # Log cache performance
            self._log_cache_performance_summary()
            
            self._log_progress("=" * 60)
    
    def _get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary for the experiment run."""
        total_time = (datetime.now(timezone.utc) - self.performance_metrics["start_time"]).total_seconds()
        
        return {
            "total_duration_seconds": total_time,
            "phase_timings": self.performance_metrics["phase_timings"],
            "cache_efficiency": {
                "hits": self.performance_metrics["cache_hits"],
                "misses": self.performance_metrics["cache_misses"],
                "hit_rate": self.performance_metrics["cache_hits"] / max(1, self.performance_metrics["cache_hits"] + self.performance_metrics["cache_misses"])
            },
            "performance_score": self._calculate_performance_score()
        }
    
    def _calculate_performance_score(self) -> float:
        """Calculate a performance score based on timing and cache efficiency."""
        # Base score starts at 100
        score = 100.0
        
        # Deduct points for slow phases (>30 seconds)
        for phase, duration in self.performance_metrics["phase_timings"].items():
            if duration > 30:
                score -= min(20, duration - 30)  # Max 20 point deduction per slow phase
        
        # Bonus points for good cache efficiency
        cache_hit_rate = self.performance_metrics["cache_hits"] / max(1, self.performance_metrics["cache_hits"] + self.performance_metrics["cache_misses"])
        if cache_hit_rate > 0.8:
            score += 10
        elif cache_hit_rate < 0.5:
            score -= 10
        
        return max(0, min(100, score))  # Clamp between 0 and 100
    
    def _load_specs(self) -> Dict[str, Any]:
        """Load experiment specifications - supports v10.0 machine-readable appendix format."""
        experiment_file = self.experiment_path / "experiment.md"
        if not experiment_file.exists():
            raise CleanAnalysisError(f"Experiment file not found: {experiment_file}")

        try:
            content = experiment_file.read_text(encoding='utf-8')
            yaml_content = ""

            # Try v10.0 delimited format first (# --- Start/End --- pattern)
            if '# --- Start of Machine-Readable Appendix ---' in content:
                start_marker = '# --- Start of Machine-Readable Appendix ---'
                end_marker = '# --- End of Machine-Readable Appendix ---'
                
                start_idx = content.find(start_marker) + len(start_marker)
                end_idx = content.find(end_marker)
                
                appendix_content = content[start_idx:end_idx].strip() if end_idx > start_idx else content[start_idx:].strip()

                if '```yaml' in appendix_content:
                    yaml_start = appendix_content.find('```yaml') + 7
                    yaml_end = appendix_content.rfind('```')
                    yaml_content = appendix_content[yaml_start:yaml_end].strip() if yaml_end > yaml_start else appendix_content[yaml_start:].strip()
                else:
                    yaml_content = appendix_content

            # Try v10.0 Configuration Appendix format (## Configuration Appendix)
            elif '## Configuration Appendix' in content:
                _, appendix_content = content.split('## Configuration Appendix', 1)
                if '```yaml' in appendix_content:
                    yaml_start = appendix_content.find('```yaml') + 7
                    yaml_end = appendix_content.rfind('```')
                    yaml_content = appendix_content[yaml_start:yaml_end].strip() if yaml_end > yaml_start else appendix_content[yaml_start:].strip()
                else:
                    yaml_content = appendix_content.strip()
            
            # Reject v7.3 frontmatter format
            elif content.startswith('---'):
                raise CleanAnalysisError(
                    "This experiment uses v7.3 frontmatter format. "
                    "CleanAnalysisOrchestrator requires v10.0 machine-readable appendix format. "
                    "Please convert to v10.0 specification."
                )
            
            else:
                raise CleanAnalysisError(
                    "Could not find v10.0 machine-readable appendix in experiment.md. "
                    "Expected either '# --- Start of Machine-Readable Appendix ---' or '## Configuration Appendix'."
                )

            if not yaml_content:
                raise CleanAnalysisError("YAML content is empty in the machine-readable appendix.")

            config = yaml.safe_load(yaml_content)
            if not isinstance(config, dict):
                raise CleanAnalysisError("Invalid YAML structure in machine-readable appendix.")

        except yaml.YAMLError as e:
            raise CleanAnalysisError(f"Failed to parse experiment.md YAML: {e}")
        except Exception as e:
            raise CleanAnalysisError(f"Failed to parse experiment.md: {e}")

        # V10 Specification Validation
        if not config.get('metadata'):
            raise CleanAnalysisError("Missing required field: metadata")
        
        if not config.get('components'):
            raise CleanAnalysisError("Missing required field: components")
        
        spec_version = config.get('metadata', {}).get('spec_version')
        if not spec_version:
            raise CleanAnalysisError("Missing required field: metadata.spec_version")
        
        if not str(spec_version).startswith('10.'):
            raise CleanAnalysisError(f"Experiment spec_version is '{spec_version}', but CleanAnalysisOrchestrator requires v10.0.")
        
        # Validate required component fields and add to config
        components = config.get('components', {})
        framework_file = components.get('framework')
        if not framework_file:
            raise CleanAnalysisError("Missing required field: components.framework")
        
        corpus_file = components.get('corpus')
        if not corpus_file:
            raise CleanAnalysisError("Missing required field: components.corpus")
            
        # Extract experiment name from metadata
        experiment_name = config.get('metadata', {}).get('experiment_name', 'unknown_experiment')
        
        # Add convenience fields to config for downstream use
        config['framework'] = framework_file
        config['corpus'] = corpus_file
        config['name'] = experiment_name
        
        return config
    
    def _run_coherence_validation(self, validation_model: str, audit_logger: AuditLogger):
        """Run experiment coherence validation with caching."""
        self._log_progress("🔬 Validating experiment coherence...")
        
        # Load framework, experiment, and corpus content for cache key generation
        framework_path = self.experiment_path / self.config['framework']
        corpus_path = self.experiment_path / self.config['corpus']
        experiment_path = self.experiment_path / "experiment.md"
        
        framework_content = framework_path.read_text(encoding='utf-8')
        corpus_content = corpus_path.read_text(encoding='utf-8')
        experiment_content = experiment_path.read_text(encoding='utf-8')
        
        # Initialize unified validation caching
        validation_cache_manager = ValidationCacheManager(self.artifact_storage, audit_logger)
        
        # Generate deterministic cache key based on all validation inputs
        cache_key = validation_cache_manager.generate_validation_cache_key(
            framework_content=framework_content,
            experiment_content=experiment_content,
            corpus_content=corpus_content,
            validation_model=validation_model
        )
        
        # Check cache first
        cache_result = validation_cache_manager.check_cache(cache_key, "ValidationPhase")
        
        if cache_result.hit:
            self._log_progress("💾 Using cached validation result")
            cached_validation = cache_result.cached_content
            
            # Check if cached validation was successful
            if not cached_validation.get('success', False):
                issues = cached_validation.get('issues', ['Unknown validation failure'])
                # Handle both string and dict formats in cached data
                if issues and len(issues) > 0:
                    if isinstance(issues[0], dict):
                        # If issues are dictionaries, extract descriptions
                        issue_descriptions = []
                        for issue in issues:
                            if isinstance(issue, dict):
                                desc = issue.get('description', str(issue))
                                issue_descriptions.append(str(desc))
                            else:
                                issue_descriptions.append(str(issue))
                    else:
                        # If issues are already strings, use them directly
                        issue_descriptions = [str(issue) for issue in issues]
                else:
                    issue_descriptions = ['Unknown validation failure']
                raise CleanAnalysisError(f"Experiment validation failed (cached): {'; '.join(issue_descriptions)}")
            
            self.performance_metrics["cache_hits"] += 1
            return
        
        # Perform validation if not cached
        self.performance_metrics["cache_misses"] += 1
        coherence_agent = ExperimentCoherenceAgent(
            model=validation_model,
            audit_logger=audit_logger
        )
        
        validation_result = coherence_agent.validate_experiment(self.experiment_path)

        # Update manifest with validation cost information
        if hasattr(validation_result, 'llm_metadata') and validation_result.llm_metadata and self.manifest:
            llm_metadata = validation_result.llm_metadata
            if "usage" in llm_metadata and "response_cost_usd" in llm_metadata["usage"]:
                cost = llm_metadata["usage"]["response_cost_usd"]
                self.manifest.record_llm_interaction(
                    interaction_hash="",
                    model=llm_metadata.get("model", "unknown"),
                    agent_name="ExperimentCoherenceAgent",
                    stage="validation",
                    prompt_length=0,  # We don't have this info
                    response_length=0,  # We don't have this info
                    metadata={"cost": cost, "agent": "ExperimentCoherenceAgent", "tokens_used": llm_metadata["usage"].get("total_tokens", 0)}
                )

        # Prepare validation result for caching
        validation_data = {
            "success": validation_result.success,
            "issues": [issue.description for issue in validation_result.issues] if hasattr(validation_result, 'issues') else [],
            "model": validation_model,
            "validated_at": datetime.now(timezone.utc).isoformat()
        }
        
        # Store validation result in cache using unified cache manager
        validation_cache_manager.store_cache(cache_key, validation_data, "ValidationPhase")
        
        # Check validation result
        if not validation_result.success:
            # Handle both ValidationIssue objects and dictionaries
            issue_descriptions = []
            for issue in validation_result.issues:
                if hasattr(issue, 'description'):
                    # ValidationIssue object
                    issue_descriptions.append(issue.description)
                elif isinstance(issue, dict):
                    # Dictionary format
                    issue_descriptions.append(issue.get('description', str(issue)))
                else:
                    # Fallback
                    issue_descriptions.append(str(issue))
            
            raise CleanAnalysisError(f"Experiment validation failed: {'; '.join(issue_descriptions)}")
    
    def _validate_corpus_files_exist(self) -> List[str]:
        """Validate that all corpus files actually exist."""
        corpus_documents = self._load_corpus_documents()
        missing_files = []
        
        corpus_dir = self.experiment_path / "corpus"
        
        for doc_info in corpus_documents:
            filename = doc_info.get('filename')
            if not filename:
                continue
            
            # Try exact match first, then fuzzy match
            source_file = self._find_corpus_file(corpus_dir, filename)
            if not source_file or not source_file.exists():
                missing_files.append(filename)
            else:
                self._log_progress(f"📁 Validated: {filename}")
        
        return missing_files
    
    def _generate_validation_cache_key(self, validation_model: str) -> str:
        """Generate cache key for validation results."""
        framework_path = self.experiment_path / self.config['framework']
        corpus_path = self.experiment_path / self.config['corpus']
        experiment_path = self.experiment_path / "experiment.md"
        
        framework_content = framework_path.read_text(encoding='utf-8')
        corpus_content = corpus_path.read_text(encoding='utf-8')
        experiment_content = experiment_path.read_text(encoding='utf-8')
        
        # Initialize unified validation caching
        validation_cache_manager = ValidationCacheManager(self.artifact_storage, self.audit_logger)
        
        # Generate cache key based on all validation inputs
        return validation_cache_manager.generate_validation_cache_key(
            framework_content=framework_content,
            experiment_content=experiment_content,
            corpus_content=corpus_content,
            validation_model=validation_model
        )
    
    def _load_corpus_documents(self) -> List[Dict[str, Any]]:
        """Load corpus documents from manifest."""
        corpus_manifest_path = self.experiment_path / self.config['corpus']
        if not corpus_manifest_path.exists():
            raise CleanAnalysisError(f"Corpus manifest not found: {corpus_manifest_path}")

        content = corpus_manifest_path.read_text(encoding='utf-8')
        
        # Extract YAML metadata from corpus.md (human-first format)
        # Follow corpus specification: look for "## Document Manifest" section first
        if '## Document Manifest' in content:
            _, yaml_block = content.split('## Document Manifest', 1)
            if '```yaml' in yaml_block:
                yaml_start = yaml_block.find('```yaml') + 7
                yaml_end = yaml_block.rfind('```')
                if yaml_end > yaml_start:
                    yaml_content = yaml_block[yaml_start:yaml_end].strip()
                    try:
                        manifest_data = yaml.safe_load(yaml_content)
                        if manifest_data and 'documents' in manifest_data:
                            return manifest_data.get('documents', [])
                    except yaml.YAMLError as e:
                        raise CleanAnalysisError(f"Invalid YAML in corpus manifest: {e}")
        
        raise CleanAnalysisError("Could not parse documents from corpus manifest.")
    
    def _find_corpus_file(self, corpus_dir: Path, filename: str) -> Path:
        """Find corpus file handling potential hash suffixes."""
        # Try exact match first
        exact_file = corpus_dir / filename
        if exact_file.exists():
            return exact_file
        
        # Try fuzzy matching for hash-suffixed files
        base_name = filename.rsplit('.', 1)[0] if '.' in filename else filename
        extension = filename.rsplit('.', 1)[1] if '.' in filename else ''
        
        pattern = f"{base_name}_*.{extension}" if extension else f"{base_name}_*"
        matches = list(corpus_dir.glob(pattern))
        
        if matches:
            self._log_progress(f"📁 Fuzzy match: {filename} → {matches[0].name}")
            return matches[0]
        
        return corpus_dir / filename
    
    def _run_analysis_phase(self, analysis_model: str, audit_logger: AuditLogger) -> List[Dict[str, Any]]:
        """Run analysis phase with unified caching."""
        self._log_progress("🔬 Running analysis phase...")
        
        # Load all content for cache key generation
        framework_path = self.experiment_path / self.config['framework']
        experiment_path = self.experiment_path / "experiment.md"
        corpus_path = self.experiment_path / self.config['corpus']
        
        framework_content = framework_path.read_text(encoding='utf-8')
        experiment_content = experiment_path.read_text(encoding='utf-8')
        corpus_content = corpus_path.read_text(encoding='utf-8')
        
        # Load corpus documents
        corpus_documents = self._load_corpus_documents()
        if not corpus_documents:
            raise CleanAnalysisError("No corpus documents found")

        # Prepare documents for analysis
        prepared_documents = self._prepare_documents_for_analysis(corpus_documents)
        
        # Include all document contents in cache key (analysis depends on all document content)
        all_document_contents = "".join([doc.get('content', '') for doc in prepared_documents])
        combined_corpus_content = corpus_content + all_document_contents
        
        # Initialize unified analysis caching
        cache_manager = AnalysisCacheManager(self.artifact_storage, audit_logger)
        
        # Generate cache key based on ALL inputs that affect analysis output
        cache_key = cache_manager.generate_analysis_cache_key(
            framework_content=framework_content,
            experiment_content=experiment_content,
            corpus_content=combined_corpus_content,
            analysis_model=analysis_model
        )
        
        # Check cache first
        cache_result = cache_manager.check_cache(cache_key, "AnalysisPhase")
        if cache_result.hit:
            self._log_progress("💾 Using cached analysis results")
            self.performance_metrics["cache_hits"] += 1
            return cache_result.cached_content["analysis_results"]
        
        # Cache miss - perform analysis
        self._log_progress("🔍 Cache miss - performing analysis...")
        self.performance_metrics["cache_misses"] += 1
        
        # Initialize analysis agent (Production THIN v2.0 with 6-step approach)
        analysis_agent = AnalysisAgent(
            security_boundary=self.security,
            audit_logger=audit_logger,
            artifact_storage=self.artifact_storage
        )
        
        # Process documents individually for scalability and caching
        analysis_results = []

        # Start document progress tracking if progress manager available
        if self.progress_manager:
            self.progress_manager.start_document_progress(len(prepared_documents), "Analyzing documents")

        for i, prepared_doc in enumerate(prepared_documents):
            doc_name = prepared_doc.get('filename', 'Unknown')
            self._log_progress(f"📄 Processing document {i+1}/{len(prepared_documents)}: {doc_name}")

            # Update document progress
            if self.progress_manager:
                self.progress_manager.update_document_progress(advance=0)  # Don't advance yet
            
            try:
                # Load framework content (not just filename)
                framework_path = self.experiment_path / self.config['framework']
                framework_content = framework_path.read_text(encoding='utf-8')
                
                # Analyze single document (analysis agent handles its own caching)
                self._log_progress(f"🔬 Analyzing document: {prepared_doc.get('filename', 'Unknown')}")
                result = analysis_agent.analyze_documents(
                    framework_content=framework_content,
                    documents=[prepared_doc],
                    experiment_metadata=self.config
                )
                
                if result and 'composite_analysis' in result:
                    # Extract analysis result from new AnalysisAgent response
                    composite_analysis = result['composite_analysis']
                    raw_analysis_response = composite_analysis.get('raw_analysis_response', '')
                    
                    # Extract scores and evidence from the new structure
                    scores_result = result.get('score_extraction', {})
                    evidence_result = result.get('evidence_extraction', {})
                    
                    # Cache performance is now tracked at the phase level, not document level

                    # Store the full result with raw_analysis_response at top level for statistical processing
                    full_result = {
                        'analysis_result': {
                            'result_content': {
                                'raw_analysis_response': raw_analysis_response
                            },
                            'cached': False  # New agent handles caching internally
                        },
                        'raw_analysis_response': raw_analysis_response,
                        'scores_hash': scores_result.get('artifact_hash', ''),
                        'evidence_hash': evidence_result.get('artifact_hash', ''),
                        'document_id': prepared_doc.get('document_id', ''),
                        'filename': prepared_doc.get('filename', 'Unknown'),
                        'verification_status': result.get('verification', {}).get('verification_status', 'unknown')
                    }

                    analysis_results.append(full_result)
                    self._log_progress(f"✅ Analysis completed for: {prepared_doc.get('filename', 'Unknown')}")
                else:
                    self._log_progress(f"⚠️ Analysis failed for: {prepared_doc.get('filename', 'Unknown')}")

            except Exception as e:
                self._log_progress(f"❌ Analysis failed for {prepared_doc.get('filename', 'Unknown')}: {str(e)}")
                # Continue with other documents
                # continue

            # Advance document progress after processing (successful or failed)
            if self.progress_manager:
                self.progress_manager.update_document_progress(advance=1)
        
        if not analysis_results:
            raise CleanAnalysisError("No documents were successfully analyzed")
        
        # Store analysis results in cache for future use
        cache_manager.store_cache(cache_key, {"analysis_results": analysis_results}, "AnalysisPhase")
        
        self._log_progress(f"✅ Analysis phase completed: {len(analysis_results)} documents processed")
        return analysis_results
    
    # REMOVED: _extract_derived_metrics_from_analysis() - DEPRECATED
    # Derived metrics are now produced by AnalysisAgent via tool calls
    # No extraction needed - just pass artifact hashes to next phase
    
    def _run_statistical_analysis_phase(self, model: str, audit_logger: AuditLogger, analysis_results: List[Dict[str, Any]], derived_metrics_results: Dict[str, Any]) -> Dict[str, Any]:
        """THIN approach: Pass analysis artifact hashes to StatisticalAgent, let it do the work."""
        self._log_progress("📊 THIN: Delegating statistical analysis to StatisticalAgent...")
        
        try:
            # Collect analysis artifact hashes
            analysis_artifact_hashes = []
            for result in analysis_results:
                if "scores_hash" in result:
                    analysis_artifact_hashes.append(result["scores_hash"])
                if "evidence_hash" in result:
                    analysis_artifact_hashes.append(result["evidence_hash"])
                if "derived_metrics_hash" in result:
                    analysis_artifact_hashes.append(result["derived_metrics_hash"])
            
            if not analysis_artifact_hashes:
                self._log_progress("⚠️ No analysis artifacts found to process")
                return {"status": "no_artifacts_found", "message": "No analysis artifacts available for statistical processing"}
            
            # Initialize StatisticalAgent
            statistical_agent = StatisticalAgent(
                security_boundary=self.security,
                audit_logger=audit_logger,
                artifact_storage=self.artifact_storage,
                model=model
            )
            
            # Let StatisticalAgent read analysis artifacts and produce statistical results
            self._log_progress(f"📊 StatisticalAgent processing {len(analysis_artifact_hashes)} analysis artifacts...")
            statistical_results = statistical_agent.process_analysis_artifacts(
                analysis_artifact_hashes=analysis_artifact_hashes,
                framework_context=self.config.get("framework_config", {})
            )
            
            if statistical_results.get("success"):
                self._log_progress("✅ StatisticalAgent completed successfully")
                return {
                    "status": "completed",
                    "statistical_results_hash": statistical_results.get("results_hash"),
                    "csv_artifacts": statistical_results.get("csv_artifacts", []),
                    "metadata": statistical_results.get("metadata", {})
                }
            else:
                raise CleanAnalysisError(f"StatisticalAgent failed: {statistical_results.get("error")}")
                
        except Exception as e:
            self._log_progress(f"❌ Statistical analysis phase failed: {str(e)}")
            raise CleanAnalysisError(f"Statistical analysis failed: {str(e)}")
    
    def _prepare_documents_for_analysis(self, corpus_documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prepare corpus documents for analysis by loading content and adding document_id."""
        prepared_docs = []
        corpus_dir = self.experiment_path / "corpus"
        
        for doc_info in corpus_documents:
            filename = doc_info.get('filename')
            if not filename:
                continue
            
            source_file = self._find_corpus_file(corpus_dir, filename)
            if not source_file or not source_file.exists():
                self._log_progress(f"⚠️ Skipping missing file for analysis: {filename}")
                continue
            
            document_content = source_file.read_text(encoding='utf-8')
            
            # Add document_id if not present (assuming filename is unique enough)
            # For now, we'll use a simple hash of the filename
            doc_id = f"doc_{hash(filename)}"
            
            prepared_docs.append({
                'filename': filename,
                'content': document_content,
                'document_id': doc_id,
                'metadata': doc_info.get('metadata', {})
            })
        
        return prepared_docs
    
    def _validate_assets(self, statistical_results: Dict[str, Any]) -> None:
        """Simple validation that basic files exist. Let the synthesis LLM handle data quality assessment."""
        self._log_progress("🔍 Validating basic synthesis prerequisites...")
        
        # 1. Framework file must exist
        framework_path = self.experiment_path / self.config['framework']
        if not framework_path.exists():
            raise CleanAnalysisError(f"SYNTHESIS BLOCKED: Framework file not found: {framework_path}")
        
        # 2. Experiment file must exist
        experiment_path = self.experiment_path / "experiment.md"
        if not experiment_path.exists():
            raise CleanAnalysisError(f"SYNTHESIS BLOCKED: Experiment file not found: {experiment_path}")
        
        # 3. Basic statistical results must exist
        if not statistical_results.get('raw_analysis_data_hash'):
            raise CleanAnalysisError("SYNTHESIS BLOCKED: No analysis data available")
        
        self._log_progress("✅ Basic prerequisites validated. Synthesis LLM will assess data quality.")
    def _build_rag_index(self, audit_logger: AuditLogger) -> None:
        """Builds the RAG index using RAGIndexManager (replaces TxtaiEvidenceCurator)."""
        self._log_progress("📚 Building RAG index for evidence retrieval...")

        evidence_hashes = []
        for artifact_hash, artifact_info in self.artifact_storage.registry.items():
            metadata = artifact_info.get("metadata", {})
            if metadata.get("artifact_type", "").startswith("evidence_v6"):
                evidence_hashes.append(artifact_hash)
        
        # Prepare source documents from evidence artifacts
        source_documents = []
        for evidence_hash in evidence_hashes:
            try:
                evidence_content = self.artifact_storage.get_artifact(evidence_hash)
                evidence_text = evidence_content.decode('utf-8')
                evidence_data = json.loads(evidence_text).get('evidence_data', [])
                for evidence in evidence_data:
                    source_documents.append({
                        'content': evidence.get('quote_text', ''),
                        'metadata': {
                            'source_type': 'evidence',
                            'filename': evidence.get('document_name', 'unknown'),
                            'purpose': 'evidence_validation'
                        }
                    })
            except Exception as e:
                self._log_progress(f"⚠️ Failed to process evidence {evidence_hash[:8]}: {e}")

        if not source_documents:
            self.logger.warning("No evidence artifacts found, RAG index will be empty.")
            from txtai.embeddings import Embeddings
            self.rag_index = Embeddings()
            return

        from .rag_index_manager import RAGIndexManager
        rag_manager = RAGIndexManager(self.artifact_storage)
        index = rag_manager.build_comprehensive_index(source_documents)

        if index is None:
            raise CleanAnalysisError("Failed to build RAG index from evidence artifacts.")
        
        self.rag_index = index
        self._log_progress(f"✅ RAG index built and loaded with {len(source_documents)} evidence documents.")

    def _build_and_cache_rag_index(self, audit_logger: AuditLogger) -> None:
        """Build and cache RAG index immediately after analysis for performance optimization."""
        self._log_progress("📚 Building and caching RAG index for future use...")
        
        # Get evidence artifact hashes
        evidence_hashes = []
        for artifact_hash, artifact_info in self.artifact_storage.registry.items():
            metadata = artifact_info.get("metadata", {})
            if metadata.get("artifact_type", "").startswith("evidence_v6"):
                evidence_hashes.append(artifact_hash)
        
        if not evidence_hashes:
            self._log_progress("⚠️ No evidence artifacts found - skipping RAG index caching")
            return
        
        # Initialize RAG index cache manager
        from .rag_index_cache import RAGIndexCacheManager
        rag_cache_manager = RAGIndexCacheManager(self.artifact_storage, audit_logger)
        
        # Generate cache key based on evidence artifacts
        cache_key = rag_cache_manager.generate_cache_key(evidence_hashes)
        
        # Check if already cached
        cache_result = rag_cache_manager.check_cache(cache_key)
        if cache_result.hit:
            self._log_progress("💾 RAG index already cached - storing for synthesis")
            self.rag_index = cache_result.cached_index
            self.performance_metrics["cache_hits"] += 1
            return
        
        # Build new RAG index using the same method as fact-checking
        # This ensures both cached and fact-checker indexes have the documents attribute
        from .rag_index_manager import RAGIndexManager

        # Prepare documents for RAGIndexManager (reuse logic from _build_fact_checker_rag_index)
        source_documents = []
        for evidence_hash in evidence_hashes:
            try:
                evidence_content = self.artifact_storage.get_artifact(evidence_hash)
                evidence_text = evidence_content.decode('utf-8')
                # Parse the evidence JSON
                evidence_data = json.loads(evidence_text)
                evidence_list = evidence_data.get('evidence_data', [])

                for evidence in evidence_list:
                    source_documents.append({
                        'content': evidence.get('quote_text', ''),
                        'metadata': {
                            'source_type': 'evidence',
                            'filename': evidence.get('document_name', 'unknown'),
                            'purpose': 'evidence_validation'
                        }
                    })
            except Exception as e:
                self._log_progress(f"⚠️ Failed to process evidence {evidence_hash[:8]}: {e}")

        if not source_documents:
            raise CleanAnalysisError("No source documents available for RAG indexing")

        # Build the index using the same method as fact-checking
        rag_manager = RAGIndexManager(self.artifact_storage)
        index = rag_manager.build_comprehensive_index(source_documents)

        if index is None:
            raise CleanAnalysisError("Failed to build RAG index for caching")
        
        # Cache the index for future use
        try:
            rag_cache_manager.store_index(cache_key, index, len(evidence_hashes))
            self._log_progress(f"💾 RAG index cached successfully with {len(evidence_hashes)} evidence sources")
            self.performance_metrics["cache_misses"] += 1
        except Exception as e:
            self._log_progress(f"⚠️ Failed to cache RAG index: {str(e)} - continuing with uncached index")
        
        # Store index for synthesis
        self.rag_index = index

    def _build_rag_index_with_cache(self, audit_logger: AuditLogger) -> None:
        """Build RAG index with cache checking (fallback for synthesis phase)."""
        self._log_progress("📚 Preparing RAG index for synthesis...")
        
        # Get evidence artifact hashes
        evidence_hashes = []
        for artifact_hash, artifact_info in self.artifact_storage.registry.items():
            metadata = artifact_info.get("metadata", {})
            if metadata.get("artifact_type", "").startswith("evidence_v6"):
                evidence_hashes.append(artifact_hash)
        
        if not evidence_hashes:
            self.logger.warning("No evidence artifacts found, RAG index will be empty.")
            from txtai.embeddings import Embeddings
            self.rag_index = Embeddings()
            return
        
        # Initialize RAG index cache manager
        from .rag_index_cache import RAGIndexCacheManager
        rag_cache_manager = RAGIndexCacheManager(self.artifact_storage, audit_logger)
        
        # Generate cache key and check cache
        cache_key = rag_cache_manager.generate_cache_key(evidence_hashes)
        cache_result = rag_cache_manager.check_cache(cache_key)
        
        if cache_result.hit:
            self._log_progress("💾 Using cached RAG index")
            self.rag_index = cache_result.cached_index
            self.performance_metrics["cache_hits"] += 1
        else:
            # Fallback to building index (should rarely happen if caching worked in Phase 4.5)
            self._log_progress("🔧 Cache miss - building RAG index from scratch")
            self._build_rag_index(audit_logger)
            self.performance_metrics["cache_misses"] += 1

    def _run_evidence_retrieval_phase(self, model: str, audit_logger: AuditLogger, statistical_results: Dict[str, Any], run_id: str = None) -> Dict[str, Any]:
        """Run evidence retrieval phase using EvidenceRetrieverAgent to curate supporting quotes."""
        self._log_progress("🔍 Starting evidence retrieval phase...")
        
        try:
            # Find framework specification artifact
            framework_hash = None
            if hasattr(self.artifact_storage, 'registry') and self.artifact_storage.registry:
                for artifact_hash, artifact_info in self.artifact_storage.registry.items():
                    metadata = artifact_info.get("metadata", {})
                    if metadata.get("artifact_type") == "framework_specification":
                        framework_hash = artifact_hash
                        break
            
            if not framework_hash:
                # Create framework specification from framework file
                framework_path = self.experiment_path / self.config['framework']
                if framework_path.exists():
                    framework_content = framework_path.read_text(encoding='utf-8')
                    framework_spec = {
                        "name": self.config.get('framework', 'Unknown Framework'),
                        "content": framework_content,
                        "source_file": str(framework_path)
                    }
                    framework_content_json = json.dumps(framework_spec, indent=2).encode('utf-8')
                    framework_hash = self.artifact_storage.put_artifact(
                        framework_content_json,
                        {"artifact_type": "framework_specification", "agent": "orchestrator"}
                    )
                    self._log_progress(f"✅ Created framework specification artifact: {framework_hash}")
                else:
                    raise CleanAnalysisError(f"Framework file not found: {framework_path}")
            
            # Find statistical results artifact
            statistical_results_hash = None
            if hasattr(self.artifact_storage, 'registry') and self.artifact_storage.registry:
                for artifact_hash, artifact_info in self.artifact_storage.registry.items():
                    metadata = artifact_info.get("metadata", {})
                    if metadata.get("artifact_type") == "statistical_results_with_data":
                        statistical_results_hash = artifact_hash
                        break
            
            if not statistical_results_hash:
                # Store current statistical results - convert tuple keys to strings for JSON serialization
                def convert_tuple_keys_for_json(obj):
                    """Convert tuple keys to strings for safe JSON serialization."""
                    if isinstance(obj, dict):
                        converted = {}
                        for k, v in obj.items():
                            if isinstance(k, tuple):
                                converted_key = str(k)
                            else:
                                converted_key = k
                            converted[converted_key] = convert_tuple_keys_for_json(v)
                        return converted
                    elif isinstance(obj, list):
                        return [convert_tuple_keys_for_json(item) for item in obj]
                    elif isinstance(obj, tuple):
                        return tuple(convert_tuple_keys_for_json(item) for item in obj)
                    else:
                        return obj
                
                safe_statistical_results = convert_tuple_keys_for_json(statistical_results)
                statistical_content = json.dumps(safe_statistical_results, indent=2).encode('utf-8')
                statistical_results_hash = self.artifact_storage.put_artifact(
                    statistical_content,
                    {"artifact_type": "statistical_results_with_data", "agent": "orchestrator"}
                )
                self._log_progress(f"✅ Created statistical results artifact: {statistical_results_hash}")
            
            # Collect evidence artifact hashes
            evidence_artifact_hashes = []
            if hasattr(self.artifact_storage, 'registry') and self.artifact_storage.registry:
                for artifact_hash, artifact_info in self.artifact_storage.registry.items():
                    metadata = artifact_info.get("metadata", {})
                    # Look for evidence artifacts by type or by name pattern
                    artifact_type = metadata.get("artifact_type", "")
                    if (artifact_type.startswith("evidence_v6") or 
                        artifact_type.startswith("evidence_extraction") or
                        artifact_hash.startswith("evidence_extraction_")):
                        evidence_artifact_hashes.append(artifact_hash)
            
            if not evidence_artifact_hashes:
                self._log_progress("⚠️ No evidence artifacts found - evidence retrieval will be limited")
                return {"status": "no_evidence_available", "message": "No evidence artifacts found"}
            
            # Initialize EvidenceRetrieverAgent with shared infrastructure
            agent_config = {
                'experiment_path': str(self.experiment_path),
                'run_id': run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
                'artifact_storage': self.artifact_storage,  # Share the same artifact storage instance
                'security_boundary': self.security,  # Share the same security boundary instance
                'model': model  # Pass the synthesis model for evidence retrieval
            }
            
            evidence_agent = EvidenceRetrieverAgent(agent_config)
            
            # Run evidence retrieval
            self._log_progress("🔍 Running evidence retrieval agent...")
            evidence_results = evidence_agent.run(
                framework_hash=framework_hash,
                statistical_results=statistical_results,  # Pass parsed results directly
                evidence_artifact_hashes=evidence_artifact_hashes
            )
            
            self._log_progress(f"✅ Evidence retrieval completed: {evidence_results.get('evidence_quotes_found', 0)} quotes found")
            return evidence_results
            
        except Exception as e:
            self._log_progress(f"❌ Evidence retrieval phase failed: {str(e)}")
            raise CleanAnalysisError(f"Evidence retrieval phase failed: {str(e)}")

    def _run_synthesis(self, synthesis_model: str, analysis_model: str, audit_logger: AuditLogger, statistical_results: Dict[str, Any], evidence_results: Dict[str, Any] = None, run_id: str = None) -> Dict[str, Any]:
        """Run synthesis using SynthesisPromptAssembler and UnifiedSynthesisAgent."""
        self._log_progress("📝 Starting synthesis phase...")
        
        try:
            # Validate synthesis assets
            self._validate_assets(statistical_results)

            # Create complete research data structure
            raw_analysis_data = self.artifact_storage.get_artifact(statistical_results['raw_analysis_data_hash']).decode('utf-8')
            derived_metrics_data = self.artifact_storage.get_artifact(statistical_results['derived_metrics_data_hash']).decode('utf-8')
            
            research_data = {
                "raw_analysis_results": json.loads(raw_analysis_data),
                "derived_metrics_results": json.loads(derived_metrics_data),
                "statistical_results": statistical_results['statistical_summary']
            }
            
            # Convert tuple keys to strings for safe JSON serialization
            def convert_tuple_keys_for_json(obj):
                """Convert tuple keys to strings for safe JSON serialization."""
                if isinstance(obj, dict):
                    converted = {}
                    for k, v in obj.items():
                        if isinstance(k, tuple):
                            converted_key = str(k)
                        else:
                            converted_key = k
                        converted[converted_key] = convert_tuple_keys_for_json(v)
                    return converted
                elif isinstance(obj, list):
                    return [convert_tuple_keys_for_json(item) for item in obj]
                elif isinstance(obj, tuple):
                    return list(convert_tuple_keys_for_json(item) for item in obj)  # Convert tuples to lists
                elif isinstance(obj, bool):
                    return obj  # Booleans are JSON serializable
                elif obj is None:
                    return obj  # None is JSON serializable
                else:
                    # For any other type, try to convert to string if not natively serializable
                    try:
                        json.dumps(obj)
                        return obj
                    except (TypeError, ValueError):
                        return str(obj)
            
            safe_research_data = convert_tuple_keys_for_json(research_data)
            research_data_hash = self.artifact_storage.put_artifact(
                json.dumps(safe_research_data, indent=2).encode('utf-8'),
                {"artifact_type": "complete_research_data"}
            )

            # New Step: Run Evidence Retrieval Agent to get curated evidence
            raw_evidence_hashes = [h for h, info in self.artifact_storage.registry.items() if info.get("metadata", {}).get("artifact_type", "").startswith("evidence_v6")]
            
            # Find framework and statistical results hashes using the same pattern
            framework_hash = None
            statistical_results_hash = None
            
            for h, info in self.artifact_storage.registry.items():
                artifact_type = info.get("metadata", {}).get("artifact_type", "")
                if artifact_type == "framework_specification":
                    framework_hash = h
                elif artifact_type == "statistical_results_with_data":
                    statistical_results_hash = h

            # Use evidence results from the main evidence retrieval phase
            # CRITICAL: Evidence retrieval must have succeeded to proceed
            if not evidence_results or not evidence_results.get('evidence_artifact_hash'):
                raise CleanAnalysisError("Evidence retrieval failed - no evidence available for synthesis")
            curated_evidence_hash = evidence_results.get('evidence_artifact_hash')

            # Create synthesis agent (THIN approach - no assembler needed)
            self._log_progress("🤖 Initializing synthesis agent...")
            synthesis_agent = UnifiedSynthesisAgent(
                model=synthesis_model,
                audit_logger=audit_logger,
            )
            # Pass both models for provenance tracking
            synthesis_agent.analysis_model = analysis_model
            synthesis_agent.synthesis_model = synthesis_model
            
            # Get current session costs for report header
            session_costs = audit_logger.get_session_costs() if audit_logger else {"total_cost_usd": 0.0}
            
            # Create assets dictionary for the new interface
            assets = {
                'framework_path': Path(self.experiment_path / self.config["framework"]),
                'experiment_path': Path(self.experiment_path / "experiment.md"),
                'research_data_artifact_hash': research_data_hash,
                'evidence_retrieval_results_hash': evidence_results.get('evidence_artifact_hash'),
                'artifact_storage': self.artifact_storage,
                'derived_metrics_results': getattr(self, '_derived_metrics_results', {}),
                'analysis_results': getattr(self, '_analysis_results', []),
                'corpus_manifest_path': Path(self.experiment_path / "corpus.md") if (self.experiment_path / "corpus.md").exists() else None,
                'run_id': run_id,
                'costs': session_costs
            }
            
            assets_dict = synthesis_agent.generate_final_report(assets=assets, artifact_storage=self.artifact_storage)

            # Extract draft report from synthesis agent output
            draft_report = assets_dict.get("final_report")
            if not draft_report:
                raise CleanAnalysisError("Synthesis agent failed to produce a draft report.")

            # Update manifest with synthesis cost information
            if "llm_metadata" in assets_dict and self.manifest:
                llm_metadata = assets_dict["llm_metadata"]
                if "usage" in llm_metadata and "response_cost_usd" in llm_metadata["usage"]:
                    cost = llm_metadata["usage"]["response_cost_usd"]
                    self.manifest.record_llm_interaction(
                        interaction_hash="",
                        model=llm_metadata.get("model", "unknown"),
                        agent_name="UnifiedSynthesisAgent",
                        stage="synthesis",
                        prompt_length=0,  # We don't have this info
                        response_length=0,  # We don't have this info
                        metadata={"cost": cost, "agent": "UnifiedSynthesisAgent", "tokens_used": llm_metadata["usage"].get("total_tokens", 0)}
                    )

            # CRITICAL: Verify statistical analysis succeeded before proceeding
            # This prevents cross-experiment data contamination
            if not research_data_hash:
                raise CleanAnalysisError("Statistical analysis results missing - cannot proceed with synthesis")
            
            # Load and validate statistical results are from THIS experiment run
            statistical_results_content = self.artifact_storage.get_artifact(research_data_hash).decode("utf-8")
            statistical_results = json.loads(statistical_results_content)
            
            # Fail-fast if statistical analysis failed - no cross-experiment data usage allowed
            if (statistical_results.get("status") == "failed" or 
                statistical_results.get("error") or
                "statistical_results" not in statistical_results):
                error_msg = statistical_results.get("error", "Statistical analysis incomplete or missing required data")
                raise CleanAnalysisError(f"Statistical analysis failed - cannot proceed with synthesis: {error_msg}")
            
            # Store the draft report first to get a report_hash for fact-checking
            draft_report_hash = self.artifact_storage.put_artifact(
                draft_report.encode("utf-8"),
                {"artifact_type": "draft_synthesis_report"},
            )
            
            # Create assets dict with report_hash for fact-checking
            assets_with_hash = assets_dict.copy()
            assets_with_hash["report_hash"] = draft_report_hash
            
            # QA agents temporarily disabled - using draft report directly
            self._log_progress("📝 Using synthesis report without QA validation (QA agents in penalty box)")
            final_report = draft_report

            synthesis_hash = self.artifact_storage.put_artifact(
                final_report.encode("utf-8"),
                {"artifact_type": "final_synthesis_report_interpolated"},
            )
            self._log_progress(f"✅ Synthesis phase completed: {len(final_report)} characters")
            return {
                "status": "completed",
                "report_hash": synthesis_hash,
                "report_length": len(final_report),
                "assets": {
                    "report_hash": synthesis_hash,
                    "final_report": final_report
                }
            }
            
        except Exception as e:
            self._log_progress(f"❌ Synthesis phase failed: {str(e)}")
            raise CleanAnalysisError(f"Synthesis phase failed: {str(e)}") from e
    
    def _run_fact_checking_phase(self, model: str, audit_logger: AuditLogger, assets: Dict[str, Any], statistical_results: Dict[str, Any]) -> Dict[str, Any]:
        """Run fact-checking validation on the synthesis report."""
        self._log_progress("🔍 Starting fact-checking phase...")
        
        try:
            # Get the final report content
            if not assets.get('report_hash'):
                raise CleanAnalysisError("No synthesis report available for fact-checking")
            
            report_content = self.artifact_storage.get_artifact(assets['report_hash'])
            report_text = report_content.decode('utf-8')
            
            # Use pre-built corpus index service from analysis phase
            print(f"🔍 DEBUG: Fact-checking phase - _corpus_index_service available: {hasattr(self, '_corpus_index_service')}")
            if hasattr(self, '_corpus_index_service'):
                print(f"🔍 DEBUG: Fact-checking phase - _corpus_index_service type: {type(self._corpus_index_service).__name__}")
                print(f"🔍 DEBUG: Fact-checking phase - _corpus_index_service id: {id(self._corpus_index_service)}")
            
            corpus_index_service = getattr(self, '_corpus_index_service', None)
            if corpus_index_service:
                self._log_progress(f"✅ Using pre-built corpus index service")
            else:
                self._log_progress("⚠️ No pre-built corpus index service available - building on-demand")
                corpus_index_service = self._build_corpus_index_service()
                if corpus_index_service:
                    self._log_progress(f"✅ Corpus index built on-demand")
                else:
                    self._log_progress("❌ Failed to build corpus index service")
            
            # Fact-checking disabled in OSS alpha; short-circuit with informational result
            self._log_progress("ℹ️ Fact-checking phase disabled in OSS alpha. Skipping.")
            return {
                "status": "skipped",
                "findings": [],
                "validation_results": {},
                "corpus_index_service_status": "operational" if corpus_index_service else "unavailable"
            }
                
        except Exception as e:
            self._log_progress(f"❌ Fact-checking phase failed: {str(e)}")
            raise CleanAnalysisError(f"Fact-checking phase failed: {str(e)}") from e
    
    def _build_fact_checker_rag_index(self, assets: Dict[str, Any], statistical_results: Dict[str, Any]):
        """Build a comprehensive RAG index for fact-checking containing ALL experiment assets."""
        self._log_progress("🔧 Building comprehensive fact-checker RAG index...")
        
        try:
            self._log_progress("📥 Importing txtai embeddings...")
            from txtai.embeddings import Embeddings
            
            # Set txtai logging to WARNING level to reduce verbosity
            import logging
            txtai_logger = logging.getLogger("txtai.embeddings")
            txtai_logger.setLevel(logging.WARNING)
            self._log_progress("🔍 Set txtai logging to WARNING level")
            
            # RAG index will be created by RAGIndexManager during construction
            
            # Collect ALL experiment assets for comprehensive fact-checking
            source_documents = []
            
            # 1. EXPERIMENT SPECIFICATION
            experiment_path = self.experiment_path / "experiment.md"
            if experiment_path.exists():
                experiment_content = self.security.secure_read_text(experiment_path)
                source_documents.append({
                    'content': experiment_content,
                    'metadata': {
                        'source_type': 'experiment_specification',
                        'filename': 'experiment.md',
                        'purpose': 'experiment_validation'
                    }
                })
                self._log_progress(f"📋 Added experiment specification: {len(experiment_content)} chars")
            else:
                self._log_progress(f"⚠️ Experiment file not found: {experiment_path}")
            
            # 2. FRAMEWORK SPECIFICATION
            framework_path = self.experiment_path / self.config.get('framework', 'framework.md')
            if framework_path.exists():
                framework_content = self.security.secure_read_text(framework_path)
                source_documents.append({
                    'content': framework_content,
                    'metadata': {
                        'source_type': 'framework_specification',
                        'filename': framework_path.name,
                        'purpose': 'dimension_validation'
                    }
                })
                self._log_progress(f"📋 Added framework specification: {len(framework_content)} chars")
            else:
                self._log_progress(f"⚠️ Framework file not found: {framework_path}")
            
            # 3. CORPUS MANIFEST
            corpus_path = self.experiment_path / "corpus.md"
            if corpus_path.exists():
                corpus_content = self.security.secure_read_text(corpus_path)
                source_documents.append({
                    'content': corpus_content,
                    'metadata': {
                        'source_type': 'corpus_manifest',
                        'filename': 'corpus.md',
                        'purpose': 'corpus_validation'
                    }
                })
            
            # 4. ORIGINAL CORPUS DOCUMENTS
            self._log_progress(f"🔍 Loading corpus documents...")
            corpus_documents = self._load_corpus_documents()
            self._log_progress(f"📋 Loaded {len(corpus_documents)} corpus documents")
            for doc in corpus_documents:
                if 'content' in doc:
                    source_documents.append({
                        'content': doc['content'],
                        'metadata': {
                            'source_type': 'corpus_document',
                            'filename': doc.get('filename', 'unknown'),
                            'purpose': 'quote_validation'
                        }
                    })
                    self._log_progress(f"📋 Added corpus document: {doc.get('filename', 'unknown')} ({len(doc['content'])} chars)")
                else:
                    self._log_progress(f"⚠️ Corpus document missing content: {doc}")
            
            # 5. RAW ANALYSIS SCORES
            if hasattr(self, '_analysis_results') and self._analysis_results:
                # Ensure all analysis results are JSON serializable
                def make_serializable(obj):
                    """Recursively convert objects to JSON-serializable format."""
                    if isinstance(obj, dict):
                        return {str(k): make_serializable(v) for k, v in obj.items()}
                    elif isinstance(obj, list):
                        return [make_serializable(item) for item in obj]
                    elif isinstance(obj, tuple):
                        return tuple(make_serializable(item) for item in obj)
                    elif hasattr(obj, '__dict__'):
                        # Handle objects with attributes
                        return make_serializable(vars(obj))
                    else:
                        # Convert non-serializable types to strings
                        try:
                            json.dumps(obj)
                            return obj
                        except (TypeError, ValueError):
                            return str(obj)

                serializable_results = make_serializable(self._analysis_results)
                analysis_json = json.dumps(serializable_results, indent=2)
                source_documents.append({
                    'content': analysis_json,
                    'metadata': {
                        'source_type': 'raw_analysis_scores',
                        'filename': 'individual_analysis_results.json',
                        'purpose': 'score_validation'
                    }
                })
            
            # 6. DERIVED METRICS
            if hasattr(self, '_derived_metrics_results') and self._derived_metrics_results:
                derived_metrics_json = json.dumps(self._derived_metrics_results, indent=2, default=str)
                source_documents.append({
                    'content': derived_metrics_json,
                    'metadata': {
                        'source_type': 'derived_metrics',
                        'filename': 'derived_metrics_results.json',
                        'purpose': 'metrics_validation'
                    }
                })
            
            # 7. STATISTICAL RESULTS
            if statistical_results:
                try:
                    # Check if we have a stats_hash (artifact reference) or direct data
                    if statistical_results.get('stats_hash'):
                        # Load from artifact storage
                        stats_content = self.artifact_storage.get_artifact(statistical_results['stats_hash'])
                        stats_text = stats_content.decode('utf-8')
                    elif statistical_results.get('statistical_data') or statistical_results.get('analysis_metadata'):
                        # Include direct statistical results data
                        stats_text = json.dumps(statistical_results, indent=2)
                    else:
                        stats_text = str(statistical_results)

                    source_documents.append({
                        'content': stats_text,
                        'metadata': {
                            'source_type': 'statistical_results',
                            'filename': 'statistical_results.json',
                            'purpose': 'statistic_validation'
                        }
                    })
                    self._log_progress(f"📋 Added statistical results: {len(stats_text)} chars")
                except Exception as e:
                    self._log_progress(f"⚠️ Could not include statistical results for fact-checking: {e}")

            # 8. EVIDENCE DATABASE (ALL evidence artifacts)
            self._log_progress(f"🔍 Collecting evidence artifacts...")
            evidence_hashes = []
            if hasattr(self.artifact_storage, 'registry') and self.artifact_storage.registry:
                self._log_progress(f"📋 Artifact registry has {len(self.artifact_storage.registry)} entries")
                for artifact_hash, artifact_info in self.artifact_storage.registry.items():
                    metadata = artifact_info.get("metadata", {})
                    if metadata.get("artifact_type", "").startswith("evidence_v6"):
                        evidence_hashes.append(artifact_hash)
                        self._log_progress(f"📋 Found evidence artifact: {artifact_hash[:8]} - {metadata.get('artifact_type', 'unknown')}")
            
            self._log_progress(f"📋 Found {len(evidence_hashes)} evidence artifacts")
            for evidence_hash in evidence_hashes:  # Include ALL evidence
                try:
                    evidence_content = self.artifact_storage.get_artifact(evidence_hash)
                    evidence_text = evidence_content.decode('utf-8')
                    source_documents.append({
                        'content': evidence_text,
                        'metadata': {
                            'source_type': 'evidence_database',
                            'filename': f'evidence_{evidence_hash[:8]}.json',
                            'purpose': 'evidence_validation'
                        }
                    })
                    self._log_progress(f"📋 Added evidence: {evidence_hash[:8]} ({len(evidence_text)} chars)")
                except Exception as e:
                    self._log_progress(f"⚠️ Could not load evidence {evidence_hash[:8]} for fact-checking: {e}")
            
            # 9. FINAL SYNTHESIS REPORT (the report being validated)
            if assets and assets.get('report_hash'):
                try:
                    report_content = self.artifact_storage.get_artifact(assets['report_hash'])
                    report_text = report_content.decode('utf-8')
                    source_documents.append({
                        'content': report_text,
                        'metadata': {
                            'source_type': 'final_report',
                            'filename': 'final_report.md',
                            'purpose': 'self_reference_validation'
                        }
                    })
                except Exception as e:
                    self._log_progress(f"⚠️ Could not load final report for fact-checking: {e}")
            
            # Build the comprehensive fact-checker RAG index
            if source_documents:
                self._log_progress(f"🔨 Building RAG index with {len(source_documents)} source documents...")
                
                # DEBUG: Log each document being added
                for i, doc in enumerate(source_documents):
                    self._log_progress(f"📄 Document {i}: {doc['metadata']['source_type']} - {len(doc['content'])} chars")
                
                # Use RAGIndexManager for consistent RAG construction
                rag_manager = RAGIndexManager(artifact_storage=self.artifact_storage)
                fact_checker_rag = rag_manager.build_comprehensive_index(source_documents)
                self._log_progress(f"✅ Built comprehensive fact-checker RAG index with {len(source_documents)} assets")
                
                # Log what was included for transparency
                asset_types = {}
                for doc in source_documents:
                    source_type = doc['metadata']['source_type']
                    asset_types[source_type] = asset_types.get(source_type, 0) + 1
                
                asset_summary = ", ".join([f"{count} {asset_type}" for asset_type, count in asset_types.items()])
                self._log_progress(f"📋 Fact-checker RAG contains: {asset_summary}")
                
                return fact_checker_rag
            else:
                self._log_progress("⚠️ No experiment assets available for fact-checker RAG index")
                raise CleanAnalysisError("Cannot build fact-checker RAG index: no source documents available")
                
        except Exception as e:
            self._log_progress(f"❌ Failed to build fact-checker RAG index: {e}")
            raise CleanAnalysisError(f"Fact-checker RAG index construction failed: {e}")
    
    def _apply_fact_checking_to_report(self, report_content: str, fact_check_results: Dict[str, Any]) -> str:
        """Apply fact-checking results to the report by prepending critical findings."""
        findings = fact_check_results.get('findings', [])
        critical_findings = [f for f in findings if f.get('severity') == 'CRITICAL']
        
        if not critical_findings:
            return report_content
        
        # Create warning notice
        warning_lines = [
            "---",
            "**⚠️ FACT-CHECK NOTICE**",
            "",
            "This report contains factual issues identified by automated validation:",
            ""
        ]
        
        for finding in critical_findings:
            warning_lines.append(f"- **{finding.get('check_name', 'Unknown Check')}**: {finding.get('description', 'No description')}")
        
        warning_lines.extend([
            "",
            "See `fact_check_results.json` for complete validation details.",
            "---",
            ""
        ])
        
        return "\n".join(warning_lines) + report_content
    
    def _get_corpus_summary(self) -> Dict[str, Any]:
        """Get corpus summary for direct context."""
        try:
            corpus_documents = self._load_corpus_documents()
            return {
                "total_documents": len(corpus_documents),
                "document_list": [doc.get('filename', 'Unknown') for doc in corpus_documents[:10]]  # Limit for context
            }
        except Exception:
            return {"total_documents": 0, "document_list": []}
    
    def _get_all_evidence(self, evidence_artifact_hashes: List[str], artifact_storage) -> List[Dict[str, Any]]:
        """Retrieve and combine all evidence from artifacts."""
        all_evidence = []
        
        for hash_id in evidence_artifact_hashes:
            try:
                evidence_content = artifact_storage.get_artifact(hash_id)
                evidence_data = json.loads(evidence_content.decode('utf-8'))
                evidence_list = evidence_data.get('evidence_data', [])
                all_evidence.extend(evidence_list)
            except Exception as e:
                self._log_progress(f"⚠️ Failed to retrieve evidence artifact {hash_id[:8]}: {e}")
                continue
        
        return all_evidence
    
    def _prepare_evidence_context(self, evidence_artifact_hashes: List[str], artifact_storage) -> str:
        """Prepare evidence context for direct citation (the working approach)."""
        all_evidence = self._get_all_evidence(evidence_artifact_hashes, artifact_storage)
        
        if not all_evidence:
            return "No evidence available for citation."
        
        evidence_lines = [
            f"EVIDENCE DATABASE: {len(all_evidence)} pieces of textual evidence extracted during analysis.",
            f"All evidence is provided below for direct citation - no queries needed.",
            "",
            "CITATION REQUIREMENTS:",
            "- Every major statistical claim MUST be supported by direct quotes from evidence below",
            "- Use format: 'As [Speaker] stated: \"[exact quote]\" (Source: [document_name])'",
            "- Prioritize evidence with confidence scores >0.8",
            "- Integrate statistical findings with textual evidence for coherent narratives",
            "",
            "AVAILABLE EVIDENCE FOR DIRECT CITATION:",
            ""
        ]
        
        for i, evidence in enumerate(all_evidence, 1):
            doc_name = evidence.get('document_name', 'Unknown')
            dimension = evidence.get('dimension', 'Unknown')
            quote = evidence.get('quote_text', '')
            confidence = evidence.get('confidence', 0.0)
            
            evidence_lines.append(f"{i}. **{dimension}** evidence from {doc_name} (confidence: {confidence:.2f}):")
            evidence_lines.append(f"   \"{quote}\"")
            evidence_lines.append("")  # Empty line for readability
        
        return "\n".join(evidence_lines)
    
    def _create_clean_results_directory(self, run_id: str, statistical_results: Dict[str, Any], assets: Dict[str, Any]) -> Path:
        """Create results directory with publication readiness features."""
        # Create run directory structure
        run_dir = self.experiment_path / "runs" / run_id
        results_dir = run_dir / "results"
        results_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy corpus documents (CRIT-001)
        self._copy_corpus_documents_to_results(results_dir)
        
        # Copy evidence database (CRIT-002)
        self._copy_evidence_database_to_results(results_dir)
        
        # Copy source metadata (CRIT-003)
        self._copy_source_metadata_to_results(results_dir)
        
        # Save statistical results
        if statistical_results.get('stats_hash'):
            stats_content = self.artifact_storage.get_artifact(statistical_results['stats_hash'])
            stats_file = results_dir / "statistical_results.json"
            with open(stats_file, 'wb') as f:
                f.write(stats_content)
        
        # Save synthesis report if available
        if assets.get('report_hash'):
            report_content = self.artifact_storage.get_artifact(assets['report_hash'])
            report_file = results_dir / "final_report.md"
            
            # Save final report (fact-checking system removed)
            with open(report_file, 'wb') as f:
                f.write(report_content)
            self._log_progress("📝 Final report saved to results")
        
        # Save synthesis metadata
        synthesis_file = results_dir / "assets.json"
        with open(synthesis_file, 'w') as f:
            # Remove large content to keep metadata file clean
            clean_synthesis = {k: v for k, v in assets.items() if k != 'assets'}
            json.dump(clean_synthesis, f, indent=2)
        
        # Create experiment summary
        summary = {
            "experiment_name": self.security.experiment_name,
            "run_id": run_id,
            "framework": self.config.get('framework'),
            "corpus": self.config.get('corpus'),
            "completion_time": datetime.now(timezone.utc).isoformat(),
            "artifacts": {
                "statistical_results.json": "Statistical analysis results",
                "assets.json": "Synthesis results",
                "corpus/": "Source documents for verification",
                "evidence/": "Evidence database for quote verification",
                "metadata/": "Source metadata for context verification"
            }
        }
        
        summary_file = results_dir / "experiment_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        self._log_progress(f"✅ Clean results created: {results_dir}")
        return results_dir
    
    def _create_basic_results_directory(self, run_id: str) -> Path:
        """Create a basic results directory in case of failure."""
        self._log_progress(f"⚠️ Creating basic results directory for run {run_id}")
        run_dir = self.experiment_path / "runs" / run_id
        results_dir = run_dir / "results"
        results_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy corpus documents (CRIT-001)
        self._copy_corpus_documents_to_results(results_dir)
        
        # Copy evidence database (CRIT-002)
        self._copy_evidence_database_to_results(results_dir)
        
        # Copy source metadata (CRIT-003)
        self._copy_source_metadata_to_results(results_dir)
        
        # Create a placeholder for statistical results
        stats_file = results_dir / "statistical_results.json"
        with open(stats_file, 'w') as f:
            json.dump({"error": "Statistical analysis failed", "status": "failed"}, f, indent=2)
        
        # Create a placeholder for synthesis results
        synthesis_file = results_dir / "assets.json"
        with open(synthesis_file, 'w') as f:
            json.dump({"error": "Synthesis failed", "status": "failed"}, f, indent=2)
        
        self._log_progress(f"✅ Basic results directory created: {results_dir}")
        return results_dir
    
    def _get_warnings(self) -> List[str]:
        """Collect warnings from the orchestrator."""
        warnings = []
        
        # Check if artifact storage is available
        if hasattr(self, 'artifact_storage') and self.artifact_storage:
            if hasattr(self.artifact_storage, 'registry') and self.artifact_storage.registry:
                if self.artifact_storage.registry.get("statistical_results_with_data"):
                    warnings.append("Statistical analysis completed, but some functions failed to execute or produce data.")
                if self.artifact_storage.registry.get("final_synthesis_report_rag"):
                    warnings.append("Synthesis completed, but report generation failed or produced an empty report.")
        
        return warnings
    
    # Include the publication readiness methods we already implemented
    def _copy_corpus_documents_to_results(self, results_dir: Path) -> None:
        """Copy corpus documents to results directory for source verification."""
        try:
            corpus_results_dir = results_dir / "corpus"
            corpus_results_dir.mkdir(exist_ok=True)
            
            corpus_documents = self._load_corpus_documents()
            corpus_dir = self.experiment_path / "corpus"
            documents_copied = 0
            
            for doc_info in corpus_documents:
                filename = doc_info.get('filename')
                if not filename:
                    continue
                
                source_file = self._find_corpus_file(corpus_dir, filename)
                if source_file and source_file.exists():
                    dest_file = corpus_results_dir / filename
                    dest_file.write_bytes(source_file.read_bytes())
                    documents_copied += 1
                    self._log_progress(f"📄 Copied corpus document: {filename}")
            
            # Copy corpus manifest
            corpus_manifest_path = self.experiment_path / self.config.get('corpus', 'corpus.md')
            if corpus_manifest_path.exists():
                dest_manifest = corpus_results_dir / "corpus.md"
                dest_manifest.write_bytes(corpus_manifest_path.read_bytes())
            
            self._log_progress(f"✅ Corpus documents copied: {documents_copied} files")
            
        except Exception as e:
            self._log_progress(f"⚠️ Failed to copy corpus documents: {str(e)}")
    
    def _copy_evidence_database_to_results(self, results_dir: Path) -> None:
        """Copy evidence database to results directory for quote verification."""
        try:
            evidence_results_dir = results_dir / "evidence"
            evidence_results_dir.mkdir(exist_ok=True)
            
            # Get evidence artifacts from current run only (filter by run ID)
            artifacts_dir = self.artifact_storage.artifacts_dir
            evidence_files = list(artifacts_dir.glob("evidence_v6_*"))
            
            if not evidence_files:
                self._log_progress("⚠️ No evidence artifacts found")
                return
            
            # Filter evidence artifacts by current run ID
            current_run_id = self.artifact_storage.run_name
            run_specific_evidence_files = []
            
            for evidence_file in evidence_files:
                # Get artifact hash from filename (first 8 characters)
                filename_hash = evidence_file.stem.replace("evidence_v6_", "")
                
                # Find matching registry entry by comparing with artifact_path
                for registry_hash, artifact_info in self.artifact_storage.registry.items():
                    if artifact_info.get("artifact_path") == evidence_file.name:
                        if artifact_info.get("source_run") == current_run_id:
                            run_specific_evidence_files.append(evidence_file)
                        break
            
            if not run_specific_evidence_files:
                self._log_progress("⚠️ No evidence artifacts found for current run")
                return
            
            # Aggregate evidence from current run only
            all_evidence = []
            for evidence_file in run_specific_evidence_files:
                try:
                    with open(evidence_file, 'r', encoding='utf-8') as f:
                        evidence_data = json.load(f)
                    evidence_pieces = evidence_data.get('evidence_data', [])
                    all_evidence.extend(evidence_pieces)
                except:
                    continue
            
            # Save evidence database
            evidence_database = {
                "evidence_database_metadata": {
                    "total_evidence_pieces": len(all_evidence),
                    "total_files_processed": len(evidence_files),
                    "collection_time": datetime.now(timezone.utc).isoformat()
                },
                "evidence_collection": all_evidence
            }
            
            evidence_db_file = evidence_results_dir / "evidence_database.json"
            with open(evidence_db_file, 'w', encoding='utf-8') as f:
                json.dump(evidence_database, f, indent=2, ensure_ascii=False)
            
            self._log_progress(f"✅ Evidence database created: {len(all_evidence)} quotes")
            
        except Exception as e:
            self._log_progress(f"⚠️ Failed to copy evidence database: {str(e)}")
    
    def _copy_source_metadata_to_results(self, results_dir: Path) -> None:
        """Copy source metadata to results directory for verification."""
        try:
            metadata_results_dir = results_dir / "metadata"
            metadata_results_dir.mkdir(exist_ok=True)
            
            corpus_documents = self._load_corpus_documents()
            
            # Extract metadata
            document_metadata = []
            for doc_info in corpus_documents:
                filename = doc_info.get('filename', '')
                document_id = doc_info.get('document_id', '')
                metadata = doc_info.get('metadata', {})
                
                doc_metadata = {
                    'filename': filename,
                    'document_id': document_id,
                    **metadata
                }
                document_metadata.append(doc_metadata)
            
            # Save metadata database
            metadata_database = {
                "metadata_summary": {
                    "total_documents": len(document_metadata),
                    "collection_time": datetime.now(timezone.utc).isoformat()
                },
                "document_metadata": document_metadata
            }
            
            metadata_db_file = metadata_results_dir / "source_metadata.json"
            with open(metadata_db_file, 'w', encoding='utf-8') as f:
                json.dump(metadata_database, f, indent=2, ensure_ascii=False)
            
            self._log_progress(f"✅ Source metadata created: {len(document_metadata)} documents")
            
        except Exception as e:
            self._log_progress(f"⚠️ Failed to copy source metadata: {str(e)}")
    
    def _log_progress(self, message: str):
        """Log progress with rich console output."""
        self.logger.debug(message)
    
    def _log_status(self, message: str):
        """Log status updates."""
        self.logger.info(f"STATUS: {message}")

    def _validate_synthesis_prerequisites(self, evidence_hashes: List[str], research_data_hash: str) -> None:
        """
        Transaction integrity check: Verify all required resources are present before synthesis.
        
        Prevents silent failures where synthesis proceeds with incomplete data.
        """
        errors = []
        
        # 1. Check evidence artifacts
        if not evidence_hashes:
            errors.append("No evidence artifacts available")
        else:
            # Verify evidence artifacts are accessible
            inaccessible_evidence = []
            for hash_val in evidence_hashes:
                try:
                    content = self.artifact_storage.get_artifact(hash_val, quiet=True)
                    if not content:
                        inaccessible_evidence.append(hash_val[:8])
                except Exception:
                    inaccessible_evidence.append(hash_val[:8])
            
            if inaccessible_evidence:
                errors.append(f"Evidence artifacts inaccessible: {inaccessible_evidence}")
        
        # 2. Check research data
        if not research_data_hash:
            errors.append("No research data hash provided")
        else:
            try:
                research_content = self.artifact_storage.get_artifact(research_data_hash)
                if not research_content:
                    errors.append("Research data artifact inaccessible")
                else:
                    # Verify research data contains required components
                    research_data = json.loads(research_content.decode('utf-8'))
                    if 'statistical_results' not in research_data:
                        errors.append("Research data missing statistical_results")
                    if research_data.get('status') == 'failed':
                        errors.append("Statistical analysis failed - cannot proceed")
            except Exception as e:
                errors.append(f"Research data validation failed: {str(e)}")
        
        # 3. Check corpus manifest access
        try:
            corpus_path = self.experiment_path / "corpus.md"
            if not corpus_path.exists():
                errors.append("Corpus manifest (corpus.md) not found")
            else:
                corpus_content = corpus_path.read_text(encoding='utf-8')
                if not corpus_content.strip():
                    errors.append("Corpus manifest is empty")
        except Exception as e:
            errors.append(f"Corpus manifest validation failed: {str(e)}")
        
        # Fail fast if any prerequisites are missing
        if errors:
            error_msg = "Synthesis prerequisites validation failed:\n" + "\n".join(f"  - {error}" for error in errors)
            raise CleanAnalysisError(error_msg)
        
        self._log_progress("✅ Synthesis prerequisites validated - all required resources present")

    def _build_synthesis_evidence_index_comprehensive(
        self, evidence_artifact_hashes: List[str]
    ) -> Optional[Embeddings]:
        """Builds a comprehensive RAG index from evidence artifacts for the synthesis agent with metadata preservation."""
        if not evidence_artifact_hashes:
            # CRITICAL: Evidence is required for synthesis - fail fast
            raise CleanAnalysisError(
                "No evidence artifacts found for synthesis. Cannot generate report without textual evidence. "
                "This indicates a failure in the analysis phase evidence extraction."
            )

        try:
            self._log_progress(
                f"🔨 Building comprehensive synthesis RAG index from {len(evidence_artifact_hashes)} evidence artifacts..."
            )
            evidence_documents = []
            for e_hash in evidence_artifact_hashes:
                content = self.artifact_storage.get_artifact(e_hash, quiet=True)
                if content:
                    # Parse the evidence JSON to extract metadata
                    try:
                        evidence_data = json.loads(content.decode("utf-8"))
                        evidence_list = evidence_data.get('evidence_data', [])
                        
                        for evidence in evidence_list:
                            evidence_documents.append({
                                'content': evidence.get('quote_text', ''),
                                'metadata': {
                                    'document_name': evidence.get('document_name', 'Unknown'),
                                    'dimension': evidence.get('dimension', 'Unknown'),
                                    'confidence': evidence.get('confidence', 0.0)
                                }
                            })
                    except json.JSONDecodeError:
                        # Fallback: treat as plain text
                        evidence_documents.append({
                            'content': content.decode("utf-8"),
                            'metadata': {'document_name': 'Unknown', 'dimension': 'Unknown', 'confidence': 0.0}
                        })

            if not evidence_documents:
                # CRITICAL: Evidence artifacts exist but couldn't be loaded - fail fast
                raise CleanAnalysisError(
                    f"Evidence artifacts found ({len(evidence_artifact_hashes)} hashes) but none could be loaded. "
                    "This indicates corrupted or inaccessible evidence artifacts."
                )

            rag_manager = RAGIndexManager(artifact_storage=self.artifact_storage)
            synthesis_rag_index = rag_manager.build_comprehensive_index(
                evidence_documents
            )

            self._log_progress("✅ Built comprehensive synthesis evidence RAG index successfully.")
            return synthesis_rag_index

        except Exception as e:
            self._log_progress(f"❌ Failed to build comprehensive synthesis evidence RAG index: {e}")
            # CRITICAL: Evidence is required for synthesis - fail fast
            raise CleanAnalysisError(f"Failed to build comprehensive synthesis evidence RAG index: {e}. Cannot proceed without evidence.")

    def _build_intelligent_evidence_wrapper(
        self, evidence_artifact_hashes: List[str]
    ) -> 'EvidenceMatchingWrapper':
        """
        Builds an intelligent evidence matching wrapper using our EvidenceMatchingWrapper.
        
        This replaces the basic RAG index with intelligent evidence matching that can:
        - Translate statistical findings into evidence queries
        - Find evidence that actually supports the statistical narrative
        - Provide framework-agnostic evidence matching
        
        Args:
            evidence_artifact_hashes: List of evidence artifact hashes
            
        Returns:
            EvidenceMatchingWrapper instance ready for intelligent evidence retrieval
        """
        if not evidence_artifact_hashes:
            # CRITICAL: Evidence is required for synthesis - fail fast
            raise CleanAnalysisError(
                "No evidence artifacts found for synthesis. Cannot generate report without textual evidence. "
                "This indicates a failure in the analysis phase evidence extraction."
            )

        try:
            self._log_progress(
                f"🧠 Building intelligent evidence matching wrapper from {len(evidence_artifact_hashes)} evidence artifacts..."
            )
            
            # Import our intelligent wrapper
            from .evidence_matching_wrapper import EvidenceMatchingWrapper
            
            # Initialize the wrapper with the synthesis model
            evidence_wrapper = EvidenceMatchingWrapper(
                model=self.synthesis_model if hasattr(self, 'synthesis_model') else "vertex_ai/gemini-2.5-pro",
                artifact_storage=self.artifact_storage,
                audit_logger=self.audit_logger if hasattr(self, 'audit_logger') else None
            )
            
            # Build the intelligent index
            success = evidence_wrapper.build_index(evidence_artifact_hashes)
            if not success:
                raise CleanAnalysisError("Failed to build intelligent evidence index")
            
            self._log_progress("✅ Built intelligent evidence matching wrapper successfully.")
            self._log_progress(f"📊 Index contains {evidence_wrapper.get_index_status()['evidence_count']} evidence pieces")
            
            return evidence_wrapper

        except Exception as e:
            self._log_progress(f"❌ Failed to build intelligent evidence matching wrapper: {e}")
            # CRITICAL: Evidence is required for synthesis - fail fast
            raise CleanAnalysisError(f"Failed to build intelligent evidence matching wrapper: {e}. Cannot proceed without evidence.")

    # REMOVED: Duplicate _run_fact_checking_phase method that was overriding the correct one
    # This was legacy code that ignored the corpus index service
    
    def _build_fact_checker_rag_index(self, assets: Dict[str, Any], statistical_results: Dict[str, Any]):
        """Build a comprehensive RAG index for fact-checking containing ALL experiment assets."""
        self._log_progress("🔧 Building comprehensive fact-checker RAG index...")
        
        try:
            self._log_progress("📥 Importing txtai embeddings...")
            from txtai.embeddings import Embeddings
            
            # Set txtai logging to WARNING level to reduce verbosity
            import logging
            txtai_logger = logging.getLogger("txtai.embeddings")
            txtai_logger.setLevel(logging.WARNING)
            self._log_progress("🔍 Set txtai logging to WARNING level")
            
            # RAG index will be created by RAGIndexManager during construction
            
            # Collect ALL experiment assets for comprehensive fact-checking
            source_documents = []
            
            # 1. EXPERIMENT SPECIFICATION
            experiment_path = self.experiment_path / "experiment.md"
            if experiment_path.exists():
                experiment_content = self.security.secure_read_text(experiment_path)
                source_documents.append({
                    'content': experiment_content,
                    'metadata': {
                        'source_type': 'experiment_specification',
                        'filename': 'experiment.md',
                        'purpose': 'experiment_validation'
                    }
                })
                self._log_progress(f"📋 Added experiment specification: {len(experiment_content)} chars")
            else:
                self._log_progress(f"⚠️ Experiment file not found: {experiment_path}")
            
            # 2. FRAMEWORK SPECIFICATION
            framework_path = self.experiment_path / self.config.get('framework', 'framework.md')
            if framework_path.exists():
                framework_content = self.security.secure_read_text(framework_path)
                source_documents.append({
                    'content': framework_content,
                    'metadata': {
                        'source_type': 'framework_specification',
                        'filename': framework_path.name,
                        'purpose': 'dimension_validation'
                    }
                })
                self._log_progress(f"📋 Added framework specification: {len(framework_content)} chars")
            else:
                self._log_progress(f"⚠️ Framework file not found: {framework_path}")
            
            # 3. CORPUS MANIFEST
            corpus_path = self.experiment_path / "corpus.md"
            if corpus_path.exists():
                corpus_content = self.security.secure_read_text(corpus_path)
                source_documents.append({
                    'content': corpus_content,
                    'metadata': {
                        'source_type': 'corpus_manifest',
                        'filename': 'corpus.md',
                        'purpose': 'corpus_validation'
                    }
                })
            
            # 4. ORIGINAL CORPUS DOCUMENTS
            self._log_progress(f"🔍 Loading corpus documents...")
            corpus_documents = self._load_corpus_documents()
            self._log_progress(f"📋 Loaded {len(corpus_documents)} corpus documents")
            for doc in corpus_documents:
                if 'content' in doc:
                    source_documents.append({
                        'content': doc['content'],
                        'metadata': {
                            'source_type': 'corpus_document',
                            'filename': doc.get('filename', 'unknown'),
                            'purpose': 'quote_validation'
                        }
                    })
                    self._log_progress(f"📋 Added corpus document: {doc.get('filename', 'unknown')} ({len(doc['content'])} chars)")
                else:
                    self._log_progress(f"⚠️ Corpus document missing content: {doc}")
            
            # 5. RAW ANALYSIS SCORES
            if hasattr(self, '_analysis_results') and self._analysis_results:
                # Ensure all analysis results are JSON serializable
                def make_serializable(obj):
                    """Recursively convert objects to JSON-serializable format."""
                    if isinstance(obj, dict):
                        return {str(k): make_serializable(v) for k, v in obj.items()}
                    elif isinstance(obj, list):
                        return [make_serializable(item) for item in obj]
                    elif isinstance(obj, tuple):
                        return tuple(make_serializable(item) for item in obj)
                    elif hasattr(obj, '__dict__'):
                        # Handle objects with attributes
                        return make_serializable(vars(obj))
                    else:
                        # Convert non-serializable types to strings
                        try:
                            json.dumps(obj)
                            return obj
                        except (TypeError, ValueError):
                            return str(obj)

                serializable_results = make_serializable(self._analysis_results)
                analysis_json = json.dumps(serializable_results, indent=2)
                source_documents.append({
                    'content': analysis_json,
                    'metadata': {
                        'source_type': 'raw_analysis_scores',
                        'filename': 'individual_analysis_results.json',
                        'purpose': 'score_validation'
                    }
                })
            
            # 6. DERIVED METRICS
            if hasattr(self, '_derived_metrics_results') and self._derived_metrics_results:
                derived_metrics_json = json.dumps(self._derived_metrics_results, indent=2, default=str)
                source_documents.append({
                    'content': derived_metrics_json,
                    'metadata': {
                        'source_type': 'derived_metrics',
                        'filename': 'derived_metrics_results.json',
                        'purpose': 'metrics_validation'
                    }
                })
            
            # 7. STATISTICAL RESULTS
            if statistical_results:
                try:
                    # Check if we have a stats_hash (artifact reference) or direct data
                    if statistical_results.get('stats_hash'):
                        # Load from artifact storage
                        stats_content = self.artifact_storage.get_artifact(statistical_results['stats_hash'])
                        stats_text = stats_content.decode('utf-8')
                    elif statistical_results.get('statistical_data') or statistical_results.get('analysis_metadata'):
                        # Include direct statistical results data
                        stats_text = json.dumps(statistical_results, indent=2)
                    else:
                        stats_text = str(statistical_results)

                    source_documents.append({
                        'content': stats_text,
                        'metadata': {
                            'source_type': 'statistical_results',
                            'filename': 'statistical_results.json',
                            'purpose': 'statistic_validation'
                        }
                    })
                    self._log_progress(f"📋 Added statistical results: {len(stats_text)} chars")
                except Exception as e:
                    self._log_progress(f"⚠️ Could not include statistical results for fact-checking: {e}")

            # 8. EVIDENCE DATABASE (ALL evidence artifacts)
            self._log_progress(f"🔍 Collecting evidence artifacts...")
            evidence_hashes = []
            if hasattr(self.artifact_storage, 'registry') and self.artifact_storage.registry:
                self._log_progress(f"📋 Artifact registry has {len(self.artifact_storage.registry)} entries")
                for artifact_hash, artifact_info in self.artifact_storage.registry.items():
                    metadata = artifact_info.get("metadata", {})
                    if metadata.get("artifact_type", "").startswith("evidence_v6"):
                        evidence_hashes.append(artifact_hash)
                        self._log_progress(f"📋 Found evidence artifact: {artifact_hash[:8]} - {metadata.get('artifact_type', 'unknown')}")
            
            self._log_progress(f"📋 Found {len(evidence_hashes)} evidence artifacts")
            for evidence_hash in evidence_hashes:  # Include ALL evidence
                try:
                    evidence_content = self.artifact_storage.get_artifact(evidence_hash)
                    evidence_text = evidence_content.decode('utf-8')
                    source_documents.append({
                        'content': evidence_text,
                        'metadata': {
                            'source_type': 'evidence_database',
                            'filename': f'evidence_{evidence_hash[:8]}.json',
                            'purpose': 'evidence_validation'
                        }
                    })
                    self._log_progress(f"📋 Added evidence: {evidence_hash[:8]} ({len(evidence_text)} chars)")
                except Exception as e:
                    self._log_progress(f"⚠️ Could not load evidence {evidence_hash[:8]} for fact-checking: {e}")
            
            # 9. FINAL SYNTHESIS REPORT (the report being validated)
            if assets and assets.get('report_hash'):
                try:
                    report_content = self.artifact_storage.get_artifact(assets['report_hash'])
                    report_text = report_content.decode('utf-8')
                    source_documents.append({
                        'content': report_text,
                        'metadata': {
                            'source_type': 'final_report',
                            'filename': 'final_report.md',
                            'purpose': 'self_reference_validation'
                        }
                    })
                except Exception as e:
                    self._log_progress(f"⚠️ Could not load final report for fact-checking: {e}")
            
            # Build the comprehensive fact-checker RAG index
            if source_documents:
                self._log_progress(f"🔨 Building RAG index with {len(source_documents)} source documents...")
                
                # DEBUG: Log each document being added
                for i, doc in enumerate(source_documents):
                    self._log_progress(f"📄 Document {i}: {doc['metadata']['source_type']} - {len(doc['content'])} chars")
                
                # Use RAGIndexManager for consistent RAG construction
                rag_manager = RAGIndexManager(artifact_storage=self.artifact_storage)
                fact_checker_rag = rag_manager.build_comprehensive_index(source_documents)
                self._log_progress(f"✅ Built comprehensive fact-checker RAG index with {len(source_documents)} assets")
                
                # Log what was included for transparency
                asset_types = {}
                for doc in source_documents:
                    source_type = doc['metadata']['source_type']
                    asset_types[source_type] = asset_types.get(source_type, 0) + 1
                
                asset_summary = ", ".join([f"{count} {asset_type}" for asset_type, count in asset_types.items()])
                self._log_progress(f"📋 Fact-checker RAG contains: {asset_summary}")
                
                return fact_checker_rag
            else:
                self._log_progress("⚠️ No experiment assets available for fact-checker RAG index")
                raise CleanAnalysisError("Cannot build fact-checker RAG index: no source documents available")
                
        except Exception as e:
            self._log_progress(f"❌ Failed to build fact-checker RAG index: {e}")
            raise CleanAnalysisError(f"Fact-checker RAG index construction failed: {e}")
    
    def _apply_fact_checking_to_report(self, report_content: str, fact_check_results: Dict[str, Any]) -> str:
        """Apply fact-checking results to the report by prepending critical findings."""
        findings = fact_check_results.get('findings', [])
        critical_findings = [f for f in findings if f.get('severity') == 'CRITICAL']
        
        if not critical_findings:
            return report_content
        
        # Create warning notice
        warning_lines = [
            "---",
            "**⚠️ FACT-CHECK NOTICE**",
            "",
            "This report contains factual issues identified by automated validation:",
            ""
        ]
        
        for finding in critical_findings:
            warning_lines.append(f"- **{finding.get('check_name', 'Unknown Check')}**: {finding.get('description', 'No description')}")
        
        warning_lines.extend([
            "",
            "See `fact_check_results.json` for complete validation details.",
            "---",
            ""
        ])
        
        return "\n".join(warning_lines) + report_content
    
    def _get_corpus_summary(self) -> Dict[str, Any]:
        """Get corpus summary for direct context."""
        try:
            corpus_documents = self._load_corpus_documents()
            return {
                "total_documents": len(corpus_documents),
                "document_list": [doc.get('filename', 'Unknown') for doc in corpus_documents[:10]]  # Limit for context
            }
        except Exception:
            return {"total_documents": 0, "document_list": []}
    
    def _get_all_evidence(self, evidence_artifact_hashes: List[str], artifact_storage) -> List[Dict[str, Any]]:
        """Retrieve and combine all evidence from artifacts."""
        all_evidence = []
        
        for hash_id in evidence_artifact_hashes:
            try:
                evidence_content = artifact_storage.get_artifact(hash_id)
                evidence_data = json.loads(evidence_content.decode('utf-8'))
                evidence_list = evidence_data.get('evidence_data', [])
                all_evidence.extend(evidence_list)
            except Exception as e:
                self._log_progress(f"⚠️ Failed to retrieve evidence artifact {hash_id[:8]}: {e}")
                continue
        
        return all_evidence
    
    def _prepare_evidence_context(self, evidence_artifact_hashes: List[str], artifact_storage) -> str:
        """Prepare evidence context for direct citation (the working approach)."""
        all_evidence = self._get_all_evidence(evidence_artifact_hashes, artifact_storage)
        
        if not all_evidence:
            return "No evidence available for citation."
        
        evidence_lines = [
            f"EVIDENCE DATABASE: {len(all_evidence)} pieces of textual evidence extracted during analysis.",
            f"All evidence is provided below for direct citation - no queries needed.",
            "",
            "CITATION REQUIREMENTS:",
            "- Every major statistical claim MUST be supported by direct quotes from evidence below",
            "- Use format: 'As [Speaker] stated: \"[exact quote]\" (Source: [document_name])'",
            "- Prioritize evidence with confidence scores >0.8",
            "- Integrate statistical findings with textual evidence for coherent narratives",
            "",
            "AVAILABLE EVIDENCE FOR DIRECT CITATION:",
            ""
        ]
        
        for i, evidence in enumerate(all_evidence, 1):
            doc_name = evidence.get('document_name', 'Unknown')
            dimension = evidence.get('dimension', 'Unknown')
            quote = evidence.get('quote_text', '')
            confidence = evidence.get('confidence', 0.0)
            
            evidence_lines.append(f"{i}. **{dimension}** evidence from {doc_name} (confidence: {confidence:.2f}):")
            evidence_lines.append(f"   \"{quote}\"")
            evidence_lines.append("")  # Empty line for readability
        
        return "\n".join(evidence_lines)
    
    def _create_clean_results_directory(self, run_id: str, statistical_results: Dict[str, Any], assets: Dict[str, Any]) -> Path:
        """Create results directory with publication readiness features."""
        # Create run directory structure
        run_dir = self.experiment_path / "runs" / run_id
        results_dir = run_dir / "results"
        results_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy corpus documents (CRIT-001)
        self._copy_corpus_documents_to_results(results_dir)
        
        # Copy evidence database (CRIT-002)
        self._copy_evidence_database_to_results(results_dir)
        
        # Copy source metadata (CRIT-003)
        self._copy_source_metadata_to_results(results_dir)
        
        # Save statistical results
        if statistical_results.get('stats_hash'):
            stats_content = self.artifact_storage.get_artifact(statistical_results['stats_hash'])
            stats_file = results_dir / "statistical_results.json"
            with open(stats_file, 'wb') as f:
                f.write(stats_content)
        
        # Save synthesis report if available
        if assets.get('report_hash'):
            report_content = self.artifact_storage.get_artifact(assets['report_hash'])
            report_file = results_dir / "final_report.md"
            
            # Save final report (fact-checking system removed)
            with open(report_file, 'wb') as f:
                f.write(report_content)
            self._log_progress("📝 Final report saved to results")
        
        # Save synthesis metadata
        synthesis_file = results_dir / "assets.json"
        with open(synthesis_file, 'w') as f:
            # Remove large content to keep metadata file clean
            clean_synthesis = {k: v for k, v in assets.items() if k != 'assets'}
            json.dump(clean_synthesis, f, indent=2)
        
        # Create experiment summary
        summary = {
            "experiment_name": self.security.experiment_name,
            "run_id": run_id,
            "framework": self.config.get('framework'),
            "corpus": self.config.get('corpus'),
            "completion_time": datetime.now(timezone.utc).isoformat(),
            "artifacts": {
                "statistical_results.json": "Statistical analysis results",
                "assets.json": "Synthesis results",
                "corpus/": "Source documents for verification",
                "evidence/": "Evidence database for quote verification",
                "metadata/": "Source metadata for context verification"
            }
        }
        
        summary_file = results_dir / "experiment_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        self._log_progress(f"✅ Clean results created: {results_dir}")
        return results_dir
    
    def _create_basic_results_directory(self, run_id: str) -> Path:
        """Create a basic results directory in case of failure."""
        self._log_progress(f"⚠️ Creating basic results directory for run {run_id}")
        run_dir = self.experiment_path / "runs" / run_id
        results_dir = run_dir / "results"
        results_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy corpus documents (CRIT-001)
        self._copy_corpus_documents_to_results(results_dir)
        
        # Copy evidence database (CRIT-002)
        self._copy_evidence_database_to_results(results_dir)
        
        # Copy source metadata (CRIT-003)
        self._copy_source_metadata_to_results(results_dir)
        
        # Create a placeholder for statistical results
        stats_file = results_dir / "statistical_results.json"
        with open(stats_file, 'w') as f:
            json.dump({"error": "Statistical analysis failed", "status": "failed"}, f, indent=2)
        
        # Create a placeholder for synthesis results
        synthesis_file = results_dir / "assets.json"
        with open(synthesis_file, 'w') as f:
            json.dump({"error": "Synthesis failed", "status": "failed"}, f, indent=2)
        
        self._log_progress(f"✅ Basic results directory created: {results_dir}")
        return results_dir
    
    def _get_warnings(self) -> List[str]:
        """Collect warnings from the orchestrator."""
        warnings = []
        
        # Check if artifact storage is available
        if hasattr(self, 'artifact_storage') and self.artifact_storage:
            if hasattr(self.artifact_storage, 'registry') and self.artifact_storage.registry:
                if self.artifact_storage.registry.get("statistical_results_with_data"):
                    warnings.append("Statistical analysis completed, but some functions failed to execute or produce data.")
                if self.artifact_storage.registry.get("final_synthesis_report_rag"):
                    warnings.append("Synthesis completed, but report generation failed or produced an empty report.")
        
        return warnings
    
    # Include the publication readiness methods we already implemented
    def _copy_corpus_documents_to_results(self, results_dir: Path) -> None:
        """Copy corpus documents to results directory for source verification."""
        try:
            corpus_results_dir = results_dir / "corpus"
            corpus_results_dir.mkdir(exist_ok=True)
            
            corpus_documents = self._load_corpus_documents()
            corpus_dir = self.experiment_path / "corpus"
            documents_copied = 0
            
            for doc_info in corpus_documents:
                filename = doc_info.get('filename')
                if not filename:
                    continue
                
                source_file = self._find_corpus_file(corpus_dir, filename)
                if source_file and source_file.exists():
                    dest_file = corpus_results_dir / filename
                    dest_file.write_bytes(source_file.read_bytes())
                    documents_copied += 1
                    self._log_progress(f"📄 Copied corpus document: {filename}")
            
            # Copy corpus manifest
            corpus_manifest_path = self.experiment_path / self.config.get('corpus', 'corpus.md')
            if corpus_manifest_path.exists():
                dest_manifest = corpus_results_dir / "corpus.md"
                dest_manifest.write_bytes(corpus_manifest_path.read_bytes())
            
            self._log_progress(f"✅ Corpus documents copied: {documents_copied} files")
            
        except Exception as e:
            self._log_progress(f"⚠️ Failed to copy corpus documents: {str(e)}")
    
    def _copy_evidence_database_to_results(self, results_dir: Path) -> None:
        """Copy evidence database to results directory for quote verification."""
        try:
            evidence_results_dir = results_dir / "evidence"
            evidence_results_dir.mkdir(exist_ok=True)
            
            # Get evidence artifacts from current run only (filter by run ID)
            artifacts_dir = self.artifact_storage.artifacts_dir
            evidence_files = list(artifacts_dir.glob("evidence_v6_*"))
            
            if not evidence_files:
                self._log_progress("⚠️ No evidence artifacts found")
                return
            
            # Filter evidence artifacts by current run ID
            current_run_id = self.artifact_storage.run_name
            run_specific_evidence_files = []
            
            for evidence_file in evidence_files:
                # Get artifact hash from filename (first 8 characters)
                filename_hash = evidence_file.stem.replace("evidence_v6_", "")
                
                # Find matching registry entry by comparing with artifact_path
                for registry_hash, artifact_info in self.artifact_storage.registry.items():
                    if artifact_info.get("artifact_path") == evidence_file.name:
                        if artifact_info.get("source_run") == current_run_id:
                            run_specific_evidence_files.append(evidence_file)
                        break
            
            if not run_specific_evidence_files:
                self._log_progress("⚠️ No evidence artifacts found for current run")
                return
            
            # Aggregate evidence from current run only
            all_evidence = []
            for evidence_file in run_specific_evidence_files:
                try:
                    with open(evidence_file, 'r', encoding='utf-8') as f:
                        evidence_data = json.load(f)
                    evidence_pieces = evidence_data.get('evidence_data', [])
                    all_evidence.extend(evidence_pieces)
                except:
                    continue
            
            # Save evidence database
            evidence_database = {
                "evidence_database_metadata": {
                    "total_evidence_pieces": len(all_evidence),
                    "total_files_processed": len(evidence_files),
                    "collection_time": datetime.now(timezone.utc).isoformat()
                },
                "evidence_collection": all_evidence
            }
            
            evidence_db_file = evidence_results_dir / "evidence_database.json"
            with open(evidence_db_file, 'w', encoding='utf-8') as f:
                json.dump(evidence_database, f, indent=2, ensure_ascii=False)
            
            self._log_progress(f"✅ Evidence database created: {len(all_evidence)} quotes")
            
        except Exception as e:
            self._log_progress(f"⚠️ Failed to copy evidence database: {str(e)}")
    
    def _copy_source_metadata_to_results(self, results_dir: Path) -> None:
        """Copy source metadata to results directory for verification."""
        try:
            metadata_results_dir = results_dir / "metadata"
            metadata_results_dir.mkdir(exist_ok=True)
            
            corpus_documents = self._load_corpus_documents()
            
            # Extract metadata
            document_metadata = []
            for doc_info in corpus_documents:
                filename = doc_info.get('filename', '')
                document_id = doc_info.get('document_id', '')
                metadata = doc_info.get('metadata', {})
                
                doc_metadata = {
                    'filename': filename,
                    'document_id': document_id,
                    **metadata
                }
                document_metadata.append(doc_metadata)
            
            # Save metadata database
            metadata_database = {
                "metadata_summary": {
                    "total_documents": len(document_metadata),
                    "collection_time": datetime.now(timezone.utc).isoformat()
                },
                "document_metadata": document_metadata
            }
            
            metadata_db_file = metadata_results_dir / "source_metadata.json"
            with open(metadata_db_file, 'w', encoding='utf-8') as f:
                json.dump(metadata_database, f, indent=2, ensure_ascii=False)
            
            self._log_progress(f"✅ Source metadata created: {len(document_metadata)} documents")
            
        except Exception as e:
            self._log_progress(f"⚠️ Failed to copy source metadata: {str(e)}")
    

    def _validate_synthesis_prerequisites(self, evidence_hashes: List[str], research_data_hash: str) -> None:
        """
        Transaction integrity check: Verify all required resources are present before synthesis.
        
        Prevents silent failures where synthesis proceeds with incomplete data.
        """
        errors = []
        
        # 1. Check evidence artifacts
        if not evidence_hashes:
            errors.append("No evidence artifacts available")
        else:
            # Verify evidence artifacts are accessible
            inaccessible_evidence = []
            for hash_val in evidence_hashes:
                try:
                    content = self.artifact_storage.get_artifact(hash_val, quiet=True)
                    if not content:
                        inaccessible_evidence.append(hash_val[:8])
                except Exception:
                    inaccessible_evidence.append(hash_val[:8])
            
            if inaccessible_evidence:
                errors.append(f"Evidence artifacts inaccessible: {inaccessible_evidence}")
        
        # 2. Check research data
        if not research_data_hash:
            errors.append("No research data hash provided")
        else:
            try:
                research_content = self.artifact_storage.get_artifact(research_data_hash)
                if not research_content:
                    errors.append("Research data artifact inaccessible")
                else:
                    # Verify research data contains required components
                    research_data = json.loads(research_content.decode('utf-8'))
                    if 'statistical_results' not in research_data:
                        errors.append("Research data missing statistical_results")
                    if research_data.get('status') == 'failed':
                        errors.append("Statistical analysis failed - cannot proceed")
            except Exception as e:
                errors.append(f"Research data validation failed: {str(e)}")
        
        # 3. Check corpus manifest access
        try:
            corpus_path = self.experiment_path / "corpus.md"
            if not corpus_path.exists():
                errors.append("Corpus manifest (corpus.md) not found")
            else:
                corpus_content = corpus_path.read_text(encoding='utf-8')
                if not corpus_content.strip():
                    errors.append("Corpus manifest is empty")
        except Exception as e:
            errors.append(f"Corpus manifest validation failed: {str(e)}")
        
        # Fail fast if any prerequisites are missing
        if errors:
            error_msg = "Synthesis prerequisites validation failed:\n" + "\n".join(f"  - {error}" for error in errors)
            raise CleanAnalysisError(error_msg)
        
        self._log_progress("✅ Synthesis prerequisites validated - all required resources present")

    def _build_synthesis_evidence_index(
        self, evidence_artifact_hashes: List[str]
    ) -> Optional[Embeddings]:
        """Builds a dedicated RAG index from evidence artifacts for the synthesis agent."""
        if not evidence_artifact_hashes:
            # CRITICAL: Evidence is required for synthesis - fail fast
            raise CleanAnalysisError(
                "No evidence artifacts found for synthesis. Cannot generate report without textual evidence. "
                "This indicates a failure in the analysis phase evidence extraction."
            )

        try:
            self._log_progress(
                f"🔨 Building synthesis RAG index from {len(evidence_artifact_hashes)} evidence artifacts..."
            )
            evidence_documents = []
            for e_hash in evidence_artifact_hashes:
                content = self.artifact_storage.get_artifact(e_hash, quiet=True)
                if content:
                    evidence_documents.append({"content": content.decode("utf-8")})

            if not evidence_documents:
                # CRITICAL: Evidence artifacts exist but couldn't be loaded - fail fast
                raise CleanAnalysisError(
                    f"Evidence artifacts found ({len(evidence_artifact_hashes)} hashes) but none could be loaded. "
                    "This indicates corrupted or inaccessible evidence artifacts."
                )

            rag_manager = RAGIndexManager(artifact_storage=self.artifact_storage)
            synthesis_rag_index = rag_manager.build_index_from_documents(
                evidence_documents
            )

            self._log_progress("✅ Built synthesis evidence RAG index successfully.")
            # TODO: Add caching and persistence for this index
            return synthesis_rag_index

        except Exception as e:
            self._log_progress(f"❌ Failed to build synthesis evidence RAG index: {e}")
            # CRITICAL: Evidence is required for synthesis - fail fast
            raise CleanAnalysisError(f"Failed to build synthesis evidence RAG index: {e}. Cannot proceed without evidence.")

    def _run_fact_checker_validation(self, synthesis_report: str) -> Dict[str, Any]:
        """Fact-checking disabled in OSS alpha; return informational status."""
        return {"issues": [], "status": "fact_check_skipped"}

    def _build_evidence_index(self) -> str:
        """Build evidence index for synthesis using RAG capabilities."""
        self._log_progress("🔧 Building evidence index for synthesis...")
        
        try:
            # Check if we already have a cached RAG index, build if needed
            if not hasattr(self, 'rag_index') or self.rag_index is None:
                self._build_rag_index_with_cache(None)  # No audit logger needed here
            
            if hasattr(self, 'rag_index') and self.rag_index:
                self._log_progress("✅ Evidence index built successfully")
                return self.rag_index
            else:
                self._log_progress("⚠️ Failed to build evidence index")
                return None
                
        except Exception as e:
            self._log_progress(f"❌ Error building evidence index: {e}")
            return None

    def _build_corpus_index_service(self) -> Any:
        """Build a corpus index service for fact-checking using Hybrid (Typesense + BM25)."""
        self._log_progress("🔧 Building hybrid corpus index service...")
        
        try:
            from ..core.hybrid_corpus_service import HybridCorpusService
            import json
            
            # Initialize hybrid corpus service
            corpus_index_service = HybridCorpusService()
            
            # Prepare corpus files for indexing
            corpus_files = []
            
            # 1. Load corpus documents
            self._log_progress(f"🔍 Loading corpus documents for indexing...")
            corpus_documents = self._load_corpus_documents()
            self._log_progress(f"📋 Loaded {len(corpus_documents)} corpus documents")
            
            for doc in corpus_documents:
                if 'content' in doc:
                    corpus_files.append({
                        'content': doc['content'],
                        'file_path': doc.get('file_path', ''),
                        'filename': doc.get('filename', 'unknown'),
                        'speaker': doc.get('speaker', ''),
                        'date': doc.get('date', ''),
                        'source_type': 'corpus_document',
                        'start_char': 0,
                        'end_char': len(doc['content']),
                        'context': doc.get('context', '')
                    })
                    self._log_progress(f"📋 Prepared corpus document: {doc.get('filename', 'unknown')} ({len(doc['content'])} chars)")
                else:
                    self._log_progress(f"⚠️ Corpus document missing content: {doc}")
            
            # 2. Add experiment specification
            experiment_path = self.experiment_path / "experiment.md"
            if experiment_path.exists():
                experiment_content = self.security.secure_read_text(experiment_path)
                corpus_files.append({
                    'content': experiment_content,
                    'file_path': str(experiment_path),
                    'filename': 'experiment.md',
                    'speaker': '',
                    'date': '',
                    'source_type': 'experiment_specification',
                    'start_char': 0,
                    'end_char': len(experiment_content),
                    'context': 'Experiment configuration and parameters'
                })
                self._log_progress(f"📋 Added experiment specification: {len(experiment_content)} chars")
            
            # 3. Add framework specification
            framework_path = self.experiment_path / self.config.get('framework', 'framework.md')
            if framework_path.exists():
                framework_content = self.security.secure_read_text(framework_path)
                corpus_files.append({
                    'content': framework_content,
                    'file_path': str(framework_path),
                    'filename': framework_path.name,
                    'speaker': '',
                    'date': '',
                    'source_type': 'framework_specification',
                    'start_char': 0,
                    'end_char': len(framework_content),
                    'context': 'Framework dimensions and methodology'
                })
                self._log_progress(f"📋 Added framework specification: {len(framework_content)} chars")
            
            # 4. Add statistical results if available
            if hasattr(self, '_analysis_results') and self._analysis_results:
                # Ensure all analysis results are JSON serializable
                def make_serializable(obj):
                    """Recursively convert objects to JSON-serializable format."""
                    if isinstance(obj, dict):
                        return {str(k): make_serializable(v) for k, v in obj.items()}
                    elif isinstance(obj, list):
                        return [make_serializable(item) for item in obj]
                    elif isinstance(obj, tuple):
                        return tuple(make_serializable(item) for item in obj)
                    elif hasattr(obj, '__dict__'):
                        # Handle objects with attributes
                        return make_serializable(vars(obj))
                    else:
                        # Convert non-serializable types to strings
                        try:
                            json.dumps(obj)
                            return obj
                        except (TypeError, ValueError):
                            return str(obj)

                serializable_results = make_serializable(self._analysis_results)
                analysis_json = json.dumps(serializable_results, indent=2)
                corpus_files.append({
                    'content': analysis_json,
                    'file_path': 'analysis_results.json',
                    'filename': 'analysis_results.json',
                    'speaker': '',
                    'date': '',
                    'source_type': 'statistical_results',
                    'start_char': 0,
                    'end_char': len(analysis_json),
                    'context': 'Raw analysis scores and statistical data'
                })
                self._log_progress(f"📋 Added analysis results: {len(analysis_json)} chars")
            
            # Index the corpus files using Typesense
            if corpus_files:
                if corpus_index_service.typesense_service.index_corpus_files(corpus_files):
                    self._log_progress(f"✅ Successfully indexed {len(corpus_files)} files in Typesense")
                    
                    # Build BM25 index for accurate scoring
                    corpus_dir = str(self.experiment_path)
                    corpus_index_service._build_bm25_index(corpus_dir, "corpus")
                    self._log_progress("✅ Built Python BM25 index for accurate scoring")
                else:
                    self._log_progress("⚠️ Failed to index corpus files, proceeding without indexing")
            else:
                self._log_progress("⚠️ No corpus files to index")
            
            return corpus_index_service
            
        except Exception as e:
            self._log_progress(f"❌ Error building hybrid corpus index service: {e}")
            # Return a basic hybrid service that will handle missing index gracefully
            from ..core.hybrid_corpus_service import HybridCorpusService
            return HybridCorpusService()

    def _run_evidence_retrieval(self, framework_hash: str, statistical_results_hash: str, evidence_artifact_hashes: List[str], audit_logger: AuditLogger) -> str:
        """Run the EvidenceRetrieverAgent to curate evidence for synthesis."""
        self._log_progress("🔍 Curating evidence for synthesis...")
        
        try:
            from ..agents.evidence_retriever_agent import EvidenceRetrieverAgent
            
            agent_config = {
                'experiment_path': str(self.experiment_path),
                'run_id': self.run_id,
                'artifact_storage': self.artifact_storage,
            }
            retriever_agent = EvidenceRetrieverAgent(agent_config)
            
            retrieval_results = retriever_agent.run(
                framework_hash=framework_hash,
                statistical_results_hash=statistical_results_hash,
                evidence_artifact_hashes=evidence_artifact_hashes
            )
            
            curated_evidence_hash = retrieval_results.get("evidence_artifact_hash")
            if not curated_evidence_hash:
                raise CleanAnalysisError("EvidenceRetrieverAgent did not return an artifact hash.")

            self._log_progress(f"✅ Evidence curation complete. Curated evidence stored in artifact: {curated_evidence_hash}")
            return curated_evidence_hash

        except Exception as e:
            self._log_progress(f"❌ Evidence retrieval and curation phase failed: {str(e)}")
            # For now, we will allow synthesis to proceed without curated evidence.
            # In a stricter future version, this might raise an exception.
            return None

    # REMOVED: 313 lines of THICK CSV generation code (lines 3782-4094)
    # All CSV generation methods removed:
    # - _generate_csv_files_direct() 
    # - _generate_scores_csv()
    # - _generate_derived_metrics_csv()
    # - _generate_evidence_csv() 
    # - _generate_metadata_csv()
    # CSV generation now handled by StatisticalAgent via tool calls
    def _copy_statistical_artifacts_to_results(self, run_id: str) -> Path:
        """THIN approach: Copy CSV files produced by StatisticalAgent to results directory."""
        self._log_progress("📊 THIN: Copying StatisticalAgent CSV outputs to results...")
        
        # Create results directory
        run_dir = self.experiment_path / "runs" / run_id
        results_dir = run_dir / "results"
        results_dir.mkdir(parents=True, exist_ok=True)
        
        # Find CSV artifacts produced by StatisticalAgent
        csv_files_copied = 0
        for artifact_hash, artifact_info in self.artifact_storage.registry.items():
            if isinstance(artifact_info, dict):
                metadata = artifact_info.get("metadata", {})
                if metadata.get("artifact_type") in ["statistical_csv", "derived_metrics_csv", "analysis_scores_csv"]:
                    # Copy CSV file to results directory with human-readable name
                    artifact_path = self.artifact_storage.artifacts_dir / artifact_hash
                    if artifact_path.exists():
                        csv_name = metadata.get("csv_filename", f"{metadata.get('artifact_type', 'data')}.csv")
                        target_path = results_dir / csv_name
                        target_path.write_bytes(artifact_path.read_bytes())
                        csv_files_copied += 1
                        self._log_progress(f"   • Copied: {csv_name}")
        
        if csv_files_copied == 0:
            self._log_progress("⚠️ No CSV files found from StatisticalAgent - may need to run statistical phase first")
        else:
            self._log_progress(f"✅ Copied {csv_files_copied} CSV files to results directory")
        
        return results_dir

    def _resume_from_statistical_prep(self, audit_logger: AuditLogger, run_id: str, start_time: datetime) -> Dict[str, Any]:
        """Resume from statistical preparation to full synthesis."""
        try:
            # Find the most recent statistical preparation run
            stats_runs = list(self.experiment_path.glob("runs/*/results/scores.csv"))
            if not stats_runs:
                raise CleanAnalysisError("No statistical preparation results found to resume from")
            
            latest_stats_run = max(stats_runs, key=lambda p: p.stat().st_mtime)
            stats_run_id = latest_stats_run.parent.parent.name
            stats_results_dir = latest_stats_run.parent
            
            self._log_progress(f"📊 Resuming from statistical preparation run: {stats_run_id}")
            
            # Initialize infrastructure for resume
            self._log_progress("🔧 Initializing infrastructure for resume...")
            self.artifact_storage = LocalArtifactStorage(
                security_boundary=self.security,
                run_folder=self.experiment_path / "runs" / run_id
            )
            
            # Load the existing analysis and derived metrics results
            self._log_progress("🔍 Loading analysis artifacts...")
            analysis_results = self._load_resume_artifacts(stats_run_id, "analysis")
            self._log_progress(f"🔍 Loaded {len(analysis_results) if analysis_results else 0} analysis results")
            
            self._log_progress("🔍 Loading derived metrics artifacts...")
            derived_metrics_results = self._load_resume_artifacts(stats_run_id, "derived_metrics")
            self._log_progress(f"🔍 Loaded derived metrics: {type(derived_metrics_results)}")
            
            if not analysis_results:
                raise CleanAnalysisError("Could not load analysis results from statistical preparation run")
            
            # Store results for synthesis access
            self._analysis_results = analysis_results
            
            # THIN: Evidence artifacts handled by EvidenceRetrieverAgent
            self._log_progress("🔍 THIN: Evidence artifacts will be handled by EvidenceRetrieverAgent")
            
            # Ensure derived metrics results have the correct structure for synthesis
            if derived_metrics_results and isinstance(derived_metrics_results, dict):
                # Create a proper structure for synthesis
                self._derived_metrics_results = {
                    'status': 'completed',
                    'derived_metrics_results': derived_metrics_results
                }
            else:
                self._derived_metrics_results = {
                    'status': 'completed',
                    'derived_metrics_results': {}
                }
            
            # Create new run directory for synthesis results
            run_dir = self.experiment_path / "runs" / run_id
            results_dir = run_dir / "results"
            results_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy statistical preparation results to new run
            self._copy_statistical_prep_results(stats_results_dir, results_dir)
            
            # Load specifications for synthesis
            self.config = self._load_specs()
            
            # Run synthesis phase
            self._log_progress("🔄 Resume mode: Running synthesis phase...")
            
            # Build RAG index for synthesis
            self._log_progress("📚 Building RAG index for synthesis...")
            self._build_rag_index(audit_logger)
            
            # Run statistical analysis
            statistical_results = self._run_statistical_analysis_phase(self.derived_metrics_model, audit_logger, analysis_results, derived_metrics_results)
            
            # Run evidence retrieval
            evidence_results = self._run_evidence_retrieval_phase(self.synthesis_model, audit_logger, statistical_results)
            
            # Run synthesis
            synthesis_results = self._run_synthesis(
                self.synthesis_model, 
                self.analysis_model,
                audit_logger, 
                statistical_results,
                evidence_results,
                run_id
            )
            
            if synthesis_results:
                self._log_progress("✅ Resume synthesis completed successfully")
                
                # Create results directory with final files (same as normal flow)
                self._log_progress("📁 Creating results directory with final files...")
                try:
                    # Prepare assets for results creation
                    assets = {
                        'report_hash': synthesis_results.get('report_hash'),
                        'stats_hash': statistical_results.get('stats_hash')
                    }
                    
                    # Create clean results directory (fact-checking system removed)
                    results_dir = self._create_clean_results_directory(run_id, statistical_results, assets)
                    self._log_progress(f"📁 Results directory created: {results_dir}")
                    
                except Exception as e:
                    self._log_progress(f"⚠️ Results creation failed: {str(e)}")
                    # Fall back to basic results directory
                    results_dir = self._create_basic_results_directory(run_id)
                
                duration = (datetime.now(timezone.utc) - start_time).total_seconds()
                log_experiment_complete(self.security.experiment_name, run_id, duration)
                
                return {
                    "run_id": run_id,
                    "results_directory": str(results_dir),
                    "analysis_documents": len(analysis_results),
                    "status": "completed_resume_synthesis",
                    "mode": "resume_from_stats",
                    "resumed_from": stats_run_id,
                    "duration_seconds": duration,
                    "performance_metrics": self._get_performance_summary(),
                    "costs": audit_logger.get_session_costs() if audit_logger else {"total_cost_usd": 0.0}
                }
            else:
                raise CleanAnalysisError("Synthesis phase failed during resume")
                
        except Exception as e:
            self._log_progress(f"❌ Resume from statistical preparation failed: {str(e)}")
            raise CleanAnalysisError(f"Resume from statistical preparation failed: {str(e)}")

    def _load_resume_artifacts(self, stats_run_id: str, artifact_type: str) -> Optional[Any]:
        """Load artifacts from a previous statistical preparation run."""
        try:
            # Look for artifacts in the shared cache
            shared_cache_dir = self.experiment_path / "shared_cache" / "artifacts"
            self._log_progress(f"🔍 Looking for {artifact_type} artifacts in: {shared_cache_dir}")
            if not shared_cache_dir.exists():
                self._log_progress(f"❌ Shared cache directory does not exist: {shared_cache_dir}")
                return None
            
            # Find artifacts by type
            if artifact_type == "analysis":
                # Look for analysis result artifacts
                analysis_files = list(shared_cache_dir.glob("analysis_result_*"))
                self._log_progress(f"🔍 Found {len(analysis_files)} analysis result files")
                if analysis_files:
                    # Load all analysis results and return as a list
                    analysis_results = []
                    for analysis_file in analysis_files:
                        self._log_progress(f"🔍 Loading analysis file: {analysis_file.name}")
                        with open(analysis_file, 'r', encoding='utf-8') as f:
                            analysis_data = json.load(f)
                            analysis_results.append(analysis_data)
                    self._log_progress(f"✅ Loaded {len(analysis_results)} analysis results")
                    return analysis_results
            
            elif artifact_type == "derived_metrics":
                # Look for derived metrics artifacts
                metrics_files = list(shared_cache_dir.glob("derived_metrics_results_with_data_*"))
                self._log_progress(f"🔍 Found {len(metrics_files)} derived metrics files")
                if metrics_files:
                    # Load the most recent derived metrics result
                    latest_metrics = max(metrics_files, key=lambda p: p.stat().st_mtime)
                    self._log_progress(f"🔍 Loading derived metrics file: {latest_metrics.name}")
                    with open(latest_metrics, 'r', encoding='utf-8') as f:
                        return json.load(f)
            
            self._log_progress(f"❌ No {artifact_type} artifacts found")
            return None
            
        except Exception as e:
            self._log_progress(f"⚠️ Could not load {artifact_type} artifacts: {str(e)}")
            import traceback
            self._log_progress(f"⚠️ Traceback: {traceback.format_exc()}")
            return None

    def _copy_statistical_prep_results(self, source_dir: Path, target_dir: Path) -> None:
        """Copy statistical preparation results to the new run directory."""
        try:
            # Copy CSV files
            for csv_file in source_dir.glob("*.csv"):
                target_file = target_dir / csv_file.name
                target_file.write_text(csv_file.read_text())
                self._log_progress(f"📋 Copied {csv_file.name} from statistical preparation")
            
            # Create a resume manifest
            resume_manifest = {
                "resume_info": {
                    "resumed_from_run": source_dir.parent.name,
                    "resume_timestamp": datetime.now(timezone.utc).isoformat(),
                    "original_statistical_prep_files": [f.name for f in source_dir.glob("*.csv")]
                }
            }
            
            manifest_file = target_dir / "resume_manifest.json"
            manifest_file.write_text(json.dumps(resume_manifest, indent=2))
            
        except Exception as e:
            self._log_progress(f"⚠️ Could not copy all statistical preparation results: {str(e)}")
            # Don't fail the entire resume for this

    # REMOVED: _create_evidence_artifacts_from_analysis() - DEPRECATED
    # Evidence artifacts now handled by EvidenceRetrieverAgent
    
    def _create_provenance_organization(self, run_id: str, audit_logger: AuditLogger) -> None:
        """Create provenance organization for the run."""
        try:
            self._log_progress("📊 Creating provenance organization...")
            run_dir = self.experiment_path / "runs" / run_id
            shared_cache_dir = self.experiment_path / "shared_cache"

            # Create ProvenanceOrganizer and organize artifacts
            provenance_organizer = ProvenanceOrganizer(self.security, audit_logger)
            provenance_result = provenance_organizer.organize_run_artifacts(
                run_dir=run_dir,
                shared_cache_dir=shared_cache_dir,
                experiment_metadata={
                    "experiment_name": self.security.experiment_name,
                    "run_id": run_id,
                    "framework": self.config.get('framework', {}),
                    "corpus": self.config.get('corpus', {}),
                    "completion_time": datetime.now(timezone.utc).isoformat()
                }
            )
            self._log_status("Provenance organization completed")
        except Exception as e:
            self._log_progress(f"⚠️ Provenance organization failed: {str(e)}")
            # Continue without provenance organization - not fatal
    
    def _reorganize_directory_structure(self, run_id: str, audit_logger: AuditLogger) -> None:
        """Reorganize directory structure for stakeholder-friendly access."""
        try:
            self._log_progress("📁 Reorganizing directory structure...")
            run_dir = self.experiment_path / "runs" / run_id
            
            # Reorganize directory structure
            reorganization_result = reorganize_directory_structure(run_dir)
            
            self._log_status(f"Directory reorganization completed: {reorganization_result['reorganization_summary']['total_directories_created']} directories, {reorganization_result['reorganization_summary']['total_files_moved']} files moved")
        except Exception as e:
            self._log_progress(f"⚠️ Directory reorganization failed: {str(e)}")
            # Continue without directory reorganization - not fatal
    
    def _auto_commit_run(self, run_id: str, audit_logger: AuditLogger) -> None:
        """Auto-commit completed research run to Git with mode-aware commit messages."""
        try:
            import subprocess
            
            run_folder = self.experiment_path / "runs" / run_id
            repo_root = self._detect_repo_root()
            if repo_root is None:
                self._log_progress("⚠️ Could not detect Git repository root; skipping auto-commit")
                return
            
            # Add the run directory to Git (force to override .gitignore for research preservation)
            result = subprocess.run(
                ["git", "add", "--force", str(run_folder.relative_to(repo_root))],
                cwd=repo_root,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                audit_logger.log_error("auto_commit_add_failed", result.stderr, {
                    "run_folder": str(run_folder),
                    "git_add_stderr": result.stderr
                })
                self._log_progress(f"⚠️ Git add failed: {result.stderr}")
                return
            
            # Create mode-aware commit message
            experiment_name = self.security.experiment_name
            commit_msg = self._generate_commit_message(run_id, experiment_name)
            
            # Ensure commit message is under 50 characters (per .cursor/rules)
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
                audit_logger.log_error("auto_commit_failed", result.stderr, {
                    "run_folder": str(run_folder),
                    "git_commit_stderr": result.stderr,
                    "commit_message": commit_msg
                })
                self._log_progress(f"⚠️ Git commit failed: {result.stderr}")
                return
            
            # Check for successful commit in output (git pre-commit hooks can write to stderr but still succeed)
            if "nothing to commit" in result.stdout.lower():
                self._log_progress("ℹ️ No changes to commit")
                return
            
            self._log_status(f"📝 Auto-committed to Git: {commit_msg}")
            
        except subprocess.TimeoutExpired:
            audit_logger.log_error("auto_commit_timeout", "Git command timed out", {
                "run_folder": str(run_folder)
            })
            self._log_progress("⚠️ Git commit timed out")
        except Exception as e:
            audit_logger.log_error("auto_commit_error", str(e), {
                "run_folder": str(run_folder)
            })
            self._log_progress(f"⚠️ Git commit failed: {str(e)}")
    
    def _detect_repo_root(self) -> Optional[Path]:
        """Detect the Git repository root robustly.
        
        Tries `git rev-parse --show-toplevel`, falling back to walking up
        from `self.experiment_path` until a `.git` directory is found.
        Returns None if no repo root can be determined.
        """
        import subprocess
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                cwd=self.experiment_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                top = result.stdout.strip()
                if top:
                    return Path(top)
        except Exception:
            pass
        # Fallback: walk up to find .git
        try:
            current = self.experiment_path
            for parent in [current] + list(current.parents):
                if (parent / ".git").exists():
                    return parent
        except Exception:
            pass
        return None
    
    def _generate_commit_message(self, run_id: str, experiment_name: str) -> str:
        """Generate mode-aware commit message based on run type."""
        if self.analysis_only:
            return f"Analysis only: {experiment_name}"
        elif self.statistical_prep:
            return f"Statistical prep: {experiment_name}"
        elif self.skip_synthesis:
            return f"Skip synthesis: {experiment_name}"
        elif self.resume_from_stats:
            return f"Resume from stats: {experiment_name}"
        else:
            return f"Complete run: {experiment_name}"
    
    def _create_clean_outputs_directory(self, run_id: str, statistical_results: Dict[str, Any], assets: Dict[str, Any]) -> Path:
        """Create outputs directory with publication readiness features."""
        # Create run directory structure
        run_dir = self.experiment_path / "runs" / run_id
        outputs_dir = run_dir / "outputs"
        outputs_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy corpus documents (CRIT-001)
        self._copy_corpus_documents_to_outputs(outputs_dir)
        
        # Copy evidence database (CRIT-002)
        self._copy_evidence_database_to_outputs(outputs_dir)
        
        # Copy source metadata (CRIT-003)
        self._copy_source_metadata_to_outputs(outputs_dir)
        
        # Save statistical results
        metadata_dir = outputs_dir / "metadata"
        metadata_dir.mkdir(exist_ok=True)
        stats_file = metadata_dir / "statistical_results.json"
        
        # Convert numpy types to JSON-serializable types
        import numpy as np
        
        def convert_to_serializable(obj):
            """Convert numpy and other non-JSON types to serializable types."""
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, (np.integer, np.int64, np.int32)):
                return int(obj)
            elif isinstance(obj, (np.floating, np.float64, np.float32)):
                return float(obj)
            elif isinstance(obj, (np.bool_, bool)):
                return bool(obj)
            elif isinstance(obj, dict):
                # Handle tuple keys by converting them to string representations
                serializable_dict = {}
                for k, v in obj.items():
                    if isinstance(k, tuple):
                        # Convert tuple keys to string format: ('a', 'b') -> "a__b"
                        serializable_key = "__".join(str(item) for item in k)
                    else:
                        serializable_key = k
                    serializable_dict[serializable_key] = convert_to_serializable(v)
                return serializable_dict
            elif isinstance(obj, list):
                return [convert_to_serializable(item) for item in obj]
            else:
                return obj
        
        serializable_stats = convert_to_serializable(statistical_results)
        
        with open(stats_file, 'w') as f:
            json.dump(serializable_stats, f, indent=2)
        
        # Save final report
        self._log_progress(f"🔧 DEBUG: Checking for report_hash in assets: {list(assets.keys())}")
        if 'report_hash' in assets:
            self._log_progress(f"🔧 DEBUG: Found report_hash: {assets['report_hash']}")
            report_content = self.artifact_storage.get_artifact(assets['report_hash'])
            report_file = outputs_dir / "final_report.md"
            
            # Save final report with appended log summary
            with open(report_file, 'wb') as f:
                f.write(report_content)
            
            # Append experiment log summary
            self._append_experiment_log_summary(report_file, run_id)
            self._log_progress("📝 Final report saved to outputs with log summary")
        else:
            self._log_progress("❌ DEBUG: No report_hash found in assets - final report not saved")
        
        # Save synthesis metadata
        synthesis_file = metadata_dir / "assets.json"  # Fixed typo
        with open(synthesis_file, 'w') as f:
            # Remove large content to keep metadata file clean
            clean_synthesis = {k: v for k, v in assets.items() if k != 'assets'}
            json.dump(clean_synthesis, f, indent=2)
        
        # Create experiment summary
        summary = {
            "experiment_name": self.security.experiment_name,
            "run_id": run_id,
            "framework": self.config.get("framework", "unknown"),
            "corpus": self.config.get("corpus", "unknown"),
            "completion_time": datetime.now(timezone.utc).isoformat(),
            "artifacts": {
                "metadata/statistical_results.json": "Statistical analysis results",
                "metadata/assets.json": "Synthesis results",
                "corpus/": "Source documents for verification",
                "evidence/": "Evidence database for quote verification",
                "metadata/": "Source metadata for context verification"
            }
        }
        
        summary_file = metadata_dir / "experiment_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        return outputs_dir
    
    def _append_experiment_log_summary(self, report_file: Path, run_id: str) -> None:
        """
        Append experiment log summary to the final report.
        
        Includes total costs, execution time, cache performance, and warnings/errors.
        """
        try:
            # Get session costs and performance data
            audit_logger = getattr(self, '_current_audit_logger', None)
            session_costs = audit_logger.get_session_costs() if audit_logger else {"total_cost_usd": 0.0}
            
            # Calculate total execution time
            start_time = getattr(self, '_experiment_start_time', datetime.now(timezone.utc))
            end_time = datetime.now(timezone.utc)
            total_duration = (end_time - start_time).total_seconds()
            
            # Format duration
            minutes = int(total_duration // 60)
            seconds = int(total_duration % 60)
            duration_str = f"{minutes}m {seconds}s" if minutes > 0 else f"{seconds}s"
            
            # Get cache performance
            cache_performance = self._generate_cache_performance_report()
            cache_hits = cache_performance.get('total_hits', 0)
            cache_misses = cache_performance.get('total_misses', 0)
            total_cache_ops = cache_hits + cache_misses
            hit_rate = (cache_hits / total_cache_ops * 100) if total_cache_ops > 0 else 0
            
            # Determine pipeline mode
            pipeline_mode = "Full (analysis → derived metrics → evidence retrieval → synthesis)"
            if self.analysis_only:
                pipeline_mode = "Analysis only"
            elif self.statistical_prep:
                pipeline_mode = "Statistical preparation (analysis → derived metrics → CSV export)"
            elif self.skip_synthesis:
                pipeline_mode = "Skip synthesis (analysis → derived metrics → evidence retrieval)"
            
            # Generate cost breakdown if available
            cost_breakdown = []
            total_cost = session_costs.get('total_cost_usd', 0.0)
            operations = session_costs.get('operations', {})
            
            if operations and total_cost > 0:
                for operation, data in operations.items():
                    cost = data.get('cost_usd', 0.0)
                    percentage = (cost / total_cost * 100) if total_cost > 0 else 0
                    cost_breakdown.append(f"- {operation.replace('_', ' ').title()}: ${cost:.4f} USD ({percentage:.0f}%)")
            
            # Collect warnings/errors (simplified for now)
            warnings_errors = []
            if cache_misses > 0:
                warnings_errors.append(f"- {cache_misses} cache miss(es) - some components regenerated")
            if not warnings_errors:
                warnings_errors.append("- No critical errors or warnings")
            
            # Build log summary
            log_summary = f"""
---

## Experiment Log Summary

**Total Experiment Cost**: ${total_cost:.4f} USD
**Total Execution Time**: {duration_str}
**Pipeline Mode**: {pipeline_mode}
**Cache Performance**: {cache_hits} hits, {cache_misses} misses ({hit_rate:.0f}% hit rate)

### Cost Breakdown
{chr(10).join(cost_breakdown) if cost_breakdown else "- Cost breakdown not available"}

### Warnings/Errors
{chr(10).join(warnings_errors)}

**Run Completed**: {end_time.strftime('%Y-%m-%d %H:%M:%S')} UTC
**Experiment ID**: {self.security.experiment_name}/{run_id}
"""
            
            # Append to report file
            with open(report_file, 'a', encoding='utf-8') as f:
                f.write(log_summary)
                
        except Exception as e:
            self._log_progress(f"⚠️ Failed to append log summary: {str(e)}")
    
    def _create_basic_outputs_directory(self, run_id: str) -> Path:
        """Create a basic outputs directory in case of failure."""
        self._log_progress(f"⚠️ Creating basic outputs directory for run {run_id}")
        run_dir = self.experiment_path / "runs" / run_id
        outputs_dir = run_dir / "outputs"
        outputs_dir.mkdir(parents=True, exist_ok=True)
        
        # Create basic summary
        summary = {
            "experiment_name": self.security.experiment_name,
            "run_id": run_id,
            "status": "basic_outputs_created",
            "completion_time": datetime.now(timezone.utc).isoformat()
        }
        
        summary_file = outputs_dir / "experiment_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        return outputs_dir

    def _copy_corpus_documents_to_outputs(self, outputs_dir: Path) -> None:
        """Copy corpus documents to outputs directory for source verification."""
        try:
            corpus_outputs_dir = outputs_dir / "corpus"
            corpus_outputs_dir.mkdir(exist_ok=True)
            
            corpus_documents = self._load_corpus_documents()
            corpus_dir = self.experiment_path / "corpus"
            documents_copied = 0
            
            for doc_info in corpus_documents:
                filename = doc_info.get("filename")
                if not filename:
                    continue
                
                source_file = corpus_dir / filename
                if source_file.exists():
                    target_file = corpus_outputs_dir / filename
                    shutil.copy2(str(source_file), str(target_file))
                    documents_copied += 1
            
            self._log_progress(f"📄 Copied {documents_copied} corpus documents to outputs")
            
        except Exception as e:
            self._log_progress(f"⚠️ Failed to copy corpus documents to outputs: {str(e)}")
    
    def _copy_evidence_database_to_outputs(self, outputs_dir: Path) -> None:
        """Copy evidence database to outputs directory."""
        try:
            evidence_outputs_dir = outputs_dir / "evidence"
            evidence_outputs_dir.mkdir(exist_ok=True)
            
            # Find evidence database in artifacts
            evidence_database_found = False
            for artifact_hash, artifact_info in self.artifact_storage.registry.items():
                metadata = artifact_info.get("metadata", {})
                if metadata.get("artifact_type", "").startswith("evidence_v6"):
                    evidence_content = self.artifact_storage.get_artifact(artifact_hash)
                    evidence_file = evidence_outputs_dir / "evidence_database.json"
                    with open(evidence_file, "wb") as f:
                        f.write(evidence_content)
                    evidence_database_found = True
                    break
            
            if evidence_database_found:
                self._log_progress("📊 Evidence database copied to outputs")
            else:
                self._log_progress("⚠️ No evidence database found to copy")
                
        except Exception as e:
            self._log_progress(f"⚠️ Failed to copy evidence database to outputs: {str(e)}")
    
    def _copy_source_metadata_to_outputs(self, outputs_dir: Path) -> None:
        """Copy source metadata to outputs directory."""
        try:
            metadata_outputs_dir = outputs_dir / "metadata"
            metadata_outputs_dir.mkdir(exist_ok=True)
            
            # Create basic source metadata
            source_metadata = {
                "experiment_name": self.security.experiment_name,
                "framework": self.config.get("framework", "unknown"),
                "corpus": self.config.get("corpus", "unknown"),
                "run_timestamp": datetime.now(timezone.utc).isoformat(),
                "total_documents": len(self._load_corpus_documents())
            }
            
            metadata_file = metadata_outputs_dir / "source_metadata.json"
            with open(metadata_file, "w") as f:
                json.dump(source_metadata, f, indent=2)
            
            self._log_progress("📋 Source metadata copied to outputs")
            
        except Exception as e:
            self._log_progress(f"⚠️ Failed to copy source metadata to outputs: {str(e)}")
    
    def _create_statistical_package(self, data_dir: Path, run_id: str) -> None:
        """Create statistical package directory with researcher-ready data package."""
        try:
            self._log_progress("📦 Creating statistical package...")
            
            # Create statistical package directory
            run_dir = self.experiment_path / "runs" / run_id
            stats_package_dir = run_dir / "statistical_package"
            stats_package_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy main dataset
            scores_file = data_dir / "scores.csv"
            if scores_file.exists():
                shutil.copy2(str(scores_file), str(stats_package_dir / "discernus_data.csv"))
            
            # Copy evidence file
            evidence_file = data_dir / "evidence.csv"
            if evidence_file.exists():
                shutil.copy2(str(evidence_file), str(stats_package_dir / "full_evidence.csv"))
            
            # Create variable codebook
            self._create_variable_codebook(stats_package_dir)
            
            # Create README
            self._create_statistical_package_readme(stats_package_dir)
            
            # Create import scripts
            self._create_import_scripts(stats_package_dir)
            
            self._log_progress(f"✅ Statistical package created: {stats_package_dir}")
            
        except Exception as e:
            self._log_progress(f"⚠️ Failed to create statistical package: {str(e)}")
    
    def _create_variable_codebook(self, stats_package_dir: Path) -> None:
        """Create variable codebook with column definitions."""
        try:
            codebook_file = stats_package_dir / "variable_codebook.csv"
            
            # Basic codebook structure
            codebook_data = [
                ["variable_name", "description", "data_type", "value_range", "notes"],
                ["document_id", "Unique identifier for each document", "string", "alphanumeric", "Primary key"],
                ["document_name", "Human-readable document name", "string", "text", "Source document identifier"],
                ["dimension_*", "Framework dimension scores", "float", "0.0-1.0", "Normalized scores for each framework dimension"],
                ["confidence_*", "Confidence scores for dimensions", "float", "0.0-1.0", "LLM confidence in scoring"],
                ["evidence_count", "Number of supporting evidence quotes", "integer", "0+", "Count of evidence quotes found"],
                ["analysis_timestamp", "When analysis was performed", "datetime", "ISO format", "Analysis completion time"]
            ]
            
            with open(codebook_file, 'w', newline='', encoding='utf-8') as f:
                import csv
                writer = csv.writer(f)
                writer.writerows(codebook_data)
                
        except Exception as e:
            self._log_progress(f"⚠️ Failed to create variable codebook: {str(e)}")
    
    def _create_statistical_package_readme(self, stats_package_dir: Path) -> None:
        """Create README for statistical package."""
        try:
            readme_file = stats_package_dir / "README.txt"
            
            readme_content = f"""Statistical Package for {self.security.experiment_name}
Generated by Discernus on {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}

This package contains analysis-ready data for statistical analysis.

FILES:
- discernus_data.csv: Main dataset with scores and metadata
- full_evidence.csv: Complete evidence quotes supporting the analysis
- variable_codebook.csv: Column definitions and data dictionary
- import_scripts/: Tool-specific import scripts

USAGE:
1. Load discernus_data.csv into your preferred statistical tool
2. Review variable_codebook.csv for column definitions
3. Use import_scripts/ for automated data loading
4. Perform your own statistical analysis and interpretation

CITATION:
Text analysis performed using Discernus; statistical analysis by [your method]

For questions about the text analysis methodology, refer to the complete
provenance documentation in the parent directory.
"""
            
            with open(readme_file, 'w', encoding='utf-8') as f:
                f.write(readme_content)
                
        except Exception as e:
            self._log_progress(f"⚠️ Failed to create statistical package README: {str(e)}")
    
    def _create_import_scripts(self, stats_package_dir: Path) -> None:
        """Create import scripts for common statistical tools."""
        try:
            scripts_dir = stats_package_dir / "import_scripts"
            scripts_dir.mkdir(exist_ok=True)
            
            # R script
            r_script = scripts_dir / "import_r.R"
            with open(r_script, 'w') as f:
                f.write("""# R Import Script for Discernus Data
# Load the main dataset
data <- read.csv("discernus_data.csv", stringsAsFactors = FALSE)

# Load evidence data
evidence <- read.csv("full_evidence.csv", stringsAsFactors = FALSE)

# Load variable codebook
codebook <- read.csv("variable_codebook.csv", stringsAsFactors = FALSE)

# Basic data exploration
str(data)
summary(data)

# Check for missing values
sapply(data, function(x) sum(is.na(x)))
""")
            
            # SPSS script
            spss_script = scripts_dir / "import_spss.sps"
            with open(spss_script, 'w') as f:
                f.write("""* SPSS Import Script for Discernus Data
GET DATA
  /TYPE=TXT
  /FILE="discernus_data.csv"
  /DELCASE=LINE
  /DELIMITERS=","
  /ARRANGEMENT=DELIMITED
  /FIRSTCASE=2
  /IMPORTCASE=ALL
  /VARIABLES=
  document_id A20
  document_name A50
  dimension_* F8.3
  confidence_* F8.3
  evidence_count F8.0
  analysis_timestamp A30.

* Basic descriptive statistics
DESCRIPTIVES VARIABLES=ALL
  /STATISTICS=MEAN STDDEV MIN MAX.

* Check for missing values
FREQUENCIES VARIABLES=ALL
  /STATISTICS=ALL.
""")
            
            # Stata script
            stata_script = scripts_dir / "import_stata.do"
            with open(stata_script, 'w') as f:
                f.write("""* Stata Import Script for Discernus Data
import delimited "discernus_data.csv", clear

* Set variable labels
label variable document_id "Document identifier"
label variable document_name "Document name"
label variable evidence_count "Number of evidence quotes"

* Basic data exploration
describe
summarize

* Check for missing values
misstable summarize

* Save as Stata format
save "discernus_data.dta", replace
""")
            
        except Exception as e:
            self._log_progress(f"⚠️ Failed to create import scripts: {str(e)}")

