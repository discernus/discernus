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
      "analysis_prompt": "You are an expert analyst specializing in political and ethical discourse analysis across diverse contexts. Your task is to analyze the provided text using the IDITI (Individual Dignity Identity v Tribal Identity) Framework v7.1, which captures identity formation patterns with enhanced metadata scoring and examines the fundamental tension between individual dignity and tribal identity.\n\nThe framework evaluates discourse across two key dimensions:\n\n**Dignity** (0.0-1.0): Affirms individual moral worth and universal rights, regardless of group identity, with markers like 'equal dignity,' 'inherent worth,' 'regardless of background,' 'individual character,' 'universal rights,' 'human agency,' 'personal dignity,' 'common humanity,' 'universal values,' 'cross-group solidarity.'\n\n**Tribalism** (0.0-1.0): Prioritizes group dominance, loyalty, or identity over individual agency, with markers like 'real Americans,' 'our people,' 'they don't belong,' 'us vs them,' 'group loyalty,' 'identity politics,' 'true believers,' 'outsiders,' 'not one of us,' 'tribal unity,' 'group supremacy,' 'in-group favoritism.'\n\nFor each dimension, provide:\n- **Score (0.0-1.0)**: Based on strength of evidence in the text\n- **Salience (0.0-1.0)**: How central is this dimension to this specific text?\n- **Confidence (0.0-1.0)**: How certain are you in this assessment?\n\nWrite a comprehensive analytical report that covers:\n- Application of the IDITI methodology to this specific text\n- Detailed analysis of each dimension with scores, salience, confidence, and evidence\n- Assessment of identity formation patterns and the dignity vs. tribalism tension\n- Overall identity profile revealing whether human dignity is treated as universal or conditional on group membership\n- Key insights about the speaker's approach to human worth and group identity\n\nEmbed your numerical assessments naturally within the analysis. For example: 'This text demonstrates strong dignity emphasis (dignity score: 0.8, salience: 0.9, confidence: 0.7) with frequent appeals to universal human worth.' Focus on rigorous intellectual analysis supported by direct textual evidence and clear reasoning for all scores and metadata."
    }
  },
  "dimension_groups": {
    "identity_axis": ["dignity", "tribalism"]
  },
  "calculation_spec": {
    "identity_axis_score": "(dignity_score - tribalism_score + 1) / 2",
    "dignity_tribalism_index": "(dignity_score + tribalism_score) / 2",
    "salience_weighted_identity_axis_score": "((dignity_score * dignity_salience) - (tribalism_score * tribalism_salience) + (dignity_salience + tribalism_salience) / 2) / (dignity_salience + tribalism_salience)",
    "salience_weighted_dignity_tribalism_index": "(dignity_score * dignity_salience + tribalism_score * tribalism_salience) / (dignity_salience + tribalism_salience)"
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
      "dignity_score": ["dignity.{0,20}score", "dignity.{0,20}rating", "dignity\\s*:\\s*[0-9]"],
      "tribalism_score": ["tribalism.{0,20}score", "tribalism.{0,20}rating", "tribalism\\s*:\\s*[0-9]"],
      "dignity_salience": ["dignity.{0,20}salience", "dignity.{0,20}importance", "dignity.{0,20}centrality"],
      "tribalism_salience": ["tribalism.{0,20}salience", "tribalism.{0,20}importance", "tribalism.{0,20}centrality"],
      "dignity_confidence": ["dignity.{0,20}confidence", "dignity.{0,20}certainty", "dignity.{0,20}sure"],
      "tribalism_confidence": ["tribalism.{0,20}confidence", "tribalism.{0,20}certainty", "tribalism.{0,20}sure"]
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
  }
}
```

</details>