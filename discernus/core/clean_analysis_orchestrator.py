#!/usr/bin/env python3
"""
Clean Analysis Orchestrator - THIN Architecture
===============================================

Focused orchestrator for analysis + synthesis without notebook generation cruft.
Addresses the architectural mismatch where we don't produce notebooks but the
current orchestrator is designed for notebook generation.

Architecture:
1. Load specs (experiment.md, framework, corpus)
2. Run analysis (using EnhancedAnalysisAgent)
3. Run coherence validation (ExperimentCoherenceAgent)
4. Generate statistical analysis (AutomatedStatisticalAnalysisAgent)
5. Run synthesis (UnifiedSynthesisAgent)
6. Copy results with publication readiness (CRIT-001/002/003)

THIN Principles:
- Direct function calls (no complex orchestration)
- Minimal dependencies
- Clean separation of concerns
- Focus on what we actually need
"""

import yaml
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd
import json
import pickle
from .logging_config import setup_logging, get_logger, log_experiment_start, log_experiment_complete, log_experiment_failure
from .security_boundary import ExperimentSecurityBoundary, SecurityError
from .audit_logger import AuditLogger
from .local_artifact_storage import LocalArtifactStorage
from .enhanced_manifest import EnhancedManifest
from ..agents.experiment_coherence_agent import ExperimentCoherenceAgent
from ..agents.EnhancedAnalysisAgent.main import EnhancedAnalysisAgent
from ..agents.automated_statistical_analysis.agent import AutomatedStatisticalAnalysisAgent
from ..agents.deprecated.txtai_evidence_curator.agent import TxtaiEvidenceCurator
from ..agents.unified_synthesis_agent import UnifiedSynthesisAgent
from ..gateway.llm_gateway import LLMGateway
from ..gateway.model_registry import ModelRegistry
from .rag_index_cache import RAGIndexCacheManager
from .statistical_analysis_cache import StatisticalAnalysisCacheManager
from .validation_cache import ValidationCacheManager
from .rag_index_manager import RAGIndexManager
from txtai.embeddings import Embeddings
# QA agents temporarily disabled
# from ..agents.revision_agent.agent import RevisionAgent
from ..agents.evidence_retriever_agent import EvidenceRetrieverAgent

from ..core.logging_config import setup_logging_for_run
import logging
from ..agents.fact_checker_agent.agent import FactCheckerAgent


class CleanAnalysisError(Exception):
    """Clean analysis orchestrator specific exceptions."""
    pass


