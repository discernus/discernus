# Development Environment Setup Guide

## The Path Problem
The AI assistant often struggles with Python import paths because the project uses a `src/` directory structure that isn't automatically in Python's module search path.

## Quick Fix: Auto-Setup Every Session

**Add this to the top of your work sessions:**

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Setup development paths
source scripts/setup_dev_env.sh
```

## What This Fixes

### ✅ **Before** (Broken):
```python
# This would fail
from narrative_gravity.engine import NarrativeGravityWellsElliptical
```

### ✅ **After** (Working):
```python
# Both of these work now
from src.narrative_gravity.engine import NarrativeGravityWellsElliptical
from narrative_gravity.engine import NarrativeGravityWellsElliptical  # Also works!
```

## Environment Variables Set

The setup script configures:
- `PROJECT_ROOT`: `/Users/jeffwhatcott/narrative_gravity_analysis`
- `PYTHONPATH`: Includes project root and `src/` directory
- `NARRATIVE_GRAVITY_*`: Helper variables for scripts
- Loads all `.env` variables automatically

## Verification

Test that everything works:
```bash
python3 -c "from src.narrative_gravity.engine import NarrativeGravityWellsElliptical; print('✅ Imports working!')"
```

## For Long-Term Use

Add to your `~/.zshrc` or `~/.bashrc`:
```bash
# Auto-setup Narrative Gravity environment when entering the project
cd() {
    builtin cd "$@"
    if [[ "$PWD" == *"narrative_gravity_analysis"* ]] && [[ -f "scripts/setup_dev_env.sh" ]]; then
        source scripts/setup_dev_env.sh > /dev/null 2>&1
    fi
}
```

## Alternative: IDE Setup

If using VS Code, add to `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.envFile": "${workspaceFolder}/.env",
    "python.analysis.extraPaths": [
        "${workspaceFolder}/src"
    ]
}
```

This ensures both AI assistant commands and your IDE can properly resolve imports. 