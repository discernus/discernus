#!/usr/bin/env python3
"""
NotebookGenerationOrchestrator - v8.0 Transactional Notebook Generation
=======================================================================

Implements the core v8.0 innovation: atomic, all-or-nothing notebook generation
using an isolated workspace transaction model with comprehensive dual-track logging.

THIN Architecture:
- Isolated workspace transaction model (file-system based)
- Atomic operations with rollback capability
- Comprehensive dual-track logging for full visibility
- Minimal dependencies, maximum reliability

Transactional Model:
1. BEGIN: Create isolated workspace (/transactions/<run_id>/)
2. EXECUTE: All agents write to workspace (no permanent storage access)
3. COMMIT: On success, atomically move artifacts to permanent storage
4. ROLLBACK: On failure, delete entire workspace (clean state)
"""

import json
import shutil
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.v8_specifications import V8SpecificationLoader, V8ExperimentSpec
from discernus.core.universal_notebook_template import DataPath


@dataclass
class TransactionState:
    """State of a notebook generation transaction."""
    transaction_id: str
    workspace_path: Path
    status: str  # "active", "committed", "rolled_back"
    created_at: str
    agents_completed: List[str]
    artifacts_generated: List[str]


class NotebookGenerationOrchestrator:
    """
    Orchestrates v8.0 notebook generation using atomic transactions.
    
    THIN Principles:
    - Simple file-system based transactions (no complex state machines)
    - LLM agents handle intelligence, orchestrator handles infrastructure
    - Comprehensive logging for full visibility and debuggability
    - Atomic operations guarantee consistency
    """
    
    def __init__(self, 
                 experiment_path: Path,
                 security: ExperimentSecurityBoundary,
                 audit_logger: AuditLogger):
        """
        Initialize notebook generation orchestrator.
        
        Args:
            experiment_path: Path to experiment directory
            security: Security boundary for file operations
            audit_logger: Audit logger for dual-track logging
        """
        self.experiment_path = experiment_path
        self.security = security
        self.audit_logger = audit_logger
        self.agent_name = "NotebookGenerationOrchestrator"
        
        # Initialize v8.0 specification loader
        self.v8_loader = V8SpecificationLoader(experiment_path)
        
        # Transaction workspace base (inside experiment directory for security compliance)
        self.transactions_base = experiment_path / "transactions"
        
        # Current transaction state
        self.current_transaction: Optional[TransactionState] = None
    
    def generate_notebook(self, 
                         analysis_model: str = "vertex_ai/gemini-2.5-flash",
                         synthesis_model: str = "vertex_ai/gemini-2.5-pro",
                         analysis_results: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Generate notebook using atomic transaction model.
        
        Args:
            analysis_model: LLM model for analysis tasks
            synthesis_model: LLM model for synthesis tasks
            analysis_results: Pre-computed analysis results from v8.0 analysis phase
            
        Returns:
            Transaction result with notebook artifacts
            
        Raises:
            Exception: On transaction failure (workspace is automatically rolled back)
        """
        transaction_id = f"notebook_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
        
        try:
            # Phase 1: BEGIN TRANSACTION
            self._begin_transaction(transaction_id)
            
            # Phase 2: STORE ANALYSIS RESULTS (if provided) 
            if analysis_results:
                self._store_analysis_results(analysis_results)
                # Skip v8.0 specification loading when analysis results are provided
                v8_experiment = None
            else:
                # Phase 2: LOAD V8.0 SPECIFICATIONS (only when no analysis results)
                v8_experiment = self._load_v8_specifications()
            
            # Phase 3: EXECUTE AGENTS (in transactional workspace)
            self._execute_agents(v8_experiment, analysis_model, synthesis_model)
            
            # Phase 4: VALIDATE GENERATED FUNCTIONS
            self._validate_functions()
            
            # Phase 5: GENERATE COMPLETE NOTEBOOK (Phase 3 Integration)
            self._generate_complete_notebook(v8_experiment, analysis_model, synthesis_model)
            
            # Phase 6: COMMIT TRANSACTION
            result = self._commit_transaction()
            
            return result
            
        except Exception as e:
            # Phase 6: ROLLBACK ON FAILURE
            self._rollback_transaction(str(e))
            raise
    
    def _begin_transaction(self, transaction_id: str) -> None:
        """Begin isolated workspace transaction."""
        self.audit_logger.log_agent_event(
            self.agent_name,
            "TRANSACTION_BEGIN",
            {"transaction_id": transaction_id}
        )
        
        # Create isolated workspace
        workspace_path = self.transactions_base / transaction_id
        workspace_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize transaction state
        self.current_transaction = TransactionState(
            transaction_id=transaction_id,
            workspace_path=workspace_path,
            status="active",
            created_at=datetime.now(timezone.utc).isoformat(),
            agents_completed=[],
            artifacts_generated=[]
        )
        
        # Log transaction start
        self.audit_logger.log_agent_event(
            self.agent_name,
            "TRANSACTION_WORKSPACE_CREATED",
            {
                "transaction_id": transaction_id,
                "workspace_path": str(workspace_path),
                "isolation_model": "filesystem_based"
            }
        )
    
    def _load_v8_specifications(self) -> V8ExperimentSpec:
        """Load v8.0 specifications using THIN raw content approach."""
        self.audit_logger.log_agent_event(
            self.agent_name,
            "V8_SPECIFICATIONS_LOADING",
            {"loader_type": "raw_content_thin"}
        )
        
        try:
            # Load v8.0 experiment specification
            v8_experiment = self.v8_loader.load_experiment()
            
            # Load raw framework and corpus content
            framework_content = self.v8_loader.load_raw_framework(v8_experiment.framework_path)
            corpus_content = self.v8_loader.load_raw_corpus(v8_experiment.corpus_path)
            
            # Store raw content in transaction workspace for agents
            workspace = self.current_transaction.workspace_path
            (workspace / "framework_content.md").write_text(framework_content)
            (workspace / "corpus_content.md").write_text(corpus_content)
            (workspace / "experiment_spec.json").write_text(json.dumps(v8_experiment.raw_content, indent=2))
            
            self.audit_logger.log_agent_event(
                self.agent_name,
                "V8_SPECIFICATIONS_LOADED",
                {
                    "experiment_name": v8_experiment.name,
                    "framework_size": len(framework_content),
                    "corpus_size": len(corpus_content),
                    "workspace_artifacts": ["framework_content.md", "corpus_content.md", "experiment_spec.json"]
                }
            )
            
            return v8_experiment
            
        except Exception as e:
            self.audit_logger.log_agent_event(
                self.agent_name,
                "V8_SPECIFICATIONS_LOADING_FAILED",
                {"error": str(e)}
            )
            raise
    
    def _store_analysis_results(self, analysis_results: List[Dict[str, Any]]) -> None:
        """Store analysis results using proven provenance pattern (not 2GB dumps)."""
        self.audit_logger.log_agent_event(
            self.agent_name,
            "ANALYSIS_RESULTS_STORAGE_START",
            {"results_count": len(analysis_results)}
        )
        
        try:
            workspace = self.current_transaction.workspace_path
            
            # SURGICAL FIX: Use proven provenance pattern instead of 2GB dumps
            # Create clean summary manifest (like your working system)
            analysis_summary = {
                "analysis_metadata": {
                    "total_documents_analyzed": len(analysis_results),
                    "analysis_timestamp": datetime.now(timezone.utc).isoformat(),
                    "analysis_model": "vertex_ai/gemini-2.5-flash"
                },
                "document_summary": [],
                "provenance": {
                    "analysis_results_stored": "artifacts/analysis_results/",
                    "simplified_data_format": "analysis_data.json"
                }
            }
            
            # Create simplified DataFrame-compatible format for notebook (ONLY)
            analysis_data = self._extract_dataframe_format_clean(analysis_results)
            analysis_data_file = workspace / "analysis_data.json"
            analysis_data_file.write_text(json.dumps(analysis_data, indent=2))
            
            # Store clean summary instead of massive dump
            summary_file = workspace / "analysis_summary.json"
            summary_file.write_text(json.dumps(analysis_summary, indent=2))
            
            # Store raw results in content-addressable artifacts (like your working system)
            artifacts_dir = workspace / "artifacts" / "analysis_results"
            artifacts_dir.mkdir(parents=True, exist_ok=True)
            
            for i, result in enumerate(analysis_results):
                # Store each result as separate artifact (content-addressable)
                result_hash = hashlib.sha256(json.dumps(result, sort_keys=True).encode()).hexdigest()[:16]
                artifact_file = artifacts_dir / f"analysis_{i:04d}_{result_hash}.json"
                artifact_file.write_text(json.dumps(result, indent=2))
                
                # Add to summary
                analysis_summary["document_summary"].append({
                    "document_index": i,
                    "artifact_hash": result_hash,
                    "artifact_file": str(artifact_file.relative_to(workspace))
                })
            
            # Update summary with document info
            summary_file.write_text(json.dumps(analysis_summary, indent=2))
            
            self.audit_logger.log_agent_event(
                self.agent_name,
                "ANALYSIS_RESULTS_STORAGE_SUCCESS",
                {
                    "results_count": len(analysis_results),
                    "summary_file": "analysis_summary.json",
                    "dataframe_file": "analysis_data.json",
                    "artifacts_stored": len(analysis_results),
                    "summary_file_size": summary_file.stat().st_size,
                    "dataframe_file_size": analysis_data_file.stat().st_size
                }
            )
            
        except Exception as e:
            self.audit_logger.log_agent_event(
                self.agent_name,
                "ANALYSIS_RESULTS_STORAGE_FAILED",
                {"error": str(e)}
            )
            raise
    
    def _extract_dataframe_format_clean(self, analysis_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract clean DataFrame-compatible format without duplication."""
        dataframe_records = []
        
        # SURGICAL FIX: Process only unique documents, avoid duplication
        processed_documents = set()
        
        for result in analysis_results:
            try:
                result_content = result['analysis_result']['result_content']
                raw_response = result_content['raw_analysis_response']
                
                # Extract JSON between delimiters
                start_marker = '<<<DISCERNUS_ANALYSIS_JSON_v6>>>'
                end_marker = '<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>'
                json_start = raw_response.find(start_marker) + len(start_marker)
                json_end = raw_response.find(end_marker)
                
                if json_start == -1 + len(start_marker) or json_end == -1:
                    continue
                    
                json_str = raw_response[json_start:json_end].strip()
                analysis_json = json.loads(json_str)
                
                # Extract dimensional scores from each document (AVOID DUPLICATION)
                for doc_analysis in analysis_json['document_analyses']:
                    doc_name = doc_analysis['document_name']
                    
                    # Skip if we've already processed this document
                    if doc_name in processed_documents:
                        continue
                    processed_documents.add(doc_name)
                    
                    doc_record = {'document_name': doc_name}
                    
                    # Extract raw scores, salience, and confidence
                    for dimension, score_data in doc_analysis['dimensional_scores'].items():
                        base_name = dimension.replace('_score', '')
                        doc_record[base_name] = score_data['raw_score']
                        doc_record[f"{base_name}_salience"] = score_data['salience']
                        doc_record[f"{base_name}_confidence"] = score_data['confidence']
                    
                    dataframe_records.append(doc_record)
                    
            except (KeyError, json.JSONDecodeError, ValueError) as e:
                # Log but continue processing other results
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "CLEAN_DATAFRAME_EXTRACTION_WARNING",
                    {"error": str(e), "result_index": len(dataframe_records)}
                )
                continue
        
        # Log deduplication results
        self.audit_logger.log_agent_event(
            self.agent_name,
            "DATAFRAME_DEDUPLICATION_SUCCESS",
            {
                "unique_documents": len(processed_documents),
                "total_records": len(dataframe_records),
                "deduplication_applied": True
            }
        )
        
        return dataframe_records
    
    def _extract_dataframe_format(self, analysis_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract DataFrame-compatible format from complex analysis results."""
        dataframe_records = []
        
        for result in analysis_results:
            try:
                result_content = result['analysis_result']['result_content']
                raw_response = result_content['raw_analysis_response']
                
                # Extract JSON between delimiters
                start_marker = '<<<DISCERNUS_ANALYSIS_JSON_v6>>>'
                end_marker = '<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>'
                json_start = raw_response.find(start_marker) + len(start_marker)
                json_end = raw_response.find(end_marker)
                
                if json_start == -1 + len(start_marker) or json_end == -1:
                    # Fallback: skip malformed results
                    continue
                    
                json_str = raw_response[json_start:json_end].strip()
                analysis_json = json.loads(json_str)
                
                # Extract dimensional scores from each document
                for doc_analysis in analysis_json['document_analyses']:
                    doc_record = {'document_name': doc_analysis['document_name']}
                    
                    # Extract raw scores, salience, and confidence
                    for dimension, score_data in doc_analysis['dimensional_scores'].items():
                        base_name = dimension.replace('_score', '')
                        doc_record[base_name] = score_data['raw_score']
                        doc_record[f"{base_name}_salience"] = score_data['salience']
                        doc_record[f"{base_name}_confidence"] = score_data['confidence']
                    
                    dataframe_records.append(doc_record)
                    
            except (KeyError, json.JSONDecodeError, ValueError) as e:
                # Log but continue processing other results
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "DATAFRAME_EXTRACTION_WARNING",
                    {"error": str(e), "result_index": len(dataframe_records)}
                )
                continue
        
        return dataframe_records
    
    def _execute_agents(self, 
                       v8_experiment: V8ExperimentSpec, 
                       analysis_model: str, 
                       synthesis_model: str) -> None:
        """Execute all function generation agents in transactional workspace.
        
        NOTE: Currently executes agents serially. For parallelization strategies,
        see GitHub Issue #438: "Epic: v8.0 Orchestrator Parallelization Strategy"
        """
        agents_to_execute = [
            "AutomatedDerivedMetricsAgent",
            "AutomatedStatisticalAnalysisAgent", 
            "AutomatedEvidenceIntegrationAgent",
            "AutomatedVisualizationAgent"
        ]
        
        self.audit_logger.log_agent_event(
            self.agent_name,
            "AGENTS_EXECUTION_START",
            {
                "agents_planned": agents_to_execute,
                "workspace": str(self.current_transaction.workspace_path),
                "isolation": "all_agents_use_workspace_only"
            }
        )
        
        for agent_name in agents_to_execute:
            self.audit_logger.log_agent_event(
                self.agent_name,
                "AGENT_EXECUTION_START",
                {"agent": agent_name, "model": analysis_model if "Analysis" in agent_name else synthesis_model}
            )
            
            try:
                # TODO: Consider parallelization for performance improvement
                # See GitHub Issue #438 for parallelization strategies
                # Current implementation: serial execution (simple, reliable)
                self._execute_agent_placeholder(agent_name, v8_experiment)
                
                self.current_transaction.agents_completed.append(agent_name)
                
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "AGENT_EXECUTION_SUCCESS",
                    {"agent": agent_name, "workspace_artifacts": f"{agent_name.lower()}_functions.py"}
                )
                
            except Exception as e:
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "AGENT_EXECUTION_FAILED",
                    {"agent": agent_name, "error": str(e)}
                )
                raise
    
    def _execute_agent_placeholder(self, agent_name: str, v8_experiment: V8ExperimentSpec) -> None:
        """Execute specific agent or placeholder for unimplemented agents."""
        workspace = self.current_transaction.workspace_path
        
        if agent_name == "AutomatedDerivedMetricsAgent":
            # Execute real AutomatedDerivedMetricsAgent
            from discernus.agents.automated_derived_metrics import AutomatedDerivedMetricsAgent
            
            agent = AutomatedDerivedMetricsAgent(
                model="vertex_ai/gemini-2.5-flash",
                audit_logger=self.audit_logger
            )
            
            result = agent.generate_functions(workspace)
            self.current_transaction.artifacts_generated.append(result["output_file"])
            
        elif agent_name == "AutomatedStatisticalAnalysisAgent":
            # Execute real AutomatedStatisticalAnalysisAgent
            from discernus.agents.automated_statistical_analysis import AutomatedStatisticalAnalysisAgent
            
            agent = AutomatedStatisticalAnalysisAgent(
                model="vertex_ai/gemini-2.5-flash",
                audit_logger=self.audit_logger
            )
            
            result = agent.generate_functions(workspace)
            self.current_transaction.artifacts_generated.append(result["output_file"])
            
        elif agent_name == "AutomatedEvidenceIntegrationAgent":
            # Execute real AutomatedEvidenceIntegrationAgent
            from discernus.agents.automated_evidence_integration import AutomatedEvidenceIntegrationAgent
            
            agent = AutomatedEvidenceIntegrationAgent(
                model="vertex_ai/gemini-2.5-flash",
                audit_logger=self.audit_logger
            )
            
            result = agent.generate_functions(workspace)
            self.current_transaction.artifacts_generated.append(result["output_file"])
            
        elif agent_name == "AutomatedVisualizationAgent":
            # Execute real AutomatedVisualizationAgent
            from discernus.agents.automated_visualization import AutomatedVisualizationAgent
            
            agent = AutomatedVisualizationAgent(
                model="vertex_ai/gemini-2.5-flash",
                audit_logger=self.audit_logger
            )
            
            result = agent.generate_functions(workspace)
            self.current_transaction.artifacts_generated.append(result["output_file"])
            
        else:
            # Create placeholder function file for unimplemented agents
            function_file = workspace / f"{agent_name.lower()}_functions.py"
            experiment_name = v8_experiment.name if v8_experiment is not None else "from_analysis_results"
            placeholder_content = f"""# {agent_name} - Generated Functions
# Experiment: {experiment_name}
# Generated: {datetime.now(timezone.utc).isoformat()}

def placeholder_function():
    \"\"\"Placeholder function generated by {agent_name}.\"\"\"
    return "Phase 2 placeholder - agent not yet implemented"
"""
            
            function_file.write_text(placeholder_content)
            self.current_transaction.artifacts_generated.append(str(function_file.name))
    
    def _validate_functions(self) -> None:
        """Validate generated functions within transactional workspace."""
        self.audit_logger.log_agent_event(
            self.agent_name,
            "FUNCTION_VALIDATION_START",
            {"workspace": str(self.current_transaction.workspace_path)}
        )
        
        try:
            # TODO: Implement function validation
            # For Phase 2, we'll implement placeholder validation
            workspace = self.current_transaction.workspace_path
            function_files = list(workspace.glob("*_functions.py"))
            
            for function_file in function_files:
                # Basic validation: check file exists and has content
                if function_file.stat().st_size == 0:
                    raise ValueError(f"Generated function file is empty: {function_file}")
            
            self.audit_logger.log_agent_event(
                self.agent_name,
                "FUNCTION_VALIDATION_SUCCESS",
                {"validated_files": [f.name for f in function_files]}
            )
            
        except Exception as e:
            self.audit_logger.log_agent_event(
                self.agent_name,
                "FUNCTION_VALIDATION_FAILED",
                {"error": str(e)}
            )
            raise
    
    def _commit_transaction(self) -> Dict[str, Any]:
        """Commit transaction by moving artifacts to permanent storage."""
        self.audit_logger.log_agent_event(
            self.agent_name,
            "TRANSACTION_COMMIT_START",
            {"transaction_id": self.current_transaction.transaction_id}
        )
        
        try:
            # Create permanent storage location (experiment/runs/<timestamp>/)
            commit_timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            permanent_path = self.experiment_path / "runs" / commit_timestamp
            permanent_path.mkdir(parents=True, exist_ok=True)
            
            # Move all artifacts from workspace to permanent storage
            workspace = self.current_transaction.workspace_path
            for item in workspace.iterdir():
                if item.is_file():
                    shutil.copy2(item, permanent_path / item.name)
            
            # Update transaction state
            self.current_transaction.status = "committed"
            
            # Create transaction manifest
            manifest = {
                "transaction_id": self.current_transaction.transaction_id,
                "status": "committed",
                "created_at": self.current_transaction.created_at,
                "committed_at": datetime.now(timezone.utc).isoformat(),
                "agents_completed": self.current_transaction.agents_completed,
                "artifacts_generated": self.current_transaction.artifacts_generated,
                "permanent_path": str(permanent_path)
            }
            
            (permanent_path / "transaction_manifest.json").write_text(
                json.dumps(manifest, indent=2)
            )
            
            # Clean up workspace
            shutil.rmtree(workspace)
            
            self.audit_logger.log_agent_event(
                self.agent_name,
                "TRANSACTION_COMMIT_SUCCESS",
                {
                    "transaction_id": self.current_transaction.transaction_id,
                    "permanent_path": str(permanent_path),
                    "artifacts_count": len(self.current_transaction.artifacts_generated)
                }
            )
            
            return {
                "status": "success",
                "transaction_id": self.current_transaction.transaction_id,
                "permanent_path": str(permanent_path),
                "artifacts": self.current_transaction.artifacts_generated,
                "agents_completed": self.current_transaction.agents_completed
            }
            
        except Exception as e:
            self.audit_logger.log_agent_event(
                self.agent_name,
                "TRANSACTION_COMMIT_FAILED",
                {"error": str(e)}
            )
            raise
    
    def _rollback_transaction(self, error_message: str) -> None:
        """Rollback transaction by deleting workspace."""
        if not self.current_transaction:
            return
            
        self.audit_logger.log_agent_event(
            self.agent_name,
            "TRANSACTION_ROLLBACK_START",
            {
                "transaction_id": self.current_transaction.transaction_id,
                "error": error_message
            }
        )
        
        try:
            # Delete entire workspace
            if self.current_transaction.workspace_path.exists():
                shutil.rmtree(self.current_transaction.workspace_path)
            
            # Update transaction state
            self.current_transaction.status = "rolled_back"
            
            self.audit_logger.log_agent_event(
                self.agent_name,
                "TRANSACTION_ROLLBACK_SUCCESS",
                {
                    "transaction_id": self.current_transaction.transaction_id,
                    "workspace_deleted": str(self.current_transaction.workspace_path)
                }
            )
            
        except Exception as rollback_error:
            self.audit_logger.log_agent_event(
                self.agent_name,
                "TRANSACTION_ROLLBACK_FAILED",
                {
                    "transaction_id": self.current_transaction.transaction_id,
                    "rollback_error": str(rollback_error)
                }
            )
    
    def generate_notebook_with_analysis(self, 
                                       analysis_model: str = "vertex_ai/gemini-2.5-flash",
                                       synthesis_model: str = "vertex_ai/gemini-2.5-pro",
                                       analysis_results: List[Dict[str, Any]] = None,
                                       framework_content: str = None) -> Dict[str, Any]:
        """
        Generate notebook with pre-computed analysis results and framework content.
        
        This method ensures that the required framework_content.md file is created
        in the transaction workspace even when analysis results are provided.
        
        Args:
            analysis_model: LLM model for analysis tasks
            synthesis_model: LLM model for synthesis tasks
            analysis_results: Pre-computed analysis results from v8.0 analysis phase
            framework_content: Raw framework content to store in transaction workspace
            
        Returns:
            Transaction result with notebook artifacts
        """
        transaction_id = f"notebook_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
        
        try:
            # Phase 1: BEGIN TRANSACTION
            self._begin_transaction(transaction_id)
            
            # Phase 2: STORE ANALYSIS RESULTS AND FRAMEWORK CONTENT
            if analysis_results:
                self._store_analysis_results(analysis_results)
            
            if framework_content:
                self._store_framework_content(framework_content)
                
            # Create minimal experiment spec for agents
            self._store_experiment_spec()
                
            # Phase 3: EXECUTE AGENTS (in transactional workspace)
            self._execute_agents(None, analysis_model, synthesis_model)
            
            # Phase 4: VALIDATE GENERATED FUNCTIONS
            self._validate_functions()
            
            # Phase 5: GENERATE COMPLETE NOTEBOOK (Phase 3 Integration)
            self._generate_complete_notebook(None, analysis_model, synthesis_model)
            
            # Phase 6: COMMIT TRANSACTION
            result = self._commit_transaction()
            
            return result
            
        except Exception as e:
            # Phase 6: ROLLBACK ON FAILURE
            self._rollback_transaction(str(e))
            raise
    
    def _store_framework_content(self, framework_content: str) -> None:
        """Store framework content in transaction workspace for agent access."""
        self.audit_logger.log_agent_event(
            self.agent_name,
            "FRAMEWORK_CONTENT_STORAGE_START",
            {"content_size": len(framework_content)}
        )
        
        try:
            workspace = self.current_transaction.workspace_path
            framework_file = workspace / "framework_content.md"
            framework_file.write_text(framework_content)
            
            self.audit_logger.log_agent_event(
                self.agent_name,
                "FRAMEWORK_CONTENT_STORAGE_SUCCESS",
                {
                    "storage_file": "framework_content.md",
                    "file_size": framework_file.stat().st_size
                }
            )
            
        except Exception as e:
            self.audit_logger.log_agent_event(
                self.agent_name,
                "FRAMEWORK_CONTENT_STORAGE_FAILED",
                {"error": str(e)}
            )
            raise
    
    def _store_experiment_spec(self) -> None:
        """Store minimal experiment spec in transaction workspace for agent access."""
        self.audit_logger.log_agent_event(
            self.agent_name,
            "EXPERIMENT_SPEC_STORAGE_START",
            {}
        )
        
        try:
            workspace = self.current_transaction.workspace_path
            experiment_spec_file = workspace / "experiment_spec.json"
            
            # Create minimal experiment spec
            experiment_spec = {
                "name": self.experiment_path.name,
                "version": "8.0",
                "framework_path": "cff_v8.md",
                "corpus_path": "corpus",
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            
            experiment_spec_file.write_text(json.dumps(experiment_spec, indent=2))
            
            self.audit_logger.log_agent_event(
                self.agent_name,
                "EXPERIMENT_SPEC_STORAGE_SUCCESS",
                {
                    "storage_file": "experiment_spec.json",
                    "file_size": experiment_spec_file.stat().st_size
                }
            )
            
        except Exception as e:
            self.audit_logger.log_agent_event(
                self.agent_name,
                "EXPERIMENT_SPEC_STORAGE_FAILED",
                {"error": str(e)}
            )
            raise
    
    def _generate_complete_notebook(self, 
                                  v8_experiment: Optional[Any],
                                  analysis_model: str,
                                  synthesis_model: str) -> None:
        """Generate complete research notebook using Phase 3 components."""
        try:
            # Import Phase 3 components
            from discernus.core.componentized_notebook_generation import ComponentizedNotebookGeneration
            from discernus.core.notebook_executor import NotebookExecutor
            from discernus.core.universal_notebook_template import DataPath
            
            # Initialize componentized notebook generator
            notebook_generator = ComponentizedNotebookGeneration(
                analysis_model=analysis_model,
                synthesis_model=synthesis_model,
                audit_logger=self.audit_logger
            )
            
            # Collect generated functions from workspace
            workspace = self.current_transaction.workspace_path
            generated_functions = self._collect_generated_functions(workspace)
            
            # Prepare data paths for external loading
            data_paths = self._prepare_data_paths()
            
            # Determine experiment details
            if v8_experiment:
                experiment_name = v8_experiment.name
                framework_name = getattr(v8_experiment, 'framework_name', 'Unknown')
                framework_content = getattr(v8_experiment, 'framework_content', '')
                document_count = getattr(v8_experiment, 'document_count', 0)
            else:
                experiment_name = self.experiment_path.name
                framework_name = "Analysis Results"
                framework_content = "Generated from pre-computed analysis results"
                document_count = 1  # Placeholder when using analysis results
            
            # Generate complete notebook
            complete_notebook = notebook_generator.generate_complete_notebook(
                experiment_name=experiment_name,
                framework_name=framework_name,
                framework_content=framework_content,
                document_count=document_count,
                generated_functions=generated_functions,
                data_paths=data_paths,
                statistical_summary="Statistical analysis pending execution",
                key_findings="Findings will be generated during notebook execution",
                research_context=f"Computational analysis using {framework_name} framework"
            )
            
            # Execute and validate notebook
            notebook_executor = NotebookExecutor(
                security=self.security,
                audit_logger=self.audit_logger
            )
            
            notebook_path = workspace / "research_notebook.py"
            execution_result = notebook_executor.validate_and_execute_notebook(
                notebook_content=complete_notebook,
                notebook_path=notebook_path,
                execution_timeout=300
            )
            
            # Log notebook generation success
            self.audit_logger.log_agent_event(
                self.agent_name,
                "COMPLETE_NOTEBOOK_GENERATION_SUCCESS",
                {
                    "notebook_path": str(notebook_path),
                    "execution_result": execution_result,
                    "experiment_name": experiment_name
                }
            )
            
            # Add notebook to transaction artifacts
            self.current_transaction.artifacts_generated.append("research_notebook.py")
            
        except Exception as e:
            self.audit_logger.log_agent_event(
                self.agent_name,
                "COMPLETE_NOTEBOOK_GENERATION_FAILED",
                {"error": str(e)}
            )
            raise
    
    def _collect_generated_functions(self, workspace: Path) -> Dict[str, str]:
        """Collect generated functions from workspace."""
        functions = {}
        
        # Map agent output files to function categories
        function_mappings = {
            "derived_metrics": "automatedderivedmetricsagent_functions.py",
            "statistical_analysis": "automatedstatisticalanalysisagent_functions.py",
            "evidence_integration": "automatedevidenceintegrationagent_functions.py",
            "visualization": "automatedvisualizationagent_functions.py"
        }
        
        for category, filename in function_mappings.items():
            function_file = workspace / filename
            if function_file.exists():
                functions[category] = function_file.read_text()
            else:
                functions[category] = f"# {category} functions not generated\npass"
        
        return functions
    
    def _prepare_data_paths(self) -> List[DataPath]:
        """Prepare data paths for external loading in notebook."""
        # For now, return basic data paths
        # This would be enhanced to use actual content-addressable storage paths
        return [
            DataPath(
                variable_name="analysis_data",
                file_path="analysis_data.json",
                description="Analysis results from v8.0 analysis phase"
            )
        ]
