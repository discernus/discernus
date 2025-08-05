# Corpus Specification (v7.1)

**Version**: 7.1  
**Status**: Active - Current Standard

**Principle**: The integrity of a computational analysis depends entirely on the integrity of the input corpus. This document defines the standard for creating a research-grade, self-documenting corpus that supports the v7.2 analysis architecture.

---

## Part I: The "Narrative + Appendix" Architecture
A Discernus corpus is a complete research artifact. It MUST contain a `corpus.md` file that separates the "what and why" from the "how":

1.  **The Narrative (The "What" and "Why")**: The main body of the `corpus.md` file. This section uses standard Markdown for the researcher to document the "story" of the corpus:
    *   **Collection Methodology**: How and where were the source texts obtained?
    *   **Ethical Considerations**: What steps were taken to ensure ethical use?
    *   **Corpus Description**: A clear description of the corpus contents, scope, and characteristics.
    *   **Support for Analytical Goals**: How does the corpus structure support the intended analysis (e.g., temporal, comparative)?

2.  **The Appendix (The "How")**: A single, collapsible appendix containing a single JSON object. This is the **single source of truth** for all machine-readable metadata.

---

## Part II: The JSON Appendix Schema (v7.1)
The appendix MUST be formatted as a JSON code block.

```json
{
  "corpus_version": "v7.1",
  "file_manifest": [
    {
      "name": "document_01.txt",
      "document_type": "inaugural",
      "party": "Republican",
      "year": 2020,
      "temporal_sequence": 1,
      "speaker": "speaker_name"
    }
  ],
  "field_naming_standards": {
    "required_consistency": ["document_type", "party", "speaker", "year"],
    "prohibited_variations": {
      "speech_type": "document_type",
      "political_party": "party",
      "author": "speaker"
    }
  },
  "statistical_readiness": {
    "grouping_variables": ["party", "speaker", "document_type"],
    "temporal_variables": ["year", "temporal_sequence"]
  }
}
```

### 1. `file_manifest`
An array of objects, where each object contains metadata for a specific file. `name` is required.

#### **Best Practices for Temporal Analysis**
For corpora designed for longitudinal or time-series analysis, the following metadata fields are strongly recommended for each document in the manifest:
- **`year` (integer)**: The publication year of the document. Essential for grouping by year.
- **`temporal_sequence` (integer)**: An explicit integer that orders the documents chronologically. This is the most reliable way to ensure correct ordering, especially for documents within the same year.
- **`date` (string, ISO 8601 format)**: For more granular analysis, a full date (e.g., `"2020-01-20"`) can be included.

A well-structured temporal corpus allows the Synthesis Agent to perform trend analysis, change point detection, and other time-series-based statistical operations.

### 2. `field_naming_standards`
- **`required_consistency`**: A list of metadata fields that MUST be used consistently across all documents in the manifest. Inconsistent naming will cause statistical analysis to fail.
- **`prohibited_variations`**: A dictionary mapping common incorrect field names to their required, standardized equivalent. This serves as a clear guide for authors.

### 3. `statistical_readiness`
- **`grouping_variables`**: A list of categorical fields that will be used for comparative analysis (e.g., ANOVA).
- **`temporal_variables`**: A list of fields that will be used for time-series analysis.

---

## Part III: Document Processing & Quality Standards

### Supported File Formats
- **Primary**: `.txt` (UTF-8), `.md`
- **Secondary (require extraction)**: `.docx`, `.rtf`
- **Deprecated**: `.pdf`

### Content Quality
- **Minimum Length**: 1,000 characters of substantive text.
- **Encoding**: UTF-8 is required.

---

## Conclusion
The Corpus Specification v7.1 provides a robust standard for creating well-documented, research-grade corpora. By adhering to these standards, particularly for temporal metadata and consistent field naming, authors enable powerful and reliable longitudinal analysis.
