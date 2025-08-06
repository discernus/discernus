# Political Worldview Triad Framework v7.3

**Version**: 7.1  
**Status**: Active  
**Major Change**: Enhanced Gasket Schema with Metadata Scores and Advanced Extraction Patterns

---

## Overview

The Political Worldview Triad Framework v7.3 identifies three competing sources of political legitimacy that shape contemporary democratic discourse with enhanced metadata scoring. This advanced framework analyzes how texts appeal to identity-based claims, dominance-seeking narratives, and universal dignity principles, revealing the underlying value structures that drive political communication.

**Purpose**: Analyzes political discourse through three competing legitimacy sources with enhanced extraction patterns and validation rules for comprehensive worldview assessment.

**Innovation**: Triadic analysis framework that captures the fundamental competing sources of political legitimacy in democratic discourse.

**Applications**: Political legitimacy analysis, democratic discourse assessment, comparative political communication studies, worldview mapping in political texts.

---

## Framework Dimensions

### **Identity-Based Legitimacy**

#### Immutable-Identity Politics (0.0-1.0)
**Definition**: Politics that centers moral status on overlapping, unchosen personal attributes.
**Key Markers**: "As Black women, we," "Center disabled queer voices," "Our lived experience as trans people," "Marginalized identities face systemic barriers," "systemic oppression," "lived experience," "intersection of race and gender"

### **Dominance-Based Legitimacy**

#### Tribal Domination (0.0-1.0)
**Definition**: Politics that asserts the legitimacy of an in-group's supremacy over out-groups.
**Key Markers**: "We must put our nation first," "They will replace us," "Only our tribe can secure the future," "Our way of life is under threat," "take back our country," "real patriots," "dominant culture"

### **Universal Dignity Legitimacy**

#### Pluralist Individual Dignity (0.0-1.0)
**Definition**: Politics that locates legitimacy in the transcendent dignity and agency of each person.
**Key Markers**: "Every individual deserves equal voice," "Citizens, regardless of background, share responsibility," "Human dignity transcends race and class," "universal rights," "shared civic space," "common good through consent"

---

## Gasket Architecture

### Raw Analysis Log Format
The analysis agent outputs a raw analysis log containing:
- Worldview dimension scores for all 3 dimensions
- Salience weights for each dimension
- Evidence quotes with confidence ratings
- Dominant worldview identification
- Qualitative reasoning about political legitimacy patterns

