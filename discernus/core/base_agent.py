#!/usr/bin/env python3
"""
BaseAgent - THIN Agent Abstraction for Discernus Agents
=======================================================

Standardizes common agent infrastructure while maintaining THIN principles:
- Redis connection management
- MinIO artifact storage integration  
- Standardized JSONL logging per Alpha System specification
- External YAML prompt loading with DNA capture for provenance
- Common error handling patterns

All agents inherit from this class to eliminate boilerplate and ensure consistency.
"""

import redis
import json
import yaml
import sys
import os
import logging
import hashlib
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime

# Add scripts directory to path for MinIO integration
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from minio_client import get_artifact, put_artifact, ArtifactStorageError

class BaseAgentError(Exception):
    """Base agent exceptions"""
    pass

class BaseAgent(ABC):
    """
    Abstract base class for all Discernus agents.
    Provides standardized infrastructure while keeping business logic in subclasses.
    """
    
    def __init__(self, agent_name: str):
        """
        Initialize base agent infrastructure.
        
        Args:
            agent_name: Name of the agent (e.g., 'AnalyseBatchAgent')
        """
        self.agent_name = agent_name
        self.start_time = time.time()
        
        # Initialize infrastructure (logging first so other methods can log)
        self._setup_logging()
        self._setup_redis()
        self._load_prompt_template()
        
    def _setup_redis(self):
        """Initialize Redis connection with environment configuration"""
        self.redis_host = os.getenv('REDIS_HOST', 'localhost')
        self.redis_port = int(os.getenv('REDIS_PORT', 6379))
        self.redis_db = int(os.getenv('REDIS_DB', 0))
        
        try:
            self.redis_client = redis.Redis(
                host=self.redis_host, 
                port=self.redis_port, 
                db=self.redis_db
            )
            # Test connection
            self.redis_client.ping()
            self._log_info("Redis connection established")
        except Exception as e:
            raise BaseAgentError(f"Redis connection failed: {e}")
    
    def _setup_logging(self):
        """Initialize standardized JSONL logging per Alpha System specification"""
        # Create agent-specific logger
        self.logger = logging.getLogger(f"discernus.{self.agent_name}")
        self.logger.setLevel(logging.INFO)
        
        # Clear existing handlers to avoid duplication
        self.logger.handlers.clear()
        
        # Create JSONL formatter
        agent_name = self.agent_name  # Capture for closure
        class JSONLFormatter(logging.Formatter):
            def format(self, record):
                log_entry = {
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "agent_name": agent_name,
                    "stage": "agent_execution",
                    "log_level": record.levelname,
                    "message": record.getMessage()
                }
                return json.dumps(log_entry)
        
        # Create console handler with JSONL format
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(JSONLFormatter())
        self.logger.addHandler(console_handler)
        
    def _load_prompt_template(self) -> str:
        """
        Load external YAML prompt template with DNA capture for provenance.
        Returns the prompt template and captures file hash for audit trail.
        """
        try:
            # Find prompt.yaml in agent directory
            agent_dir = os.path.dirname(sys.modules[self.__class__.__module__].__file__)
            prompt_path = os.path.join(agent_dir, 'prompt.yaml')
            
            if not os.path.exists(prompt_path):
                raise BaseAgentError(f"Prompt file not found: {prompt_path}")
            
            # Load prompt template
            with open(prompt_path, 'r') as f:
                prompt_content = f.read()
                prompt_data = yaml.safe_load(prompt_content)
            
            if 'template' not in prompt_data:
                raise BaseAgentError(f"Prompt file missing 'template' key: {prompt_path}")
            
            # Capture prompt DNA for provenance
            self.prompt_hash = hashlib.sha256(prompt_content.encode()).hexdigest()
            self.prompt_path = prompt_path
            self.prompt_template = prompt_data['template']
            
            self._log_info(f"Loaded prompt template (DNA: {self.prompt_hash[:8]}...)")
            return self.prompt_template
            
        except Exception as e:
            raise BaseAgentError(f"Prompt loading failed: {e}")
    
    def capture_prompt_dna(self, run_folder: str) -> str:
        """
        Capture prompt DNA for provenance by storing prompt.yaml in run assets.
        
        Args:
            run_folder: Path to experiment run folder
            
        Returns:
            SHA-256 hash of the prompt file for manifest recording
        """
        try:
            # Read current prompt file
            with open(self.prompt_path, 'rb') as f:
                prompt_content = f.read()
            
            # Store in MinIO for permanent provenance
            prompt_hash = put_artifact(prompt_content)
            
            # Also copy to run assets folder for easy access
            assets_dir = os.path.join(run_folder, 'assets')
            os.makedirs(assets_dir, exist_ok=True)
            
            prompt_filename = f"{self.agent_name.lower()}_prompt_{prompt_hash[:8]}.yaml"
            prompt_asset_path = os.path.join(assets_dir, prompt_filename)
            
            with open(prompt_asset_path, 'wb') as f:
                f.write(prompt_content)
            
            self._log_info(f"Captured prompt DNA: {prompt_hash}")
            return prompt_hash
            
        except Exception as e:
            self._log_error(f"Prompt DNA capture failed: {e}")
            raise BaseAgentError(f"Prompt DNA capture failed: {e}")
    
    def _log_info(self, message: str, **kwargs):
        """Log info message with optional run_id context"""
        self.logger.info(message, extra=kwargs)
    
    def _log_error(self, message: str, **kwargs):
        """Log error message with optional run_id context"""
        self.logger.error(message, extra=kwargs)
    
    def _log_warning(self, message: str, **kwargs):
        """Log warning message with optional run_id context"""
        self.logger.warning(message, extra=kwargs)
    
    def report_fatal_error(self, error: Exception, task_id: str):
        """
        Report fatal error with standardized error handling.
        Logs error and marks task as failed in Redis.
        """
        error_message = f"Fatal error in {self.agent_name}: {str(error)}"
        self._log_error(error_message, extra={"task_id": task_id})
        
        # Mark task as failed in Redis for orchestration visibility
        try:
            error_data = {
                "agent_name": self.agent_name,
                "task_id": task_id,
                "error": str(error),
                "timestamp": time.time()
            }
            self.redis_client.xadd('tasks.error', error_data)
        except Exception as redis_error:
            self._log_error(f"Failed to report error to Redis: {redis_error}")
    
    @abstractmethod
    def process_task(self, task_id: str) -> bool:
        """
        Process a single task - implemented by subclasses.
        
        Args:
            task_id: Redis stream message ID
            
        Returns:
            True if successful, False if failed
        """
        pass
    
    def run_agent(self, task_id: str) -> int:
        """
        Main entry point for agent execution.
        Handles errors and provides consistent exit codes.
        
        Returns:
            0 for success, 1 for failure
        """
        try:
            self._log_info(f"Starting {self.agent_name} for task {task_id}")
            
            success = self.process_task(task_id)
            
            if success:
                duration = time.time() - self.start_time
                self._log_info(f"{self.agent_name} completed successfully", 
                             extra={"task_id": task_id, "duration_seconds": duration})
                return 0
            else:
                self._log_error(f"{self.agent_name} failed", extra={"task_id": task_id})
                return 1
                
        except Exception as e:
            self.report_fatal_error(e, task_id)
            return 1

def main_agent_entry_point(agent_class, agent_name: str):
    """
    Standard entry point for all agents.
    Handles command line arguments and error reporting.
    """
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <task_id>", file=sys.stderr)
        sys.exit(1)
    
    task_id = sys.argv[1]
    
    try:
        agent = agent_class(agent_name)
        exit_code = agent.run_agent(task_id)
        sys.exit(exit_code)
    except Exception as e:
        print(f"Fatal {agent_name} error: {e}", file=sys.stderr)
        sys.exit(1) 