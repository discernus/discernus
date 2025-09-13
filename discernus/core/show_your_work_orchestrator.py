#!/usr/bin/env python3
"""
Show Your Work Orchestrator
===========================

This orchestrator manages the complete "Show Your Work" workflow, implementing
the new architecture with tool-calling, adversarial verification, and fail-fast behavior.

Key Features:
- Per-document analysis with derived metrics calculation
- Adversarial verification of all calculations
- Batch statistical analysis with verification
- Evidence CSV generation
- Fail-fast error handling
- Content-addressable storage
- Comprehensive audit logging
"""

import json
import hashlib
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.experiment_state_manager import ExperimentStateManager
from discernus.core.error_reporter import ErrorReporter
from discernus.core.cache_manager import CacheManager
from discernus.core.progress_manager import ProgressManager
from discernus.gateway.model_registry import ModelRegistry
from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway

# Import agents
from discernus.agents.EnhancedAnalysisAgent.agent_multi_tool import EnhancedAnalysisAgentMultiTool
from discernus.agents.verification_agent.agent import VerificationAgent
from discernus.agents.statistical_planning_execution.agent import StatisticalPlanningExecutionAgent
from discernus.agents.statistical_verification.agent import StatisticalVerificationAgent
from discernus.core.evidence_csv_export import EvidenceCSVExportModule


