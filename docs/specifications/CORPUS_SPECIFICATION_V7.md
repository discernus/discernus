# Corpus Specification (v7.0)

**Version**: 7.0
**Status**: Active
**Major Change**: Gasket Architecture Integration, Enhanced Field Naming Standards, and Document Processing Standards

**Principle**: The integrity of a computational analysis depends entirely on the integrity of the input corpus. This document defines the standard for creating a research-grade, self-documenting corpus that supports the v7.0 gasket architecture.

**🚀 NEW IN V7.0: Gasket Architecture Support + Document Processing Standards**

Version 7.0 aligns with Framework Specification v7.0 and Experiment Specification v7.0 to support the complete gasket architecture workflow. Enhanced field naming standards prevent statistical processing failures and ensure MECE Trinity coherence. Document processing standards ensure reliable analysis across all supported file formats.

---

## Part I: Document Processing Standards (v7.0)

### Supported File Formats

**Primary Formats** (Recommended):
- **`.txt`** (UTF-8 encoded) - Most reliable for analysis
- **`.md`** (Markdown) - Good for structured content
- **`.csv`** (Comma-separated values) - For tabular data
- **`.json`** (JavaScript Object Notation) - For structured data
- **`.yaml`** / **`.yml`** (YAML) - For configuration data

**Secondary Formats** (Supported with caveats):
- **`.doc`** / **`.docx`** (Microsoft Word) - Requires text extraction
- **`.rtf`** (Rich Text Format) - Requires text extraction
- **`.pdf`** (Portable Document Format) - **Deprecated**, requires text extraction

**File Size Limits by Model**:
- **Flash Lite**: Maximum 500KB text content (~250K tokens)
- **Flash**: Maximum 1MB text content (~500K tokens)  
- **Pro**: Maximum 2MB text content (~1M tokens)

### Content Quality Standards

**Minimum Requirements**:
- **Content Length**: Minimum 1,000 characters of substantive text
- **Language**: Primary language must be clearly identifiable
- **Structure**: Should have logical paragraph breaks and formatting
- **Encoding**: UTF-8 encoding throughout

**Quality Validation**:
- **File Size**: Within model limits for target LLM
- **Content Quality**: Substantive content, not empty or corrupted
- **Metadata Completeness**: All required fields present
- **Encoding Validation**: UTF-8 without corruption
- **Token Estimation**: Approximate token count validation

### Preprocessing Requirements

**Text Extraction (Complex Formats)**:
- Extract to UTF-8 `.txt` format
- Preserve paragraph structure and logical flow
- Remove headers/footers/page numbers where appropriate
- Maintain speaker attribution if present
- Preserve document metadata in corpus manifest

**Error Handling**:
- **Oversized Files**: Automatic rejection with clear error message
- **Missing Metadata**: Warning with default values
- **Encoding Issues**: Automatic UTF-8 conversion attempt
- **Empty Content**: Rejection with explanation
- **Unsupported Formats**: Clear guidance on required conversion

---

## Part II: The "Narrative + Appendix" Architecture

A Discernus corpus is not just a collection of text files; it is a complete, self-contained research artifact. To achieve this, a corpus directory MUST contain a `corpus.md` file that follows our "Narrative + Appendix" architecture.

1.  **The Narrative (Human-Focused)**: The main body of the `corpus.md` file. This section uses standard Markdown for the researcher to document the "story" of the corpus:
    *   **Collection Methodology**: How and where were the source texts obtained?
    *   **Ethical Considerations**: What steps were taken to ensure ethical use?
    *   **Corpus Description**: A clear description of the corpus contents, scope, and characteristics.
    *   **🆕 Gasket Architecture Compatibility**: How the corpus supports Framework v7.0 analytical dimensions and evidence requirements.
    *   **🆕 Document Processing Standards**: How the corpus complies with v7.0 document processing requirements.

2.  **The Appendix (Machine-Focused)**: A single appendix at the end of the file that contains a single, unambiguous JSON object. This is the **single source of truth** for all machine-readable metadata about the corpus.

---

## Part III: The JSON Appendix Schema (v7.0)

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
  "document_processing_standards": {
    "max_file_size": "500KB",
    "preferred_format": "txt",
    "supported_formats": ["txt", "md", "csv", "json", "yaml", "doc", "docx", "rtf"],
    "deprecated_formats": ["pdf"],
    "encoding": "UTF-8",
    "min_content_length": 1000,
    "quality_validation": [
      "File size within model limits",
      "Content quality meets minimum standards",
      "Metadata completeness for all documents",
      "Encoding validation (UTF-8)",
      "Token count estimation"
    ]
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
      "character_profile": "institutional",
      "file_size": "45KB",
      "content_quality": "high",
      "metadata_complete": true,
      "processing_note": "Extracted from PDF to resolve token limit issues"
    },
    {
      "name": "document_02.txt", 
      "document_type": "sotu",
      "political_party": "Democrat",
      "year": 2021,
      "temporal_sequence": 2,
      "speaker": "speaker_name",
      "ideology": "progressive", 
      "character_profile": "populist",
      "file_size": "38KB",
      "content_quality": "high",
      "metadata_complete": true
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
*   **`document_processing_standards`**: **REQUIRED** - Defines file format support, size limits, and quality requirements
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

### New v7.0 Document Processing Fields:

*   **`file_size`**: Approximate file size in KB/MB
*   **`content_quality`**: Quality assessment ("high", "medium", "low")
*   **`metadata_complete`**: Boolean indicating all required metadata present
*   **`processing_note`**: Optional note about preprocessing (e.g., "Extracted from PDF")

---

## Part IV: Field Naming Standards (v7.0)

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
5. **Document Processing Standards**: File formats, sizes, and quality meet v7.0 requirements

---

## Part V: Statistical Processing Requirements

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

## Part VI: Gasket Architecture Integration

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

## Part VII: MECE Trinity Coherence

Corpus v7.0 ensures coherence with:

- **Framework v7.0**: Supports analytical dimensions and evidence requirements
- **Experiment v7.0**: Provides statistical variables for hypothesis testing
- **Corpus v7.0**: Maintains internal consistency and gasket architecture readiness

---

## Part VIII: Migration from v3.2

### Key Changes from v3.2

1. **Added Gasket Architecture Support**: New metadata sections for v7.0 compatibility
2. **Enhanced Field Naming Standards**: Strict consistency requirements
3. **Statistical Readiness Validation**: Required grouping and categorical variables
4. **Document Processing Standards**: File format support, size limits, and quality requirements
5. **MECE Trinity Integration**: Coherence with Framework v7.0 and Experiment v7.0

### Migration Guide

To convert a v3.2 corpus to v7.0:

1. **Update corpus_version** to "v7.0"
2. **Add gasket_architecture_support section** with v7.0 metadata
3. **Add document_processing_standards section** with file format requirements
4. **Standardize field names** according to v7.0 requirements
5. **Add statistical_readiness section** with required variables
6. **Validate field naming consistency** across all documents
7. **Test with ExperimentCoherenceAgent** to ensure MECE Trinity coherence

---

## Conclusion

The Corpus Specification v7.0 completes the MECE Trinity alignment with Framework v7.0 and Experiment v7.0. Together, they ensure that your corpus provides the reliable, consistent data foundation required for gasket architecture processing.

Your v7.0 corpus is not just a collection of texts; it's a research-grade artifact that enables reliable, reproducible analysis through the complete gasket architecture workflow with robust document processing standards.