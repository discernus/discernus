# Political Discourse Two-Axis Analysis v7.1

**Version**: 7.1  
**Status**: Active  
**Major Change**: Enhanced Gasket Schema with Metadata Scores and Advanced Extraction Patterns

---

## Overview

The Political Discourse Two-Axis Analysis v7.1 represents a revolutionary framework that resolves fundamental conceptual overlap problems in traditional competitive political models. This enhanced version uses orthogonal axes to capture core tensions in democratic political discourse without crowding-out effects, now with advanced metadata scoring for robust analysis.

**Purpose**: Analyzes political discourse using two independent orthogonal dimensions with enhanced extraction patterns and validation rules for comprehensive political positioning assessment.

**Innovation**: Two-axis orthogonal architecture eliminates the "Bolsonaro Problem" where traditional frameworks failed to accurately capture high populism and high nationalism simultaneously.

**Applications**: Political positioning analysis, democratic discourse assessment, comparative political communication studies, electoral strategy analysis.

---

## Framework Dimensions

### **Vertical Axis: Populism ↔ Pluralism**

#### Populism (0.0-1.0)
**Definition**: Direct popular sovereignty, anti-elite sentiment, Manichaean worldview.
**Key Markers**: "the people," "corrupt elite," "establishment," "will of the people," "us versus them," "drain the swamp," "real Americans/citizens," "ordinary people"

#### Pluralism (0.0-1.0)
**Definition**: Institutional mediation, diverse representation, expert knowledge.
**Key Markers**: "institutions," "experts," "diverse perspectives," "democratic process," "checks and balances," "constitutional principles," "stakeholder input," "evidence-based"

### **Horizontal Axis: Nationalism ↔ Patriotism**

#### Nationalism (0.0-1.0)
**Definition**: Ethnic/cultural identity emphasis, national supremacy claims.
**Key Markers**: "our people," "national greatness," "cultural heritage," "traditional values," "foreign influence," "national identity," "cultural purity," "ancestral homeland"

#### Patriotism (0.0-1.0)
**Definition**: Civic attachment to political institutions and constitutional values.
**Key Markers**: "constitution," "democratic values," "rule of law," "civic duty," "constitutional rights," "democratic institutions," "equal justice," "civic participation"

---

## Gasket Architecture

### Raw Analysis Log Format
The analysis agent outputs a raw analysis log containing:
- Vertical axis (populism-pluralism) and horizontal axis (nationalism-patriotism) scores
- Salience weights for each axis
- Evidence quotes with confidence ratings
- Quadrant classification based on axis intersection
- Qualitative reasoning about political positioning patterns

