"""
Comprehensive Experiment Logging System for Narrative Gravity Analysis
Phase 5: Integration, Testing & Comprehensive Logging

Extends existing logging infrastructure with research-specific capabilities:
- Academic audit trails for institutional compliance
- Experiment lifecycle tracking with hypothesis validation
- Corpus management logging with integrity validation
- Context propagation quality assurance
- Research ethics and reproducibility tracking
"""

import json
import time
import traceback
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
from dataclasses import dataclass, field

from .logging_config import StructuredLogger, MetricsCollector, ErrorCodes

class ExperimentErrorCodes(ErrorCodes):
    """Extended error codes for experiment orchestrator (E6000-E6999)"""
    
    # Experiment Definition Errors (E6000-E6099)
    EXPERIMENT_DEFINITION_INVALID = "E6001"
    EXPERIMENT_SCHEMA_VALIDATION_FAILED = "E6002"
    EXPERIMENT_MISSING_REQUIRED_FIELDS = "E6003"
    EXPERIMENT_INVALID_HYPOTHESIS_FORMAT = "E6004"
    EXPERIMENT_CONTEXT_CREATION_FAILED = "E6005"
    
    # Component Registration Errors (E6100-E6199)
    COMPONENT_FRAMEWORK_REGISTRATION_FAILED = "E6101"
    COMPONENT_PROMPT_REGISTRATION_FAILED = "E6102"
    COMPONENT_WEIGHTING_REGISTRATION_FAILED = "E6103"
    COMPONENT_CORPUS_REGISTRATION_FAILED = "E6104"
    COMPONENT_AUTO_REGISTRATION_FAILED = "E6105"
    COMPONENT_VALIDATION_FAILED = "E6106"
    
    # Corpus Management Errors (E6200-E6299)
    CORPUS_HASH_VALIDATION_FAILED = "E6201"
    CORPUS_FILE_NOT_FOUND = "E6202"
    CORPUS_INTEGRITY_CHECK_FAILED = "E6203"
    CORPUS_MANIFEST_GENERATION_FAILED = "E6204"
    CORPUS_COLLECTION_VALIDATION_FAILED = "E6205"
    CORPUS_AUTO_REGISTRATION_FAILED = "E6206"
    
    # Context Propagation Errors (E6300-E6399)
    CONTEXT_ENRICHMENT_FAILED = "E6301"
    CONTEXT_PROMPT_MODIFICATION_FAILED = "E6302"
    CONTEXT_METADATA_PROPAGATION_FAILED = "E6303"
    CONTEXT_HYPOTHESIS_INTEGRATION_FAILED = "E6304"
    CONTEXT_VALIDATION_REPORT_FAILED = "E6305"
    
    # Execution & Analysis Errors (E6400-E6499)
    EXECUTION_PRE_FLIGHT_FAILED = "E6401"
    EXECUTION_EXPERIMENT_FAILED = "E6402"
    EXECUTION_PIPELINE_INTERRUPTED = "E6403"
    EXECUTION_QUALITY_VALIDATION_FAILED = "E6404"
    
    # Academic Compliance Errors (E6500-E6599)
    ACADEMIC_ETHICS_CLEARANCE_MISSING = "E6501"
    ACADEMIC_PI_AUTHORIZATION_FAILED = "E6502"
    ACADEMIC_INSTITUTIONAL_COMPLIANCE_FAILED = "E6503"
    ACADEMIC_AUDIT_TRAIL_INCOMPLETE = "E6504"
    ACADEMIC_REPRODUCIBILITY_VALIDATION_FAILED = "E6505"

@dataclass
class ExperimentRunMetrics:
    """Metrics for experiment execution tracking"""
    experiment_id: str
    run_id: str
    start_time: str
    end_time: Optional[str] = None
    duration_seconds: Optional[float] = None
    components_validated: int = 0
    components_auto_registered: int = 0
    corpus_files_processed: int = 0
    analysis_requests: int = 0
    api_cost_total: float = 0.0
    success: bool = False
    error_count: int = 0
    warning_count: int = 0
    context_propagations: int = 0
    hypothesis_validations: int = 0

