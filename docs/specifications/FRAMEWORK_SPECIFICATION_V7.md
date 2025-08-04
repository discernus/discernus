# Framework Specification (v7.1)

**Version**: 7.1  
**Status**: Active  
**Major Change**: Enhanced Gasket Schema with Advanced Extraction Patterns and Metadata Scores

**⚠️ BREAKING CHANGE: No Backward Compatibility**

Version 7.1 does NOT support v5.0/v6.0/v7.0 frameworks. All frameworks must use the v7.1 enhanced gasket schema. This is a clean architectural break to establish a single, advanced standard.

A Discernus framework is a self-contained markdown file that embodies the core principles of computational social science research. It serves as both human-readable methodology and machine-executable instructions, ensuring perfect coherence between theory and practice.

**🚀 V7.1 ENHANCED GASKET ARCHITECTURE**

Version 7.1 builds upon the Raw Analysis Log paradigm with advanced extraction capabilities:
- **Advanced Extraction Patterns**: Regex-based pattern matching with multiple fallback strategies
- **Metadata Scores**: Salience and confidence scores for academic-grade provenance
- **Framework-Specific Validation**: Customizable validation rules and error handling
- **Native v7.1 Processing**: No backward compatibility conversions or legacy format support

---

## Terminology Glossary

To ensure consistency across all frameworks, these terms have specific meanings:

**Framework**: The complete analytical system including theory, methodology, and implementation.
**Dimension**: Individual measurable element that receives a 0.0-1.0 score (e.g., Fear, Hope).
**Analysis Variant**: Different analytical approaches within the same framework (e.g., a "default" full version vs. a "descriptive_only" simplified version).
**Raw Analysis Log**: Single, human-readable text block containing scores, evidence, and reasoning from the Analysis Agent with embedded metadata scores.
**🆕 Enhanced Gasket Schema**: Advanced configuration with extraction patterns, validation rules, and metadata requirements for the Intelligent Extractor.
**🆕 Extraction Patterns**: Regex patterns that enable flexible, robust extraction of scores and metadata from Raw Analysis Logs.
**🆕 Metadata Scores**: Salience (0.0-1.0) and confidence (0.0-1.0) scores that provide additional analytical context.
**Intelligent Extractor**: Native v7.1 component that uses advanced pattern matching to extract structured data from Raw Analysis Logs.

---

## Framework Size and Performance Guidelines

### Character Limit Policy

**Maximum Framework Size**: 30,000 characters (30KB)

**Rationale**: Framework quality and comprehensiveness are prioritized over size constraints. Modern LLM context windows and negligible token costs make the previous 15KB limit an unnecessary constraint on analytical sophistication. The v7.0 gasket architecture dramatically simplifies Analysis Agent requirements while eliminating parsing brittleness.

**Validation**: The system enforces this limit during experiment ingest.

### Evidence Optimization Notice

**System Behavior**: The analysis agent is optimized for synthesis efficiency and will automatically limit evidence to the strongest 1-2 quotes per dimension.

**Framework Authors**: Design your evidence requirements around **quality over quantity**.

---

## Part I: Core Principles

1.  **The THIN Philosophy**: LLMs do intelligence, software does infrastructure. Your framework contains the domain-specific intelligence; the gasket architecture handles the interfaces.
2.  **Documentation-Execution Coherence**: What you promise in the documentation must exactly match what you deliver in the executable prompt.
3.  **Human Expert Simulation**: Write prompts like you're briefing a brilliant colleague, not like you're programming a data entry system.
4.  **Epistemic Integrity**: Every analytical decision must be traceable. Scores without evidence are meaningless.
5.  **Synthesis Efficiency**: Balance analytical rigor with synthesis efficiency. Focus on the strongest evidence.
6.  **🆕 Raw Analysis Log Paradigm**: Analysis Agents produce natural, human-readable analysis logs instead of complex structured data. This liberates intellectual analysis from formatting constraints.
7.  **Mathematical Separation**: Analysis agents provide ONLY raw scores, evidence, and reasoning. All mathematical calculations are performed by explicit, auditable code in the synthesis pipeline.
8.  **🆕 Gasket Architecture**: Three gaskets handle all interface complexity - Human-to-Pipeline validation, LLM-to-Math extraction, and Pipeline-to-Human delivery.
9.  **🆕 Parallel Stream Processing**: Raw Analysis Logs feed both quantitative (scores) and qualitative (evidence) processing streams independently and efficiently.

