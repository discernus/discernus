#!/usr/bin/env python3
"""
Parsing Utilities for the Discernus Platform.

Provides robust, THIN-compliant parsing functions to handle LLM outputs,
gracefully managing common formatting issues and ensuring reliable data extraction.
"""

import json
import re
from typing import Dict, Any, Optional

from discernus.gateway.llm_gateway import LLMGateway
from discernus.core.audit_logger import AuditLogger


def _request_llm_json_reformat(
    raw_response: str,
    model: str,
    llm_gateway: LLMGateway,
    audit_logger: Optional[AuditLogger] = None,
) -> Dict[str, Any]:
    """
    Requests an LLM to reformat a raw string into a valid JSON object.

    This is a fallback mechanism used when standard JSON parsing fails.

    Args:
        raw_response: The malformed string response from a previous LLM call.
        model: The name of the model to use for the reformatting task.
        llm_gateway: The LLM gateway instance to execute the call.
        audit_logger: The audit logger for provenance.

    Returns:
        A dictionary parsed from the LLM's reformatted response.

    Raises:
        json.JSONDecodeError: If the LLM also fails to return valid JSON.
    """
    reformat_prompt = (
        "The following text is a response from an AI that was expected to be a "
        "valid JSON object, but it is malformed. Please extract and return only "
        "the JSON object from this text, ensuring it is correctly formatted. "
        "Do not add any commentary, explanations, or markdown formatting. "
        "Only return the raw JSON.\n\n"
        f"Malformed text:\n---\n{raw_response}\n---"
    )

    if audit_logger:
        audit_logger.log_agent_event(
            "parsing_utils",
            "llm_reformat_request",
            {"original_response_length": len(raw_response), "model": model},
        )

    response, metadata = llm_gateway.execute_call(
        model=model,
        prompt=reformat_prompt,
        system_prompt="You are a JSON formatting expert.",
    )

    try:
        # Attempt to parse the reformatted response
        parsed_response = json.loads(response)
        if audit_logger:
            audit_logger.log_agent_event(
                "parsing_utils",
                "llm_reformat_success",
                {"reformatted_response_length": len(response)},
            )
        return parsed_response
    except json.JSONDecodeError as e:
        if audit_logger:
            audit_logger.log_error(
                "parsing_utils.llm_reformat_failed",
                f"LLM reformatting also failed to produce valid JSON: {e}",
                {"reformatted_response": response},
            )
        # Re-raise the exception to indicate a hard failure
        raise e


def parse_llm_json_response(
    response: str,
    llm_gateway: LLMGateway,
    model: str,
    audit_logger: Optional[AuditLogger] = None,
) -> Dict[str, Any]:
    """
    Parses a JSON object from an LLM response with robust fallbacks.

    This function attempts to:
    1. Directly parse the response as JSON.
    2. Extract a JSON object from within markdown code blocks.
    3. As a last resort, ask another LLM to reformat the response into valid JSON.

    Args:
        response: The raw string response from the LLM.
        llm_gateway: The LLM gateway for the reformatting fallback.
        model: The model to use for the reformatting fallback.
        audit_logger: The audit logger for provenance.

    Returns:
        A dictionary containing the parsed JSON data.

    Raises:
        ValueError: If parsing fails through all mechanisms.
    """
    try:
        # Attempt 1: Direct parsing
        return json.loads(response)
    except json.JSONDecodeError:
        # Attempt 2: Extract from markdown code block
        json_match = re.search(r"```json\n(\{.*?\})\n```", response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass  # Fall through to the next attempt

        # Attempt 3: Regex search for any JSON object
        json_match_any = re.search(r"\{.*\}", response, re.DOTALL)
        if json_match_any:
            try:
                return json.loads(json_match_any.group(0))
            except json.JSONDecodeError:
                pass # Fall through to the LLM reformat

    # Attempt 4: LLM-based reformatting as a final fallback
    try:
        if audit_logger:
            audit_logger.log_agent_event(
                "parsing_utils",
                "invoking_llm_reformat_fallback",
                {"response_snippet": response[:100]},
            )
        return _request_llm_json_reformat(response, model, llm_gateway, audit_logger)
    except json.JSONDecodeError:
        raise ValueError("Failed to parse LLM response after all fallbacks.")


