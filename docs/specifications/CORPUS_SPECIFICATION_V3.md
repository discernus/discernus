# Corpus Specification (v3.2)

**Version**: 3.2
**Status**: Active
**Principle**: The integrity of a computational analysis depends entirely on the integrity of the input corpus. This document defines the standard for creating a research-grade, self-documenting corpus.

---

## Part I: The "Narrative + Appendix" Architecture

A Discernus corpus is not just a collection of text files; it is a complete, self-contained research artifact. To achieve this, a corpus directory MUST contain a `corpus.md` file that follows our "Narrative + Appendix" architecture.

1.  **The Narrative (Human-Focused)**: The main body of the `corpus.md` file. This section uses standard Markdown for the researcher to document the "story" of the corpus:
    *   **Collection Methodology**: How and where were the source texts obtained?
    *   **Ethical Considerations**: What steps were taken to ensure ethical use?
    *   **Corpus Description**: A clear description of the corpus contents, scope, and characteristics.

2.  **The Appendix (Machine-Focused)**: A single appendix at the end of the file that contains a single, unambiguous JSON object. This is the **single source of truth** for all machine-readable metadata about the corpus.

---

## Part II: The JSON Appendix Schema

The appendix MUST be formatted as a JSON code block using triple backticks with `json` language specification. The JSON object MUST conform to the following schema:

```json
{
  "file_manifest": [
    {
      "name": "document_01.txt",
      "document_type": "inaugural",
      "political_party": "Republican",
      "year": 2020,
      "temporal_sequence": 1
    },
    {
      "name": "document_02.txt", 
      "document_type": "sotu",
      "political_party": "Democrat",
      "year": 2021,
      "temporal_sequence": 2
    }
  ]
}
```

**Component Explanations**:

*   **`file_manifest`**: (Optional) An array of objects, where each object contains metadata for a specific file in the corpus directory. The `name` field must match the filename exactly. This is used for experiments that require pre-categorized data.

### Field Naming Standards

**CRITICAL**: All corpus manifests MUST use consistent field names across all documents to enable proper statistical analysis. Inconsistent field naming will cause ANOVA and other statistical tests to fail.

**Required Fields**:
*   **`name`**: (Required) Exact filename including path relative to corpus root
*   **`document_type`**: (Required) Categorical field for grouping documents. Must use consistent values across all documents.

**Common Field Patterns**:
*   **`document_type`**: Use consistent categorical values (e.g., "inaugural", "sotu", "party_platform", "speech", "statement")
*   **`political_party`**: Use consistent party names (e.g., "Republican", "Democrat", "Independent")
*   **`year`**: Use integer year values
*   **`temporal_sequence`**: Use integer sequence numbers for chronological ordering
*   **`speaker`** or **`president`**: Use consistent speaker names
*   **`ideology`**: Use consistent ideological labels (e.g., "progressive", "conservative", "moderate")

**Field Naming Rules**:
1. **Consistency**: Use the same field name for the same concept across ALL documents
2. **Completeness**: All documents must have values for required fields
3. **Uniqueness**: Field names must be unique within each document object
4. **Case Sensitivity**: Field names are case-sensitive - use consistent casing
5. **No Mixed Patterns**: Do not use different field names for the same concept (e.g., don't mix `speech_type` and `document_type`)

**Example of CORRECT Implementation**:
```json
{
  "file_manifest": [
    {
      "name": "clinton_inaugural_1993.txt",
      "document_type": "inaugural",
      "president": "Bill Clinton",
      "political_party": "Democrat",
      "year": 1993,
      "temporal_sequence": 1
    },
    {
      "name": "clinton_sotu_1993.txt",
      "document_type": "sotu", 
      "president": "Bill Clinton",
      "political_party": "Democrat",
      "year": 1993,
      "temporal_sequence": 2
    },
    {
      "name": "democratic_platform_1992.txt",
      "document_type": "party_platform",
      "political_party": "Democrat", 
      "year": 1992,
      "temporal_sequence": 3
    }
  ]
}
```

**Example of INCORRECT Implementation** (causes statistical test failures):
```json
{
  "file_manifest": [
    {
      "name": "clinton_inaugural_1993.txt",
      "speech_type": "inaugural",  // ❌ Inconsistent field name
      "president": "Bill Clinton"
    },
    {
      "name": "democratic_platform_1992.txt", 
      "document_type": "party_platform",  // ❌ Different field name for same concept
      "political_party": "Democrat"
    }
  ]
}
```

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

### 4. Field Naming Validation

*   **Consistency Check**: Verify that all documents use the same field names for the same concepts.
*   **Completeness Check**: Ensure all required fields have values for every document.
*   **Statistical Test Validation**: Test that ANOVA and other statistical tests can find the expected grouping variables.
*   **Cross-Reference Validation**: Verify that field names match what the experiment specification expects.

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

---

## Changelog

### v3.2 (2025-07-31)
- **CRITICAL ADDITION**: Added comprehensive Field Naming Standards section to prevent statistical test failures
- **Rationale**: Inconsistent field naming (e.g., mixing `speech_type` and `document_type`) causes ANOVA and other statistical tests to fail
- **New Requirements**: 
  - All corpus manifests MUST use consistent field names across all documents
  - `document_type` is now a required field for categorical grouping
  - Added validation guidelines for field naming consistency
  - Provided correct/incorrect implementation examples
- **Impact**: Prevents task failures like `task_07_contextual_variation_analysis` that occurred due to inconsistent column naming

### v3.1 (2025-07-31)
- **BREAKING CHANGE**: Updated JSON appendix format specification to use ````json` code blocks instead of `<details><summary>` HTML tags
- **Rationale**: Aligns specification with implementation reality and simplifies corpus manifest parsing
- **Migration**: Replace `<details><summary>Machine-Readable Configuration</summary>` with ````json` and `</details>` with ```` 