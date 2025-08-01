#!/usr/bin/env python3
"""
CSV Export Agent - Gasket #3a (Pipeline-to-Human)
==================================================

Provides mid-point data export for researchers who want to use their own
statistical tools (R, SPSS, etc.) for final analysis and interpretation.

This agent implements Gasket #3a by creating clean CSV files with:
- Raw scores from analysis
- Calculated metrics (tensions, composite scores)
- Hash-linked evidence references
- Experiment and document metadata

Key Features:
- Framework-agnostic CSV generation
- Hash-linked evidence for provenance
- Multiple export formats (standard, R-friendly, etc.)
- Configurable export options
- THIN architecture compliance
"""

import os
import csv
import json
import logging
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from discernus.core.audit_logger import AuditLogger
from discernus.storage.minio_client import DiscernusArtifactClient


@dataclass
class ExportResult:
    """Result of CSV export operation with metadata."""
    success: bool
    export_path: str
    files_created: List[str]
    total_records: int
    export_time_seconds: float
    error_message: Optional[str] = None


@dataclass
class ExportOptions:
    """Configuration options for CSV export."""
    include_calculated_metrics: bool = True
    evidence_detail_level: str = "hashes_only"  # "hashes_only", "quotes", "full"
    export_format: str = "standard"  # "standard", "r_friendly", "spss_friendly"
    custom_column_names: Optional[Dict[str, str]] = None
    include_metadata: bool = True


class CSVExportError(Exception):
    """CSV Export Agent specific exceptions."""
    pass


