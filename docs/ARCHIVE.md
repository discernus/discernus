# Archive Strategy for OSS Alpha

To keep the open source repository pristine while preserving history, we use an "attic" branch that contains all deprecated/legacy code. Main/dev remain clean.

## Attic Branch
- Branch: `attic`
- Tag: `attic-2025-09-10`
- Archived content (moved under `attic/` on `attic` branch):
  - `core_deprecated/` (from `discernus/core/deprecated/`)
  - `agents_deprecated/` (from `discernus/agents/deprecated/`)
  - `fact_checker_agent/` (from `discernus/agents/fact_checker_agent/`)
  - `revision_agent/` (from `discernus/agents/revision_agent/`)
  - `cli_clean.py`, `cli_console.py`

## Retrieval
```bash
# Inspect attic branch
git checkout attic
ls attic/

# Retrieve a specific file from attic without switching branches
# Example: restore legacy thin_orchestrator.py into a scratch path
git show attic:attic/core_deprecated/thin_orchestrator.py > /tmp/thin_orchestrator.py
```

## Rationale
- Preserve full history and code for research purposes
- Ensure OSS alpha surface area only includes supported and maintained components
- Allow selective reintroduction (via cherry-pick) without polluting main

## Guardrails (Recommended Post-Alpha)
- Pre-commit/CI denylist for reintroducing `discernus/core/deprecated/` or `discernus/agents/deprecated/` paths
- Periodic attic tag updates when new archives occur
