#!/usr/bin/env python3
"""
Framework Dimension Validator for the Reliability Analysis Agent.
"""

from typing import Dict, Any
from datetime import datetime

from ..agent import DimensionValidationResult


def validate_framework_dimensions(
    agent,
    framework_content: str,
    analysis_results: str,
    **kwargs,
) -> DimensionValidationResult:
    """
    Validate that all required framework dimensions were detected in analysis results.
    """
    try:
        if agent.audit_logger:
            agent.audit_logger.log_agent_event(
                agent.agent_name, "framework_dimension_validation_started",
                {"framework_length": len(framework_content), "analysis_results_length": len(analysis_results)}
            )

        prompt_template = agent.prompts.get("framework_dimension_validation", {}).get("template", "")
        if not prompt_template:
            raise ValueError("Framework dimension validation prompt template not found")

        validation_prompt = prompt_template.format(
            current_date=datetime.now().strftime("%Y-%m-%d"),
            framework_content=framework_content,
            analysis_results=analysis_results,
            **kwargs
        )

        response, metadata = agent.llm_gateway.execute_call(
            model=agent.model,
            prompt=validation_prompt,
            system_prompt="You are a reliability analysis expert for the Discernus research platform."
        )

        if agent.audit_logger:
            agent.audit_logger.log_agent_event(
                agent.agent_name, "framework_dimension_validation_response",
                {"response_length": len(response), "metadata": metadata}
            )

        result = agent._parse_dimension_validation_response(response)

        if agent.audit_logger:
            agent.audit_logger.log_agent_event(
                agent.agent_name, "framework_dimension_validation_complete",
                {
                    "validation_passed": result.validation_passed,
                    "missing_required_count": len(result.missing_required_dimensions),
                    "recommended_action": result.recommended_action
                }
            )
        return result

    except Exception as e:
        error_msg = f"Framework dimension validation failed: {str(e)}"
        if agent.audit_logger:
            agent.audit_logger.log_error("framework_dimension_validation_error", error_msg, {"agent": agent.agent_name})
        return DimensionValidationResult(
            validation_passed=False,
            missing_required_dimensions=[],
            missing_optional_dimensions=[],
            present_dimensions=[],
            impact_assessment="Validation failed due to system error",
            recommended_action="FAIL_EXPERIMENT",
            error_message=error_msg
        )


