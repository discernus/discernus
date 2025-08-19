# Corpus Specification (v8.0)

**Version**: 8.0  
**Status**: Current Standard  
**Replaces**: v7.3

The `corpus.md` file defines a collection of documents for analysis in the v8.0 Discernus system. It serves as the **manifest and metadata source** for all textual materials in an experiment, providing human-readable descriptions with structured YAML metadata.

**Design Philosophy**: Human-first readability with rich metadata to inform analysis strategy (not analyzed as content).

---

## 1. File Structure & Location

The corpus file MUST be a Markdown file named `corpus.md` located at the **project root** (not in corpus directory).

```
my_research_project/
├── experiment.md                 # Experiment specification
├── corpus.md                     # Corpus specification (at root)
├── framework.md                  # Framework file (descriptive name)
└── corpus/                       # Document directory (flat structure)
    ├── document1.txt             # Text files only
    ├── document2.txt
    └── document3.txt
```

**Key Principles:**
- Corpus specification at project root (with other input files)
- Actual documents in `/corpus/` directory
- Text files only (`.txt` format for simplicity)
- Flat directory structure (no nested folders)
- Metadata informs analysis strategy (not analyzed as content)

---

## 2. File Format

The file follows the **human-first** format: natural language description followed by YAML metadata appendix.

```markdown
# Political Speeches Corpus

Four paradigmatic examples of American political communication spanning institutional and populist approaches. Selected to represent key temporal moments and rhetorical styles in contemporary democratic discourse.

The corpus includes concession speeches, floor speeches, and campaign addresses that demonstrate different approaches to democratic engagement and public persuasion.

## Document Overview

- **McCain 2008**: Institutional democratic discourse emphasizing unity and norms
- **Sanders 2025**: Progressive populist rhetoric with economic justice themes  
- **AOC 2025**: Progressive populist discourse with systemic critique
- **King 2017**: Conservative populist discourse with nationalist themes

---

## Document Manifest

```yaml
name: "Political Speeches Corpus"
version: "8.0"
total_documents: 4
date_range: "2008-2025"

documents:
  - filename: "mccain_2008_concession.txt"
    speaker: "John McCain"
    year: 2008
    party: "Republican"
    style: "institutional"
    type: "concession_speech"
    
  - filename: "sanders_2025_oligarchy.txt"
    speaker: "Bernie Sanders"
    year: 2025
    party: "Independent"
    style: "populist_progressive"
    type: "policy_statement"
```
```

---

## 3. Validation Rules

### File Structure
- ✅ File must be named `corpus.md`
- ✅ File must be located in experiment root directory
- ✅ File must contain valid markdown syntax

### Required Content
- ✅ Corpus name in header (`# Corpus Name`)
- ✅ Overview section with corpus description
- ✅ Documents section listing all files
- ✅ Each document must have brief description

### Document Requirements  
- ✅ All listed documents must exist in `corpus/` directory
- ✅ Document filenames must match exactly (case-sensitive)
- ✅ Documents must be readable text files (.txt, .md preferred)
- ✅ No empty or corrupted files

### Optional Metadata
- ✅ If present, metadata must be valid YAML
- ✅ Metadata should provide useful context for analysis
- ✅ Document metadata keys must match actual filenames

---

## Migration from v7.3 to v8.0

**File Name**: `corpus.md` → `corpus.md` (no change needed)
**Location**: Move to experiment root directory
**Format**: Keep human-readable markdown with YAML metadata
**Structure**: Maintain document manifest format

### Migration Steps:
1. **No file rename needed** - keep `corpus.md`
2. **Move file** from `corpus/` directory to experiment root
3. **Update experiment.md** to reference `corpus.md` (not `corpus/corpus_v8.md`)
4. **Verify YAML metadata** is properly formatted
5. **Ensure text files** remain in `corpus/` directory

### Compatibility
- **v8.0 corpus** specifications are NOT compatible with v7.3 systems
- **v7.3 corpus** specifications are NOT compatible with v8.0 pipeline
- **No automatic migration** - corpus files must be manually updated

---

## 5. Example v8.0 Corpus

A valid corpus manifest `corpus.md` file MUST be a Markdown document containing a YAML appendix with the following structure:

```yaml
name: "Name of the Corpus"
version: "1.0"
description: "A brief description of the corpus."
documents:
  - filename: "document1.txt"
    document_id: "unique_id_1"
    metadata:
      author: "Author Name"
      date: "YYYY-MM-DD"
  - filename: "document2.txt"
    document_id: "unique_id_2"
    metadata:
      author: "Another Author"
      date: "YYYY-MM-DD"
```

### 3. Document Content

Each document listed in the manifest must exist as a plain text (`.txt`) file within the `corpus/` subdirectory of the experiment.

### 4. Validation Rules

1.  **YAML Validity:** The appendix must be valid YAML.
2.  **Required Fields:** The `name`, `version`, and `documents` fields are mandatory.
3.  **Document Fields:** Each entry in `documents` must have a `filename` and a `document_id`.
4.  **File Existence:** The file specified in `filename` must exist in the `corpus/` directory.
5.  **ID Uniqueness:** All `document_id` values must be unique within the manifest.

---

## 6. Integration with v8.0 Pipeline

### Loading Process
1. **Specification Reading**: v8.0 loader reads raw corpus.md content
2. **Document Discovery**: Automatically scans corpus/ directory
3. **Metadata Extraction**: Parses optional YAML metadata if present
4. **Validation**: Ensures all listed documents exist and are readable
5. **Content Preparation**: Loads document content for analysis agents

### Analysis Integration
- **Framework Agnostic**: Works with any v8.0 framework
- **Flexible Metadata**: Optional structured data for advanced analysis
- **Human Context**: Document descriptions inform analysis approach
- **Scalable**: Handles small focused corpora or large document collections

---

## 7. Best Practices

### Corpus Design
- **Focused Selection**: Choose documents that serve specific research questions
- **Representative Sample**: Include diverse perspectives relevant to analysis
- **Quality Control**: Ensure all documents are complete and readable
- **Appropriate Scale**: Match corpus size to analytical capacity

### Document Descriptions
- **Informative**: Provide context about content and significance
- **Concise**: Keep descriptions brief but meaningful
- **Consistent**: Use similar format and detail level across documents
- **Objective**: Focus on factual description, not interpretation

### Metadata Usage
- **Optional Enhancement**: Use metadata to enrich analysis, not replace description
- **Structured Consistency**: If using metadata, apply consistently across documents
- **Relevant Fields**: Include metadata that supports research questions
- **Validation Ready**: Ensure metadata accuracy for reliable analysis

### File Organization
- **Clear Naming**: Use descriptive, consistent document filenames
- **Logical Structure**: Organize documents meaningfully within corpus/
- **Version Control**: Track changes to corpus composition and metadata
- **Documentation**: Explain corpus creation and curation decisions

This v8.0 specification balances human readability with structured metadata support, enabling both intuitive corpus management and systematic analysis.
