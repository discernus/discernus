# Political Discourse Two-Axis Analysis v7.3

**Version**: 7.1  
**Status**: Active  
**Major Change**: Enhanced Gasket Schema with Metadata Scores and Advanced Extraction Patterns

---

## Overview

The Political Discourse Two-Axis Analysis v7.3 represents a revolutionary framework that resolves fundamental conceptual overlap problems in traditional competitive political models. This enhanced version uses orthogonal axes to capture core tensions in democratic political discourse without crowding-out effects, now with advanced metadata scoring for robust analysis.

**Purpose**: Analyzes political discourse using two independent orthogonal dimensions with enhanced extraction patterns and validation rules for comprehensive political positioning assessment.

**Innovation**: Two-axis orthogonal architecture eliminates the "Bolsonaro Problem" where traditional frameworks failed to accurately capture high populism and high nationalism simultaneously.

**Applications**: Political positioning analysis, democratic discourse assessment, comparative political communication studies, electoral strategy analysis.

---

## Framework Dimensions

### **Vertical Axis: Populism ↔ Pluralism**

#### Populism (0.0-1.0)
**Definition**: Direct popular sovereignty, anti-elite sentiment, Manichaean worldview.
**Key Markers**: "the people," "corrupt elite," "establishment," "will of the people," "us versus them," "drain the swamp," "real Americans/citizens," "ordinary people"

#### Pluralism (0.0-1.0)
**Definition**: Institutional mediation, diverse representation, expert knowledge.
**Key Markers**: "institutions," "experts," "diverse perspectives," "democratic process," "checks and balances," "constitutional principles," "stakeholder input," "evidence-based"

### **Horizontal Axis: Nationalism ↔ Patriotism**

#### Nationalism (0.0-1.0)
**Definition**: Ethnic/cultural identity emphasis, national supremacy claims.
**Key Markers**: "our people," "national greatness," "cultural heritage," "traditional values," "foreign influence," "national identity," "cultural purity," "ancestral homeland"

#### Patriotism (0.0-1.0)
**Definition**: Civic attachment to political institutions and constitutional values.
**Key Markers**: "constitution," "democratic values," "rule of law," "civic duty," "constitutional rights," "democratic institutions," "equal justice," "civic participation"

---

## Gasket Architecture

### Raw Analysis Log Format
The analysis agent outputs a raw analysis log containing:
- Vertical axis (populism-pluralism) and horizontal axis (nationalism-patriotism) scores
- Salience weights for each axis
- Evidence quotes with confidence ratings
- Quadrant classification based on axis intersection
- Qualitative reasoning about political positioning patterns

