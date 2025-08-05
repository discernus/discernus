# Moral Foundations Theory Framework v7.1

**Version**: 7.1  
**Status**: Active  
**Major Change**: Enhanced Gasket Schema with Metadata Scores and Advanced Extraction Patterns

---

## Overview

The Moral Foundations Theory Framework v7.1 provides comprehensive analysis of moral reasoning patterns in political discourse using the six moral foundation pairs with enhanced metadata scoring. This advanced framework evaluates moral strategic contradictions and rhetorical coherence patterns with robust extraction patterns and validation rules.

**Purpose**: Analyzes moral reasoning in political discourse through six foundation pairs with enhanced extraction patterns and validation rules for comprehensive moral assessment.

**Innovation**: Comprehensive moral foundation analysis with tension mathematics revealing moral strategic contradictions in discourse.

**Applications**: Moral psychology analysis, political discourse assessment, comparative moral reasoning studies, rhetorical coherence evaluation.

---

## Framework Dimensions

### **Individualizing Foundations**

#### Care (0.0-1.0)
**Definition**: Compassion, protection, suffering prevention.
**Key Markers**: "compassion," "protect," "care for victims," "prevent suffering," "help those in need"

#### Harm (0.0-1.0)
**Definition**: Cruelty concern, violence prevention, victim advocacy.
**Key Markers**: "prevent violence," "stop cruelty," "victim advocacy," "end harm," "protect from damage"

#### Fairness (0.0-1.0)
**Definition**: Justice, equality, proportional treatment.
**Key Markers**: "justice," "equality," "fair treatment," "proportional response," "equal rights"

#### Cheating (0.0-1.0)
**Definition**: Unfairness concern, exploitation prevention, corruption focus.
**Key Markers**: "prevent exploitation," "stop corruption," "unfair advantage," "cheating system," "abuse of power"

### **Binding Foundations**

#### Loyalty (0.0-1.0)
**Definition**: Group cohesion, fidelity, solidarity.
**Key Markers**: "loyalty," "group solidarity," "fidelity," "team unity," "stand together"

#### Betrayal (0.0-1.0)
**Definition**: Group abandonment concern, treachery prevention.
**Key Markers**: "prevent betrayal," "stop treachery," "group abandonment," "disloyalty," "breaking trust"

#### Authority (0.0-1.0)
**Definition**: Hierarchy respect, tradition, legitimate order.
**Key Markers**: "respect authority," "traditional order," "legitimate hierarchy," "institutional respect," "proper order"

#### Subversion (0.0-1.0)
**Definition**: Rebellion concern, tradition undermining, hierarchy disruption.
**Key Markers**: "prevent rebellion," "stop subversion," "undermine tradition," "disrupt order," "challenge authority"

#### Sanctity (0.0-1.0)
**Definition**: Sacred preservation, purity, transcendence.
**Key Markers**: "sacred values," "purity," "transcendence," "holy," "spiritual sanctity"

#### Degradation (0.0-1.0)
**Definition**: Contamination concern, profane prevention, sacred violation.
**Key Markers**: "prevent contamination," "stop degradation," "sacred violation," "profane," "corrupted purity"

### **Liberty Foundation**

#### Liberty (0.0-1.0)
**Definition**: Freedom, autonomy, self-determination.
**Key Markers**: "freedom," "autonomy," "self-determination," "individual liberty," "personal choice"

#### Oppression (0.0-1.0)
**Definition**: Control concern, domination prevention, freedom protection.
**Key Markers**: "prevent oppression," "stop domination," "protect freedom," "resist control," "fight tyranny"

---

## Gasket Architecture

### Raw Analysis Log Format
The analysis agent outputs a raw analysis log containing:
- Moral foundation scores for all 12 foundations
- Salience weights for each foundation
- Evidence quotes with confidence ratings
- Qualitative reasoning about moral patterns

