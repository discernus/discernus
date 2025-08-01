# Corpus Specification (v7.0)

**Version**: 7.0
**Status**: Active
**Major Change**: Gasket Architecture Integration and Enhanced Field Naming Standards

**Principle**: The integrity of a computational analysis depends entirely on the integrity of the input corpus. This document defines the standard for creating a research-grade, self-documenting corpus that supports the v7.0 gasket architecture.

**🚀 NEW IN V7.0: Gasket Architecture Support**

Version 7.0 aligns with Framework Specification v7.0 and Experiment Specification v7.0 to support the complete gasket architecture workflow. Enhanced field naming standards prevent statistical processing failures and ensure MECE Trinity coherence.

---

## Part I: The "Narrative + Appendix" Architecture

A Discernus corpus is not just a collection of text files; it is a complete, self-contained research artifact. To achieve this, a corpus directory MUST contain a `corpus.md` file that follows our "Narrative + Appendix" architecture.

1.  **The Narrative (Human-Focused)**: The main body of the `corpus.md` file. This section uses standard Markdown for the researcher to document the "story" of the corpus:
    *   **Collection Methodology**: How and where were the source texts obtained?
    *   **Ethical Considerations**: What steps were taken to ensure ethical use?
    *   **Corpus Description**: A clear description of the corpus contents, scope, and characteristics.
    *   **🆕 Gasket Architecture Compatibility**: How the corpus supports Framework v7.0 analytical dimensions and evidence requirements.

2.  **The Appendix (Machine-Focused)**: A single appendix at the end of the file that contains a single, unambiguous JSON object. This is the **single source of truth** for all machine-readable metadata about the corpus.

---

## Part II: The JSON Appendix Schema (v7.0)

The appendix MUST be formatted as a JSON code block using triple backticks with `json` language specification. The JSON object MUST conform to the following v7.0 schema:

```json
{
  "corpus_version": "v7.0",
  "gasket_architecture_support": {
    "framework_compatibility": ["v7.0"],
    "raw_analysis_log_ready": true,
    "evidence_extraction_optimized": true,
    "field_naming_validated": true
  },
  "file_manifest": [
    {
      "name": "document_01.txt",
      "document_type": "inaugural",
      "political_party": "Republican",
      "year": 2020,
      "temporal_sequence": 1,
      "speaker": "speaker_name",
      "ideology": "conservative",
      "character_profile": "institutional"
    },
    {
      "name": "document_02.txt", 
      "document_type": "sotu",
      "political_party": "Democrat",
      "year": 2021,
      "temporal_sequence": 2,
      "speaker": "speaker_name",
      "ideology": "progressive", 
      "character_profile": "populist"
    }
  ],
  "field_naming_standards": {
    "required_consistency": [
      "document_type",
      "political_party", 
      "speaker",
      "ideology"
    ],
    "prohibited_variations": [
      "speech_type (use document_type)",
      "party (use political_party)",
      "author (use speaker)"
    ]
  },
  "statistical_readiness": {
    "grouping_variables": ["ideology", "speaker", "political_party"],
    "temporal_variables": ["year", "temporal_sequence"],
    "categorical_variables": ["document_type", "character_profile"],
    "missing_data_tolerance": 0.10
  }
}
```

**Component Explanations**:

### New v7.0 Fields:

*   **`corpus_version`**: **REQUIRED** - Must be "v7.0" for gasket architecture compatibility
*   **`gasket_architecture_support`**: **REQUIRED** - Metadata confirming corpus readiness for v7.0 workflow
*   **`field_naming_standards`**: **REQUIRED** - Enforces consistent field naming to prevent statistical failures
*   **`statistical_readiness`**: **REQUIRED** - Defines variables for mathematical processing and ANOVA analysis

### Enhanced v7.0 File Manifest:

*   **`file_manifest`**: An array of objects, where each object contains metadata for a specific file in the corpus directory. The `name` field must match the filename exactly.

### Required v7.0 Fields per Document:

