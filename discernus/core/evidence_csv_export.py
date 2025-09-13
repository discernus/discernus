#!/usr/bin/env python3
"""
Evidence CSV Export Module
=========================

Deterministic module for generating evidence.csv from analysis artifacts.
This replaces LLM-based CSV generation to avoid output token constraints.
"""

import json
import csv
from pathlib import Path
from typing import Dict, Any, List, Optional
from io import StringIO

from discernus.core.local_artifact_storage import LocalArtifactStorage


class EvidenceCSVExportModule:
    """Deterministic evidence CSV export module"""
    
    def __init__(self, storage: LocalArtifactStorage):
        """
        Initialize the evidence CSV export module
        
        Args:
            storage: The artifact storage instance
        """
        self.storage = storage
    
    def generate_evidence_csv(self, analysis_artifacts: List[str]) -> Dict[str, Any]:
        """
        Generate evidence.csv from analysis artifacts
        
        Args:
            analysis_artifacts: List of analysis artifact IDs
            
        Returns:
            Dictionary with success status and artifact information
        """
        try:
            evidence_data = []
            
            # Process each analysis artifact
            for artifact_id in analysis_artifacts:
                if not artifact_id.endswith("_analysis.json"):
                    continue  # Skip non-analysis artifacts
                
                try:
                    # Load analysis artifact
                    artifact_content = self.storage.get_artifact(artifact_id)
                    analysis_data = json.loads(artifact_content.decode('utf-8'))
                    
                    # Extract evidence data
                    document_analyses = analysis_data.get("document_analyses", [])
                    
                    for doc_analysis in document_analyses:
                        document_id = doc_analysis.get("document_id", "unknown")
                        document_name = doc_analysis.get("document_name", "unknown")
                        evidence_list = doc_analysis.get("evidence", [])
                        
                        for evidence_item in evidence_list:
                            evidence_data.append({
                                "document_id": document_id,
                                "document_name": document_name,
                                "dimension": evidence_item.get("dimension", ""),
                                "quote_text": evidence_item.get("quote_text", ""),
                                "confidence": evidence_item.get("confidence", 0.0),
                                "context_type": evidence_item.get("context_type", "")
                            })
                
                except Exception as e:
                    # Skip corrupted artifacts but continue processing
                    print(f"Warning: Could not process artifact {artifact_id}: {e}")
                    continue
            
            if not evidence_data:
                return {
                    "success": False,
                    "error": "No evidence data found in analysis artifacts"
                }
            
            # Generate CSV content
            csv_content = self._generate_csv_content(evidence_data)
            
            # Store CSV artifact
            csv_artifact_id = self.storage.put_artifact(
                csv_content.encode('utf-8'),
                {
                    "artifact_type": "evidence_csv",
                    "source_artifacts": analysis_artifacts,
                    "row_count": len(evidence_data)
                }
            )
            
            return {
                "success": True,
                "artifacts": [csv_artifact_id],
                "row_count": len(evidence_data),
                "csv_size_bytes": len(csv_content)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to generate evidence CSV: {e}"
            }
    
    def _generate_csv_content(self, evidence_data: List[Dict[str, Any]]) -> str:
        """
        Generate CSV content from evidence data
        
        Args:
            evidence_data: List of evidence records
            
        Returns:
            CSV content as string
        """
        if not evidence_data:
            return ""
        
        # Create CSV in memory
        output = StringIO()
        fieldnames = ["document_id", "document_name", "dimension", "quote_text", "confidence", "context_type"]
        
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        
        for record in evidence_data:
            writer.writerow(record)
        
        return output.getvalue()
    
    def get_evidence_summary(self, analysis_artifacts: List[str]) -> Dict[str, Any]:
        """
        Get a summary of evidence data without generating the full CSV
        
        Args:
            analysis_artifacts: List of analysis artifact IDs
            
        Returns:
            Evidence summary statistics
        """
        try:
            total_evidence = 0
            dimensions = set()
            documents = set()
            
            for artifact_id in analysis_artifacts:
                if not artifact_id.endswith("_analysis.json"):
                    continue
                
                try:
                    artifact_content = self.storage.get_artifact(artifact_id)
                    analysis_data = json.loads(artifact_content.decode('utf-8'))
                    
                    document_analyses = analysis_data.get("document_analyses", [])
                    
                    for doc_analysis in document_analyses:
                        document_name = doc_analysis.get("document_name", "unknown")
                        documents.add(document_name)
                        
                        evidence_list = doc_analysis.get("evidence", [])
                        total_evidence += len(evidence_list)
                        
                        for evidence_item in evidence_list:
                            dimension = evidence_item.get("dimension", "")
                            if dimension:
                                dimensions.add(dimension)
                
                except Exception:
                    continue
            
            return {
                "total_evidence_items": total_evidence,
                "unique_dimensions": len(dimensions),
                "unique_documents": len(documents),
                "dimensions": sorted(list(dimensions)),
                "documents": sorted(list(documents))
            }
            
        except Exception as e:
            return {
                "error": f"Failed to generate evidence summary: {e}"
            }