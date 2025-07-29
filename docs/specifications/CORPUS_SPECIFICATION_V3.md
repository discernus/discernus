# Corpus Specification (v3.0)

**Version**: 3.0
**Status**: Active
**Principle**: The integrity of a computational analysis depends entirely on the integrity of the input corpus. This document defines the standard for creating a research-grade, self-documenting corpus.

---

## Part I: The "Narrative + Appendix" Architecture

A Discernus corpus is not just a collection of text files; it is a complete, self-contained research artifact. To achieve this, a corpus directory MUST contain a `corpus.md` file that follows our "Narrative + Appendix" architecture.

1.  **The Narrative (Human-Focused)**: The main body of the `corpus.md` file. This section uses standard Markdown for the researcher to document the "story" of the corpus:
    *   **Collection Methodology**: How and where were the source texts obtained?
    *   **Ethical Considerations**: What steps were taken to ensure ethical use?
    *   **Corpus Description**: A clear description of the corpus contents, scope, and characteristics.

2.  **The Appendix (Machine-Focused)**: A single, collapsible appendix at the end of the file that contains a single, unambiguous JSON object. This is the **single source of truth** for all machine-readable metadata about the corpus.

---

## Part II: The JSON Appendix Schema

The appendix MUST begin with `<details><summary>Machine-Readable Configuration</summary>` and end with `</details>`. It MUST contain a single JSON code block with the following schema:

```json
{
  "file_manifest": [
    {
      "name": "document_01.txt",
      "expert_categorization": "statement_of_principle",
      "political_party": "Republican"
    },
    {
      "name": "document_02.txt",
      "expert_categorization": "legislative_action",
      "political_party": "Democrat"
    }
  ]
}
```

**Component Explanations**:

*   **`file_manifest`**: (Optional) An array of objects, where each object contains metadata for a specific file in the corpus directory. The `name` field must match the filename exactly. This is used for experiments that require pre-categorized data.

---

## Part III: Best Practices

### 1. Corpus Documentation

A well-documented corpus should include:

*   **Clear Collection Methodology**: Document how and where source texts were obtained, including any selection criteria or sampling methods.
*   **Ethical Considerations**: Describe steps taken to ensure ethical use, including any necessary permissions or anonymization.
*   **Corpus Characteristics**: Provide a clear description of the corpus contents, including scope, time period, and key characteristics.
*   **Quality Assurance**: Document any quality control measures applied to the corpus.

### 2. File Organization

*   **Consistent Naming**: Use clear, descriptive filenames that reflect the content.
*   **Standard Formats**: Use plain text (.txt) or markdown (.md) files for maximum compatibility.
*   **Metadata Documentation**: Include relevant metadata in the file manifest for experiments requiring pre-categorized data.

### 3. Provenance

*   **Source Attribution**: Clearly document the original sources of all texts in the corpus.
*   **Processing History**: Document any processing or transformation applied to the original texts.
*   **Version Control**: Maintain clear version information for the corpus.

---

## Part IV: Integration with Experiment Specification

The corpus specification integrates with the experiment specification through:

*   **File Manifest Utilization**: The experiment specification can reference file manifest metadata for pre-categorized analysis.
*   **Corpus Documentation**: The narrative section provides context for experiment interpretation.
*   **Quality Assurance**: Corpus documentation supports experiment quality validation.

---

## Part V: Conclusion

The Corpus Specification v3.0 provides a simplified, focused approach to corpus management that emphasizes documentation, provenance, and integration with the broader Discernus research platform. By removing complexity while maintaining essential functionality, it enables researchers to focus on their core analytical work while ensuring proper corpus documentation and metadata management.

**Note**: Sanitization processes have been removed from this specification. If bias analysis requires sanitization, this should be addressed through the experiment specification and validated through research. See Issue #158 for details on the research task to evaluate sanitization necessity and sufficiency. 