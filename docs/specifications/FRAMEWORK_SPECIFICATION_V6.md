# Framework Specification (v6.0)

**Version**: 6.0  
**Status**: Active  
**Major Change**: Return to JSON Architecture with Enhanced Synthesis Integration

A Discernus framework is a self-contained markdown file that embodies the core principles of computational social science research. It serves as both human-readable methodology and machine-executable instructions, ensuring perfect coherence between theory and practice.

**🚀 NEW IN V6.0: Enhanced JSON Output Contract**

Version 6.0 returns to the JSON-first architecture from v4.0 while retaining all scalability improvements from v5.0. This eliminates CSV parsing brittleness while maintaining synthesis efficiency through the THIN code-generated synthesis pipeline. The result is more reliable LLM output generation with the same massive-scale synthesis capabilities (3,000-8,000 documents per run).

---

## Terminology Glossary

To ensure consistency across all frameworks, these terms have specific meanings:

**Framework**: The complete analytical system including theory, methodology, and implementation.
**Dimension**: Individual measurable element that receives a 0.0-1.0 score (e.g., Fear, Hope).
**Analysis Variant**: Different analytical approaches within the same framework (e.g., a "default" full version vs. a "descriptive_only" simplified version).
**Structured JSON**: Rich JSON objects containing nested data for scores, evidence, and calculations.

---

## Framework Size and Performance Guidelines

### Character Limit Policy

**Maximum Framework Size**: 15,000 characters (15KB)

**Rationale**: Concise frameworks ensure lower operational costs, reduce LLM processing latency, and promote clear, focused instructions that improve analytical reliability. The v6.0 JSON architecture maintains synthesis efficiency without requiring verbose CSV generation instructions.

**Validation**: The system enforces this limit during experiment ingest.

### Evidence Optimization Notice

**System Behavior**: The analysis agent is optimized for synthesis efficiency and will automatically limit evidence to the strongest 1-2 quotes per dimension.

**Framework Authors**: Design your evidence requirements around **quality over quantity**.

---

## Part I: Core Principles

1.  **The THIN Philosophy**: LLMs do intelligence, software does infrastructure. Your framework contains the domain-specific intelligence; the software just routes it.
2.  **Documentation-Execution Coherence**: What you promise in the documentation must exactly match what you deliver in the executable prompt.
3.  **Human Expert Simulation**: Write prompts like you're briefing a brilliant colleague, not like you're calling a technical API.
4.  **Epistemic Integrity**: Every analytical decision must be traceable. Scores without evidence are meaningless.
5.  **Synthesis Efficiency**: Balance analytical rigor with synthesis efficiency. Focus on the strongest evidence.
6.  **🆕 JSON-First Architecture (v6.0)**: Generate rich, structured JSON that enables code-driven synthesis without CSV parsing brittleness.
7.  **🆕 Mathematical Separation (v6.0)**: Analysis agents provide ONLY raw scores and evidence. All mathematical calculations are performed by explicit, auditable code in the synthesis pipeline.

---

## Part II: Technical Implementation

### 1. File Structure

A framework file is a standard Markdown (`.md`) file containing:
1.  **The Narrative**: The human-readable explanation of the framework's theory, methodology, and quality standards.
2.  **The Appendix**: A single, collapsible appendix (`<details>...<\/details>`) containing a single JSON code block. This is the **single source of truth for execution**.

### 2. The JSON Appendix: The Single Source of Truth

#### Required JSON Schema (v6.0)

```json
{
  "name": "unique_framework_name",
  "version": "v6.0",
  "display_name": "Human-Readable Framework Name",
  "analysis_variants": {
    "default": {
      "description": "Complete implementation of the framework methodology.",
      "analysis_prompt": "Your complete prompt implementing all methodology, focusing on rich JSON generation."
    },
    "descriptive_only": {
      "description": "A simplified version focusing on descriptive elements.",
      "analysis_prompt": "A simplified prompt that still generates the required JSON structure."
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
    "structured_data_requirements": {
      "scores": {
        "description": "Nested object containing ONLY raw dimensional scores (NO calculated metrics)",
        "structure": {
          "dimensions": {
            "dimension_name": {
              "score": "number (0.0-1.0)",
              "salience": "number (0.0-1.0)",
              "confidence": "number (0.0-1.0)"
            }
          },
          "metadata": {
            "total_dimensions": "number",
            "analysis_completeness": "number (0.0-1.0)"
          }
        }
      },
      "evidence": {
        "description": "Nested object containing structured evidence data for audit and replication",
        "structure": {
          "by_dimension": {
            "dimension_name": [
              {
                "quote_id": "string",
                "quote_text": "string", 
                "confidence": "number (0.0-1.0)",
                "context_type": "string",
                "salience_justification": "string"
              }
            ]
          },
          "metadata": {
            "total_quotes": "number",
            "average_confidence": "number"
          }
        }
      }
    },
    "instructions": "IMPORTANT: Your response MUST be a single, valid JSON object containing all required fields with the nested structures specified above. The salience_ranking should be an ordered array of objects, each containing 'dimension', 'salience_score', and 'rank'. All numerical scores must be between 0.0 and 1.0. DO NOT perform any mathematical calculations or compute derived metrics - provide ONLY raw dimensional scores, salience, confidence, and evidence."
  }
}
```

