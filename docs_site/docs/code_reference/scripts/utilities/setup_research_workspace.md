# Setup Research Workspace

**Module:** `scripts.utilities.setup_research_workspace`
**File:** `/app/scripts/utilities/setup_research_workspace.py`
**Package:** `utilities`

## Dependencies

- `argparse`
- `pathlib`

## Table of Contents

### Functions
- [setup_research_workspace](#setup-research-workspace)

## Functions

### `setup_research_workspace`
```python
setup_research_workspace(base_path: str)
```

Creates the standard directory structure for a new research workspace.
This ensures that a new user has the necessary folders to begin
creating frameworks, experiments, and other research assets without
having to create them manually.

Args:
    base_path (str): The root path where the 'research_workspaces'
                     directory should be created or verified.

---

*Generated on 2025-06-21 20:19:04*