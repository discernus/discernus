# Framework Specification (v7.1)

**Version**: 7.1  
**Status**: Active  
**Major Change**: Enhanced Gasket Schema with Metadata Scores and Advanced Extraction Patterns

A Discernus framework is a self-contained markdown file that embodies the core principles of computational social science research. It serves as both human-readable methodology and machine-executable instructions, ensuring perfect coherence between theory and practice.

**🚀 V7.1 ENHANCEMENT: Metadata-Rich Gasket Architecture**

Version 7.1 builds upon the v7.0 Raw Analysis Log paradigm with enhanced gasket schema capabilities:
- **Metadata Scores**: Salience and confidence scores for dimension importance and analyst certainty
- **Advanced Extraction Patterns**: Regex-based pattern matching with fallback strategies
- **Framework-Specific Validation**: Customizable validation rules and error handling
- **Enhanced Data Quality**: Comprehensive metadata for academic-grade provenance

**⚠️ BREAKING CHANGE: No Backward Compatibility**

Version 7.1 does NOT maintain backward compatibility with v5.0/v6.0/v7.0 frameworks. All frameworks must be upgraded to v7.1 specification. This is a clean architectural break to establish a single, enhanced standard.

---

## Terminology Glossary

To ensure consistency across all frameworks, these terms have specific meanings:

**Framework**: The complete analytical system including theory, methodology, and implementation.
**Dimension**: Individual measurable element that receives a 0.0-1.0 score (e.g., Fear, Hope).
**Analysis Variant**: Different analytical approaches within the same framework (e.g., a "default" full version vs. a "descriptive_only" simplified version).
**Raw Analysis Log**: Single, human-readable text block containing scores, evidence, and reasoning from the Analysis Agent.
**🆕 Metadata Scores**: Salience (0.0-1.0) and confidence (0.0-1.0) scores that provide additional context for each dimension.
**🆕 Enhanced Gasket Schema**: Advanced configuration for the Intelligent Extractor with regex patterns, validation rules, and fallback strategies.
**🆕 Extraction Patterns**: Regex patterns that enable flexible, robust extraction of scores and metadata from Raw Analysis Logs.

---

## Framework Size and Performance Guidelines

### Character Limit Policy

**Maximum Framework Size**: 30,000 characters (30KB)

**Rationale**: Framework quality and comprehensiveness are prioritized over size constraints. The v7.1 enhanced gasket architecture provides sophisticated extraction capabilities while maintaining analytical rigor.

**Validation**: The system enforces this limit during experiment ingest.

### Evidence Optimization Notice

**System Behavior**: The analysis agent is optimized for synthesis efficiency and will automatically limit evidence to the strongest 1-2 quotes per dimension.

**Framework Authors**: Design your evidence requirements around **quality over quantity**.

---

## Part I: Core Principles

1.  **The THIN Philosophy**: LLMs do intelligence, software does infrastructure. Your framework contains the domain-specific intelligence; the enhanced gasket architecture handles the interfaces.
2.  **Documentation-Execution Coherence**: What you promise in the documentation must exactly match what you deliver in the executable prompt.
3.  **Human Expert Simulation**: Write prompts like you're briefing a brilliant colleague, not like you're programming a data entry system.
4.  **Epistemic Integrity**: Every analytical decision must be traceable. Scores without evidence are meaningless.
5.  **Synthesis Efficiency**: Balance analytical rigor with synthesis efficiency. Focus on the strongest evidence.
6.  **Raw Analysis Log Paradigm**: Analysis Agents produce natural, human-readable analysis logs instead of complex structured data.
7.  **Mathematical Separation**: Analysis agents provide ONLY raw scores, evidence, and reasoning. All mathematical calculations are performed by explicit, auditable code in the synthesis pipeline.
8.  **🆕 Enhanced Gasket Architecture**: Advanced gasket schema with metadata scores, extraction patterns, and validation rules.
9.  **🆕 Metadata-Rich Analysis**: Salience and confidence scores provide academic-grade context for all dimensions.
10. **🆕 Robust Extraction**: Multiple regex patterns and fallback strategies ensure reliable data extraction across diverse analytical styles.

