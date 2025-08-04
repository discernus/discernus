# Cohesive Flourishing Framework v6.0

**Version**: 6.0
**Status**: Active
**Major Change**: JSON-First Architecture with Enhanced Synthesis Integration

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
  "name": "cff_v6_0",
  "version": "v6.0",
  "display_name": "Cohesive Flourishing Framework v6.0",
  "analysis_variants": {
    "default": {
      "description": "Complete salience-weighted analysis with rhetorical tension pattern quantification and JSON-first output.",
      "analysis_prompt": "Phase 1: Cognitive Priming: You are an expert discourse analyst specializing in social cohesion and rhetorical strategy analysis across diverse political contexts. Phase 2: Framework Methodology: Your task is to analyze the text using the Cohesive Flourishing Framework v6.0, which measures discourse patterns through ten dimensions across five strategic axes. Phase 3: Operational Definitions: Evaluate ten dimensions across five axes: Identity (Tribal Dominance vs. Individual Dignity), Emotional Climate (Fear vs. Hope), Success Orientation (Envy vs. Compersion), Relational Climate (Enmity vs. Amity), and Goal Orientation (Fragmentative vs. Cohesive Goals). Phase 4: Scoring Protocol: For each of the ten dimensions, provide ONLY: (1) intensity score (0.0-1.0), (2) salience (0.0-1.0), (3) confidence (0.0-1.0), (4) evidence quotes with justification. Phase 5: JSON Structure Requirements: Your response must be a single, valid JSON object with nested structures for scores, evidence, reasoning, and salience ranking as specified in the output contract. Phase 6: Output Specification: Return structured JSON with raw dimensional scores only - NO calculation of tension scores or SCI (these will be computed by code)."
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
      "strategic_cohesion_patterns": "object"
    },
    "structured_data_requirements": {
      "scores": {
        "description": "Nested object containing ONLY raw dimensional scores (NO calculated tension indices)",
        "structure": {
          "dimensions": {
            "tribal_dominance": {
              "score": "number (0.0-1.0)",
              "salience": "number (0.0-1.0)",
              "confidence": "number (0.0-1.0)"
            },
            "individual_dignity": {
              "score": "number (0.0-1.0)",
              "salience": "number (0.0-1.0)",
              "confidence": "number (0.0-1.0)"
            },
            "fear": {
              "score": "number (0.0-1.0)",
              "salience": "number (0.0-1.0)",
              "confidence": "number (0.0-1.0)"
            },
            "hope": {
              "score": "number (0.0-1.0)",
              "salience": "number (0.0-1.0)",
              "confidence": "number (0.0-1.0)"
            },
            "envy": {
              "score": "number (0.0-1.0)",
              "salience": "number (0.0-1.0)",
              "confidence": "number (0.0-1.0)"
            },
            "compersion": {
              "score": "number (0.0-1.0)",
              "salience": "number (0.0-1.0)",
              "confidence": "number (0.0-1.0)"
            },
            "enmity": {
              "score": "number (0.0-1.0)",
              "salience": "number (0.0-1.0)",
              "confidence": "number (0.0-1.0)"
            },
            "amity": {
              "score": "number (0.0-1.0)",
              "salience": "number (0.0-1.0)",
              "confidence": "number (0.0-1.0)"
            },
            "fragmentative_goals": {
              "score": "number (0.0-1.0)",
              "salience": "number (0.0-1.0)",
              "confidence": "number (0.0-1.0)"
            },
            "cohesive_goals": {
              "score": "number (0.0-1.0)",
              "salience": "number (0.0-1.0)",
              "confidence": "number (0.0-1.0)"
            }
          },
          "metadata": {
            "total_dimensions": "number",
            "analysis_completeness": "number (0.0-1.0)"
          }
        }
      },
      "evidence": {
        "description": "Nested object containing structured evidence data for audit and replication",
        "structure": {
          "by_dimension": {
            "tribal_dominance": [
              {
                "quote_id": "string",
                "quote_text": "string", 
                "confidence": "number (0.0-1.0)",
                "context_type": "string",
                "salience_justification": "string"
              }
            ]
          },
          "metadata": {
            "total_quotes": "number",
            "average_confidence": "number"
          }
        }
      }
    },
    "instructions": "IMPORTANT: Your response MUST be a single, valid JSON object containing all required fields with the nested structures specified above. The salience_ranking should be an ordered array of objects, each containing 'dimension', 'salience_score', and 'rank'. The strategic_cohesion_patterns should contain qualitative reasoning about cohesion patterns (NO mathematical calculations). All numerical scores must be between 0.0 and 1.0. DO NOT compute tension scores or SCI - provide ONLY raw dimensional scores."
  }
}
```

</details> 