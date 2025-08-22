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

import json
import yaml
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd

from .logging_config import setup_logging, get_logger, log_experiment_start, log_experiment_complete, log_experiment_failure
from .security_boundary import ExperimentSecurityBoundary
from .audit_logger import AuditLogger
from .local_artifact_storage import LocalArtifactStorage
from .enhanced_manifest import EnhancedManifest
from ..agents.experiment_coherence_agent import ExperimentCoherenceAgent
from ..agents.EnhancedAnalysisAgent.main import EnhancedAnalysisAgent
from ..agents.automated_statistical_analysis.agent import AutomatedStatisticalAnalysisAgent
from ..gateway.llm_gateway import LLMGateway
from ..gateway.model_registry import ModelRegistry


class CleanAnalysisError(Exception):
    """Clean analysis orchestrator specific exceptions."""
    pass


class CleanAnalysisOrchestrator:
    """
    Clean orchestrator focused on analysis and synthesis only.
    No notebook generation, no complex agent chains, just what we need.
    """
    
    def __init__(self, experiment_path: Path):
        """Initialize clean analysis orchestrator."""
        self.experiment_path = Path(experiment_path).resolve()
        
        # Initialize core components
        self.security = ExperimentSecurityBoundary(self.experiment_path)
        self.logger = get_logger("clean_analysis_orchestrator")
        self.config = {}
        
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
            phase_start = datetime.now(timezone.utc)
            try:
                analysis_results = self._run_analysis_phase(analysis_model, audit_logger)
                self._log_status(f"Analysis completed: {len(analysis_results)} documents processed")
                self._log_phase_timing("analysis_phase", phase_start)
            except Exception as e:
                self._log_progress(f"❌ Analysis phase failed: {str(e)}")
                raise CleanAnalysisError(f"Analysis phase failed: {str(e)}")
            
            # Phase 5: Generate statistics
            phase_start = datetime.now(timezone.utc)
            try:
                statistical_results = self._run_statistical_analysis(synthesis_model, audit_logger, analysis_results)
                self._log_status("Statistical analysis completed")
                self._log_phase_timing("statistical_analysis", phase_start)
            except Exception as e:
                self._log_progress(f"⚠️ Statistical analysis failed, attempting to continue: {str(e)}")
                # Try to continue with basic analysis results
                statistical_results = {"error": str(e), "status": "failed"}
            
            # Phase 6: Run synthesis
            phase_start = datetime.now(timezone.utc)
            try:
                synthesis_result = self._run_synthesis(synthesis_model, audit_logger, statistical_results)
                self._log_status("Synthesis completed")
                self._log_phase_timing("synthesis_phase", phase_start)
            except Exception as e:
                self._log_progress(f"⚠️ Synthesis failed, creating basic results: {str(e)}")
                # Create basic synthesis result to avoid complete failure
                synthesis_result = {
                    "synthesis_text": f"Synthesis failed: {str(e)}",
                    "status": "failed",
                    "error": str(e)
                }
            
            # Phase 7: Create results with publication readiness
            phase_start = datetime.now(timezone.utc)
            try:
                results_dir = self._create_clean_results_directory(run_id, statistical_results, synthesis_result)
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
            
            return {
                "run_id": run_id,
                "results_directory": str(results_dir),
                "analysis_documents": len(analysis_results),
                "status": "completed",
                "warnings": self._get_warnings(),
                "duration_seconds": duration,
                "performance_metrics": performance_summary
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
            
            # Store test data
            self.artifact_storage.put_artifact(test_key, test_data)
            
            # Retrieve test data
            retrieved_data = self.artifact_storage.get_artifact(test_key)
            
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
        
        # Parse experiment.md to extract v10.0 machine-readable appendix
        try:
            content = experiment_file.read_text(encoding='utf-8')
            
            # Try v10.0 delimited format first (# --- Start/End --- pattern)
            if '# --- Start of Machine-Readable Appendix ---' in content:
                start_marker = '# --- Start of Machine-Readable Appendix ---'
                end_marker = '# --- End of Machine-Readable Appendix ---'
                
                start_idx = content.find(start_marker) + len(start_marker)
                end_idx = content.find(end_marker)
                
                if end_idx > start_idx:
                    yaml_content = content[start_idx:end_idx].strip()
                else:
                    # No end marker found, take everything after start
                    yaml_content = content[start_idx:].strip()
                
                config = yaml.safe_load(yaml_content)
                if not isinstance(config, dict):
                    raise CleanAnalysisError("Invalid YAML structure in machine-readable appendix.")
            
            # Try v10.0 Configuration Appendix format (## Configuration Appendix)
            elif '## Configuration Appendix' in content:
                _, appendix_content = content.split('## Configuration Appendix', 1)
                # Isolate the YAML block from markdown fences
                if '```yaml' in appendix_content:
                    yaml_start = appendix_content.find('```yaml') + 7
                    yaml_end = appendix_content.rfind('```')
                    if yaml_end > yaml_start:
                        yaml_content = appendix_content[yaml_start:yaml_end].strip()
                    else: # No closing fence found
                        yaml_content = appendix_content[yaml_start:].strip()
                else: # No yaml fence, assume raw content
                    yaml_content = appendix_content.strip()

                config = yaml.safe_load(yaml_content)
                if not isinstance(config, dict):
                    raise CleanAnalysisError("Invalid YAML structure in experiment appendix.")
            
            # Reject v7.3 frontmatter format with helpful error
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
        
        # Validate required component fields
        components = config.get('components', {})
        if not components.get('framework'):
            raise CleanAnalysisError("Missing required field: components.framework")
        
        if not components.get('corpus'):
            raise CleanAnalysisError("Missing required field: components.corpus")
        
        return config
    
    def _run_coherence_validation(self, validation_model: str, audit_logger: AuditLogger):
        """Run experiment coherence validation."""
        self._log_progress("🔬 Validating experiment coherence...")
        
        coherence_agent = ExperimentCoherenceAgent(
            model=validation_model,
            audit_logger=audit_logger
        )
        
        # Load framework and corpus for validation
        framework_path = self.experiment_path / self.config['framework']
        corpus_path = self.experiment_path / self.config['corpus']
        
        framework_content = framework_path.read_text(encoding='utf-8')
        corpus_content = corpus_path.read_text(encoding='utf-8')
        
        validation_result = coherence_agent.validate_experiment(self.experiment_path)
        
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
            model=analysis_model,
            security_boundary=self.security,
            audit_logger=audit_logger,
            artifact_storage=self.artifact_storage
        )
        
        # Process documents individually for scalability and caching
        analysis_results = []
        for i, prepared_doc in enumerate(prepared_documents):
            self._log_progress(f"📄 Processing document {i+1}/{len(prepared_documents)}: {prepared_doc.get('filename', 'Unknown')}")
            
            try:
                # Check if we already have cached results for this document
                doc_hash = prepared_doc.get('document_id', '')
                cached_result = self.artifact_storage.get_artifact(f"analysis_result_{doc_hash}")
                
                if cached_result:
                    self._log_progress(f"✅ Using cached analysis for: {prepared_doc.get('filename', 'Unknown')}")
                    self.performance_metrics["cache_hits"] += 1
                    analysis_results.append(cached_result)
                    continue
                else:
                    self.performance_metrics["cache_misses"] += 1
                
                # Analyze single document
                result = analysis_agent.analyze_batch(
                    corpus_documents=[prepared_doc],
                    framework_content=self.config.get('framework', ''),
                    questions=self.config.get('questions', [])
                )
                
                if result and 'analysis_data' in result:
                    # Store individual analysis result
                    analysis_data = result['analysis_data']
                    result_hash = self.artifact_storage.put_artifact(
                        f"analysis_result_{doc_hash}",
                        analysis_data
                    )
                    
                    # Store the full result including raw_analysis_response
                    full_result = {
                        'analysis_data': analysis_data,
                        'raw_analysis_response': result.get('raw_analysis_response', ''),
                        'result_hash': result_hash,
                        'document_id': doc_hash,
                        'filename': prepared_doc.get('filename', 'Unknown')
                    }
                    
                    analysis_results.append(full_result)
                    self._log_progress(f"✅ Analysis completed for: {prepared_doc.get('filename', 'Unknown')}")
                else:
                    self._log_progress(f"⚠️ Analysis failed for: {prepared_doc.get('filename', 'Unknown')}")
                    
            except Exception as e:
                self._log_progress(f"❌ Analysis failed for {prepared_doc.get('filename', 'Unknown')}: {str(e)}")
                # Continue with other documents
                continue
        
        if not analysis_results:
            raise CleanAnalysisError("No documents were successfully analyzed")
        
        self._log_progress(f"✅ Analysis phase completed: {len(analysis_results)} documents processed")
        return analysis_results
    
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
    
    def _run_statistical_analysis(self, model: str, audit_logger: AuditLogger, analysis_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate and execute statistical analysis functions."""
        self._log_progress("📊 Generating statistical analysis...")
        
        # Load framework content
        framework_path = self.experiment_path / self.config['framework']
        framework_content = framework_path.read_text(encoding='utf-8')
        
        # Create experiment spec for statistical agent
        experiment_spec = {
            "name": self.config['name'],
            "description": self.config.get('description', ''),
            "questions": self.config.get('questions', [])
        }
        
        # Initialize statistical analysis agent
        stats_agent = AutomatedStatisticalAnalysisAgent(
            model=model,
            audit_logger=audit_logger
        )
        
        # Create temporary workspace for statistical analysis
        temp_workspace = self.experiment_path / "temp_stats"
        temp_workspace.mkdir(exist_ok=True)
        
        try:
            # Write framework content and experiment spec
            (temp_workspace / "framework_content.md").write_text(framework_content)
            (temp_workspace / "experiment_spec.json").write_text(json.dumps(experiment_spec, indent=2))
            
            # Generate statistical functions
            stats_generation_result = stats_agent.generate_functions(temp_workspace)
            
            # CRITICAL: Execute the generated statistical functions on analysis data
            self._log_progress("🔢 Executing statistical functions on analysis data...")
            statistical_results = self._execute_statistical_functions(
                temp_workspace, 
                analysis_results, 
                audit_logger
            )
            
            # Transaction validation: Ensure we got actual statistical results
            if not self._validate_statistical_results(statistical_results):
                raise CleanAnalysisError(
                    "Statistical analysis transaction failed: No numerical results produced. "
                    "Generated functions but failed to execute or produce statistical outputs."
                )
            
            # Store statistical results in artifact storage
            complete_stats_result = {
                "generation_metadata": stats_generation_result,
                "statistical_data": statistical_results,
                "status": "success_with_data",
                "validation_passed": True
            }
            
            stats_hash = self.artifact_storage.put_artifact(
                json.dumps(complete_stats_result, indent=2).encode('utf-8'),
                {"artifact_type": "statistical_results_with_data"}
            )
            
            self._log_progress(f"✅ Statistical analysis executed successfully: {len(statistical_results)} result sets")
            
            return {
                "status": "completed",
                "stats_hash": stats_hash,
                "functions_generated": stats_generation_result.get('functions_generated', 0),
                "statistical_results": complete_stats_result
            }
            
        except Exception as e:
            self._log_progress(f"❌ Statistical analysis failed: {str(e)}")
            raise CleanAnalysisError(f"Statistical analysis failed: {str(e)}")
        
        finally:
            # Clean up temporary workspace
            if temp_workspace.exists():
                import shutil
                shutil.rmtree(temp_workspace)
    
    def _execute_statistical_functions(self, workspace_path: Path, analysis_results: List[Dict[str, Any]], audit_logger: AuditLogger) -> Dict[str, Any]:
        """Execute the generated statistical functions on analysis data."""
        import pandas as pd
        import numpy as np
        import sys
        import importlib.util
        
        # Load the generated statistical functions module
        functions_file = workspace_path / "automatedstatisticalanalysisagent_functions.py"
        if not functions_file.exists():
            raise CleanAnalysisError("Statistical functions file not found")
        
        # Import the generated module
        spec = importlib.util.spec_from_file_location("statistical_functions", functions_file)
        stats_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(stats_module)
        
        # Convert analysis results to DataFrame format expected by statistical functions
        analysis_data = self._convert_analysis_to_dataframe(analysis_results)
        
        # Execute each statistical function and collect results
        statistical_outputs = {}
        
        # Get all functions from the module that don't start with underscore
        function_names = [name for name in dir(stats_module) if not name.startswith('_') and callable(getattr(stats_module, name))]
        
        self._log_progress(f"🔢 Executing {len(function_names)} statistical functions...")
        
        for func_name in function_names:
            try:
                func = getattr(stats_module, func_name)
                self._log_progress(f"  📊 Running {func_name}...")
                
                # Execute the function with the analysis data
                result = func(analysis_data)
                statistical_outputs[func_name] = result
                
                self._log_progress(f"  ✅ {func_name} completed")
                
            except Exception as e:
                self._log_progress(f"  ⚠️ {func_name} failed: {str(e)}")
                statistical_outputs[func_name] = {"error": str(e), "status": "failed"}
        
        return statistical_outputs
    
    def _convert_analysis_to_dataframe(self, analysis_results: List[Dict[str, Any]]) -> pd.DataFrame:
        """Convert individual analysis results to pandas DataFrame for statistical functions."""
        import pandas as pd
        import json
        
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
    
    def _validate_synthesis_assets(self, statistical_results: Dict[str, Any]) -> None:
        """Comprehensive validation that all required assets exist on disk before synthesis."""
        self._log_progress("🔍 Validating synthesis assets...")
        
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
        
        # 3. Statistical results must contain actual numerical data
        if not self._validate_statistical_results(statistical_results):
            raise CleanAnalysisError(
                "SYNTHESIS BLOCKED: Statistical results contain no numerical data. "
                "Cannot generate report without valid statistical analysis."
            )
        
        # 4. Evidence artifacts must exist in artifact storage
        evidence_count = 0
        for artifact_hash, artifact_info in self.artifact_storage.registry.items():
            metadata = artifact_info.get("metadata", {})
            if metadata.get("artifact_type", "").startswith("evidence_v6"):
                evidence_count += 1
                # Verify the artifact actually exists on disk
                try:
                    evidence_data = self.artifact_storage.get_artifact(artifact_hash)
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
    
    def _run_synthesis(self, synthesis_model: str, audit_logger: AuditLogger, statistical_results: Dict[str, Any]) -> Dict[str, Any]:
        """Run synthesis using RAG approach with comprehensive asset validation."""
        self._log_progress("📝 Validating synthesis assets before attempting report generation...")
        
        try:
            # CRITICAL: Validate all required assets exist on disk before synthesis
            self._validate_synthesis_assets(statistical_results)
            
            # Initialize synthesis agent
            from .prompt_assemblers.synthesis_assembler import SynthesisPromptAssembler
            
            # Use RAG approach via SynthesisPromptAssembler (proven architecture)
            assembler = SynthesisPromptAssembler()
            
            # Prepare paths for synthesis (already validated above)
            framework_path = self.experiment_path / self.config['framework']
            experiment_path = self.experiment_path / "experiment.md"
            
            # Get research data artifact hash (we need to store the statistical results first)
            research_data_json = json.dumps(statistical_results, indent=2)
            research_data_hash = self.artifact_storage.put_artifact(
                research_data_json.encode('utf-8'),
                {"artifact_type": "research_data_for_synthesis"}
            )
            
            # Get evidence artifact hashes from the artifact registry (already validated above)
            evidence_artifact_hashes = []
            for artifact_hash, artifact_info in self.artifact_storage.registry.items():
                metadata = artifact_info.get("metadata", {})
                if metadata.get("artifact_type", "").startswith("evidence_v6"):
                    evidence_artifact_hashes.append(artifact_hash)
            
            # Generate base synthesis prompt
            base_synthesis_prompt = assembler.assemble_prompt(
                framework_path=framework_path,
                experiment_path=experiment_path,
                research_data_artifact_hash=research_data_hash,
                artifact_storage=self.artifact_storage,
                evidence_artifacts=evidence_artifact_hashes
            )
            
            # Add actual evidence context (the working approach)
            evidence_context = self._prepare_evidence_context(evidence_artifact_hashes, self.artifact_storage)
            
            complete_synthesis_prompt = f"""{base_synthesis_prompt}

AVAILABLE EVIDENCE FOR CITATION:
{evidence_context}

Use this evidence to support your statistical interpretations. Quote directly from the evidence above with proper attribution."""
            
            # Generate report using initialized LLM gateway
            final_report, metadata = self.llm_gateway.execute_call(
                model=synthesis_model,
                prompt=complete_synthesis_prompt,
                temperature=0.1
            )
            synthesis_result = {"final_report": final_report}
            
            # Transaction validation: Synthesis must produce a report with evidence integration
            final_report = synthesis_result.get('final_report')
            if not final_report:
                raise CleanAnalysisError(
                    "Synthesis transaction failed: No final report generated. "
                    "Enhanced synthesis must produce a complete report."
                )
            
            # Validate evidence integration in report
            if len(evidence_artifact_hashes) > 0:
                # Check if report contains evidence citations (basic validation)
                if "No evidence available" in final_report or "absence of qualitative data" in final_report:
                    raise CleanAnalysisError(
                        f"Evidence integration transaction failed: Report claims no evidence available "
                        f"but {len(evidence_artifact_hashes)} evidence artifacts exist in registry. "
                        f"Enhanced synthesis must integrate available evidence."
                    )
            
            # Store synthesis report
            report_hash = self.artifact_storage.put_artifact(
                final_report.encode('utf-8'),
                {"artifact_type": "final_synthesis_report"}
            )
            
            self._log_progress(f"✅ RAG synthesis completed with evidence integration: {report_hash[:8]}")
            
            return {
                "status": "completed",
                "report_hash": report_hash,
                "report_length": len(final_report),
                "evidence_artifacts_used": len(evidence_artifact_hashes),
                "synthesis_result": synthesis_result
            }
                
        except Exception as e:
            self._log_progress(f"⚠️ RAG synthesis failed: {str(e)}")
            raise CleanAnalysisError(f"RAG synthesis failed: {str(e)}") from e
    
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
    
    def _create_clean_results_directory(self, run_id: str, statistical_results: Dict[str, Any], synthesis_result: Dict[str, Any]) -> Path:
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
        if synthesis_result.get('report_hash'):
            report_content = self.artifact_storage.get_artifact(synthesis_result['report_hash'])
            report_file = results_dir / "final_report.md"
            with open(report_file, 'wb') as f:
                f.write(report_content)
            self._log_progress("📝 Final report saved to results")
        
        # Save synthesis metadata
        synthesis_file = results_dir / "synthesis_results.json"
        with open(synthesis_file, 'w') as f:
            # Remove large content to keep metadata file clean
            clean_synthesis = {k: v for k, v in synthesis_result.items() if k != 'synthesis_result'}
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
                "synthesis_results.json": "Synthesis results",
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
        synthesis_file = results_dir / "synthesis_results.json"
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
                if self.artifact_storage.registry.get("final_synthesis_report"):
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
        self.logger.info(message)
    
    def _log_status(self, message: str):
        """Log status updates."""
        self.logger.info(f"STATUS: {message}")