**Component Explanations**:
*   **`analysis_variants`**: Allows a framework to support multiple analysis types for greater flexibility.
*   **`dimension_groups`**: (Optional) Groups dimensions into conceptual clusters for higher-level meta-analysis.
*   **`calculation_spec`**: (Optional) Formulas for code-based calculation. These are now executed by explicit code rather than LLM computation.
*   **`reliability_rubric`**: (Optional) Defines quality thresholds for automated framework fit assessments.
*   **`output_contract.structured_data_requirements`**: Defines the rich JSON structure that replaces CSV output. Enables direct code consumption without parsing brittleness.
*   **`output_contract.instructions`**: Enforces specific JSON structures for reliable parsing.

### 3. Framework Prompt Guidelines

Your framework's `analysis_prompt` should focus on domain-specific instructions:

1. **DO Include**:
   - Your framework's methodology and theory
   - Dimension definitions and scoring criteria
   - Evidence requirements and context types
   - Framework-specific calculations and metrics
   - JSON structure requirements for your specific framework

2. **DO NOT Include**:
   - Agent infrastructure details (the agent handles this)
   - Generic JSON formatting instructions (the agent handles this)
   - Document handling instructions (the agent handles this)
   - **Mathematical calculations, formulas, or computed metrics** (the synthesis pipeline's code execution handles ALL calculations)

Remember: Your framework owns the domain-specific intelligence; the agent and code own the infrastructure.

### 4. Critical Separation of Concerns (v6.0)

**Analysis Agent Responsibilities (LLM):**
- Dimensional scoring (0.0-1.0 values only)
- Salience assessment (0.0-1.0 values only)  
- Confidence rating (0.0-1.0 values only)
- Evidence extraction and reasoning
- Structured JSON output generation

**Code Generation/Execution Responsibilities:**
- ALL mathematical calculations and formulas
- Statistical computations and derived metrics
- Correlation analysis and reliability measures
- Any computational processing of the raw scores

**CRITICAL**: Analysis agents must NEVER attempt mathematical calculations. The `calculation_spec` in frameworks is for code execution only.

### 5. Six-Phase Prompt Structure

**Phase 1: Cognitive Priming**: `You are an expert [domain] analyst...`
**Phase 2: Framework Methodology**: `Your task is to analyze the text using [framework name]...`
**Phase 3: Operational Definitions**: `The framework evaluates [number] dimensions: - [Dimension 1]: [Clear definition]...`
**Phase 4: Scoring Protocol**: `For each dimension, provide ONLY: (1) score (0.0-1.0), (2) salience (0.0-1.0), (3) confidence (0.0-1.0), (4) evidence quotes...`
**Phase 5: JSON Structure Requirements**: `Your JSON output must include the nested structures specified in the output_contract...`
**Phase 6: Output Specification**: `Return a single, valid JSON object with raw scores only - NO calculations or derived metrics...`

---

## Part III: Quality Assurance

### Self-Validation Checklist
- **Coherence Check**: Does the prompt implement all documented methodology?
- **Intelligence Check**: Is the prompt a natural language briefing for an expert?
- **Completeness Check**: Does the output include all data needed for synthesis?
- **Role Separation Check**: Does your prompt focus on domain-specific instructions?
- **JSON Structure Check**: Are your framework's JSON requirements clearly defined?
- **🆕 Mathematical Separation Check**: Does your prompt explicitly forbid the LLM from performing calculations and clearly state that only raw scores should be provided?
- **🆕 Calculation Spec Check**: Are all mathematical formulas properly defined in `calculation_spec` for code execution rather than LLM computation?

---

## Part IV: Migration from v5.0

### Key Changes from v5.0

1. **Eliminated CSV Requirements**: No more embedded CSV delimiters or parsing
2. **Enhanced JSON Structure**: Rich nested objects replace flat CSV rows
3. **Mathematical Separation**: Calculations moved from LLM to explicit code
4. **Improved Reliability**: JSON generation is more natural for LLMs than CSV

### Migration Guide

To convert a v5.0 framework to v6.0:

1. **Remove CSV sections** from `output_contract.embedded_csv_requirements`
2. **Add structured_data_requirements** with equivalent JSON structures
3. **Update analysis_prompt** to remove CSV generation instructions
4. **Add JSON structure requirements** to the prompt
5. **Move calculations** from prompt to `calculation_spec` for code execution

---

## Part V: Meta-Prompt Usage

Researchers can paste this specification into an LLM and provide their research goals to bootstrap a compliant v6.0 framework file.

**Example**: `I need to create a Discernus framework for analyzing political speeches... Please help me create a v6.0 framework file that follows this specification, ensuring it contains a valid JSON appendix with structured data requirements...`

---

## Part VI: Conclusion

The Framework Specification v6.0 combines the reliability of JSON-first architecture with the scalability achievements of v5.0. By eliminating CSV parsing brittleness while maintaining massive-scale synthesis capabilities, we achieve both reliability and performance.

Your v6.0 framework is not just a configuration file; it's a contribution to the next generation of computational social science infrastructure that prioritizes both scale and scientific rigor.

**Remember**: v6.0 frameworks make reliable, massive-scale research possible. Brittle CSV parsing makes it unreliable. 