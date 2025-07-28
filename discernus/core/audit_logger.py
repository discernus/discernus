"""
Audit logger for experiment provenance.

Records all agent actions and system events in JSONL format.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional


class AuditLogger:
    """
    Audit logger for experiment provenance.
    
    Records all agent actions and system events in JSONL format.
    """
    
    def __init__(self, logs_dir: Path):
        """
        Initialize audit logger.
        
        Args:
            logs_dir: Directory to store log files
        """
        self.logs_dir = Path(logs_dir)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Create log files
        self.agent_log = self.logs_dir / "agents.jsonl"
        self.artifact_log = self.logs_dir / "artifacts.jsonl"
        self.llm_log = self.logs_dir / "llm_interactions.jsonl"
        self.system_log = self.logs_dir / "system.jsonl"
        
        # Initialize log files
        for log_file in [self.agent_log, self.artifact_log, self.llm_log, self.system_log]:
            if not log_file.exists():
                log_file.touch()
    
    def log_agent_event(self, agent_name: str, event_type: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Log agent event.
        
        Args:
            agent_name: Name of agent
            event_type: Type of event
            metadata: Additional event metadata
        """
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agent": agent_name,
            "event": event_type,
            "metadata": metadata or {}
        }
        
        with open(self.agent_log, "a") as f:
            f.write(json.dumps(event) + "\n")
    
    def log_artifact_event(self, artifact_hash: str, event_type: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Log artifact event.
        
        Args:
            artifact_hash: Hash of artifact
            event_type: Type of event
            metadata: Additional event metadata
        """
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "artifact_hash": artifact_hash,
            "event": event_type,
            "metadata": metadata or {}
        }
        
        with open(self.artifact_log, "a") as f:
            f.write(json.dumps(event) + "\n")
    
    def log_llm_event(self, model: str, event_type: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Log LLM interaction event.
        
        Args:
            model: LLM model name
            event_type: Type of event
            metadata: Additional event metadata
        """
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model": model,
            "event": event_type,
            "metadata": metadata or {}
        }
        
        with open(self.llm_log, "a") as f:
            f.write(json.dumps(event) + "\n")
    
    def log_system_event(self, event_type: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Log system event.
        
        Args:
            event_type: Type of event
            metadata: Additional event metadata
        """
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event_type,
            "metadata": metadata or {}
        }
        
        with open(self.system_log, "a") as f:
            f.write(json.dumps(event) + "\n") 

    def log_orchestrator_event(self, event_type: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Log orchestrator event.
        
        Args:
            event_type: Type of event
            metadata: Additional event metadata
        """
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "component": "orchestrator",
            "event": event_type,
            "metadata": metadata or {}
        }
        
        with open(self.system_log, "a") as f:
            f.write(json.dumps(event) + "\n") 