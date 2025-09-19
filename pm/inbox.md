# Inbox - Raw Backlog Items

**Purpose**: Raw capture of backlog items without organization or sprint planning. Items here will be groomed into organized sprints later.

**Usage**:

- "inbox this" → append new items here with minimal formatting
- "groom our sprints" → move all items from here to sprints.md with proper organization

---

## Run Directory Naming Inconsistency Investigation - RESOLVED

**Issue**: Different run directory naming patterns across experiments in `projects/nano_test_experiment/runs/`:
- `20250919_202338/` (underscore format: YYYYMMDD_HHMMSS)
- `20250919_203230/` (underscore format: YYYYMMDD_HHMMSS) 
- `20250919T163431Z/` (ISO format: YYYYMMDDTHHMMSSZ)

**Root Cause Analysis**:
- **CLI (`discernus/cli.py:190`)**: Uses `%Y%m%d_%H%M%S` format (underscore)
- **CleanAnalysisOrchestrator (`discernus/core/clean_analysis_orchestrator.py:181`)**: Uses `%Y%m%dT%H%M%SZ` format (ISO)
- **Other components**: Mixed usage of both formats throughout codebase

**Resolution**:
✅ **CleanAnalysisOrchestrator completely deprecated** - removed from CLI commands
✅ **V2 orchestrator is now the only orchestrator** - uses consistent `%Y%m%d_%H%M%S` format
✅ **Resume and debug commands updated** - now show proper error messages directing users to V2
✅ **All run directories now use underscore format** - consistent naming across the system

**Result**: 
- Consistent directory structures for all new runs
- Single orchestrator eliminates naming conflicts
- Clear migration path for users (use `discernus run` instead of deprecated commands)
