# Development Environment Setup - Quick Reference

> **Note**: Complete development environment guidance is in `.cursorrules`. This document provides IDE-specific setup and quick reference.

## Quick Setup Commands

```bash
# Essential setup for every session
source venv/bin/activate
source scripts/setup_dev_env.sh

# Verify imports work
python3 -c "from src.narrative_gravity.engine import NarrativeGravityWellsElliptical; print('✅ Imports working!')"
```

## IDE Configuration

### VS Code Setup
Add to `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.envFile": "${workspaceFolder}/.env",
    "python.analysis.extraPaths": [
        "${workspaceFolder}/src"
    ]
}
```

### PyCharm Setup
1. **File → Settings → Project → Python Interpreter**
2. Select the virtual environment: `./venv/bin/python`
3. **File → Settings → Project → Project Structure**
4. Mark `src/` directory as "Sources Root"

## Shell Integration (Optional)

Add to `~/.zshrc` or `~/.bashrc` for automatic setup:
```bash
# Auto-setup when entering project directory
cd() {
    builtin cd "$@"
    if [[ "$PWD" == *"narrative_gravity_analysis"* ]] && [[ -f "scripts/setup_dev_env.sh" ]]; then
        source scripts/setup_dev_env.sh > /dev/null 2>&1
    fi
}
```

## Common Issues

**Import failures?** → Run `source scripts/setup_dev_env.sh`  
**Command not found: python?** → Use `python3`  
**Wrong dates in files?** → Use `date` command or `./scripts/get_current_date.sh`

---

**For complete development environment guidance, see `.cursorrules`** 