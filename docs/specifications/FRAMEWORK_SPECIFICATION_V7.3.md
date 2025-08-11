# Framework Specification (v7.3)

**Version**: 7.3  
**Status**: DRAFT - Proposed Definitive Standard

---

## Introduction

A Discernus framework is a self-contained markdown file that serves as the core intellectual asset for rigorous, repeatable text analysis. It represents the primary **analytical lens** through which all analysis and synthesis is performed in an experiment. As such, it must be carefully crafted to provide the intended insights, while also being scoped to a focused set of related concepts.

The framework's core innovation is its unique combination of a human-readable scholarly narrative with machine-executable instructions. This creates a direct, auditable link between research methodology and its computational implementation. This specification details the principles and technical requirements for building these powerful, research-grade analytical tools.

---

## Part I: Core Principles

1.  **The THIN Philosophy**: LLMs do intelligence, software does infrastructure.
2.  **Documentation-Execution Coherence**: The narrative ("what" and "why") must perfectly align with the appendix ("how").
3.  **Human Expert Simulation**: Write prompts like you're briefing a brilliant colleague.
4.  **Chain-of-Thought Analysis**: Break down complex analysis into sequential, focused steps.
5.  **Epistemic Integrity**: All analytical decisions must be traceable and auditable.
6.  **Cognitive Task Separation**: Analysis (LLM) and calculation (code) must be separate.
7.  **Theoretically Grounded Measurement**: All metrics, weights, and classifications must be justified by theory.
8.  **The Principle of Parsimony**: Strive for the simplest effective model.

---

## Part II: Framework Authoring Guide

### 1. File Structure: The "Narrative + Appendix" Architecture
A framework file MUST contain two sections that separate the "what and why" from the "how":
1.  **The Narrative (The "What" and "Why")**: The main body of the file, explaining the framework's theory, methodology, and objectives.
2.  **The Appendix (The "How")**: A single, collapsible appendix containing a single JSON object—the **single source of truth for execution**.

### 2. The Narrative: The Story of Your Framework
Your narrative is a scholarly document and must contain:
- **Raison d'Être**: The research gap the framework fills.
- **Research Foundations**: The academic theories it is built upon, with citations.
- **Framework Dimensions and Axes**: Define each dimension conceptually. If dimensions form a bipolar pair (e.g., Hope vs. Fear), define this "axis".
- **Linguistic Markers**: Illustrative linguistic patterns for each dimension. **Critical**: These markers represent semantic spaces, not keyword lists. Framework authors should emphasize that analysts should look for the underlying concepts and meanings, not just literal word matches. Include guidance like "Look for [concept] patterns such as [examples], but consider related semantic expressions beyond these specific words."
- **Analysis Methodology**: Explain your chain-of-thought process and scoring logic. **Recommended**: Structure analysis as sequential, focused steps where each step examines one dimension group or axis at a time. This approach has shown significant improvements in analytical consistency and evidence quality.
- **Weighting Scheme**: Explicitly define and justify your chosen weighting scheme. Both **dynamic** (e.g., salience) and **static** (theory-driven) weights are supported.
- **Calculated Metrics & Pattern Classifications**: Explain the theory behind all derived values (e.g., Tension Mathematics) and interpretive rubrics (e.g., Strategic Contradiction Indices).
- **Reliability and Validity**: Explain the basis for the framework's reliability.
- **Considerations on Bias**: A discussion of potential biases and how the framework's design attempts to mitigate them.

**Advanced Narrative Patterns (Recommended Best Practices):**
- **Analytical Layers**: For complex frameworks, you may define normative "layers" (e.g., Layer 1: Pattern Recognition, Layer 3: Social Health Evaluation) to provide transparency about the interpretive depth of your analysis.
- **Inter-Framework Relationships**: If your framework is designed to be used in concert with others (see `docs/research/TRIADIC_ANALYSIS_GUIDE.md`), describe its role in that larger analytical system.

### 3. The Appendix: The Single Source of Truth
The appendix MUST begin with `<details><summary>Machine-Readable Configuration</summary>` and end with `</details>`.

