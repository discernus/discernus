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
      "analysis_prompt": "You are an expert analyst of political discourse with deep knowledge of populist rhetoric, democratic theory, and American political communication across diverse contexts. Your task is to analyze the provided text using the Political Discourse Analysis Framework v7.1, which measures populist discourse emergence through two orthogonal axes with enhanced metadata scoring and longitudinal analysis capabilities.\n\nThe framework evaluates discourse across two key axes:\n\n**Populism-Pluralism Axis (Vertical Dimension)** (0.0-1.0): Measures the tension between populist direct popular sovereignty appeals versus pluralist institutional mediation approaches. Populist markers include 'the people,' 'establishment,' 'elites,' 'us versus them,' 'rigged system,' while pluralist markers include 'democratic institutions,' 'evidence-based,' 'diverse perspectives,' 'bipartisan cooperation.'\n\n**Nationalism-Patriotism Axis (Horizontal Dimension)** (0.0-1.0): Measures the tension between nationalist ethnic/cultural identity emphasis versus patriotic civic attachment to political institutions. Nationalist markers include 'American greatness,' 'real Americans,' 'traditional culture,' 'foreign influence,' while patriotic markers include 'Constitution,' 'civic responsibility,' 'equal justice,' 'nation of immigrants.'\n\nFor each axis, provide:\n- **Score (0.0-1.0)**: Based on strength of evidence in the text\n- **Salience (0.0-1.0)**: How central is this axis to this specific text?\n- **Confidence (0.0-1.0)**: How certain are you in this assessment?\n\nWrite a comprehensive analytical report that covers:\n- Application of the Political Discourse Analysis methodology to this specific text\n- Detailed analysis of each axis with scores, salience, confidence, and evidence\n- Assessment of populist discourse emergence patterns and democratic authority tensions\n- Overall discourse profile across both orthogonal axes with salience weighting\n- Key insights about the speaker's approach to democratic authority and national identity\n\nEmbed your numerical assessments naturally within the analysis. For example: 'This text demonstrates strong populism-pluralism axis activity (populism-pluralism axis score: 0.8, salience: 0.9, confidence: 0.7) with clear establishment versus people framing.' Focus on rigorous intellectual analysis supported by direct textual evidence and clear reasoning for all scores and metadata."
    },
    "longitudinal_analysis": {
      "description": "Specialized temporal analysis for populism evolution with raw analysis log output.",
      "analysis_prompt": "You are conducting longitudinal analysis of populist discourse evolution in American presidential rhetoric with expertise in temporal political communication patterns. Your task is to analyze populist discourse emergence using the Political Discourse Analysis Framework v7.1 with focus on temporal indicators and historical context of populist rhetorical development.\n\nFocus your analysis on temporal indicators of populist emergence, institutional critique patterns, and anti-elite sentiment development across the two orthogonal axes. Pay particular attention to historical context and populist discourse evolution patterns that reveal shifts in democratic authority appeals and national identity framing over time.\n\nFor each axis, provide scores, salience, and confidence with specific attention to temporal evidence and historical positioning. Write a comprehensive longitudinal analysis that covers populism emergence patterns, historical context, and temporal discourse evolution supported by direct textual evidence and clear reasoning for all scores and metadata."
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
      "populism_pluralism_axis_score": ["populism.{0,20}pluralism.{0,20}axis.{0,20}score", "populism.{0,20}axis.{0,20}rating", "vertical\\s*axis\\s*:\\s*[0-9]"],
      "nationalism_patriotism_axis_score": ["nationalism.{0,20}patriotism.{0,20}axis.{0,20}score", "nationalism.{0,20}axis.{0,20}rating", "horizontal\\s*axis\\s*:\\s*[0-9]"],
      "populism_pluralism_axis_salience": ["populism.{0,20}pluralism.{0,20}axis.{0,20}salience", "populism.{0,20}axis.{0,20}importance", "vertical.{0,20}axis.{0,20}centrality"],
      "nationalism_patriotism_axis_salience": ["nationalism.{0,20}patriotism.{0,20}axis.{0,20}salience", "nationalism.{0,20}axis.{0,20}importance", "horizontal.{0,20}axis.{0,20}centrality"],
      "populism_pluralism_axis_confidence": ["populism.{0,20}pluralism.{0,20}axis.{0,20}confidence", "populism.{0,20}axis.{0,20}certainty", "vertical.{0,20}axis.{0,20}sure"],
      "nationalism_patriotism_axis_confidence": ["nationalism.{0,20}patriotism.{0,20}axis.{0,20}confidence", "nationalism.{0,20}axis.{0,20}certainty", "horizontal.{0,20}axis.{0,20}sure"]
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
  }
}
```

</details>