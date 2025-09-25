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

### Section 4: Available Analytical Capabilities

**(Reference Information)**
Discernus provides a comprehensive suite of statistical and analytical tools for your experiments. When designing your statistical analysis plan, you have access to:

**Statistical Analysis Capabilities:**
- **Core Statistics**: Hypothesis testing, effect sizes, and advanced statistical modeling
- **Post-hoc Testing**: Multiple comparison corrections (Dunn's, Tukey's, etc.)
- **Data Manipulation**: Data processing, aggregation, and analysis
- **Visualization**: Statistical plots and interactive dashboards

**Text Analysis Capabilities:**
- **Sentiment Analysis**: Emotional tone analysis and sentiment scoring
- **Text Processing**: Tokenization, stemming, and readability metrics
- **Pattern Recognition**: Regular expressions and string manipulation tools

**Power Analysis & Sample Size Planning:**
- Power analysis and effect size calculations
- Three-tier statistical approaches based on sample size adequacy
- See the [Core Capabilities Registry](../../discernus/core/presets/core_capabilities.yaml) for the complete list of available libraries and their specific functions

**Best Practice**: When specifying statistical tests in your experiment, consider the available tools and design your analysis plan accordingly. The system will automatically select appropriate statistical methods based on your sample sizes and research questions. The capabilities registry is maintained by the platform and may be updated to include additional libraries as they become available.

### Section 5: Data Grouping and Custom Variable Mapping

**(Required for Statistical Analysis)**
If your experiment requires statistical analysis using grouping variables not explicitly present in the corpus manifest (e.g., `time_period`, `category`, `group_type`), you MUST define them explicitly.

#### 5.1 Corpus Manifest Integration
- Statistical analyses must use corpus manifest metadata as the primary data source
- Standard manifest fields vary by domain but commonly include: `speaker`, `author`, `year`, `category`, `type`, `format`
- **CRITICAL**: Custom grouping variables (e.g., `time_period`, `administration`) MUST be present as fields in the corpus manifest metadata
- **FORBIDDEN**: Statistical agents must NEVER parse filenames to derive metadata - all metadata must come from the corpus manifest

#### 5.2 Custom Grouping Variables
There are two approaches for grouping variables:

**Option A: Direct Corpus Field** (Preferred)
If the corpus manifest already contains the grouping field (e.g., `administration: "Trump"`), use it directly in statistical analyses.

**Option B: Derived Mapping** (When needed)
When your experiment requires grouping logic beyond simple corpus fields:

**Example: Time Period Mapping**
```yaml
time_period_mapping:
  "Early Period":
    speakers: ["Author A", "Speaker 1"]
    years: [1990-1995]
    context: "Initial development phase"
    
  "Middle Period":
    speakers: ["Author B", "Author C"]
    years: [1996-2005]
    context: "Expansion and growth"
    
  "Recent Period":
    speakers: ["Author D", "Speaker 2", "Author E"]
    years: [2006-present]
    context: "Modern developments"
    note: "Combines multiple recent contributors"
```

**Statistical Grouping Instructions:**
- **Primary Analysis Variable**: Specify the main grouping variable and number of groups
- **Baseline References**: Groups excluded from inferential tests (e.g., n=1 groups)
- **Secondary Variables**: Additional grouping variables for analysis
- **Corpus Manifest Mapping**: How to derive custom variables from manifest fields
- **Missing Data Handling**: How to handle unmatched or missing cases

#### 5.3 Statistical Executability Requirements
- **ANOVA Groups**: All groups must have n≥2 for inferential testing
- **Baseline Groups**: Single-observation groups (n=1) must be designated as baselines, excluded from ANOVA
- **Variance Tests**: Groups must have sufficient variance for homogeneity testing
- **Missing Data**: Specify handling of speakers/documents that don't match the mapping