#### **JSON Schema (v7.3)**
```json
{
  "name": "unique_framework_name",
  "version": "v7.3",
  "display_name": "Human-Readable Framework Name",
  "analysis_variants": {
    "default": {
      "description": "The primary analysis method for this framework.",
      "analysis_prompt": "You are an expert analyst specializing in [your domain]. Analyze this text through focused sequential steps, examining each dimension group independently before integration.\n\nSTEP 1 - [DIMENSION_GROUP_1] ANALYSIS\nFocus ONLY on [group description] patterns (ignore other dimensions for now):\n- Look for [dimension_1] patterns: [specific linguistic examples] (Note: These are semantic concepts - look for the underlying meaning, not just these exact words)\n- Look for [dimension_2] patterns: [specific linguistic examples] (Note: These are semantic concepts - look for the underlying meaning, not just these exact words)\n- Score each dimension (0.0-1.0) with specific textual evidence\n- Assess salience for each dimension (0.0-1.0): How central is each specific dimension to the overall message?\n- State confidence for each dimension (0.0-1.0): How certain are you about each score?\nShow your analytical work and evidence before proceeding.\n\nSTEP 2 - [DIMENSION_GROUP_2] ANALYSIS\nNow focus ONLY on [group description] patterns:\n- Look for [dimension_3] patterns: [specific linguistic examples] (Note: These are semantic concepts - look for the underlying meaning, not just these exact words)\n- Look for [dimension_4] patterns: [specific linguistic examples] (Note: These are semantic concepts - look for the underlying meaning, not just these exact words)\n- Score each dimension (0.0-1.0) with specific textual evidence\n- Assess salience for each dimension (0.0-1.0): How central is each specific dimension to the overall message?\n- State confidence for each dimension (0.0-1.0): How certain are you about each score?\nShow your analytical work and evidence before proceeding.\n\n[Continue pattern for each dimension group...]\n\nFINAL STEP - INTEGRATION AND VALIDATION\nReview your step-by-step analysis:\n- Check for scoring consistency across all dimension groups\n- Validate that evidence quality meets academic standards\n- Identify any cross-dimensional patterns or relationships\n- Confirm confidence levels are appropriately calibrated\n- Calculate any derived metrics specified in the framework\n- Apply pattern classifications if defined\n\nProvide your final structured analysis following the output_contract format."
    },
    "longitudinal_analysis": {
      "description": "A variant for analyzing texts as part of a time series.",
      "analysis_prompt": "A prompt tailored to elicit time-aware analysis with sequential dimension focus."
    }
  },
  "dimension_groups": {
    "example_axis": ["dimension_a", "dimension_b"]
  },
  "static_weights": {
    "primary_dimension": 1.0,
    "secondary_dimension": 0.8
  },
  "calculation_spec": {
    "explanation": "Brief description of the calculations. Can be empty if the framework is purely descriptive.",
    "execution_order": [
      "dimension_tension",
      "composite_index"
    ],
    "formulas": {
      "dimension_tension": "min(dimension_a_score, dimension_b_score) * abs(dimension_a_salience - dimension_b_salience)",
      "composite_index": "(dimension_tension + other_metric) / 2"
    },
    "pattern_classifications": {
      "dimension_tension": {
        "Low": [0.0, 0.10],
        "Moderate": [0.11, 0.30],
        "High": [0.31, 999]
      }
    }
  },
  "reporting_metadata": {
      "bias_summary": "This framework mitigates bias by using ideologically neutral linguistic markers and..."
  },
  "reliability_rubric": {
    "cronbachs_alpha": { "excellent": [0.80, 1.0] }
  },
  "output_contract": {
    "raw_analysis_log_structure": [
      "## Dimension Group 1: Example Analysis",
      "**Dimension A Score**: [score]",
      "**Evidence**: [quotes]"
    ],
    "instructions": "Your response must be a single, human-readable text block following the specified structure."
  },
  "gasket_schema": {
    "version": "v7.3",
    "target_keys": ["dimension_a_score", "categorical_dimension"],
    "extraction_patterns": {
      "dimension_a_score": ["dimension_a.{0,20}score"],
      "categorical_dimension": ["category:.{0,20}(value1|value2)"]
    },
    "validation_rules": {
      "score_ranges": { "default": {"min": 0.0, "max": 1.0} }
    }
  }
}

### 6. Gasket Schema Requirements (v7.3)

**Core Principle**: The gasket schema enables automated data extraction and synthesis by providing a structured contract between framework analysis and system infrastructure.

#### **6.1 Proprietary Markers (REQUIRED)**
All gasket schema content MUST be wrapped in proprietary markers to ensure reliable extraction:

```markdown
<GASKET_SCHEMA_START>
{
  "version": "v7.3",
  "target_keys": [...],
  "extraction_patterns": {...},
  "validation_rules": {...}
}
<GASKET_SCHEMA_END>
```

**Benefits**:
- **Eliminates parsing ambiguity** - markers are impossible to miss
- **Maintains THIN principles** - simple extraction, LLM intelligence
- **Framework author control** - exact placement of gasket content
- **Future-proof** - easy to extend with new marker types

#### **6.2 Namespace Protection (REQUIRED)**
**Critical**: The terms "gasket_schema", "target_keys", "extraction_patterns", and "validation_rules" MUST NOT appear anywhere in the framework narrative or documentation outside the marked section.

**Prohibited in Narrative**:
- ❌ "This framework uses a gasket schema for data extraction"
- ❌ "The target_keys define what we extract"
- ❌ "Extraction patterns guide the analysis"

**Allowed in Narrative**:
- ✅ "This framework analyzes political discourse patterns"
- ✅ "Dimensions include dignity, truth, and justice"
- ✅ "Analysis follows sequential methodology"

**Namespace Protection Benefits**:
- **Prevents parser confusion** - no false positives
- **Maintains clean separation** - narrative vs. execution
- **Ensures reliable extraction** - markers are unambiguous

#### **6.3 Gasket Schema Structure (REQUIRED)**
```json
{
  "version": "v7.3",
  "extraction_method": "intelligent_extractor",
  "target_keys": [
    "dimension_a_score", "dimension_a_salience", "dimension_a_confidence",
    "dimension_b_score", "dimension_b_salience", "dimension_b_confidence"
  ],
  "extraction_patterns": {
    "dimension_a_score": ["dimension_a.{0,20}score", "dimension_a.{0,20}[0-9]\\.[0-9]"],
    "dimension_a_salience": ["dimension_a.{0,20}salience", "dimension_a.{0,20}salience.{0,20}[0-9]\\.[0-9]"],
    "dimension_a_confidence": ["dimension_a.{0,20}confidence", "dimension_a.{0,20}confidence.{0,20}[0-9]\\.[0-9]"]
  },
  "validation_rules": {
    "required_fields": ["dimension_a_score", "dimension_a_salience", "dimension_a_confidence"],
    "score_ranges": {"min": 0.0, "max": 1.0},
    "metadata_ranges": {
      "salience": {"min": 0.0, "max": 1.0},
      "confidence": {"min": 0.0, "max": 1.0}
    },
    "fallback_strategy": "use_default_values"
  }
}
```

#### **6.4 Validation Requirements**
The coherence agent validates:
- **Marker Presence**: `<GASKET_SCHEMA_START>` and `<GASKET_SCHEMA_END>` are present
- **Namespace Cleanliness**: No gasket keywords in narrative sections
- **Schema Completeness**: All required fields are present
- **Pattern Validity**: Extraction patterns are valid regex
- **Version Compliance**: Version is "v7.3" or "7.3"

**Failure Modes**:
- **Missing Markers**: Framework rejected as non-compliant
- **Namespace Violation**: Warning issued, extraction may fail
- **Schema Incomplete**: Framework rejected until fixed
```