### Intelligent Extractor Schema
```json
{
  "gasket_schema": {
    "target_keys": [
      "care_score", "harm_score", "fairness_score", "cheating_score",
      "loyalty_score", "betrayal_score", "authority_score", "subversion_score",
      "sanctity_score", "degradation_score", "liberty_score", "oppression_score",
      "care_salience", "harm_salience", "fairness_salience", "cheating_salience",
      "loyalty_salience", "betrayal_salience", "authority_salience", "subversion_salience",
      "sanctity_salience", "degradation_salience", "liberty_salience", "oppression_salience",
      "care_confidence", "harm_confidence", "fairness_confidence", "cheating_confidence",
      "loyalty_confidence", "betrayal_confidence", "authority_confidence", "subversion_confidence",
      "sanctity_confidence", "degradation_confidence", "liberty_confidence", "oppression_confidence"
    ]
  }
}
```

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "moral_foundations_theory_v7_1",
  "version": "v7.1",
  "display_name": "Moral Foundations Theory Framework v7.1",
  "analysis_variants": {
    "default": {
      "description": "Complete salience-weighted moral foundation analysis with tension pattern quantification and raw analysis log output.",
      "analysis_prompt": "You are an expert analyst specializing in moral psychology and Moral Foundations Theory across diverse contexts. Your task is to analyze the provided text using the Moral Foundations Theory Framework v7.1, which captures moral reasoning patterns through six foundation pairs with enhanced metadata scoring and comprehensive moral assessment.\n\nThe framework evaluates moral reasoning across six foundation pairs:\n\n**Individualizing Foundations**: Care (0.0-1.0) - compassion, protection, suffering prevention vs. Harm (0.0-1.0) - cruelty concern, violence prevention; Fairness (0.0-1.0) - justice, equality, proportional treatment vs. Cheating (0.0-1.0) - unfairness concern, exploitation prevention.\n\n**Binding Foundations**: Loyalty (0.0-1.0) - group cohesion, fidelity, solidarity vs. Betrayal (0.0-1.0) - group abandonment concern; Authority (0.0-1.0) - hierarchy respect, tradition, legitimate order vs. Subversion (0.0-1.0) - rebellion concern, tradition undermining; Sanctity (0.0-1.0) - sacred preservation, purity, transcendence vs. Degradation (0.0-1.0) - contamination concern, profane prevention.\n\n**Liberty Foundation**: Liberty (0.0-1.0) - freedom, autonomy, self-determination vs. Oppression (0.0-1.0) - control concern, domination prevention.\n\nFor each foundation, provide:\n- **Score (0.0-1.0)**: Based on strength of evidence in the text\n- **Salience (0.0-1.0)**: How central is this foundation to this specific text?\n- **Confidence (0.0-1.0)**: How certain are you in this assessment?\n\nWrite a comprehensive analytical report that covers:\n- Application of the Moral Foundations Theory methodology to this specific text\n- Detailed analysis of each relevant foundation with scores, salience, confidence, and evidence\n- Assessment of moral reasoning patterns and strategic contradictions\n- Overall moral profile with salience weighting across all six foundation pairs\n- Key insights about the speaker's moral framework and rhetorical approach\n\nEmbed your numerical assessments naturally within the analysis. For example: 'This text demonstrates strong care foundation appeals (care score: 0.8, salience: 0.9, confidence: 0.7) with frequent references to compassion and protection.' Focus on rigorous intellectual analysis supported by direct textual evidence and clear reasoning for all scores and metadata."
    }
  },
  "dimension_groups": {
    "individualizing_foundations": ["care", "harm", "fairness", "cheating"],
    "binding_foundations": ["loyalty", "betrayal", "authority", "subversion", "sanctity", "degradation"],
    "liberty_foundation": ["liberty", "oppression"],
    "foundation_pairs": ["care_harm", "fairness_cheating", "loyalty_betrayal", "authority_subversion", "sanctity_degradation", "liberty_oppression"]
  },
  "calculation_spec": {
    "individualizing_foundations_score": "(care_score + fairness_score - harm_score - cheating_score) / 4",
    "binding_foundations_score": "(loyalty_score + authority_score + sanctity_score - betrayal_score - subversion_score - degradation_score) / 6",
    "liberty_foundation_score": "(liberty_score - oppression_score) / 2",
    "care_harm_tension": "min(care_score, harm_score) * abs(care_salience - harm_salience)",
    "fairness_cheating_tension": "min(fairness_score, cheating_score) * abs(fairness_salience - cheating_salience)",
    "loyalty_betrayal_tension": "min(loyalty_score, betrayal_score) * abs(loyalty_salience - betrayal_salience)",
    "authority_subversion_tension": "min(authority_score, subversion_score) * abs(authority_salience - subversion_salience)",
    "sanctity_degradation_tension": "min(sanctity_score, degradation_score) * abs(sanctity_salience - degradation_salience)",
    "liberty_oppression_tension": "min(liberty_score, oppression_score) * abs(liberty_salience - oppression_salience)",
    "moral_strategic_contradiction_index": "(care_harm_tension + fairness_cheating_tension + loyalty_betrayal_tension + authority_subversion_tension + sanctity_degradation_tension + liberty_oppression_tension) / 6"
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
      "care_score", "harm_score", "fairness_score", "cheating_score",
      "loyalty_score", "betrayal_score", "authority_score", "subversion_score",
      "sanctity_score", "degradation_score", "liberty_score", "oppression_score",
      "care_salience", "harm_salience", "fairness_salience", "cheating_salience",
      "loyalty_salience", "betrayal_salience", "authority_salience", "subversion_salience",
      "sanctity_salience", "degradation_salience", "liberty_salience", "oppression_salience",
      "care_confidence", "harm_confidence", "fairness_confidence", "cheating_confidence",
      "loyalty_confidence", "betrayal_confidence", "authority_confidence", "subversion_confidence",
      "sanctity_confidence", "degradation_confidence", "liberty_confidence", "oppression_confidence"
    ],
    "extraction_patterns": {
      "care_score": ["care.{0,20}score", "care.{0,20}rating", "care\\s*:\\s*[0-9]"],
      "harm_score": ["harm.{0,20}score", "harm.{0,20}rating", "harm\\s*:\\s*[0-9]"],
      "fairness_score": ["fairness.{0,20}score", "fairness.{0,20}rating", "fairness\\s*:\\s*[0-9]"],
      "cheating_score": ["cheating.{0,20}score", "cheating.{0,20}rating", "cheating\\s*:\\s*[0-9]"],
      "loyalty_score": ["loyalty.{0,20}score", "loyalty.{0,20}rating", "loyalty\\s*:\\s*[0-9]"],
      "betrayal_score": ["betrayal.{0,20}score", "betrayal.{0,20}rating", "betrayal\\s*:\\s*[0-9]"],
      "authority_score": ["authority.{0,20}score", "authority.{0,20}rating", "authority\\s*:\\s*[0-9]"],
      "subversion_score": ["subversion.{0,20}score", "subversion.{0,20}rating", "subversion\\s*:\\s*[0-9]"],
      "sanctity_score": ["sanctity.{0,20}score", "sanctity.{0,20}rating", "sanctity\\s*:\\s*[0-9]"],
      "degradation_score": ["degradation.{0,20}score", "degradation.{0,20}rating", "degradation\\s*:\\s*[0-9]"],
      "liberty_score": ["liberty.{0,20}score", "liberty.{0,20}rating", "liberty\\s*:\\s*[0-9]"],
      "oppression_score": ["oppression.{0,20}score", "oppression.{0,20}rating", "oppression\\s*:\\s*[0-9]"],
      "care_salience": ["care.{0,20}salience", "care.{0,20}importance", "care.{0,20}centrality"],
      "harm_salience": ["harm.{0,20}salience", "harm.{0,20}importance", "harm.{0,20}centrality"],
      "fairness_salience": ["fairness.{0,20}salience", "fairness.{0,20}importance", "fairness.{0,20}centrality"],
      "cheating_salience": ["cheating.{0,20}salience", "cheating.{0,20}importance", "cheating.{0,20}centrality"],
      "loyalty_salience": ["loyalty.{0,20}salience", "loyalty.{0,20}importance", "loyalty.{0,20}centrality"],
      "betrayal_salience": ["betrayal.{0,20}salience", "betrayal.{0,20}importance", "betrayal.{0,20}centrality"],
      "authority_salience": ["authority.{0,20}salience", "authority.{0,20}importance", "authority.{0,20}centrality"],
      "subversion_salience": ["subversion.{0,20}salience", "subversion.{0,20}importance", "subversion.{0,20}centrality"],
      "sanctity_salience": ["sanctity.{0,20}salience", "sanctity.{0,20}importance", "sanctity.{0,20}centrality"],
      "degradation_salience": ["degradation.{0,20}salience", "degradation.{0,20}importance", "degradation.{0,20}centrality"],
      "liberty_salience": ["liberty.{0,20}salience", "liberty.{0,20}importance", "liberty.{0,20}centrality"],
      "oppression_salience": ["oppression.{0,20}salience", "oppression.{0,20}importance", "oppression.{0,20}centrality"],
      "care_confidence": ["care.{0,20}confidence", "care.{0,20}certainty", "care.{0,20}sure"],
      "harm_confidence": ["harm.{0,20}confidence", "harm.{0,20}certainty", "harm.{0,20}sure"],
      "fairness_confidence": ["fairness.{0,20}confidence", "fairness.{0,20}certainty", "fairness.{0,20}sure"],
      "cheating_confidence": ["cheating.{0,20}confidence", "cheating.{0,20}certainty", "cheating.{0,20}sure"],
      "loyalty_confidence": ["loyalty.{0,20}confidence", "loyalty.{0,20}certainty", "loyalty.{0,20}sure"],
      "betrayal_confidence": ["betrayal.{0,20}confidence", "betrayal.{0,20}certainty", "betrayal.{0,20}sure"],
      "authority_confidence": ["authority.{0,20}confidence", "authority.{0,20}certainty", "authority.{0,20}sure"],
      "subversion_confidence": ["subversion.{0,20}confidence", "subversion.{0,20}certainty", "subversion.{0,20}sure"],
      "sanctity_confidence": ["sanctity.{0,20}confidence", "sanctity.{0,20}certainty", "sanctity.{0,20}sure"],
      "degradation_confidence": ["degradation.{0,20}confidence", "degradation.{0,20}certainty", "degradation.{0,20}sure"],
      "liberty_confidence": ["liberty.{0,20}confidence", "liberty.{0,20}certainty", "liberty.{0,20}sure"],
      "oppression_confidence": ["oppression.{0,20}confidence", "oppression.{0,20}certainty", "oppression.{0,20}sure"]
    },
    "validation_rules": {
      "required_fields": [
        "care_score", "harm_score", "fairness_score", "cheating_score",
        "loyalty_score", "betrayal_score", "authority_score", "subversion_score",
        "sanctity_score", "degradation_score", "liberty_score", "oppression_score"
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