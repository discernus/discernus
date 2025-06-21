# Framework Sync

**Module:** `scripts.applications.framework_sync`
**File:** `/Users/jeffwhatcott/Library/Mobile Documents/com~apple~CloudDocs/Coding Projects/discernus/scripts/applications/framework_sync.py`
**Package:** `applications`

Framework Synchronization Tool
Manages the relationship between filesystem frameworks (development) and database frameworks (source of truth).

Database = Source of Truth (used by application)
Filesystem = Development Workspace (for editing and testing)

Usage:
    python scripts/framework_sync.py status                    # Show sync status
    python scripts/framework_sync.py export [framework]        # Export DB -> filesystem
    python scripts/framework_sync.py import [framework]        # Import filesystem -> DB
    python scripts/framework_sync.py validate [framework]      # Validate framework files
    python scripts/framework_sync.py migrate-all              # Migrate all to v2.0

## Dependencies

- `argparse`
- `datetime`
- `hashlib`
- `json`
- `migrate_frameworks_to_v2`
- `os`
- `pathlib`
- `sqlalchemy`
- `sqlalchemy.orm`
- `src.models.component_models`
- `src.utils.database`
- `sys`
- `typing`

## Table of Contents

### Classes
- [FrameworkSyncManager](#frameworksyncmanager)

### Functions
- [main](#main)

## Classes

### FrameworkSyncManager

Manages synchronization between filesystem and database frameworks.

#### Methods

##### `__init__`
```python
__init__(self)
```

##### `get_filesystem_frameworks`
```python
get_filesystem_frameworks(self) -> Dict[Any]
```

Get all frameworks from filesystem with metadata.

##### `get_database_frameworks`
```python
get_database_frameworks(self) -> Dict[Any]
```

Get all frameworks from database.

##### `_calculate_framework_hash`
```python
_calculate_framework_hash(self, framework_dir: Path) -> str
```

Calculate hash of all framework files for change detection.

##### `show_status`
```python
show_status(self)
```

Show synchronization status between filesystem and database.

##### `_analyze_sync_status`
```python
_analyze_sync_status(self, fs_frameworks: Dict, db_frameworks: Dict)
```

Analyze and report sync status between filesystem and database.

##### `export_framework`
```python
export_framework(self, framework_name: str, version: str)
```

Export framework from database to filesystem.

##### `import_framework`
```python
import_framework(self, framework_name: str, create_new_version: bool)
```

Import framework from filesystem to database.

##### `_generate_next_version`
```python
_generate_next_version(self, session, framework_name: str) -> str
```

Generate next version number for framework.

##### `_generate_readme`
```python
_generate_readme(self, framework: [FrameworkVersion](src/models/component_models.md#frameworkversion)) -> str
```

Generate README content for framework.

##### `_format_wells_list`
```python
_format_wells_list(self, dipoles_data: Dict) -> str
```

Format wells list for README.

##### `validate_framework`
```python
validate_framework(self, framework_name: str) -> bool
```

Validate framework files in filesystem.

##### `migrate_all_to_v2`
```python
migrate_all_to_v2(self)
```

Migrate all frameworks to v2.0 specification.

---

## Functions

### `main`
```python
main()
```

---

*Generated on 2025-06-21 12:44:48*