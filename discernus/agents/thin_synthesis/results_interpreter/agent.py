#!/usr/bin/env python3
"""
ResultsInterpreter Agent

Synthesizes statistical results and curated evidence into narrative reports.
"""

import logging
import yaml
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from pathlib import Path

from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry
from discernus.core.audit_logger import AuditLogger
from .builders.prompt_builder import build_interpretation_prompt
from .builders.response_parser import parse_interpretation_response
from .builders.validator import validate_required_data


@dataclass
class InterpretationRequest:
    """Request structure for results interpretation."""
    statistical_results: Dict[str, Any]
    curated_evidence: Dict[str, List[Any]]
    framework_spec: str
    experiment_context: Optional[str] = None
    run_id: Optional[str] = None
    models_used: Optional[Dict[str, str]] = None
    execution_timestamp_utc: Optional[str] = None
    reporting_metadata: Optional[Dict[str, Any]] = None


@dataclass
class InterpretationResponse:
    """Response structure containing the final narrative report."""
    narrative_report: str
    success: bool
    word_count: int
    error_message: Optional[str] = None
    executive_summary: str = ""
    key_findings: List[str] = list
    methodology_notes: str = ""
    statistical_summary: Dict[str, Any] = dict
    evidence_integration_summary: Dict[str, Any] = dict


class ResultsInterpreter:
    """Synthesizes statistical results and curated evidence into narrative reports."""

    def __init__(self, model: str, audit_logger=None):
        self.model = model
        self.llm_gateway = LLMGateway(ModelRegistry())
        self.logger = logging.getLogger(__name__)
        self.audit_logger = audit_logger
        self.agent_name = "ResultsInterpreter"
        self.prompt_template = self._load_prompt_template()

        if self.audit_logger:
            self.audit_logger.log_agent_event(self.agent_name, "initialization", {"model": self.model})

    def _load_prompt_template(self) -> str:
        """Load the prompt template from YAML file."""
        prompt_file = Path(__file__).parent / "prompt.yaml"
        with open(prompt_file, 'r') as f:
            return yaml.safe_load(f)['template']

    def interpret_results(self, request: InterpretationRequest) -> InterpretationResponse:
        """Generate comprehensive narrative interpretation of results."""
        if self.audit_logger:
            self.audit_logger.log_agent_event(self.agent_name, "interpretation_start", {"run_id": request.run_id})
        try:
            if (error := validate_required_data(request)):
                self.logger.error(f"Interpretation failed: {error}")
                if self.audit_logger:
                    self.audit_logger.log_error("validation_failed", error, {"agent": self.agent_name})
                return InterpretationResponse(narrative_report="", success=False, word_count=0, error_message=error)

            prompt = build_interpretation_prompt(request, self.prompt_template)
            response_content, metadata = self.llm_gateway.execute_call(model=self.model, prompt=prompt)

            if self.audit_logger:
                self.audit_logger.log_llm_interaction(
                    model=self.model, prompt=prompt, response=response_content,
                    agent_name=self.agent_name, metadata={"operation": "interpretation"}
                )
            if not response_content or not metadata.get('success'):
                error_msg = metadata.get('error', 'Empty response from LLM')
                if self.audit_logger:
                    self.audit_logger.log_error("llm_call_failed", error_msg, {"agent": self.agent_name})
                return InterpretationResponse(
                    narrative_report="", success=False, word_count=0,
                    error_message=error_msg
                )

            response = parse_interpretation_response(response_content)
            if self.audit_logger:
                self.audit_logger.log_agent_event(self.agent_name, "interpretation_success", {"word_count": response.word_count})
            return response

        except Exception as e:
            self.logger.error(f"Results interpretation failed: {str(e)}")
            if self.audit_logger:
                self.audit_logger.log_error("interpretation_failed", str(e), {"agent": self.agent_name})
            return InterpretationResponse(narrative_report="", success=False, word_count=0, error_message=str(e)) 