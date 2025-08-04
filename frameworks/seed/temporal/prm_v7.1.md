# Populist Rhetoric Module (PRM) v7.1

**Version**: 7.1  
**Status**: Active  
**Major Change**: Enhanced Gasket Schema with Metadata Scores and Advanced Extraction Patterns

---

## Overview

The Populist Rhetoric Module (PRM) v7.1 represents a temporal module capturing era-specific populist phenomena (2010s-2020s) with enhanced metadata analysis. This framework analyzes contemporary populist political communication patterns through salience-weighted strategic emphasis assessment, revealing which populist appeals speakers prioritize rhetorically.

**Purpose**: Analyzes contemporary populist mobilization priorities and strategic communication patterns with advanced extraction patterns and validation rules for robust analysis.

**Innovation**: Salience-weighted analysis captures not just populist appeal presence but which populist dimensions receive the most rhetorical emphasis.

**Applications**: Populist strategy analysis, contemporary political intelligence, comparative populism studies, democratic response strategy.

---

## Framework Dimensions

### **Core Populist Appeals**

#### People vs Elite Framing (0.0-1.0)
**Definition**: Politics as conflict between ordinary people and privileged elite.
**Key Markers**: "establishment," "ruling class," "real Americans," "working families," "us versus them," "drain the swamp"

#### Authentic Representation Claims (0.0-1.0)
**Definition**: Assertions about representing genuine popular will.
**Key Markers**: "real representation," "genuine voice," "authentic leadership," "straight talk," "fake representation"

#### Anti-System Mobilization (0.0-1.0)
**Definition**: Mobilization against existing political systems.
**Key Markers**: "rigged system," "broken system," "corrupt system," "political outsider," "outside the system"

### **Populist Mobilization Strategies**

#### Direct Democracy Appeals (0.0-1.0)
**Definition**: Direct popular sovereignty emphasis.
**Key Markers**: "people decide," "popular vote," "democratic mandate," "will of people," "bypass Congress"

#### Common Sense vs Expertise (0.0-1.0)
**Definition**: Popular wisdom over professional expertise.
**Key Markers**: "common sense," "practical wisdom," "out-of-touch experts," "ivory tower," "expert failure"

#### Cultural Authenticity Claims (0.0-1.0)
**Definition**: Authentic cultural values versus cosmopolitan alternatives.
**Key Markers**: "traditional values," "cultural heritage," "cultural displacement," "foreign influence"

---

## Gasket Architecture

### Raw Analysis Log Format
The analysis agent outputs a raw analysis log containing:
- Populist dimension scores for all 6 dimensions
- Salience weights for each dimension
- Evidence quotes with confidence ratings
- Qualitative reasoning about populist patterns

