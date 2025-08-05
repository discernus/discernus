# Framework Specification (v7.2)

**Version**: 7.2  
**Status**: Active - Current Standard

A Discernus framework is a self-contained markdown file that serves as the core intellectual asset for rigorous, repeatable text analysis. It represents the primary **analytical lens** through which all analysis and synthesis is performed in an experiment. As such, it must be carefully crafted to provide the intended insights, while also being scoped to a focused set of related concepts.

The framework's core innovation is its unique combination of a human-readable scholarly narrative with machine-executable instructions. This creates a direct, auditable link between research methodology and its computational implementation. This specification details the principles and technical requirements for building these powerful, research-grade analytical tools.

---

## Part I: Core Principles
1.  **The THIN Philosophy**: LLMs do intelligence, software does infrastructure.
2.  **Documentation-Execution Coherence**: What you promise in the narrative must match what you deliver in the appendix.
3.  **Human Expert Simulation**: Write prompts like you're briefing a brilliant colleague.
4.  **Chain-of-Thought Analysis**: Break down complex analysis into sequential, focused steps.
5.  **Epistemic Integrity**: Every analytical decision must be traceable and auditable.
6.  **Cognitive Task Separation**: Analysis (LLM) and calculation (code) must be separate.
7.  **Theoretically Grounded Measurement**: All metrics and weighting schemes must be justified by theory.
8.  **The Principle of Parsimony**: Strive for the simplest effective model.

---

## Part II: Framework Authoring Guide

### 1. File Structure: The "Narrative + Appendix" Architecture
A framework file MUST contain two sections that separate the "what and why" from the "how":
1.  **The Narrative (The "What" and "Why")**: The main body of the file, explaining the framework's theory, methodology, and objectives.
2.  **The Appendix (The "How")**: A single, collapsible appendix containing a single JSON object—the **single source of truth for execution**.

### 2. The Narrative: The Story of Your Framework
Your narrative must explain the "what" and "why" of your framework. It should contain:
- **Raison d'Être**: The research gap the framework fills.
- **Research Foundations**: The academic theories it is built upon, with citations.
- **Framework Dimensions and Axes**: Definitions for each dimension. If dimensions form a bipolar pair (e.g., Hope vs. Fear), define this "axis" and its theoretical basis.
- **Linguistic Markers**: Illustrative linguistic patterns for each dimension.
- **Analysis Methodology**: Your chain-of-thought process, scoring logic, and chosen **weighting scheme** (e.g., salience), with theoretical justification.
- **Calculated Metrics**: The theory and formulas for any derived values.
- **Reliability and Validity**: The theoretical basis for the framework's reliability.

### 3. The Appendix: The Single Source of Truth
The appendix MUST begin with `<details><summary>Machine-Readable Configuration</summary>` and end with `</details>`. It MUST contain a single JSON code block.

#### **JSON Schema (v7.2)**
```json
{
  "name": "unique_framework_name",
  "version": "v7.2",
  "display_name": "Human-Readable Framework Name",
  "analysis_variants": {
    "default": {
      "description": "The primary analysis method for this framework.",
      "analysis_prompt": "The multi-step prompt that implements the default methodology."
    },
    "longitudinal_analysis": {
      "description": "A variant for analyzing texts as part of a time series.",
      "analysis_prompt": "A prompt tailored to elicit time-aware analysis from the LLM."
    }
  },
  "dimension_groups": {
    "identity_axis": ["tribal_dominance", "individual_dignity"]
  },
  "calculation_spec": {
    "explanation": "Brief description of the calculations.",
    "formulas": {
      "identity_tension": "min(tribal_dominance_score, individual_dignity_score) * abs(tribal_dominance_salience - individual_dignity_salience)"
    }
  },
  "reliability_rubric": {
    "cronbachs_alpha": { "excellent": [0.80, 1.0] }
  },
  "gasket_schema": {
    "version": "v7.2",
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

### 4. Advanced Feature: Specialized Analysis Variants
The `analysis_variants` object is a powerful feature for creating multiple, specialized analytical modes within a single framework.
- **Purpose**: To tailor the analysis to different research questions (e.g., static vs. temporal, descriptive vs. causal) without duplicating the entire framework.
- **Implementation**:
  - The `default` variant is required.
  - Additional variants (e.g., `longitudinal_analysis`, `comparative_analysis`) can be defined with their own descriptions and tailored prompts.
  - Prompts for specialized variants should instruct the LLM to adopt a specific focus (e.g., "Pay attention to historical context and shifts over time").
- **Activation**: A specific variant is chosen in the `experiment.md` file using the `analysis.variant` field. This provides a clear link between the research question (in the experiment) and the analytical method (in the framework).

---

## Part III: Quality Assurance
### Self-Validation Checklist
- **Coherence Check**: Does the narrative justify every part of the appendix?
- **Intelligence Check**: Does the prompt feel like an expert briefing?
- **Chain-of-Thought Check**: Is the analysis broken into logical steps?
- **Parsimony Check**: Is the framework as simple as possible while still being effective?

### Common Failure Patterns
- **The "Monolithic Prompt" Trap**: Asking for everything at once.
- **The "Black Box Calculation" Trap**: Hiding math inside the prompt.
- **The "Unjustified Metric" Trap**: Creating formulas without theoretical justification.
- **The "Over-Engineered Framework" Trap**: Including too many dimensions, leading to a noisy analysis.

---

## Conclusion
The Framework Specification v7.2 provides a complete guide to creating powerful and reliable analytical tools. By adhering to these principles, your framework becomes a robust, auditable, and scientifically sound contribution to research.
