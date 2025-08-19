#!/usr/bin/env python3
"""
THIN Orchestrator - Clean Architecture
==========================================

A focused orchestrator for experiments that preserves a working
analysis stage and adds clean notebook generation without legacy synthesis complexity.

Architecture:
1. Load specs (experiment.md, framework, corpus)
2. Run analysis (using EnhancedAnalysisAgent)
3. Run coherence validation (ExperimentCoherenceAgent)
4. Execute agents via NotebookGenerationOrchestrator
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
import yaml

from .logging_config import setup_logging, get_logger, log_experiment_start, log_experiment_complete, log_experiment_failure
from .security_boundary import ExperimentSecurityBoundary
from .audit_logger import AuditLogger
from .local_artifact_storage import LocalArtifactStorage
from .enhanced_manifest import EnhancedManifest
from .notebook_generation_orchestrator import NotebookGenerationOrchestrator
from ..cli_console import DiscernusConsole
from .prompt_assemblers.data_aggregation_assembler import DataAggregationPromptAssembler
from ..gateway.llm_gateway import LLMGateway
from ..gateway.model_registry import ModelRegistry
from .secure_code_executor import SecureCodeExecutor
import pandas as pd
from ..agents.experiment_coherence_agent import ExperimentCoherenceAgent
from ..agents.EnhancedAnalysisAgent.main import EnhancedAnalysisAgent


class V8OrchestrationError(Exception):
    """Custom exception for orchestration errors."""
    pass


class ExperimentOrchestrator:
    """
    Clean orchestrator focused on notebook generation.
    
    Preserves the working analysis stage and adds clean agent execution
    without the complexity of legacy synthesis pipelines.
    """
    
    def __init__(self, experiment_path: Path):
        """Initialize orchestrator for an experiment."""
        self.experiment_path = Path(experiment_path).resolve()
        
        # Initialize core components
        self.security = ExperimentSecurityBoundary(self.experiment_path)
        self.console = DiscernusConsole()
        self.logger = get_logger("experiment_orchestrator")
        self.config = {}
        self.llm_gateway = None
        self.secure_code_executor = None
        
        self.logger.info(f"Orchestrator initialized for: {self.security.experiment_name}")
        self._log_progress(f"🎯 Orchestrator initialized for: {self.security.experiment_name}")
    
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
        Run complete experiment pipeline.
        
        Args:
            analysis_model: LLM model for analysis tasks
            synthesis_model: LLM model for synthesis tasks (used by agents)
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
            
            self._log_progress("🚀 Starting experiment pipeline...")
            
            # Phase 1: Load and validate specifications
            self._log_progress("📋 Loading specifications...")
            self.config = self._load_specs()
            self._log_status("Specifications loaded")
            
            # Phase 2: Run coherence validation (unless skipped)
            if not skip_validation:
                self._run_coherence_validation(validation_model, audit_logger)
                self._log_status("Experiment coherence validated")
            
            # Phase 3: Run analysis (our reliable working component)
            analysis_artifact_paths = self._run_analysis_phase(analysis_model, audit_logger)
            self._log_status(f"Analysis completed: {len(analysis_artifact_paths)} documents processed")

            # Phase 4: Aggregate analysis results
            raw_scores_df = self._aggregate_analysis_results(analysis_artifact_paths)
            self._log_status(f"Analysis results aggregated into DataFrame ({raw_scores_df.shape[0]} rows)")

            # Phase 5: Calculate derived metrics
            # ... integration for DerivedMetricsPipeline will go here ...

            self._log_progress("✅ Experiment completed successfully!")
            self.console.print_success("Experiment completed successfully!")
            
            return results
            
        except V8OrchestrationError as e:
            log_experiment_failure(self.security.experiment_name, run_id, str(e), "orchestration")
            self._log_progress(f"❌ Experiment failed: {str(e)}")
            raise V8OrchestrationError(f"Experiment failed: {str(e)}") from e
    
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

            # Initialize LLM Gateway
            self._log_progress("🔧 Initializing LLM Gateway...")
            self.llm_gateway = LLMGateway(ModelRegistry())

            # Initialize Secure Code Executor
            self._log_progress("🔧 Initializing Secure Code Executor...")
            self.secure_code_executor = SecureCodeExecutor()
            
            return audit_logger
        except Exception as e:
            self._log_progress(f"❌ Infrastructure initialization failed: {str(e)}")
            raise
    
    def _load_specs(self) -> Dict[str, Any]:
        """Load experiment specifications - experiment agnostic."""
        experiment_file = Path(self.experiment_path) / "experiment.md"
        if not experiment_file.exists():
            raise V8OrchestrationError(f"Experiment file not found: {experiment_file}")
        
        # Parse experiment.md to extract YAML appendix
        try:
            content = experiment_file.read_text(encoding='utf-8')
            if '## Configuration Appendix' in content:
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

                import yaml
                config = yaml.safe_load(yaml_content)
                if not isinstance(config, dict):
                    raise V8OrchestrationError("Invalid YAML structure in experiment appendix.")
            else:
                raise V8OrchestrationError("Could not find '## Configuration Appendix' in experiment.md.")
        except Exception as e:
            raise V8OrchestrationError(f"Failed to parse experiment.md YAML: {e}")

        # V10 Specification Validation
        spec_version = config.get('metadata', {}).get('spec_version')
        if not spec_version or not str(spec_version).startswith('10.'):
             raise V8OrchestrationError(f"Experiment spec_version is '{spec_version}', but this orchestrator requires v10.0.")

        framework_filename = config.get('components', {}).get('framework')
        corpus_filename = config.get('components', {}).get('corpus')

        if not framework_filename or not corpus_filename:
            raise V8OrchestrationError("Experiment `components` section must specify both `framework` and `corpus` files.")
            
        return {
            "name": config.get('metadata', {}).get('experiment_name', self.experiment_path.name),
            "version": "10.0", 
            "framework": framework_filename,
            "corpus": corpus_filename
        }
    
    def _run_coherence_validation(self, validation_model: str, audit_logger: AuditLogger):
        """Run experiment coherence validation using the intelligent agent."""
        self._log_progress("🔬 Validating experiment coherence with AI agent...")
        
        # Define paths to the V10 specification documents
        # Assuming a standard project structure where 'docs' is at the project root
        project_root = Path(__file__).resolve().parents[2]
        spec_paths = {
            "FRAMEWORK_SPECIFICATION": project_root / "docs/specifications/FRAMEWORK_SPECIFICATION.md",
            "EXPERIMENT_SPECIFICATION": project_root / "docs/specifications/EXPERIMENT_SPECIFICATION_V10.md",
            "CORPUS_SPECIFICATION": project_root / "docs/specifications/CORPUS_SPECIFICATION.md"
        }

        # Read specification contents
        spec_references = {}
        for name, path in spec_paths.items():
            if path.exists():
                spec_references[name] = path.read_text(encoding='utf-8')
            else:
                self._log_progress(f"⚠️ Warning: Specification file not found at {path}. Validation may be incomplete.")
                spec_references[name] = "Specification not found."

        validator = ExperimentCoherenceAgent(
            model=validation_model,
            audit_logger=audit_logger,
            specification_references=spec_references
        )
        
        validation_result = validator.validate_experiment(self.experiment_path)
        
        # Check for blocking issues
        blocking_issues = validation_result.get_issues_by_priority("BLOCKING")
        if blocking_issues:
            issues_summary = "; ".join([issue.description for issue in blocking_issues])
            raise V8OrchestrationError(f"Blocking validation issues: {issues_summary}")
    
    def _run_analysis_phase(self, analysis_model: str, audit_logger: AuditLogger) -> List[Path]:
        """Run analysis phase using a corrected, proven pattern."""
        self._log_progress("📊 Starting corrected analysis phase...")
        
        framework_content = (self.experiment_path / self.config['framework']).read_text(encoding='utf-8')
        
        analysis_agent = EnhancedAnalysisAgent(
            security_boundary=self.security,
            audit_logger=audit_logger,
            artifact_storage=self.artifact_storage
        )

        documents = self._load_corpus_documents()
        self._log_progress(f"📋 Analyzing {len(documents)} documents from corpus manifest...")

        results = []
        for i, doc_manifest in enumerate(documents):
            doc_filename = doc_manifest.get('filename')
            if not doc_filename:
                self._log_progress(f"⚠️ Skipping document {i+1} due to missing filename in manifest.")
                continue

            doc_path = self.experiment_path / 'corpus' / doc_filename
            if not doc_path.exists():
                self._log_progress(f"⚠️ Skipping missing document: {doc_path}")
                continue
            
            doc_content = doc_path.read_text(encoding='utf-8')
            doc_metadata = doc_manifest.get('metadata', {})
            
            self._log_progress(f"📄 Analyzing document {i+1}/{len(documents)}: {doc_filename}")
            
            try:
                # This is the proven pattern: analyze one document at a time for caching
                analysis_data = analysis_agent.analyze_batch(
                    framework_content=framework_content,
                    corpus_documents=[{'filename': doc_filename, 'content': doc_content, 'metadata': doc_metadata}],
                    experiment_config=self.config,
                    model=analysis_model,
                )
                
                # The orchestrator is responsible for storing the artifact
                artifact_hash = self.artifact_storage.put_artifact(
                    content=json.dumps(analysis_data).encode('utf-8'),
                    metadata={
                        'artifact_type': 'analysis_result',
                        'document_id': doc_manifest.get('document_id', doc_filename)
                    }
                )
                artifact_path = self.artifact_storage.get_artifact_path(artifact_hash)
                
                results.append({
                    "document": doc_filename,
                    "artifact_path": artifact_path,
                    "status": "success"
                })
                self._log_status(f"Document {doc_filename} analyzed successfully.")

            except Exception as e:
                self._log_progress(f"❌ Analysis failed for document {doc_filename}: {e}")
                results.append({"document": doc_filename, "status": "failed", "error": str(e)})

        successful_analyses = [r for r in results if r['status'] == 'success']
        self._log_status(f"Analysis phase complete: {len(successful_analyses)}/{len(documents)} documents processed.")
        
        return [r['artifact_path'] for r in successful_analyses]

    def _load_corpus_documents(self) -> List[Dict[str, Any]]:
        """Loads and parses the corpus manifest to get document details."""
        corpus_manifest_path = self.experiment_path / self.config['corpus']
        if not corpus_manifest_path.exists():
            raise V8OrchestrationError(f"Corpus manifest not found: {corpus_manifest_path}")

        content = corpus_manifest_path.read_text(encoding='utf-8')
        if '## Document Manifest' in content:
            _, yaml_block = content.split('## Document Manifest', 1)
            if '```yaml' in yaml_block:
                yaml_start = yaml_block.find('```yaml') + 7
                yaml_end = yaml_block.rfind('```')
                yaml_content = yaml_block[yaml_start:yaml_end].strip() if yaml_end > yaml_start else yaml_block[yaml_start:].strip()
                manifest_data = yaml.safe_load(yaml_content)
                return manifest_data.get('documents', [])
        
        raise V8OrchestrationError("Could not parse `documents` from corpus manifest.")

    def _aggregate_analysis_results(self, analysis_artifact_paths: List[Path]) -> pd.DataFrame:
        """
        Generates and executes code to aggregate individual analysis JSON files into a single DataFrame.
        """
        self._log_progress("📊 Aggregating analysis results...")

        # 1. Assemble the prompt for the aggregation script
        assembler = DataAggregationPromptAssembler()
        prompt = assembler.assemble_prompt(
            framework_path=self.experiment_path / self.config['framework'],
            analysis_file_paths=analysis_artifact_paths
        )

        # 2. Generate the aggregation script via LLM
        # This uses the architectural mandate for structured output
        code_schema = {
            "type": "object", "properties": {"code": {"type": "string"}}, "required": ["code"]
        }
        model_name = "vertex_ai/gemini-2.5-flash" # Use a fast model for code-gen
        
        structured_response, metadata = self.llm_gateway.execute_call(
            model=model_name,
            prompt=prompt,
            response_schema=code_schema
        )
        if not metadata.get("success"):
            raise V8OrchestrationError(f"Failed to generate data aggregation script: {metadata.get('error')}")
        
        aggregation_script = structured_response.get("code")
        if not aggregation_script:
            raise V8OrchestrationError("LLM failed to return code for data aggregation.")

        # 3. Execute the script
        # The script's `aggregate_data` function needs the list of file paths.
        # We pass the paths as a list of strings to be JSON-safe for the executor.
        file_paths_str = [str(p) for p in analysis_artifact_paths]
        
        executor = SecureCodeExecutor()
        result = executor.execute_code(
            code_str=aggregation_script,
            function_to_call="aggregate_data",
            function_args=[file_paths_str]
        )

        if not result["success"]:
            raise V8OrchestrationError(f"Failed to execute data aggregation script: {result['stderr']}")
            
        # The result of the function call is returned as a JSON string in 'result_json'
        df_json = result.get("result_json")
        if not df_json:
            raise V8OrchestrationError("Aggregation script did not return the expected JSON result.")
            
        return pd.read_json(df_json, orient='split')


    def _execute_v8_agents(self, 
                          analysis_results: List[Dict[str, Any]], 
                          analysis_model: str, 
                          synthesis_model: str, 
                          audit_logger: AuditLogger) -> Dict[str, Any]:
        """Execute agents via the notebook generation orchestrator."""
        self._log_progress("🔬 Executing agents via notebook orchestrator...")
        
        # Initialize notebook generation orchestrator
        notebook_orchestrator = NotebookGenerationOrchestrator(
            experiment_path=self.experiment_path,
            security=self.security,
            audit_logger=audit_logger
        )
        
        # Load framework content for the notebook orchestrator (experiment agnostic)
        experiment_config = self._load_specs()
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
