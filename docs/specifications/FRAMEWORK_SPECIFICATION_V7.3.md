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
- **Linguistic Markers**: Illustrative linguistic patterns for each dimension.
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
      "analysis_prompt": "You are an expert analyst specializing in [your domain]. Analyze this text through focused sequential steps, examining each dimension group independently before integration.\n\nSTEP 1 - [DIMENSION_GROUP_1] ANALYSIS\nFocus ONLY on [group description] patterns (ignore other dimensions for now):\n- Look for [dimension_1] markers: [specific linguistic patterns]\n- Look for [dimension_2] markers: [specific linguistic patterns]\n- Score each dimension (0.0-1.0) with specific textual evidence\n- Assess salience (0.0-1.0): How central are these patterns to the overall message?\n- State confidence (0.0-1.0): How certain are you in this assessment?\nShow your analytical work and evidence before proceeding.\n\nSTEP 2 - [DIMENSION_GROUP_2] ANALYSIS\nNow focus ONLY on [group description] patterns:\n- Look for [dimension_3] markers: [specific linguistic patterns]\n- Look for [dimension_4] markers: [specific linguistic patterns]\n- Score each dimension (0.0-1.0) with specific textual evidence\n- Assess salience (0.0-1.0): How central are these patterns to the message?\n- State confidence (0.0-1.0): How certain are you in this assessment?\nShow your analytical work and evidence before proceeding.\n\n[Continue pattern for each dimension group...]\n\nFINAL STEP - INTEGRATION AND VALIDATION\nReview your step-by-step analysis:\n- Check for scoring consistency across all dimension groups\n- Validate that evidence quality meets academic standards\n- Identify any cross-dimensional patterns or relationships\n- Confirm confidence levels are appropriately calibrated\n- Calculate any derived metrics specified in the framework\n- Apply pattern classifications if defined\n\nProvide your final structured analysis following the output_contract format."
    },
    "longitudinal_analysis": {
      "description": "A variant for analyzing texts as part of a time series.",
      "analysis_prompt": "A prompt tailored to elicit time-aware analysis with sequential dimension focus."
    }
  },
  "dimension_groups": {
    "identity_axis": ["tribal_dominance", "individual_dignity"]
  },
  "static_weights": {
    "primary_dimension": 1.0,
    "secondary_dimension": 0.8
  },
  "calculation_spec": {
    "explanation": "Brief description of the calculations. Can be empty if the framework is purely descriptive.",
    "formulas": {
      "identity_tension": "min(tribal_dominance_score, individual_dignity_score) * abs(tribal_dominance_salience - individual_dignity_salience)"
    },
    "pattern_classifications": {
      "identity_tension": {
        "Harmony": [0.0, 0.10],
        "Strategic Tension": [0.11, 0.30],
        "Contradiction": [0.31, 999]
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
      "## Axis 1: Identity",
      "**Tribal Dominance Score**: [score]",
      "**Evidence**: [quotes]"
    ],
    "instructions": "Your response must be a single, human-readable text block following the specified structure."
  },
  "gasket_schema": {
    "version": "v7.3",
    "target_keys": ["dimension1_score", "categorical_dimension"],
    "extraction_patterns": {
      "dimension1_score": ["dimension1.{0,20}score"],
      "categorical_dimension": ["category:.{0,20}(value1|value2)"]
    },
    "validation_rules": {
      "score_ranges": { "default": {"min": 0.0, "max": 1.0} }
    }
  }
}
```

### 4. Advanced Schema Features
- **`analysis_variants`**: Define multiple, tailored analysis prompts.
- **`dimension_groups`**: Formally declare conceptually opposed pairs of dimensions (axes).
- **`static_weights`**: Define fixed, theory-driven weights for dimensions.
- **`calculation_spec` Philosophy**: A framework can be **Prescriptive** (defining a rich `calculation_spec`) or **Descriptive** (defining a minimal or empty `calculation_spec` to embody a "raw scores only" philosophy). Both are valid.
- **`pattern_classifications`**: Define rubrics to translate a calculated metric into a qualitative category.
- **`reporting_metadata`**: Provide concise summaries from the narrative for direct inclusion in the final report.
- **`output_contract`**: Provide a template to guide the structure of the LLM's text output, improving reliability.

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

---

## Conclusion
The Framework Specification v7.3 provides a complete guide to creating powerful and reliable analytical tools. By adhering to these principles, your framework becomes a robust, auditable, and scientifically sound contribution to research.
