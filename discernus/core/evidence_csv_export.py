#!/usr/bin/env python3
"""
Evidence CSV Export Module
=========================

This module generates evidence.csv from analysis artifacts.
This is deterministic Python code, not an LLM agent.
"""

import json
import csv
import io
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.audit_logger import AuditLogger


class EvidenceCSVExportModule:
    """Deterministic module for generating evidence.csv from analysis artifacts"""

    def __init__(self, artifact_storage: LocalArtifactStorage, audit_logger: AuditLogger):
        self.storage = artifact_storage
        self.audit = audit_logger
        self.module_name = "EvidenceCSVExportModule"
        
        self.audit.log_agent_event(self.module_name, "initialization", {
            "capabilities": ["deterministic_csv_generation", "evidence_extraction"]
        })

    def generate_evidence_csv(self, analysis_artifact_ids: List[str]) -> str:
        """Generate evidence.csv from analysis artifacts"""
        
        self.audit.log_agent_event(self.module_name, "csv_generation_start", {
            "num_artifacts": len(analysis_artifact_ids)
        })
        
        # Load all analysis artifacts and extract evidence
        evidence_rows = []
        
        for artifact_id in analysis_artifact_ids:
            artifact_content = self.storage.get_artifact(artifact_id)
            if not artifact_content:
                self.audit.log_agent_event(self.module_name, "artifact_load_error", {
                    "artifact_id": artifact_id,
                    "error": "Could not load artifact"
                })
                continue
            
            try:
                analysis_content = json.loads(artifact_content.decode('utf-8'))
                
                # Extract evidence from this analysis
                document_id = analysis_content.get('document_id', 'unknown')
                framework_name = analysis_content.get('framework_name', 'unknown')
                evidence_list = analysis_content.get('evidence', [])
                
                for evidence_item in evidence_list:
                    row = {
                        'document_id': document_id,
                        'framework_name': framework_name,
                        'dimension': evidence_item.get('dimension', ''),
                        'quote_text': evidence_item.get('quote', ''),
                        'source': evidence_item.get('source', ''),
                        'offset': evidence_item.get('offset', 0),
                        'confidence': evidence_item.get('confidence', 0.0)
                    }
                    evidence_rows.append(row)
                    
            except Exception as e:
                self.audit.log_agent_event(self.module_name, "artifact_parse_error", {
                    "artifact_id": artifact_id,
                    "error": str(e)
                })
                continue
        
        # Generate CSV content
        csv_content = self._generate_csv_content(evidence_rows)
        
        # Save CSV artifact
        csv_artifact_id = self.storage.put_artifact(
            csv_content.encode('utf-8'),
            {
                "artifact_type": "evidence_csv",
                "num_rows": len(evidence_rows),
                "generated_at": datetime.now(timezone.utc).isoformat()
            }
        )
        
        self.audit.log_agent_event(self.module_name, "csv_generation_complete", {
            "csv_artifact_id": csv_artifact_id,
            "num_rows": len(evidence_rows)
        })
        
        return csv_artifact_id
    
    def _generate_csv_content(self, evidence_rows: List[Dict[str, Any]]) -> str:
        """Generate CSV content from evidence rows"""
        
        if not evidence_rows:
            return "document_id,framework_name,dimension,quote_text,source,offset,confidence\n"
        
        # Define CSV fieldnames
        fieldnames = [
            'document_id',
            'framework_name', 
            'dimension',
            'quote_text',
            'source',
            'offset',
            'confidence'
        ]
        
        # Generate CSV content
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(evidence_rows)
        
        return output.getvalue()
    
    def get_evidence_summary(self, analysis_artifact_ids: List[str]) -> Dict[str, Any]:
        """Get a summary of evidence data for reporting"""
        
        evidence_rows = []
        dimension_counts = {}
        framework_counts = {}
        
        for artifact_id in analysis_artifact_ids:
            artifact_content = self.storage.get_artifact(artifact_id)
            if not artifact_content:
                continue
            
            try:
                analysis_content = json.loads(artifact_content.decode('utf-8'))
                evidence_list = analysis_content.get('evidence', [])
                
                framework_name = analysis_content.get('framework_name', 'unknown')
                framework_counts[framework_name] = framework_counts.get(framework_name, 0) + len(evidence_list)
                
                for evidence_item in evidence_list:
                    dimension = evidence_item.get('dimension', 'unknown')
                    dimension_counts[dimension] = dimension_counts.get(dimension, 0) + 1
                    
            except Exception:
                continue
        
        return {
            "total_evidence_items": sum(dimension_counts.values()),
            "dimension_counts": dimension_counts,
            "framework_counts": framework_counts,
            "num_documents": len(analysis_artifact_ids)
        }