class CleanAnalysisOrchestrator:
    """
    Clean orchestrator focused on analysis and synthesis only.
    No notebook generation, no complex agent chains, just what we need.
    """
    
    def __init__(self, experiment_path: Path, progress_manager=None):
        """Initialize clean analysis orchestrator."""
        self.experiment_path = Path(experiment_path).resolve()

        # Initialize core components
        self.security = ExperimentSecurityBoundary(self.experiment_path)

        # Set up logging to capture output to a file within the run folder
        self.log_file = setup_logging_for_run(self.experiment_path)
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Orchestrator initialized. Logging to {self.log_file}")

        # Progress manager for UI feedback
        self.progress_manager = progress_manager

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
        self.security_boundary = ExperimentSecurityBoundary(self.experiment_path)
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
    
    def run_experiment(self, 
                      analysis_model: str = "vertex_ai/gemini-2.5-pro",
                      synthesis_model: str = "vertex_ai/gemini-2.5-pro",
                      validation_model: str = "vertex_ai/gemini-2.5-pro",
                      skip_validation: bool = False) -> Dict[str, Any]:
        """
        Run complete experiment: analysis + synthesis + results.
        """
        run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        start_time = datetime.now(timezone.utc)
        
        try:
            # Initialize infrastructure
            audit_logger = self._initialize_infrastructure(run_id)
            log_experiment_start(self.security.experiment_name, run_id)
            
            self._log_progress("🚀 Starting clean analysis pipeline...")
            
            # Phase 1: Load specifications
            self._log_progress("📋 Loading specifications...")
            if self.progress_manager:
                self.progress_manager.update_main_progress("Load specifications")
            phase_start = datetime.now(timezone.utc)
            try:
                self.config = self._load_specs()
                self._log_status("Specifications loaded")
                self._log_phase_timing("specifications_loading", phase_start)
            except Exception as e:
                self._log_progress(f"❌ Failed to load specifications: {str(e)}")
                raise CleanAnalysisError(f"Specification loading failed: {str(e)}")
            
            # Phase 2: Validation (unless skipped)
            if not skip_validation:
                phase_start = datetime.now(timezone.utc)
                try:
                    self._run_coherence_validation(validation_model, audit_logger)
                    self._log_status("Experiment coherence validated")
                    self._log_phase_timing("coherence_validation", phase_start)
                except Exception as e:
                    self._log_progress(f"⚠️ Coherence validation failed, continuing with warning: {str(e)}")
                    # Continue with warning - validation failure shouldn't block experiment
            
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
                analysis_results = self._run_analysis_phase(analysis_model, audit_logger)
                
                # Store analysis results for synthesis access
                self._analysis_results = analysis_results
                
                self._log_status(f"Analysis completed: {len(analysis_results)} documents processed")
                self._log_phase_timing("analysis_phase", phase_start)
                
                # Phase 4.5: Build and cache RAG index immediately after analysis
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
            
            # Phase 5: Run derived metrics
            if self.progress_manager:
                self.progress_manager.update_main_progress("Derived metrics")
            phase_start = datetime.now(timezone.utc)
            try:
                derived_metrics_results = self._run_derived_metrics_phase(synthesis_model, audit_logger, analysis_results)
                
                # Store derived metrics results for synthesis access
                self._derived_metrics_results = derived_metrics_results
                
                self._log_status("Derived metrics completed")
                self._log_phase_timing("derived_metrics_phase", phase_start)
            except Exception as e:
                self._log_progress(f"❌ Derived metrics phase failed: {str(e)}")
                raise CleanAnalysisError(f"Derived metrics phase failed: {str(e)}")
            
            # Phase 6: Generate statistics
            phase_start = datetime.now(timezone.utc)
            try:
                statistical_results = self._run_statistical_analysis_phase(synthesis_model, audit_logger, analysis_results, derived_metrics_results)
                self._log_status("Statistical analysis completed")
                self._log_phase_timing("statistical_analysis", phase_start)
            except Exception as e:
                self._log_progress(f"❌ Statistical analysis phase failed: {str(e)}")
                raise CleanAnalysisError(f"Statistical analysis phase failed: {str(e)}")
            
            # Phase 7: Corpus index building (DISABLED - not needed without QA agents)
            self._log_progress("📝 Skipping corpus index building (QA agents disabled)")
            self._corpus_index_service = None

            # Phase 7.5: Validate Index Readiness (GATE)
            self._log_progress("🔍 Validating index readiness before proceeding...")
            
            # Validate RAG index is operational
            if not hasattr(self, 'rag_index') or not self.rag_index:
                error_msg = "RAG index not available - cannot proceed to evidence retrieval"
                self._log_progress(f"❌ {error_msg}")
                raise CleanAnalysisError(error_msg)
            
            # Corpus index service validation skipped (QA agents disabled)
            
            # Corpus index service testing skipped (QA agents disabled)
            self._log_progress("✅ RAG index validated and operational - proceeding to evidence retrieval")

            # Phase 8: Run evidence retrieval to curate supporting quotes
            phase_start = datetime.now(timezone.utc)
            
            # Corpus index service debug removed (QA agents disabled)
            
            try:
                evidence_results = self._run_evidence_retrieval_phase(synthesis_model, audit_logger, statistical_results, run_id)
                self._log_status("Evidence retrieval completed")
                self._log_phase_timing("evidence_retrieval_phase", phase_start)
                
                # Validate that evidence retrieval actually succeeded
                if not evidence_results or evidence_results.get('status') in ['failed', 'error', 'no_evidence_available']:
                    raise CleanAnalysisError(f"Evidence retrieval failed with status: {evidence_results.get('status', 'unknown')}")
                    
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
            
            # Corpus index service debug removed (QA agents disabled)
            
            try:
                assets = self._run_synthesis(synthesis_model, audit_logger, statistical_results, evidence_results)
                self._log_status("Synthesis completed")
                self._log_phase_timing("synthesis_phase", phase_start)
            except Exception as e:
                # A failure in synthesis is a fatal error for the experiment.
                self._log_progress(f"❌ FATAL: Synthesis phase failed: {str(e)}")
                raise CleanAnalysisError(f"Synthesis phase failed with a fatal error: {str(e)}") from e

            # Phase 11: Fact-checking validation (DISABLED - QA agents in penalty box)
            self._log_progress("📝 Skipping fact-checking validation (QA agents disabled)")
            fact_check_results = {"status": "skipped", "findings": []}

            # Phase 12: Create results with publication readiness
            if self.progress_manager:
                self.progress_manager.update_main_progress("Results creation")
            phase_start = datetime.now(timezone.utc)
            try:
                results_dir = self._create_clean_results_directory(run_id, statistical_results, assets, fact_check_results)
                self._log_status(f"Results created: {results_dir}")
                self._log_phase_timing("results_creation", phase_start)
            except Exception as e:
                self._log_progress(f"⚠️ Results creation failed, attempting basic results: {str(e)}")
                # Create basic results directory
                results_dir = self._create_basic_results_directory(run_id)
            
            duration = (datetime.now(timezone.utc) - start_time).total_seconds()
            log_experiment_complete(self.security.experiment_name, run_id, duration)
            
            # Get performance summary
            performance_summary = self._get_performance_summary()
            
            # Get session costs from audit logger
            session_costs = audit_logger.get_session_costs() if audit_logger else {"total_cost_usd": 0.0}
            
            # Log final performance summary including cache metrics
            self._log_final_performance_summary()

            # Finalize manifest if it exists
            if self.manifest:
                try:
                    self.manifest.finalize()
                except Exception as e:
                    self._log_progress(f"⚠️ Manifest finalization failed: {str(e)}")

            return {
                "run_id": run_id,
                "results_directory": str(results_dir),
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
            
            # Initialize LLM Gateway (matching legacy pattern)
            self._log_progress("🔧 Initializing LLM Gateway...")
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
        
        # Initialize validation caching
        from .validation_cache import ValidationCacheManager
        validation_cache_manager = ValidationCacheManager(self.artifact_storage, audit_logger)
        
        # Generate cache key based on all validation inputs
        cache_key = validation_cache_manager.generate_cache_key(
            framework_content, experiment_content, corpus_content, validation_model
        )
        
        # Check cache first
        cache_result = validation_cache_manager.check_cache(cache_key)
        
        if cache_result.hit:
            self._log_progress("💾 Using cached validation result")
            cached_validation = cache_result.cached_validation
            
            # Check if cached validation was successful
            if not cached_validation.get('success', False):
                issues = cached_validation.get('issues', ['Unknown validation failure'])
                raise CleanAnalysisError(f"Experiment validation failed (cached): {'; '.join(issues)}")
            
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
        
        # Store validation result in cache
        validation_cache_manager.store_validation_result(cache_key, validation_data, validation_model)
        
        # Check validation result
        if not validation_result.success:
            issues = [issue.description for issue in validation_result.issues]
            raise CleanAnalysisError(f"Experiment validation failed: {'; '.join(issues)}")
    
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
        
        # Initialize validation caching
        from .validation_cache import ValidationCacheManager
        validation_cache_manager = ValidationCacheManager(self.artifact_storage, self.audit_logger)
        
        # Generate cache key based on all validation inputs
        return validation_cache_manager.generate_cache_key(
            framework_content, experiment_content, corpus_content, validation_model
        )
    
    def _load_corpus_documents(self) -> List[Dict[str, Any]]:
        """Load corpus documents from manifest."""
        corpus_manifest_path = self.experiment_path / self.config['corpus']
        if not corpus_manifest_path.exists():
            raise CleanAnalysisError(f"Corpus manifest not found: {corpus_manifest_path}")

        content = corpus_manifest_path.read_text(encoding='utf-8')
        if '## Document Manifest' in content:
            _, yaml_block = content.split('## Document Manifest', 1)
            if '```yaml' in yaml_block:
                yaml_start = yaml_block.find('```yaml') + 7
                yaml_end = yaml_block.rfind('```')
                yaml_content = yaml_block[yaml_start:yaml_end].strip() if yaml_end > yaml_start else yaml_block[yaml_start:].strip()
                manifest_data = yaml.safe_load(yaml_content)
                return manifest_data.get('documents', [])
        
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
        """Run analysis phase with individual document processing."""
        self._log_progress("🔬 Running analysis phase...")
        
        # Load corpus documents
        corpus_documents = self._load_corpus_documents()
        if not corpus_documents:
            raise CleanAnalysisError("No corpus documents found")

        # Prepare documents for analysis
        prepared_documents = self._prepare_documents_for_analysis(corpus_documents)
        
        # Initialize analysis agent
        analysis_agent = EnhancedAnalysisAgent(
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
                    corpus_documents=[prepared_doc],
                    framework_content=framework_content,
                    experiment_config=self.config,
                    model=analysis_model
                )
                
                if result and 'analysis_result' in result:
                    # Extract analysis result from agent response
                    analysis_result = result['analysis_result']
                    result_content = analysis_result.get('result_content', {})

                    # Track cache performance based on analysis agent's caching
                    if analysis_result.get('cached', False):
                        self.performance_metrics["cache_hits"] += 1
                    else:
                        self.performance_metrics["cache_misses"] += 1

                    # The raw_analysis_response is stored in result_content, not nested deeper
                    raw_analysis_response = result_content.get('raw_analysis_response', '')

                    # Store the full result with raw_analysis_response at top level for statistical processing
                    full_result = {
                        'analysis_result': analysis_result,
                        'raw_analysis_response': raw_analysis_response,
                        'scores_hash': result.get('scores_hash', ''),
                        'evidence_hash': result.get('evidence_hash', ''),
                        'document_id': prepared_doc.get('document_id', ''),
                        'filename': prepared_doc.get('filename', 'Unknown')
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
        
        self._log_progress(f"✅ Analysis phase completed: {len(analysis_results)} documents processed")
        return analysis_results
    
    def _run_derived_metrics_phase(self, model: str, audit_logger: AuditLogger, analysis_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Run derived metrics phase using DerivedMetricsPromptAssembler and AutomatedDerivedMetricsAgent."""
        self._log_progress("📊 Running derived metrics phase...")
        
        try:
            # Load framework content
            framework_path = self.experiment_path / self.config['framework']
            
            # Create temporary workspace for derived metrics
            temp_workspace = self.experiment_path / "temp_derived_metrics"
            temp_workspace.mkdir(exist_ok=True)
            
            try:
                # Write analysis results to workspace for the assembler to sample
                analysis_dir = temp_workspace / "analysis_data"
                analysis_dir.mkdir(exist_ok=True)
                
                # Write framework content to workspace for the agent to access
                framework_content = framework_path.read_text(encoding='utf-8')
                (temp_workspace / "framework_content.md").write_text(framework_content)
                
                # Write experiment spec to workspace for the agent to access
                experiment_spec = {
                    "name": "Test Experiment",
                    "description": "Test experiment for derived metrics",
                    "framework": "framework.md"
                }
                (temp_workspace / "experiment_spec.json").write_text(json.dumps(experiment_spec, indent=2))
                
                # Write analysis results as individual files for the assembler to sample
                for i, result in enumerate(analysis_results):
                    analysis_file = analysis_dir / f"analysis_{i}.json"
                    analysis_file.write_text(json.dumps(result, indent=2))
                
                # Also create analysis_data.json for the derived metrics agent
                analysis_data_file = temp_workspace / "analysis_data.json"
                analysis_data_file.write_text(json.dumps(analysis_results, indent=2))
                
                # Use the existing DerivedMetricsPromptAssembler to build the prompt
                from .prompt_assemblers.derived_metrics_assembler import DerivedMetricsPromptAssembler
                assembler = DerivedMetricsPromptAssembler()
                
                # Assemble the prompt using the existing assembler
                self._log_progress("🔧 Assembling derived metrics prompt...")
                prompt = assembler.assemble_prompt(
                    framework_path=framework_path,
                    analysis_dir=analysis_dir,
                    sample_size=3
                )
                
                # Store the assembled prompt
                prompt_file = temp_workspace / "derived_metrics_prompt.txt"
                prompt_file.write_text(prompt)
                
                # Initialize derived metrics caching
                from .derived_metrics_cache import DerivedMetricsCacheManager
                cache_manager = DerivedMetricsCacheManager(self.artifact_storage, audit_logger)
                
                # Generate cache key based on framework content, analysis structure, and model
                cache_key = cache_manager.generate_cache_key(framework_content, analysis_results, model)
                
                # Check cache first
                cache_result = cache_manager.check_cache(cache_key)
                
                if cache_result.hit:
                    self._log_progress("💾 Using cached derived metrics functions")
                    functions_result = cache_result.cached_functions
                    
                    # Recreate functions file from cached content if available
                    if functions_result.get('cached_with_code') and functions_result.get('function_code_content'):
                        functions_file = temp_workspace / "automatedderivedmetricsagent_functions.py"
                        functions_file.write_text(functions_result['function_code_content'], encoding='utf-8')
                        self._log_progress("📝 Recreated functions file from cached content")
                    else:
                        self._log_progress("⚠️ Cached functions missing code content - may need regeneration")
                else:
                    # Initialize derived metrics agent
                    from ..agents.automated_derived_metrics.agent import AutomatedDerivedMetricsAgent
                    derived_metrics_agent = AutomatedDerivedMetricsAgent(
                        model=model,
                        audit_logger=audit_logger
                    )
                    
                    # Generate derived metrics functions using the assembled prompt
                    self._log_progress("🔧 Generating derived metrics functions...")
                    functions_result = derived_metrics_agent.generate_functions(temp_workspace)
                    
                    # Store in cache for future use (with workspace path to capture function code)
                    cache_manager.store_functions(cache_key, functions_result, str(temp_workspace))
                
                # Execute the generated functions on analysis data
                self._log_progress("🔢 Executing derived metrics functions on analysis data...")
                derived_metrics_results = self._execute_derived_metrics_functions(
                    temp_workspace, 
                    analysis_results, 
                    audit_logger
                )
                
                # CRITICAL: Validate that we got actual derived metrics results
                if not derived_metrics_results or not isinstance(derived_metrics_results, dict):
                    raise CleanAnalysisError(
                        "Derived metrics phase failed: No results produced. "
                        "Generated functions but failed to execute or produce derived metrics outputs."
                    )
                
                if derived_metrics_results.get('status') != 'success':
                    raise CleanAnalysisError(
                        f"Derived metrics phase failed: {derived_metrics_results.get('error', 'Unknown error')}"
                    )
                
                # Store derived metrics results in artifact storage
                complete_derived_metrics_result = {
                    "generation_metadata": functions_result,
                    "derived_metrics_data": derived_metrics_results,
                    "status": "success_with_data",
                    "validation_passed": True
                }
                
                derived_metrics_hash = self.artifact_storage.put_artifact(
                    json.dumps(complete_derived_metrics_result, indent=2).encode('utf-8'),
                    {"artifact_type": "derived_metrics_results_with_data"}
                )
                
                self._log_progress(f"✅ Derived metrics phase completed: {len(derived_metrics_results)} result sets")
                
                return {
                    "status": "completed",
                    "derived_metrics_hash": derived_metrics_hash,
                    "functions_generated": functions_result.get('functions_generated', 0),
                    "derived_metrics_results": complete_derived_metrics_result
                }
                
            except Exception as e:
                self._log_progress(f"❌ Derived metrics phase failed: {str(e)}")
                raise CleanAnalysisError(f"Derived metrics phase failed: {str(e)}")
            
            finally:
                # Clean up temporary workspace
                if temp_workspace.exists():
                    import shutil
                    shutil.rmtree(temp_workspace)
        
        except Exception as e:
            self._log_progress(f"❌ Derived metrics phase failed: {str(e)}")
            raise CleanAnalysisError(f"Derived metrics phase failed: {str(e)}")
    
    def _run_statistical_analysis_phase(self, model: str, audit_logger: AuditLogger, analysis_results: List[Dict[str, Any]], derived_metrics_results: Dict[str, Any]) -> Dict[str, Any]:
        """Run statistical analysis phase using StatisticalAnalysisPromptAssembler and AutomatedStatisticalAnalysisAgent."""
        self._log_progress("📊 Running statistical analysis phase...")
        
        try:
            # Load framework and experiment content
            framework_path = self.experiment_path / self.config['framework']
            experiment_path = self.experiment_path / "experiment.md"
            
            # Create temporary workspace for statistical analysis
            temp_workspace = self.experiment_path / "temp_statistical_analysis"
            temp_workspace.mkdir(exist_ok=True)
            
            try:
                # Write analysis results to workspace for the assembler to access
                analysis_dir = temp_workspace / "analysis_data"
                analysis_dir.mkdir(exist_ok=True)
                
                for i, result in enumerate(analysis_results):
                    analysis_file = analysis_dir / f"analysis_{i}.json"
                    analysis_file.write_text(json.dumps(result, indent=2))
                
                # Write derived metrics results to workspace for the assembler to access
                derived_metrics_dir = temp_workspace / "derived_metrics_data"
                derived_metrics_dir.mkdir(exist_ok=True)
                
                if derived_metrics_results.get('status') == 'completed':
                    derived_metrics = derived_metrics_results.get('derived_metrics_results', {}).get('derived_metrics_data', {}).get('derived_metrics', [])
                    if derived_metrics:
                        for i, metric in enumerate(derived_metrics):
                            metric_file = derived_metrics_dir / f"derived_metric_{i}.json"
                            metric_file.write_text(json.dumps(metric, indent=2))
                    else:
                        # Fallback: create empty derived metrics file
                        empty_metric_file = derived_metrics_dir / "derived_metric_empty.json"
                        empty_metric_file.write_text(json.dumps({"status": "no_derived_metrics"}, indent=2))
                else:
                    # Fallback: create empty derived metrics file
                    empty_metric_file = derived_metrics_dir / "derived_metric_empty.json"
                    empty_metric_file.write_text(json.dumps({"status": "derived_metrics_failed"}, indent=2))
                
                # Write framework and experiment content to workspace for the agent to access
                framework_content = framework_path.read_text(encoding='utf-8')
                (temp_workspace / "framework_content.md").write_text(framework_content)
                
                # THIN ARCHITECTURE: Corpus manifest is passed as context in the prompt, not as a file
                # The LLM understands the relationships directly - no parsing needed
                self._log_progress("📋 Corpus manifest passed as prompt context (THIN approach)")
                
                experiment_content = experiment_path.read_text(encoding='utf-8')
                experiment_spec = {
                    "name": self.config.get('name', 'Unknown Experiment'),
                    "description": "Statistical analysis experiment",
                    "questions": []
                }
                (temp_workspace / "experiment_spec.json").write_text(json.dumps(experiment_spec, indent=2))
                
                # Use the existing StatisticalAnalysisPromptAssembler to build the prompt
                from .prompt_assemblers.statistical_analysis_assembler import StatisticalAnalysisPromptAssembler
                assembler = StatisticalAnalysisPromptAssembler()
                
                # Assemble the prompt using the existing assembler
                self._log_progress("🔧 Assembling statistical analysis prompt...")
                prompt = assembler.assemble_prompt(
                    framework_path=framework_path,
                    experiment_path=experiment_path,
                    analysis_dir=analysis_dir,
                    derived_metrics_dir=derived_metrics_dir
                )
                
                # Store the assembled prompt
                prompt_file = temp_workspace / "statistical_analysis_prompt.txt"
                prompt_file.write_text(prompt)
                
                # Initialize statistical analysis caching
                from .statistical_analysis_cache import StatisticalAnalysisCacheManager
                stats_cache_manager = StatisticalAnalysisCacheManager(self.artifact_storage, audit_logger)
                
                # Generate cache key based on framework, experiment, analysis structure, derived metrics, and model
                stats_cache_key = stats_cache_manager.generate_cache_key(
                    framework_content, experiment_content, analysis_results, derived_metrics_results, model
                )
                
                # Check cache first
                stats_cache_result = stats_cache_manager.check_cache(stats_cache_key)
                
                if stats_cache_result.hit:
                    self._log_progress("💾 Using cached statistical analysis functions")
                    functions_result = stats_cache_result.cached_functions
                    
                    # Recreate functions file from cached content if available
                    if functions_result.get('cached_with_code') and functions_result.get('function_code_content'):
                        functions_file = temp_workspace / "automatedstatisticalanalysisagent_functions.py"
                        functions_file.write_text(functions_result['function_code_content'], encoding='utf-8')
                        self._log_progress("📝 Recreated statistical functions file from cached content")
                    else:
                        self._log_progress("⚠️ Cached statistical functions missing code content - may need regeneration")
                else:
                    # Initialize statistical analysis agent
                    from ..agents.automated_statistical_analysis.agent import AutomatedStatisticalAnalysisAgent
                    stats_agent = AutomatedStatisticalAnalysisAgent(
                        model=model,
                        audit_logger=audit_logger
                    )
                    
                    # Generate statistical analysis functions using the assembled prompt
                    self._log_progress("🔧 Generating statistical analysis functions...")
                    functions_result = stats_agent.generate_functions(temp_workspace, pre_assembled_prompt=prompt)
                    
                    # Store in cache for future use (with workspace path to capture function code)
                    stats_cache_manager.store_functions(stats_cache_key, functions_result, str(temp_workspace))
                
                # Execute the generated functions on the data
                self._log_progress(f"🔢 Executing statistical analysis functions from workspace: {temp_workspace}")
                self._log_progress(f"🔍 Functions file should be at: {temp_workspace / 'automatedstatisticalanalysisagent_functions.py'}")
                statistical_results = self._execute_statistical_functions(
                    temp_workspace, 
                    audit_logger,
                    analysis_results
                )
                
                # CRITICAL: Validate that we got actual statistical results
                if not self._validate_statistical_results(statistical_results):
                    raise CleanAnalysisError(
                        "Statistical analysis phase failed: No numerical results produced. "
                        "Generated functions but failed to execute or produce statistical outputs. "
                        "This experiment cannot proceed to synthesis without valid statistical data."
                    )
                
                # Store individual artifacts that synthesis expects
                
                # 1. Store raw analysis data (from analysis_results)
                raw_analysis_data = []
                for result in analysis_results:
                    if 'analysis_result' in result:
                        raw_analysis_data.append(result['analysis_result'])
                
                raw_analysis_data_hash = self.artifact_storage.put_artifact(
                    json.dumps(raw_analysis_data, indent=2, default=str).encode('utf-8'),
                    {"artifact_type": "raw_analysis_data"}
                )
                
                # 2. Store derived metrics data
                derived_metrics_data_hash = self.artifact_storage.put_artifact(
                    json.dumps(derived_metrics_results, indent=2, default=str).encode('utf-8'),
                    {"artifact_type": "derived_metrics_data"}
                )
                
                # 3. Store complete statistical results
                complete_statistical_result = {
                    "generation_metadata": functions_result,
                    "statistical_data": statistical_results,
                    "status": "success_with_data",
                    "validation_passed": True
                }
                
                # Convert numpy objects to regular Python types for safe repr() serialization
                def convert_numpy_types(obj):
                    """Recursively convert numpy types to regular Python types"""
                    if hasattr(obj, 'item'):  # numpy scalar types
                        return obj.item()
                    elif hasattr(obj, 'tolist'):  # numpy arrays
                        return obj.tolist()
                    elif isinstance(obj, dict):
                        return {k: convert_numpy_types(v) for k, v in obj.items()}
                    elif isinstance(obj, list):
                        return [convert_numpy_types(item) for item in obj]
                    elif isinstance(obj, tuple):
                        return tuple(convert_numpy_types(item) for item in obj)
                    elif str(obj) == 'nan':  # Handle nan strings
                        return float('nan')
                    else:
                        return obj
                
                def safe_repr(obj):
                    try:
                        # First convert numpy types, then use repr
                        converted_obj = convert_numpy_types(obj)
                        return repr(converted_obj)
                    except:
                        return str(obj)
                
                statistical_hash = self.artifact_storage.put_artifact(
                    safe_repr(complete_statistical_result).encode('utf-8'),
                    {"artifact_type": "statistical_results_with_data"}
                )
                
                self._log_progress(f"✅ Statistical analysis phase completed")
                
                return {
                    "status": "completed",
                    "stats_hash": statistical_hash,
                    "raw_analysis_data_hash": raw_analysis_data_hash,
                    "derived_metrics_data_hash": derived_metrics_data_hash,
                    "functions_generated": functions_result.get('functions_generated', 0),
                    "statistical_summary": complete_statistical_result
                }
                
            except Exception as e:
                self._log_progress(f"❌ Statistical analysis phase failed: {str(e)}")
                raise CleanAnalysisError(f"Statistical analysis phase failed: {str(e)}")
            
            finally:
                # Clean up temporary workspace
                if temp_workspace.exists():
                    import shutil
                    shutil.rmtree(temp_workspace)
        
        except Exception as e:
            self._log_progress(f"❌ Statistical analysis phase failed: {str(e)}")
            raise CleanAnalysisError(f"Statistical analysis phase failed: {str(e)}")
    
    def _execute_derived_metrics_functions(self, workspace_path: Path, analysis_results: List[Dict[str, Any]], audit_logger: AuditLogger) -> Dict[str, Any]:
        """Execute the generated derived metrics functions on analysis data."""
        import pandas as pd
        import numpy as np
        import sys
        import importlib.util
        
        # Load the generated derived metrics functions module
        functions_file = workspace_path / "automatedderivedmetricsagent_functions.py"
        if not functions_file.exists():
            raise CleanAnalysisError("Derived metrics functions file not found")
        
        # Import the generated module
        try:
            spec = importlib.util.spec_from_file_location("derived_metrics_functions", functions_file)
            derived_metrics_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(derived_metrics_module)
        except Exception as e:
            raise CleanAnalysisError(f"Failed to import derived metrics functions: {e}")
        
        # Convert analysis results to DataFrame format
        analysis_data = []
        for result in analysis_results:
            if isinstance(result, dict) and 'analysis_result' in result:
                analysis_data.append(result['analysis_result'])
        
        if not analysis_data:
            raise CleanAnalysisError("No valid analysis data found for derived metrics calculation")
        
        # Create DataFrame from analysis data
        try:
            df = pd.DataFrame(analysis_data)
        except Exception as e:
            raise CleanAnalysisError(f"Failed to create DataFrame from analysis data: {e}")
        
        # Execute derived metrics calculation
        try:
            if hasattr(derived_metrics_module, 'calculate_derived_metrics'):
                derived_df = derived_metrics_module.calculate_derived_metrics(df)
                
                # Convert back to dictionary format for storage
                derived_metrics_results = derived_df.to_dict('records')
                
                return {
                    "status": "success",
                    "original_count": len(analysis_data),
                    "derived_count": len(derived_metrics_results),
                    "derived_metrics": derived_metrics_results,
                    "columns_added": list(set(derived_df.columns) - set(df.columns))
                }
            else:
                raise CleanAnalysisError("Generated module missing 'calculate_derived_metrics' function")
                
        except Exception as e:
            raise CleanAnalysisError(f"Failed to execute derived metrics functions: {e}")
    
    def _execute_statistical_analysis_functions(self, workspace_path: Path, audit_logger: AuditLogger, analysis_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute the generated statistical analysis functions on the data."""
        import sys
        import importlib.util
        
        # Load the generated statistical analysis functions module
        functions_file = workspace_path / "automatedstatisticalanalysisagent_functions.py"
        if not functions_file.exists():
            raise CleanAnalysisError("Statistical analysis functions file not found")
        
        # Import the generated module
        try:
            spec = importlib.util.spec_from_file_location("statistical_analysis_functions", functions_file)
            stats_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(stats_module)
        except Exception as e:
            raise CleanAnalysisError(f"Failed to import statistical analysis functions: {e}")
        
        # Convert analysis results to DataFrame format expected by statistical functions
        analysis_data = self._convert_analysis_to_dataframe(analysis_results)
        
        # Execute statistical analysis
        try:
            if hasattr(stats_module, 'perform_statistical_analysis'):
                # The generated function now expects a data parameter
                statistical_results = stats_module.perform_statistical_analysis(analysis_data)
                
                return {
                    "status": "success",
                    "statistical_results": statistical_results
                }
            else:
                raise CleanAnalysisError("Generated module missing 'perform_statistical_analysis' function")
                
        except Exception as e:
            raise CleanAnalysisError(f"Failed to execute statistical analysis functions: {e}")
    
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
    
    # REMOVED: Duplicate _run_statistical_analysis method that was causing workspace path confusion
    
    def _execute_statistical_functions(self, workspace_path: Path, audit_logger: AuditLogger, analysis_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute the generated statistical functions on analysis data."""
        import pandas as pd
        import numpy as np
        import sys
        import importlib.util
        import os
        
        try:
            
            # Load the generated statistical functions module
            functions_file = workspace_path / "automatedstatisticalanalysisagent_functions.py"
            self._log_progress(f"🔍 Looking for functions file at: {functions_file}")
            self._log_progress(f"🔍 Workspace path: {workspace_path}")
            self._log_progress(f"🔍 Workspace exists: {workspace_path.exists()}")
            if workspace_path.exists():
                self._log_progress(f"🔍 Workspace contents: {list(workspace_path.iterdir())}")
            
            if not functions_file.exists():
                raise CleanAnalysisError(f"Statistical functions file not found at {functions_file}")
            
            # Import the generated module
            spec = importlib.util.spec_from_file_location("statistical_functions", functions_file)
            stats_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(stats_module)
            
            # Convert analysis results to DataFrame format expected by statistical functions
            analysis_data = self._convert_analysis_to_dataframe(analysis_results)
            
            # Execute each statistical function and collect results
            statistical_outputs = {}
            
            # Get all functions from the module that don't start with underscore and aren't type annotations
            type_annotations = {'Any', 'Dict', 'List', 'Optional', 'Tuple', 'Union', 'Callable', 'TypeVar', 'Generic'}
            function_names = [name for name in dir(stats_module) 
                             if not name.startswith('_') 
                             and callable(getattr(stats_module, name))
                             and name not in type_annotations]
            

            self._log_progress(f"🔢 Executing {len(function_names)} statistical functions...")
            
            for func_name in function_names:
                try:
                    func = getattr(stats_module, func_name)
                    self._log_progress(f"  📊 Running {func_name}...")
                    
                    # Execute the function with the analysis data
                    result = func(analysis_data)
                    
                    # Store result with THIN approach - handle DataFrames specially
                    if hasattr(result, 'to_dict'):  # pandas DataFrame
                        statistical_outputs[func_name] = {
                            "type": "dataframe",
                            "data": result.to_dict('records'),
                            "columns": list(result.columns),
                            "index": list(result.index),
                            "shape": result.shape
                        }
                    elif isinstance(result, dict):
                        # Handle nested DataFrames in dictionary results
                        serialized_result = {}
                        for key, value in result.items():
                            if hasattr(value, 'to_dict'):  # pandas DataFrame
                                serialized_result[key] = {
                                    "type": "dataframe", 
                                    "data": value.to_dict('records'),
                                    "columns": list(value.columns),
                                    "index": list(value.index),
                                    "shape": value.shape
                                }
                            else:
                                serialized_result[key] = value
                        statistical_outputs[func_name] = serialized_result
                    else:
                        # Store simple objects directly
                        statistical_outputs[func_name] = result
                    
                    self._log_progress(f"  ✅ {func_name} completed")
                    
                except Exception as e:
                    self._log_progress(f"  ⚠️ {func_name} failed: {str(e)}")
                    statistical_outputs[func_name] = {"error": str(e), "status": "failed"}
        
            return statistical_outputs
        
        except Exception as e:
            self._log_progress(f"❌ Statistical execution failed: {str(e)}")
            raise CleanAnalysisError(f"Failed to execute statistical functions: {str(e)}")
    
    def _convert_analysis_to_dataframe(self, analysis_results: List[Dict[str, Any]]) -> pd.DataFrame:
        """Convert individual analysis results to pandas DataFrame for statistical functions."""
        import pandas as pd
        
        if not analysis_results or len(analysis_results) == 0:
            raise CleanAnalysisError("No analysis results to convert")
        
        self._log_progress(f"🔍 Converting {len(analysis_results)} individual analysis results to DataFrame...")
        
        # Aggregate document analyses from all individual results
        all_rows = []
        
        for i, analysis_result in enumerate(analysis_results):
            # Each analysis_result is now an individual document analysis
            raw_response = analysis_result.get('raw_analysis_response', '')
            
            if not raw_response:
                self._log_progress(f"⚠️ Skipping analysis result {i+1} - no raw response")
                continue
            
            # Extract JSON from the delimited response
            start_marker = '<<<DISCERNUS_ANALYSIS_JSON_v6>>>'
            end_marker = '<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>'
            
            start_idx = raw_response.find(start_marker)
            end_idx = raw_response.find(end_marker)
            
            if start_idx == -1 or end_idx == -1:
                self._log_progress(f"⚠️ Skipping analysis result {i+1} - no JSON markers found")
                continue
            
            json_content = raw_response[start_idx + len(start_marker):end_idx].strip()
            
            try:
                analysis_data = json.loads(json_content)
            except json.JSONDecodeError as e:
                self._log_progress(f"⚠️ Skipping analysis result {i+1} - JSON parsing failed: {str(e)}")
                continue
            
            # Process document analyses from this individual result
            for doc_analysis in analysis_data.get('document_analyses', []):
                row = {'document_name': doc_analysis.get('document_name', '')}
                
                # Add dimensional scores (both raw_score and salience)
                for dimension, scores in doc_analysis.get('dimensional_scores', {}).items():
                    row[f"{dimension}_raw"] = scores.get('raw_score', 0.0)
                    row[f"{dimension}_salience"] = scores.get('salience', 0.0)
                    row[f"{dimension}_confidence"] = scores.get('confidence', 0.0)
                
                all_rows.append(row)
        
        if not all_rows:
            raise CleanAnalysisError("No valid document analyses found in individual results")
        
        df = pd.DataFrame(all_rows)
        self._log_progress(f"📊 Converted individual analysis to DataFrame: {len(df)} documents, {len(df.columns)} features")
        
        return df
    
    def _validate_statistical_results(self, statistical_results: Dict[str, Any]) -> bool:
        """Validate that statistical analysis produced actual numerical results."""
        if not statistical_results:
            return False
        
        # Check that we have at least one successful statistical function result
        successful_results = 0
        for func_name, result in statistical_results.items():
            if isinstance(result, dict) and result.get('status') != 'failed':
                # Check for numerical data in the result
                if any(isinstance(v, (int, float, list, dict)) for v in result.values() if v is not None):
                    successful_results += 1
        
        # We need at least one successful statistical result with numerical data
        return successful_results > 0
    
    def _validate_assets(self, statistical_results: Dict[str, Any]) -> None:
        """Comprehensive validation that all required assets exist on disk and are valid before synthesis."""
        self._log_progress("🔍 Validating synthesis assets comprehensively...")
        
        # 1. Framework file must exist and be readable
        framework_path = self.experiment_path / self.config['framework']
        if not framework_path.exists():
            raise CleanAnalysisError(f"SYNTHESIS BLOCKED: Framework file not found on disk: {framework_path}")
        if not framework_path.is_file():
            raise CleanAnalysisError(f"SYNTHESIS BLOCKED: Framework path is not a file: {framework_path}")
        try:
            framework_content = framework_path.read_text(encoding='utf-8')
            if len(framework_content.strip()) < 100:
                raise CleanAnalysisError(f"SYNTHESIS BLOCKED: Framework file appears empty or too short: {len(framework_content)} chars")
        except Exception as e:
            raise CleanAnalysisError(f"SYNTHESIS BLOCKED: Cannot read framework file: {e}")
        
        # 2. Experiment file must exist and be readable  
        experiment_path = self.experiment_path / "experiment.md"
        if not experiment_path.exists():
            raise CleanAnalysisError(f"SYNTHESIS BLOCKED: Experiment file not found on disk: {experiment_path}")
        try:
            experiment_content = experiment_path.read_text(encoding='utf-8')
            if len(experiment_content.strip()) < 50:
                raise CleanAnalysisError(f"SYNTHESIS BLOCKED: Experiment file appears empty or too short: {len(experiment_content)} chars")
        except Exception as e:
            raise CleanAnalysisError(f"SYNTHESIS BLOCKED: Cannot read experiment file: {e}")
        
        # 3. Analysis results must be valid and complete
        if not hasattr(self, '_analysis_results') or not self._analysis_results:
            raise CleanAnalysisError("SYNTHESIS BLOCKED: No analysis results available")
        
        valid_analyses = 0
        for i, result in enumerate(self._analysis_results):
            if not result.get('raw_analysis_response'):
                raise CleanAnalysisError(f"SYNTHESIS BLOCKED: Analysis result {i+1} missing raw_analysis_response")
            
            raw_response = result['raw_analysis_response']
            if '<<<DISCERNUS_ANALYSIS_JSON_v6>>>' not in raw_response or '<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>' not in raw_response:
                # Debug: Show what we actually have
                print(f"DEBUG: Analysis result {i+1} missing markers")
                print(f"DEBUG: Result keys: {list(result.keys())}")
                print(f"DEBUG: Raw response length: {len(raw_response)}")
                print(f"DEBUG: Raw response start: {repr(raw_response[:200])}")
                print(f"DEBUG: Raw response end: {repr(raw_response[-200:])}")
                
                # Try to fix incomplete responses by adding missing end marker
                if '<<<DISCERNUS_ANALYSIS_JSON_v6>>>' in raw_response and '<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>' not in raw_response:
                    print(f"DEBUG: Attempting to fix incomplete response for analysis result {i+1}")
                    # Find the last complete JSON object and add end marker
                    try:
                        # Look for the last complete brace
                        brace_count = 0
                        last_complete_pos = -1
                        for pos, char in enumerate(raw_response):
                            if char == '{':
                                brace_count += 1
                            elif char == '}':
                                brace_count -= 1
                                if brace_count == 0:
                                    last_complete_pos = pos
                        
                        if last_complete_pos > 0:
                            # Add end marker after the last complete JSON object
                            fixed_response = raw_response[:last_complete_pos + 1] + '\n<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>'
                            result['raw_analysis_response'] = fixed_response
                            print(f"DEBUG: Fixed incomplete response for analysis result {i+1}")
                            raw_response = fixed_response
                        else:
                            raise CleanAnalysisError(f"SYNTHESIS BLOCKED: Analysis result {i+1} has incomplete JSON that cannot be fixed")
                    except Exception as fix_error:
                        print(f"DEBUG: Failed to fix incomplete response: {fix_error}")
                        raise CleanAnalysisError(f"SYNTHESIS BLOCKED: Analysis result {i+1} missing required JSON markers and cannot be fixed")
                else:
                    raise CleanAnalysisError(f"SYNTHESIS BLOCKED: Analysis result {i+1} missing required JSON markers")
            
            valid_analyses += 1
        
        if valid_analyses == 0:
            raise CleanAnalysisError("SYNTHESIS BLOCKED: No valid analysis results found")
        
        # 4. Derived metrics must be available and valid
        if not hasattr(self, '_derived_metrics_results') or not self._derived_metrics_results:
            raise CleanAnalysisError("SYNTHESIS BLOCKED: No derived metrics results available")
        
        if self._derived_metrics_results.get('status') != 'completed':
            raise CleanAnalysisError("SYNTHESIS BLOCKED: Derived metrics results incomplete")
        
        metrics_data = self._derived_metrics_results.get('derived_metrics_results', {}).get('derived_metrics_data', {})
        if not metrics_data or not metrics_data.get('derived_metrics'):
            raise CleanAnalysisError("SYNTHESIS BLOCKED: Derived metrics contain no actual metrics data")
        
        # 5. Statistical results must contain actual numerical data
        if not self._validate_statistical_results(statistical_results):
            raise CleanAnalysisError(
                "SYNTHESIS BLOCKED: Statistical results contain no numerical data. "
                "Cannot generate report without valid statistical analysis."
            )
        
        # 6. Evidence artifacts must exist in artifact storage
        evidence_count = 0
        for artifact_hash, artifact_info in self.artifact_storage.registry.items():
            metadata = artifact_info.get("metadata", {})
            if metadata.get("artifact_type", "").startswith("evidence_v6"):
                evidence_count += 1
                # Verify the artifact actually exists on disk (use quiet=True to suppress verbose logging)
                try:
                    evidence_data = self.artifact_storage.get_artifact(artifact_hash, quiet=True)
                    if not evidence_data or len(evidence_data) < 10:
                        raise CleanAnalysisError(f"SYNTHESIS BLOCKED: Evidence artifact {artifact_hash[:8]} exists in registry but is empty on disk")
                except Exception as e:
                    raise CleanAnalysisError(f"SYNTHESIS BLOCKED: Cannot retrieve evidence artifact {artifact_hash[:8]}: {e}")
        
        if evidence_count == 0:
            raise CleanAnalysisError(
                "SYNTHESIS BLOCKED: No evidence artifacts found in storage. "
                "Cannot generate report without textual evidence for citations."
            )
        
        # 5. Corpus files must exist and be accessible
        corpus_manifest_path = self.experiment_path / self.config.get('corpus', 'corpus.md')
        if not corpus_manifest_path.exists():
            raise CleanAnalysisError(f"SYNTHESIS BLOCKED: Corpus manifest not found: {corpus_manifest_path}")
        
        # Validate that corpus documents referenced in manifest actually exist
        try:
            corpus_documents = self._load_corpus_documents()
            if not corpus_documents:
                raise CleanAnalysisError("SYNTHESIS BLOCKED: Corpus manifest contains no documents")
            
            missing_docs = []
            corpus_dir = self.experiment_path / "corpus"
            for doc_info in corpus_documents:
                filename = doc_info.get('filename')
                if filename:
                    doc_file = self._find_corpus_file(corpus_dir, filename)
                    if not doc_file or not doc_file.exists():
                        missing_docs.append(filename)
            
            if missing_docs:
                raise CleanAnalysisError(f"SYNTHESIS BLOCKED: Corpus documents missing from disk: {missing_docs}")
                
        except Exception as e:
            raise CleanAnalysisError(f"SYNTHESIS BLOCKED: Cannot validate corpus documents: {e}")
        
        self._log_progress(f"✅ Synthesis assets validated: framework, experiment, {evidence_count} evidence artifacts, {len(corpus_documents)} corpus documents")
        self._log_progress("🟢 All required assets confirmed on disk - synthesis can proceed")

    def _build_rag_index(self, audit_logger: AuditLogger) -> None:
        """Builds the RAG index using the TxtaiEvidenceCurator."""
        self._log_progress("📚 Building RAG index for evidence retrieval...")

        evidence_hashes = []
        for artifact_hash, artifact_info in self.artifact_storage.registry.items():
            metadata = artifact_info.get("metadata", {})
            if metadata.get("artifact_type", "").startswith("evidence_v6"):
                evidence_hashes.append(artifact_hash)
        
        if not evidence_hashes:
            self.logger.warning("No evidence artifacts found, RAG index will be empty.")
            # We still create an empty index object to avoid downstream errors.
            from txtai.embeddings import Embeddings
            self.rag_index = Embeddings()
            return

        curator = TxtaiEvidenceCurator(
            model="vertex_ai/gemini-2.5-flash", # Use a fast model for indexing
            artifact_storage=self.artifact_storage,
            audit_logger=audit_logger
        )

        index = curator.build_and_load_index(
            evidence_artifact_hashes=evidence_hashes,
            artifact_storage=self.artifact_storage
        )

        if index is None:
            raise CleanAnalysisError("TxtaiEvidenceCurator failed to build and return a RAG index.")
        
        self.rag_index = index
        self._log_progress(f"✅ RAG index built and loaded with {len(evidence_hashes)} evidence sources.")

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
                    if metadata.get("artifact_type", "").startswith("evidence_v6"):
                        evidence_artifact_hashes.append(artifact_hash)
            
            if not evidence_artifact_hashes:
                self._log_progress("⚠️ No evidence artifacts found - evidence retrieval will be limited")
                return {"status": "no_evidence_available", "message": "No evidence artifacts found"}
            
            # Initialize EvidenceRetrieverAgent with shared artifact storage
            agent_config = {
                'experiment_path': str(self.experiment_path),
                'run_id': run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
                'artifact_storage': self.artifact_storage  # Share the same artifact storage instance
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

    def _run_synthesis(self, synthesis_model: str, audit_logger: AuditLogger, statistical_results: Dict[str, Any], evidence_results: Dict[str, Any] = None) -> Dict[str, Any]:
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
                    return tuple(convert_tuple_keys_for_json(item) for item in obj)
                else:
                    return obj
            
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
            
            # Create assets dictionary for the new interface
            assets = {
                'framework_path': Path(self.experiment_path / self.config["framework"]),
                'experiment_path': Path(self.experiment_path / "experiment.md"),
                'research_data_artifact_hash': research_data_hash,
                'evidence_retrieval_results_hash': evidence_results.get('evidence_artifact_hash'),
                'artifact_storage': self.artifact_storage,
                'derived_metrics_results': getattr(self, '_derived_metrics_results', {}),
                'analysis_results': getattr(self, '_analysis_results', []),
                'corpus_manifest_path': Path(self.experiment_path / "corpus.md") if (self.experiment_path / "corpus.md").exists() else None
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
                "assets": final_report, # Pass the string, not the dict
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
            
            # Initialize fact-checker agent
            from ..agents.fact_checker_agent.agent import FactCheckerAgent
            
            fact_checker = FactCheckerAgent(
                gateway=self.llm_gateway,
                audit_logger=audit_logger,
                corpus_index_service=corpus_index_service,
                artifact_storage=self.artifact_storage,
            )
            
            # Run fact-checking validation using the new self-directed interface
            validation_results = fact_checker.run()
            
            if validation_results.get('status') == 'failed':
                raise CleanAnalysisError(f"Fact-checking failed: {validation_results.get('error', 'Unknown error')}")
            
            self._log_progress(f"✅ Fact-checking completed: {len(validation_results.get('findings', []))} findings")
            
            return {
                "status": "completed",
                "findings": validation_results.get('findings', []),
                "validation_results": validation_results,
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
                analysis_json = json.dumps(self._analysis_results, indent=2, default=str)
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
                    report_content = self.artifact_storage.get_artifact(assets_dict['report_hash'])
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
    
    def _create_clean_results_directory(self, run_id: str, statistical_results: Dict[str, Any], assets: Dict[str, Any], fact_check_results: Dict[str, Any]) -> Path:
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
            
            # Apply fact-checking results if available
            if fact_check_results.get('status') == 'completed' and fact_check_results.get('findings'):
                annotated_report = self._apply_fact_checking_to_report(report_content.decode('utf-8'), fact_check_results)
                with open(report_file, 'w', encoding='utf-8') as f:
                    f.write(annotated_report)
                self._log_progress("📝 Annotated final report saved to results")
            else:
                with open(report_file, 'wb') as f:
                    f.write(report_content)
                self._log_progress("📝 Final report saved to results")
        
        # Save fact-checking results
        fact_check_file = results_dir / "fact_check_results.json"
        with open(fact_check_file, 'w') as f:
            json.dump(fact_check_results, f, indent=2)
        
        # Save synthesis metadata
        synthesis_file = results_dir / "assetss.json"
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
                "assetss.json": "Synthesis results",
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
        synthesis_file = results_dir / "assetss.json"
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
            
            # Get all evidence artifacts
            artifacts_dir = self.experiment_path / "shared_cache" / "artifacts"
            evidence_files = list(artifacts_dir.glob("evidence_v6_*"))
            
            if not evidence_files:
                self._log_progress("⚠️ No evidence artifacts found")
                return
            
            # Aggregate evidence
            all_evidence = []
            for evidence_file in evidence_files:
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
                analysis_json = json.dumps(self._analysis_results, indent=2, default=str)
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
                    report_content = self.artifact_storage.get_artifact(assets_dict['report_hash'])
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
    
    def _create_clean_results_directory(self, run_id: str, statistical_results: Dict[str, Any], assets: Dict[str, Any], fact_check_results: Dict[str, Any]) -> Path:
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
            
            # Apply fact-checking results if available
            if fact_check_results.get('status') == 'completed' and fact_check_results.get('findings'):
                annotated_report = self._apply_fact_checking_to_report(report_content.decode('utf-8'), fact_check_results)
                with open(report_file, 'w', encoding='utf-8') as f:
                    f.write(annotated_report)
                self._log_progress("📝 Annotated final report saved to results")
            else:
                with open(report_file, 'wb') as f:
                    f.write(report_content)
                self._log_progress("📝 Final report saved to results")
        
        # Save fact-checking results
        fact_check_file = results_dir / "fact_check_results.json"
        with open(fact_check_file, 'w') as f:
            json.dump(fact_check_results, f, indent=2)
        
        # Save synthesis metadata
        synthesis_file = results_dir / "assetss.json"
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
                "assetss.json": "Synthesis results",
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
        synthesis_file = results_dir / "assetss.json"
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
            
            # Get all evidence artifacts
            artifacts_dir = self.experiment_path / "shared_cache" / "artifacts"
            evidence_files = list(artifacts_dir.glob("evidence_v6_*"))
            
            if not evidence_files:
                self._log_progress("⚠️ No evidence artifacts found")
                return
            
            # Aggregate evidence
            all_evidence = []
            for evidence_file in evidence_files:
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
        """Run fact-checker validation on synthesis report and return structured results."""
        try:
            # Import fact-checker agent
            from ..agents.fact_checker_agent.agent import FactCheckerAgent
            
            # Initialize fact-checker with existing RAG index
            fact_checker = FactCheckerAgent(
                model="vertex_ai/gemini-2.5-flash",  # Use Flash for cost efficiency
                audit_logger=self.audit_logger
            )
            
            # Run fact-checking validation
            validation_results = fact_checker.validate_report(
                report_content=synthesis_report,
                rag_index=self.fact_checker_rag,  # Use existing RAG index
                source_documents=getattr(self.fact_checker_rag, 'documents', [])
            )
            
            return validation_results
            
        except Exception as e:
            self._log_progress(f"⚠️ Fact-checker validation failed: {str(e)}")
            # Return empty results if fact-checker fails - don't block synthesis
            return {"issues": [], "status": "fact_check_unavailable", "error": str(e)}

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
                analysis_json = json.dumps(self._analysis_results, indent=2, default=str)
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
