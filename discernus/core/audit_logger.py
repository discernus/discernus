#!/usr/bin/env python3
"""
Comprehensive Audit Logging System for Discernus THIN v2.0
==========================================================

Provides complete audit trail capture for all system operations:
- JSONL logging for all orchestrator and agent activities
- LLM interaction logging (prompts, responses, models, costs)
- Artifact chain tracking with cache status
- Real-time append-only logging for crash recovery

Ensures complete academic integrity and reproducibility.
"""

# Copyright (C) 2025  Discernus Team

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from .security_boundary import ExperimentSecurityBoundary


class AuditLogger:
    """
    Comprehensive audit logging system that captures all system activities
    for complete provenance and academic integrity.
    """
    
    def __init__(self, security_boundary: ExperimentSecurityBoundary, run_folder: Path):
        """
        Initialize audit logger for a specific experiment run.
        
        Args:
            security_boundary: Security boundary for file operations
            run_folder: The specific run folder for this experiment
        """
        self.security = security_boundary
        self.run_folder = security_boundary.validate_path(run_folder)
        
        # Create logs directory
        self.logs_dir = self.security.secure_mkdir(run_folder / "logs")
        
        # Define log file paths
        self.orchestrator_log = self.logs_dir / "orchestrator.jsonl"
        self.agent_log = self.logs_dir / "agents.jsonl"
        self.llm_log = self.logs_dir / "llm_interactions.jsonl"
        self.artifact_log = self.logs_dir / "artifacts.jsonl"
        self.system_log = self.logs_dir / "system.jsonl"
        self.cost_log = self.logs_dir / "costs.jsonl"
        
        # Initialize session metadata
        self.session_id = self._generate_session_id()
        self.start_time = self._get_timestamp()
        
        print(f"📋 Audit logging initialized: {self.logs_dir}")
        
        # Log session start
        self._log_system_event("audit_session_start", {
            "session_id": self.session_id,
            "experiment_root": str(security_boundary.experiment_root),
            "run_folder": str(self.run_folder),
            "start_time": self.start_time
        })
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID for this audit session."""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        random_suffix = hashlib.sha256(str(datetime.now()).encode()).hexdigest()[:8]
        return f"{timestamp}_{random_suffix}"
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        return datetime.now(timezone.utc).isoformat()
    
    def _append_to_log(self, log_file: Path, entry: Dict[str, Any]) -> None:
        """
        Append entry to JSONL log file (real-time, append-only).
        
        Args:
            log_file: Path to log file
            entry: Dictionary to log as JSON
        """
        try:
            # Add session metadata to every entry
            entry.update({
                "session_id": self.session_id,
                "timestamp": self._get_timestamp()
            })
            
            # Convert to JSON line
            json_line = json.dumps(entry, ensure_ascii=False, separators=(',', ':'))
            
            # Append to file (create if doesn't exist)
            with self.security.secure_open(log_file, 'a', encoding='utf-8') as f:
                f.write(json_line + '\n')
                f.flush()  # Ensure immediate write for crash recovery
                
        except Exception as e:
            print(f"⚠️ Audit logging error: {e}")
            # Don't fail the main process due to logging issues
    
    def log_orchestrator_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """
        Log orchestrator-level events.
        
        Args:
            event_type: Type of orchestrator event
            data: Event data dictionary
        """
        entry = {
            "log_type": "orchestrator",
            "event_type": event_type,
            "data": data
        }
        self._append_to_log(self.orchestrator_log, entry)
    
    def log_agent_event(self, agent_name: str, event_type: str, data: Dict[str, Any]) -> None:
        """
        Log agent execution events.
        
        Args:
            agent_name: Name of the agent (e.g., "AnalyseBatchAgent")
            event_type: Type of agent event
            data: Event data dictionary
        """
        entry = {
            "log_type": "agent",
            "agent_name": agent_name,
            "event_type": event_type,
            "data": data
        }
        self._append_to_log(self.agent_log, entry)
    
    def log_llm_interaction(self, 
                           model: str, 
                           prompt: str, 
                           response: str,
                           agent_name: str,
                           interaction_type: str = "completion",
                           metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Log complete LLM interaction with full details.
        
        Args:
            model: LLM model identifier
            prompt: Full prompt sent to LLM
            response: Full response from LLM
            agent_name: Which agent made the call
            interaction_type: Type of interaction (completion, chat, etc.)
            metadata: Additional metadata (cost, tokens, etc.)
        
        Returns:
            Interaction hash for reference
        """
        # Create interaction hash for reference
        interaction_data = f"{model}:{prompt}:{response}".encode('utf-8')
        interaction_hash = hashlib.sha256(interaction_data).hexdigest()[:16]
        
        entry = {
            "log_type": "llm_interaction",
            "interaction_hash": interaction_hash,
            "agent_name": agent_name,
            "model": model,
            "interaction_type": interaction_type,
            "prompt": prompt,
            "response": response,
            "prompt_length": len(prompt),
            "response_length": len(response),
            "metadata": metadata or {}
        }
        
        self._append_to_log(self.llm_log, entry)
        return interaction_hash
    
    def log_artifact_operation(self, 
                              operation: str,
                              artifact_hash: str,
                              artifact_type: str,
                              metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Log artifact storage/retrieval operations.
        
        Args:
            operation: Type of operation (store, retrieve, cache_hit)
            artifact_hash: SHA-256 hash of the artifact
            artifact_type: Type of artifact (framework, document, result, etc.)
            metadata: Additional metadata
        """
        entry = {
            "log_type": "artifact",
            "operation": operation,
            "artifact_hash": artifact_hash,
            "artifact_type": artifact_type,
            "metadata": metadata or {}
        }
        self._append_to_log(self.artifact_log, entry)
    
    def log_artifact_chain(self, 
                          stage: str,
                          input_hashes: List[str],
                          output_hash: str,
                          agent_name: str,
                          llm_interaction_hash: Optional[str] = None) -> None:
        """
        Log artifact transformation chain (input -> process -> output).
        
        Args:
            stage: Processing stage name
            input_hashes: List of input artifact hashes
            output_hash: Hash of produced output artifact
            agent_name: Agent that performed the transformation
            llm_interaction_hash: Reference to LLM interaction if applicable
        """
        entry = {
            "log_type": "artifact_chain",
            "stage": stage,
            "input_hashes": input_hashes,
            "output_hash": output_hash,
            "agent_name": agent_name,
            "llm_interaction_hash": llm_interaction_hash
        }
        self._append_to_log(self.artifact_log, entry)
    
    def _log_system_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """
        Log system-level events.
        
        Args:
            event_type: Type of system event
            data: Event data dictionary
        """
        entry = {
            "log_type": "system",
            "event_type": event_type,
            "data": data
        }
        self._append_to_log(self.system_log, entry)
    
    def log_error(self, error_type: str, error_message: str, 
                  context: Optional[Dict[str, Any]] = None) -> None:
        """
        Log error events with full context.
        
        Args:
            error_type: Type of error
            error_message: Error message
            context: Additional context information
        """
        entry = {
            "log_type": "error",
            "error_type": error_type,
            "error_message": error_message,
            "context": context or {}
        }
        self._append_to_log(self.system_log, entry)
    
    def log_performance_metric(self, metric_name: str, value: Union[float, int],
                              context: Optional[Dict[str, Any]] = None) -> None:
        """
        Log performance metrics.
        
        Args:
            metric_name: Name of the metric
            value: Metric value
            context: Additional context
        """
        entry = {
            "log_type": "performance",
            "metric_name": metric_name,
            "value": value,
            "context": context or {}
        }
        self._append_to_log(self.system_log, entry)
    
    def get_session_summary(self) -> Dict[str, Any]:
        """
        Get summary of current audit session.
        
        Returns:
            Dictionary with session summary
        """
        return {
            "session_id": self.session_id,
            "start_time": self.start_time,
            "current_time": self._get_timestamp(),
            "logs_directory": str(self.logs_dir),
            "log_files": {
                "orchestrator": str(self.orchestrator_log.relative_to(self.run_folder)),
                "agents": str(self.agent_log.relative_to(self.run_folder)),
                "llm_interactions": str(self.llm_log.relative_to(self.run_folder)),
                "artifacts": str(self.artifact_log.relative_to(self.run_folder)),
                "system": str(self.system_log.relative_to(self.run_folder)),
                "costs": str(self.cost_log.relative_to(self.run_folder))
            }
        }
    
    def log_cost(self, 
                 operation: str,
                 model: str,
                 tokens_used: int,
                 cost_usd: float,
                 agent_name: str,
                 interaction_hash: Optional[str] = None,
                 metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Log cost information for LLM operations.
        
        Args:
            operation: Type of operation (analysis, synthesis, validation, etc.)
            model: LLM model used
            tokens_used: Total tokens consumed
            cost_usd: Cost in USD
            agent_name: Agent that incurred the cost
            interaction_hash: Reference to LLM interaction
            metadata: Additional cost-related metadata
        """
        entry = {
            "log_type": "cost_tracking",
            "timestamp": self._get_timestamp(),
            "operation": operation,
            "agent_name": agent_name,
            "model": model,
            "tokens_used": tokens_used,
            "cost_usd": round(cost_usd, 6),  # 6 decimal places for precision
            "interaction_hash": interaction_hash,
            "metadata": metadata or {}
        }
        self._append_to_log(self.cost_log, entry)
    
    def get_session_costs(self) -> Dict[str, Any]:
        """
        Calculate total costs for the current session by reading cost log.
        
        Returns:
            Dictionary with cost breakdown and totals
        """
        if not self.cost_log.exists():
            return {
                "total_cost_usd": 0.0,
                "total_tokens": 0,
                "operations": {},
                "models": {},
                "agents": {}
            }
        
        total_cost = 0.0
        total_tokens = 0
        operations = {}
        models = {}
        agents = {}
        
        try:
            with open(self.cost_log, 'r') as f:
                for line in f:
                    if line.strip():
                        entry = json.loads(line)
                        
                        cost = entry.get("cost_usd", 0.0)
                        tokens = entry.get("tokens_used", 0)
                        operation = entry.get("operation", "unknown")
                        model = entry.get("model", "unknown")
                        agent = entry.get("agent_name", "unknown")
                        
                        # Aggregate totals
                        total_cost += cost
                        total_tokens += tokens
                        
                        # Aggregate by operation
                        if operation not in operations:
                            operations[operation] = {"cost_usd": 0.0, "tokens": 0, "calls": 0}
                        operations[operation]["cost_usd"] += cost
                        operations[operation]["tokens"] += tokens
                        operations[operation]["calls"] += 1
                        
                        # Aggregate by model
                        if model not in models:
                            models[model] = {"cost_usd": 0.0, "tokens": 0, "calls": 0}
                        models[model]["cost_usd"] += cost
                        models[model]["tokens"] += tokens
                        models[model]["calls"] += 1
                        
                        # Aggregate by agent
                        if agent not in agents:
                            agents[agent] = {"cost_usd": 0.0, "tokens": 0, "calls": 0}
                        agents[agent]["cost_usd"] += cost
                        agents[agent]["tokens"] += tokens
                        agents[agent]["calls"] += 1
                        
        except Exception as e:
            print(f"Warning: Error reading cost log: {e}")
        
        return {
            "total_cost_usd": round(total_cost, 6),
            "total_tokens": total_tokens,
            "operations": operations,
            "models": models,
            "agents": agents
        }
    
    def estimate_remaining_cost(self, 
                               documents_analyzed: int, 
                               total_documents: int,
                               synthesis_pending: bool = True) -> Dict[str, Any]:
        """
        Estimate remaining costs based on current usage patterns.
        
        Args:
            documents_analyzed: Number of documents already processed
            total_documents: Total documents in experiment
            synthesis_pending: Whether synthesis stage is still pending
            
        Returns:
            Cost estimation breakdown
        """
        current_costs = self.get_session_costs()
        
        if documents_analyzed == 0:
            return {
                "estimated_remaining_usd": 0.0,
                "estimated_total_usd": 0.0,
                "confidence": "low",
                "note": "No analysis completed yet - cannot estimate"
            }
        
        # Calculate per-document analysis cost
        analysis_operations = ["analysis", "document_processing", "framework_validation"]
        analysis_cost = sum(
            current_costs["operations"].get(op, {}).get("cost_usd", 0.0) 
            for op in analysis_operations
        )
        
        per_document_cost = analysis_cost / documents_analyzed if documents_analyzed > 0 else 0.0
        remaining_documents = total_documents - documents_analyzed
        estimated_analysis_remaining = per_document_cost * remaining_documents
        
        # Estimate synthesis cost (typically 10-20% of analysis cost)
        synthesis_cost_estimate = 0.0
        if synthesis_pending:
            if "synthesis" in current_costs["operations"]:
                # Use actual synthesis cost if we have it
                synthesis_cost_estimate = current_costs["operations"]["synthesis"]["cost_usd"]
            else:
                # Estimate as 15% of total analysis cost
                total_analysis_cost = analysis_cost + estimated_analysis_remaining
                synthesis_cost_estimate = total_analysis_cost * 0.15
        
        total_estimated_remaining = estimated_analysis_remaining + synthesis_cost_estimate
        total_estimated_experiment = current_costs["total_cost_usd"] + total_estimated_remaining
        
        return {
            "estimated_remaining_usd": round(total_estimated_remaining, 4),
            "estimated_total_usd": round(total_estimated_experiment, 4),
            "breakdown": {
                "remaining_analysis": round(estimated_analysis_remaining, 4),
                "estimated_synthesis": round(synthesis_cost_estimate, 4)
            },
            "confidence": "high" if documents_analyzed >= 3 else "medium",
            "per_document_cost": round(per_document_cost, 4)
        }
    
    def finalize_session(self) -> None:
        """Finalize the audit session and log completion."""
        end_time = self._get_timestamp()
        
        self._log_system_event("audit_session_end", {
            "session_id": self.session_id,
            "start_time": self.start_time,
            "end_time": end_time,
            "session_duration": self._calculate_duration(self.start_time, end_time)
        })
        
        print(f"📋 Audit session finalized: {self.session_id}")
    
    def _calculate_duration(self, start: str, end: str) -> float:
        """Calculate duration between timestamps in seconds."""
        try:
            start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
            return (end_dt - start_dt).total_seconds()
        except Exception:
            return 0.0


def create_audit_logger(security_boundary: ExperimentSecurityBoundary, run_folder: Path) -> AuditLogger:
    """Create an audit logger instance."""
    return AuditLogger(security_boundary, run_folder) 