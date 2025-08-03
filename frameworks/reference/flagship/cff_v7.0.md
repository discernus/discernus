# Cohesive Flourishing Framework v7.0
**Version**: 7.0
**Status**: Active
**Major Change**: Gasket Architecture with Raw Analysis Log

---

## Executive Summary

The Cohesive Flourishing Framework (CFF) v7.0 integrates tension pattern analysis to provide a multi-dimensional assessment of discourse. It quantifies rhetorical contradictions between opposing dimensions and calculates an overall Strategic Contradiction Index (SCI). This allows for a nuanced understanding of a speaker's strategic coherence and rhetorical strategy.

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
    ],
    "target_dimensions": [
      "fear_hope_tension",
      "enmity_amity_tension",
      "envy_compersion_tension",
      "dominance_dignity_tension",
      "fragmentative_cohesive_tension",
      "strategic_contradiction_index"
    ]
  }
}
```

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "cff_v7_0",
  "version": "v7.0",
  "display_name": "Cohesive Flourishing Framework v7.0",
  "analysis_variants": {
    "default": {
      "description": "Complete salience-weighted analysis with rhetorical tension pattern quantification and raw analysis log output.",
      "analysis_prompt": "Phase 1: Cognitive Priming: You are an expert discourse analyst specializing in social cohesion and rhetorical strategy analysis across diverse political contexts. Phase 2: Framework Methodology: Your task is to analyze the text using the Cohesive Flourishing Framework v7.0, which measures discourse patterns through ten dimensions across five strategic axes. Phase 3: Operational Definitions: Evaluate ten dimensions across five axes: Identity (Tribal Dominance vs. Individual Dignity), Emotional Climate (Fear vs. Hope), Success Orientation (Envy vs. Compersion), Relational Climate (Enmity vs. Amity), and Goal Orientation (Fragmentative vs. Cohesive Goals). Phase 4: Scoring Protocol: For each of the ten dimensions, provide ONLY: (1) intensity score (0.0-1.0), (2) salience (0.0-1.0), (3) confidence (0.0-1.0), (4) evidence quotes with justification. Phase 5: Raw Analysis Log Requirements: Your response must be a raw analysis log containing dimensional scores, evidence, and reasoning - NO JSON structure or derived calculations. Phase 6: Output Specification: Return raw analysis log with dimensional scores only - NO calculation of tension scores or SCI (these will be computed by code)."
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
    "target_dimensions": [
      "fear_hope_tension",
      "enmity_amity_tension",
      "envy_compersion_tension",
      "dominance_dignity_tension",
      "fragmentative_cohesive_tension",
      "strategic_contradiction_index"
    ]
  },
  "raw_analysis_log_format": {
    "description": "Raw analysis log containing dimensional scores, evidence, and reasoning without structured JSON",
    "content": "Free-form text with cohesion analysis including scores, evidence quotes, and qualitative reasoning"
  }
}
```

</details> 