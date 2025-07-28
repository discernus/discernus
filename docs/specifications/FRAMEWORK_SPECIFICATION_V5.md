# Framework Specification (v5.0)

**Version**: 5.0  
**Status**: Active  
**Major Change**: Embedded CSV Architecture for Synthesis Scalability

A Discernus framework is a self-contained markdown file that embodies the core principles of computational social science research. It serves as both human-readable methodology and machine-executable instructions, ensuring perfect coherence between theory and practice.

**🚀 NEW IN V5.0: Embedded CSV Output Contract**

Version 5.0 introduces the **Embedded CSV Architecture** to solve synthesis scalability bottlenecks. Frameworks must now embed standardized CSV segments directly in their LLM responses using Discernus-specific delimiters, enabling processing of 3,000-8,000 documents per synthesis run (a 60-800x improvement over current academic practice).

---

## Terminology Glossary

To ensure consistency across all frameworks, these terms have specific meanings:

**Framework**: The complete analytical system including theory, methodology, and implementation.
**Dimension**: Individual measurable element that receives a 0.0-1.0 score (e.g., Fear, Hope).
**Analysis Variant**: Different analytical approaches within the same framework (e.g., a "default" full version vs. a "descriptive_only" simplified version).
**Embedded CSV**: Standardized CSV segments embedded directly in LLM responses for synthesis scalability.

---

## Framework Size and Performance Guidelines

### Character Limit Policy

**Maximum Framework Size**: 15,000 characters (15KB)

**Rationale**: While the v5.0 Embedded CSV architecture removes synthesis bottlenecks, prompt size remains a critical factor for cost, performance, and quality. A concise framework (under 15KB) ensures lower operational costs, reduces LLM processing latency, and promotes clear, focused instructions that improve analytical reliability.

**Validation**: The system enforces this limit during experiment ingest.

### Evidence Optimization Notice

**System Behavior**: The analysis agent is optimized for synthesis efficiency and will automatically limit evidence to the strongest 1-2 quotes per dimension.

**Framework Authors**: Design your evidence requirements around **quality over quantity**.

---

## Part I: Core Principles

1.  **The THIN Philosophy**: LLMs do intelligence, software does infrastructure. Your framework contains the intelligence; the software just routes it.
2.  **Documentation-Execution Coherence**: What you promise in the documentation must exactly match what you deliver in the executable prompt.
3.  **Human Expert Simulation**: Write prompts like you're briefing a brilliant colleague, not like you're calling a technical API.
4.  **Epistemic Integrity**: Every analytical decision must be traceable. Scores without evidence are meaningless.
5.  **Synthesis Efficiency**: Balance analytical rigor with synthesis efficiency. Focus on the strongest evidence.
6.  **🆕 Embedded CSV Compliance (v5.0)**: Embed standardized CSVs in all responses to enable massive-scale synthesis.

---

## Part II: Technical Implementation

### 1. File Structure

A framework file is a standard Markdown (`.md`) file containing:
1.  **The Narrative**: The human-readable explanation of the framework's theory, methodology, and quality standards.
2.  **The Appendix**: A single, collapsible appendix (`<details>...<\/details>`) containing a single JSON code block. This is the **single source of truth for execution**.

### 2. The JSON Appendix: The Single Source of Truth

#### Required JSON Schema (v5.0)