---

## Part II: Technical Implementation

### 1. File Structure

A framework file is a standard Markdown (`.md`) file containing:
1.  **The Narrative**: The human-readable explanation of the framework's theory, methodology, and quality standards.
2.  **The Appendix**: A single, collapsible appendix (`<details>...<\/details>`) containing a single JSON code block. This is the **single source of truth for execution** and includes the enhanced gasket_schema for Intelligent Extractor configuration.

### 2. The JSON Appendix: The Single Source of Truth

#### Required JSON Schema (v7.1)

```json
{
  "name": "unique_framework_name",
  "version": "v7.1",
  "display_name": "Human-Readable Framework Name",
  "analysis_variants": {
    "default": {
      "description": "Complete implementation of the framework methodology with metadata scores.",
      "analysis_prompt": "Your complete prompt implementing all methodology, focusing on natural human-readable analysis with salience and confidence scores."
    }
  },
  "dimension_groups": {
    "primary_axis": ["dimension1", "dimension2"],
    "secondary_cluster": ["dimension3", "dimension4", "dimension5"]
  },
  "gasket_schema": {
    "version": "7.1",
    "extraction_method": "intelligent_extractor",
    "target_keys": [
      "dimension1_score",
      "dimension2_score",
      "dimension1_salience",
      "dimension2_salience", 
      "dimension1_confidence",
      "dimension2_confidence"
    ],
    "extraction_patterns": {
      "dimension1_score": ["dimension1.{0,20}score", "dim1.{0,20}score"],
      "dimension2_score": ["dimension2.{0,20}score", "dim2.{0,20}score"],
      "dimension1_salience": ["dimension1.{0,20}salience", "dim1.{0,20}salience"],
      "dimension2_salience": ["dimension2.{0,20}salience", "dim2.{0,20}salience"],
      "dimension1_confidence": ["dimension1.{0,20}confidence", "dim1.{0,20}confidence"],
      "dimension2_confidence": ["dimension2.{0,20}confidence", "dim2.{0,20}confidence"]
    },
    "validation_rules": {
      "required_fields": ["dimension1_score", "dimension2_score"],
      "score_ranges": {"min": 0.0, "max": 1.0},
      "metadata_ranges": {"salience": {"min": 0.0, "max": 1.0}, "confidence": {"min": 0.0, "max": 1.0}},
      "fallback_strategy": "use_default_values"
    }
  }
}
```

---

## Part III: Enhanced Gasket Schema (v7.1)

### 1. Metadata Scores

**Salience Score (0.0-1.0)**: Measures the importance or relevance of a dimension within the specific text being analyzed.
- **1.0**: Central theme, extensively discussed
- **0.5**: Moderately present, some discussion
- **0.0**: Barely mentioned or absent

**Confidence Score (0.0-1.0)**: Measures the analyst's certainty in their dimensional assessment.
- **1.0**: Very confident, clear textual evidence
- **0.5**: Moderately confident, some ambiguity
- **0.0**: Low confidence, limited or unclear evidence

### 2. Advanced Extraction Patterns

**Regex Pattern Structure**: Flexible patterns that accommodate natural language variation:
```json
"extraction_patterns": {
  "dimension_score": [
    "dimension.{0,20}score",           // Primary pattern
    "dim.{0,20}score",                 // Abbreviation pattern  
    "dimension.{0,20}rating"           // Alternative terminology
  ]
}
```

**Pattern Matching Strategy**:
1. **Primary Pattern**: Most specific, preferred extraction
2. **Fallback Patterns**: Alternative patterns for robustness
3. **Flexible Spacing**: `{0,20}` allows natural language spacing

### 3. Validation Rules

**Required Fields**: Minimum dimensions that must be extracted for valid analysis.
**Score Ranges**: Numerical bounds for all extracted values.
**Metadata Ranges**: Separate validation for salience and confidence scores.
**Fallback Strategy**: Behavior when extraction fails (use defaults, retry, or error).

