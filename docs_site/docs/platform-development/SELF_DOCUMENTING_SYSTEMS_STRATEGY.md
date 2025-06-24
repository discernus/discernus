# Self-Documenting Systems Strategy

This document outlines the strategy for creating a "self-documenting" system in the Discernus project. The goal is not to eliminate documentation, but to create an ecosystem where accurate, up-to-date documentation is a natural byproduct of the development process, rather than a separate and burdensome task.

---

This strategy is built on four core pillars:

### 1. Code as Documentation (The Source of Truth)

**Philosophy**: The code itself, when well-written and annotated, is the most accurate and reliable source of information.

-   **Standard**: All production Python code must use **Google-style docstrings** to explain the purpose, arguments, return values, and exceptions of functions and classes. This standard is defined in our [`CODE_ORGANIZATION_STANDARDS.md`](../CODE_ORGANIZATION_STANDARDS.md).
-   **Enforcement**: We use the `pydocstyle` linter to automatically check for compliance with our docstring standards. This is a required check before submitting a Pull Request.

---

### 2. Schemas as Contracts (Configuration as Documentation)

**Philosophy**: When configuration drives application behavior, the schema for that configuration becomes a form of "active" documentation that is both descriptive and functional.

-   **Standard**: Critical configuration files, such as experiment definitions, must be defined by a formal **JSON Schema**.
-   **Example**: The [`experiment_schema.json`](../specifications/experiment_schema.json) file serves as the canonical reference for all valid experiment options.
-   **Enforcement**: Our core scripts, like the experiment orchestrator, should validate all configuration files against this schema before execution. This ensures that the documentation (the schema) and the application are always in sync.

---

### 3. Automation (Let the Tools Do the Work)

**Philosophy**: Manual documentation tasks that can be automated, should be. This reduces tedious work and ensures that generated documentation is always current.

-   **Documentation Website**: We use **MkDocs** to automatically build a modern, searchable documentation site from our collection of Markdown files.
-   **Automated Indexing**: We have created scripts like `update_research_workspace_index.py` to automatically scan directories and generate indexes. This eliminates the need to manually update lists of experiments or frameworks.
-   **Self-Documenting CLIs**: All command-line interfaces are required to have comprehensive `--help` output, which is generated automatically from the argument parser's configuration.

---

### 4. Process as Guardrails (Making it Habit)

**Philosophy**: Good tooling is most effective when it is integrated directly into the established development workflow, guiding developers toward best practices.

-   **Contribution Guidelines**: The [`CONTRIBUTING.md`](../CONTRIBUTING.md) file provides a clear "Golden Path" for all contributors.
-   **Pull Request Template**: The [`.github/pull_request_template.md`](../../../.github/pull_request_template.md) includes a mandatory checklist. This forces every developer to consciously consider documentation tasks—such as updating the `CHANGELOG.md` and running the docstring linter—before their code can be merged.

By adhering to these four pillars, we create a system where documentation is not an afterthought, but a core, integrated, and sustainable part of our engineering culture.

## **✅ Benefits of Self-Documenting Systems**

**Reduced Maintenance Burden**: Code changes automatically propagate to documentation, reducing the overhead of keeping docs synchronized.

**Real-Time Documentation**: Users always have access to current, accurate information about system capabilities and interfaces.

**Example**: The Framework Specification v3.1 and YAML-based experiment definitions serve as the canonical reference for all valid framework and experiment options.

**Enforcement**: Our core scripts, like the experiment orchestrator, should validate all configurations against these specifications to ensure consistency. 