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
        
        self.logger.info(f"Clean orchestrator initialized for: {self.security.experiment_name}")
    
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
            self.config = self._load_specs()
            self._log_status("Specifications loaded")
            
            # Phase 2: Validation (unless skipped)
            if not skip_validation:
                self._run_coherence_validation(validation_model, audit_logger)
                self._log_status("Experiment coherence validated")
            
            # Phase 3: Validate corpus files
            missing_files = self._validate_corpus_files_exist()
            if missing_files:
                error_msg = f"Corpus validation failed. Missing files: {', '.join(missing_files)}"
                raise CleanAnalysisError(error_msg)
            self._log_status("Corpus files validated")
            
            # Phase 4: Run analysis
            analysis_results = self._run_analysis_phase(analysis_model, audit_logger)
            self._log_status(f"Analysis completed: {len(analysis_results)} documents processed")
            
            # Phase 5: Generate statistics
            statistical_results = self._run_statistical_analysis(synthesis_model, audit_logger, analysis_results)
            self._log_status("Statistical analysis completed")
            
            # Phase 6: Run synthesis
            synthesis_result = self._run_synthesis(synthesis_model, audit_logger, statistical_results)
            self._log_status("Synthesis completed")
            
            # Phase 7: Create results with publication readiness
            results_dir = self._create_clean_results_directory(run_id, statistical_results, synthesis_result)
            self._log_status(f"Results created: {results_dir}")
            
            duration = (datetime.now(timezone.utc) - start_time).total_seconds()
            log_experiment_complete(self.security.experiment_name, run_id, duration)
            
            return {
                "run_id": run_id,
                "results_directory": str(results_dir),
                "analysis_documents": len(analysis_results),
                "status": "completed"
            }
            
        except Exception as e:
            log_experiment_failure(self.security.experiment_name, run_id, "experiment_execution", str(e))
            self._log_progress(f"❌ Experiment failed: {str(e)}")
            raise CleanAnalysisError(f"Experiment failed: {str(e)}")
    
    def _initialize_infrastructure(self, run_id: str) -> AuditLogger:
        """Initialize minimal infrastructure components."""
        # Initialize audit logging
        session_dir = self.experiment_path / "session" / run_id
        session_dir.mkdir(parents=True, exist_ok=True)
        
        audit_logger = AuditLogger(
            security_boundary=self.security,
            run_folder=session_dir / "logs"
        )
        self._log_progress(f"📋 Audit logging initialized: {session_dir / 'logs'}")
        
        # Initialize artifact storage
        shared_cache_dir = self.experiment_path / "shared_cache" / "artifacts"
        shared_cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.artifact_storage = LocalArtifactStorage(
            security_boundary=self.security,
            run_folder=shared_cache_dir,
            run_name=run_id
        )
        self._log_progress(f"🗄️ Local artifact storage initialized")
        
        return audit_logger
    
    def _load_specs(self) -> Dict[str, Any]:
        """Load experiment specifications."""
        experiment_file = self.experiment_path / "experiment.md"
        if not experiment_file.exists():
            raise CleanAnalysisError(f"Experiment file not found: {experiment_file}")
        
        # Parse frontmatter from experiment.md
        content = experiment_file.read_text(encoding='utf-8')
        if content.startswith('---'):
            _, frontmatter_block, _ = content.split('---', 2)
            config = yaml.safe_load(frontmatter_block)
            return config
        else:
            raise CleanAnalysisError("Experiment file missing YAML frontmatter")
    
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
        """Run analysis phase using EnhancedAnalysisAgent."""
        self._log_progress("📊 Starting analysis phase...")
        
        # Load corpus documents
        corpus_documents = self._load_corpus_documents()
        self._log_progress(f"📋 Analyzing {len(corpus_documents)} documents from corpus manifest...")
        
        # Load framework
        framework_path = self.experiment_path / self.config['framework']
        framework_content = framework_path.read_text(encoding='utf-8')
        
        # Initialize analysis agent
        analysis_agent = EnhancedAnalysisAgent(
            security_boundary=self.security,
            audit_logger=audit_logger,
            artifact_storage=self.artifact_storage
        )
        
        # Prepare corpus documents with content for batch analysis
        corpus_dir = self.experiment_path / "corpus"
        prepared_documents = []
        
        for doc_info in corpus_documents:
            filename = doc_info.get('filename')
            if not filename:
                continue
                
            # Find and load document
            source_file = self._find_corpus_file(corpus_dir, filename)
            if not source_file.exists():
                self._log_progress(f"⚠️ Skipping missing file: {filename}")
                continue
            
            document_content = source_file.read_text(encoding='utf-8')
            
            # Prepare document in the format expected by analyze_batch
            prepared_doc = {
                'filename': filename,
                'content': document_content,
                'metadata': doc_info.get('metadata', {})
            }
            prepared_documents.append(prepared_doc)
        
        # Create experiment config for analysis
        experiment_config = {
            "name": self.config['name'],
            "description": self.config.get('description', ''),
            "questions": self.config.get('questions', [])
        }
        
        # Run batch analysis (this is how the working orchestrator does it)
        self._log_progress(f"📊 Running batch analysis on {len(prepared_documents)} documents...")
        
        try:
            analysis_result = analysis_agent.analyze_batch(
                framework_content=framework_content,
                corpus_documents=prepared_documents,
                experiment_config=experiment_config,
                model=analysis_model
            )
            
            self._log_status(f"Batch analysis completed successfully")
            return [analysis_result]  # Return as list for consistency
            
        except Exception as e:
            self._log_progress(f"❌ Batch analysis failed: {str(e)}")
            raise CleanAnalysisError(f"Analysis phase failed: {str(e)}")
    
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
        """Convert analysis results to pandas DataFrame for statistical functions."""
        import pandas as pd
        import json
        
        # Extract the analysis data from the first result (batch analysis)
        if not analysis_results or len(analysis_results) == 0:
            raise CleanAnalysisError("No analysis results to convert")
        
        analysis_result = analysis_results[0]
        
        # Debug: Log the structure of analysis_result
        self._log_progress(f"🔍 Analysis result keys: {list(analysis_result.keys())}")
        
        # Parse the raw analysis response to get document analyses
        raw_response = analysis_result.get('raw_analysis_response', '')
        
        # If raw_response is empty, load it from artifact storage
        if not raw_response:
            self._log_progress(f"📥 Loading raw analysis response from artifact storage...")
            
            # Load the raw analysis response from artifact storage
            artifacts_dir = self.experiment_path / "shared_cache" / "artifacts" / "artifacts"
            raw_response_files = list(artifacts_dir.glob("raw_analysis_response_v6_*"))
            
            if raw_response_files:
                # Take the most recent one (sorted by name which includes timestamp)
                raw_response_file = sorted(raw_response_files)[-1]
                raw_response = raw_response_file.read_text(encoding='utf-8')
                self._log_progress(f"📥 Loaded raw analysis response from {raw_response_file.name}")
            else:
                raise CleanAnalysisError("No raw analysis response found in artifacts directory")
        
        # Extract JSON from the delimited response
        start_marker = '<<<DISCERNUS_ANALYSIS_JSON_v6>>>'
        end_marker = '<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>'
        
        start_idx = raw_response.find(start_marker)
        end_idx = raw_response.find(end_marker)
        
        if start_idx == -1 or end_idx == -1:
            # Debug: Log what we actually have
            self._log_progress(f"❌ Could not find JSON markers. Response length: {len(raw_response)}")
            self._log_progress(f"❌ Response preview: {raw_response[:500]}...")
            raise CleanAnalysisError(f"Could not find analysis JSON markers in response. Response length: {len(raw_response)}")
        
        json_content = raw_response[start_idx + len(start_marker):end_idx].strip()
        
        try:
            analysis_data = json.loads(json_content)
        except json.JSONDecodeError as e:
            self._log_progress(f"❌ JSON parsing failed: {str(e)}")
            self._log_progress(f"❌ JSON content preview: {json_content[:500]}...")
            raise CleanAnalysisError(f"Failed to parse analysis JSON: {str(e)}")
        
        # Convert document analyses to DataFrame rows
        rows = []
        for doc_analysis in analysis_data.get('document_analyses', []):
            row = {'document_name': doc_analysis.get('document_name', '')}
            
            # Add dimensional scores (both raw_score and salience)
            for dimension, scores in doc_analysis.get('dimensional_scores', {}).items():
                row[f"{dimension}_raw"] = scores.get('raw_score', 0.0)
                row[f"{dimension}_salience"] = scores.get('salience', 0.0)
                row[f"{dimension}_confidence"] = scores.get('confidence', 0.0)
            
            rows.append(row)
        
        df = pd.DataFrame(rows)
        self._log_progress(f"📊 Converted analysis to DataFrame: {len(df)} documents, {len(df.columns)} features")
        
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
    
    def _run_synthesis(self, synthesis_model: str, audit_logger: AuditLogger, statistical_results: Dict[str, Any]) -> Dict[str, Any]:
        """Run synthesis to generate final report."""
        self._log_progress("📝 Running synthesis...")
        
        try:
            # Initialize synthesis agent
            from .reuse_candidates.unified_synthesis_agent import UnifiedSynthesisAgent
            
            synthesis_agent = UnifiedSynthesisAgent(
                model=synthesis_model,
                audit_logger=audit_logger,
                enhanced_mode=True
            )
            
            # Prepare paths for synthesis
            framework_path = self.experiment_path / self.config['framework']
            experiment_path = self.experiment_path / "experiment.md"
            
            # Get research data artifact hash (we need to store the statistical results first)
            research_data_json = json.dumps(statistical_results, indent=2)
            research_data_hash = self.artifact_storage.put_artifact(
                research_data_json.encode('utf-8'),
                {"artifact_type": "research_data_for_synthesis"}
            )
            
            # Get evidence artifact hashes from the artifacts directory
            evidence_artifact_hashes = []
            artifacts_dir = self.experiment_path / "shared_cache" / "artifacts"
            if artifacts_dir.exists():
                evidence_files = list(artifacts_dir.glob("evidence_v6_*"))
                evidence_artifact_hashes = [f.stem for f in evidence_files]
            
            # Generate synthesis report
            synthesis_result = synthesis_agent.generate_final_report(
                framework_path=framework_path,
                experiment_path=experiment_path,
                research_data_artifact_hash=research_data_hash,
                evidence_artifact_hashes=evidence_artifact_hashes,
                artifact_storage=self.artifact_storage
            )
            
            # Store synthesis report
            if synthesis_result.get('final_report'):
                report_hash = self.artifact_storage.put_artifact(
                    synthesis_result['final_report'].encode('utf-8'),
                    {"artifact_type": "final_synthesis_report"}
                )
                
                self._log_progress(f"📝 Synthesis report generated and stored: {report_hash[:8]}")
                
                return {
                    "status": "completed",
                    "report_hash": report_hash,
                    "report_length": len(synthesis_result['final_report']),
                    "synthesis_result": synthesis_result
                }
            else:
                self._log_progress("⚠️ Synthesis completed but no report generated")
                return {
                    "status": "completed_no_report",
                    "synthesis_result": synthesis_result
                }
                
        except Exception as e:
            self._log_progress(f"⚠️ Synthesis failed: {str(e)}")
            # Return placeholder on failure
            return {
                "status": "failed",
                "error": str(e),
                "report": "Synthesis failed - statistical analysis completed successfully",
                "statistical_summary": statistical_results
            }
    
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
