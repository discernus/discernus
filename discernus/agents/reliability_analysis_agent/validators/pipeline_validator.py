#!/usr/bin/env python3
"""
Pipeline Health Validator for the Reliability Analysis Agent.
"""

import json
from typing import Dict, Any
from datetime import datetime

from ..types import PipelineHealthResult


def assess_pipeline_health(
    agent,
    audit_logs: str,
    pipeline_artifacts: Dict[str, Any],
    **kwargs,
) -> PipelineHealthResult:
    """
    Assess overall pipeline health from audit logs and artifacts.
    """
    try:
        if agent.audit_logger:
            agent.audit_logger.log_agent_event(
                agent.agent_name, "pipeline_health_assessment_started",
                {"audit_logs_length": len(audit_logs), "artifacts_count": len(pipeline_artifacts)}
            )

        prompt_template = agent.prompts.get("pipeline_health_assessment", {}).get("template", "")
        if not prompt_template:
            raise ValueError("Pipeline health assessment prompt template not found")

        assessment_prompt = prompt_template.format(
            current_date=datetime.now().strftime("%Y-%m-%d"),
            audit_logs=audit_logs,
            pipeline_artifacts=json.dumps(pipeline_artifacts, indent=2),
            **kwargs
        )

        response, metadata = agent.llm_gateway.execute_call(
            model=agent.model,
            prompt=assessment_prompt,
            system_prompt="You are a pipeline reliability expert for the Discernus research platform."
        )

        if agent.audit_logger:
            agent.audit_logger.log_agent_event(
                agent.agent_name, "pipeline_health_assessment_response",
                {"response_length": len(response), "metadata": metadata}
            )

        result = agent._parse_pipeline_health_response(response)

        if agent.audit_logger:
            agent.audit_logger.log_agent_event(
                agent.agent_name, "pipeline_health_assessment_complete",
                {
                    "health_status": result.health_status,
                    "alert_level": result.alert_level,
                    "error_patterns_count": len(result.error_patterns)
                }
            )
        return result

    except Exception as e:
        error_msg = f"Pipeline health assessment failed: {str(e)}"
        if agent.audit_logger:
            agent.audit_logger.log_error("pipeline_health_assessment_error", error_msg, {"agent": agent.agent_name})
        return PipelineHealthResult(
            health_status="critical",
            error_patterns=[],
            performance_issues=[],
            reliability_metrics={},
            recommended_actions=[],
            alert_level="critical"
        )


