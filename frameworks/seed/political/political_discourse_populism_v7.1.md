# Political Discourse Analysis Framework v7.1 - Populism Emergence Study

**Version**: 7.1  
**Status**: Active  
**Major Change**: Enhanced Gasket Schema with Metadata Scores and Advanced Extraction Patterns

A specialized Discernus framework for analyzing the emergence and evolution of populist discourse in American presidential rhetoric. This framework employs a sophisticated two-axis model to capture the fundamental tensions in democratic political discourse: the vertical Populism↔Pluralism axis examining people versus institutions, and the horizontal Nationalism↔Patriotism axis examining ethnic versus civic identity.

## Framework Innovation

This framework resolves the "Bolsonaro Problem" where traditional single-axis models failed to capture simultaneous high populism and high nationalism. The orthogonal architecture eliminates conceptual crowding-out effects, enabling precise measurement of populist discourse evolution across different presidential administrations.

## Core Analysis Dimensions

### **Populism-Pluralism Axis (Vertical Dimension)**

**Populism (High Score: 0.7-1.0)**: Direct popular sovereignty, anti-elite sentiment, Manichaean worldview

**Enhanced Linguistic Markers** (inspired by PDAF):
- **Core Populist Appeals**: "the people," "ordinary Americans," "working families," "forgotten Americans," "real Americans"
- **Anti-Elite Language**: "establishment," "elites," "corrupt politicians," "Washington insiders," "special interests," "swamp"
- **Manichaean Framing**: "us versus them," "good versus evil," "pure people versus corrupt elite"
- **Direct Democracy Appeals**: "will of the people," "voice of the people," "people's choice," "popular mandate"
- **Economic Populism**: "rigged system," "unfair trade," "economic nationalism," "America First economics"
- **Cultural Populism**: "common sense," "traditional values," "heartland," "main street versus Wall Street"

**Pluralism (Low Score: 0.0-0.3)**: Institutional mediation, diverse representation, expert knowledge

**Enhanced Linguistic Markers**:
- **Institutional Respect**: "democratic institutions," "constitutional process," "checks and balances," "rule of law"
- **Expert Deference**: "evidence-based," "scientific consensus," "expert analysis," "data-driven decisions"
- **Stakeholder Inclusion**: "diverse perspectives," "stakeholder input," "broad coalition," "inclusive democracy"
- **Procedural Norms**: "due process," "constitutional principles," "democratic norms," "institutional integrity"
- **Compromise Language**: "bipartisan cooperation," "finding common ground," "working across the aisle"
- **Technocratic Appeals**: "policy expertise," "professional judgment," "administrative competence"

### **Nationalism-Patriotism Axis (Horizontal Dimension)**

**Nationalism (High Score: 0.7-1.0)**: Ethnic/cultural identity emphasis, national supremacy claims

**Enhanced Linguistic Markers**:
- **Cultural Supremacy**: "American greatness," "exceptional nation," "greatest country," "superior civilization"
- **Ethnic Identity**: "our people," "real Americans," "American stock," "heritage Americans," "blood and soil"
- **Cultural Purity**: "traditional culture," "American way of life," "cultural heritage," "ancestral values"
- **Foreign Threat**: "foreign influence," "cultural invasion," "demographic replacement," "alien values"
- **Territorial Claims**: "homeland," "native soil," "ancestral territory," "rightful place"
- **Historical Mythology**: "founding fathers' vision," "original America," "true American spirit"

**Patriotism (Low Score: 0.0-0.3)**: Civic attachment to political institutions and constitutional values

**Enhanced Linguistic Markers**:
- **Constitutional Devotion**: "Constitution," "Bill of Rights," "constitutional democracy," "founding principles"
- **Civic Duty**: "civic responsibility," "democratic participation," "citizen engagement," "public service"
- **Institutional Pride**: "democratic institutions," "system of government," "peaceful transfer of power"
- **Universal Rights**: "equal justice," "civil rights," "human dignity," "equal protection"
- **Inclusive Citizenship**: "nation of immigrants," "diverse democracy," "American dream for all"
- **Service Ideals**: "public service," "duty to country," "sacrifice for democracy," "serving the people"

