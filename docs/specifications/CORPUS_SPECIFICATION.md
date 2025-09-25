# Corpus Specification (v8.0.2)

**Version**: 8.0.2  
**Status**: Current Standard  
**Replaces**: v8.0.1
**Change**: Added custom analytical groupings requirement for statistical analysis

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
└── corpus/                       # Document directory (flexible structure)
    ├── campaign_2024/            # Organized by campaign phase
    │   ├── primary_speeches/     # Sub-organized by speech type
    │   │   ├── speech1.txt
    │   │   └── speech2.txt
    │   └── general_election/     # Another sub-organization
    │       └── speech3.txt
    ├── presidency_2017_2020/     # Organized by time period
    │   ├── inaugural.txt
    │   └── sotu_2020.txt
    └── post_presidency/          # Organized by political phase
        └── rally_2022.txt
```

**Key Principles:**
- Corpus specification at project root (with other input files)
- Actual documents in `/corpus/` directory
- Text files only (`.txt` format for simplicity)
- **Flexible directory structure**: Nested directories allowed for human organization
- **Explicit metadata required**: Directory structure meaning must be defined in metadata, not implied by structure
- Metadata informs analysis strategy (not analyzed as content)

---

## 1.1 Directory Structure Principles

**Human Organization vs. Machine Understanding**

The corpus directory structure serves **human researchers** for organization and convenience, but **all semantic meaning must be explicitly defined in metadata**.

### ✅ **Good: Explicit Metadata with Organized Structure**
```yaml
documents:
  - filename: "campaign_2024/primary_speeches/speech1.txt"
    political_phase: "campaign_2024"
    speech_type: "primary_campaign"
    speaker: "Donald Trump"
    date: "2024-01-15"
    venue: "Iowa Rally"
    
  - filename: "presidency_2017_2020/inaugural.txt"
    political_phase: "first_presidency"
    speech_type: "inaugural_address"
    speaker: "Donald Trump"
    date: "2017-01-20"
    venue: "US Capitol"
```

**Important**: Filenames are **relative to the corpus directory**. Do NOT include `corpus/` prefix in filenames.

### ❌ **Bad: Implicit Meaning from Directory Structure**
```yaml
documents:
  - filename: "campaign_2024/primary_speeches/speech1.txt"
    # Missing political_phase, speech_type - system cannot infer meaning
    speaker: "Donald Trump"
    date: "2024-01-15"
```

### ❌ **Bad: Incorrect Path Prefix**
```yaml
documents:
  - filename: "corpus/campaign_2024/speech1.txt"  # WRONG: includes corpus/ prefix
    speaker: "Donald Trump"
    date: "2024-01-15"