*   **`name`**: Exact filename in corpus directory
*   **`document_type`**: Type of document (e.g., "inaugural", "sotu", "speech", "debate")
*   **`political_party`**: Political affiliation (e.g., "Republican", "Democrat", "Independent")
*   **`year`**: Year of document creation (integer)
*   **`temporal_sequence`**: Sequential ordering for temporal analysis (integer)
*   **`speaker`**: Name or identifier of the speaker
*   **`ideology`**: Ideological classification (e.g., "conservative", "progressive", "moderate")
*   **`character_profile`**: Character style classification (e.g., "institutional", "populist", "diplomatic")

---

## Part III: Field Naming Standards (v7.0)

**CRITICAL**: Version 7.0 introduces strict field naming standards to prevent statistical processing failures.

### Required Field Names

These field names MUST be used consistently across all documents:

- **`document_type`** (NOT `speech_type`, `text_type`, or `type`)
- **`political_party`** (NOT `party`, `affiliation`, or `political_affiliation`)
- **`speaker`** (NOT `author`, `politician`, or `name`)
- **`ideology`** (NOT `political_ideology`, `leaning`, or `position`)

### Prohibited Field Variations

These variations will cause statistical processing failures:

- ❌ `speech_type` → ✅ `document_type`
- ❌ `party` → ✅ `political_party`
- ❌ `author` → ✅ `speaker`
- ❌ Mixed usage of any field name variations

### Validation Requirements

The ExperimentCoherenceAgent will validate:

1. **Consistency**: All documents use identical field names
2. **Completeness**: All required fields are present
3. **Statistical Readiness**: Grouping variables are properly defined
4. **Gasket Compatibility**: Fields support Framework v7.0 analytical dimensions

---

## Part IV: Statistical Processing Requirements

### Grouping Variables for ANOVA

The corpus MUST support these statistical analyses:

- **Ideological Analysis**: `ideology` field enables ideological comparison
- **Speaker Analysis**: `speaker` field enables speaker-specific analysis  
- **Party Analysis**: `political_party` field enables partisan analysis
- **Temporal Analysis**: `year` and `temporal_sequence` enable temporal trends

### Missing Data Tolerance

- **Maximum Missing Data**: 10% per field
- **Required Fields**: Cannot have missing data: `name`, `document_type`, `speaker`
- **Statistical Fields**: Cannot have missing data: `ideology`, `political_party`

---

## Part V: Gasket Architecture Integration

### Framework v7.0 Compatibility

The corpus must support Framework v7.0 requirements:

- **Analytical Dimensions**: Corpus metadata enables framework dimension analysis
- **Evidence Extraction**: Document structure supports evidence quote extraction
- **Raw Analysis Log**: Content format supports natural language analysis

### Intelligent Extractor Support

The corpus structure must support Gasket #2 (Intelligent Extractor):

- **Clear Document Boundaries**: Each document is a separate file
- **Consistent Metadata**: Field naming enables reliable extraction
- **Evidence Traceability**: Document structure supports provenance tracking

---

## Part VI: MECE Trinity Coherence

Corpus v7.0 ensures coherence with:

- **Framework v7.0**: Supports analytical dimensions and evidence requirements
- **Experiment v7.0**: Provides statistical variables for hypothesis testing
- **Corpus v7.0**: Maintains internal consistency and gasket architecture readiness

---

## Part VII: Migration from v3.2

### Key Changes from v3.2

1. **Added Gasket Architecture Support**: New metadata sections for v7.0 compatibility
2. **Enhanced Field Naming Standards**: Strict consistency requirements
3. **Statistical Readiness Validation**: Required grouping and categorical variables
4. **MECE Trinity Integration**: Coherence with Framework v7.0 and Experiment v7.0

### Migration Guide

To convert a v3.2 corpus to v7.0:

1. **Update corpus_version** to "v7.0"
2. **Add gasket_architecture_support section** with v7.0 metadata
3. **Standardize field names** according to v7.0 requirements
4. **Add statistical_readiness section** with required variables
5. **Validate field naming consistency** across all documents
6. **Test with ExperimentCoherenceAgent** to ensure MECE Trinity coherence

---

## Conclusion

The Corpus Specification v7.0 completes the MECE Trinity alignment with Framework v7.0 and Experiment v7.0. Together, they ensure that your corpus provides the reliable, consistent data foundation required for gasket architecture processing.

Your v7.0 corpus is not just a collection of texts; it's a research-grade artifact that enables reliable, reproducible analysis through the complete gasket architecture workflow.