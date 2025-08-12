# Lakoff Framing Framework v7.1

**Version**: 7.1
**Status**: Active
**Major Change**: Enhanced Gasket Schema with Metadata Scores and Advanced Extraction Patterns

---

## Executive Summary

The Lakoff Framing Framework v7.1 analyzes political and social discourse using George Lakoff's model of family-based morality with enhanced metadata analysis. It identifies whether communication is framed through a "Strict Father" model (emphasizing authority, discipline, and self-reliance) or a "Nurturant Parent" model (emphasizing empathy, cooperation, and interdependence), with advanced extraction patterns and validation rules for robust analysis.

**Innovation**: Salience-weighted analysis captures not just family model presence but which moral frameworks receive the most rhetorical emphasis.

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
  "name": "lakoff_framing_v7_1",
  "version": "v7.1",
  "display_name": "Lakoff Framing Framework v7.1",
  "analysis_variants": {
    "default": {
      "description": "Complete salience-weighted family model analysis with raw analysis log output.",
      "analysis_prompt": "You are an expert in cognitive linguistics and political psychology, specializing in Lakoff's family model theory across diverse cultural contexts. Your task is to analyze the provided text using the Lakoff Framing Framework v7.1, which measures family model patterns through three bipolar dimensions with enhanced metadata scoring based on George Lakoff's model of family-based morality.\n\nThe framework evaluates discourse across three bipolar dimensions on a scale from Strict Father (1.0) to Nurturant Parent (0.0):\n\n**Authority vs Empathy** (0.0-1.0): Strict Father model emphasizes strong leadership, moral authority, decisive action (1.0) vs. Nurturant Parent model emphasizes understanding, inclusive dialogue, listening to voices (0.0).\n\n**Competition vs Cooperation** (0.0-1.0): Strict Father model emphasizes natural hierarchy, merit-based systems, individual achievement (1.0) vs. Nurturant Parent model emphasizes working together, shared responsibility, collaborative approaches (0.0).\n\n**Self-Reliance vs Interdependence** (0.0-1.0): Strict Father model emphasizes personal responsibility, self-reliance, bootstrap philosophy (1.0) vs. Nurturant Parent model emphasizes stronger together, mutual dependence, common good emphasis (0.0).\n\nFor each dimension, provide:\n- **Score (0.0-1.0)**: Based on strength of evidence in the text (0.0 = pure Nurturant Parent, 1.0 = pure Strict Father)\n- **Salience (0.0-1.0)**: How central is this dimension to this specific text?\n- **Confidence (0.0-1.0)**: How certain are you in this assessment?\n\nWrite a comprehensive analytical report that covers:\n- Application of the Lakoff Framing methodology to this specific text\n- Detailed analysis of each bipolar dimension with scores, salience, confidence, and evidence\n- Assessment of family model patterns and strategic moral framework deployment\n- Overall family model profile revealing Strict Father vs. Nurturant Parent orientation\n- Key insights about the speaker's approach to family-based moral reasoning\n\nEmbed your numerical assessments naturally within the analysis. For example: 'This text demonstrates strong authority vs empathy tension (authority vs empathy score: 0.8, salience: 0.9, confidence: 0.7) with clear Strict Father model orientation.' Focus on rigorous intellectual analysis supported by direct textual evidence and clear reasoning for all scores and metadata."
    }
  },
  "dimension_groups": {
    "family_model_axes": ["authority_vs_empathy", "competition_vs_cooperation", "self_reliance_vs_interdependence"]
  },
  "calculation_spec": {
    "family_model_tension_mathematics": "Family model tension quantification for bipolar dimensions using formula: Family Model Tension = min(dimension_score, 1.0 - dimension_score) × |salience_effect|.",
    "family_model_tensions": {
      "authority_empathy_tension": "min(authority_vs_empathy_score, 1.0 - authority_vs_empathy_score) * authority_vs_empathy_salience",
      "competition_cooperation_tension": "min(competition_vs_cooperation_score, 1.0 - competition_vs_cooperation_score) * competition_vs_cooperation_salience",
      "self_reliance_interdependence_tension": "min(self_reliance_vs_interdependence_score, 1.0 - self_reliance_vs_interdependence_score) * self_reliance_vs_interdependence_salience"
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
  }
}
```

</details>

<GASKET_SCHEMA_START>
{
  "gasket_schema": {
    "version": "v7.1",
    "extraction_method": "intelligent_extractor",
    "target_keys": [
      "authority_vs_empathy_score", "competition_vs_cooperation_score", "self_reliance_vs_interdependence_score",
      "authority_vs_empathy_salience", "competition_vs_cooperation_salience", "self_reliance_vs_interdependence_salience",
      "authority_vs_empathy_confidence", "competition_vs_cooperation_confidence", "self_reliance_vs_interdependence_confidence"
    ],
    "extraction_patterns": {
      "authority_vs_empathy_score": ["authority.{0,20}vs.{0,20}empathy.{0,20}score", "authority.{0,20}empathy.{0,20}rating", "authority\\s*vs\\s*empathy\\s*:\\s*[0-9]"],
      "competition_vs_cooperation_score": ["competition.{0,20}vs.{0,20}cooperation.{0,20}score", "competition.{0,20}cooperation.{0,20}rating", "competition\\s*vs\\s*cooperation\\s*:\\s*[0-9]"],
      "self_reliance_vs_interdependence_score": ["self.{0,20}reliance.{0,20}vs.{0,20}interdependence.{0,20}score", "self.{0,20}reliance.{0,20}rating", "self\\s*reliance\\s*vs\\s*interdependence\\s*:\\s*[0-9]"]
    },
    "validation_rules": {
      "required_fields": [
        "authority_vs_empathy_score", "competition_vs_cooperation_score", "self_reliance_vs_interdependence_score"
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