# Cohesive Flourishing Framework v7.1
**Version**: 7.1
**Status**: Active
**Major Change**: Enhanced Gasket Schema with Metadata Scores and Advanced Extraction Patterns

---

## Executive Summary

The Cohesive Flourishing Framework (CFF) v7.1 integrates tension pattern analysis to provide a multi-dimensional assessment of discourse. It quantifies rhetorical contradictions between opposing dimensions and calculates an overall Strategic Contradiction Index (SCI). This version includes enhanced gasket schema with metadata scores (salience and confidence) and advanced extraction patterns for robust analysis.

---

## Framework Dimensions

### **Identity Axis**

**Tribal Dominance** (0.0-1.0): In-group supremacy and exclusionary identity patterns  
**Individual Dignity** (0.0-1.0): Universal human worth and inclusive dignity appeals

### **Emotional Climate**

**Fear** (0.0-1.0): Crisis mentality, threat perception, vulnerability emphasis  
**Hope** (0.0-1.0): Progress orientation, opportunity focus, optimistic vision

### **Success Orientation** 

**Envy** (0.0-1.0): Resentment toward others' success, zero-sum thinking  
**Compersion** (0.0-1.0): Celebration of others' success, abundance mindset

### **Relational Climate**

**Enmity** (0.0-1.0): Hostility, antagonism, adversarial positioning  
**Amity** (0.0-1.0): Friendship, cooperation, collaborative approach

### **Goal Orientation**

**Fragmentative Goals** (0.0-1.0): Division, separation, destructive objectives  
**Cohesive Goals** (0.0-1.0): Unity, building, integrative objectives

---

## Tension Mathematics

### **Dimensional Tension Scoring**

**Formula**: `Tension Score = min(Anchor_A_score, Anchor_B_score) × |Salience_A - Salience_B|`

### **Strategic Contradiction Index (SCI)**

**Formula**: `SCI = (Sum of all Tension Scores) / Number of Opposing Pairs`

---

## Gasket Architecture

### Raw Analysis Log Format
The analysis agent outputs a raw analysis log containing:
- Dimensional scores for all 10 dimensions across 5 axes
- Salience weights for each dimension
- Evidence quotes with confidence ratings
- Qualitative reasoning about cohesion patterns

