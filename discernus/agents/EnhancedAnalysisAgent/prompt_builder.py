#!/usr/bin/env python3
"""
Prompt Builder for the Enhanced Analysis Agent.

Handles the creation of LLM prompts for analysis.
"""

import base64
from typing import List, Dict


def format_documents_for_prompt(documents: List[Dict]) -> str:
    """Format documents for LLM prompt with enhanced metadata."""
    formatted = []
    for document in documents:
        formatted.append(
            f"=== DOCUMENT {document['index']} (base64 encoded) ===\n"
            f"Filename: {document.get('filename', 'unknown')}\n"
            f"Hash: {document['hash'][:12]}...\n"
            f"{document['content']}\n"
        )
    return "\n".join(formatted)


def create_analysis_prompt(
    prompt_template: str,
    analysis_id: str,
    framework_content: str,
    documents: List[Dict],
) -> str:
    """Create the full analysis prompt."""
    framework_b64 = base64.b64encode(framework_content.encode('utf-8')).decode('utf-8')

    return prompt_template.format(
        analysis_id=analysis_id,
        frameworks=f"=== FRAMEWORK 1 (base64 encoded) ===\n{framework_b64}\n",
        documents=format_documents_for_prompt(documents),
        num_frameworks=1,
        num_documents=len(documents)
    )


