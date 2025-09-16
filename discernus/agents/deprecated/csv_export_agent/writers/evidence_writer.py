#!/usr/bin/env python3
"""
CSV Evidence Writer for the Discernus Platform.

Handles the deterministic generation of evidence.csv files.
"""

import csv
import os
import logging
from typing import Dict, Any

from ..types import ExportOptions

logger = logging.getLogger(__name__)


def generate_evidence_csv(
    evidence_data: Dict[str, Any],
    export_path: str,
    export_options: ExportOptions,
    format_column_names_func,
    create_evidence_hash_func,
) -> str:
    """
    Generate evidence.csv with hash-linked evidence references.
    """
    filename = "evidence.csv"
    filepath = os.path.join(export_path, filename)

    headers = ['document_id', 'evidence_hash', 'dimension', 'score', 'quote_text', 'reasoning']
    headers = format_column_names_func(headers, export_options)

    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)

        # Handle both old document_analyses format and new pre-extracted evidence format
        if 'evidence_data' in evidence_data:
            # NEW: Pre-extracted evidence format
            evidence_items = evidence_data.get('evidence_data', [])
            for evidence_item in evidence_items:
                document_name = evidence_item.get('document_name', 'unknown')
                dimension = evidence_item.get('dimension', 'unknown')
                quote_text = evidence_item.get('quote_text', '')
                confidence = evidence_item.get('confidence', 0.0)
                context_type = evidence_item.get('context_type', 'unknown')
                evidence_hash = create_evidence_hash_func(evidence_item)

                # Create reasoning from available metadata
                reasoning = f"Confidence: {confidence}, Context: {context_type}"

                row = [document_name, evidence_hash, dimension, confidence, quote_text, reasoning]
                writer.writerow(row)
        else:
            # OLD: Document analyses format (fallback)
            document_analyses = evidence_data.get('document_analyses', [])
            for doc in document_analyses:
                document_id = doc.get('document_id', 'unknown')
                analysis_scores = doc.get('analysis_scores', {})
                evidence_hash = create_evidence_hash_func(doc)

                # For each score, create an evidence record
                for dimension, score in analysis_scores.items():
                    if score is not None:
                        # Extract quote and reasoning based on detail level
                        quote_text = ""
                        reasoning = ""

                        if export_options.evidence_detail_level in ["quotes", "full"]:
                            # Try to extract evidence from document if available
                            quote_text = f"Evidence for {dimension}"
                            if export_options.evidence_detail_level == "full":
                                reasoning = f"Analysis reasoning for {dimension} score: {score}"

                        row = [document_id, evidence_hash, dimension, score, quote_text, reasoning]
                        writer.writerow(row)

    logger.info(f"Generated {filename}")
    return filename