### Intelligent Extractor Schema
```json
{
  "gasket_schema": {
    "target_keys": [
      "people_vs_elite_framing_score",
      "authentic_representation_claims_score",
      "anti_system_mobilization_score",
      "direct_democracy_appeals_score",
      "common_sense_vs_expertise_score",
      "cultural_authenticity_claims_score",
      "people_vs_elite_framing_salience",
      "authentic_representation_claims_salience",
      "anti_system_mobilization_salience",
      "direct_democracy_appeals_salience",
      "common_sense_vs_expertise_salience",
      "cultural_authenticity_claims_salience",
      "people_vs_elite_framing_confidence",
      "authentic_representation_claims_confidence",
      "anti_system_mobilization_confidence",
      "direct_democracy_appeals_confidence",
      "common_sense_vs_expertise_confidence",
      "cultural_authenticity_claims_confidence"
    ],
    "target_dimensions": [
      "core_populist_appeal_score",
      "populist_mobilization_score",
      "populist_rhetoric_index"
    ]
  }
}
```

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "prm_v7_1",
  "version": "v7.1",
  "display_name": "Populist Rhetoric Module (PRM) v7.1",
  "analysis_variants": {
    "default": {
      "description": "Complete salience-enhanced contemporary populist assessment with raw analysis log output.",
      "analysis_prompt": "Phase 1: Cognitive Priming: You are an expert analyst specializing in contemporary populist political communication and democratic mobilization strategies across diverse contexts. Phase 2: Framework Methodology: Your task is to analyze the provided text using the Populist Rhetoric Module (PRM) v7.1, which captures era-specific populist communication patterns (2010s-2020s) with enhanced metadata scoring. Phase 3: Operational Definitions: Evaluate 6 populist dimensions: People vs Elite Framing, Authentic Representation Claims, Anti-System Mobilization, Direct Democracy Appeals, Common Sense vs Expertise, and Cultural Authenticity Claims. Each dimension receives a score (0.0-1.0), salience weight (0.0-1.0), and confidence rating (0.0-1.0). Phase 4: Scoring Protocol: For each dimension, provide ONLY: (1) score (0.0-1.0), (2) salience (0.0-1.0), (3) confidence (0.0-1.0), (4) evidence quotes with justification. Phase 5: Raw Analysis Log Requirements: Your response must be a raw analysis log containing dimensional scores, evidence, and reasoning - NO JSON structure or derived calculations. Phase 6: Output Specification: Return raw analysis log with dimensional scores only - NO calculations of populist indices or derived metrics (these will be computed by code)."
    }
  },
  "dimension_groups": {
    "core_populist_appeals": ["people_vs_elite_framing", "authentic_representation_claims", "anti_system_mobilization"],
    "populist_mobilization_strategies": ["direct_democracy_appeals", "common_sense_vs_expertise", "cultural_authenticity_claims"]
  },
  "calculation_spec": {
    "core_populist_appeal_score": "(people_vs_elite_framing_score + authentic_representation_claims_score + anti_system_mobilization_score) / 3",
    "populist_mobilization_score": "(direct_democracy_appeals_score + common_sense_vs_expertise_score + cultural_authenticity_claims_score) / 3", 
    "populist_rhetoric_index": "(core_populist_appeal_score + populist_mobilization_score) / 2"
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
      "people_vs_elite_framing_score",
      "authentic_representation_claims_score",
      "anti_system_mobilization_score",
      "direct_democracy_appeals_score",
      "common_sense_vs_expertise_score",
      "cultural_authenticity_claims_score",
      "people_vs_elite_framing_salience",
      "authentic_representation_claims_salience",
      "anti_system_mobilization_salience",
      "direct_democracy_appeals_salience",
      "common_sense_vs_expertise_salience",
      "cultural_authenticity_claims_salience",
      "people_vs_elite_framing_confidence",
      "authentic_representation_claims_confidence",
      "anti_system_mobilization_confidence",
      "direct_democracy_appeals_confidence",
      "common_sense_vs_expertise_confidence",
      "cultural_authenticity_claims_confidence"
    ],
    "extraction_patterns": {
      "people_vs_elite_framing_score": ["people.{0,20}vs.{0,20}elite.{0,20}framing.{0,20}score", "people.{0,20}elite.{0,20}score", "elite.{0,20}framing.{0,20}score"],
      "authentic_representation_claims_score": ["authentic.{0,20}representation.{0,20}claims.{0,20}score", "authentic.{0,20}representation.{0,20}score"],
      "anti_system_mobilization_score": ["anti.{0,20}system.{0,20}mobilization.{0,20}score", "anti.{0,20}system.{0,20}score"],
      "direct_democracy_appeals_score": ["direct.{0,20}democracy.{0,20}appeals.{0,20}score", "direct.{0,20}democracy.{0,20}score"],
      "common_sense_vs_expertise_score": ["common.{0,20}sense.{0,20}vs.{0,20}expertise.{0,20}score", "common.{0,20}sense.{0,20}score"],
      "cultural_authenticity_claims_score": ["cultural.{0,20}authenticity.{0,20}claims.{0,20}score", "cultural.{0,20}authenticity.{0,20}score"],
      "people_vs_elite_framing_salience": ["people.{0,20}vs.{0,20}elite.{0,20}framing.{0,20}salience", "people.{0,20}elite.{0,20}salience"],
      "authentic_representation_claims_salience": ["authentic.{0,20}representation.{0,20}claims.{0,20}salience", "authentic.{0,20}representation.{0,20}salience"],
      "anti_system_mobilization_salience": ["anti.{0,20}system.{0,20}mobilization.{0,20}salience", "anti.{0,20}system.{0,20}salience"],
      "direct_democracy_appeals_salience": ["direct.{0,20}democracy.{0,20}appeals.{0,20}salience", "direct.{0,20}democracy.{0,20}salience"],
      "common_sense_vs_expertise_salience": ["common.{0,20}sense.{0,20}vs.{0,20}expertise.{0,20}salience", "common.{0,20}sense.{0,20}salience"],
      "cultural_authenticity_claims_salience": ["cultural.{0,20}authenticity.{0,20}claims.{0,20}salience", "cultural.{0,20}authenticity.{0,20}salience"],
      "people_vs_elite_framing_confidence": ["people.{0,20}vs.{0,20}elite.{0,20}framing.{0,20}confidence", "people.{0,20}elite.{0,20}confidence"],
      "authentic_representation_claims_confidence": ["authentic.{0,20}representation.{0,20}claims.{0,20}confidence", "authentic.{0,20}representation.{0,20}confidence"],
      "anti_system_mobilization_confidence": ["anti.{0,20}system.{0,20}mobilization.{0,20}confidence", "anti.{0,20}system.{0,20}confidence"],
      "direct_democracy_appeals_confidence": ["direct.{0,20}democracy.{0,20}appeals.{0,20}confidence", "direct.{0,20}democracy.{0,20}confidence"],
      "common_sense_vs_expertise_confidence": ["common.{0,20}sense.{0,20}vs.{0,20}expertise.{0,20}confidence", "common.{0,20}sense.{0,20}confidence"],
      "cultural_authenticity_claims_confidence": ["cultural.{0,20}authenticity.{0,20}claims.{0,20}confidence", "cultural.{0,20}authenticity.{0,20}confidence"]
    },
    "validation_rules": {
      "required_fields": [
        "people_vs_elite_framing_score", "authentic_representation_claims_score", "anti_system_mobilization_score",
        "direct_democracy_appeals_score", "common_sense_vs_expertise_score", "cultural_authenticity_claims_score"
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
    "description": "Raw analysis log containing populist dimension scores, evidence, and reasoning without structured JSON",
    "content": "Free-form text with populist rhetoric analysis including scores, evidence quotes, and qualitative reasoning"
  }
}
```

</details>