### 4. Framework-Specific Configuration

Each framework can customize:
- **Extraction Patterns**: Domain-specific terminology and patterns
- **Validation Rules**: Framework-appropriate requirements
- **Metadata Requirements**: Whether salience/confidence are required or optional
- **Fallback Behavior**: How to handle extraction failures

---

## Part IV: Analysis Prompt Requirements

### 1. Natural Language Analysis

**Primary Output**: Human-readable analysis with clear reasoning and evidence.
**Score Integration**: Numerical scores embedded naturally within analytical text.
**Evidence Support**: Direct quotes with clear justification for each score.

### 2. Metadata Score Requirements

**Salience Reporting**: For each dimension, report its importance in this specific text.
**Confidence Reporting**: For each dimension, report your certainty in the assessment.
**Natural Integration**: Metadata scores should flow naturally within the analysis, not as separate data points.

### 3. Example Output Structure

```
This text demonstrates strong populist rhetoric (populism score: 0.8, salience: 0.9, confidence: 0.7) 
with frequent appeals to "the people" versus "the establishment." The populist dimension is highly 
salient in this speech, appearing throughout multiple sections, though some passages are ambiguous 
in their anti-elite framing, reducing my confidence slightly.

The nationalism dimension shows moderate presence (nationalism score: 0.4, salience: 0.3, confidence: 0.8) 
with limited cultural supremacy language. While the few nationalist appeals are clear and 
unambiguous, the dimension is not central to this particular text.
```

---

## Part V: Breaking Changes from v7.0

### 1. Enhanced Gasket Schema

**New Requirements**:
- Metadata scores (salience, confidence) for all dimensions
- Advanced extraction patterns with regex support
- Framework-specific validation rules
- Fallback strategies for extraction failures

### 2. No Backward Compatibility

**Migration Required**: All v5.0/v6.0/v7.0 frameworks must be upgraded to v7.1
**Clean Break**: No support for older framework versions
**Single Standard**: All frameworks must use v7.1 enhanced gasket schema

### 3. Enhanced Data Quality

**Academic Provenance**: Metadata scores provide academic-grade context
**Robust Extraction**: Multiple patterns ensure reliable data extraction
**Quality Assurance**: Comprehensive validation prevents data quality issues

---

## Part VI: Implementation Guidelines

### 1. Framework Authors

**Design Process**:
1. Define your analytical dimensions and methodology
2. Create natural language analysis prompts
3. Design extraction patterns for your terminology
4. Configure validation rules for your domain
5. Test with diverse texts to ensure robust extraction

### 2. Extraction Pattern Design

**Best Practices**:
- Include primary and fallback patterns
- Account for natural language variation
- Test patterns with actual analysis outputs
- Use flexible spacing patterns (`{0,20}`)
- Include common abbreviations and synonyms

### 3. Validation Configuration

**Recommended Settings**:
- Require core dimensions only
- Set appropriate score ranges (typically 0.0-1.0)
- Configure metadata requirements based on analytical needs
- Choose fallback strategies that maintain data integrity

---

## Part VII: Quality Assurance

### 1. Framework Validation

All v7.1 frameworks must pass:
- **Schema Validation**: Correct JSON structure and required fields
- **Pattern Testing**: Extraction patterns work with sample outputs
- **Validation Rules**: Appropriate bounds and requirements
- **Academic Standards**: Methodology meets scholarly rigor requirements

### 2. Extraction Quality

The enhanced gasket schema ensures:
- **Reliable Extraction**: Multiple patterns prevent extraction failures
- **Metadata Richness**: Salience and confidence provide analytical context
- **Academic Provenance**: Complete traceability of all analytical decisions
- **Mathematical Integrity**: Clean separation of analysis and calculation

---

## Conclusion

Framework Specification v7.1 represents a mature, production-ready standard for computational social science research. The enhanced gasket schema provides the robustness and metadata richness required for academic-grade analysis while maintaining the THIN philosophy of letting LLMs do intelligence and software do infrastructure.

**All frameworks must upgrade to v7.1 - no backward compatibility is maintained.**