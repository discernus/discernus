#!/usr/bin/env python3
"""
Data Extraction Agent - THIN agent for tidying raw analysis data
================================================================

THIN Principle: This agent acts as a classic "Tool-Using" agent. It takes a
machine-readable input (the conversation.jsonl log) and uses a deterministic
Python script to transform it into another machine-readable format (a CSV),
making it immediately available for statistical analysis.
"""

import sys
import json
import csv
import re
from pathlib import Path
from typing import Dict, Any, List, Optional

class DataExtractionAgent:
    """
    Parses a conversation log to extract structured numerical data into a
    tidy CSV format.
    """

    def extract_tidy_data(self, conversation_log_path: str, output_csv_path: str, framework_content: str):
        """
        Reads a JSONL conversation log, extracts analysis data, and writes a CSV.

        Args:
            conversation_log_path: Path to the input conversation.jsonl file.
            output_csv_path: Path to write the output results.csv file.
            framework_content: The full content of the framework.md file to identify metrics.
        """
        print(f"DataExtractionAgent: Starting data extraction from {conversation_log_path}")

        records = []
        with open(conversation_log_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    log_entry = json.loads(line)
                    # We only care about responses from analysis agents
                    if not log_entry.get('speaker', '').startswith('analysis_agent'):
                        continue

                    # The actual analysis is often in a JSON block inside the message
                    message_content = log_entry.get('message', '')
                    json_match = re.search(r'```json\n(.*?)\n```', message_content, re.DOTALL)
                    
                    if not json_match:
                        continue
                        
                    analysis_json_str = json_match.group(1)
                    analysis_data = json.loads(analysis_json_str)
                    
                    # --- Core Record Creation ---
                    # The 'metadata' in the log entry has the model name and other details
                    metadata = log_entry.get('metadata', {})
                    base_record = {
                        'session_id': metadata.get('session_id', 'unknown'),
                        'run_num': metadata.get('run_num', 1),
                        'model_name': metadata.get('model_name', 'unknown'),
                        'corpus_file': metadata.get('file_name', 'unknown'),
                    }

                    # --- Score Extraction ---
                    # Assumes scores are in a nested dictionary (e.g., pdaf_v1_1_scores)
                    # This part might need to be more robust or framework-aware
                    score_data = next((v for k, v in analysis_data.items() if 'scores' in k.lower()), None)
                    if not score_data:
                        continue

                    for anchor, values in score_data.items():
                        if isinstance(values, dict):
                            record = base_record.copy()
                            record['anchor'] = anchor
                            record['score'] = values.get('score')
                            # Also capture classification for anchors like MFT's economic direction
                            record['classification'] = values.get('classification')
                            records.append(record)

                except (json.JSONDecodeError, AttributeError) as e:
                    # Silently skip lines that are not valid JSON or don't have the expected structure
                    continue
        
        if not records:
            print("DataExtractionAgent: No valid analysis records found to extract.")
            return

        # --- Write to CSV ---
        # Dynamically determine headers from the first record
        headers = list(records[0].keys())
        
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(records)

        print(f"DataExtractionAgent: Successfully wrote {len(records)} records to {output_csv_path}")

    def get_thin_compliance(self) -> Dict[str, Any]:
        """Returns THIN compliance information for this agent."""
        return {
            "thin_compliant": True,
            "archetype": "Tool-Using",
            "description": "Performs a deterministic data transformation from JSONL to CSV using standard Python libraries. No LLM calls are made.",
            "issues": []
        } 