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
      "analysis_prompt": "You are an expert analyst specializing in contemporary populist political communication and democratic mobilization strategies across diverse contexts. Your task is to analyze the provided text using the Populist Rhetoric Module (PRM) v7.1, which captures era-specific populist communication patterns (2010s-2020s) with enhanced metadata scoring and salience-weighted strategic emphasis assessment.\n\nThe framework evaluates contemporary populist mobilization across six dimensions:\n\n**Core Populist Appeals**:\n1. **People vs Elite Framing** (0.0-1.0): Politics as conflict between ordinary people and privileged elite\n2. **Authentic Representation Claims** (0.0-1.0): Assertions about representing genuine popular will\n3. **Anti-System Mobilization** (0.0-1.0): Mobilization against existing political systems\n\n**Populist Mobilization Strategies**:\n4. **Direct Democracy Appeals** (0.0-1.0): Direct popular sovereignty emphasis\n5. **Common Sense vs Expertise** (0.0-1.0): Popular wisdom over professional expertise\n6. **Cultural Authenticity Claims** (0.0-1.0): Authentic cultural values versus cosmopolitan alternatives\n\nFor each dimension, provide:\n- **Score (0.0-1.0)**: Based on strength of evidence in the text\n- **Salience (0.0-1.0)**: How central is this dimension to this specific text?\n- **Confidence (0.0-1.0)**: How certain are you in this assessment?\n\nWrite a comprehensive analytical report that covers:\n- Application of the PRM methodology to this specific text\n- Detailed analysis of each relevant dimension with scores, salience, confidence, and evidence\n- Assessment of contemporary populist communication patterns and strategic priorities\n- Overall populist rhetoric profile with salience weighting\n- Key insights about the speaker's populist mobilization approach\n\nEmbed your numerical assessments naturally within the analysis. For example: 'This text demonstrates strong people vs elite framing (people vs elite framing score: 0.8, salience: 0.9, confidence: 0.7) with clear establishment versus ordinary people dichotomy.' Focus on rigorous intellectual analysis supported by direct textual evidence and clear reasoning for all scores and metadata."
    }
  },
  "dimension_groups": {
    "core_populist_appeals": ["people_vs_elite_framing", "authentic_representation_claims", "anti_system_mobilization"],
    "populist_mobilization_strategies": ["direct_democracy_appeals", "common_sense_vs_expertise", "cultural_authenticity_claims"]
  },
  "calculation_spec": {
    "core_populist_appeal_score": "(people_vs_elite_framing_score + authentic_representation_claims_score + anti_system_mobilization_score) / 3",
    "populist_mobilization_score": "(direct_democracy_appeals_score + common_sense_vs_expertise_score + cultural_authenticity_claims_score) / 3", 
    "populist_rhetoric_index": "(core_populist_appeal_score + populist_mobilization_score) / 2",
    "salience_weighted_core_populist_appeal_score": "(people_vs_elite_framing_score * people_vs_elite_framing_salience + authentic_representation_claims_score * authentic_representation_claims_salience + anti_system_mobilization_score * anti_system_mobilization_salience) / (people_vs_elite_framing_salience + authentic_representation_claims_salience + anti_system_mobilization_salience + 1e-9)",
    "salience_weighted_populist_mobilization_score": "(direct_democracy_appeals_score * direct_democracy_appeals_salience + common_sense_vs_expertise_score * common_sense_vs_expertise_salience + cultural_authenticity_claims_score * cultural_authenticity_claims_salience) / (direct_democracy_appeals_salience + common_sense_vs_expertise_salience + cultural_authenticity_claims_salience + 1e-9)",
    "salience_weighted_populist_rhetoric_index": "(salience_weighted_core_populist_appeal_score * ((people_vs_elite_framing_salience + authentic_representation_claims_salience + anti_system_mobilization_salience + 1e-9) / 3) + salience_weighted_populist_mobilization_score * ((direct_democracy_appeals_salience + common_sense_vs_expertise_salience + cultural_authenticity_claims_salience + 1e-9) / 3)) / (((people_vs_elite_framing_salience + authentic_representation_claims_salience + anti_system_mobilization_salience + 1e-9) / 3) + ((direct_democracy_appeals_salience + common_sense_vs_expertise_salience + cultural_authenticity_claims_salience + 1e-9) / 3))"
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
      "people_vs_elite_framing_score": ["people.{0,20}vs.{0,20}elite.{0,20}framing.{0,20}score", "people.{0,20}elite.{0,20}rating", "elite\\s*framing\\s*:\\s*[0-9]"],
      "authentic_representation_claims_score": ["authentic.{0,20}representation.{0,20}claims.{0,20}score", "authentic.{0,20}representation.{0,20}rating", "authentic\\s*representation\\s*:\\s*[0-9]"],
      "anti_system_mobilization_score": ["anti.{0,20}system.{0,20}mobilization.{0,20}score", "anti.{0,20}system.{0,20}rating", "anti\\s*system\\s*:\\s*[0-9]"],
      "direct_democracy_appeals_score": ["direct.{0,20}democracy.{0,20}appeals.{0,20}score", "direct.{0,20}democracy.{0,20}rating", "direct\\s*democracy\\s*:\\s*[0-9]"],
      "common_sense_vs_expertise_score": ["common.{0,20}sense.{0,20}vs.{0,20}expertise.{0,20}score", "common.{0,20}sense.{0,20}rating", "common\\s*sense\\s*:\\s*[0-9]"],
      "cultural_authenticity_claims_score": ["cultural.{0,20}authenticity.{0,20}claims.{0,20}score", "cultural.{0,20}authenticity.{0,20}rating", "cultural\\s*authenticity\\s*:\\s*[0-9]"],
      "people_vs_elite_framing_salience": ["people.{0,20}vs.{0,20}elite.{0,20}framing.{0,20}salience", "people.{0,20}elite.{0,20}importance", "elite.{0,20}framing.{0,20}centrality"],
      "authentic_representation_claims_salience": ["authentic.{0,20}representation.{0,20}claims.{0,20}salience", "authentic.{0,20}representation.{0,20}importance", "authentic.{0,20}representation.{0,20}centrality"],
      "anti_system_mobilization_salience": ["anti.{0,20}system.{0,20}mobilization.{0,20}salience", "anti.{0,20}system.{0,20}importance", "anti.{0,20}system.{0,20}centrality"],
      "direct_democracy_appeals_salience": ["direct.{0,20}democracy.{0,20}appeals.{0,20}salience", "direct.{0,20}democracy.{0,20}importance", "direct.{0,20}democracy.{0,20}centrality"],
      "common_sense_vs_expertise_salience": ["common.{0,20}sense.{0,20}vs.{0,20}expertise.{0,20}salience", "common.{0,20}sense.{0,20}importance", "common.{0,20}sense.{0,20}centrality"],
      "cultural_authenticity_claims_salience": ["cultural.{0,20}authenticity.{0,20}claims.{0,20}salience", "cultural.{0,20}authenticity.{0,20}importance", "cultural.{0,20}authenticity.{0,20}centrality"],
      "people_vs_elite_framing_confidence": ["people.{0,20}vs.{0,20}elite.{0,20}framing.{0,20}confidence", "people.{0,20}elite.{0,20}certainty", "elite.{0,20}framing.{0,20}sure"],
      "authentic_representation_claims_confidence": ["authentic.{0,20}representation.{0,20}claims.{0,20}confidence", "authentic.{0,20}representation.{0,20}certainty", "authentic.{0,20}representation.{0,20}sure"],
      "anti_system_mobilization_confidence": ["anti.{0,20}system.{0,20}mobilization.{0,20}confidence", "anti.{0,20}system.{0,20}certainty", "anti.{0,20}system.{0,20}sure"],
      "direct_democracy_appeals_confidence": ["direct.{0,20}democracy.{0,20}appeals.{0,20}confidence", "direct.{0,20}democracy.{0,20}certainty", "direct.{0,20}democracy.{0,20}sure"],
      "common_sense_vs_expertise_confidence": ["common.{0,20}sense.{0,20}vs.{0,20}expertise.{0,20}confidence", "common.{0,20}sense.{0,20}certainty", "common.{0,20}sense.{0,20}sure"],
      "cultural_authenticity_claims_confidence": ["cultural.{0,20}authenticity.{0,20}claims.{0,20}confidence", "cultural.{0,20}authenticity.{0,20}certainty", "cultural.{0,20}authenticity.{0,20}sure"]
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
  }
}
```

</details>