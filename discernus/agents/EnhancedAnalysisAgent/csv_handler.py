#!/usr/bin/env python3
"""
CSV Handler - THIN Component
============================

Handles CSV extraction and persistence for analysis results.
Pure software component - no LLM intelligence.
"""

import re
from pathlib import Path
from typing import Optional, Tuple

from discernus.core.local_artifact_storage import LocalArtifactStorage


class CSVHandler:
    """
    Handles CSV extraction from LLM responses and persistence to artifacts.
    
    THIN Principle: Pure software CSV processing.
    Mechanical extraction and storage operations only.
    """
    
    def __init__(self, storage: LocalArtifactStorage, provenance_metadata: dict):
        self.storage = storage
        self.provenance_metadata = provenance_metadata
    
    def extract_embedded_csv(self, analysis_response: str, artifact_id: str) -> Tuple[str, str]:
        """
        Extract pre-formatted CSV segments from an LLM response.
        
        Args:
            analysis_response: Raw LLM response containing embedded CSVs
            artifact_id: Artifact ID to replace placeholder
            
        Returns:
            Tuple of (scores_csv, evidence_csv)
        """
        # Find the last occurrence of each delimiter
        scores_start = analysis_response.rfind("<<<DISCERNUS_SCORES_CSV_v1>>>")
        scores_end = analysis_response.rfind("<<<END_DISCERNUS_SCORES_CSV_v1>>>")
        evidence_start = analysis_response.rfind("<<<DISCERNUS_EVIDENCE_CSV_v1>>>")
        evidence_end = analysis_response.rfind("<<<END_DISCERNUS_EVIDENCE_CSV_v1>>>")
        
        # Extract CSV sections if found
        scores_csv = ""
        evidence_csv = ""
        
        if scores_start >= 0 and scores_end > scores_start:
            scores_csv = analysis_response[scores_start + len("<<<DISCERNUS_SCORES_CSV_v1>>>"):scores_end].strip()
            
        if evidence_start >= 0 and evidence_end > evidence_start:
            evidence_csv = analysis_response[evidence_start + len("<<<DISCERNUS_EVIDENCE_CSV_v1>>>"):evidence_end].strip()
        
        # Replace placeholder with actual artifact ID
        scores_csv = scores_csv.replace("{artifact_id}", artifact_id)
        evidence_csv = evidence_csv.replace("{artifact_id}", artifact_id)
        
        return scores_csv, evidence_csv
    
    def append_to_csv_artifact(self, current_hash: Optional[str], new_csv_data: str, 
                              artifact_name: str) -> Optional[str]:
        """
        Append CSV data to existing artifact or create new one.
        
        Args:
            current_hash: Hash of existing CSV artifact (if any)
            new_csv_data: New CSV data to append
            artifact_name: Name of the artifact (e.g., "scores.csv")
            
        Returns:
            Hash of the updated artifact
        """
        if not new_csv_data.strip():
            return current_hash
        
        # Load existing CSV content if available
        existing_content = ""
        if current_hash:
            try:
                existing_bytes = self.storage.get_artifact(current_hash)
                existing_content = existing_bytes.decode('utf-8')
            except Exception as e:
                print(f"⚠️ Could not load existing CSV artifact {current_hash}: {e}")
                existing_content = ""
        
        # Append new data (handle headers properly)
        if existing_content.strip():
            # Skip header line in new data if existing content has data
            new_lines = new_csv_data.strip().split('\n')
            if len(new_lines) > 1:
                # Skip first line (header) when appending
                data_to_append = '\n'.join(new_lines[1:])
                updated_csv_content = existing_content.rstrip() + '\n' + data_to_append
            else:
                # Only header line in new data, don't append
                updated_csv_content = existing_content
        else:
            # No existing content, use new data as-is
            updated_csv_content = new_csv_data
        
        # Store updated content with provenance metadata
        metadata = {
            **self.provenance_metadata,
            "artifact_type": f"intermediate_{artifact_name}",
            "appended_from": current_hash
        }
        
        new_hash = self.storage.put_artifact(
            updated_csv_content.encode('utf-8'),
            metadata
        )
        
        return new_hash
    
    def extract_and_persist_csvs(self, analysis_response: str, artifact_id: str,
                                current_scores_hash: Optional[str], 
                                current_evidence_hash: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
        """
        Extract CSVs from response and persist to artifacts.
        
        Args:
            analysis_response: Raw LLM response
            artifact_id: Artifact ID for CSV content
            current_scores_hash: Current scores artifact hash
            current_evidence_hash: Current evidence artifact hash
            
        Returns:
            Tuple of (new_scores_hash, new_evidence_hash)
        """
        scores_csv, evidence_csv = self.extract_embedded_csv(analysis_response, artifact_id)
        
        new_scores_hash = self.append_to_csv_artifact(
            current_scores_hash, scores_csv, "scores.csv"
        )
        new_evidence_hash = self.append_to_csv_artifact(
            current_evidence_hash, evidence_csv, "evidence.csv"
        )
        
        return new_scores_hash, new_evidence_hash