### Intelligent Extractor Schema
```json
{
  "gasket_schema": {
    "target_keys": [
      "vertical_axis_score",
      "horizontal_axis_score",
      "populism_score",
      "pluralism_score", 
      "nationalism_score",
      "patriotism_score",
      "vertical_axis_salience",
      "horizontal_axis_salience",
      "populism_salience",
      "pluralism_salience",
      "nationalism_salience", 
      "patriotism_salience",
      "vertical_axis_confidence",
      "horizontal_axis_confidence",
      "populism_confidence",
      "pluralism_confidence",
      "nationalism_confidence",
      "patriotism_confidence"
    ]
  }
}
```

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "political_discourse_two_axis_v7_1",
  "version": "v7.3",
  "display_name": "Political Discourse Two-Axis Analysis v7.3",
  "analysis_variants": {
    "default": {
      "description": "Sequential two-axis political discourse analysis with chain-of-thought methodology",
      "analysis_prompt": "You are an expert analyst specializing in political discourse analysis and democratic communication patterns across diverse contexts. Analyze this text through focused sequential steps, examining each political axis independently before integration.\n\nSTEP 1 - VERTICAL AXIS ANALYSIS (POPULISM ↔ PLURALISM)\nFocus ONLY on vertical axis patterns (ignore horizontal axis for now):\n- Look for populism patterns: direct popular sovereignty ('the people,' 'will of the people,' 'people's voice'), anti-elite sentiment ('corrupt elite,' 'establishment,' 'out of touch elites'), Manichaean worldview ('us versus them,' 'good versus evil,' 'pure people versus corrupt elite') - Note: These are semantic concepts, look for direct popular sovereignty and anti-elite sentiment, not just these exact phrases\n- Look for pluralism patterns: institutional mediation ('institutions,' 'democratic processes,' 'constitutional framework'), diverse representation ('experts,' 'diverse perspectives,' 'multiple viewpoints'), knowledge-based governance ('evidence-based,' 'expert knowledge,' 'careful deliberation') - Note: These are semantic concepts, look for institutional mediation and expert-based governance, not just these exact terms\n- Score populism dimension (0.0-1.0) with specific textual evidence\n- Score pluralism dimension (0.0-1.0) with specific textual evidence\n- Assess salience (0.0-1.0): How central are vertical axis appeals to the overall message?\n- State confidence (0.0-1.0): How certain are you in this assessment?\nShow your analytical work and evidence before proceeding.\n\nSTEP 2 - HORIZONTAL AXIS ANALYSIS (NATIONALISM ↔ PATRIOTISM)\nNow focus ONLY on horizontal axis patterns:\n- Look for nationalism patterns: ethnic/cultural identity ('our people,' 'our culture,' 'our heritage'), national supremacy ('national greatness,' 'superior nation,' 'dominant culture'), cultural emphasis ('cultural heritage,' 'traditional values,' 'authentic identity') - Note: These are semantic concepts, look for ethnic/cultural identity emphasis and national supremacy claims, not just these exact expressions\n- Look for patriotism patterns: civic attachment ('constitution,' 'democratic institutions,' 'rule of law'), constitutional values ('democratic values,' 'constitutional principles,' 'civic responsibility'), institutional loyalty ('respect for institutions,' 'democratic norms,' 'constitutional order') - Note: These are semantic concepts, look for civic attachment to political institutions and constitutional values, not just these exact principles\n- Score nationalism dimension (0.0-1.0) with specific textual evidence\n- Score patriotism dimension (0.0-1.0) with specific textual evidence\n- Assess salience (0.0-1.0): How central are horizontal axis appeals to the message?\n- State confidence (0.0-1.0): How certain are you in this assessment?\nShow your analytical work and evidence before proceeding.\n\nFINAL STEP - INTEGRATION AND VALIDATION\nReview your step-by-step analysis:\n- Check for scoring consistency across both political axes\n- Validate that evidence quality meets academic standards\n- Assess political positioning patterns and orthogonal axis dynamics\n- Confirm confidence levels are appropriately calibrated\n- Map overall political discourse profile with quadrant classification\n- Apply pattern classifications based on axis combinations\n\nProvide your final structured analysis following this format:\n\n**POLITICAL DISCOURSE ASSESSMENT**\n\n**Vertical Axis**: Populism [score]/Pluralism [score] (salience: [score], confidence: [score])\n**Horizontal Axis**: Nationalism [score]/Patriotism [score] (salience: [score], confidence: [score])\n\n**Calculated Metrics**:\n- Political Positioning: [quadrant classification]\n- Democratic Authority Profile: [populist/pluralist orientation]\n- National Identity Profile: [nationalist/patriotic orientation]\n\n**Key Insights**: [Summary of political positioning, axis dynamics, and approach to political legitimacy and identity]"
    }
  },
  "dimension_groups": {
    "vertical_axis": ["populism", "pluralism"],
    "horizontal_axis": ["nationalism", "patriotism"]
  },
  "calculation_spec": {
    "vertical_axis_score": "(populism_score - pluralism_score + 1) / 2",
    "horizontal_axis_score": "(nationalism_score - patriotism_score + 1) / 2",
    "political_discourse_index": "sqrt(vertical_axis_score^2 + horizontal_axis_score^2) / sqrt(2)"
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
      "vertical_axis_score",
      "horizontal_axis_score",
      "populism_score",
      "pluralism_score",
      "nationalism_score",
      "patriotism_score",
      "vertical_axis_salience",
      "horizontal_axis_salience",
      "populism_salience",
      "pluralism_salience",
      "nationalism_salience",
      "patriotism_salience",
      "vertical_axis_confidence",
      "horizontal_axis_confidence",
      "populism_confidence",
      "pluralism_confidence",
      "nationalism_confidence",
      "patriotism_confidence"
    ],
    "extraction_patterns": {
      "vertical_axis_score": ["vertical.{0,20}axis.{0,20}score", "vertical.{0,20}axis.{0,20}rating", "vertical\\s*axis\\s*:\\s*[0-9]"],
      "horizontal_axis_score": ["horizontal.{0,20}axis.{0,20}score", "horizontal.{0,20}axis.{0,20}rating", "horizontal\\s*axis\\s*:\\s*[0-9]"],
      "populism_score": ["populism.{0,20}score", "populism.{0,20}rating", "populism\\s*:\\s*[0-9]"],
      "pluralism_score": ["pluralism.{0,20}score", "pluralism.{0,20}rating", "pluralism\\s*:\\s*[0-9]"],
      "nationalism_score": ["nationalism.{0,20}score", "nationalism.{0,20}rating", "nationalism\\s*:\\s*[0-9]"],
      "patriotism_score": ["patriotism.{0,20}score", "patriotism.{0,20}rating", "patriotism\\s*:\\s*[0-9]"],
      "vertical_axis_salience": ["vertical.{0,20}axis.{0,20}salience", "vertical.{0,20}axis.{0,20}importance", "populism.{0,20}pluralism.{0,20}centrality"],
      "horizontal_axis_salience": ["horizontal.{0,20}axis.{0,20}salience", "horizontal.{0,20}axis.{0,20}importance", "nationalism.{0,20}patriotism.{0,20}centrality"],
      "populism_salience": ["populism.{0,20}salience", "populism.{0,20}importance", "populism.{0,20}centrality"],
      "pluralism_salience": ["pluralism.{0,20}salience", "pluralism.{0,20}importance", "pluralism.{0,20}centrality"],
      "nationalism_salience": ["nationalism.{0,20}salience", "nationalism.{0,20}importance", "nationalism.{0,20}centrality"],
      "patriotism_salience": ["patriotism.{0,20}salience", "patriotism.{0,20}importance", "patriotism.{0,20}centrality"],
      "vertical_axis_confidence": ["vertical.{0,20}axis.{0,20}confidence", "vertical.{0,20}axis.{0,20}certainty", "populism.{0,20}pluralism.{0,20}sure"],
      "horizontal_axis_confidence": ["horizontal.{0,20}axis.{0,20}confidence", "horizontal.{0,20}axis.{0,20}certainty", "nationalism.{0,20}patriotism.{0,20}sure"],
      "populism_confidence": ["populism.{0,20}confidence", "populism.{0,20}certainty", "populism.{0,20}sure"],
      "pluralism_confidence": ["pluralism.{0,20}confidence", "pluralism.{0,20}certainty", "pluralism.{0,20}sure"],
      "nationalism_confidence": ["nationalism.{0,20}confidence", "nationalism.{0,20}certainty", "nationalism.{0,20}sure"],
      "patriotism_confidence": ["patriotism.{0,20}confidence", "patriotism.{0,20}certainty", "patriotism.{0,20}sure"]
    },
    "validation_rules": {
      "required_fields": [
        "vertical_axis_score", "horizontal_axis_score", "populism_score", "pluralism_score", "nationalism_score", "patriotism_score"
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