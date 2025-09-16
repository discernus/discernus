# Repository Guidelines

## Project Structure & Module Organization
- `discernus/` — Python package (core, agents, CLI). Examples: `discernus/agents/*/agent.py`, `discernus/core/*`.
- `discernus/tests/` — Pytest suite and quick checks. Run smoke test via `python3 discernus/tests/quick_test.py`.
- `docs/` — User docs and CLI reference (`docs/user/CLI_REFERENCE.md`).
- `frameworks/` — Methodology specs and validation assets.
- `projects/` — Example experiments; run with the CLI.
- `scripts/` — Developer utilities (env checks, validation tools).

## Build, Test, and Development Commands
- `make install` — Install dependencies from `requirements.txt`.
- `make check` — Validate local environment (Python, tools, paths).
- `make test` — Fast smoke test to verify setup.
- `pytest` — Run full test suite (configured in `pyproject.toml`).
- `make run EXPERIMENT=projects/<name>` — Execute an experiment via CLI.
- `make clean` / `make clean-all` — Remove caches and misc artifacts.
Examples:
```
pytest -q
discernus run projects/micro_test_experiment --analysis-only
```

## Coding Style & Naming Conventions
- Formatting: Black (line length 120) and isort (profile=black). Prefer 4‑space indents.
- Linting: Pylint config in `.pylintrc`; keep warnings low, fix true issues first.
- Naming: `snake_case` for modules/functions, `PascalCase` for classes, `CONSTANT_CASE` for constants.
- Type hints encouraged for new/changed code; validate data models with Pydantic where applicable.

## Testing Guidelines
- Framework: Pytest (`[tool.pytest.ini_options]` in `pyproject.toml`).
- Location: `discernus/tests/`. Files start with `test_*.py`; functions `test_*`.
- Expectations: Add unit tests for new logic and regressions; keep tests fast and deterministic.
- Run: `pytest` (full) or `make test` (smoke). Prefer local seeds/mocks over network calls.

## Commit & Pull Request Guidelines
- Commits: Imperative, concise subject; scope when helpful. Examples in history: “Optimize derived metrics…”, “Complete run: {experiment}”, “Analysis only: {experiment}”.
- PRs: Clear description, linked issues, rationale, test coverage notes, and CLI/log screenshots for user-facing changes. Include `projects/<example>` steps if behavior changes.

## Security & Configuration Tips
- Do not commit secrets or tokens. Use environment variables and `.env` locally.
- For noisy LLM logs, see `make litellm-setup`. Prefer `make run-safe` to use the safe Python wrapper.

## Agent-Specific Notes
- Agent definitions live under `discernus/agents/*` with paired prompts (`prompt.yaml`). Keep prompts versioned and deterministic; document inputs/outputs alongside the agent.
