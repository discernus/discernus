# Political Discourse Analysis Framework v6.0 - Populism Emergence Study

**Version**: 6.0  
**Status**: Active  
**Major Change**: Return to JSON Architecture with Enhanced Populism-Pluralism Analysis

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
  "name": "political_discourse_populism_v6",
  "version": "v6.0",
  "display_name": "Political Discourse Analysis Framework v6.0 - Populism Emergence Study",
  "analysis_variants": {
    "default": {
      "description": "Complete two-axis populism-pluralism analysis with enhanced linguistic markers.",
      "analysis_prompt": "You are an expert analyst of political discourse with deep knowledge of populist rhetoric, democratic theory, and American political communication. Your task is to analyze the text using the Political Discourse Analysis Framework v6.0, which measures populist discourse emergence through two orthogonal axes. Analyze the POPULISM-PLURALISM AXIS (vertical): Score from 0.0 (pure pluralism) to 1.0 (pure populism). Look for populist markers: 'the people,' 'ordinary Americans,' 'establishment,' 'elites,' 'corrupt politicians,' 'us versus them,' 'will of the people,' 'rigged system,' 'common sense,' 'heartland.' Look for pluralist markers: 'democratic institutions,' 'evidence-based,' 'diverse perspectives,' 'expert analysis,' 'bipartisan cooperation,' 'constitutional process.' Analyze the NATIONALISM-PATRIOTISM AXIS (horizontal): Score from 0.0 (pure patriotism) to 1.0 (pure nationalism). Look for nationalist markers: 'American greatness,' 'our people,' 'real Americans,' 'traditional culture,' 'foreign influence,' 'cultural heritage,' 'exceptional nation.' Look for patriotic markers: 'Constitution,' 'Bill of Rights,' 'civic responsibility,' 'equal justice,' 'nation of immigrants,' 'democratic institutions.' Determine quadrant classification based on axis intersection. Provide strongest 1-2 quotes as evidence for each axis with confidence ratings. Your response must be a single, valid JSON object with the required nested structures. Provide ONLY raw axis scores and evidence - NO calculations or derived metrics."
    },
    "longitudinal_analysis": {
      "description": "Specialized analysis for temporal populism evolution studies across presidential administrations.",
      "analysis_prompt": "You are conducting longitudinal analysis of populist discourse evolution in American presidential rhetoric. Focus on temporal indicators of populist emergence, institutional critique patterns, and anti-elite sentiment development. Score both axes with attention to historical context and populist discourse evolution. Provide evidence that demonstrates populist rhetoric development or institutional democratic language. Return a single JSON object with required structures focusing on populism emergence patterns."
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
    "populist_intensity_index": "Combined measure of populist discourse strength: (populism_pluralism_score * 0.7) + (nationalism_patriotism_score * 0.3)",
    "democratic_institutionalism_index": "Combined measure of democratic institutional respect: ((1 - populism_pluralism_score) * 0.7) + ((1 - nationalism_patriotism_score) * 0.3)",
    "quadrant_classification": "Four-quadrant typology based on axis intersection thresholds"
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
  "output_contract": {
    "schema": {
      "worldview": "string",
      "scores": "object",
      "evidence": "object", 
      "reasoning": "object",
      "axis_analysis": "object",
      "quadrant_classification": "string"
    },
    "structured_data_requirements": {
      "scores": {
        "description": "Nested object containing ONLY raw axis scores (NO calculated metrics)",
        "structure": {
          "dimensions": {
            "populism_pluralism_axis": {
              "score": "number (0.0-1.0)",
              "salience": "number (0.0-1.0)",
              "confidence": "number (0.0-1.0)"
            },
            "nationalism_patriotism_axis": {
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
        "description": "Nested object containing structured evidence data for populism discourse analysis",
        "structure": {
          "by_dimension": {
            "populism_pluralism_axis": [
              {
                "quote_id": "string",
                "quote_text": "string", 
                "confidence": "number (0.0-1.0)",
                "context_type": "string",
                "discourse_marker_type": "string"
              }
            ],
            "nationalism_patriotism_axis": [
              {
                "quote_id": "string",
                "quote_text": "string", 
                "confidence": "number (0.0-1.0)",
                "context_type": "string",
                "discourse_marker_type": "string"
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
    "instructions": "IMPORTANT: Your response MUST be a single, valid JSON object containing all required fields with the nested structures specified above. Score the populism_pluralism_axis from 0.0 (pure pluralism) to 1.0 (pure populism). Score the nationalism_patriotism_axis from 0.0 (pure patriotism) to 1.0 (pure nationalism). Include salience and confidence for each axis. Provide 1-2 strongest quotes as evidence for each axis with discourse marker classification. DO NOT perform any mathematical calculations or compute derived metrics - provide ONLY raw axis scores, salience, confidence, and evidence."
  }
}
```

</details> 
