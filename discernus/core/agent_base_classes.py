#!/usr/bin/env python3
"""
Agent Base Classes
==================

Defines specialized base classes for different types of V2 agents.
These provide common functionality and patterns for each agent type.
"""

from abc import abstractmethod
from typing import Dict, Any, List, Optional
import time

from .standard_agent import StandardAgent
from .agent_result import AgentResult, VerificationResult
from .agent_config import AgentConfig


class ToolCallingAgent(StandardAgent):
    """
    Base class for agents that use tool calling for structured output.
    
    This is for agents that need to emit structured results via tool calls
    or code execution returns, following the "Show Your Work" architecture.
    """
    
    def __init__(self, 
                 security,
                 storage,
                 audit,
                 config: Optional[AgentConfig] = None):
        super().__init__(security, storage, audit, config)
        self.tool_calls = []
        self.execution_results = []
    
    def record_tool_call(self, tool_name: str, parameters: Dict[str, Any], result: Any) -> str:
        """
        Record a tool call and its result.
        
        Args:
            tool_name: Name of the tool that was called
            parameters: Parameters passed to the tool
            result: Result returned by the tool
            
        Returns:
            Artifact ID for the tool call record
        """
        tool_call_data = {
            "tool_name": tool_name,
            "parameters": parameters,
            "result": result,
            "timestamp": time.time()
        }
        
        artifact_id = self.storage.store_artifact(
            f"tool_call_{tool_name}_{int(time.time())}",
            tool_call_data
        )
        
        self.tool_calls.append({
            "artifact_id": artifact_id,
            "tool_name": tool_name,
            "parameters": parameters
        })
        
        return artifact_id
    
    def get_capabilities(self) -> List[str]:
        """Tool calling agents can perform structured operations"""
        return ["tool_calling", "structured_output", "code_execution"]


class ValidationAgent(StandardAgent):
    """
    Base class for verification and coherence checking agents.
    
    This is for agents that validate other agents' work or check
    system coherence and consistency.
    """
    
    def __init__(self, 
                 security,
                 storage,
                 audit,
                 config: Optional[AgentConfig] = None):
        super().__init__(security, storage, audit, config)
        self.validation_rules = []
        self.validation_results = []
    
    @abstractmethod
    def validate(self, target_data: Dict[str, Any], **kwargs) -> AgentResult:
        """
        Validate target data according to agent-specific rules.
        
        Args:
            target_data: Data to validate
            **kwargs: Additional validation parameters
            
        Returns:
            AgentResult with validation results
        """
        pass
    
    def add_validation_rule(self, rule_name: str, rule_function) -> None:
        """Add a validation rule to the agent"""
        self.validation_rules.append({
            "name": rule_name,
            "function": rule_function
        })
    
    def get_capabilities(self) -> List[str]:
        """Validation agents can perform verification and coherence checking"""
        return ["validation", "verification", "coherence_checking"]


class SynthesisAgent(StandardAgent):
    """
    Base class for report generation agents.
    
    This is for agents that synthesize information from multiple sources
    into coherent reports or summaries.
    """
    
    def __init__(self, 
                 security,
                 storage,
                 audit,
                 config: Optional[AgentConfig] = None):
        super().__init__(security, storage, audit, config)
        self.synthesis_sources = []
        self.synthesis_metadata = {}
    
    @abstractmethod
    def synthesize(self, source_data: Dict[str, Any], **kwargs) -> AgentResult:
        """
        Synthesize information from source data into a coherent report.
        
        Args:
            source_data: Data to synthesize
            **kwargs: Additional synthesis parameters
            
        Returns:
            AgentResult with synthesis results
        """
        pass
    
    def add_synthesis_source(self, source_type: str, source_data: Any) -> None:
        """Add a source for synthesis"""
        self.synthesis_sources.append({
            "type": source_type,
            "data": source_data
        })
    
    def get_capabilities(self) -> List[str]:
        """Synthesis agents can generate reports and summaries"""
        return ["synthesis", "report_generation", "summarization"]


class VerificationAgent(StandardAgent):
    """
    Base class for adversarial attestation agents.
    
    This is for agents that perform adversarial verification of other
    agents' work, following the "Show Your Work" principles.
    """
    
    def __init__(self, 
                 security,
                 storage,
                 audit,
                 config: Optional[AgentConfig] = None):
        super().__init__(security, storage, audit, config)
        self.verification_targets = []
        self.attestation_data = {}
    
    @abstractmethod
    def verify(self, 
               primary_results: Dict[str, Any],
               computational_work: Dict[str, Any]) -> VerificationResult:
        """
        Adversarial verification of primary agent work.
        
        Args:
            primary_results: Results from the primary agent
            computational_work: Computational work to verify
            
        Returns:
            VerificationResult with verification status and discrepancies
        """
        pass
    
    def add_verification_target(self, target_type: str, target_data: Any) -> None:
        """Add a target for verification"""
        self.verification_targets.append({
            "type": target_type,
            "data": target_data
        })
    
    def create_attestation(self, verification_result: VerificationResult) -> str:
        """
        Create an attestation artifact for verification results.
        
        Args:
            verification_result: Result of verification
            
        Returns:
            Artifact ID for the attestation
        """
        attestation_data = {
            "verified": verification_result.verified,
            "discrepancies": verification_result.discrepancies,
            "attestation_data": verification_result.attestation_data,
            "primary_artifact_id": verification_result.primary_artifact_id,
            "verification_artifact_id": verification_result.verification_artifact_id,
            "timestamp": time.time()
        }
        
        artifact_id = self.storage.store_artifact(
            f"attestation_{int(time.time())}",
            attestation_data
        )
        
        self.attestation_data[artifact_id] = attestation_data
        return artifact_id
    
    def get_capabilities(self) -> List[str]:
        """Verification agents can perform adversarial attestation"""
        return ["verification", "attestation", "adversarial_validation"]