### Intelligent Extractor Schema
```json
{
  "gasket_schema": {
    "target_keys": [
      "immutable_identity_politics_score",
      "tribal_domination_score",
      "pluralist_individual_dignity_score",
      "immutable_identity_politics_salience",
      "tribal_domination_salience",
      "pluralist_individual_dignity_salience",
      "immutable_identity_politics_confidence",
      "tribal_domination_confidence",
      "pluralist_individual_dignity_confidence"
    ]
  }
}
```

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "political_worldview_triad_v7_1",
  "version": "v7.3",
  "display_name": "Political Worldview Triad Framework v7.3",
  "analysis_variants": {
    "default": {
      "description": "Complete triadic worldview analysis across all three political legitimacy sources with raw analysis log output.",
      "analysis_prompt": "You are an expert analyst specializing in political worldview analysis and democratic legitimacy frameworks across diverse contexts. Your task is to analyze the provided text using the Political Worldview Triad Framework v7.3, which captures competing sources of political legitimacy with enhanced metadata scoring and identifies fundamental value structures in political communication.\n\nThe framework evaluates discourse across three competing sources of political legitimacy:\n\n**Immutable-Identity Politics** (0.0-1.0): Politics that centers moral status on overlapping, unchosen personal attributes, with markers like 'As Black women, we,' 'Center disabled queer voices,' 'Our lived experience,' 'systemic oppression,' 'marginalized identities.'\n\n**Tribal Domination** (0.0-1.0): Politics that asserts the legitimacy of an in-group's supremacy over out-groups, with markers like 'We must put our nation first,' 'They will replace us,' 'take back our country,' 'real patriots,' 'dominant culture.'\n\n**Pluralist Individual Dignity** (0.0-1.0): Politics that locates legitimacy in the transcendent dignity and agency of each person, with markers like 'Every individual deserves equal voice,' 'Human dignity transcends race and class,' 'universal rights,' 'shared civic space.'\n\nFor each dimension, provide:\n- **Score (0.0-1.0)**: Based on strength of evidence in the text\n- **Salience (0.0-1.0)**: How central is this dimension to this specific text?\n- **Confidence (0.0-1.0)**: How certain are you in this assessment?\n\nWrite a comprehensive analytical report that covers:\n- Application of the Political Worldview Triad methodology to this specific text\n- Detailed analysis of each worldview dimension with scores, salience, confidence, and evidence\n- Assessment of competing legitimacy sources and value structure patterns\n- Overall worldview profile with identification of dominant legitimacy framework\n- Key insights about the speaker's approach to political legitimacy and moral authority\n\nEmbed your numerical assessments naturally within the analysis. For example: 'This text demonstrates strong pluralist individual dignity (pluralist individual dignity score: 0.8, salience: 0.9, confidence: 0.7) with frequent appeals to universal human dignity.' Focus on rigorous intellectual analysis supported by direct textual evidence and clear reasoning for all scores and metadata."
    }
  },
  "dimension_groups": {
    "political_legitimacy_sources": ["immutable_identity_politics", "tribal_domination", "pluralist_individual_dignity"]
  },
  "calculation_spec": {
    "worldview_legitimacy_index": "(immutable_identity_politics_score + tribal_domination_score + pluralist_individual_dignity_score) / 3",
    "dominant_worldview": "argmax(immutable_identity_politics_score, tribal_domination_score, pluralist_individual_dignity_score)"
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
      "immutable_identity_politics_score",
      "tribal_domination_score",
      "pluralist_individual_dignity_score",
      "immutable_identity_politics_salience",
      "tribal_domination_salience",
      "pluralist_individual_dignity_salience",
      "immutable_identity_politics_confidence",
      "tribal_domination_confidence",
      "pluralist_individual_dignity_confidence"
    ],
    "extraction_patterns": {
      "immutable_identity_politics_score": ["immutable.{0,20}identity.{0,20}politics.{0,20}score", "identity.{0,20}politics.{0,20}rating", "identity\\s*politics\\s*:\\s*[0-9]"],
      "tribal_domination_score": ["tribal.{0,20}domination.{0,20}score", "tribal.{0,20}domination.{0,20}rating", "tribal\\s*domination\\s*:\\s*[0-9]"],
      "pluralist_individual_dignity_score": ["pluralist.{0,20}individual.{0,20}dignity.{0,20}score", "individual.{0,20}dignity.{0,20}rating", "individual\\s*dignity\\s*:\\s*[0-9]"],
      "immutable_identity_politics_salience": ["immutable.{0,20}identity.{0,20}politics.{0,20}salience", "identity.{0,20}politics.{0,20}importance", "identity.{0,20}politics.{0,20}centrality"],
      "tribal_domination_salience": ["tribal.{0,20}domination.{0,20}salience", "tribal.{0,20}domination.{0,20}importance", "domination.{0,20}centrality"],
      "pluralist_individual_dignity_salience": ["pluralist.{0,20}individual.{0,20}dignity.{0,20}salience", "individual.{0,20}dignity.{0,20}importance", "individual.{0,20}dignity.{0,20}centrality"],
      "immutable_identity_politics_confidence": ["immutable.{0,20}identity.{0,20}politics.{0,20}confidence", "identity.{0,20}politics.{0,20}certainty", "identity.{0,20}politics.{0,20}sure"],
      "tribal_domination_confidence": ["tribal.{0,20}domination.{0,20}confidence", "tribal.{0,20}domination.{0,20}certainty", "domination.{0,20}sure"],
      "pluralist_individual_dignity_confidence": ["pluralist.{0,20}individual.{0,20}dignity.{0,20}confidence", "individual.{0,20}dignity.{0,20}certainty", "individual.{0,20}dignity.{0,20}sure"]
    },
    "validation_rules": {
      "required_fields": [
        "immutable_identity_politics_score", "tribal_domination_score", "pluralist_individual_dignity_score"
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