# Export Academic Data

**Module:** `scripts.cli.export_academic_data`
**File:** `/app/scripts/cli/export_academic_data.py`
**Package:** `cli`

Academic Data Export CLI - Simple wrapper for existing functionality

Uses the existing AcademicDataExporter to export PostgreSQL data to academic formats.
This is a thin CLI layer over the existing academic module functionality.

Usage:
    python export_academic_data.py --experiment-ids exp1,exp2 --output-dir exports/study2025 --formats csv,stata,r,json
    python export_academic_data.py --study-name my_study --all-experiments --include-metadata

## Dependencies

- `argparse`
- `pathlib`
- `src.academic`
- `sys`

## Table of Contents

### Functions
- [export_data_cli](#export-data-cli)

## Functions

### `export_data_cli`
```python
export_data_cli()
```

CLI interface for academic data export.

---

*Generated on 2025-06-23 10:38:43*