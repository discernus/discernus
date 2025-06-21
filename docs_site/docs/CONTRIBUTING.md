# Contributing to Discernus

Thank you for contributing to the Discernus project! This document provides the essential guidelines for contributing to the project, ensuring a consistent, high-quality development process. For a complete map of all project documentation, please see the **[`DOCUMENTATION_INDEX.md`](DOCUMENTATION_INDEX.md)**.

---

## 🚀 The Contribution Workflow

We follow a systematic, documentation-driven workflow. Following these steps is mandatory for all contributions.

1.  **Consult the Documentation Index**: Before starting any work, familiarize yourself with the project by reviewing the [`DOCUMENTATION_INDEX.md`](DOCUMENTATION_INDEX.md). This will help you understand the existing architecture and standards.

2.  **Check for Existing Systems**: Never build without checking first. Use the `check_existing_systems.py` script to ensure you are not duplicating existing functionality.
    ```bash
    python scripts/applications/check_existing_systems.py "a description of the functionality you need"
    ```

3.  **Develop in an Experimental Context**: All new features, scripts, or components **must** begin their life in the `experimental/` or `sandbox/` directories. This prevents destabilizing the production systems.

4.  **Follow Code Organization Standards**: Adhere strictly to the principles outlined in [`CODE_ORGANIZATION_STANDARDS.md`](CODE_ORGANIZATION_STANDARDS.md).

5.  **Submit a Pull Request (PR)**: Once your work is complete and tested within the experimental context, submit a Pull Request to the `dev` branch. Your PR description should clearly explain the changes and reference any relevant issues.

6.  **Pass Code Review**: Your PR will be reviewed for compliance with the project's standards (see Code Review Guidelines below). Be prepared to make changes based on feedback.

7.  **Promotion to Production**: Once approved, your feature will be merged and may be promoted from `experimental/` to `src/` or `scripts/applications/` by the repository maintainers.

---

## 🤝 Code Review Guidelines

Code reviews are critical for maintaining the quality and integrity of the codebase. Reviewers will focus on the following key areas:

1.  **Architectural Compliance**: Does the contribution adhere to the project's architecture and organization standards?
2.  **Documentation**: Are the changes documented in the `CHANGELOG.md`? Is any new functionality clearly explained with comments or accompanying documentation?
3.  **Database Usage**: Is PostgreSQL being used correctly for all persistent application data?
4.  **Testing**: Do all existing tests pass? Are there new tests that cover the new functionality?
5.  **Error Handling**: Does the code handle potential errors gracefully?

### Docstring Linting
To ensure our code is self-documenting, all production code must pass `pydocstyle` checks. Before submitting a PR, run the linter on your changed files.

```bash
# Run the docstring linter on the entire src directory
python3 -m pydocstyle src/
```

This check enforces the Google-style docstring format defined in [`CODE_ORGANIZATION_STANDARDS.md`](CODE_ORGANIZATION_STANDARDS.md).

---

## 🔧 Development Setup

For detailed instructions on setting up your local or Docker-based development environment, please see **[`platform-development/DEV_ENVIRONMENT.md`](platform-development/DEV_ENVIRONMENT.md)**.

---

## 🧪 Testing Standards

### Test Organization
- **Unit tests**: `tests/unit/` - Should use in-memory SQLite.
- **Integration tests**: `tests/integration/` - Can use the actual PostgreSQL database.
- **End-to-end tests**: `tests/e2e/` - Test the full application flow.

### Running the Test Suite
While you can run tests with `pytest` directly, the preferred method is to use the provided test runner script, which ensures all categories of tests are executed with the correct configuration.

```bash
# Run the complete test suite (unit, integration, and e2e)
python tests/run_tests.py
```

This script handles the necessary setup and provides a comprehensive overview of test results. For more granular testing, you can still use `pytest`:

```bash
# Run tests in a specific category
pytest tests/unit/

# Run tests with a coverage report
pytest --cov=src
```

---

## Pull Request (PR) Process

To ensure a smooth and efficient review process, all Pull Requests must adhere to the following structure:

1.  **PR Title**: The title should follow the [Conventional Commits](https://www.conventionalcommits.org/) specification (e.g., `feat: Add new visualization engine`, `fix: Correct orchestrator fallback logic`).

2.  **PR Description**: The description must provide:
    - A clear summary of the changes.
    - The "why" behind the change (e.g., what problem it solves).
    - A link to any relevant issues (e.g., `Closes #123`).

3.  **Changelog Entry**: For any user-facing changes, you must add an entry to `CHANGELOG.md` under the `[Unreleased]` section.

4.  **Self-Review**: Before submitting, perform a self-review to ensure your PR meets the guidelines in this document and in `CODE_ORGANIZATION_STANDARDS.md`.

---

## 📝 Changelog Requirements

*For all other standards, including project organization, database architecture, file movement protocols, and release processes, please refer to the relevant documents linked in the [`DOCUMENTATION_INDEX.md`](DOCUMENTATION_INDEX.md).* 