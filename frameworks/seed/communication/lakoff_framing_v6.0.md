# Lakoff Framing Framework v6.0

**Version**: 6.0
**Status**: Active
**Major Change**: JSON-First Architecture with Enhanced Synthesis Integration

---

## Executive Summary

The Lakoff Framing Framework v6.0 analyzes political and social discourse using George Lakoff's model of family-based morality. It identifies whether communication is framed through a "Strict Father" model (emphasizing authority, discipline, and self-reliance) or a "Nurturant Parent" model (emphasizing empathy, cooperation, and interdependence). 

**NEW IN V6.0**: Returns to JSON-first output architecture while maintaining all analytical capabilities from v5.0, eliminating the complex 14-column CSV brittleness while preserving synthesis scalability. All tension calculations are now handled by explicit, auditable code execution.

---

## Framework Dimensions

### **Three Bipolar Dimensions: Family Model Architecture**

**1. Authority vs Empathy**
- **Strict Father (1.0)**: Strong leadership, moral authority, decisive action
- **Nurturant Parent (0.0)**: Understanding, inclusive dialogue, listening to voices

**2. Competition vs Cooperation**  
- **Strict Father (1.0)**: Natural hierarchy, merit-based systems, individual achievement
- **Nurturant Parent (0.0)**: Working together, shared responsibility, collaborative approaches

**3. Self-Reliance vs Interdependence**
- **Strict Father (1.0)**: Personal responsibility, self-reliance, bootstrap philosophy  
- **Nurturant Parent (0.0)**: Stronger together, mutual dependence, common good emphasis

---

## Family Model Tension Mathematics

### **Family Model Tension Scoring**

**Formula**: `Family Model Tension = min(Strict_Father_score, Nurturant_Parent_score) × |Strict_Father_salience - Nurturant_Parent_salience|`

### **Family Model Strategic Contradiction Index (FMSCI)**

**Formula**: `FMSCI = (Sum of all Family Model Tension Scores) / Number of Dimensions`

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "lakoff_framing_v6_0",
  "version": "v6.0",
  "display_name": "Lakoff Framing Framework v6.0",
  "analysis_variants": {
    "default": {
      "description": "Complete salience-weighted family model analysis with raw scoring only - mathematical tension calculations handled by code execution.",
      "analysis_prompt": "Phase 1: Cognitive Priming: You are an expert in cognitive linguistics and political psychology, specializing in Lakoff's family model theory. Phase 2: Framework Methodology: Your task is to analyze the text using the Lakoff Framing Framework v6.0. Phase 3: Operational Definitions: Evaluate three bipolar dimensions on a scale from Strict Father (1.0) to Nurturant Parent (0.0): Authority vs. Empathy, Competition vs. Cooperation, and Self-Reliance vs. Interdependence. Phase 4: Scoring Protocol: For each dimension, provide ONLY: (1) Raw score (0.0-1.0) representing the position on the Strict Father to Nurturant Parent spectrum, (2) Strict Father salience (0.0-1.0) based on prominence of authoritarian themes, (3) Nurturant Parent salience (0.0-1.0) based on prominence of cooperative themes, (4) Confidence score (0.0-1.0) based on evidence strength, (5) Supporting quotes with contextual analysis. DO NOT perform any mathematical calculations such as tension scores or FMSCI - this will be handled by code execution. Phase 5: JSON Structure Requirements: Your response must be a structured JSON object with nested data for raw scores only (NO calculated metrics), evidence organized by dimension, and reasoning for each assessment. Phase 6: Output Specification: Return a single, valid JSON object with raw dimensional scores only - NO tension calculations, FMSCI, or derived metrics. All mathematical processing will be handled by code execution."
    }
  },
  "dimension_groups": {
    "family_model_axes": ["authority_vs_empathy", "competition_vs_cooperation", "self_reliance_vs_interdependence"]
  },
  "calculation_spec": {
    "family_model_tension_mathematics": "Family model tension quantification for bipolar dimensions using formula: Family Model Tension = min(dimension_score, 1.0 - dimension_score) × |salience_effect|.",
    "family_model_tensions": {
      "authority_empathy_tension": "min(authority_vs_empathy, 1.0 - authority_vs_empathy) * abs(strict_father_salience_authority - nurturant_parent_salience_authority)",
      "competition_cooperation_tension": "min(competition_vs_cooperation, 1.0 - competition_vs_cooperation) * abs(strict_father_salience_competition - nurturant_parent_salience_competition)",
      "self_reliance_interdependence_tension": "min(self_reliance_vs_interdependence, 1.0 - self_reliance_vs_interdependence) * abs(strict_father_salience_self_reliance - nurturant_parent_salience_self_reliance)"
    },
    "family_model_strategic_contradiction_index": "(authority_empathy_tension + competition_cooperation_tension + self_reliance_interdependence_tension) / 3"
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
      "tension_analysis": "object"
    },
    "structured_data_requirements": {
      "scores": {
        "description": "Nested object containing ONLY raw dimensional scores (NO calculated metrics)",
        "structure": {
          "dimensions": {
            "authority_vs_empathy": {
              "score": "number (0.0-1.0)",
              "strict_father_salience": "number (0.0-1.0)",
              "nurturant_parent_salience": "number (0.0-1.0)",
              "confidence": "number (0.0-1.0)"
            },
            "competition_vs_cooperation": {
              "score": "number (0.0-1.0)",
              "strict_father_salience": "number (0.0-1.0)",
              "nurturant_parent_salience": "number (0.0-1.0)",
              "confidence": "number (0.0-1.0)"
            },
            "self_reliance_vs_interdependence": {
              "score": "number (0.0-1.0)",
              "strict_father_salience": "number (0.0-1.0)",
              "nurturant_parent_salience": "number (0.0-1.0)",
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
            "authority_vs_empathy": [
              {
                "quote_id": "string",
                "quote_text": "string", 
                "confidence": "number (0.0-1.0)",
                "context_type": "string",
                "family_model_justification": "string"
              }
            ],
            "competition_vs_cooperation": "array_of_evidence_objects",
            "self_reliance_vs_interdependence": "array_of_evidence_objects"
          },
          "metadata": {
            "total_quotes": "number",
            "average_confidence": "number"
          }
        }
      }
    },
    "instructions": "IMPORTANT: Your response MUST be a single, valid JSON object containing all required fields with the nested structures specified above. The tension_analysis should contain qualitative reasoning about family model patterns (NO mathematical calculations). All numerical scores must be between 0.0 and 1.0. DO NOT compute tension scores, FMSCI, or derived metrics - provide ONLY raw dimensional scores, salience values, confidence, and evidence."
  }
}
```

</details>