# Bloat Prevention System

**Module:** `scripts.applications.bloat_prevention_system`
**File:** `/app/scripts/applications/bloat_prevention_system.py`
**Package:** `applications`

Bloat Prevention System

Comprehensive system to prevent storage, logging, and database bloat
from testing and development activities.

## Dependencies

- `argparse`
- `dataclasses`
- `datetime`
- `json`
- `logging`
- `os`
- `pathlib`
- `re`
- `shutil`
- `sqlite3`
- `sys`
- `test_result_preservation_system`
- `time`
- `typing`

## Table of Contents

### Classes
- [CleanupStats](#cleanupstats)
- [BloatPreventionSystem](#bloatpreventionsystem)

### Functions
- [main](#main)

## Classes

### CleanupStats

Statistics from cleanup operations

---

### BloatPreventionSystem

Comprehensive bloat prevention and cleanup system

#### Methods

##### `__init__`
```python
__init__(self, project_root: Path)
```

##### `cleanup_test_experiments`
```python
cleanup_test_experiments(self, dry_run: bool, days_old: int) -> [CleanupStats](scripts/applications/bloat_prevention_system.md#cleanupstats)
```

Clean up test experiment directories

##### `cleanup_duplicate_experiments`
```python
cleanup_duplicate_experiments(self, dry_run: bool) -> [CleanupStats](scripts/applications/bloat_prevention_system.md#cleanupstats)
```

Remove duplicate experiment directories (keep latest)

##### `rotate_logs`
```python
rotate_logs(self, dry_run: bool, max_size_mb: float, keep_lines: int) -> [CleanupStats](scripts/applications/bloat_prevention_system.md#cleanupstats)
```

Rotate large log files

##### `cleanup_old_log_archives`
```python
cleanup_old_log_archives(self, dry_run: bool, days_old: int) -> [CleanupStats](scripts/applications/bloat_prevention_system.md#cleanupstats)
```

Remove old log archives

##### `cleanup_test_database_records`
```python
cleanup_test_database_records(self, dry_run: bool) -> [CleanupStats](scripts/applications/bloat_prevention_system.md#cleanupstats)
```

Clean up test records from database

##### `cleanup_orphaned_assets`
```python
cleanup_orphaned_assets(self, dry_run: bool) -> [CleanupStats](scripts/applications/bloat_prevention_system.md#cleanupstats)
```

Clean up orphaned assets in content-addressable storage

##### `cleanup_temp_files`
```python
cleanup_temp_files(self, dry_run: bool) -> [CleanupStats](scripts/applications/bloat_prevention_system.md#cleanupstats)
```

Clean up temporary files and caches

##### `_get_directory_size_mb`
```python
_get_directory_size_mb(self, directory: Path) -> float
```

Get directory size in MB

##### `_extract_experiment_base_name`
```python
_extract_experiment_base_name(self, name: str) -> str
```

Extract base experiment name without timestamp

##### `_is_empty_recursive`
```python
_is_empty_recursive(self, directory: Path) -> bool
```

Check if directory is empty recursively

##### `run_full_cleanup`
```python
run_full_cleanup(self, dry_run: bool, aggressive: bool) -> [CleanupStats](scripts/applications/bloat_prevention_system.md#cleanupstats)
```

Run comprehensive cleanup

##### `setup_automated_cleanup`
```python
setup_automated_cleanup(self)
```

Set up automated cleanup (cron job, etc.)

---

## Functions

### `main`
```python
main()
```

CLI entry point

---

*Generated on 2025-06-21 20:19:04*