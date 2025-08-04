# Political Worldview Triad Framework v7.1

**Version**: 7.1  
**Status**: Active  
**Major Change**: Enhanced Gasket Schema with Metadata Scores and Advanced Extraction Patterns

---

## Overview

The Political Worldview Triad Framework v7.1 identifies three competing sources of political legitimacy that shape contemporary democratic discourse with enhanced metadata scoring. This advanced framework analyzes how texts appeal to identity-based claims, dominance-seeking narratives, and universal dignity principles, revealing the underlying value structures that drive political communication.

**Purpose**: Analyzes political discourse through three competing legitimacy sources with enhanced extraction patterns and validation rules for comprehensive worldview assessment.

**Innovation**: Triadic analysis framework that captures the fundamental competing sources of political legitimacy in democratic discourse.

**Applications**: Political legitimacy analysis, democratic discourse assessment, comparative political communication studies, worldview mapping in political texts.

---

## Framework Dimensions

### **Identity-Based Legitimacy**

#### Immutable-Identity Politics (0.0-1.0)
**Definition**: Politics that centers moral status on overlapping, unchosen personal attributes.
**Key Markers**: "As Black women, we," "Center disabled queer voices," "Our lived experience as trans people," "Marginalized identities face systemic barriers," "systemic oppression," "lived experience," "intersection of race and gender"

### **Dominance-Based Legitimacy**

#### Tribal Domination (0.0-1.0)
**Definition**: Politics that asserts the legitimacy of an in-group's supremacy over out-groups.
**Key Markers**: "We must put our nation first," "They will replace us," "Only our tribe can secure the future," "Our way of life is under threat," "take back our country," "real patriots," "dominant culture"

### **Universal Dignity Legitimacy**

#### Pluralist Individual Dignity (0.0-1.0)
**Definition**: Politics that locates legitimacy in the transcendent dignity and agency of each person.
**Key Markers**: "Every individual deserves equal voice," "Citizens, regardless of background, share responsibility," "Human dignity transcends race and class," "universal rights," "shared civic space," "common good through consent"

---

## Gasket Architecture

### Raw Analysis Log Format
The analysis agent outputs a raw analysis log containing:
- Worldview dimension scores for all 3 dimensions
- Salience weights for each dimension
- Evidence quotes with confidence ratings
- Dominant worldview identification
- Qualitative reasoning about political legitimacy patterns

### Intelligent Extractor Schema
```json
{
  "gasket_schema": {
    "target_keys": [
      "immutable_identity_politics_score",
      "tribal_domination_score",
      "pluralist_individual_dignity_score",
      "immutable_identity_politics_salience",
      "tribal_domination_salience",
      "pluralist_individual_dignity_salience",
      "immutable_identity_politics_confidence",
      "tribal_domination_confidence",
      "pluralist_individual_dignity_confidence"
    ],
    "target_dimensions": [
      "worldview_legitimacy_index",
      "dominant_worldview"
    ]
  }
}
```

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "political_worldview_triad_v7_1",
  "version": "v7.1",
  "display_name": "Political Worldview Triad Framework v7.1",
  "analysis_variants": {
    "default": {
      "description": "Complete triadic worldview analysis across all three political legitimacy sources with raw analysis log output.",
      "analysis_prompt": "Phase 1: Cognitive Priming: You are an expert analyst specializing in political worldview analysis and democratic legitimacy frameworks across diverse contexts. Phase 2: Framework Methodology: Your task is to analyze the provided text using the Political Worldview Triad Framework v7.1, which captures competing sources of political legitimacy with enhanced metadata scoring. Phase 3: Operational Definitions: Evaluate 3 worldview dimensions: Immutable-Identity Politics, Tribal Domination, and Pluralist Individual Dignity. Each dimension receives a score (0.0-1.0), salience weight (0.0-1.0), and confidence rating (0.0-1.0). Phase 4: Scoring Protocol: For each dimension, provide ONLY: (1) score (0.0-1.0), (2) salience (0.0-1.0), (3) confidence (0.0-1.0), (4) evidence quotes with justification. Identify the dominant worldview (highest scoring). Phase 5: Raw Analysis Log Requirements: Your response must be a raw analysis log containing dimensional scores, evidence, and reasoning - NO JSON structure or derived calculations. Phase 6: Output Specification: Return raw analysis log with worldview scores only - NO calculations of worldview indices or derived metrics (these will be computed by code)."
    }
  },
  "dimension_groups": {
    "political_legitimacy_sources": ["immutable_identity_politics", "tribal_domination", "pluralist_individual_dignity"]
  },
  "calculation_spec": {
    "worldview_legitimacy_index": "(immutable_identity_politics_score + tribal_domination_score + pluralist_individual_dignity_score) / 3",
    "dominant_worldview": "argmax(immutable_identity_politics_score, tribal_domination_score, pluralist_individual_dignity_score)"
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
      "immutable_identity_politics_score",
      "tribal_domination_score",
      "pluralist_individual_dignity_score",
      "immutable_identity_politics_salience",
      "tribal_domination_salience",
      "pluralist_individual_dignity_salience",
      "immutable_identity_politics_confidence",
      "tribal_domination_confidence",
      "pluralist_individual_dignity_confidence"
    ],
    "extraction_patterns": {
      "immutable_identity_politics_score": ["immutable.{0,20}identity.{0,20}politics.{0,20}score", "identity.{0,20}politics.{0,20}score"],
      "tribal_domination_score": ["tribal.{0,20}domination.{0,20}score", "domination.{0,20}score"],
      "pluralist_individual_dignity_score": ["pluralist.{0,20}individual.{0,20}dignity.{0,20}score", "individual.{0,20}dignity.{0,20}score"],
      "immutable_identity_politics_salience": ["immutable.{0,20}identity.{0,20}politics.{0,20}salience", "identity.{0,20}politics.{0,20}salience"],
      "tribal_domination_salience": ["tribal.{0,20}domination.{0,20}salience", "domination.{0,20}salience"],
      "pluralist_individual_dignity_salience": ["pluralist.{0,20}individual.{0,20}dignity.{0,20}salience", "individual.{0,20}dignity.{0,20}salience"],
      "immutable_identity_politics_confidence": ["immutable.{0,20}identity.{0,20}politics.{0,20}confidence", "identity.{0,20}politics.{0,20}confidence"],
      "tribal_domination_confidence": ["tribal.{0,20}domination.{0,20}confidence", "domination.{0,20}confidence"],
      "pluralist_individual_dignity_confidence": ["pluralist.{0,20}individual.{0,20}dignity.{0,20}confidence", "individual.{0,20}dignity.{0,20}confidence"]
    },
    "validation_rules": {
      "required_fields": [
        "immutable_identity_politics_score", "tribal_domination_score", "pluralist_individual_dignity_score"
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
    "description": "Raw analysis log containing political worldview scores, evidence, and reasoning without structured JSON",
    "content": "Free-form text with worldview legitimacy analysis including scores, evidence quotes, and qualitative reasoning"
  }
}
```

</details>