# Individual Dignity Identity v Tribal Identity v7.1

**Version**: 7.1  
**Status**: Active  
**Major Change**: Enhanced Gasket Schema with Metadata Scores and Advanced Extraction Patterns

---

## Overview

The IDITI (Individual Dignity Identity v Tribal Identity) Framework v7.1 analyzes the fundamental tension between individual dignity and tribal identity in political discourse with enhanced metadata scoring. This specialized framework examines how texts either affirm universal human worth or prioritize group-based identity and loyalty, revealing the core moral question of whether human dignity is universal or conditional on group membership.

**Purpose**: Analyzes the dignity vs. tribalism axis in political and ethical discourse with enhanced extraction patterns and validation rules for comprehensive identity assessment.

**Innovation**: Philosophical framework examining whether human dignity is treated as universal (dignity) or conditional on group membership (tribalism).

**Applications**: Ethics analysis, identity politics assessment, democratic discourse evaluation, moral philosophy studies.

---

## Framework Dimensions

### **Universal Dignity Emphasis**

#### Dignity (0.0-1.0)
**Definition**: Affirms individual moral worth and universal rights, regardless of group identity.
**Key Markers**: "equal dignity," "inherent worth," "regardless of background," "individual character," "universal rights," "human agency," "personal dignity," "individual merit," "common humanity," "respect for all," "universal values," "cross-group solidarity," "individual autonomy," "character-based judgment"

### **Group-Based Identity Emphasis**

#### Tribalism (0.0-1.0)
**Definition**: Prioritizes group dominance, loyalty, or identity over individual agency.
**Key Markers**: "real Americans," "our people," "they don't belong," "us vs them," "group loyalty," "identity politics," "blood and soil," "true believers," "outsiders," "not one of us," "tribal unity," "group supremacy," "in-group favoritism," "group-based hierarchy," "exclusion markers"

---

## Gasket Architecture

### Raw Analysis Log Format
The analysis agent outputs a raw analysis log containing:
- Dignity and tribalism dimension scores
- Salience weights for each dimension
- Evidence quotes with confidence ratings
- Qualitative reasoning about identity formation patterns

### Intelligent Extractor Schema
```json
{
  "gasket_schema": {
    "target_keys": [
      "dignity_score",
      "tribalism_score",
      "dignity_salience",
      "tribalism_salience",
      "dignity_confidence",
      "tribalism_confidence"
    ],
    "target_dimensions": [
      "identity_axis_score",
      "dignity_tribalism_index"
    ]
  }
}
```

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "iditi_v7_1",
  "version": "v7.1",
  "display_name": "Individual Dignity Identity v Tribal Identity v7.1",
  "analysis_variants": {
    "default": {
      "description": "Complete analysis of the dignity vs. tribalism axis with raw analysis log output.",
      "analysis_prompt": "Phase 1: Cognitive Priming: You are an expert analyst specializing in political and ethical discourse analysis across diverse contexts. Phase 2: Framework Methodology: Your task is to analyze the provided text using the IDITI (Individual Dignity Identity v Tribal Identity) Framework v7.1, which captures identity formation patterns with enhanced metadata scoring. Phase 3: Operational Definitions: Evaluate 2 dimensions: Dignity (affirming universal human worth) and Tribalism (prioritizing group identity). Each dimension receives a score (0.0-1.0), salience weight (0.0-1.0), and confidence rating (0.0-1.0). Phase 4: Scoring Protocol: For each dimension, provide ONLY: (1) score (0.0-1.0), (2) salience (0.0-1.0), (3) confidence (0.0-1.0), (4) evidence quotes with justification. Phase 5: Raw Analysis Log Requirements: Your response must be a raw analysis log containing dimensional scores, evidence, and reasoning - NO JSON structure or derived calculations. Phase 6: Output Specification: Return raw analysis log with dimensional scores only - NO calculations of identity indices or derived metrics (these will be computed by code)."
    }
  },
  "dimension_groups": {
    "identity_axis": ["dignity", "tribalism"]
  },
  "calculation_spec": {
    "identity_axis_score": "(dignity_score - tribalism_score + 1) / 2",
    "dignity_tribalism_index": "(dignity_score + tribalism_score) / 2"
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
  "gasket_schema": {
    "version": "7.1",
    "extraction_method": "intelligent_extractor",
    "target_keys": [
      "dignity_score",
      "tribalism_score",
      "dignity_salience",
      "tribalism_salience",
      "dignity_confidence",
      "tribalism_confidence"
    ],
    "extraction_patterns": {
      "dignity_score": ["dignity.{0,20}score"],
      "tribalism_score": ["tribalism.{0,20}score"],
      "dignity_salience": ["dignity.{0,20}salience"],
      "tribalism_salience": ["tribalism.{0,20}salience"],
      "dignity_confidence": ["dignity.{0,20}confidence"],
      "tribalism_confidence": ["tribalism.{0,20}confidence"]
    },
    "validation_rules": {
      "required_fields": [
        "dignity_score", "tribalism_score"
      ],
      "score_ranges": {"min": 0.0, "max": 1.0},
      "metadata_ranges": {
        "salience": {"min": 0.0, "max": 1.0},
        "confidence": {"min": 0.0, "max": 1.0}
      },
      "fallback_strategy": "use_default_values"
    }
  },
  "raw_analysis_log_format": {
    "description": "Raw analysis log containing dignity vs tribalism scores, evidence, and reasoning without structured JSON",
    "content": "Free-form text with identity analysis including scores, evidence quotes, and qualitative reasoning"
  }
}
```

</details>