@dataclass
class AcademicAuditTrail:
    """Academic compliance and audit trail information"""
    experiment_id: str
    principal_investigator: Optional[str] = None
    institution: Optional[str] = None
    ethical_clearance: Optional[str] = None
    funding_source: Optional[str] = None
    research_protocol: Optional[str] = None
    data_classification: str = "unclassified"
    retention_period: Optional[str] = None
    publication_intent: bool = False
    reproducibility_package: Dict[str, Any] = field(default_factory=dict)
    compliance_checks: List[str] = field(default_factory=list)

class ExperimentMetricsCollector(MetricsCollector):
    """Extended metrics collector for experiment orchestrator"""
    
    def __init__(self):
        super().__init__()
        # Add experiment-specific metrics
        self.metrics["experiment_orchestrator"] = {
            "total_experiments": 0,
            "successful_experiments": 0,
            "failed_experiments": 0,
            "total_components_validated": 0,
            "auto_registrations_attempted": 0,
            "auto_registrations_successful": 0,
            "corpus_files_processed": 0,
            "context_propagations": 0,
            "hypothesis_validations": 0,
            "academic_compliance_checks": 0,
            "integrity_validations": 0
        }
        
        # Track current experiment runs
        self.active_experiments: Dict[str, ExperimentRunMetrics] = {}
        self.academic_trails: Dict[str, AcademicAuditTrail] = {}
    
    def start_experiment(self, experiment_id: str, run_id: str, academic_info: Dict[str, Any] = None) -> str:
        """Start tracking an experiment run"""
        start_time = datetime.now(timezone.utc).isoformat()
        
        metrics = ExperimentRunMetrics(
            experiment_id=experiment_id,
            run_id=run_id,
            start_time=start_time
        )
        
        self.active_experiments[run_id] = metrics
        
        # Create academic audit trail if provided
        if academic_info:
            audit_trail = AcademicAuditTrail(
                experiment_id=experiment_id,
                principal_investigator=academic_info.get('principal_investigator'),
                institution=academic_info.get('institution'),
                ethical_clearance=academic_info.get('ethical_clearance'),
                funding_source=academic_info.get('funding_source'),
                research_protocol=academic_info.get('research_protocol'),
                data_classification=academic_info.get('data_classification', 'unclassified'),
                retention_period=academic_info.get('retention_period'),
                publication_intent=academic_info.get('publication_intent', False)
            )
            self.academic_trails[run_id] = audit_trail
        
        self.metrics["experiment_orchestrator"]["total_experiments"] += 1
        return run_id
    
    def end_experiment(self, run_id: str, success: bool = True):
        """End tracking an experiment run"""
        if run_id not in self.active_experiments:
            return
        
        metrics = self.active_experiments[run_id]
        end_time = datetime.now(timezone.utc).isoformat()
        start_dt = datetime.fromisoformat(metrics.start_time.replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        
        metrics.end_time = end_time
        metrics.duration_seconds = (end_dt - start_dt).total_seconds()
        metrics.success = success
        
        if success:
            self.metrics["experiment_orchestrator"]["successful_experiments"] += 1
        else:
            self.metrics["experiment_orchestrator"]["failed_experiments"] += 1
    
    def record_component_validation(self, run_id: str, component_type: str, success: bool):
        """Record component validation event"""
        if run_id in self.active_experiments:
            self.active_experiments[run_id].components_validated += 1
        self.metrics["experiment_orchestrator"]["total_components_validated"] += 1
    
    def record_auto_registration(self, run_id: str, component_type: str, success: bool):
        """Record auto-registration event"""
        if run_id in self.active_experiments:
            self.active_experiments[run_id].components_auto_registered += 1
        
        self.metrics["experiment_orchestrator"]["auto_registrations_attempted"] += 1
        if success:
            self.metrics["experiment_orchestrator"]["auto_registrations_successful"] += 1
    
    def record_corpus_processing(self, run_id: str, files_count: int, success: bool):
        """Record corpus processing event"""
        if run_id in self.active_experiments:
            self.active_experiments[run_id].corpus_files_processed += files_count
        self.metrics["experiment_orchestrator"]["corpus_files_processed"] += files_count
    
    def record_context_propagation(self, run_id: str, success: bool):
        """Record context propagation event"""
        if run_id in self.active_experiments:
            self.active_experiments[run_id].context_propagations += 1
        self.metrics["experiment_orchestrator"]["context_propagations"] += 1
    
    def record_hypothesis_validation(self, run_id: str, hypothesis_count: int):
        """Record hypothesis validation event"""
        if run_id in self.active_experiments:
            self.active_experiments[run_id].hypothesis_validations += hypothesis_count
        self.metrics["experiment_orchestrator"]["hypothesis_validations"] += hypothesis_count
    
    def record_academic_compliance_check(self, run_id: str, check_type: str, result: bool):
        """Record academic compliance check"""
        if run_id in self.academic_trails:
            self.academic_trails[run_id].compliance_checks.append(
                f"{check_type}: {'PASS' if result else 'FAIL'}"
            )
        self.metrics["experiment_orchestrator"]["academic_compliance_checks"] += 1
    
    def get_experiment_summary(self, run_id: str) -> Dict[str, Any]:
        """Get comprehensive experiment run summary"""
        if run_id not in self.active_experiments:
            return {}
        
        metrics = self.active_experiments[run_id]
        audit_trail = self.academic_trails.get(run_id)
        
        summary = {
            "experiment_metrics": {
                "experiment_id": metrics.experiment_id,
                "run_id": metrics.run_id,
                "start_time": metrics.start_time,
                "end_time": metrics.end_time,
                "duration_seconds": metrics.duration_seconds,
                "success": metrics.success,
                "components_validated": metrics.components_validated,
                "components_auto_registered": metrics.components_auto_registered,
                "corpus_files_processed": metrics.corpus_files_processed,
                "context_propagations": metrics.context_propagations,
                "hypothesis_validations": metrics.hypothesis_validations,
                "api_cost_total": metrics.api_cost_total,
                "error_count": metrics.error_count,
                "warning_count": metrics.warning_count
            }
        }
        
        if audit_trail:
            summary["academic_audit_trail"] = {
                "principal_investigator": audit_trail.principal_investigator,
                "institution": audit_trail.institution,
                "ethical_clearance": audit_trail.ethical_clearance,
                "funding_source": audit_trail.funding_source,
                "data_classification": audit_trail.data_classification,
                "publication_intent": audit_trail.publication_intent,
                "compliance_checks": audit_trail.compliance_checks,
                "reproducibility_package": audit_trail.reproducibility_package
            }
        
        return summary

class ExperimentLogger(StructuredLogger):
    """Research-specific structured logger for experiment orchestrator"""
    
    def __init__(self, name: str, experiment_metrics: ExperimentMetricsCollector = None):
        super().__init__(name)
        self.metrics = experiment_metrics or ExperimentMetricsCollector()
        self.current_run_id: Optional[str] = None
    
    def start_experiment_logging(self, experiment_id: str, experiment_context: Dict[str, Any] = None, 
                                academic_info: Dict[str, Any] = None) -> str:
        """Start experiment-scoped logging"""
        run_id = f"{experiment_id}_{int(time.time())}"
        self.current_run_id = run_id
        
        self.metrics.start_experiment(experiment_id, run_id, academic_info)
        
        self.info("Experiment started", extra_data={
            "experiment_id": experiment_id,
            "run_id": run_id,
            "experiment_context": experiment_context,
            "academic_info": academic_info
        })
        
        return run_id
    
    def end_experiment_logging(self, success: bool = True):
        """End experiment-scoped logging"""
        if not self.current_run_id:
            return
        
        self.metrics.end_experiment(self.current_run_id, success)
        
        summary = self.metrics.get_experiment_summary(self.current_run_id)
        
        self.info("Experiment completed", extra_data={
            "run_id": self.current_run_id,
            "success": success,
            "experiment_summary": summary
        })
        
        self.current_run_id = None
    
    def log_component_validation(self, component_type: str, component_id: str, 
                               success: bool, validation_details: Dict[str, Any] = None):
        """Log component validation with research context"""
        self.metrics.record_component_validation(self.current_run_id, component_type, success)
        
        if success:
            self.info(f"Component validation successful: {component_type}:{component_id}", 
                     extra_data={
                         "component_type": component_type,
                         "component_id": component_id,
                         "validation_details": validation_details,
                         "run_id": self.current_run_id
                     })
        else:
            self.error(f"Component validation failed: {component_type}:{component_id}",
                      error_code=ExperimentErrorCodes.COMPONENT_VALIDATION_FAILED,
                      extra_data={
                          "component_type": component_type,
                          "component_id": component_id,
                          "validation_details": validation_details,
                          "run_id": self.current_run_id
                      })
    
    def log_auto_registration(self, component_type: str, component_id: str, 
                            success: bool, registration_details: Dict[str, Any] = None):
        """Log auto-registration events"""
        self.metrics.record_auto_registration(self.current_run_id, component_type, success)
        
        if success:
            self.info(f"Auto-registration successful: {component_type}:{component_id}",
                     extra_data={
                         "component_type": component_type,
                         "component_id": component_id,
                         "registration_details": registration_details,
                         "run_id": self.current_run_id
                     })
        else:
            error_code = getattr(ExperimentErrorCodes, f"COMPONENT_{component_type.upper()}_REGISTRATION_FAILED", 
                                ExperimentErrorCodes.COMPONENT_AUTO_REGISTRATION_FAILED)
            self.error(f"Auto-registration failed: {component_type}:{component_id}",
                      error_code=error_code,
                      extra_data={
                          "component_type": component_type,
                          "component_id": component_id,
                          "registration_details": registration_details,
                          "run_id": self.current_run_id
                      })
    
    def log_corpus_processing(self, corpus_id: str, files_processed: int, 
                            integrity_checks: Dict[str, Any], success: bool):
        """Log corpus processing with integrity validation"""
        self.metrics.record_corpus_processing(self.current_run_id, files_processed, success)
        
        if success:
            self.info(f"Corpus processing successful: {corpus_id}",
                     extra_data={
                         "corpus_id": corpus_id,
                         "files_processed": files_processed,
                         "integrity_checks": integrity_checks,
                         "run_id": self.current_run_id
                     })
        else:
            self.error(f"Corpus processing failed: {corpus_id}",
                      error_code=ExperimentErrorCodes.CORPUS_AUTO_REGISTRATION_FAILED,
                      extra_data={
                          "corpus_id": corpus_id,
                          "files_processed": files_processed,
                          "integrity_checks": integrity_checks,
                          "run_id": self.current_run_id
                      })
    
    def log_context_propagation(self, context_type: str, success: bool, 
                              propagation_details: Dict[str, Any] = None):
        """Log context propagation events"""
        self.metrics.record_context_propagation(self.current_run_id, success)
        
        if success:
            self.info(f"Context propagation successful: {context_type}",
                     extra_data={
                         "context_type": context_type,
                         "propagation_details": propagation_details,
                         "run_id": self.current_run_id
                     })
        else:
            self.error(f"Context propagation failed: {context_type}",
                      error_code=ExperimentErrorCodes.CONTEXT_ENRICHMENT_FAILED,
                      extra_data={
                          "context_type": context_type,
                          "propagation_details": propagation_details,
                          "run_id": self.current_run_id
                      })
    
    def log_hypothesis_validation(self, hypotheses: List[str], validation_results: Dict[str, Any]):
        """Log hypothesis validation with research context"""
        self.metrics.record_hypothesis_validation(self.current_run_id, len(hypotheses))
        
        self.info(f"Hypothesis validation completed: {len(hypotheses)} hypotheses",
                 extra_data={
                     "hypotheses": hypotheses,
                     "validation_results": validation_results,
                     "run_id": self.current_run_id
                 })
    
    def log_academic_compliance(self, check_type: str, result: bool, 
                              compliance_details: Dict[str, Any] = None):
        """Log academic compliance checks"""
        self.metrics.record_academic_compliance_check(self.current_run_id, check_type, result)
        
        if result:
            self.info(f"Academic compliance check passed: {check_type}",
                     extra_data={
                         "check_type": check_type,
                         "compliance_details": compliance_details,
                         "run_id": self.current_run_id
                     })
        else:
            error_code = ExperimentErrorCodes.ACADEMIC_INSTITUTIONAL_COMPLIANCE_FAILED
            self.warning(f"Academic compliance check failed: {check_type}",
                        error_code=error_code,
                        extra_data={
                            "check_type": check_type,
                            "compliance_details": compliance_details,
                            "run_id": self.current_run_id
                        })
    
    def log_integrity_validation(self, file_path: str, expected_hash: str, 
                               calculated_hash: str, success: bool):
        """Log file integrity validation"""
        if success:
            self.info(f"Integrity validation successful: {file_path}",
                     extra_data={
                         "file_path": file_path,
                         "expected_hash": expected_hash,
                         "calculated_hash": calculated_hash,
                         "run_id": self.current_run_id
                     })
        else:
            self.error(f"Integrity validation failed: {file_path}",
                      error_code=ExperimentErrorCodes.CORPUS_INTEGRITY_CHECK_FAILED,
                      extra_data={
                          "file_path": file_path,
                          "expected_hash": expected_hash,
                          "calculated_hash": calculated_hash,
                          "run_id": self.current_run_id
                      })
    
    def generate_experiment_report(self, run_id: str = None) -> Dict[str, Any]:
        """Generate comprehensive experiment report"""
        target_run_id = run_id or self.current_run_id
        if not target_run_id:
            return {}
        
        summary = self.metrics.get_experiment_summary(target_run_id)
        
        # Add success rates and quality metrics
        metrics = summary.get("experiment_metrics", {})
        
        if metrics.get("components_validated", 0) > 0:
            validation_success_rate = (
                (metrics.get("components_validated", 0) - metrics.get("error_count", 0)) /
                metrics.get("components_validated", 1)
            ) * 100
        else:
            validation_success_rate = 0.0
        
        report = {
            **summary,
            "quality_metrics": {
                "validation_success_rate": validation_success_rate,
                "auto_registration_success_rate": (
                    metrics.get("components_auto_registered", 0) / 
                    max(1, metrics.get("components_validated", 1))
                ) * 100,
                "context_propagation_count": metrics.get("context_propagations", 0),
                "hypothesis_validation_count": metrics.get("hypothesis_validations", 0),
                "integrity_checks_performed": metrics.get("corpus_files_processed", 0)
            },
            "reproducibility_metadata": {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "run_id": target_run_id,
                "logging_version": "experiment_logger_v1.0",
                "comprehensive_audit_trail": True
            }
        }
        
        return report

# Global instance for experiment logging
experiment_metrics = ExperimentMetricsCollector()

def get_experiment_logger(name: str) -> ExperimentLogger:
    """Get experiment logger instance"""
    return ExperimentLogger(name, experiment_metrics)

def setup_experiment_logging(log_level: str = "INFO", log_file: str = None):
    """Setup experiment logging with extended configuration"""
    from .logging_config import setup_logging
    
    # Use existing setup but with experiment-specific file
    if log_file is None:
        log_file = "logs/experiment_orchestrator.log"
    
    setup_logging(log_level, log_file)
    
    # Initialize experiment metrics collector
    global experiment_metrics
    experiment_metrics = ExperimentMetricsCollector() 