#### 5.4 Coherence Validation
The coherence agent will validate that:
1. **Grouping Variable Existence**: Every grouping variable requested for statistical analysis in this experiment MUST exist as a metadata field in the associated `corpus.md` manifest for all documents.
2. **Statistical Executability**: All groups intended for comparative statistical analysis (e.g., ANOVA) must contain a sufficient number of documents (n≥2). Single-document groups must be explicitly designated as baselines.
3. **Mapping Logic**: If custom variable mappings are used, the logic must be unambiguous and complete.

**Experiments that reference undefined grouping variables will fail coherence validation.**

---

## Part 2: The Machine-Readable Appendix

This is a single YAML block at the end of the document containing the precise configuration for the orchestrator.

### Section 6: Configuration Appendix

**(Required)**

```yaml
# --- Start of Machine-Readable Appendix ---

# 6.1: Metadata (Required)
metadata:
  experiment_name: "your_experiment_name_in_snake_case"
  author: "Your Name or Organization"
  spec_version: "10.0"

# 6.2: Components (Required)
components:
  # The framework file must be named "framework.md" and located in the same directory as this experiment.md.
  # This standardized naming eliminates the need for path parsing and ensures consistent file discovery.
  framework: "framework.md"

  # The corpus manifest file must be named "corpus.md" and located in the same directory as this experiment.md.
  corpus: "corpus.md"

# --- End of Machine-Readable Appendix ---
```

---

## Validation Rules

### Basic Requirements
-   The file must be named `experiment.md`.
-   It must contain a valid YAML appendix.
-   All required fields (`experiment_name`, `spec_version`, `framework`, `corpus`) must be present.
-   The `spec_version` in the experiment must be compatible with the `spec_version` in the referenced framework.
-   The framework file must be named `framework.md` and located in the same directory as `experiment.md`.
-   The corpus manifest file must be named `corpus.md` and located in the same directory as `experiment.md`.
-   The corpus directory must exist and contain the files specified in the corpus manifest.

### Statistical Analysis Requirements (New in v10.0)
-   **Corpus Metadata Linkage**: All grouping variables used in statistical analyses MUST either:
    - Exist directly as fields in the corpus manifest metadata, OR
    - Be explicitly defined via mappings in the **Data Grouping and Custom Variable Mapping** section
-   **No Filename Parsing**: Statistical agents are FORBIDDEN from parsing filenames to derive metadata
-   **Statistical Executability**: All ANOVA groups must have n≥2. Single-observation groups (n=1) must be designated as baselines and excluded from inferential testing.
-   **Semantic Alignment**: The experiment, corpus manifest, and framework must use consistent terminology. Custom mappings must eliminate ambiguity about how corpus metadata maps to analysis variables.

### Statistical Power and Methodology Requirements
-   **Sample Size Adequacy**: Statistical tests must be appropriate for available sample sizes:
    - **N≥30**: Full inferential statistical analysis with adequate power
    - **N=20-29**: Limited inferential testing, focus on effect sizes and confidence intervals  
    - **N=10-19**: Descriptive statistics only, no hypothesis testing
    - **N=4-9**: Case study analysis, qualitative patterns, individual document insights
    - **N<4**: Single case or comparative case analysis only
-   **Test Appropriateness**: Statistical tests must match data types and research questions:
    - **Non-parametric tests** for ordinal data or small samples
    - **Parametric tests** only when assumptions are met (normality, equal variance)
    - **Post-hoc corrections** required for multiple comparisons
-   **Power Analysis**: For experiments with N<30, include power analysis and effect size calculations
-   **Methodological Coherence**: Statistical tests must align with framework output dimensions and measurement scales

### Coherence Validation Requirements
The coherence agent will validate that:
-   **Grouping Variable Presence**: All grouping variables referenced in the experiment exist in the corpus manifest's metadata for every document.
-   **Statistical Requirements**: Group sizes and variance meet the minimum requirements for the specified statistical tests.
-   **Methodological Appropriateness**: Statistical tests are suitable for the data types and sample sizes available.
-   **Executability**: The overall experiment design is coherent and executable with the provided corpus data.
