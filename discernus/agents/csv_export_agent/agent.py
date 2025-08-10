#!/usr/bin/env python3
"""
CSV Export Agent - Gasket #3a (Pipeline-to-Human)
==================================================

Deterministic CSV export agent that generates clean CSV files from MathToolkit
structured data. Framework-agnostic design that dynamically adapts to any
framework's output structure.
"""

import csv
import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

from discernus.core.audit_logger import AuditLogger
from .types import ExportResult, ExportOptions, CSVExportError
from .writers.scores_writer import generate_scores_csv
from .writers.evidence_writer import generate_evidence_csv
from .writers.metadata_writer import generate_metadata_csv, generate_final_metadata_csv
from .writers.stats_writer import generate_statistical_results_csv


class CSVExportAgent:
    """
    CSV Export Agent - Gasket #3a for Pipeline-to-Human interface.

    Deterministic implementation that generates CSV files from structured
    MathToolkit data without requiring LLM calls.
    """

    def __init__(self, audit_logger: Optional[AuditLogger] = None):
        """
        Initialize CSV Export Agent.

        Args:
            audit_logger: Optional audit logger for provenance
        """
        self.agent_name = "CSVExportAgent"
        self.audit_logger = audit_logger
        self.logger = logging.getLogger(__name__)
        self.artifact_storage = None

        if self.audit_logger:
            self.audit_logger.log_agent_event(
                self.agent_name,
                "initialization",
                {
                    "architecture": "deterministic_csv_export",
                    "capabilities": ["csv_generation", "evidence_linking", "metadata_export"],
                    "gasket_type": "pipeline_to_human",
                    "framework_agnostic": True
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
        """Export mid-point data after analysis completion (analysis-only mode)."""
        start_time = datetime.now()
        export_options = export_options or ExportOptions()

        if self.audit_logger:
            self.audit_logger.log_agent_event(
                self.agent_name, "export_start",
                {"scores_hash": scores_hash, "evidence_hash": evidence_hash, "export_path": export_path,
                 "export_options": export_options.__dict__}
            )

        try:
            os.makedirs(export_path, exist_ok=True)
            analysis_data = self._load_artifact_data(scores_hash)
            evidence_data = self._load_artifact_data(evidence_hash) if evidence_hash != scores_hash else analysis_data

            files_created = [
                generate_scores_csv(analysis_data, export_path, export_options, self._format_column_names, self._create_evidence_hash),
                generate_evidence_csv(evidence_data, export_path, export_options, self._format_column_names, self._create_evidence_hash),
            ]

            if export_options.include_metadata:
                files_created.append(generate_metadata_csv(framework_config, corpus_manifest, analysis_data, export_path, export_options, self._format_column_names))

            export_time = (datetime.now() - start_time).total_seconds()
            total_records = len(analysis_data.get('document_analyses', []))

            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    self.agent_name, "export_success",
                    {"files_created": files_created, "total_records": total_records, "export_time_seconds": export_time}
                )

            return ExportResult(True, export_path, files_created, total_records, export_time)

        except Exception as e:
            error_msg = f"CSV export failed: {str(e)}"
            self.logger.error(error_msg)
            if self.audit_logger:
                self.audit_logger.log_agent_event(self.agent_name, "export_error", {"error": error_msg})
            return ExportResult(False, export_path, [], 0, (datetime.now() - start_time).total_seconds(), error_msg)

    def export_final_synthesis_data(
        self, scores_hash: str, evidence_hash: str, statistical_results_hash: str, curated_evidence_hash: str,
        framework_config: Dict[str, Any], corpus_manifest: Dict[str, Any], synthesis_metadata: Dict[str, Any],
        export_path: str, export_options: Optional[ExportOptions] = None
    ) -> ExportResult:
        """Export comprehensive final CSV files after synthesis completion."""
        start_time = datetime.now()
        export_options = export_options or ExportOptions()

        if self.audit_logger:
            self.audit_logger.log_agent_event(
                self.agent_name, "final_synthesis_export_start",
                {"export_path": export_path, "export_type": "comprehensive_final"}
            )

        try:
            os.makedirs(export_path, exist_ok=True)
            scores_data_raw = synthesis_metadata.get("scores_data_raw")
            statistical_results_raw = synthesis_metadata.get("statistical_results_raw")
            analysis_data = scores_data_raw if scores_data_raw else self._load_artifact_data(scores_hash)
            evidence_data = self._load_artifact_data(evidence_hash) if evidence_hash != scores_hash else analysis_data

            statistical_results = statistical_results_raw or self._load_artifact_data(statistical_results_hash)

            files_created = [
                generate_scores_csv(analysis_data, export_path, export_options, self._format_column_names, self._create_evidence_hash),
                generate_evidence_csv(evidence_data, export_path, export_options, self._format_column_names, self._create_evidence_hash),
                generate_statistical_results_csv(statistical_results, export_path, export_options),
            ]

            if export_options.include_metadata:
                files_created.append(generate_final_metadata_csv(framework_config, corpus_manifest, synthesis_metadata, analysis_data, export_path, export_options, self._format_column_names))

            export_time = (datetime.now() - start_time).total_seconds()
            total_records = len(analysis_data.get('document_analyses', []))

            if self.audit_logger:
                self.audit_logger.log_agent_event(
                    self.agent_name, "final_synthesis_export_success",
                    {"files_created": files_created, "total_records": total_records, "export_time_seconds": export_time}
                )

            return ExportResult(True, export_path, files_created, total_records, export_time)

        except Exception as e:
            error_msg = f"Final synthesis CSV export failed: {str(e)}"
            self.logger.error(error_msg)
            if self.audit_logger:
                self.audit_logger.log_agent_event(self.agent_name, "final_synthesis_export_failed", {"error_message": str(e)})
            return ExportResult(False, export_path, [], 0, (datetime.now() - start_time).total_seconds(), str(e))

    def _load_artifact_data(self, artifact_hash: str) -> Dict[str, Any]:
        """Load artifact data from storage."""
        try:
            if self.artifact_storage:
                artifact_content = self.artifact_storage.get_artifact(artifact_hash)
                return json.loads(artifact_content.decode('utf-8'))

            shared_cache_path = Path("projects/simple_test/shared_cache/artifacts")
            artifact_path = shared_cache_path / artifact_hash
            if not artifact_path.exists():
                raise FileNotFoundError(f"Artifact not found: {artifact_hash}")

            with open(artifact_path, 'rb') as f:
                return json.loads(f.read().decode('utf-8'))
        except Exception as e:
            raise CSVExportError(f"Failed to load artifact {artifact_hash}: {str(e)}")

    def _format_column_names(self, headers: List[str], export_options: ExportOptions) -> List[str]:
        """Format column names based on export format preferences."""
        if export_options.export_format == "r_friendly":
            headers = [h.lower().replace(' ', '_').replace('-', '_') for h in headers]
        elif export_options.export_format == "spss_friendly":
            headers = [h.replace('_', '').replace(' ', '')[:8] for h in headers]
        if export_options.custom_column_names:
            headers = [export_options.custom_column_names.get(h, h) for h in headers]
        return headers

    def _create_evidence_hash(self, document_analysis: Dict[str, Any]) -> str:
        """Create a hash for evidence linking."""
        import hashlib
        document_id = document_analysis.get('document_id', '')
        analysis_scores = document_analysis.get('analysis_scores', {})
        hash_content = f"{document_id}:{json.dumps(analysis_scores, sort_keys=True)}"
        return hashlib.sha256(hash_content.encode('utf-8')).hexdigest()[:16]

    def get_export_stats(self) -> Dict[str, Any]:
        """Get export agent statistics."""
        return {
            "agent_name": self.agent_name,
            "architecture": "deterministic_csv_export",
            "gasket_type": "pipeline_to_human",
            "framework_agnostic": True,
            "cost_per_export": 0.0,
            "supported_formats": ["standard", "r_friendly", "spss_friendly"]
        }