# Cohesive Flourishing Framework v5.0

**Version**: 5.0
**Status**: Active
**Major Change**: Embedded CSV Architecture for Synthesis Scalability

---

## Executive Summary

The Cohesive Flourishing Framework (CFF) v5.0 integrates tension pattern analysis to provide a multi-dimensional assessment of discourse. It quantifies rhetorical contradictions between opposing dimensions and calculates an overall Strategic Contradiction Index (SCI). This allows for a nuanced understanding of a speaker's strategic coherence and rhetorical strategy.

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

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "cff_v5_0",
  "version": "v5.0",
  "display_name": "Cohesive Flourishing Framework v5.0",
  "analysis_variants": {
    "default": {
      "description": "Complete salience-weighted analysis with rhetorical tension pattern quantification and embedded CSV output.",
      "analysis_prompt": "Phase 1: Cognitive Priming: You are an expert discourse analyst specializing in social cohesion. Phase 2: Framework Methodology: Your task is to analyze the text using the Cohesive Flourishing Framework v5.0. Phase 3: Operational Definitions: Evaluate ten dimensions across five axes: Identity (Tribal Dominance vs. Individual Dignity), Emotional Climate (Fear vs. Hope), Success Orientation (Envy vs. Compersion), Relational Climate (Enmity vs. Amity), and Goal Orientation (Fragmentative vs. Cohesive). Phase 4: Scoring Protocol: For each of the ten dimensions, score its intensity (0.0-1.0) and salience (0.0-1.0). Provide the strongest 1-2 quotes as evidence. Calculate the tension score for each opposing pair and the overall Strategic Contradiction Index (SCI). Phase 5: Embedded CSV Generation: CRITICAL: Your response must include two embedded CSV segments using these exact delimiters: <<<DISCERNUS_SCORES_CSV_v1>>> and <<<DISCERNUS_EVIDENCE_CSV_v1>>>. The scores CSV must have columns for each dimension's score and salience, each tension score, and the SCI. The evidence CSV must have columns for dimension, quote, and confidence. Phase 6: Output Specification: Return a complete response containing both a comprehensive JSON analysis and the embedded CSV segments as specified in the output_contract."
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
  "output_contract": {
    "schema": {
      "worldview": "string",
      "scores": "object",
      "evidence": "object",
      "reasoning": "object",
      "salience_ranking": "array",
      "tension_analysis": "object"
    },
    "embedded_csv_requirements": {
      "scores_csv": {
        "delimiter_start": "<<<DISCERNUS_SCORES_CSV_v1>>>",
        "delimiter_end": "<<<END_DISCERNUS_SCORES_CSV_v1>>>",
        "description": "CSV for all dimensional scores, salience scores, tension scores, and calculated metrics."
      },
      "evidence_csv": {
        "delimiter_start": "<<<DISCERNUS_EVIDENCE_CSV_v1>>>",
        "delimiter_end": "<<<END_DISCERNUS_EVIDENCE_CSV_v1>>>",
        "description": "CSV for structured evidence data for audit and replication."
      }
    },
    "instructions": "IMPORTANT: Your response MUST include both a complete JSON analysis AND embedded CSV segments using the exact delimiters specified. The salience_ranking should be an ordered array of objects, each containing 'dimension', 'salience_score', and 'rank'."
  }
}
```

</details> 