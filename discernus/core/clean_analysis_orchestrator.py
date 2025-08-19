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
            statistical_results = self._run_statistical_analysis(synthesis_model, audit_logger)
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
    
    def _run_statistical_analysis(self, model: str, audit_logger: AuditLogger) -> Dict[str, Any]:
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
            stats_result = stats_agent.generate_functions(temp_workspace)
            
            # Store statistical results in artifact storage
            stats_hash = self.artifact_storage.put_artifact(
                json.dumps(stats_result, indent=2).encode('utf-8'),
                {"artifact_type": "statistical_results"}
            )
            
            self._log_progress(f"📊 Statistical analysis completed and stored: {stats_hash[:8]}")
            
            return {
                "status": "completed",
                "stats_hash": stats_hash,
                "functions_generated": len(stats_result.get('functions', {})),
                "statistical_results": stats_result
            }
            
        finally:
            # Clean up temporary workspace
            if temp_workspace.exists():
                import shutil
                shutil.rmtree(temp_workspace)
    
    def _run_synthesis(self, synthesis_model: str, audit_logger: AuditLogger, statistical_results: Dict[str, Any]) -> Dict[str, Any]:
        """Run synthesis to generate final report."""
        self._log_progress("📝 Running synthesis...")
        
        try:
            # Initialize synthesis agent
            from .reuse_candidates.unified_synthesis_agent import UnifiedSynthesisAgent
            
            synthesis_agent = UnifiedSynthesisAgent(
                model=synthesis_model,
                audit_logger=audit_logger,
                artifact_storage=self.artifact_storage
            )
            
            # Load framework and experiment content for synthesis
            framework_path = self.experiment_path / self.config['framework']
            framework_content = framework_path.read_text(encoding='utf-8')
            
            experiment_content = f"""
            Experiment: {self.config['name']}
            Description: {self.config.get('description', '')}
            Questions: {'; '.join(self.config.get('questions', []))}
            """
            
            # Create synthesis request
            synthesis_request = {
                "framework_content": framework_content,
                "experiment_content": experiment_content,
                "research_data": statistical_results.get('statistical_results', {}),
                "evidence_context": "Evidence available in shared cache"
            }
            
            # Generate synthesis report
            synthesis_result = synthesis_agent.generate_synthesis_report(synthesis_request)
            
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
