# Experiment Specification (v10.0)

**Version**: 10.0  
**Status**: Active Standard  
**Replaces**: v8.0

---

## Introduction: The Experiment as a Research Plan

An **Experiment** in Discernus is a formal research plan. It is a self-contained document that brings together a `Framework` and a `Corpus` to investigate a specific set of research questions. Like the `v10.0` Framework, it is a hybrid document, designed for both human comprehension and machine execution.

The `experiment.md` file is the single source of truth that tells the Discernus system what to analyze, how to analyze it, and why.

---

## Part 1: The Scholarly Document (The Human-Readable Narrative)

This part is written in standard Markdown and outlines the intellectual goals of the experiment.

### Section 1: Abstract

**(Required)**
A brief, high-level summary of the experiment's purpose, scope, and expected contribution.

### Section 2: Research Questions

**(Required)**
A list of the specific, answerable research questions that the experiment is designed to investigate.

### Section 3: Expected Outcomes

**(Optional but Recommended)**
A description of the anticipated results or the types of analysis that will be conducted (e.g., "A comparative statistical analysis of cohesion scores between the two speakers.").

---

## Part 2: The Machine-Readable Appendix

This is a single YAML block at the end of the document containing the precise configuration for the orchestrator.

### Section 4: Configuration Appendix

**(Required)**

```yaml
# --- Start of Machine-Readable Appendix ---

# 4.1: Metadata (Required)
metadata:
  experiment_name: "your_experiment_name_in_snake_case"
  author: "Your Name or Organization"
  spec_version: "10.0"

# 4.2: Components (Required)
components:
  # The filename of the v10.0 Framework file.
  # Must be in the same directory as this experiment.md.
  framework: "cff_v10.md"

  # The filename of the v8.0 compliant Corpus manifest file.
  # Must be in the same directory as this experiment.md.
  corpus: "corpus.md"

# --- End of Machine-Readable Appendix ---
```

---

## Validation Rules

-   The file must be named `experiment.md`.
-   It must contain a valid YAML appendix.
-   All required fields (`experiment_name`, `spec_version`, `framework`, `corpus`) must be present.
-   The `spec_version` in the experiment must be compatible with the `spec_version` in the referenced framework.
-   The files specified in `framework` and `corpus` must exist in the same directory as the `experiment.md` file.
