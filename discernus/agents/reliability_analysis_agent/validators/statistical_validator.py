#!/usr/bin/env python3
"""
Statistical Health Validator for the Reliability Analysis Agent.
"""

from typing import Dict, Any
from datetime import datetime

from ..agent import StatisticalHealthResult


def validate_statistical_health(
    agent,
    statistical_results: str,
    **kwargs,
) -> StatisticalHealthResult:
    """
    Validate statistical calculation health and identify data quality issues.
    """
    try:
        if agent.audit_logger:
            agent.audit_logger.log_agent_event(
                agent.agent_name, "statistical_health_validation_started",
                {"statistical_results_length": len(statistical_results)}
            )

        prompt_template = agent.prompts.get("statistical_health_validation", {}).get("template", "")
        if not prompt_template:
            raise ValueError("Statistical health validation prompt template not found")

        validation_prompt = prompt_template.format(
            current_date=datetime.now().strftime("%Y-%m-%d"),
            statistical_results=statistical_results,
            **kwargs
        )

        response, metadata = agent.llm_gateway.execute_call(
            model=agent.model,
            prompt=validation_prompt,
            system_prompt="You are a statistical analysis expert for the Discernus research platform."
        )

        if agent.audit_logger:
            agent.audit_logger.log_agent_event(
                agent.agent_name, "statistical_health_validation_response",
                {"response_length": len(response), "metadata": metadata}
            )

        result = agent._parse_statistical_health_response(response)

        if agent.audit_logger:
            agent.audit_logger.log_agent_event(
                agent.agent_name, "statistical_health_validation_complete",
                {
                    "validation_passed": result.validation_passed,
                    "calculation_failures_count": len(result.calculation_failures),
                    "recommended_action": result.recommended_action
                }
            )
        return result

    except Exception as e:
        error_msg = f"Statistical health validation failed: {str(e)}"
        if agent.audit_logger:
            agent.audit_logger.log_error("statistical_health_validation_error", error_msg, {"agent": agent.agent_name})
        return StatisticalHealthResult(
            validation_passed=False,
            calculation_failures=[],
            perfect_correlations=[],
            statistical_warnings=[],
            sample_size_assessment="unknown",
            recommended_action="FAIL_EXPERIMENT",
            error_message=error_msg
        )