---

## Part II: Technical Implementation

### 1. File Structure

A framework file is a standard Markdown (`.md`) file containing:
1.  **The Narrative**: The human-readable explanation of the framework's theory, methodology, and quality standards.
2.  **The Appendix**: A single, collapsible appendix (`<details>...<\/details>`) containing a single JSON code block. This is the **single source of truth for execution** and includes the gasket_schema for Intelligent Extractor configuration.

### 2. The JSON Appendix: The Single Source of Truth

#### Required JSON Schema (v7.1)

```json
{
  "name": "unique_framework_name",
  "version": "v7.1",
  "display_name": "Human-Readable Framework Name",
  "analysis_variants": {
    "default": {
      "description": "Complete implementation of the framework methodology.",
      "analysis_prompt": "Your complete prompt implementing all methodology, focusing on natural human-readable analysis."
    },
    "descriptive_only": {
      "description": "A simplified version focusing on descriptive elements.",
      "analysis_prompt": "A simplified prompt producing natural analysis with core dimensions."
    }
  },
  "dimension_groups": {
    "identity_axis": ["dignity", "tribalism"],
    "emotional_climate_axis": ["fear", "hope"],
    "virtue_cluster": ["dignity", "truth", "justice", "hope", "pragmatism"]
  },
  "gasket_schema": {
    "version": "7.1",
    "extraction_method": "intelligent_extractor",
    "target_keys": [
      "dignity_score",
      "tribalism_score",
      "dignity_salience",
      "tribalism_salience",
      "dignity_confidence",
      "tribalism_confidence",
      "truth_score",
      "manipulation_score",
      "truth_salience",
      "manipulation_salience",
      "truth_confidence",
      "manipulation_confidence",
      "justice_score",
      "resentment_score",
      "justice_resentment_tension",
      "hope_score",
      "fear_score",
      "hope_fear_tension",
      "pragmatism_score",
      "fantasy_score",
      "pragmatism_fantasy_tension",
      "mc_sci_score"
    ],
    "extraction_patterns": {
      "dignity_score": ["dignity.{0,20}score", "dignity.{0,20}rating"],
      "tribalism_score": ["tribalism.{0,20}score", "tribalism.{0,20}rating"],
      "dignity_salience": ["dignity.{0,20}salience", "dignity.{0,20}importance"],
      "tribalism_salience": ["tribalism.{0,20}salience", "tribalism.{0,20}importance"],
      "dignity_confidence": ["dignity.{0,20}confidence", "dignity.{0,20}certainty"],
      "tribalism_confidence": ["tribalism.{0,20}confidence", "tribalism.{0,20}certainty"]
    },
    "validation_rules": {
      "required_fields": ["dignity_score", "tribalism_score"],
      "score_ranges": {"min": 0.0, "max": 1.0},
      "metadata_ranges": {
        "salience": {"min": 0.0, "max": 1.0},
        "confidence": {"min": 0.0, "max": 1.0}
      },
      "fallback_strategy": "use_default_values"
    }
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
    "format": "raw_analysis_log",
    "description": "Analysis Agent produces a single, human-readable text block containing scores, evidence, and reasoning",
    "requirements": {
      "content_sections": [
        "Framework application and methodology",
        "Dimensional analysis with scores (0.0-1.0 scale)",
        "Evidence quotes with justification",
        "Salience assessment and reasoning",
        "Overall analytical narrative"
      ],
      "scoring_format": "Natural language with clear numerical scores",
      "evidence_format": "Direct quotes with context and reasoning",
      "tone": "Expert analytical report, human-readable",
      "structure": "Coherent narrative flow, not rigid formatting"
    },
    "instructions": "Write a comprehensive analytical report in natural language. Include clear numerical scores (0.0-1.0) for each dimension with supporting evidence and reasoning. Focus on intellectual analysis rather than data formatting. The Intelligent Extractor will handle all structured data extraction."
  }
}
```

