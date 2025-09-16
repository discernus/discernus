#!/usr/bin/env python3
"""
CSV Export Agent Types
======================

Shared types for the CSV Export Agent to avoid circular imports.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ExportOptions:
    """Configuration options for CSV export."""
    include_calculated_metrics: bool = True
    evidence_detail_level: str = "hashes_only"  # "hashes_only", "quotes", "full"
    export_format: str = "standard"  # "standard", "r_friendly", "spss_friendly"
    custom_column_names: Optional[dict] = None
    include_metadata: bool = True


@dataclass
class ExportResult:
    """Result of CSV export operation with metadata."""
    success: bool
    export_path: str
    files_created: list
    total_records: int
    export_time_seconds: float
    error_message: Optional[str] = None


class CSVExportError(Exception):
    """CSV Export specific exceptions."""
    pass