### Intelligent Extractor Schema
```json
{
  "gasket_schema": {
    "target_keys": [
      "tribal_dominance_score",
      "individual_dignity_score",
      "fear_score",
      "hope_score",
      "envy_score",
      "compersion_score",
      "enmity_score",
      "amity_score",
      "fragmentative_goals_score",
      "cohesive_goals_score",
      "tribal_dominance_salience",
      "individual_dignity_salience",
      "fear_salience",
      "hope_salience",
      "envy_salience",
      "compersion_salience",
      "enmity_salience",
      "amity_salience",
      "fragmentative_goals_salience",
      "cohesive_goals_salience",
      "tribal_dominance_confidence",
      "individual_dignity_confidence",
      "fear_confidence",
      "hope_confidence",
      "envy_confidence",
      "compersion_confidence",
      "enmity_confidence",
      "amity_confidence",
      "fragmentative_goals_confidence",
      "cohesive_goals_confidence"
    ]
  }
}
```

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "cff_v7_1",
  "version": "v7.1",
  "display_name": "Cohesive Flourishing Framework v7.1",
  "analysis_variants": {
    "default": {
      "description": "Complete salience-weighted analysis with rhetorical tension pattern quantification and raw analysis log output.",
      "analysis_prompt": "You are an expert discourse analyst specializing in social cohesion and rhetorical strategy analysis across diverse political contexts. Your task is to analyze the provided text using the Cohesive Flourishing Framework (CFF) v7.1, which measures discourse patterns through ten dimensions across five strategic axes with enhanced metadata reporting.\n\nThe framework evaluates discourse across five strategic axes:\n\n**Identity Axis**: Tribal Dominance (0.0-1.0) - in-group supremacy and exclusionary identity patterns vs. Individual Dignity (0.0-1.0) - universal human worth and inclusive dignity appeals.\n\n**Emotional Climate**: Fear (0.0-1.0) - crisis mentality, threat perception, vulnerability emphasis vs. Hope (0.0-1.0) - progress orientation, opportunity focus, optimistic vision.\n\n**Success Orientation**: Envy (0.0-1.0) - resentment toward others' success, zero-sum thinking vs. Compersion (0.0-1.0) - celebration of others' success, abundance mindset.\n\n**Relational Climate**: Enmity (0.0-1.0) - hostility, antagonism, adversarial positioning vs. Amity (0.0-1.0) - friendship, cooperation, collaborative approach.\n\n**Goal Orientation**: Fragmentative Goals (0.0-1.0) - division, separation, destructive objectives vs. Cohesive Goals (0.0-1.0) - unity, building, integrative objectives.\n\nFor each dimension, provide:\n- **Score (0.0-1.0)**: Based on strength of evidence in the text\n- **Salience (0.0-1.0)**: How central is this dimension to this specific text?\n- **Confidence (0.0-1.0)**: How certain are you in this assessment?\n\nWrite a comprehensive analytical report that covers:\n- Application of the CFF methodology to this specific text\n- Detailed analysis of each relevant dimension with scores, salience, confidence, and evidence\n- Assessment of strategic tensions between opposing dimensions\n- Overall discourse pattern profile with salience weighting\n- Key insights about the speaker's rhetorical approach\n\nEmbed your numerical assessments naturally within the analysis. For example: 'This text demonstrates strong hope appeals (hope score: 0.8, salience: 0.9, confidence: 0.7) with frequent references to positive possibilities.' Focus on rigorous intellectual analysis supported by direct textual evidence and clear reasoning for all scores and metadata."
    }
  },
  "dimension_groups": {
    "identity_axis": ["tribal_dominance", "individual_dignity"],
    "emotional_climate_axis": ["fear", "hope"],
    "success_orientation_axis": ["envy", "compersion"],
    "relational_climate_axis": ["enmity", "amity"],
    "goal_orientation_axis": ["fragmentative_goals", "cohesive_goals"]
  },
  "calculation_spec": {
    "tension_mathematics_explanation": "Rhetorical tension quantification using formula: Tension Score = min(Anchor_A_score, Anchor_B_score) × |Salience_A - Salience_B|.",
    "dimensional_tensions": {
      "fear_hope_tension": "min(fear, hope) * abs(fear_salience - hope_salience)",
      "enmity_amity_tension": "min(enmity, amity) * abs(enmity_salience - amity_salience)",
      "envy_compersion_tension": "min(envy, compersion) * abs(envy_salience - compersion_salience)",
      "dominance_dignity_tension": "min(tribal_dominance, individual_dignity) * abs(tribal_dominance_salience - individual_dignity_salience)",
      "fragmentative_cohesive_tension": "min(fragmentative_goals, cohesive_goals) * abs(fragmentative_goals_salience - cohesive_goals_salience)"
    },
    "strategic_contradiction_index": "(fear_hope_tension + enmity_amity_tension + envy_compersion_tension + dominance_dignity_tension + fragmentative_cohesive_tension) / 5"
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
      "tribal_dominance_score",
      "individual_dignity_score",
      "fear_score",
      "hope_score",
      "envy_score",
      "compersion_score",
      "enmity_score",
      "amity_score",
      "fragmentative_goals_score",
      "cohesive_goals_score",
      "tribal_dominance_salience",
      "individual_dignity_salience",
      "fear_salience",
      "hope_salience",
      "envy_salience",
      "compersion_salience",
      "enmity_salience",
      "amity_salience",
      "fragmentative_goals_salience",
      "cohesive_goals_salience",
      "tribal_dominance_confidence",
      "individual_dignity_confidence",
      "fear_confidence",
      "hope_confidence",
      "envy_confidence",
      "compersion_confidence",
      "enmity_confidence",
      "amity_confidence",
      "fragmentative_goals_confidence",
      "cohesive_goals_confidence"
    ],
    "extraction_patterns": {
      "tribal_dominance_score": ["tribal.{0,20}dominance.{0,20}score", "tribal.{0,20}dominance.{0,20}rating", "tribal\\s*dominance\\s*:\\s*[0-9]"],
      "individual_dignity_score": ["individual.{0,20}dignity.{0,20}score", "individual.{0,20}dignity.{0,20}rating", "dignity\\s*:\\s*[0-9]"],
      "fear_score": ["fear.{0,20}score", "fear.{0,20}rating", "fear\\s*:\\s*[0-9]"],
      "hope_score": ["hope.{0,20}score", "hope.{0,20}rating", "hope\\s*:\\s*[0-9]"],
      "envy_score": ["envy.{0,20}score", "envy.{0,20}rating", "envy\\s*:\\s*[0-9]"],
      "compersion_score": ["compersion.{0,20}score", "compersion.{0,20}rating", "compersion\\s*:\\s*[0-9]"],
      "enmity_score": ["enmity.{0,20}score", "enmity.{0,20}rating", "enmity\\s*:\\s*[0-9]"],
      "amity_score": ["amity.{0,20}score", "amity.{0,20}rating", "amity\\s*:\\s*[0-9]"],
      "fragmentative_goals_score": ["fragmentative.{0,20}goals.{0,20}score", "fragmentative.{0,20}score", "fragmentative\\s*:\\s*[0-9]"],
      "cohesive_goals_score": ["cohesive.{0,20}goals.{0,20}score", "cohesive.{0,20}score", "cohesive\\s*:\\s*[0-9]"],
      "tribal_dominance_salience": ["tribal.{0,20}dominance.{0,20}salience", "tribal.{0,20}dominance.{0,20}importance", "dominance.{0,20}centrality"],
      "individual_dignity_salience": ["individual.{0,20}dignity.{0,20}salience", "dignity.{0,20}importance", "dignity.{0,20}centrality"],
      "fear_salience": ["fear.{0,20}salience", "fear.{0,20}importance", "fear.{0,20}centrality"],
      "hope_salience": ["hope.{0,20}salience", "hope.{0,20}importance", "hope.{0,20}centrality"],
      "envy_salience": ["envy.{0,20}salience", "envy.{0,20}importance", "envy.{0,20}centrality"],
      "compersion_salience": ["compersion.{0,20}salience", "compersion.{0,20}importance", "compersion.{0,20}centrality"],
      "enmity_salience": ["enmity.{0,20}salience", "enmity.{0,20}importance", "enmity.{0,20}centrality"],
      "amity_salience": ["amity.{0,20}salience", "amity.{0,20}importance", "amity.{0,20}centrality"],
      "fragmentative_goals_salience": ["fragmentative.{0,20}goals.{0,20}salience", "fragmentative.{0,20}importance", "fragmentative.{0,20}centrality"],
      "cohesive_goals_salience": ["cohesive.{0,20}goals.{0,20}salience", "cohesive.{0,20}importance", "cohesive.{0,20}centrality"],
      "tribal_dominance_confidence": ["tribal.{0,20}dominance.{0,20}confidence", "tribal.{0,20}dominance.{0,20}certainty", "dominance.{0,20}sure"],
      "individual_dignity_confidence": ["individual.{0,20}dignity.{0,20}confidence", "dignity.{0,20}certainty", "dignity.{0,20}sure"],
      "fear_confidence": ["fear.{0,20}confidence", "fear.{0,20}certainty", "fear.{0,20}sure"],
      "hope_confidence": ["hope.{0,20}confidence", "hope.{0,20}certainty", "hope.{0,20}sure"],
      "envy_confidence": ["envy.{0,20}confidence", "envy.{0,20}certainty", "envy.{0,20}sure"],
      "compersion_confidence": ["compersion.{0,20}confidence", "compersion.{0,20}certainty", "compersion.{0,20}sure"],
      "enmity_confidence": ["enmity.{0,20}confidence", "enmity.{0,20}certainty", "enmity.{0,20}sure"],
      "amity_confidence": ["amity.{0,20}confidence", "amity.{0,20}certainty", "amity.{0,20}sure"],
      "fragmentative_goals_confidence": ["fragmentative.{0,20}goals.{0,20}confidence", "fragmentative.{0,20}certainty", "fragmentative.{0,20}sure"],
      "cohesive_goals_confidence": ["cohesive.{0,20}goals.{0,20}confidence", "cohesive.{0,20}certainty", "cohesive.{0,20}sure"]
    },
    "validation_rules": {
      "required_fields": [
        "tribal_dominance_score", "individual_dignity_score", "fear_score", "hope_score", "envy_score",
        "compersion_score", "enmity_score", "amity_score", "fragmentative_goals_score", "cohesive_goals_score"
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