### 4. Advanced Schema Features
- **`analysis_variants`**: Define multiple, tailored analysis prompts.
- **`dimension_groups`**: Formally declare conceptually opposed pairs of dimensions (axes).
- **`static_weights`**: Define fixed, theory-driven weights for dimensions.
- **`calculation_spec` Philosophy**: A framework can be **Prescriptive** (defining a rich `calculation_spec`) or **Descriptive** (defining a minimal or empty `calculation_spec` to embody a "raw scores only" philosophy). Both are valid.
- **`pattern_classifications`**: Define rubrics to translate a calculated metric into a qualitative category.
- **`reporting_metadata`**: Provide concise summaries from the narrative for direct inclusion in the final report.
- **`output_contract`**: Provide a template to guide the structure of the LLM's text output, improving reliability.

### 5. THIN Calculation Architecture (v7.3)

**Core Principle**: The framework's `calculation_spec` is the **single source of truth** for all mathematical operations. This eliminates LLM formula generation and ensures mathematical consistency.

#### **5.1 Execution Order (REQUIRED for dependent calculations)**
```json
"execution_order": [
  "base_metric_1",
  "base_metric_2", 
  "derived_metric_using_base_metrics"
]
```
- **Purpose**: Specifies the exact sequence for calculating dependent formulas
- **THIN Benefit**: Eliminates complex dependency resolution algorithms in infrastructure
- **Validation**: Coherence agent validates that execution_order respects formula dependencies

