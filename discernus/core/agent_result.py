#!/usr/bin/env python3
"""
Agent Result Classes
===================

Defines the standard result types for V2 agents in the Discernus ecosystem.
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from datetime import datetime


@dataclass
class AgentResult:
    """
    Standard result type for all V2 agents.
    
    This provides a consistent interface for agent execution results
    across the entire V2 ecosystem.
    """
    success: bool
    artifacts: List[str]
    metadata: Dict[str, Any]
    error_message: Optional[str] = None
    execution_time_seconds: Optional[float] = None
    timestamp: Optional[datetime] = None
    
    def __post_init__(self):
        """Set timestamp if not provided"""
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class VerificationResult:
    """
    Result type for verification agents.
    
    Extends AgentResult with verification-specific fields.
    """
    verified: bool
    discrepancies: List[str]
    attestation_data: Dict[str, Any]
    primary_artifact_id: str
    verification_artifact_id: str
    
    def __post_init__(self):
        """Ensure verification result has success based on verified status"""
        if not hasattr(self, 'success'):
            self.success = self.verified
