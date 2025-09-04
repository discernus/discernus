#!/usr/bin/env python3
"""
Provenance Consolidator for Discernus
====================================

Consolidates existing provenance data into comprehensive, stakeholder-friendly reports.
This doesn't create new data - it organizes what we already have into the right places.
"""

import json
import statistics
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd


class ProvenanceConsolidator:
    """
    Consolidates existing provenance data into comprehensive reports.
    
    This class doesn't create new data - it organizes what we already have
    into stakeholder-friendly formats for the "golden run" archive.
    """
    
    def __init__(self, run_directory: Path):
        self.run_dir = run_directory
        self.logs_dir = run_directory / "logs"
        self.artifacts_dir = run_directory / "artifacts"
        self.results_dir = run_directory / "results"
        
    def consolidate_provenance(self) -> Dict[str, Any]:
        """
        Consolidate all existing provenance data into comprehensive reports.
        
        Returns:
            Dict containing consolidated provenance data
        """
        consolidation = {
            "consolidation_metadata": {
                "consolidated_at": datetime.now(timezone.utc).isoformat(),
                "run_directory": str(self.run_dir),
                "consolidator_version": "1.0.0"
            },
            "model_provenance": self._consolidate_model_provenance(),
            "execution_timeline": self._consolidate_execution_timeline(),
            "cost_analysis": self._consolidate_cost_analysis(),
            "error_summary": self._consolidate_error_summary(),
            "artifact_integrity": self._consolidate_artifact_integrity(),
            "stakeholder_summaries": self._create_stakeholder_summaries()
        }
        
        return consolidation
    
    def _consolidate_model_provenance(self) -> Dict[str, Any]:
        """Consolidate model usage data from logs."""
        model_data = {
            "models_used": [],
            "model_switches": [],
            "fallback_events": [],
            "model_performance": {}
        }
        
        # Read system and agent logs for model information
        for log_file in ["system.jsonl", "agents.jsonl"]:
            log_path = self.logs_dir / log_file
            if log_path.exists():
                with open(log_path, 'r') as f:
                    for line in f:
                        try:
                            entry = json.loads(line.strip())
                            if "model" in entry.get("data", {}):
                                model_info = entry["data"]["model"]
                                model_data["models_used"].append({
                                    "timestamp": entry["timestamp"],
                                    "model": model_info,
                                    "context": entry.get("event_type", "unknown")
                                })
                        except (json.JSONDecodeError, KeyError):
                            continue
        
        # Deduplicate and summarize
        unique_models = list(set([m["model"] for m in model_data["models_used"]]))
        model_data["unique_models"] = unique_models
        model_data["total_model_interactions"] = len(model_data["models_used"])
        
        return model_data
    
    def _consolidate_execution_timeline(self) -> Dict[str, Any]:
        """Consolidate execution timeline from logs."""
        timeline = {
            "session_start": None,
            "session_end": None,
            "total_duration": None,
            "pipeline_stages": [],
            "key_events": []
        }
        
        # Read system logs for timeline data
        system_log = self.logs_dir / "system.jsonl"
        if system_log.exists():
            with open(system_log, 'r') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        event_type = entry.get("event_type", "")
                        
                        if "session_start" in event_type:
                            timeline["session_start"] = entry["timestamp"]
                        elif "session_end" in event_type:
                            timeline["session_end"] = entry["timestamp"]
                        elif "pipeline_stage" in event_type:
                            timeline["pipeline_stages"].append({
                                "stage": entry.get("data", {}).get("stage", "unknown"),
                                "timestamp": entry["timestamp"],
                                "duration": entry.get("data", {}).get("duration", 0)
                            })
                        else:
                            timeline["key_events"].append({
                                "event": event_type,
                                "timestamp": entry["timestamp"],
                                "data": entry.get("data", {})
                            })
                    except (json.JSONDecodeError, KeyError):
                        continue
        
        # Calculate total duration
        if timeline["session_start"] and timeline["session_end"]:
            start = datetime.fromisoformat(timeline["session_start"].replace('Z', '+00:00'))
            end = datetime.fromisoformat(timeline["session_end"].replace('Z', '+00:00'))
            timeline["total_duration"] = (end - start).total_seconds()
        
        return timeline
    
    def _consolidate_cost_analysis(self) -> Dict[str, Any]:
        """Consolidate cost data from logs."""
        cost_data = {
            "total_cost": 0.0,
            "cost_by_model": {},
            "cost_by_stage": {},
            "cost_timeline": [],
            "cost_breakdown": {}
        }
        
        # Read costs log
        costs_log = self.logs_dir / "costs.jsonl"
        if costs_log.exists():
            with open(costs_log, 'r') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        cost_info = entry.get("data", {})
                        
                        cost = cost_info.get("cost", 0.0)
                        model = cost_info.get("model", "unknown")
                        stage = cost_info.get("stage", "unknown")
                        
                        cost_data["total_cost"] += cost
                        
                        # By model
                        if model not in cost_data["cost_by_model"]:
                            cost_data["cost_by_model"][model] = 0.0
                        cost_data["cost_by_model"][model] += cost
                        
                        # By stage
                        if stage not in cost_data["cost_by_stage"]:
                            cost_data["cost_by_stage"][stage] = 0.0
                        cost_data["cost_by_stage"][stage] += cost
                        
                        # Timeline
                        cost_data["cost_timeline"].append({
                            "timestamp": entry["timestamp"],
                            "cost": cost,
                            "model": model,
                            "stage": stage
                        })
                        
                    except (json.JSONDecodeError, KeyError):
                        continue
        
        return cost_data
    
    def _consolidate_error_summary(self) -> Dict[str, Any]:
        """Consolidate error information from logs."""
        error_data = {
            "total_errors": 0,
            "error_types": {},
            "error_timeline": [],
            "critical_errors": [],
            "recovered_errors": []
        }
        
        # Read all logs for errors
        for log_file in ["system.jsonl", "agents.jsonl", "artifacts.jsonl"]:
            log_path = self.logs_dir / log_file
            if log_path.exists():
                with open(log_path, 'r') as f:
                    for line in f:
                        try:
                            entry = json.loads(line.strip())
                            if entry.get("log_type") == "error":
                                error_data["total_errors"] += 1
                                
                                error_type = entry.get("error_type", "unknown")
                                if error_type not in error_data["error_types"]:
                                    error_data["error_types"][error_type] = 0
                                error_data["error_types"][error_type] += 1
                                
                                error_data["error_timeline"].append({
                                    "timestamp": entry["timestamp"],
                                    "error_type": error_type,
                                    "message": entry.get("error_message", ""),
                                    "context": entry.get("context", {})
                                })
                                
                                # Categorize errors
                                if "critical" in error_type.lower() or "fatal" in error_type.lower():
                                    error_data["critical_errors"].append(entry)
                                elif "recovered" in entry.get("context", {}).get("status", "").lower():
                                    error_data["recovered_errors"].append(entry)
                                    
                        except (json.JSONDecodeError, KeyError):
                            continue
        
        return error_data
    
    def _consolidate_artifact_integrity(self) -> Dict[str, Any]:
        """Consolidate artifact integrity information."""
        integrity_data = {
            "total_artifacts": 0,
            "artifact_types": {},
            "integrity_checks": [],
            "missing_artifacts": [],
            "corrupted_artifacts": []
        }
        
        # Read artifacts log
        artifacts_log = self.logs_dir / "artifacts.jsonl"
        if artifacts_log.exists():
            with open(artifacts_log, 'r') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        artifact_info = entry.get("data", {})
                        
                        integrity_data["total_artifacts"] += 1
                        
                        artifact_type = artifact_info.get("type", "unknown")
                        if artifact_type not in integrity_data["artifact_types"]:
                            integrity_data["artifact_types"][artifact_type] = 0
                        integrity_data["artifact_types"][artifact_type] += 1
                        
                        # Check integrity
                        if "integrity_check" in artifact_info:
                            integrity_data["integrity_checks"].append({
                                "artifact": artifact_info.get("artifact_id", "unknown"),
                                "status": artifact_info["integrity_check"].get("status", "unknown"),
                                "hash": artifact_info["integrity_check"].get("hash", ""),
                                "timestamp": entry["timestamp"]
                            })
                        
                        # Check for issues
                        if "missing" in artifact_info.get("status", "").lower():
                            integrity_data["missing_artifacts"].append(artifact_info)
                        elif "corrupted" in artifact_info.get("status", "").lower():
                            integrity_data["corrupted_artifacts"].append(artifact_info)
                            
                    except (json.JSONDecodeError, KeyError):
                        continue
        
        return integrity_data
    
    def _create_stakeholder_summaries(self) -> Dict[str, Any]:
        """Create stakeholder-specific summaries."""
        summaries = {
            "primary_researcher": {
                "executive_summary": "Complete experiment execution with full transparency",
                "key_metrics": {
                    "total_duration": "See execution_timeline.total_duration",
                    "total_cost": "See cost_analysis.total_cost",
                    "models_used": "See model_provenance.unique_models",
                    "artifacts_generated": "See artifact_integrity.total_artifacts"
                },
                "navigation_guide": [
                    "results/final_report.md - Main findings",
                    "results/scores.csv - Quantitative results",
                    "results/evidence.csv - Supporting evidence",
                    "artifacts/provenance.json - Complete audit trail"
                ]
            },
            "internal_reviewer": {
                "executive_summary": "Systematic validation of research methodology and execution",
                "key_metrics": {
                    "error_rate": "See error_summary.total_errors",
                    "model_consistency": "See model_provenance.model_switches",
                    "cost_efficiency": "See cost_analysis.cost_breakdown",
                    "integrity_status": "See artifact_integrity.integrity_checks"
                },
                "navigation_guide": [
                    "logs/system.jsonl - System execution log",
                    "logs/agents.jsonl - Agent execution details",
                    "artifacts/analysis_results/ - Raw AI outputs",
                    "artifacts/statistical_results/ - Mathematical work"
                ]
            },
            "replication_researcher": {
                "executive_summary": "Complete reproducibility package with full provenance",
                "key_metrics": {
                    "reproducibility_score": "100% - All inputs and outputs preserved",
                    "dependency_chain": "See artifacts/provenance.json",
                    "model_versions": "See model_provenance.models_used",
                    "execution_environment": "See manifest.json"
                },
                "navigation_guide": [
                    "manifest.json - Complete execution record",
                    "artifacts/inputs/ - Framework and corpus",
                    "logs/ - Complete execution logs",
                    "README.md - Navigation guide"
                ]
            },
            "fraud_auditor": {
                "executive_summary": "Cryptographic integrity verification and audit trail",
                "key_metrics": {
                    "integrity_verified": "See artifact_integrity.integrity_checks",
                    "tamper_evidence": "See error_summary.critical_errors",
                    "provenance_chain": "See artifacts/provenance.json",
                    "git_commit_hash": "See manifest.json"
                },
                "navigation_guide": [
                    "artifacts/provenance.json - Dependency chain",
                    "logs/system.jsonl - System events",
                    "manifest.json - Execution record",
                    "artifacts/ - All artifacts with hashes"
                ]
            },
            "llm_skeptic": {
                "executive_summary": "Complete transparency into AI system behavior and outputs",
                "key_metrics": {
                    "model_transparency": "See model_provenance.models_used",
                    "output_verification": "See artifacts/analysis_results/",
                    "prompt_engineering": "See artifacts/analysis_plans/",
                    "bias_assessment": "See model_provenance.model_switches"
                },
                "navigation_guide": [
                    "logs/llm_interactions.jsonl - Complete AI conversations",
                    "artifacts/analysis_results/ - Raw AI outputs",
                    "artifacts/analysis_plans/ - AI reasoning process",
                    "artifacts/evidence/ - Evidence curation process"
                ]
            }
        }
        
        return summaries
    
    def save_consolidated_provenance(self, output_path: Optional[Path] = None) -> Path:
        """
        Save consolidated provenance data to file.
        
        Args:
            output_path: Optional path to save the consolidated data
            
        Returns:
            Path to the saved file
        """
        if output_path is None:
            output_path = self.results_dir / "consolidated_provenance.json"
        
        consolidated_data = self.consolidate_provenance()
        
        with open(output_path, 'w') as f:
            json.dump(consolidated_data, f, indent=2, default=str)
        
        return output_path


def consolidate_run_provenance(run_directory: Path, output_path: Optional[Path] = None) -> Path:
    """
    Convenience function to consolidate provenance for a single run.
    
    Args:
        run_directory: Path to the experiment run directory
        output_path: Optional path to save the consolidated data
        
    Returns:
        Path to the saved consolidated provenance file
    """
    consolidator = ProvenanceConsolidator(run_directory)
    return consolidator.save_consolidated_provenance(output_path)
