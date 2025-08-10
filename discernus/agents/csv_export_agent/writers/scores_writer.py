#!/usr/bin/env python3
"""
CSV Scores Writer for the Discernus Platform.

Handles the deterministic generation of scores.csv files.
"""

import csv
import os
import logging
from typing import Dict, Any, List

from ..agent import ExportOptions, CSVExportError

logger = logging.getLogger(__name__)


def generate_scores_csv(
    analysis_data: Dict[str, Any],
    export_path: str,
    export_options: ExportOptions,
    format_column_names_func,
    create_evidence_hash_func,
) -> str:
    """
    Generate scores.csv with raw dimensional scores and calculated metrics.
    """
    filename = "scores.csv"
    filepath = os.path.join(export_path, filename)

    document_analyses = analysis_data.get('document_analyses', [])
    if not document_analyses:
        raise CSVExportError("No document analyses found in analysis data")

    # Dynamically discover all score columns (framework-agnostic)
    all_score_keys = set()
    for doc in document_analyses:
        analysis_scores = doc.get('analysis_scores', {})
        all_score_keys.update(analysis_scores.keys())

    # Sort keys for consistent output
    score_columns = sorted(list(all_score_keys))

    # Define CSV headers
    headers = ['document_id', 'filename'] + score_columns + ['evidence_hash']

    # Apply column name formatting based on export format
    headers = format_column_names_func(headers, export_options)

    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)

        for doc in document_analyses:
            document_id = doc.get('document_id', 'unknown')
            document_name = doc.get('document_name', 'unknown')
            analysis_scores = doc.get('analysis_scores', {})

            # Create evidence hash for this document
            evidence_hash = create_evidence_hash_func(doc)

            # Build row data
            row = [document_id, document_name]

            # Add scores in consistent order
            for score_key in score_columns:
                score_value = analysis_scores.get(score_key)
                # Convert None to empty string for CSV
                row.append(score_value if score_value is not None else '')

            row.append(evidence_hash)
            writer.writerow(row)

    logger.info(f"Generated {filename} with {len(document_analyses)} records")
    return filename
