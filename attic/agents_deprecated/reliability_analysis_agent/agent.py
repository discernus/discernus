#!/usr/bin/env python3
"""
ReliabilityAnalysisAgent

Orchestrates reliability analysis using modular validator components.
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
from discernus.core.parsing_utils import parse_llm_json_response
from .types import DimensionValidationResult, StatisticalHealthResult, PipelineHealthResult
from .validators.dimension_validator import validate_framework_dimensions
from .validators.statistical_validator import validate_statistical_health
from .validators.pipeline_validator import assess_pipeline_health


class ReliabilityAnalysisAgent:
    """Orchestrates reliability analysis using modular validators."""

    def __init__(self, model: str = "vertex_ai/gemini-2.5-pro", audit_logger: Optional[AuditLogger] = None):
        self.agent_name = "ReliabilityAnalysisAgent"
        self.model = model
        self.audit_logger = audit_logger
        self.llm_gateway = LLMGateway(ModelRegistry())
        self.prompts = self._load_prompts()
        if self.audit_logger:
            self.audit_logger.log_agent_event(self.agent_name, "agent_initialized", {"model": self.model})

    def _load_prompts(self) -> Dict[str, Any]:
        """Load YAML prompt templates."""
        try:
            prompt_file = Path(__file__).parent / "prompt.yaml"
            with open(prompt_file, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Warning: Failed to load prompts for {self.agent_name}: {e}")
            return {}

    def _reformat_and_parse_with_llm(self, response: str) -> Dict[str, Any]:
        """Fallback to ask an LLM to reformat the JSON."""
        return parse_llm_json_response(response, self.llm_gateway, self.model, self.audit_logger)

    def validate_framework_dimensions(self, framework_content: str, analysis_results: str, **kwargs) -> DimensionValidationResult:
        return validate_framework_dimensions(self, framework_content, analysis_results, **kwargs)

    def validate_statistical_health(self, statistical_results: str, **kwargs) -> StatisticalHealthResult:
        return validate_statistical_health(self, statistical_results, **kwargs)

    def assess_pipeline_health(self, audit_logs: str, pipeline_artifacts: Dict[str, Any], **kwargs) -> PipelineHealthResult:
        return assess_pipeline_health(self, audit_logs, pipeline_artifacts, **kwargs)

    def _parse_dimension_validation_response(self, response: str) -> DimensionValidationResult:
        """Parse LLM response for dimension validation."""
        try:
            result_data = self._reformat_and_parse_with_llm(response)
            return DimensionValidationResult(**result_data)
        except (json.JSONDecodeError, ValueError, TypeError) as e:
            return DimensionValidationResult(
                validation_passed=False, missing_required_dimensions=[], missing_optional_dimensions=[],
                present_dimensions=[], impact_assessment=f"Failed to parse validation response: {e}",
                recommended_action="FAIL_EXPERIMENT", error_message=f"Response parsing failed: {e}"
            )

    def _parse_statistical_health_response(self, response: str) -> StatisticalHealthResult:
        """Parse LLM response for statistical health validation."""
        try:
            result_data = self._reformat_and_parse_with_llm(response)
            return StatisticalHealthResult(**result_data)
        except (json.JSONDecodeError, ValueError, TypeError) as e:
            return StatisticalHealthResult(
                validation_passed=False, calculation_failures=[], perfect_correlations=[],
                statistical_warnings=[], sample_size_assessment="unknown",
                recommended_action="FAIL_EXPERIMENT", error_message=f"Response parsing failed: {e}"
            )

    def _parse_pipeline_health_response(self, response: str) -> PipelineHealthResult:
        """Parse LLM response for pipeline health assessment."""
        try:
            result_data = self._reformat_and_parse_with_llm(response)
            return PipelineHealthResult(**result_data)
        except (json.JSONDecodeError, ValueError, TypeError) as e:
            return PipelineHealthResult(
                health_status="critical", error_patterns=[], performance_issues=[],
                reliability_metrics={}, recommended_actions=[], alert_level="critical"
            )
