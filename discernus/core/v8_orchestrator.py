#!/usr/bin/env python3
"""
THIN V8.0 Orchestrator - Clean Architecture
==========================================

A focused 150-line orchestrator for v8.0 experiments that preserves the working
analysis stage and adds clean notebook generation without legacy synthesis complexity.

Architecture:
1. Load v8.0 specs (experiment.md, cff_v8.md, corpus)
2. Run analysis (reuse existing EnhancedAnalysisAgent - our only reliable piece)
3. Run coherence validation (ExperimentCoherenceAgent)
4. Execute v8.0 agents via NotebookGenerationOrchestrator
5. Generate notebook with functions

THIN Principles:
- Reuse working components (analysis stage)
- Direct function calls (no Redis)
- Robust logging and provenance
- Clean separation of concerns
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

from .security_boundary import ExperimentSecurityBoundary
from .audit_logger import AuditLogger
from .local_artifact_storage import LocalArtifactStorage
from .enhanced_manifest import EnhancedManifest
from .logging_config import setup_logging, get_logger, log_experiment_start, log_experiment_complete, log_experiment_failure
from ..agents.EnhancedAnalysisAgent.main import EnhancedAnalysisAgent
from ..agents.experiment_coherence_agent import ExperimentCoherenceAgent
from .notebook_generation_orchestrator import NotebookGenerationOrchestrator
from ..cli_console import DiscernusConsole


class V8OrchestrationError(Exception):
    """V8.0 orchestrator specific exceptions"""
    pass


class V8Orchestrator:
    """
    Clean v8.0 orchestrator focused on notebook generation.
    
    Preserves the working analysis stage and adds clean v8.0 agent execution
    without the complexity of legacy synthesis pipelines.
    """
    
    def __init__(self, experiment_path: Path):
        """Initialize v8.0 orchestrator for an experiment."""
        self.experiment_path = Path(experiment_path).resolve()
        
        # Initialize core infrastructure (reuse existing, working components)
        self.security = ExperimentSecurityBoundary(self.experiment_path)
        self.logger = get_logger("v8_orchestrator")
        self.console = DiscernusConsole()
        
        self.logger.info(f"V8.0 Orchestrator initialized for: {self.security.experiment_name}")
        self._log_progress(f"🎯 V8.0 Orchestrator initialized for: {self.security.experiment_name}")
    
    def _log_progress(self, message: str):
        """Log progress with rich console output."""
        self.logger.info(message)
        self.console.echo(message)
    
    def _log_status(self, message: str):
        """Log status updates."""
        self.logger.info(f"STATUS: {message}")
        self.console.echo(f"✅ {message}")
    
    def run_experiment(self, 
                      analysis_model: str = "vertex_ai/gemini-2.5-flash",
                      synthesis_model: str = "vertex_ai/gemini-2.5-pro",
                      validation_model: str = "vertex_ai/gemini-2.5-pro",
                      skip_validation: bool = False) -> Dict[str, Any]:
        """
        Run complete v8.0 experiment pipeline.
        
        Args:
            analysis_model: LLM model for analysis tasks
            synthesis_model: LLM model for synthesis tasks (used by v8.0 agents)
            validation_model: LLM model for validation tasks
            skip_validation: Skip coherence validation
            
        Returns:
            Experiment results with notebook artifacts
        """
        run_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        start_time = datetime.now(timezone.utc)
        
        try:
            # Initialize infrastructure
            self._log_progress("🔧 Initializing infrastructure...")
            audit_logger = self._initialize_infrastructure(run_id)
            log_experiment_start(self.security.experiment_name, run_id)
            
            self._log_progress("🚀 Starting V8.0 experiment pipeline...")
            
            # Phase 1: Load and validate v8.0 specifications
            self._log_progress("📋 Loading V8.0 specifications...")
            experiment_config = self._load_v8_specs()
            self._log_status("V8.0 specifications loaded")
            
            # Phase 2: Run coherence validation (unless skipped)
            if not skip_validation:
                self._run_coherence_validation(validation_model, audit_logger)
                self._log_status("Experiment coherence validated")
            
            # Phase 3: Run analysis (our reliable working component)
            analysis_results = self._run_analysis_phase(analysis_model, audit_logger)
            successful_analyses = len([r for r in analysis_results if 'error' not in r])
            self._log_status(f"Analysis completed: {successful_analyses}/{len(analysis_results)} documents analyzed successfully")
            
            # Phase 4: Execute v8.0 agents via notebook orchestrator
            notebook_results = self._execute_v8_agents(
                analysis_results, 
                analysis_model, 
                synthesis_model, 
                audit_logger
            )
            self._log_status("V8.0 agents executed successfully")
            
            # Phase 5: Finalize and return results
            results = {
                "run_id": run_id,
                "experiment_name": self.security.experiment_name,
                "analysis_results": analysis_results,
                "notebook_results": notebook_results,
                "status": "completed",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            duration_seconds = (datetime.now(timezone.utc) - start_time).total_seconds()
            log_experiment_complete(self.security.experiment_name, run_id, duration_seconds)
            self._log_progress("✅ V8.0 experiment completed successfully!")
            
            return results
            
        except Exception as e:
            log_experiment_failure(self.security.experiment_name, run_id, str(e), "orchestration")
            self._log_progress(f"❌ V8.0 experiment failed: {str(e)}")
            raise V8OrchestrationError(f"V8.0 experiment failed: {str(e)}") from e
    
    def _initialize_infrastructure(self, run_id: str) -> AuditLogger:
        """Initialize logging and storage infrastructure."""
        try:
            # Setup logging
            self._log_progress("🔧 Setting up logging...")
            run_folder = Path(self.experiment_path) / "session" / run_id
            run_folder.mkdir(parents=True, exist_ok=True)
            setup_logging(Path(self.experiment_path), run_folder)
            
            # Initialize audit logger
            self._log_progress("🔧 Initializing audit logger...")
            audit_logger = AuditLogger(
                security_boundary=self.security,
                run_folder=run_folder
            )
            
            # Initialize artifact storage - USE SHARED CACHE for perfect caching
            self._log_progress("🔧 Initializing artifact storage...")
            shared_cache_dir = self.experiment_path / "shared_cache"
            self.security.secure_mkdir(shared_cache_dir)
            self.artifact_storage = LocalArtifactStorage(
                security_boundary=self.security,
                run_folder=shared_cache_dir,
                run_name=run_id
            )
            
            # Initialize manifest
            self._log_progress("🔧 Initializing manifest...")
            self.manifest = EnhancedManifest(
                security_boundary=self.security,
                run_folder=run_folder,
                audit_logger=audit_logger,
                artifact_storage=self.artifact_storage
            )
            
            return audit_logger
        except Exception as e:
            self._log_progress(f"❌ Infrastructure initialization failed: {str(e)}")
            raise
    
    def _load_v8_specs(self) -> Dict[str, Any]:
        """Load v8.0 experiment specifications - experiment agnostic."""
        experiment_file = Path(self.experiment_path) / "experiment.md"
        if not experiment_file.exists():
            raise V8OrchestrationError(f"Experiment file not found: {experiment_file}")
        
        # Parse experiment.md to extract actual framework and corpus paths
        experiment_content = experiment_file.read_text(encoding='utf-8')
        
        # Extract framework path (look for .md files that aren't experiment.md)
        framework_files = [f for f in Path(self.experiment_path).glob("*.md") 
                          if f.name != "experiment.md"]
        if not framework_files:
            raise V8OrchestrationError("No framework file found (expected .md file other than experiment.md)")
        
        # Use the first framework file found (or could parse from experiment.md frontmatter)
        framework_path = framework_files[0].name
        
        # Detect corpus structure
        corpus_path = Path(self.experiment_path) / "corpus"
        if not corpus_path.exists():
            raise V8OrchestrationError(f"Corpus directory not found: {corpus_path}")
        
        return {
            "name": self.experiment_path.name,
            "version": "8.0", 
            "framework": framework_path,
            "corpus": "corpus"
        }
    
    def _run_coherence_validation(self, validation_model: str, audit_logger: AuditLogger):
        """Run experiment coherence validation."""
        validator = ExperimentCoherenceAgent(
            model=validation_model,
            audit_logger=audit_logger
        )
        
        validation_result = validator.validate_experiment(self.experiment_path)
        
        # Check for blocking issues
        blocking_issues = validation_result.get_issues_by_priority("BLOCKING")
        if blocking_issues:
            issues_summary = "; ".join([issue.description for issue in blocking_issues])
            raise V8OrchestrationError(f"Blocking validation issues: {issues_summary}")
    
    def _run_analysis_phase(self, analysis_model: str, audit_logger: AuditLogger) -> List[Dict[str, Any]]:
        """Run analysis phase using the existing, working analysis agent - experiment agnostic."""
        # Get experiment specifications (agnostic detection)
        experiment_config = self._load_v8_specs()
        
        # Load corpus documents (agnostic to file types and count)
        corpus_path = Path(self.experiment_path) / experiment_config["corpus"]
        if not corpus_path.exists():
            raise V8OrchestrationError(f"Corpus directory not found: {corpus_path}")
        
        # Load framework (agnostic to framework name)
        framework_path = Path(self.experiment_path) / experiment_config["framework"]
        if not framework_path.exists():
            raise V8OrchestrationError(f"Framework not found: {framework_path}")
        
        framework_content = framework_path.read_text(encoding='utf-8')
        
        # Initialize analysis agent (our reliable working component)
        analysis_agent = EnhancedAnalysisAgent(
            security_boundary=self.security,
            audit_logger=audit_logger,
            artifact_storage=self.artifact_storage
        )
        
        # Get corpus documents (text files only, intelligent filtering)
        corpus_documents = []
        
        # V8.0 Specification: Text files only in corpus directory
        for doc_file in corpus_path.glob("*.txt"):
            corpus_documents.append({
                "filename": doc_file.name,
                "content": doc_file.read_text(encoding='utf-8')
            })
        
        if not corpus_documents:
            raise V8OrchestrationError(f"No text documents found in {corpus_path} (v8.0 requires .txt files only)")
        
        # Load corpus metadata for analysis context (do NOT analyze as content)
        corpus_metadata = self._load_corpus_metadata()
        
        self._log_progress(f"📊 Analyzing {len(corpus_documents)} text documents with metadata context...")
        
        # Run sequential analysis on documents (THIN principle: one at a time for scalability)
        self._log_progress(f"🚀 Starting sequential analysis of {len(corpus_documents)} documents...")
        
        experiment_config = {
            "name": self.experiment_path.name,
            "version": "8.0"
        }
        
        analysis_results = []
        
        # Process each document individually for optimal caching and scalability
        for i, doc in enumerate(corpus_documents):
            doc_filename = doc.get('filename', 'unknown')
            self._log_progress(f"📄 Analyzing document {i+1}/{len(corpus_documents)}: {doc_filename}")
            
            try:
                # Single document analysis (proven ThinOrchestrator pattern)
                result = analysis_agent.analyze_batch(
                    framework_content=framework_content,
                    corpus_documents=[doc],  # Single document for optimal caching
                    experiment_config=experiment_config,
                    model=analysis_model,
                    current_scores_hash=None,  # Individual document analysis
                    current_evidence_hash=None
                )
                
                # Log successful analysis with provenance
                self._log_status(f"Document {doc_filename} analyzed successfully")
                audit_logger.log_agent_event(
                    "v8_analysis_phase", 
                    "document_analysis_complete",
                    {
                        "document_filename": doc_filename,
                        "document_index": i + 1,
                        "total_documents": len(corpus_documents),
                        "analysis_model": analysis_model,
                        "scores_hash": result.get('scores_hash'),
                        "evidence_hash": result.get('evidence_hash')
                    }
                )
                
                # Preserve individual document results for v8.0 agents
                analysis_results.append(result)
                
            except Exception as e:
                error_msg = f"Analysis failed for document {doc_filename}: {str(e)}"
                self._log_progress(f"❌ {error_msg}")
                audit_logger.log_agent_event(
                    "v8_analysis_phase",
                    "document_analysis_error", 
                    {
                        "document_filename": doc_filename,
                        "document_index": i + 1,
                        "error": str(e)
                    }
                )
                # Store error result for completeness
                analysis_results.append({
                    "error": str(e), 
                    "document": doc_filename,
                    "document_index": i + 1
                })
        
        # Log completion with accurate count
        successful_analyses = len([r for r in analysis_results if 'error' not in r])
        self._log_status(f"Sequential analysis completed: {successful_analyses}/{len(corpus_documents)} documents analyzed successfully")
        
        return analysis_results
    
    def _execute_v8_agents(self, 
                          analysis_results: List[Dict[str, Any]], 
                          analysis_model: str, 
                          synthesis_model: str, 
                          audit_logger: AuditLogger) -> Dict[str, Any]:
        """Execute v8.0 agents via the notebook generation orchestrator."""
        self._log_progress("🔬 Executing V8.0 agents via notebook orchestrator...")
        
        # Initialize notebook generation orchestrator
        notebook_orchestrator = NotebookGenerationOrchestrator(
            experiment_path=self.experiment_path,
            security=self.security,
            audit_logger=audit_logger
        )
        
        # Load framework content for the notebook orchestrator (experiment agnostic)
        experiment_config = self._load_v8_specs()
        framework_path = Path(self.experiment_path) / experiment_config["framework"]
        framework_content = framework_path.read_text(encoding='utf-8')
        
        # Execute notebook generation with analysis results and framework content
        notebook_results = notebook_orchestrator.generate_notebook_with_analysis(
            analysis_model=analysis_model,
            synthesis_model=synthesis_model,
            analysis_results=analysis_results,
            framework_content=framework_content
        )
        
        return notebook_results
    
    def _load_corpus_metadata(self) -> Dict[str, Any]:
        """Load corpus metadata from corpus.md (do NOT analyze as content)."""
        corpus_metadata_file = Path(self.experiment_path) / "corpus.md"
        
        if not corpus_metadata_file.exists():
            self._log_progress("⚠️ No corpus.md found - proceeding without metadata context")
            return {}
        
        try:
            corpus_content = corpus_metadata_file.read_text(encoding='utf-8')
            
            # Extract YAML metadata from corpus.md (human-first format)
            if '```yaml' in corpus_content:
                yaml_start = corpus_content.find('```yaml') + 7
                yaml_end = corpus_content.find('```', yaml_start)
                if yaml_end > yaml_start:
                    import yaml
                    yaml_content = corpus_content[yaml_start:yaml_end].strip()
                    metadata = yaml.safe_load(yaml_content)
                    
                    self._log_progress(f"📋 Loaded corpus metadata: {metadata.get('name', 'Unknown')} ({metadata.get('total_documents', 0)} documents)")
                    return metadata
            
            # Fallback: basic metadata
            return {"source": "corpus.md", "format": "markdown"}
            
        except Exception as e:
            self._log_progress(f"⚠️ Could not parse corpus metadata: {str(e)}")
            return {}
