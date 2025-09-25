#!/usr/bin/env python3
"""
Standard Agent Interface
========================

Defines the canonical interface for all V2 agents in the Discernus ecosystem.
This ensures consistency and enables the orchestrator to work with any agent
that implements this interface.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pathlib import Path

from .security_boundary import ExperimentSecurityBoundary
from .audit_logger import AuditLogger
from .local_artifact_storage import LocalArtifactStorage
from .agent_result import AgentResult
from .gateway_policy_enforcement import require_gateway_usage


@require_gateway_usage
class StandardAgent(ABC):
    """
    Abstract base class for all V2 agents.
    
    This defines the canonical interface that all agents must implement,
    ensuring consistency across the ecosystem and enabling the orchestrator
    to work with any agent type.
    """
    
    def __init__(self, 
                 security: ExperimentSecurityBoundary,
                 storage: LocalArtifactStorage,
                 audit: AuditLogger,
                 config: Optional[Any] = None):
        """
        Initialize the agent with required dependencies.
        
        Args:
            security: Security boundary for the experiment
            storage: Artifact storage for persistence
            audit: Audit logger for provenance tracking
            config: Optional configuration (AgentConfig or dict)
        """
        self.security = security
        self.storage = storage
        self.audit = audit
        self.config = config or {}
        
        # Log agent initialization
        config_keys = []
        if hasattr(self.config, 'to_dict'):
            config_keys = list(self.config.to_dict().keys())
        elif isinstance(self.config, dict):
            config_keys = list(self.config.keys())
            
        self.audit.log_agent_event(self.__class__.__name__, "initialization", {
            "agent_type": self.__class__.__name__,
            "config_keys": config_keys
        })
    
    @abstractmethod
    def execute(self, **kwargs) -> AgentResult:
        """
        Execute the agent's primary functionality.
        
        This is the main entry point for agent execution. Each agent
        should implement this method to perform its specific work.
        
        Args:
            **kwargs: Agent-specific parameters
            
        Returns:
            AgentResult: Standardized result with artifacts and metadata
        """
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """
        Declare agent capabilities for orchestrator discovery.
        
        Returns:
            List of capability strings that describe what this agent can do
        """
        pass
    
    def validate_inputs(self, **kwargs) -> bool:
        """
        Validate input parameters before execution.
        
        Override this method in subclasses to implement input validation.
        
        Args:
            **kwargs: Input parameters to validate
            
        Returns:
            True if inputs are valid, False otherwise
        """
        return True
    
    def get_required_inputs(self) -> List[str]:
        """
        Get list of required input parameter names.
        
        Override this method in subclasses to declare required inputs.
        
        Returns:
            List of required parameter names
        """
        return []
    
    def get_optional_inputs(self) -> List[str]:
        """
        Get list of optional input parameter names.
        
        Override this method in subclasses to declare optional inputs.
        
        Returns:
            List of optional parameter names
        """
        return []
    
    def log_execution_start(self, **kwargs) -> None:
        """Log the start of agent execution"""
        self.audit.log_agent_event(self.__class__.__name__, "execution_start", {
            "agent_type": self.__class__.__name__,
            "input_keys": list(kwargs.keys())
        })
    
    def log_execution_complete(self, result: AgentResult) -> None:
        """Log the completion of agent execution"""
        self.audit.log_agent_event(self.__class__.__name__, "execution_complete", {
            "agent_type": self.__class__.__name__,
            "success": result.success,
            "artifacts_count": len(result.artifacts),
            "execution_time_seconds": result.execution_time_seconds
        })
    
    def log_execution_error(self, error: Exception) -> None:
        """Log agent execution errors"""
        self.audit.log_agent_event(self.__class__.__name__, "execution_error", {
            "agent_type": self.__class__.__name__,
            "error_type": type(error).__name__,
            "error_message": str(error)
        })
