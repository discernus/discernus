# Individual Dignity Identity v Tribal Identity v7.3

**Version**: 7.3  
**Status**: Active  
**Major Change**: Enhanced Gasket Schema with Metadata Scores and Advanced Extraction Patterns

---

## Overview

The IDITI (Individual Dignity Identity v Tribal Identity) Framework v7.3 analyzes the fundamental tension between individual dignity and tribal identity in political discourse with enhanced metadata scoring. This specialized framework examines how texts either affirm universal human worth or prioritize group-based identity and loyalty, revealing the core moral question of whether human dignity is universal or conditional on group membership.

**Purpose**: Analyzes the dignity vs. tribalism axis in political and ethical discourse with enhanced extraction patterns and validation rules for comprehensive identity assessment.

**Innovation**: Philosophical framework examining whether human dignity is treated as universal (dignity) or conditional on group membership (tribalism).

**Applications**: Ethics analysis, identity politics assessment, democratic discourse evaluation, moral philosophy studies.

---

## Framework Dimensions

### **Universal Dignity Emphasis**

#### Dignity (0.0-1.0)
**Definition**: Affirms individual moral worth and universal rights, regardless of group identity.
**Key Markers**: "equal dignity," "inherent worth," "regardless of background," "individual character," "universal rights," "human agency," "personal dignity," "individual merit," "common humanity," "respect for all," "universal values," "cross-group solidarity," "individual autonomy," "character-based judgment"

### **Group-Based Identity Emphasis**

#### Tribalism (0.0-1.0)
**Definition**: Prioritizes group dominance, loyalty, or identity over individual agency.
**Key Markers**: "real Americans," "our people," "they don't belong," "us vs them," "group loyalty," "identity politics," "blood and soil," "true believers," "outsiders," "not one of us," "tribal unity," "group supremacy," "in-group favoritism," "group-based hierarchy," "exclusion markers"

---

## Gasket Architecture

### Raw Analysis Log Format
The analysis agent outputs a raw analysis log containing:
- Dignity and tribalism dimension scores
- Salience weights for each dimension
- Evidence quotes with confidence ratings
- Qualitative reasoning about identity formation patterns

### Intelligent Extractor Schema
```json
{
  "gasket_schema": {
    "target_keys": [
      "dignity_score",
      "tribalism_score",
      "dignity_salience",
      "tribalism_salience",
      "dignity_confidence",
      "tribalism_confidence"
    ]
  }
}
```

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "iditi_v7_1",
  "version": "v7.3",
  "display_name": "Individual Dignity Identity v Tribal Identity v7.3",
  "analysis_variants": {
    "default": {
      "description": "Sequential dignity vs tribalism analysis with chain-of-thought methodology",
      "analysis_prompt": "You are an expert analyst specializing in political and ethical discourse analysis across diverse contexts. Analyze this text through focused sequential steps, examining the dignity-tribalism tension systematically before integration.\n\nSTEP 1 - DIGNITY DIMENSION ANALYSIS\nFocus ONLY on individual dignity patterns (ignore tribalism for now):\n- Look for dignity patterns: universal worth language ('equal dignity,' 'inherent worth,' 'regardless of background,' 'individual character'), rights emphasis ('universal rights,' 'human agency,' 'personal dignity'), inclusive humanity ('common humanity,' 'universal values,' 'cross-group solidarity') - Note: These are semantic concepts, look for affirmation of individual moral worth and universal rights regardless of group identity, not just these exact phrases\n- Assess dignity completeness and universality claims\n- Score dignity dimension (0.0-1.0) with specific textual evidence\n- Assess salience (0.0-1.0): How central are dignity appeals to the overall message?\n- State confidence (0.0-1.0): How certain are you in this assessment?\nShow your analytical work and evidence before proceeding.\n\nSTEP 2 - TRIBALISM DIMENSION ANALYSIS\nNow focus ONLY on tribal identity patterns:\n- Look for tribalism patterns: group identity language ('real Americans,' 'our people,' 'they don't belong,' 'us vs them'), loyalty emphasis ('group loyalty,' 'identity politics,' 'true believers'), exclusion markers ('outsiders,' 'not one of us,' 'tribal unity,' 'group supremacy,' 'in-group favoritism') - Note: These are semantic concepts, look for prioritizing group dominance, loyalty, or identity over individual agency, not just these exact terms\n- Assess tribalism intensity and exclusionary logic\n- Score tribalism dimension (0.0-1.0) with specific textual evidence\n- Assess salience (0.0-1.0): How central are tribal identity appeals to the message?\n- State confidence (0.0-1.0): How certain are you in this assessment?\nShow your analytical work and evidence before proceeding.\n\nFINAL STEP - INTEGRATION AND VALIDATION\nReview your step-by-step analysis:\n- Check for scoring consistency between dignity and tribalism dimensions\n- Validate that evidence quality meets academic standards\n- Assess the fundamental tension between individual dignity and tribal identity\n- Confirm confidence levels are appropriately calibrated\n- Determine whether human dignity is treated as universal or conditional on group membership\n- Apply pattern classifications based on overall identity approach\n\nProvide your final structured analysis following this format:\n\n**IDENTITY FORMATION ASSESSMENT**\n\n**Dignity**: [score] (salience: [score], confidence: [score])\n**Tribalism**: [score] (salience: [score], confidence: [score])\n\n**Calculated Metrics**:\n- Identity Tension Index: [calculated score]\n- Human Worth Universality: [universal/conditional classification]\n\n**Key Insights**: [Summary of identity formation patterns, dignity-tribalism tension, and approach to human worth and group identity]"
    }
  },
  "dimension_groups": {
    "identity_axis": ["dignity", "tribalism"]
  },
  "calculation_spec": {
    "identity_axis_score": "(dignity_score - tribalism_score + 1) / 2",
    "dignity_tribalism_index": "(dignity_score + tribalism_score) / 2",
    "salience_weighted_identity_axis_score": "((dignity_score * dignity_salience) - (tribalism_score * tribalism_salience) + (dignity_salience + tribalism_salience + 1e-9) / 2) / (dignity_salience + tribalism_salience + 1e-9)",
    "salience_weighted_dignity_tribalism_index": "(dignity_score * dignity_salience + tribalism_score * tribalism_salience) / (dignity_salience + tribalism_salience + 1e-9)"
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
    "version": "v7.3",
    "extraction_method": "intelligent_extractor",
    "target_keys": [
      "dignity_score", "tribalism_score", "dignity_salience", "tribalism_salience", "dignity_confidence", "tribalism_confidence"
    ],
    "extraction_patterns": {
      "dignity_score": ["dignity.*?score.*?([0-9]\\.[0-9])", "dignity.*?([0-9]\\.[0-9])", "dignity\\s*:\\s*([0-9]\\.[0-9])"],
      "tribalism_score": ["tribalism.*?score.*?([0-9]\\.[0-9])", "tribalism.*?([0-9]\\.[0-9])", "tribalism\\s*:\\s*([0-9]\\.[0-9])"]
    },
    "validation_rules": {
      "required_fields": [
        "dignity_score", "tribalism_score"
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