## Quadrant Classification System

**High Populism + High Nationalism (0.7+ both axes)**: Ethno-Populist Discourse
**High Populism + Low Nationalism (0.7+ vertical, 0.3- horizontal)**: Civic Populist Discourse  
**Low Populism + High Nationalism (0.3- vertical, 0.7+ horizontal)**: Elite Nationalist Discourse
**Low Populism + Low Nationalism (0.3- both axes)**: Liberal Democratic Discourse

## Longitudinal Analysis Capabilities

This framework is optimized for temporal analysis of populist discourse emergence, enabling:
- **Trend Detection**: Measuring populist rhetoric evolution across presidential terms
- **Shift Point Identification**: Detecting critical moments in populist discourse adoption
- **Cross-Administration Comparison**: Comparing populist tendencies across different presidencies
- **Contextual Variation**: Analyzing populist discourse differences between speech types

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "political_discourse_populism_v7_1",
  "version": "v7.1",
  "display_name": "Political Discourse Analysis Framework v7.1 - Populism Emergence Study",
  "analysis_variants": {
    "default": {
      "description": "Complete two-axis populism-pluralism analysis with raw analysis log output.",
      "analysis_prompt": "Phase 1: Cognitive Priming: You are an expert analyst of political discourse with deep knowledge of populist rhetoric, democratic theory, and American political communication across diverse contexts. Phase 2: Framework Methodology: Your task is to analyze the text using the Political Discourse Analysis Framework v7.1, which measures populist discourse emergence through two orthogonal axes with enhanced metadata scoring. Phase 3: Operational Definitions: Evaluate the POPULISM-PLURALISM AXIS (0.0-1.0): populist markers ('the people,' 'establishment,' 'elites,' 'us versus them,' 'rigged system') versus pluralist markers ('democratic institutions,' 'evidence-based,' 'diverse perspectives,' 'bipartisan cooperation'). Evaluate the NATIONALISM-PATRIOTISM AXIS (0.0-1.0): nationalist markers ('American greatness,' 'real Americans,' 'traditional culture,' 'foreign influence') versus patriotic markers ('Constitution,' 'civic responsibility,' 'equal justice,' 'nation of immigrants'). Phase 4: Scoring Protocol: For each axis, provide ONLY: (1) score (0.0-1.0), (2) salience (0.0-1.0), (3) confidence (0.0-1.0), (4) evidence quotes with justification. Phase 5: Raw Analysis Log Requirements: Your response must be a raw analysis log containing axis scores, evidence, and reasoning - NO JSON structure or derived calculations. Phase 6: Output Specification: Return raw analysis log with axis scores only - NO quadrant calculations or derived metrics (these will be computed by code)."
    },
    "longitudinal_analysis": {
      "description": "Specialized temporal analysis for populism evolution with raw analysis log output.",
      "analysis_prompt": "Phase 1: Cognitive Priming: You are conducting longitudinal analysis of populist discourse evolution in American presidential rhetoric with expertise in temporal political communication patterns. Phase 2: Framework Methodology: Your task is to analyze populist discourse emergence using the Political Discourse Analysis Framework v7.1 with focus on temporal indicators. Phase 3: Operational Definitions: Focus on temporal indicators of populist emergence, institutional critique patterns, and anti-elite sentiment development across the two orthogonal axes. Phase 4: Scoring Protocol: Score both axes with attention to historical context and populist discourse evolution, providing scores, salience, and confidence with temporal evidence. Phase 5: Raw Analysis Log Requirements: Your response must be a raw analysis log focusing on populism emergence patterns - NO JSON structure or derived calculations. Phase 6: Output Specification: Return raw analysis log with axis scores only - NO quadrant calculations or longitudinal metrics (these will be computed by code)."
    }
  },
  "dimension_groups": {
    "vertical_axis": ["populism_indicators", "pluralism_indicators"],
    "horizontal_axis": ["nationalism_indicators", "patriotism_indicators"],
    "populist_discourse_markers": ["anti_elite_sentiment", "people_versus_establishment", "manichaean_framing"],
    "democratic_discourse_markers": ["institutional_respect", "pluralist_inclusion", "constitutional_reverence"]
  },
  "calculation_spec": {
    "populism_pluralism_score": "Vertical axis score measuring populist versus pluralist discourse (0.0 = pure pluralism, 1.0 = pure populism)",
    "nationalism_patriotism_score": "Horizontal axis score measuring nationalist versus patriotic discourse (0.0 = pure patriotism, 1.0 = pure nationalism)",
    "populist_intensity_index": "(populism_pluralism_axis_score * 0.7) + (nationalism_patriotism_axis_score * 0.3)",
    "democratic_institutionalism_index": "((1 - populism_pluralism_axis_score) * 0.7) + ((1 - nationalism_patriotism_axis_score) * 0.3)",
    "quadrant_classification": "Determine based on axis thresholds: High Populism + High Nationalism (0.7+ both), Civic Populist (0.7+ vertical, 0.3- horizontal), Elite Nationalist (0.3- vertical, 0.7+ horizontal), Liberal Democratic (0.3- both)"
  },
  "reliability_rubric": {
    "cronbachs_alpha": {
      "excellent": [0.80, 1.0],
      "good": [0.70, 0.79],
      "acceptable": [0.60, 0.69],
      "poor": [0.0, 0.59]
    },
    "notes": "Defines quality thresholds for framework reliability in longitudinal populism studies."
  },
  "gasket_schema": {
    "version": "7.1",
    "extraction_method": "intelligent_extractor",
    "target_keys": [
      "populism_pluralism_axis_score",
      "nationalism_patriotism_axis_score",
      "populism_pluralism_axis_salience",
      "nationalism_patriotism_axis_salience",
      "populism_pluralism_axis_confidence",
      "nationalism_patriotism_axis_confidence"
    ],
    "extraction_patterns": {
      "populism_pluralism_axis_score": ["populism.{0,20}pluralism.{0,20}axis.{0,20}score", "populism.{0,20}axis.{0,20}score", "vertical.{0,20}axis.{0,20}score"],
      "nationalism_patriotism_axis_score": ["nationalism.{0,20}patriotism.{0,20}axis.{0,20}score", "nationalism.{0,20}axis.{0,20}score", "horizontal.{0,20}axis.{0,20}score"],
      "populism_pluralism_axis_salience": ["populism.{0,20}pluralism.{0,20}axis.{0,20}salience", "populism.{0,20}axis.{0,20}salience", "vertical.{0,20}axis.{0,20}salience"],
      "nationalism_patriotism_axis_salience": ["nationalism.{0,20}patriotism.{0,20}axis.{0,20}salience", "nationalism.{0,20}axis.{0,20}salience", "horizontal.{0,20}axis.{0,20}salience"],
      "populism_pluralism_axis_confidence": ["populism.{0,20}pluralism.{0,20}axis.{0,20}confidence", "populism.{0,20}axis.{0,20}confidence", "vertical.{0,20}axis.{0,20}confidence"],
      "nationalism_patriotism_axis_confidence": ["nationalism.{0,20}patriotism.{0,20}axis.{0,20}confidence", "nationalism.{0,20}axis.{0,20}confidence", "horizontal.{0,20}axis.{0,20}confidence"]
    },
    "validation_rules": {
      "required_fields": [
        "populism_pluralism_axis_score", "nationalism_patriotism_axis_score"
      ],
      "score_ranges": {"min": 0.0, "max": 1.0},
      "metadata_ranges": {
        "salience": {"min": 0.0, "max": 1.0},
        "confidence": {"min": 0.0, "max": 1.0}
      },
      "fallback_strategy": "use_default_values"
    }
  },
  "raw_analysis_log_format": {
    "description": "Raw analysis log containing axis scores, evidence, and reasoning without structured JSON",
    "content": "Free-form text with populism-pluralism analysis including scores, evidence quotes, and qualitative reasoning"
  }
}
```

</details>