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
from .prompt_assemblers.data_aggregation_assembler import DataAggregationPromptAssembler
from ..gateway.llm_gateway import LLMGateway
from ..gateway.model_registry import ModelRegistry
from .secure_code_executor import SecureCodeExecutor
from .capability_registry import CapabilityRegistry
from .unified_synthesis_agent import UnifiedSynthesisAgent
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
        self.logger = get_logger("experiment_orchestrator")
        self.config = {}
        self.llm_gateway = None
        self.secure_code_executor = None
        
        self.logger.info(f"Orchestrator initialized for: {self.security.experiment_name}")
    
    def _log_progress(self, message: str):
        """Log progress with rich console output."""
        self.logger.info(message)
    
    def _log_status(self, message: str):
        """Log status updates."""
        self.logger.info(f"STATUS: {message}")
    
    def run_experiment(self, 
                      analysis_model: str = "vertex_ai/gemini-2.5-pro",
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

            # Phase 4: Load analysis results from simplified format
            raw_scores_df = self._load_analysis_data_simple()
            self._log_status(f"Analysis data loaded into DataFrame ({raw_scores_df.shape[0]} rows)")

            # Phase 5: Calculate derived metrics
            derived_metrics_df = self._calculate_derived_metrics(raw_scores_df, synthesis_model)
            self._log_status(f"Derived metrics calculated ({derived_metrics_df.shape[1] - raw_scores_df.shape[1]} new columns)")

            # Phase 6: Perform statistical analysis
            statistical_results = self._perform_statistical_analysis(raw_scores_df, derived_metrics_df, synthesis_model)
            self._log_status(f"Statistical analysis completed ({len(statistical_results)} result categories)")

            # Phase 7: Store all research artifacts
            artifact_hashes = self._store_research_artifacts(raw_scores_df, derived_metrics_df, statistical_results)
            self._log_status(f"Research artifacts stored: {len(artifact_hashes)} files")

            # Phase 8: Generate final synthesis report (optional - continue on failure)
            synthesis_result = None
            try:
                synthesis_result = self._generate_final_report(synthesis_model, artifact_hashes)
                self._log_status(f"Final synthesis report generated: {synthesis_result['report_length']} characters")
            except Exception as e:
                self._log_progress(f"⚠️ Synthesis failed (core pipeline still successful): {e}")
                # Continue without synthesis - core research deliverables are complete

            # Phase 9: Organize final results in run-specific directory
            results_dir = self._create_run_results_directory(run_id, artifact_hashes, synthesis_result)
            self._log_status(f"Final results organized in: {results_dir}")

            self._log_progress("✅ Experiment completed successfully!")
            
            return {
                "status": "completed", 
                "run_id": run_id,
                "results_directory": str(results_dir),
                "final_report": synthesis_result["final_report"],
                "raw_scores_df": raw_scores_df, 
                "derived_metrics_df": derived_metrics_df, 
                "statistical_results": statistical_results,
                "artifact_hashes": artifact_hashes,
                "synthesis_quality": synthesis_result["quality_metrics"]
            }
            
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
            capability_registry = CapabilityRegistry()
            self.secure_code_executor = SecureCodeExecutor(capability_registry=capability_registry)
            
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
        
        # Define paths to the current specification documents
        # Assuming a standard project structure where 'docs' is at the project root
        project_root = Path(__file__).resolve().parents[2]
        spec_paths = {
            "FRAMEWORK_SPECIFICATION": project_root / "docs/specifications/FRAMEWORK_SPECIFICATION.md",
            "EXPERIMENT_SPECIFICATION": project_root / "docs/specifications/EXPERIMENT_SPECIFICATION.md",
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
                
                # Get the full path from the artifact metadata
                metadata = self.artifact_storage.get_artifact_metadata(artifact_hash)
                relative_path = metadata.get('artifact_path')
                if not relative_path:
                    raise V8OrchestrationError(f"Artifact {artifact_hash} was stored, but no path was found in metadata.")
                
                artifact_path = self.artifact_storage.run_folder / relative_path

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
        # Use natural markdown format instead of structured output for better reliability
        model_name = "vertex_ai/gemini-2.5-flash" # Use Flash for reliable code generation
        
        response_text, metadata = self.llm_gateway.execute_call(
            model=model_name,
            prompt=prompt
        )
        if not metadata.get("success") or not response_text:
            raise V8OrchestrationError(f"Failed to generate data aggregation script: {metadata.get('error')}")
        
        # Handle both pure Python (Flash) and markdown-wrapped Python (Flash Lite)
        aggregation_script = response_text.strip()
        
        # If wrapped in markdown blocks, extract the code
        if aggregation_script.startswith('```python') and aggregation_script.endswith('```'):
            lines = aggregation_script.split('\n')
            aggregation_script = '\n'.join(lines[1:-1])  # Remove first and last lines
        
        # Basic validation - ensure it looks like Python code
        if not aggregation_script or not any(keyword in aggregation_script for keyword in ['def ', 'import ', 'pandas']):
            raise V8OrchestrationError(f"LLM response does not appear to be Python code. Response: {response_text[:200]}...")

        # 3. Execute the script
        # The script's `aggregate_data` function needs the list of file paths.
        # We pass the paths as a list of strings to be JSON-safe for the executor.
        file_paths_str = [str(p) for p in analysis_artifact_paths]
        
        # Simple approach: append our execution code after the LLM script
        # The SecureCodeExecutor will execute everything and we'll extract result_json from the context
        execution_code = f"""{aggregation_script}

# Execution wrapper - call the function and store result
import json
file_paths = {file_paths_str}
result_df = aggregate_data(file_paths)
result_json = result_df.to_json(orient='records')
"""
        
        # Use data_aggregation preset for controlled file operations
        capability_registry = CapabilityRegistry()
        executor = SecureCodeExecutor(capability_registry=capability_registry)
        result = executor.execute_code(code=execution_code)

        if not result["success"]:
            raise V8OrchestrationError(f"Failed to execute data aggregation script: {result['error']}")
            
        # Extract the result_json from the execution context
        context = result.get("context", {})
        df_json = context.get("result_json")
        if not df_json:
            raise V8OrchestrationError("Aggregation script did not return the expected JSON result.")
            
        return pd.read_json(df_json, orient='records')

    def _load_analysis_data_simple(self):
        """
        Load analysis data directly from raw_analysis_response files.
        This works with the current storage architecture.
        """
        artifacts_dir = self.experiment_path / "shared_cache/artifacts"
        raw_files = list(artifacts_dir.glob("raw_analysis_response_v6_*"))
        
        if not raw_files:
            raise V8OrchestrationError("No raw analysis response files found")
        
        dimensions_data = []
        
        for raw_file in raw_files:
            with open(raw_file, 'r') as f:
                raw_response = f.read()
            
            # Parse the JSON content
            import re
            json_match = re.search(r'<<<DISCERNUS_ANALYSIS_JSON_v6>>>\n(.*)\n<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>', raw_response, re.DOTALL)
            
            if json_match:
                try:
                    inner_json = json.loads(json_match.group(1))
                    doc_analysis = inner_json['document_analyses'][0]
                    
                    dimensions_data.append({
                        'document_name': doc_analysis.get('document_name'),
                        'document_id': doc_analysis.get('document_id', doc_analysis.get('document_name')),
                        'dimensions': doc_analysis.get('dimensional_scores', {})
                    })
                except (json.JSONDecodeError, KeyError, IndexError) as e:
                    self.logger.warning(f"Failed to parse {raw_file.name}: {e}")
                    continue
        
        if not dimensions_data:
            raise V8OrchestrationError("No valid analysis data could be parsed from raw response files")
        
        return pd.DataFrame(dimensions_data)

    def _calculate_derived_metrics(self, raw_scores_df, model_name: str):
        """
        Generate and execute Python code to calculate derived metrics from raw scores.
        Uses the same THIN approach as data aggregation.
        """
        self._log_progress("📊 Generating derived metrics calculation code...")
        
        # 1. Get framework derived metrics definitions
        framework_derived_metrics = self._get_framework_derived_metrics()
        if not framework_derived_metrics:
            self._log_progress("ℹ️  No derived metrics defined in framework, skipping calculation")
            return raw_scores_df
        
        # 2. Convert DataFrame to JSON sample for the prompt  
        sample_data = raw_scores_df.head(2).to_dict('records')  # Use first 2 rows as sample
        
        prompt = f"""You are a Python code generator. Your response must contain ONLY executable Python code, no explanations, no markdown blocks, no comments outside the code.

Generate a function `calculate_derived_metrics(df: pd.DataFrame) -> pd.DataFrame` that:
1. Takes a pandas DataFrame where each row has a 'dimensions' column containing nested dimensional scores
2. Calculates derived metrics by implementing the mathematical formulas explicitly (NO eval, NO dynamic execution)
3. Access nested values like: row['dimensions']['tribal_dominance']['raw_score']
4. Returns the original DataFrame with new derived metric columns added
5. Uses only these allowed libraries: pandas, numpy, math, statistics
6. CRITICAL: Do NOT use eval(), exec(), or any dynamic code execution - write explicit calculations

FRAMEWORK DERIVED METRICS TO IMPLEMENT:
{json.dumps(framework_derived_metrics, indent=2)}

DATA STRUCTURE SAMPLE (first 2 rows):
{json.dumps(sample_data, indent=2)}

EXAMPLE: For formula "min(dimensions.fear.raw_score, dimensions.hope.raw_score)", write:
min(row['dimensions']['fear']['raw_score'], row['dimensions']['hope']['raw_score'])

Respond with pure Python code only - no markdown, no explanations."""

        # 3. Generate the derived metrics script via LLM
        
        response_text, metadata = self.llm_gateway.execute_call(
            model=model_name,
            prompt=prompt
        )
        if not metadata.get("success") or not response_text:
            raise V8OrchestrationError(f"Failed to generate derived metrics script: {metadata.get('error')}")
        
        # 4. Handle both pure Python (Flash) and markdown-wrapped Python (Flash Lite)
        derived_metrics_script = response_text.strip()
        
        # If wrapped in markdown blocks, extract the code
        if derived_metrics_script.startswith('```python') and derived_metrics_script.endswith('```'):
            lines = derived_metrics_script.split('\n')
            derived_metrics_script = '\n'.join(lines[1:-1])
        
        # Basic validation
        if not derived_metrics_script or not any(keyword in derived_metrics_script for keyword in ['def ', 'import ', 'pandas']):
            raise V8OrchestrationError(f"LLM response does not appear to be Python code. Response: {response_text[:200]}...")

        # 5. Execute the script with the raw scores DataFrame
        execution_script = f"""{derived_metrics_script}

# Execute the function and store result
import json
result_df = calculate_derived_metrics(df)
result_json = result_df.to_json(orient='records')
"""

        # Use core capabilities (includes pandas, numpy, math, statistics)
        capability_registry = CapabilityRegistry()
        executor = SecureCodeExecutor(capability_registry=capability_registry)
        
        result = executor.execute_code(
            code=execution_script,
            context={'df': raw_scores_df}
        )
        
        if not result['success']:
            raise V8OrchestrationError(f"Failed to execute derived metrics script: {result['error']}")
        
        # Extract the result DataFrame
        context = result.get('context', {})
        result_json = context.get('result_json')
        if not result_json:
            raise V8OrchestrationError("Derived metrics script did not return result_json")
        
        # Convert back to DataFrame
        derived_metrics_df = pd.read_json(result_json, orient='records')
        
        return derived_metrics_df

    def _perform_statistical_analysis(self, raw_scores_df, derived_metrics_df, model_name: str):
        """
        Generate and execute Python code for comprehensive statistical analysis.
        Uses the same THIN approach as other code generation components.
        """
        self._log_progress("📊 Generating statistical analysis code...")
        
        # 1. Assemble the prompt for statistical analysis code generation
        from .prompt_assemblers.statistical_analysis_assembler import StatisticalAnalysisPromptAssembler
        assembler = StatisticalAnalysisPromptAssembler()
        
        prompt = assembler.assemble_prompt(
            framework_path=self.experiment_path / self.config['framework'],
            experiment_path=self.experiment_path / 'experiment.md',
            raw_scores_df=raw_scores_df,
            derived_metrics_df=derived_metrics_df
        )

        # 2. Generate the statistical analysis script via LLM
        
        response_text, metadata = self.llm_gateway.execute_call(
            model=model_name,
            prompt=prompt
        )
        if not metadata.get("success") or not response_text:
            raise V8OrchestrationError(f"Failed to generate statistical analysis script: {metadata.get('error')}")
        
        # 3. Handle both pure Python (Flash) and markdown-wrapped Python (Flash Lite)
        statistical_script = response_text.strip()
        
        # If wrapped in markdown blocks, extract the code
        if statistical_script.startswith('```python') and statistical_script.endswith('```'):
            lines = statistical_script.split('\n')
            statistical_script = '\n'.join(lines[1:-1])
        
        # Basic validation
        if not statistical_script or not any(keyword in statistical_script for keyword in ['def ', 'import ', 'pandas']):
            raise V8OrchestrationError(f"LLM response does not appear to be Python code. Response: {response_text[:200]}...")

        # 4. Execute the script with both DataFrames
        execution_script = f"""{statistical_script}

# Execute the function and store result
import json
statistical_results = perform_statistical_analysis(raw_df, derived_df)
result_json = json.dumps(statistical_results, default=str)  # Handle numpy types
"""

        # Use core capabilities (includes pandas, numpy, scipy, statistics)
        capability_registry = CapabilityRegistry()
        executor = SecureCodeExecutor(capability_registry=capability_registry)
        
        result = executor.execute_code(
            code=execution_script,
            context={'raw_df': raw_scores_df, 'derived_df': derived_metrics_df}
        )
        
        if not result['success']:
            raise V8OrchestrationError(f"Failed to execute statistical analysis script: {result['error']}")
        
        # Extract the result
        context = result.get('context', {})
        result_json = context.get('result_json')
        if not result_json:
            raise V8OrchestrationError("Statistical analysis script did not return result_json")
        
        # Parse the statistical results
        statistical_results = json.loads(result_json)
        
        return statistical_results

    def _store_research_artifacts(self, raw_scores_df, derived_metrics_df, statistical_results):
        """
        Store all research deliverables as persistent artifacts with full provenance.
        This is what makes an experiment actually complete.
        """
        self._log_progress("💾 Storing research artifacts...")
        
        artifact_hashes = {}
        
        # 1. Store Raw Analysis Data CSV
        raw_scores_csv = raw_scores_df.to_csv(index=False)
        raw_scores_hash = self.artifact_storage.put_artifact(
            content=raw_scores_csv.encode('utf-8'),
            metadata={
                'artifact_type': 'raw_analysis_data_csv',
                'experiment_name': self.security.experiment_name,
                'document_count': len(raw_scores_df),
                'dimension_count': len([col for col in raw_scores_df.columns if col.startswith('dimensions')])
            }
        )
        artifact_hashes['raw_scores_csv'] = raw_scores_hash
        
        # 2. Store Derived Metrics Data CSV  
        derived_metrics_csv = derived_metrics_df.to_csv(index=False)
        derived_metrics_hash = self.artifact_storage.put_artifact(
            content=derived_metrics_csv.encode('utf-8'),
            metadata={
                'artifact_type': 'derived_metrics_csv',
                'experiment_name': self.security.experiment_name,
                'metrics_count': len(derived_metrics_df.columns) - len(raw_scores_df.columns)
            }
        )
        artifact_hashes['derived_metrics_csv'] = derived_metrics_hash
        
        # 3. Store Statistical Results JSON
        statistical_json = json.dumps(statistical_results, indent=2, default=str)
        statistical_hash = self.artifact_storage.put_artifact(
            content=statistical_json.encode('utf-8'),
            metadata={
                'artifact_type': 'statistical_results_json',
                'experiment_name': self.security.experiment_name,
                'result_categories': len(statistical_results)
            }
        )
        artifact_hashes['statistical_results'] = statistical_hash
        
        # 4. Store Combined Research Data (for synthesis)
        research_data = {
            'experiment_metadata': {
                'name': self.security.experiment_name,
                'framework': self.config.get('framework'),
                'corpus_documents': len(raw_scores_df),
            },
            'raw_analysis_data': raw_scores_df.to_dict('records'),
            'derived_metrics_data': derived_metrics_df.to_dict('records'), 
            'statistical_results': statistical_results
        }
        
        research_data_json = json.dumps(research_data, indent=2, default=str)
        research_data_hash = self.artifact_storage.put_artifact(
            content=research_data_json.encode('utf-8'),
            metadata={
                'artifact_type': 'complete_research_data',
                'experiment_name': self.security.experiment_name,
                'ready_for_synthesis': True
            }
        )
        artifact_hashes['research_data'] = research_data_hash
        
        self._log_progress(f"📋 Artifacts stored with hashes: {list(artifact_hashes.keys())}")
        
        return artifact_hashes

    def _generate_final_report(self, synthesis_model: str, artifact_hashes: Dict[str, str]) -> Dict[str, Any]:
        """
        Generate final synthesis report using unified synthesis agent with txtai RAG integration.
        """
        self._log_progress("📝 Generating final synthesis report...")
        
        # Get evidence artifact hashes from the registry
        evidence_hashes = []
        for artifact_hash, artifact_info in self.artifact_storage.registry.items():
            metadata = artifact_info.get("metadata", {})
            if metadata.get("artifact_type", "").startswith("evidence_v6"):
                evidence_hashes.append(artifact_hash)
        
        if not evidence_hashes:
            raise V8OrchestrationError("No evidence artifacts found for synthesis")
        
        # Initialize unified synthesis agent with enhanced mode
        synthesis_agent = UnifiedSynthesisAgent(
            model=synthesis_model,
            audit_logger=self.audit_logger if hasattr(self, 'audit_logger') else None,
            enhanced_mode=True  # Enable CRIT-006 enhanced synthesis capabilities
        )
        
        # Generate final report
        synthesis_result = synthesis_agent.generate_final_report(
            framework_path=self.experiment_path / self.config['framework'],
            experiment_path=self.experiment_path / 'experiment.md',
            research_data_artifact_hash=artifact_hashes['research_data'],
            evidence_artifact_hashes=evidence_hashes,
            artifact_storage=self.artifact_storage
        )
        
        # Store final report as artifact
        final_report_hash = self.artifact_storage.put_artifact(
            content=synthesis_result['final_report'].encode('utf-8'),
            metadata={
                'artifact_type': 'final_synthesis_report',
                'experiment_name': self.security.experiment_name,
                'report_length': len(synthesis_result['final_report']),
                'evidence_pieces': synthesis_result['evidence_pieces_indexed'],
                'quality_score': synthesis_result['quality_metrics'].get('meets_basic_structure', False)
            }
        )
        
        return {
            "final_report": synthesis_result['final_report'],
            "quality_metrics": synthesis_result['quality_metrics'],
            "report_hash": final_report_hash,
            "report_length": len(synthesis_result['final_report'])
        }

    def _create_run_results_directory(self, run_id: str, artifact_hashes: Dict[str, str], synthesis_result: Optional[Dict[str, Any]] = None) -> Path:
        """
        Create run-specific results directory and copy final research artifacts there.
        This provides researchers with a clean, organized view of their results.
        """
        # Create run directory structure
        run_dir = self.experiment_path / "runs" / run_id
        results_dir = run_dir / "results"
        results_dir.mkdir(parents=True, exist_ok=True)
        
        # Define user-friendly filenames for research deliverables
        artifact_mappings = {
            'raw_scores_csv': 'raw_analysis_data.csv',
            'derived_metrics_csv': 'derived_metrics.csv', 
            'statistical_results': 'statistical_results.json',
            'research_data': 'complete_research_data.json'
        }
        
        # Add final report if synthesis was completed
        if synthesis_result and 'report_hash' in synthesis_result:
            artifact_mappings['final_report'] = 'final_report.md'
            artifact_hashes['final_report'] = synthesis_result['report_hash']
        
        # Copy artifacts to results directory with user-friendly names
        for artifact_key, user_filename in artifact_mappings.items():
            if artifact_key in artifact_hashes:
                artifact_hash = artifact_hashes[artifact_key]
                
                # Get artifact content from storage
                artifact_content = self.artifact_storage.get_artifact(artifact_hash)
                
                # Write to user-friendly location
                result_file = results_dir / user_filename
                with open(result_file, 'wb') as f:
                    f.write(artifact_content)
                
                self._log_progress(f"📄 Copied {artifact_key} → {user_filename}")
        
        # Create a summary file
        summary = {
            "experiment_name": self.security.experiment_name,
            "run_id": run_id,
            "framework": self.config.get('framework'),
            "corpus": self.config.get('corpus'),
            "completion_time": datetime.now(timezone.utc).isoformat(),
            "artifacts": {
                "raw_analysis_data.csv": "Complete dimensional scores for all documents",
                "derived_metrics.csv": "Calculated composite metrics and tension indices",
                "statistical_results.json": "Comprehensive statistical analysis results",
                "complete_research_data.json": "Combined dataset ready for synthesis",
                "final_report.md": "Publication-ready research report with evidence citations"
            },
            "artifact_hashes": artifact_hashes
        }
        
        summary_file = results_dir / "experiment_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        return results_dir

    def _get_framework_derived_metrics(self):
        """Extract derived metrics definitions from the loaded framework."""
        framework_content = self._read_file(self.experiment_path / self.config['framework'])
        framework_yaml = self._parse_framework_yaml(framework_content)
        return framework_yaml.get('derived_metrics', {})

    def _parse_framework_yaml(self, content: str):
        """Parse YAML from framework's machine-readable appendix."""
        try:
            if '## Part 2: The Machine-Readable Appendix' in content:
                _, appendix_content = content.split('## Part 2: The Machine-Readable Appendix', 1)
                if '```yaml' in appendix_content:
                    yaml_start = appendix_content.find('```yaml') + 7
                    yaml_end = appendix_content.rfind('```')
                    yaml_content = appendix_content[yaml_start:yaml_end].strip() if yaml_end > yaml_start else appendix_content[yaml_start:].strip()
                    return yaml.safe_load(yaml_content)
            raise ValueError("Machine-readable appendix not found in framework.")
        except Exception as e:
            raise ValueError(f"Failed to parse framework YAML: {e}")

    def _read_file(self, file_path):
        """Read file content safely."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    
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