class CSVExportAgent:
    """
    CSV Export Agent - Gasket #3a for Pipeline-to-Human interface.
    
    Provides clean CSV export for researchers who want to use external
    statistical tools for analysis and interpretation.
    """
    
    def __init__(self, audit_logger: Optional[AuditLogger] = None):
        """
        Initialize CSV Export Agent.
        
        Args:
            audit_logger: Optional audit logger for provenance tracking
        """
        self.agent_name = "CSVExportAgent"
        self.audit_logger = audit_logger
        
        # Initialize artifact client
        self.artifact_client = DiscernusArtifactClient()
        
        # Set up logging
        self.logger = logging.getLogger(__name__)
        
        # Log initialization
        if self.audit_logger:
            self.audit_logger.log_agent_event(
                self.agent_name,
                "initialization",
                {
                    "architecture": "csv_export_gasket",
                    "capabilities": ["csv_generation", "evidence_linking", "metadata_export"],
                    "gasket_type": "pipeline_to_human"
                }
            )
    
    def export_mid_point_data(
        self,
        scores_hash: str,
        evidence_hash: str,
        framework_config: Dict[str, Any],
        corpus_manifest: Dict[str, Any],
        export_path: str,
        export_options: Optional[ExportOptions] = None
    ) -> ExportResult:
        """
        Export clean CSV files for external analysis.
        
        This is the main method implementing Gasket #3a functionality.
        
        Args:
            scores_hash: Hash of the analysis scores artifact
            evidence_hash: Hash of the evidence artifact  
            framework_config: Framework configuration for context
            corpus_manifest: Corpus metadata
            export_path: Directory path for CSV file output
            export_options: Export configuration options
            
        Returns:
            ExportResult with export details and file paths
        """
        start_time = datetime.now()
        
        # Use default options if none provided
        if export_options is None:
            export_options = ExportOptions()
        
        # Log export start
        if self.audit_logger:
            self.audit_logger.log_agent_event(
                self.agent_name,
                "export_start",
                {
                    "scores_hash": scores_hash,
                    "evidence_hash": evidence_hash,
                    "export_path": export_path,
                    "export_options": export_options.__dict__
                }
            )
        
        try:
            # Create export directory
            os.makedirs(export_path, exist_ok=True)
            
            # Load analysis data
            analysis_data = self._load_analysis_data(scores_hash)
            evidence_data = self._load_evidence_data(evidence_hash) if evidence_hash != scores_hash else analysis_data
            
            # Generate CSV files
            files_created = []
            total_records = 0
            
            # 1. Generate scores.csv
            scores_file = self._generate_scores_csv(
                analysis_data, corpus_manifest, export_path, export_options
            )
            files_created.append(scores_file)
            total_records += len(analysis_data.get('document_analyses', []))
            
            # 2. Generate metrics.csv (if calculated metrics exist and requested)
            if export_options.include_calculated_metrics:
                metrics_file = self._generate_metrics_csv(
                    analysis_data, export_path, export_options
                )
                if metrics_file:
                    files_created.append(metrics_file)
            
            # 3. Generate evidence.csv
            evidence_file = self._generate_evidence_csv(
                evidence_data, export_path, export_options
            )
            files_created.append(evidence_file)
            
            # 4. Generate metadata.csv (if requested)
            if export_options.include_metadata:
                metadata_file = self._generate_metadata_csv(
                    analysis_data, framework_config, corpus_manifest, export_path, export_options
                )
                files_created.append(metadata_file)
            
            # Calculate export time
            export_time = (datetime.now() - start_time).total_seconds()
            
            # Log successful export
            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "export_success",
                    {
                        "files_created": files_created,
                        "total_records": total_records,
                        "export_time_seconds": export_time
                    }
                )
            
            return ExportResult(
                success=True,
                export_path=export_path,
                files_created=files_created,
                total_records=total_records,
                export_time_seconds=export_time
            )
            
        except Exception as e:
            export_time = (datetime.now() - start_time).total_seconds()
            
            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    self.agent_name,
                    "export_failure",
                    {
                        "error": str(e),
                        "error_type": type(e).__name__,
                        "export_time_seconds": export_time
                    }
                )
            
            return ExportResult(
                success=False,
                export_path=export_path,
                files_created=[],
                total_records=0,
                export_time_seconds=export_time,
                error_message=str(e)
            )
    
    def _load_analysis_data(self, scores_hash: str) -> Dict[str, Any]:
        """Load analysis data from artifact storage."""
        try:
            artifact_data = self.artifact_client.get_artifact(scores_hash)
            if not artifact_data:
                raise CSVExportError(f"Analysis artifact not found: {scores_hash}")
            
            return json.loads(artifact_data.decode('utf-8'))
            
        except Exception as e:
            raise CSVExportError(f"Failed to load analysis data: {e}")
    
    def _load_evidence_data(self, evidence_hash: str) -> Dict[str, Any]:
        """Load evidence data from artifact storage."""
        try:
            artifact_data = self.artifact_client.get_artifact(evidence_hash)
            if not artifact_data:
                raise CSVExportError(f"Evidence artifact not found: {evidence_hash}")
            
            return json.loads(artifact_data.decode('utf-8'))
            
        except Exception as e:
            raise CSVExportError(f"Failed to load evidence data: {e}")
    
    def _generate_scores_csv(
        self,
        analysis_data: Dict[str, Any],
        corpus_manifest: Dict[str, Any],
        export_path: str,
        export_options: ExportOptions
    ) -> str:
        """Generate scores.csv with raw dimensional scores."""
        filename = "scores.csv"
        filepath = os.path.join(export_path, filename)
        
        document_analyses = analysis_data.get('document_analyses', [])
        if not document_analyses:
            raise CSVExportError("No document analyses found in analysis data")
        
        # Collect all unique score keys from all documents
        all_score_keys = set()
        for doc in document_analyses:
            analysis_scores = doc.get('analysis_scores', {})
            all_score_keys.update(analysis_scores.keys())
        
        # Sort keys for consistent output
        score_columns = sorted(list(all_score_keys))
        
        # Define CSV headers
        headers = ['document_id', 'filename'] + score_columns + ['evidence_hash']
        
        # Apply custom column names if provided
        if export_options.custom_column_names:
            headers = [export_options.custom_column_names.get(h, h) for h in headers]
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            
            for doc in document_analyses:
                document_id = doc.get('document_id', 'unknown')
                document_name = doc.get('document_name', 'unknown')
                analysis_scores = doc.get('analysis_scores', {})
                
                # Create evidence hash for this document
                evidence_hash = self._create_evidence_hash(doc)
                
                # Build row data
                row = [document_id, document_name]
                
                # Add scores in consistent order
                for score_key in score_columns:
                    score_value = analysis_scores.get(score_key)
                    # Convert None to empty string for CSV
                    row.append(score_value if score_value is not None else '')
                
                row.append(evidence_hash)
                writer.writerow(row)
        
        self.logger.info(f"Generated {filename} with {len(document_analyses)} records")
        return filename
    
    def _generate_metrics_csv(
        self,
        analysis_data: Dict[str, Any],
        export_path: str,
        export_options: ExportOptions
    ) -> Optional[str]:
        """Generate metrics.csv with calculated metrics (tensions, composite scores)."""
        # For now, calculated metrics are included in the scores CSV
        # This could be extended in the future to separate them
        return None
    
    def _generate_evidence_csv(
        self,
        evidence_data: Dict[str, Any],
        export_path: str,
        export_options: ExportOptions
    ) -> str:
        """Generate evidence.csv with hash-linked evidence references."""
        filename = "evidence.csv"
        filepath = os.path.join(export_path, filename)
        
        headers = ['document_id', 'evidence_hash', 'dimension', 'score', 'quote_text', 'context_type']
        
        # Apply custom column names if provided
        if export_options.custom_column_names:
            headers = [export_options.custom_column_names.get(h, h) for h in headers]
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            
            # Extract evidence from document analyses
            document_analyses = evidence_data.get('document_analyses', [])
            for doc in document_analyses:
                document_id = doc.get('document_id', 'unknown')
                analysis_scores = doc.get('analysis_scores', {})
                evidence_hash = self._create_evidence_hash(doc)
                
                # For each score, create an evidence record
                for dimension, score in analysis_scores.items():
                    if score is not None:
                        # Create evidence row
                        quote_text = f"Evidence for {dimension}" if export_options.evidence_detail_level == "quotes" else ""
                        context_type = "analysis_based"
                        
                        row = [document_id, evidence_hash, dimension, score, quote_text, context_type]
                        writer.writerow(row)
        
        self.logger.info(f"Generated {filename}")
        return filename
    
    def _generate_metadata_csv(
        self,
        analysis_data: Dict[str, Any],
        framework_config: Dict[str, Any],
        corpus_manifest: Dict[str, Any],
        export_path: str,
        export_options: ExportOptions
    ) -> str:
        """Generate metadata.csv with experiment and document metadata."""
        filename = "metadata.csv"
        filepath = os.path.join(export_path, filename)
        
        headers = ['document_id', 'filename', 'framework_name', 'framework_version', 'export_timestamp', 'gasket_version']
        
        # Apply custom column names if provided
        if export_options.custom_column_names:
            headers = [export_options.custom_column_names.get(h, h) for h in headers]
        
        analysis_metadata = analysis_data.get('analysis_metadata', {})
        framework_name = framework_config.get('name', analysis_metadata.get('framework_name', 'unknown'))
        framework_version = framework_config.get('version', analysis_metadata.get('framework_version', 'unknown'))
        export_timestamp = datetime.now().isoformat()
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            
            document_analyses = analysis_data.get('document_analyses', [])
            for doc in document_analyses:
                document_id = doc.get('document_id', 'unknown')
                document_name = doc.get('document_name', 'unknown')
                
                # Get gasket version from extraction metadata
                extraction_metadata = doc.get('extraction_metadata', {})
                gasket_version = extraction_metadata.get('gasket_version', 'v7.0')
                
                row = [document_id, document_name, framework_name, framework_version, export_timestamp, gasket_version]
                writer.writerow(row)
        
        self.logger.info(f"Generated {filename}")
        return filename
    
    def _create_evidence_hash(self, document_analysis: Dict[str, Any]) -> str:
        """Create a hash for evidence linking."""
        # Create hash based on document content and scores
        document_id = document_analysis.get('document_id', '')
        analysis_scores = document_analysis.get('analysis_scores', {})
        
        # Create a stable string representation
        hash_content = f"{document_id}:{json.dumps(analysis_scores, sort_keys=True)}"
        
        # Generate SHA-256 hash
        return hashlib.sha256(hash_content.encode('utf-8')).hexdigest()[:16]
    
    def get_export_stats(self) -> Dict[str, Any]:
        """
        Get export statistics for monitoring and optimization.
        
        Returns:
            Dictionary with export performance metrics
        """
        return {
            "agent_name": self.agent_name,
            "gasket_type": "pipeline_to_human",
            "capabilities": ["csv_generation", "evidence_linking", "metadata_export"],
            "supported_formats": ["standard", "r_friendly", "spss_friendly"]
        }