**Component Explanations**:
*   **`analysis_variants`**: Allows a framework to support multiple analysis types for greater flexibility.
*   **`dimension_groups`**: (Optional) Groups dimensions into conceptual clusters for higher-level meta-analysis.
*   **`gasket_schema`**: **REQUIRED** - Configuration for the Intelligent Extractor (Gasket #2). Maps framework dimensions to flat JSON keys for robust extraction from Raw Analysis Logs.
*   **`calculation_spec`**: (Optional) Formulas for code-based calculation. These are executed by explicit code, never by LLMs.
*   **`reliability_rubric`**: (Optional) Defines quality thresholds for automated framework fit assessments.
*   **`output_contract`**: **PARADIGM SHIFT** - Specifies Raw Analysis Log format instead of complex JSON structures. Liberates Analysis Agents from formatting constraints.
*   **`output_contract.instructions`**: Emphasizes natural language analysis over rigid data formatting.

### 3. 🆕 Gasket Schema Specification

The `gasket_schema` section is **required** in v7.0 frameworks and configures the Intelligent Extractor (Gasket #2):

#### Required Fields:

**`target_keys`**: Array of exact JSON key names that the Intelligent Extractor will use for flat data output.
- Must match the exact keys expected by downstream mathematical processing
- Should include both raw dimension scores and calculated metrics
- Example: `["dignity_score", "tribalism_score", "dignity_tribalism_tension", "mc_sci_score"]`

**`target_dimensions`**: Array of human-readable dimension names that correspond to the target_keys.
- Must be in the same order as target_keys
- Used by the Intelligent Extractor to map between human language and JSON keys
- Example: `["Dignity", "Tribalism", "Dignity-Tribalism Tension", "Moral Character Strategic Contradiction Index"]`

#### Gasket Schema Design Principles:

1. **Framework-Agnostic**: The gasket schema should work with any framework that follows the v7.0 specification
2. **Flat Structure**: Target keys should represent a flat JSON structure, not nested objects
3. **Complete Coverage**: Include all dimensions and calculated metrics that need to be extracted
4. **Clear Mapping**: Target dimensions should clearly correspond to their target keys
5. **Mathematical Integration**: Include calculated metrics that will be computed by the synthesis pipeline

### 4. Framework Prompt Guidelines

Your framework's `analysis_prompt` should focus on natural, human-readable analysis:

1. **DO Include**:
   - Your framework's methodology and theory
   - Dimension definitions and scoring criteria
   - Evidence requirements and context types
   - Clear instructions for natural language reporting
   - Emphasis on intellectual analysis and reasoning

2. **DO NOT Include**:
   - Complex JSON formatting requirements (the Intelligent Extractor handles this)
   - Data structure specifications (the gasket_schema handles this)
   - Mathematical calculations or formulas (the synthesis pipeline handles this)
   - Rigid formatting constraints (focus on analytical content)

3. **🆕 Raw Analysis Log Focus**:
   - Write prompts for human-readable analytical reports
   - Emphasize clear numerical scores within natural text
   - Request evidence quotes with contextual reasoning
   - Focus on analytical narrative over data formatting

Remember: Your framework owns the domain-specific intelligence; the gasket architecture handles all interface complexity.

### 5. Critical Separation of Concerns (v7.0)

**Analysis Agent Responsibilities (LLM):**
- Intellectual analysis using framework methodology
- Dimensional scoring (0.0-1.0 values) within natural narrative
- Evidence extraction with contextual reasoning
- Salience assessment with justification
- **🆕 Raw Analysis Log generation** (single, human-readable analytical report)
- **🆕 Liberation from formatting constraints** (focus purely on analysis)

**Intelligent Extractor Responsibilities (Gasket #2):**
- Extract numerical scores from Raw Analysis Log text
- Map framework dimensions to flat JSON structure using gasket_schema
- Handle semantic variations and natural language context
- Provide robust extraction without brittle parsing
- **🆕 Read like a human, extract like a machine**

**Mathematical Processing Responsibilities (Code):**
- ALL mathematical calculations and formulas from calculation_spec
- Statistical computations and derived metrics
- Correlation analysis and reliability measures
- Any computational processing of extracted scores

**PARADIGM SHIFT**: Analysis Agents are liberated from data formatting and focus entirely on intellectual analysis. The Intelligent Extractor handles all LLM-to-Math interface complexity.

### 6. 🆕 Raw Analysis Log Prompt Structure

**Phase 1: Cognitive Priming**: `You are an expert [domain] analyst conducting rigorous academic research...`
**Phase 2: Framework Methodology**: `Your task is to analyze the text using [framework name] methodology...`
**Phase 3: Operational Definitions**: `The framework evaluates [number] dimensions: - [Dimension 1]: [Clear definition]...`
**Phase 4: Analysis Instructions**: `For each dimension, provide: (1) clear numerical score (0.0-1.0), (2) supporting evidence quotes, (3) analytical reasoning, (4) salience assessment...`
**Phase 5: Reporting Format**: `Write a comprehensive analytical report in natural language. Include all scores and evidence within a coherent narrative...`
**Phase 6: Output Specification**: `Focus on intellectual analysis rather than data formatting. The system will extract structured data from your natural language report...`

---

## Part III: Quality Assurance

### Self-Validation Checklist
- **Coherence Check**: Does the prompt implement all documented methodology?
- **Intelligence Check**: Is the prompt a natural language briefing for an expert analyst?
- **Completeness Check**: Does the output include all analytical content needed for extraction and synthesis?
- **Role Separation Check**: Does your prompt focus on intellectual analysis rather than data formatting?
- **🆕 Raw Analysis Log Check**: Does your prompt emphasize natural language reporting over rigid structures?
- **Mathematical Separation Check**: Does your prompt explicitly state that mathematical calculations are handled by code, not the LLM?
- **Calculation Spec Check**: Are all mathematical formulas properly defined in `calculation_spec` for code execution?
- **🆕 Gasket Schema Check**: Does your framework include a complete `gasket_schema` with target_keys and target_dimensions for the Intelligent Extractor?
- **🆕 Liberation Check**: Does your framework liberate the Analysis Agent from formatting constraints to focus on intellectual work?

---

## Part IV: Migration from v6.0

### Key Changes from v6.0

1. **🚨 PARADIGM SHIFT**: Raw Analysis Log replaces complex JSON output requirements
2. **Added Gasket Schema**: New `gasket_schema` section required for Intelligent Extractor integration
3. **Liberated Analysis Agents**: Removed rigid formatting constraints, focus on intellectual analysis
4. **Enhanced Reliability**: Gasket architecture eliminates Data Sparsity warnings and parsing failures
5. **Simplified Prompts**: Analysis prompts focus on natural language reporting, not data structures

### Migration Guide

To convert a v6.0 framework to v7.0:

1. **Add gasket_schema section** with target_keys and target_dimensions covering all dimensions and calculated metrics
2. **Update output_contract** to specify "raw_analysis_log" format instead of complex JSON structures
3. **Simplify analysis_prompt** to focus on natural language analytical reporting
4. **Update version** to "v7.0"
5. **Remove JSON formatting requirements** from prompt instructions
6. **Test with framework validator** to ensure v7.0 compliance

### Backward Compatibility

- **v6.0 frameworks**: Will continue to work during transition period but will show warnings
- **v7.0 frameworks**: Require gasket_schema and Raw Analysis Log format
- **Migration path**: Gradual transition supported with validation warnings for guidance
- **Benefits**: Immediate elimination of parsing failures and improved analytical focus

---

## Part V: Meta-Prompt Usage

Researchers can paste this specification into an LLM and provide their research goals to bootstrap a compliant v7.0 framework file.

**Example**: `I need to create a Discernus framework for analyzing political speeches... Please help me create a v7.0 framework file that follows this specification, ensuring it contains a valid JSON appendix with gasket_schema and structured data requirements...`

---

## Part VI: Conclusion

The Framework Specification v7.0 represents a fundamental paradigm shift from complex JSON formatting to natural, human-readable Raw Analysis Logs. By liberating Analysis Agents from formatting constraints and introducing the Intelligent Extractor (Gasket #2), we eliminate Data Sparsity warnings and brittle parsing failures while dramatically improving analytical focus and reliability.

Your v7.0 framework is not just a configuration file; it's a contribution to the next generation of computational social science infrastructure that prioritizes intellectual analysis over data formatting, scientific rigor over technical complexity.

**The Paradigm Shift**: Analysis Agents think and communicate like human experts. The Intelligent Extractor reads like a human and extracts like a machine. Mathematical processing is handled by explicit, auditable code. This separation of concerns creates a more reliable, maintainable, and intellectually honest research platform.

**Remember**: v7.0 frameworks liberate human intelligence from machine constraints. The gasket architecture handles all interface complexity, allowing researchers and Analysis Agents to focus on what matters most - rigorous, insightful analysis. 