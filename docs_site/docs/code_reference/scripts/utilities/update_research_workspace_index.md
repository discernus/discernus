# Update Research Workspace Index

**Module:** `scripts.utilities.update_research_workspace_index`
**File:** `/app/scripts/utilities/update_research_workspace_index.py`
**Package:** `utilities`

## Dependencies

- `argparse`
- `pathlib`
- `re`

## Table of Contents

### Functions
- [update_index](#update-index)
- [main](#main)

## Functions

### `update_index`
```python
update_index(readme_path: Path, frameworks_path: Path, experiments_path: Path)
```

Scans the frameworks and experiments directories and updates the index tables
in the specified README.md file.

Args:
    readme_path (Path): The path to the README.md file to update.
    frameworks_path (Path): The path to the frameworks directory.
    experiments_path (Path): The path to the experiments directory.

---

### `main`
```python
main()
```

---

*Generated on 2025-06-21 20:19:04*