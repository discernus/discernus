# Lakoff Framing Framework v5.0

**Version**: 5.0
**Status**: Active
**Major Change**: Embedded CSV Architecture for Synthesis Scalability

---

## Executive Summary

The Lakoff Framing Framework v5.0 analyzes political and social discourse using George Lakoff's model of family-based morality. It identifies whether communication is framed through a "Strict Father" model (emphasizing authority, discipline, and self-reliance) or a "Nurturant Parent" model (emphasizing empathy, cooperation, and interdependence). This version introduces tension analysis to quantify contradictions within a speaker's framing.

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
  "name": "lakoff_framing_v5_0",
  "version": "v5.0",
  "display_name": "Lakoff Framing Framework v5.0",
  "analysis_variants": {
    "default": {
      "description": "Complete salience-weighted family model analysis with moral framework tension pattern quantification and embedded CSV output.",
      "analysis_prompt": "Phase 1: Cognitive Priming: You are an expert in cognitive linguistics and political psychology, specializing in Lakoff's family model theory. Phase 2: Framework Methodology: Your task is to analyze the text using the Lakoff Framing Framework v5.0. Phase 3: Operational Definitions: Evaluate three bipolar dimensions on a scale from Strict Father (1.0) to Nurturant Parent (0.0): Authority vs. Empathy, Competition vs. Cooperation, and Self-Reliance vs. Interdependence. Phase 4: Scoring Protocol: For each dimension, determine the score (0.0-1.0), assess the salience of each pole (Strict Father and Nurturant Parent), and provide the strongest 1-2 quotes as evidence. Calculate the tension score for each dimension and the overall Family Model Strategic Contradiction Index (FMSCI). Phase 5: Framework-Specific CSV Structure: Your scores CSV must contain exactly 14 columns in this order: aid, authority_vs_empathy, competition_vs_cooperation, self_reliance_vs_interdependence, strict_father_salience_authority, nurturant_parent_salience_authority, strict_father_salience_competition, nurturant_parent_salience_competition, strict_father_salience_self_reliance, nurturant_parent_salience_self_reliance, authority_empathy_tension, competition_cooperation_tension, self_reliance_interdependence_tension, family_model_strategic_contradiction_index. Your evidence CSV must contain exactly 6 columns: aid, dimension, quote_id, quote_text, confidence_score, context_type. Phase 6: Output Specification: Return a complete response containing both a comprehensive JSON analysis AND the embedded CSV segments using the exact delimiters and column structures specified in the output_contract."
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
    "embedded_csv_requirements": {
      "scores_csv": {
        "delimiter_start": "<<<DISCERNUS_SCORES_CSV_v1>>>",
        "delimiter_end": "<<<END_DISCERNUS_SCORES_CSV_v1>>>",
        "description": "CSV for all dimensional scores, salience scores, tension scores, and calculated metrics.",
        "columns": [
          "aid",
          "authority_vs_empathy",
          "competition_vs_cooperation", 
          "self_reliance_vs_interdependence",
          "strict_father_salience_authority",
          "nurturant_parent_salience_authority",
          "strict_father_salience_competition",
          "nurturant_parent_salience_competition",
          "strict_father_salience_self_reliance",
          "nurturant_parent_salience_self_reliance",
          "authority_empathy_tension",
          "competition_cooperation_tension",
          "self_reliance_interdependence_tension",
          "family_model_strategic_contradiction_index"
        ]
      },
      "evidence_csv": {
        "delimiter_start": "<<<DISCERNUS_EVIDENCE_CSV_v1>>>",
        "delimiter_end": "<<<END_DISCERNUS_EVIDENCE_CSV_v1>>>",
        "description": "CSV for structured evidence data for audit and replication.",
        "columns": [
          "aid",
          "dimension",
          "quote_id",
          "quote_text", 
          "confidence_score",
          "context_type"
        ]
      }
    },
    "instructions": "IMPORTANT: Your response MUST include both a complete JSON analysis AND embedded CSV segments using the exact delimiters specified. The scores CSV must include exactly 14 columns: aid + 3 dimension scores + 6 salience scores + 3 tension scores + 1 FMSCI. The evidence CSV must include exactly 6 columns: aid + dimension + quote_id + quote_text + confidence_score + context_type."
  }
}
```

</details> 