#### **5.2 Column Name Consistency (REQUIRED)**
All formula variables MUST match the actual DataFrame column structure:
- **Dimension scores**: Use `dimension_name_score` (e.g., `dimension_a_score`, `dimension_b_score`)
- **Salience values**: Use `dimension_name_salience` (e.g., `dimension_a_salience`, `dimension_b_salience`) 
- **Confidence values**: Use `dimension_name_confidence` (e.g., `dimension_a_confidence`, `dimension_b_confidence`)

**Example**:
```json
"formulas": {
  "dimension_tension": "min(dimension_a_score, dimension_b_score) * abs(dimension_a_salience - dimension_b_salience)"
}
```

#### **5.3 Mathematical Best Practices**
**Range-Aware Thresholds**: When creating pattern classifications, ensure thresholds are mathematically achievable:
```json
// WRONG: Impossible for 0.0-1.0 scores (max variance ≈ 0.25)
"incoherent_messaging": {"condition": "dimension_variance > 0.3"}

// CORRECT: Achievable threshold
"incoherent_messaging": {"condition": "dimension_variance >= 0.22"}
```

**Division Safety**: Protect against zero denominators using epsilon values:
```json
// WRONG: Risk of division by zero
"weighted_index": "numerator / (sum_of_weights)"

// CORRECT: Protected from zero division
"weighted_index": "numerator / (sum_of_weights + 1e-9)"
```

**Confidence Granularity Alignment**: Ensure analysis prompts and extraction schemas agree:
- Analysis prompt: `"State justice confidence (0.0-1.0) and resentment confidence (0.0-1.0)"`
- Extraction schema: `["justice_confidence", "resentment_confidence"]`

#### **5.4 Mathematical Validation**
The coherence agent validates:
- **Syntax**: All formulas are syntactically valid Python expressions
- **Dependencies**: execution_order correctly sequences dependent calculations  
- **Completeness**: All referenced variables exist in expected DataFrame columns
- **Consistency**: Column names follow v7.3 naming conventions
- **Mathematical Soundness**: Thresholds and conditions are achievable given input ranges
- **Division Safety**: Formulas avoid divide-by-zero errors (add small epsilon values when needed)

---

## Part III: Quality Assurance
### Self-Validation Checklist
- **Coherence Check**: Does the narrative justify every part of the appendix?
- **Parsimony Check**: Is the framework as simple as possible while still being effective?
- **Bias Check**: Have potential biases been thoughtfully considered and addressed in the narrative?

### Common Failure Patterns
- **The "Over-Engineered Framework" Trap**: Including too many dimensions, leading to a noisy analysis.
- **The "Unjustified Metric" Trap**: Creating formulas without theoretical justification.
- **The "Black Box Calculation" Trap**: Hiding math inside the prompt.
- **The "Impossible Threshold" Trap**: Setting pattern classification thresholds outside the mathematically possible range (e.g., variance > 0.25 for 0.0-1.0 scores).
- **The "Division by Zero" Trap**: Creating formulas that divide by variables that could be zero (use epsilon values like `+ 1e-9` in denominators).
- **The "Confidence Mismatch" Trap**: Analysis prompts requesting different confidence granularity than extraction schema expects.

---

## Conclusion
The Framework Specification v7.3 provides a complete guide to creating powerful and reliable analytical tools. By adhering to these principles, your framework becomes a robust, auditable, and scientifically sound contribution to research.
