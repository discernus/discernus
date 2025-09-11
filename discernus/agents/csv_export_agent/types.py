#!/usr/bin/env python3
"""
CSV Export Agent Types
======================

Shared types for the CSV Export Agent to avoid circular imports.
"""

Copyright (C) 2025  Discernus Team

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.


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
