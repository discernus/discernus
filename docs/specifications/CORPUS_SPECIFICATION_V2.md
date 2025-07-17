# Corpus Specification (v2.0)

**Version**: 2.0
**Status**: Active
**Principle**: The integrity of a computational analysis depends entirely on the integrity of the input corpus. This document defines the standard for creating a research-grade, self-documenting corpus.

---

## Part I: The "Narrative + Appendix" Architecture

A Discernus corpus is not just a collection of text files; it is a complete, self-contained research artifact. To achieve this, a corpus directory MUST contain a `corpus.md` file that follows our "Narrative + Appendix" architecture.

1.  **The Narrative (Human-Focused)**: The main body of the `corpus.md` file. This section uses standard Markdown for the researcher to document the "story" of the corpus:
    *   **Collection Methodology**: How and where were the source texts obtained?
    *   **Ethical Considerations**: What steps were taken to ensure ethical use?
    *   **Sanitization Process**: If the corpus was sanitized, what prompts and methods were used? This section should include the exact prompts for full reproducibility.
    *   **Corpus State**: A clear statement of whether this corpus is `original`, `sanitized`, or `translated`.

2.  **The Appendix (Machine-Focused)**: A single, collapsible appendix at the end of the file that contains a single, unambiguous JSON object. This is the **single source of truth** for all machine-readable metadata about the corpus.

---

## Part II: The JSON Appendix Schema

The appendix MUST begin with `<details><summary>Machine-Readable Configuration</summary>` and end with `</details>`. It MUST contain a single JSON code block with the following schema:

```json
{
  "file_manifest": [
    {
      "name": "9c759f7025a4.txt",
      "expert_categorization": "statement_of_principle",
      "political_party": "Republican"
    },
    {
      "name": "cccec508db40.txt",
      "expert_categorization": "legislative_action",
      "political_party": "Democrat"
    }
  ],
  "speaker_mapping": [
    {
      "hash": "9c759f7025a4",
      "speaker": "Mitt Romney",
      "title": "2020 Impeachment Vote Speech",
      "source": "mitt_romney_2020_impeachment.txt"
    },
    {
      "hash": "cccec508db40",
      "speaker": "Cory Booker",
      "title": "First Step Act Speech",
      "source": "cory_booker_2018_first_step_act.txt"
    }
  ]
}
```

**Component Explanations**:

*   **`file_manifest`**: (Optional) An array of objects, where each object contains metadata for a specific file in the corpus directory. The `name` field must match the filename exactly. This is used for experiments that require pre-categorized data.
*   **`speaker_mapping`**: (Required for `sanitized` or `translated` corpora) An array of objects that serves as the secure lookup table, mapping anonymized hashes back to their original source information. Storing it here ensures that the mapping is intrinsically tied to the specific corpus it describes, enhancing provenance.

---

## Part III: Corpus States and Best Practices

### 1. The "Corpus State" Methodology

For rigorous bias analysis, we recommend preparing your corpus in multiple states, each in its own directory with its own `corpus.md` file.

*   **`/corpus_original/`**: Contains raw source texts and a `corpus.md` with an empty `speaker_mapping`.
*   **`/corpus_sanitized/`**: Contains sanitized texts with hashed filenames and a `corpus.md` with a complete `speaker_mapping`.
*   **`/corpus_translated/`**: Contains translated texts with hashed filenames and a corresponding `corpus.md`.

An experiment is run against a specific corpus state by pointing to its directory in the `experiment.md`.

### 2. Sanitization and Hashing

*   **Goal**: To remove all **Identity Vectors** (speaker names, locations, etc.) while preserving the core **Rhetorical Architecture**.
*   **Process**: The exact prompts used for sanitization MUST be documented in the narrative section of the `corpus.md` for that corpus state.
*   **Tooling**: A reference script for generating hashed filenames is available in `scripts/hash_generator.py`.

### 3. Security

By embedding the `speaker_mapping` within the `corpus.md` appendix, we ensure it is never processed as part of the corpus text itself. The orchestrator is responsible for parsing this appendix and providing the mapping data to the final synthesis step, but it is never sent to the `AnalysisAgent`'s LLM call. This prevents accidental de-anonymization during analysis. 