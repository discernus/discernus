# Populist Rhetoric Module (PRM) v7.3

**Version**: 7.1  
**Status**: Active  
**Major Change**: Enhanced Gasket Schema with Metadata Scores and Advanced Extraction Patterns

---

## Overview

The Populist Rhetoric Module (PRM) v7.3 represents a temporal module capturing era-specific populist phenomena (2010s-2020s) with enhanced metadata analysis. This framework analyzes contemporary populist political communication patterns through salience-weighted strategic emphasis assessment, revealing which populist appeals speakers prioritize rhetorically.

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

<GASKET_SCHEMA_START>
{
  "gasket_schema": {
    "version": "v7.3",
    "extraction_method": "intelligent_extractor",
    "target_keys": [
      "people_vs_elite_framing_score", "authentic_representation_claims_score", "anti_system_mobilization_score",
      "direct_democracy_appeals_score", "common_sense_vs_expertise_score", "cultural_authenticity_claims_score",
      "people_vs_elite_framing_salience", "authentic_representation_claims_salience", "anti_system_mobilization_salience",
      "direct_democracy_appeals_salience", "common_sense_vs_expertise_salience", "cultural_authenticity_claims_salience",
      "people_vs_elite_framing_confidence", "authentic_representation_claims_confidence", "anti_system_mobilization_confidence",
      "direct_democracy_appeals_confidence", "common_sense_vs_expertise_confidence", "cultural_authenticity_claims_confidence"
    ],
    "extraction_patterns": {
      "people_vs_elite_framing_score": ["people.*?vs.*?elite.*?framing.*?score.*?([0-9]\\.[0-9])", "people.*?elite.*?framing.*?([0-9]\\.[0-9])", "elite\\s*framing\\s*:\\s*([0-9]\\.[0-9])"],
      "authentic_representation_claims_score": ["authentic.*?representation.*?claims.*?score.*?([0-9]\\.[0-9])", "authentic.*?representation.*?([0-9]\\.[0-9])", "authentic\\s*representation\\s*:\\s*([0-9]\\.[0-9])"],
      "anti_system_mobilization_score": ["anti.*?system.*?mobilization.*?score.*?([0-9]\\.[0-9])", "anti.*?system.*?([0-9]\\.[0-9])", "anti\\s*system\\s*:\\s*([0-9]\\.[0-9])"],
      "direct_democracy_appeals_score": ["direct.*?democracy.*?appeals.*?score.*?([0-9]\\.[0-9])", "direct.*?democracy.*?([0-9]\\.[0-9])", "direct\\s*democracy\\s*:\\s*([0-9]\\.[0-9])"],
      "common_sense_vs_expertise_score": ["common.*?sense.*?vs.*?expertise.*?score.*?([0-9]\\.[0-9])", "common.*?sense.*?([0-9]\\.[0-9])", "common\\s*sense\\s*:\\s*([0-9]\\.[0-9])"],
      "cultural_authenticity_claims_score": ["cultural.*?authenticity.*?claims.*?score.*?([0-9]\\.[0-9])", "cultural.*?authenticity.*?([0-9]\\.[0-9])", "cultural\\s*authenticity\\s*:\\s*([0-9]\\.[0-9])"]
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
<GASKET_SCHEMA_END>