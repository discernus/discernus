#!/usr/bin/env python3
"""
Agent Configuration System
==========================

Defines configuration classes for V2 agents, including retry policies
and verification settings.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional, List


@dataclass
class RetryConfig:
    """
    Configuration for retry policies in agents.
    """
    max_retries: int = 3
    backoff_factor: float = 2.0
    initial_delay_seconds: float = 1.0
    max_delay_seconds: float = 60.0
    retryable_errors: List[str] = None
    
    def __post_init__(self):
        """Set default retryable errors if not provided"""
        if self.retryable_errors is None:
            self.retryable_errors = [
                "RateLimitError",
                "TimeoutError", 
                "ConnectionError",
                "ServiceUnavailableError"
            ]


@dataclass
class VerificationConfig:
    """
    Configuration for verification settings in agents.
    """
    enable_verification: bool = True
    verification_model: Optional[str] = None
    verification_timeout_seconds: float = 300.0
    verification_retry_config: Optional[RetryConfig] = None
    verification_threshold: float = 0.8
    
    def __post_init__(self):
        """Set default retry config if not provided"""
        if self.verification_retry_config is None:
            self.verification_retry_config = RetryConfig(
                max_retries=2,
                backoff_factor=1.5,
                initial_delay_seconds=2.0
            )


@dataclass
class AgentConfig:
    """
    Main configuration class for V2 agents.
    
    This provides a standardized way to configure agents with
    model selection, retry policies, and verification settings.
    """
    model: str = "vertex_ai/gemini-2.5-flash"
    parameters: Dict[str, Any] = None
    retry_config: Optional[RetryConfig] = None
    verification_config: Optional[VerificationConfig] = None
    timeout_seconds: float = 300.0
    enable_caching: bool = True
    enable_logging: bool = True
    
    def __post_init__(self):
        """Set default values if not provided"""
        if self.parameters is None:
            self.parameters = {}
        
        if self.retry_config is None:
            self.retry_config = RetryConfig()
        
        if self.verification_config is None:
            self.verification_config = VerificationConfig()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "model": self.model,
            "parameters": self.parameters,
            "retry_config": {
                "max_retries": self.retry_config.max_retries,
                "backoff_factor": self.retry_config.backoff_factor,
                "initial_delay_seconds": self.retry_config.initial_delay_seconds,
                "max_delay_seconds": self.retry_config.max_delay_seconds,
                "retryable_errors": self.retry_config.retryable_errors
            } if self.retry_config else None,
            "verification_config": {
                "enable_verification": self.verification_config.enable_verification,
                "verification_model": self.verification_config.verification_model,
                "verification_timeout_seconds": self.verification_config.verification_timeout_seconds,
                "verification_threshold": self.verification_config.verification_threshold,
                "verification_retry_config": {
                    "max_retries": self.verification_config.verification_retry_config.max_retries,
                    "backoff_factor": self.verification_config.verification_retry_config.backoff_factor,
                    "initial_delay_seconds": self.verification_config.verification_retry_config.initial_delay_seconds
                } if self.verification_config.verification_retry_config else None
            } if self.verification_config else None,
            "timeout_seconds": self.timeout_seconds,
            "enable_caching": self.enable_caching,
            "enable_logging": self.enable_logging
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentConfig':
        """Create AgentConfig from dictionary"""
        # Extract retry config
        retry_config = None
        if data.get('retry_config'):
            retry_data = data['retry_config']
            retry_config = RetryConfig(
                max_retries=retry_data.get('max_retries', 3),
                backoff_factor=retry_data.get('backoff_factor', 2.0),
                initial_delay_seconds=retry_data.get('initial_delay_seconds', 1.0),
                max_delay_seconds=retry_data.get('max_delay_seconds', 60.0),
                retryable_errors=retry_data.get('retryable_errors', [])
            )
        
        # Extract verification config
        verification_config = None
        if data.get('verification_config'):
            verif_data = data['verification_config']
            verif_retry_config = None
            if verif_data.get('verification_retry_config'):
                retry_data = verif_data['verification_retry_config']
                verif_retry_config = RetryConfig(
                    max_retries=retry_data.get('max_retries', 2),
                    backoff_factor=retry_data.get('backoff_factor', 1.5),
                    initial_delay_seconds=retry_data.get('initial_delay_seconds', 2.0)
                )
            
            verification_config = VerificationConfig(
                enable_verification=verif_data.get('enable_verification', True),
                verification_model=verif_data.get('verification_model'),
                verification_timeout_seconds=verif_data.get('verification_timeout_seconds', 300.0),
                verification_threshold=verif_data.get('verification_threshold', 0.8),
                verification_retry_config=verif_retry_config
            )
        
        return cls(
            model=data.get('model', 'vertex_ai/gemini-2.5-flash'),
            parameters=data.get('parameters', {}),
            retry_config=retry_config,
            verification_config=verification_config,
            timeout_seconds=data.get('timeout_seconds', 300.0),
            enable_caching=data.get('enable_caching', True),
            enable_logging=data.get('enable_logging', True)
        )
