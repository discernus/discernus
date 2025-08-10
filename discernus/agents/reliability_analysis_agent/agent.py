#!/usr/bin/env python3
"""
ReliabilityAnalysisAgent

Infrastructure reliability analysis agent for the Discernus research platform.
Provides LLM-based artifact analysis for reliability monitoring and validation.

THIN approach: Uses LLM intelligence for complex artifact analysis instead of 
brittle parsing code. Follows THIN architecture with externalized YAML prompts.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry
from discernus.core.audit_logger import AuditLogger


@dataclass
class DimensionValidationResult:
    """Result of framework dimension validation."""
    validation_passed: bool
    missing_required_dimensions: List[str]
    missing_optional_dimensions: List[str]
    present_dimensions: List[str]
    impact_assessment: str
    recommended_action: str  # PROCEED, RETRY_ANALYSIS, FAIL_EXPERIMENT
    error_message: Optional[str] = None


@dataclass
class StatisticalHealthResult:
    """Result of statistical health validation."""
    validation_passed: bool
    calculation_failures: List[str]
    perfect_correlations: List[str]
    statistical_warnings: List[str]
    sample_size_assessment: str  # adequate, minimal, insufficient
    recommended_action: str  # PROCEED, WARN_RESEARCHER, FAIL_EXPERIMENT
    error_message: Optional[str] = None


@dataclass
class PipelineHealthResult:
    """Result of pipeline health assessment."""
    health_status: str  # healthy, degraded, critical
    error_patterns: List[str]
    performance_issues: List[str]
    reliability_metrics: Dict[str, Any]
    recommended_actions: List[str]
    alert_level: str  # none, warning, critical


class ReliabilityAnalysisAgent:
    """
    Infrastructure reliability analysis agent.
    
    Provides LLM-based analysis of various artifacts for reliability monitoring:
    - Framework dimension validation
    - Statistical health assessment  
    - Pipeline health monitoring
    """
    
    def __init__(
        self,
        model: str = "vertex_ai/gemini-2.5-flash-lite",
        audit_logger: Optional[AuditLogger] = None
    ):
        """Initialize the reliability analysis agent."""
        self.agent_name = "ReliabilityAnalysisAgent"
        self.model = model
        self.audit_logger = audit_logger
        
        # Initialize LLM gateway with model registry
        model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(model_registry)
        
        # Load YAML prompts
        self.prompts = self._load_prompts()
        
        # Log agent initialization
        if self.audit_logger:
            self.audit_logger.log_agent_event(
                self.agent_name,
                "agent_initialized",
                {"model": self.model}
            )
    
    def _load_prompts(self) -> Dict[str, Any]:
        """Load YAML prompt templates."""
        try:
            prompt_file = Path(__file__).parent / "prompt.yaml"
            with open(prompt_file, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Warning: Failed to load prompts for {self.agent_name}: {e}")
            return {}
    
    def validate_framework_dimensions(
        self,
        framework_content: str,
        analysis_results: str,
        **kwargs
    ) -> DimensionValidationResult:
        """
        Validate that all required framework dimensions were detected in analysis results.
        
        Args:
            framework_content: Full framework specification content
            analysis_results: JSON string of analysis results from extraction
            **kwargs: Additional context for the analysis
            
        Returns:
            DimensionValidationResult with validation status and detailed findings
        """
        try:
            # Log validation start
            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "framework_dimension_validation_started",
                    {
                        "framework_length": len(framework_content),
                        "analysis_results_length": len(analysis_results)
                    }
                )
            
            # Get prompt template
            prompt_template = self.prompts.get("framework_dimension_validation", {}).get("template", "")
            if not prompt_template:
                raise ValueError("Framework dimension validation prompt template not found")
            
            # Format prompt with current context
            validation_prompt = prompt_template.format(
                current_date=datetime.now().strftime("%Y-%m-%d"),
                framework_content=framework_content,
                analysis_results=analysis_results,
                **kwargs
            )
            
            # Execute LLM call
            response, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=validation_prompt,
                system_prompt="You are a reliability analysis expert for the Discernus research platform."
            )
            
            # Log LLM response
            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "framework_dimension_validation_response",
                    {"response_length": len(response), "metadata": metadata}
                )
            
            # Parse validation result
            result = self._parse_dimension_validation_response(response)
            
            # Log validation completion
            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "framework_dimension_validation_complete",
                    {
                        "validation_passed": result.validation_passed,
                        "missing_required_count": len(result.missing_required_dimensions),
                        "recommended_action": result.recommended_action
                    }
                )
            
            return result
            
        except Exception as e:
            error_msg = f"Framework dimension validation failed: {str(e)}"
            if self.audit_logger:
                self.audit_logger.log_error(
                    "framework_dimension_validation_error",
                    error_msg,
                    {"agent": self.agent_name}
                )
            
            return DimensionValidationResult(
                validation_passed=False,
                missing_required_dimensions=[],
                missing_optional_dimensions=[],
                present_dimensions=[],
                impact_assessment="Validation failed due to system error",
                recommended_action="FAIL_EXPERIMENT",
                error_message=error_msg
            )
    
    def validate_statistical_health(
        self,
        statistical_results: str,
        **kwargs
    ) -> StatisticalHealthResult:
        """
        Validate statistical calculation health and identify data quality issues.
        
        Args:
            statistical_results: JSON string of statistical analysis results
            **kwargs: Additional context for the analysis
            
        Returns:
            StatisticalHealthResult with health assessment and recommendations
        """
        try:
            # Log validation start
            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "statistical_health_validation_started",
                    {"statistical_results_length": len(statistical_results)}
                )
            
            # Get prompt template
            prompt_template = self.prompts.get("statistical_health_validation", {}).get("template", "")
            if not prompt_template:
                raise ValueError("Statistical health validation prompt template not found")
            
            # Format prompt with current context
            validation_prompt = prompt_template.format(
                current_date=datetime.now().strftime("%Y-%m-%d"),
                statistical_results=statistical_results,
                **kwargs
            )
            
            # Execute LLM call
            response, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=validation_prompt,
                system_prompt="You are a statistical analysis expert for the Discernus research platform."
            )
            
            # Log LLM response
            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "statistical_health_validation_response",
                    {"response_length": len(response), "metadata": metadata}
                )
            
            # Parse validation result
            result = self._parse_statistical_health_response(response)
            
            # Log validation completion
            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "statistical_health_validation_complete",
                    {
                        "validation_passed": result.validation_passed,
                        "calculation_failures_count": len(result.calculation_failures),
                        "recommended_action": result.recommended_action
                    }
                )
            
            return result
            
        except Exception as e:
            error_msg = f"Statistical health validation failed: {str(e)}"
            if self.audit_logger:
                self.audit_logger.log_error(
                    "statistical_health_validation_error",
                    error_msg,
                    {"agent": self.agent_name}
                )
            
            return StatisticalHealthResult(
                validation_passed=False,
                calculation_failures=[],
                perfect_correlations=[],
                statistical_warnings=[],
                sample_size_assessment="unknown",
                recommended_action="FAIL_EXPERIMENT",
                error_message=error_msg
            )
    
    def assess_pipeline_health(
        self,
        audit_logs: str,
        pipeline_artifacts: Dict[str, Any],
        **kwargs
    ) -> PipelineHealthResult:
        """
        Assess overall pipeline health from audit logs and artifacts.
        
        Args:
            audit_logs: Audit log entries for analysis
            pipeline_artifacts: Dictionary of pipeline artifacts and metadata
            **kwargs: Additional context for the analysis
            
        Returns:
            PipelineHealthResult with health status and recommendations
        """
        try:
            # Log assessment start
            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "pipeline_health_assessment_started",
                    {
                        "audit_logs_length": len(audit_logs),
                        "artifacts_count": len(pipeline_artifacts)
                    }
                )
            
            # Get prompt template
            prompt_template = self.prompts.get("pipeline_health_assessment", {}).get("template", "")
            if not prompt_template:
                raise ValueError("Pipeline health assessment prompt template not found")
            
            # Format prompt with current context
            assessment_prompt = prompt_template.format(
                current_date=datetime.now().strftime("%Y-%m-%d"),
                audit_logs=audit_logs,
                pipeline_artifacts=json.dumps(pipeline_artifacts, indent=2),
                **kwargs
            )
            
            # Execute LLM call
            response, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=assessment_prompt,
                system_prompt="You are a pipeline reliability expert for the Discernus research platform."
            )
            
            # Log LLM response
            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "pipeline_health_assessment_response",
                    {"response_length": len(response), "metadata": metadata}
                )
            
            # Parse assessment result
            result = self._parse_pipeline_health_response(response)
            
            # Log assessment completion
            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "pipeline_health_assessment_complete",
                    {
                        "health_status": result.health_status,
                        "alert_level": result.alert_level,
                        "error_patterns_count": len(result.error_patterns)
                    }
                )
            
            return result
            
        except Exception as e:
            error_msg = f"Pipeline health assessment failed: {str(e)}"
            if self.audit_logger:
                self.audit_logger.log_error(
                    "pipeline_health_assessment_error",
                    error_msg,
                    {"agent": self.agent_name}
                )
            
            return PipelineHealthResult(
                health_status="critical",
                error_patterns=[],
                performance_issues=[],
                reliability_metrics={},
                recommended_actions=[],
                alert_level="critical"
            )
    
    def _parse_dimension_validation_response(self, response: str) -> DimensionValidationResult:
        """Parse LLM response for dimension validation."""
        try:
            # Extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                result_data = json.loads(json_match.group(0))
            else:
                result_data = json.loads(response)
            
            return DimensionValidationResult(
                validation_passed=result_data.get("validation_passed", False),
                missing_required_dimensions=result_data.get("missing_required_dimensions", []),
                missing_optional_dimensions=result_data.get("missing_optional_dimensions", []),
                present_dimensions=result_data.get("present_dimensions", []),
                impact_assessment=result_data.get("impact_assessment", "Unknown impact"),
                recommended_action=result_data.get("recommended_action", "FAIL_EXPERIMENT"),
                error_message=result_data.get("error_message")
            )
            
        except Exception as e:
            return DimensionValidationResult(
                validation_passed=False,
                missing_required_dimensions=[],
                missing_optional_dimensions=[],
                present_dimensions=[],
                impact_assessment=f"Failed to parse validation response: {str(e)}",
                recommended_action="FAIL_EXPERIMENT",
                error_message=f"Response parsing failed: {str(e)}"
            )
    
    def _parse_statistical_health_response(self, response: str) -> StatisticalHealthResult:
        """Parse LLM response for statistical health validation."""
        try:
            # Extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                result_data = json.loads(json_match.group(0))
            else:
                result_data = json.loads(response)
            
            return StatisticalHealthResult(
                validation_passed=result_data.get("validation_passed", False),
                calculation_failures=result_data.get("calculation_failures", []),
                perfect_correlations=result_data.get("perfect_correlations", []),
                statistical_warnings=result_data.get("statistical_warnings", []),
                sample_size_assessment=result_data.get("sample_size_assessment", "unknown"),
                recommended_action=result_data.get("recommended_action", "FAIL_EXPERIMENT"),
                error_message=result_data.get("error_message")
            )
            
        except Exception as e:
            return StatisticalHealthResult(
                validation_passed=False,
                calculation_failures=[],
                perfect_correlations=[],
                statistical_warnings=[],
                sample_size_assessment="unknown",
                recommended_action="FAIL_EXPERIMENT",
                error_message=f"Response parsing failed: {str(e)}"
            )
    
    def _parse_pipeline_health_response(self, response: str) -> PipelineHealthResult:
        """Parse LLM response for pipeline health assessment."""
        try:
            # Extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                result_data = json.loads(json_match.group(0))
            else:
                result_data = json.loads(response)
            
            return PipelineHealthResult(
                health_status=result_data.get("health_status", "critical"),
                error_patterns=result_data.get("error_patterns", []),
                performance_issues=result_data.get("performance_issues", []),
                reliability_metrics=result_data.get("reliability_metrics", {}),
                recommended_actions=result_data.get("recommended_actions", []),
                alert_level=result_data.get("alert_level", "critical")
            )
            
        except Exception as e:
            return PipelineHealthResult(
                health_status="critical",
                error_patterns=[],
                performance_issues=[],
                reliability_metrics={},
                recommended_actions=[],
                alert_level="critical"
            )