```json
{
  "name": "unique_framework_name",
  "version": "v5.0",
  "display_name": "Human-Readable Framework Name",
  "analysis_variants": {
    "default": {
      "description": "Complete implementation of the framework methodology.",
      "analysis_prompt": "Your complete prompt implementing all methodology, including CSV generation."
    },
    "descriptive_only": {
      "description": "A simplified version focusing on descriptive elements.",
      "analysis_prompt": "A simplified prompt that still generates the required CSVs."
    }
  },
  "dimension_groups": {
    "identity_axis": ["tribal_dominance", "individual_dignity"],
    "emotional_climate_axis": ["fear", "hope"],
    "virtue_cluster": ["dignity", "truth", "justice", "hope", "pragmatism"]
  },
  "calculation_spec": {
    "moral_character_sci": "(dignity_tribalism_tension + truth_manipulation_tension + justice_resentment_tension + hope_fear_tension + pragmatism_fantasy_tension) / 5",
    "salience_weighting_explanation": "All indices use salience-weighted calculations."
  },
  "reliability_rubric": {
    "cronbachs_alpha": {
      "excellent": [0.80, 1.0],
      "good": [0.70, 0.79],
      "acceptable": [0.60, 0.69],
      "poor": [0.0, 0.59]
    },
    "notes": "Defines quality thresholds for framework reliability. The Synthesis Agent uses this for automated fit assessment."
  },
  "output_contract": {
    "schema": {
      "worldview": "string",
      "scores": "object",
      "evidence": "object",
      "reasoning": "object",
      "salience_ranking": "array",
      "character_clusters": "object"
    },
    "embedded_csv_requirements": {
      "scores_csv": {
        "delimiter_start": "<<<DISCERNUS_SCORES_CSV_v1>>>",
        "delimiter_end": "<<<END_DISCERNUS_SCORES_CSV_v1>>>",
        "description": "CSV for all dimensional scores and calculated metrics."
      },
      "evidence_csv": {
        "delimiter_start": "<<<DISCERNUS_EVIDENCE_CSV_v1>>>",
        "delimiter_end": "<<<END_DISCERNUS_EVIDENCE_CSV_v1>>>",
        "description": "CSV for structured evidence data for audit and replication."
      }
    },
    "instructions": "IMPORTANT: Your response MUST include both a complete JSON analysis AND embedded CSV segments using the exact delimiters specified. The salience_ranking should be an ordered array of objects, each containing 'dimension', 'salience_score', and 'rank'."
  }
}
```

**Component Explanations**:
*   **`analysis_variants`**: Allows a framework to support multiple analysis types (e.g., a full version and a descriptive version) for greater flexibility.
*   **`dimension_groups`**: (Optional) Groups dimensions into conceptual clusters (e.g., "axes") for higher-level meta-analysis by the Synthesis Agent.
*   **`calculation_spec`**: (Optional) A dictionary of named formulas for the `CalculationAgent`. Providing clear, self-documenting names is a best practice.
*   **`reliability_rubric`**: (Optional) Defines quality thresholds for reliability metrics (e.g., Cronbach's Alpha) for automated framework fit assessments by the Synthesis Agent.
*   **`output_contract.instructions`**: A powerful THIN pattern to enforce specific JSON structures (e.g., the contents of an array of objects) without requiring complex software-side parsing.

### 3. Six-Phase Prompt Structure

**Phase 1: Cognitive Priming**: `You are an expert [domain] analyst...`
**Phase 2: Framework Methodology**: `Your task is to analyze the text using [framework name]...`
**Phase 3: Operational Definitions**: `The framework evaluates [number] dimensions: - [Dimension 1]: [Clear definition]...`
**Phase 4: Scoring Protocol**: `For each dimension, score based on [criteria] and provide [evidence]...`
**Phase 5: 🆕 Embedded CSV Generation**: `CRITICAL: Your response must include embedded CSV segments using these exact delimiters: <<<DISCERNUS_SCORES_CSV_v1>>>...`
**Phase 6: Output Specification**: `Return a complete response containing both a comprehensive JSON analysis and the embedded CSV segments...`

---

## Part III: Quality Assurance

### Self-Validation Checklist
- **Coherence Check**: Does the prompt implement all documented methodology?
- **Intelligence Check**: Is the prompt a natural language briefing for an expert?
- **Completeness Check**: Does the output include all data needed for synthesis?
- **🆕 CSV Compliance Check**: Are the exact delimiters, columns, and instructions for both CSVs present in the prompt and `output_contract`?

---

## Part IV: Meta-Prompt Usage

Researchers can paste this specification into an LLM and provide their research goals to bootstrap a compliant v5.0 framework file.

**Example**: `I need to create a Discernus framework for analyzing political speeches... Please help me create a v5.0 framework file that follows this specification, ensuring it contains a valid JSON appendix with embedded CSV requirements...`

---

## Part V: Conclusion

The Framework Specification v5.0 represents a generational leap in research capability. By embedding standardized CSV segments, we enable analysis of 3,000-8,000 documents per synthesis run—a 60-800x improvement.

Your v5.0 framework is not just a configuration file; it's a contribution to the next generation of computational social science infrastructure.

**Remember**: v5.0 frameworks make unprecedented scale research possible. Non-compliant frameworks make it impossible. 