class ShowYourWorkOrchestrator:
    """Orchestrator for the Show Your Work architecture"""
    
    def __init__(self, 
                 experiment_path: Path,
                 run_name: Optional[str] = None,
                 enable_verification: bool = True,
                 enable_caching: bool = True):
        """
        Initialize the Show Your Work Orchestrator
        
        Args:
            experiment_path: Path to the experiment directory
            run_name: Optional explicit run name (defaults to timestamp)
            enable_verification: Whether to enable adversarial verification
            enable_caching: Whether to enable artifact caching
        """
        self.experiment_path = Path(experiment_path)
        self.run_name = run_name or f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.enable_verification = enable_verification
        self.enable_caching = enable_caching
        
        # Setup logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(f"ShowYourWorkOrchestrator.{self.run_name}")
        self.logger.info(f"Initializing orchestrator for experiment: {self.experiment_path}")
        
        # Initialize core components
        self.security = ExperimentSecurityBoundary(experiment_path=self.experiment_path)
        self.audit = AuditLogger(self.security, self.experiment_path)
        self.run_folder = self.experiment_path / self.run_name
        self.run_folder.mkdir(exist_ok=True)
        self.storage = LocalArtifactStorage(self.security, self.run_folder)
        self.state_manager = ExperimentStateManager(self.run_folder)
        self.error_reporter = ErrorReporter(self.run_folder)
        self.cache_manager = CacheManager(self.storage) if enable_caching else None
        self.progress = ProgressManager()
        
        # Initialize agents (will be properly initialized in execute_experiment)
        self.analysis_agent = None
        self.verification_agent = VerificationAgent(
            self.security, self.audit, self.storage
        ) if enable_verification else None
        self.statistical_agent = StatisticalPlanningExecutionAgent(
            self.security, self.audit, self.storage
        )
        self.statistical_verification_agent = StatisticalVerificationAgent(
            self.security, self.audit, self.storage
        ) if enable_verification else None
        self.evidence_csv_module = EvidenceCSVExportModule(self.storage)
        
        # Initialize model registry
        self.model_registry = ModelRegistry()
        
        self.audit.log_orchestrator_event("initialization", {
            "experiment_path": str(self.experiment_path),
            "run_name": self.run_name,
            "enable_verification": enable_verification,
            "enable_caching": enable_caching,
            "architecture": "show_your_work"
        })
    
    def execute_experiment(self, 
                          framework_path: Path,
                          corpus_path: Path,
                          analysis_model: str = "vertex_ai/gemini-2.5-flash",
                          statistical_model: str = "vertex_ai/gemini-2.5-pro") -> Dict[str, Any]:
        """
        Execute a complete experiment using the Show Your Work architecture
        
        Args:
            framework_path: Path to the framework specification
            corpus_path: Path to the corpus directory
            analysis_model: Model to use for analysis
            statistical_model: Model to use for statistical analysis
            
        Returns:
            Dictionary containing experiment results and metadata
        """
        start_time = datetime.now(timezone.utc)
        self.logger.info(f"Starting experiment execution")
        self.logger.info(f"  Framework: {framework_path}")
        self.logger.info(f"  Corpus: {corpus_path}")
        self.logger.info(f"  Analysis model: {analysis_model}")
        self.logger.info(f"  Statistical model: {statistical_model}")
        
        try:
            # Initialize analysis agent with the specified model
            self.logger.info("Initializing analysis agent...")
            self.analysis_agent = EnhancedAnalysisAgentMultiTool(
                self.security, self.audit, self.storage,
                llm_gateway=EnhancedLLMGateway(self.model_registry),
                model=analysis_model
            )
            self.logger.info("Analysis agent initialized successfully")
            
            self.audit.log_orchestrator_event("experiment_start", {
                "framework_path": str(framework_path),
                "corpus_path": str(corpus_path),
                "analysis_model": analysis_model,
                "statistical_model": statistical_model
            })
            
            # Phase 1: Per-document analysis with verification
            self.logger.info("Starting Phase 1: Analysis phase")
            analysis_results = self._execute_analysis_phase(
                framework_path, corpus_path, analysis_model
            )
            
            if not analysis_results["success"]:
                self.logger.error("Analysis phase failed")
                return self._handle_experiment_failure("analysis_phase_failed", analysis_results)
            
            self.logger.info(f"Analysis phase completed successfully. Artifacts: {len(analysis_results['artifacts'])}")
            
            # Phase 2: Statistical analysis with verification
            self.logger.info("Starting Phase 2: Statistical phase")
            statistical_results = self._execute_statistical_phase(
                analysis_results["artifacts"], statistical_model
            )
            
            if not statistical_results["success"]:
                self.logger.error("Statistical phase failed")
                return self._handle_experiment_failure("statistical_phase_failed", statistical_results)
            
            self.logger.info(f"Statistical phase completed successfully. Artifacts: {len(statistical_results['artifacts'])}")
            
            # Phase 3: Evidence CSV generation
            self.logger.info("Starting Phase 3: Evidence phase")
            evidence_results = self._execute_evidence_phase(analysis_results["artifacts"])
            
            if not evidence_results["success"]:
                self.logger.error("Evidence phase failed")
                return self._handle_experiment_failure("evidence_phase_failed", evidence_results)
            
            self.logger.info(f"Evidence phase completed successfully. Artifacts: {len(evidence_results['artifacts'])}")
            
            # Compile final results
            end_time = datetime.now(timezone.utc)
            duration = (end_time - start_time).total_seconds()
            
            final_results = {
                "success": True,
                "experiment_id": self.run_name,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "duration_seconds": duration,
                "analysis_results": analysis_results,
                "statistical_results": statistical_results,
                "evidence_results": evidence_results,
                "artifacts": {
                    "analysis_artifacts": analysis_results["artifacts"],
                    "statistical_artifacts": statistical_results["artifacts"],
                    "evidence_artifacts": evidence_results["artifacts"]
                }
            }
            
            # Save final state
            self.state_manager.save_final_state(final_results)
            
            self.audit.log_orchestrator_event("experiment_complete", {
                "duration_seconds": duration,
                "total_artifacts": len(analysis_results["artifacts"]) + 
                                 len(statistical_results["artifacts"]) + 
                                 len(evidence_results["artifacts"]),
                "verification_enabled": self.enable_verification
            })
            
            return final_results
            
        except Exception as e:
            return self._handle_experiment_failure("orchestrator_error", {
                "error": str(e),
                "error_type": type(e).__name__
            })
    
    def _execute_analysis_phase(self, 
                               framework_path: Path, 
                               corpus_path: Path, 
                               model: str) -> Dict[str, Any]:
        """Execute the per-document analysis phase with verification"""
        
        self.logger.info("Executing analysis phase")
        self.audit.log_orchestrator_event("analysis_phase_start", {
            "framework_path": str(framework_path),
            "corpus_path": str(corpus_path),
            "model": model
        })
        
        # Load framework and corpus
        self.logger.info("Loading framework and corpus...")
        framework_content = self._load_framework(framework_path)
        corpus_documents = self._load_corpus(corpus_path)
        self.logger.info(f"Loaded {len(corpus_documents)} documents from corpus")
        
        analysis_artifacts = []
        verification_artifacts = []
        
        # Process each document
        for i, document in enumerate(corpus_documents):
            try:
                self.logger.info(f"Processing document {i+1}/{len(corpus_documents)}: {document['name']}")
                self.progress.update_progress("analysis", i, len(corpus_documents), f"Processing {document['name']}")
                
                # Analyze document
                self.logger.info(f"Calling analysis agent for {document['name']}...")
                analysis_result = self.analysis_agent.analyze_document(
                    document_content=document["content"],
                    framework_content=framework_content,
                    document_id=document["name"]
                )
                self.logger.info(f"Analysis result for {document['name']}: success={analysis_result.get('success', False)}")
                
                if not analysis_result["success"]:
                    raise Exception(f"Analysis failed for {document['name']}: {analysis_result.get('error')}")
                
                # Collect artifacts from multi-tool analysis
                document_artifacts = [
                    analysis_result["scores_artifact"],
                    analysis_result["evidence_artifact"],
                    analysis_result["work_artifact"]
                ]
                analysis_artifacts.extend([a for a in document_artifacts if a is not None])
                
                # Verify analysis if verification is enabled
                if self.enable_verification and self.verification_agent and analysis_result["work_artifact"]:
                    verification_result = self.verification_agent.verify_analysis(
                        analysis_artifact_id=analysis_result["scores_artifact"],
                        work_artifact_id=analysis_result["work_artifact"],
                        model=None  # Auto-select verifier model
                    )
                    
                    if not verification_result["success"]:
                        raise Exception(f"Verification failed for {document['name']}: {verification_result.get('reasoning')}")
                    
                    verification_artifacts.append(verification_result["attestation_artifact"])
                
            except Exception as e:
                error_details = self.error_reporter.create_error_report(
                    phase="analysis",
                    document_name=document["name"],
                    error=str(e),
                    context={"framework_path": str(framework_path), "model": model}
                )
                raise Exception(f"Analysis phase failed: {error_details}")
        
        self.audit.log_orchestrator_event("analysis_phase_complete", {
            "documents_processed": len(corpus_documents),
            "analysis_artifacts": len(analysis_artifacts),
            "verification_artifacts": len(verification_artifacts)
        })
        
        return {
            "success": True,
            "artifacts": analysis_artifacts + verification_artifacts,
            "documents_processed": len(corpus_documents)
        }
    
    def _execute_statistical_phase(self, 
                                  analysis_artifacts: List[str], 
                                  model: str) -> Dict[str, Any]:
        """Execute the statistical analysis phase with verification"""
        
        self.logger.info(f"Executing statistical phase with {len(analysis_artifacts)} analysis artifacts")
        self.audit.log_orchestrator_event("statistical_phase_start", {
            "analysis_artifacts_count": len(analysis_artifacts),
            "model": model
        })
        
        try:
            # Execute statistical analysis
            self.logger.info("Calling statistical agent...")
            statistical_result = self.statistical_agent.execute_statistical_analysis(
                analysis_artifacts=analysis_artifacts,
                model=model
            )
            self.logger.info(f"Statistical analysis result: success={statistical_result.get('success', False)}")
            
            if not statistical_result["success"]:
                raise Exception(f"Statistical analysis failed: {statistical_result.get('error')}")
            
            # Extract artifacts from the result
            statistical_artifacts = [
                statistical_result["statistics_artifact"],
                statistical_result["work_artifact"], 
                statistical_result["csv_artifact"]
            ]
            
            # Verify statistical analysis if verification is enabled
            if self.enable_verification and self.statistical_verification_agent:
                verification_result = self.statistical_verification_agent.verify_statistical_analysis(
                    statistics_artifact_id=statistical_artifacts[0],  # statistics.json
                    work_artifact_id=statistical_artifacts[1],        # work.json
                    csv_artifact_id=statistical_artifacts[2],         # csv data
                    model=None  # Auto-select verifier model
                )
                
                if not verification_result["success"]:
                    raise Exception(f"Statistical verification failed: {verification_result.get('reasoning')}")
                
                statistical_artifacts.append(verification_result["attestation_artifact"])
            
            self.audit.log_orchestrator_event("statistical_phase_complete", {
                "statistical_artifacts": len(statistical_artifacts)
            })
            
            return {
                "success": True,
                "artifacts": statistical_artifacts
            }
            
        except Exception as e:
            self.logger.error(f"Statistical phase failed: {e}")
            error_details = self.error_reporter.create_error_report(
                phase="statistical",
                error=str(e),
                context={"analysis_artifacts_count": len(analysis_artifacts), "model": model}
            )
            raise Exception(f"Statistical phase failed: {error_details}")
    
    def _execute_evidence_phase(self, analysis_artifacts: List[str]) -> Dict[str, Any]:
        """Execute the evidence CSV generation phase"""
        
        self.audit.log_orchestrator_event("evidence_phase_start", {
            "analysis_artifacts_count": len(analysis_artifacts)
        })
        
        try:
            # Generate evidence CSV
            evidence_result = self.evidence_csv_module.generate_evidence_csv(
                analysis_artifacts=analysis_artifacts
            )
            
            if not evidence_result["success"]:
                raise Exception(f"Evidence CSV generation failed: {evidence_result.get('error')}")
            
            self.audit.log_orchestrator_event("evidence_phase_complete", {
                "evidence_artifacts": len(evidence_result["artifacts"])
            })
            
            return {
                "success": True,
                "artifacts": evidence_result["artifacts"]
            }
            
        except Exception as e:
            error_details = self.error_reporter.create_error_report(
                phase="evidence",
                error=str(e),
                context={"analysis_artifacts_count": len(analysis_artifacts)}
            )
            raise Exception(f"Evidence phase failed: {error_details}")
    
    def _load_framework(self, framework_path: Path) -> str:
        """Load framework content"""
        try:
            with open(framework_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise Exception(f"Failed to load framework from {framework_path}: {e}")
    
    def _load_corpus(self, corpus_path: Path) -> List[Dict[str, Any]]:
        """Load corpus documents"""
        documents = []
        
        try:
            if corpus_path.is_file():
                # Single file
                with open(corpus_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                documents.append({
                    "name": corpus_path.name,
                    "content": content
                })
            elif corpus_path.is_dir():
                # Directory of files
                for file_path in corpus_path.glob("*.txt"):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    documents.append({
                        "name": file_path.name,
                        "content": content
                    })
            else:
                raise Exception(f"Corpus path does not exist: {corpus_path}")
                
        except Exception as e:
            raise Exception(f"Failed to load corpus from {corpus_path}: {e}")
        
        if not documents:
            raise Exception(f"No documents found in corpus: {corpus_path}")
        
        return documents
    
    def _handle_experiment_failure(self, failure_type: str, details: Dict[str, Any]) -> Dict[str, Any]:
        """Handle experiment failure with detailed error reporting"""
        
        error_report = self.error_reporter.create_error_report(
            phase=failure_type,
            error=details.get("error", "Unknown error"),
            context=details
        )
        
        self.audit.log_orchestrator_event("experiment_failure", {
            "failure_type": failure_type,
            "error_report": error_report,
            "details": details
        })
        
        return {
            "success": False,
            "failure_type": failure_type,
            "error_report": error_report,
            "details": details,
            "experiment_id": self.run_name
        }
    
    def get_experiment_status(self) -> Dict[str, Any]:
        """Get current experiment status"""
        return self.state_manager.get_current_status()
    
    def resume_experiment(self) -> Dict[str, Any]:
        """Resume a failed or interrupted experiment"""
        return self.state_manager.resume_experiment()