### Intelligent Extractor Schema
```json
{
  "gasket_schema": {
    "target_keys": [
      "vertical_axis_score",
      "horizontal_axis_score",
      "populism_score",
      "pluralism_score", 
      "nationalism_score",
      "patriotism_score",
      "vertical_axis_salience",
      "horizontal_axis_salience",
      "populism_salience",
      "pluralism_salience",
      "nationalism_salience", 
      "patriotism_salience",
      "vertical_axis_confidence",
      "horizontal_axis_confidence",
      "populism_confidence",
      "pluralism_confidence",
      "nationalism_confidence",
      "patriotism_confidence"
    ],
    "target_dimensions": [
      "political_discourse_index",
      "quadrant_classification"
    ]
  }
}
```

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "political_discourse_two_axis_v7_1",
  "version": "v7.1",
  "display_name": "Political Discourse Two-Axis Analysis v7.1",
  "analysis_variants": {
    "default": {
      "description": "Complete two-axis political discourse analysis with raw analysis log output.",
      "analysis_prompt": "Phase 1: Cognitive Priming: You are an expert analyst specializing in political discourse analysis and democratic communication patterns across diverse contexts. Phase 2: Framework Methodology: Your task is to analyze the provided text using the Political Discourse Two-Axis Analysis v7.1, which captures political positioning through orthogonal axes with enhanced metadata scoring. Phase 3: Operational Definitions: Evaluate two orthogonal axes: Vertical Axis (Populism vs Pluralism) and Horizontal Axis (Nationalism vs Patriotism). Each axis and component receives a score (0.0-1.0), salience weight (0.0-1.0), and confidence rating (0.0-1.0). Phase 4: Scoring Protocol: For each axis and component, provide ONLY: (1) score (0.0-1.0), (2) salience (0.0-1.0), (3) confidence (0.0-1.0), (4) evidence quotes with justification. Determine quadrant classification based on axis intersection. Phase 5: Raw Analysis Log Requirements: Your response must be a raw analysis log containing axis scores, evidence, and reasoning - NO JSON structure or derived calculations. Phase 6: Output Specification: Return raw analysis log with axis scores only - NO calculations of political indices or derived metrics (these will be computed by code)."
    }
  },
  "dimension_groups": {
    "vertical_axis": ["populism", "pluralism"],
    "horizontal_axis": ["nationalism", "patriotism"]
  },
  "calculation_spec": {
    "vertical_axis_score": "(populism_score - pluralism_score + 1) / 2",
    "horizontal_axis_score": "(nationalism_score - patriotism_score + 1) / 2",
    "political_discourse_index": "sqrt(vertical_axis_score^2 + horizontal_axis_score^2) / sqrt(2)"
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
      "vertical_axis_score",
      "horizontal_axis_score",
      "populism_score",
      "pluralism_score",
      "nationalism_score",
      "patriotism_score",
      "vertical_axis_salience",
      "horizontal_axis_salience",
      "populism_salience",
      "pluralism_salience",
      "nationalism_salience",
      "patriotism_salience",
      "vertical_axis_confidence",
      "horizontal_axis_confidence",
      "populism_confidence",
      "pluralism_confidence",
      "nationalism_confidence",
      "patriotism_confidence"
    ],
    "extraction_patterns": {
      "vertical_axis_score": ["vertical.{0,20}axis.{0,20}score", "populism.{0,20}pluralism.{0,20}score"],
      "horizontal_axis_score": ["horizontal.{0,20}axis.{0,20}score", "nationalism.{0,20}patriotism.{0,20}score"],
      "populism_score": ["populism.{0,20}score"],
      "pluralism_score": ["pluralism.{0,20}score"],
      "nationalism_score": ["nationalism.{0,20}score"],
      "patriotism_score": ["patriotism.{0,20}score"],
      "vertical_axis_salience": ["vertical.{0,20}axis.{0,20}salience", "populism.{0,20}pluralism.{0,20}salience"],
      "horizontal_axis_salience": ["horizontal.{0,20}axis.{0,20}salience", "nationalism.{0,20}patriotism.{0,20}salience"],
      "populism_salience": ["populism.{0,20}salience"],
      "pluralism_salience": ["pluralism.{0,20}salience"],
      "nationalism_salience": ["nationalism.{0,20}salience"],
      "patriotism_salience": ["patriotism.{0,20}salience"],
      "vertical_axis_confidence": ["vertical.{0,20}axis.{0,20}confidence", "populism.{0,20}pluralism.{0,20}confidence"],
      "horizontal_axis_confidence": ["horizontal.{0,20}axis.{0,20}confidence", "nationalism.{0,20}patriotism.{0,20}confidence"],
      "populism_confidence": ["populism.{0,20}confidence"],
      "pluralism_confidence": ["pluralism.{0,20}confidence"],
      "nationalism_confidence": ["nationalism.{0,20}confidence"],
      "patriotism_confidence": ["patriotism.{0,20}confidence"]
    },
    "validation_rules": {
      "required_fields": [
        "vertical_axis_score", "horizontal_axis_score", "populism_score", "pluralism_score", "nationalism_score", "patriotism_score"
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
    "description": "Raw analysis log containing political discourse axis scores, evidence, and reasoning without structured JSON",
    "content": "Free-form text with political positioning analysis including axis scores, evidence quotes, and qualitative reasoning"
  }
}
```

</details>