```

### **Directory Organization Guidelines**
- **Use meaningful names**: `campaign_2024/` not `folder1/`
- **Group logically**: By time period, campaign phase, speech type, etc.
- **Keep reasonable depth**: 2-3 levels maximum for maintainability
- **Document organization**: Explain your directory structure in the corpus overview

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
version: "8.0.1"
total_documents: 4
date_range: "2008-2025"

documents:
  - filename: "campaign_2008/mccain_concession.txt"
    speaker: "John McCain"
    year: 2008
    party: "Republican"
    style: "institutional"
    type: "concession_speech"
    political_phase: "campaign_2008"
    administration: "Bush W."  # Custom analytical grouping
    
  - filename: "policy_2025/sanders_oligarchy.txt"
    speaker: "Bernie Sanders"
    year: 2025
    party: "Independent"
    style: "populist_progressive"
    type: "policy_statement"
    political_phase: "policy_2025"
    administration: "Biden"  # Custom analytical grouping
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
- ✅ All listed documents must exist in `corpus/` directory (including nested paths)
- ✅ Document filenames must be **relative to the corpus directory** (no `corpus/` prefix)
- ✅ Document filenames must match exactly (case-sensitive, including path separators)
- ✅ Documents must be readable text files (.txt, .md preferred)
- ✅ No empty or corrupted files
- ✅ **All semantic meaning must be explicitly defined in metadata** (not inferred from directory structure)

### Optional Metadata
- ✅ If present, metadata must be valid YAML
- ✅ Metadata should provide useful context for analysis
- ✅ Document metadata keys must match actual filenames
- ✅ **Custom Analytical Groupings**: For experiments involving statistical comparisons, custom grouping variables (e.g., `administration`, `political_phase`, `speaker_category`) MUST be included as metadata fields for each document. These variables are essential for statistical agents and coherence validation.
- ✅ **Mandatory for Statistical Analysis**: If an experiment's statistical analysis depends on grouping variables, those variables MUST be present in every document's metadata within this corpus. The Coherence Agent will validate this requirement.
- ✅ **Sample Size Adequacy**: Corpus design should consider statistical power requirements. See the Sample Size Requirements section for guidance on appropriate corpus sizes for different types of statistical analysis.

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

### **Update Note (v8.0.1)**
- **Nested directory support**: Added support for organized directory structures
- **Metadata requirement**: All semantic meaning must be explicitly defined in metadata
- **Validation updated**: System now validates nested paths correctly
- **Backward compatible**: Existing flat-structure corpora continue to work

---

## 5. Example v8.0.1 Corpus

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
1. **Specification Reading**: v8.0.1 loader reads raw corpus.md content
2. **Document Discovery**: Loads files according to manifest (no directory scanning)
3. **Path Resolution**: Handles nested directory paths correctly
4. **Metadata Extraction**: Parses optional YAML metadata if present
5. **Validation**: Ensures all listed documents exist and are readable
6. **Content Preparation**: Loads document content for analysis agents

### Analysis Integration
- **Framework Agnostic**: Works with any v8.0.1 framework
- **Flexible Metadata**: Optional structured data for advanced analysis
- **Human Context**: Document descriptions inform analysis approach
- **Scalable**: Handles small focused corpora or large document collections
- **Organized Structure**: Supports nested directories for logical organization
- **Explicit Semantics**: All analytical meaning comes from metadata, not structure

### Custom Analytical Groupings for Statistical Analysis

For experiments that require statistical analysis (e.g., ANOVA, t-tests), the corpus manifest MUST provide the necessary grouping variables in each document's metadata. This is a critical requirement for coherence and valid statistical execution.

- **Defining Grouping Variables**: Add custom key-value pairs to each document's metadata. The key represents the grouping variable (e.g., `administration`), and the value is the group assignment (e.g., `"Trump"`).
- **Consistency is Key**: The grouping variable must be applied consistently to all documents in the corpus.
- **Experiment Coherence**: The grouping variables defined here MUST align with the variables requested in the `experiment.md` file. The Coherence Agent will validate this linkage.
- **No Implied Metadata**: Statistical agents are strictly forbidden from parsing filenames or directory structures to infer analytical groups. All grouping information must be explicit in the manifest.

### Sample Size Requirements for Statistical Analysis

When designing corpora for statistical analysis, consider the following sample size requirements:

- **N≥30**: Full inferential statistical analysis with adequate power
- **N=20-29**: Limited inferential testing, focus on effect sizes and confidence intervals  
- **N=10-19**: Descriptive statistics only, no hypothesis testing
- **N=4-9**: Case study analysis, qualitative patterns, individual document insights
- **N<4**: Single case or comparative case analysis only

**Statistical Power Considerations:**
- **Group Comparisons**: Each group should have sufficient sample size for the intended statistical tests
- **Multiple Comparisons**: Account for post-hoc correction requirements when planning group sizes
- **Effect Size Detection**: Larger samples enable detection of smaller, more meaningful effects

**Available Analytical Capabilities:**
See the [Core Capabilities Registry](../../discernus/core/presets/core_capabilities.yaml) for the complete list of available statistical libraries and their specific functions. The registry is maintained by the platform and may be updated to include additional libraries as they become available.

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

This v8.0.1 specification balances human readability with structured metadata support, enabling both intuitive corpus management and systematic analysis. It now supports organized directory structures while maintaining the principle that all semantic meaning must be explicitly defined in metadata.
