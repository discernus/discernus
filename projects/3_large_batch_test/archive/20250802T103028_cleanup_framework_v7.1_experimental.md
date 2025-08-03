# Political Discourse Analysis Framework v7.1 - Populism Emergence Study

**Version**: 7.1  
**Status**: Active  
**Major Change**: Enhanced Gasket Architecture with Explicit Schema Mapping

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

## V7.1 Enhanced Gasket Architecture

**CRITICAL**: This framework uses the V7.1 Enhanced Gasket Architecture with explicit schema mapping for reliable data extraction.

### Raw Analysis Log Output Requirements
The Analysis Agent must produce natural language analysis containing these exact elements:
- **Populism-Pluralism Score**: Single number 0.0-1.0 
- **Nationalism-Patriotism Score**: Single number 0.0-1.0
- **Populism-Pluralism Salience**: Single number 0.0-1.0
- **Nationalism-Patriotism Salience**: Single number 0.0-1.0
- **Populism-Pluralism Confidence**: Single number 0.0-1.0
- **Nationalism-Patriotism Confidence**: Single number 0.0-1.0
- **Evidence Quotes**: 1-2 quotes per axis with reasoning

### Gasket Schema (Intelligent Extractor Mapping)
```json
{
  "gasket_schema": {
    "version": "7.1",
    "extraction_targets": {
      "core_scores": {
        "populism_pluralism_score": {
          "type": "float",
          "range": [0.0, 1.0],
          "description": "Vertical axis score: 0.0=pure pluralism, 1.0=pure populism",
          "extraction_patterns": ["populism.{0,20}score", "populism.{0,20}pluralism.{0,20}score", "vertical.{0,20}axis.{0,20}score"]
        },
        "nationalism_patriotism_score": {
          "type": "float", 
          "range": [0.0, 1.0],
          "description": "Horizontal axis score: 0.0=pure patriotism, 1.0=pure nationalism",
          "extraction_patterns": ["nationalism.{0,20}score", "nationalism.{0,20}patriotism.{0,20}score", "horizontal.{0,20}axis.{0,20}score"]
        }
      },
      "metadata_scores": {
        "populism_pluralism_salience": {
          "type": "float",
          "range": [0.0, 1.0],
          "extraction_patterns": ["populism.{0,20}salience", "vertical.{0,20}salience"]
        },
        "nationalism_patriotism_salience": {
          "type": "float",
          "range": [0.0, 1.0], 
          "extraction_patterns": ["nationalism.{0,20}salience", "horizontal.{0,20}salience"]
        },
        "populism_pluralism_confidence": {
          "type": "float",
          "range": [0.0, 1.0],
          "extraction_patterns": ["populism.{0,20}confidence", "vertical.{0,20}confidence"]
        },
        "nationalism_patriotism_confidence": {
          "type": "float",
          "range": [0.0, 1.0],
          "extraction_patterns": ["nationalism.{0,20}confidence", "horizontal.{0,20}confidence"]
        }
      },
      "required_fields": [
        "populism_pluralism_score",
        "nationalism_patriotism_score"
      ],
      "optional_fields": [
        "populism_pluralism_salience",
        "nationalism_patriotism_salience", 
        "populism_pluralism_confidence",
        "nationalism_patriotism_confidence"
      ]
    }
  }
}
```

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "political_discourse_populism_v7_1",
  "version": "v7.1",
  "display_name": "Political Discourse Analysis Framework v7.1 - Populism Emergence Study",
  "analysis_variants": {
    "default": {
      "description": "Complete two-axis populism-pluralism analysis with enhanced gasket architecture.",
      "analysis_prompt": "You are an expert analyst of political discourse with deep knowledge of populist rhetoric, democratic theory, and American political communication. Your task is to analyze the text using the Political Discourse Analysis Framework v7.1, which measures populist discourse emergence through two orthogonal axes.\n\nANALYZE THE POPULISM-PLURALISM AXIS (vertical): Score from 0.0 (pure pluralism) to 1.0 (pure populism). Look for populist markers: 'the people,' 'ordinary Americans,' 'establishment,' 'elites,' 'corrupt politicians,' 'us versus them,' 'will of the people,' 'rigged system,' 'common sense,' 'heartland.' Look for pluralist markers: 'democratic institutions,' 'evidence-based,' 'diverse perspectives,' 'expert analysis,' 'bipartisan cooperation,' 'constitutional process.'\n\nANALYZE THE NATIONALISM-PATRIOTISM AXIS (horizontal): Score from 0.0 (pure patriotism) to 1.0 (pure nationalism). Look for nationalist markers: 'American greatness,' 'our people,' 'real Americans,' 'traditional culture,' 'foreign influence,' 'cultural heritage,' 'exceptional nation.' Look for patriotic markers: 'Constitution,' 'Bill of Rights,' 'civic responsibility,' 'equal justice,' 'nation of immigrants,' 'democratic institutions.'\n\nCRITICAL OUTPUT REQUIREMENTS:\nYour analysis must include these exact phrases and scores:\n- Populism-Pluralism Score: [0.0-1.0 number]\n- Nationalism-Patriotism Score: [0.0-1.0 number] \n- Populism-Pluralism Salience: [0.0-1.0 number]\n- Nationalism-Patriotism Salience: [0.0-1.0 number]\n- Populism-Pluralism Confidence: [0.0-1.0 number]\n- Nationalism-Patriotism Confidence: [0.0-1.0 number]\n\nProvide 1-2 strongest quotes as evidence for each axis. Write in natural language analysis format - NO JSON structure. The Intelligent Extractor will parse your natural language output."
    },
    "longitudinal_analysis": {
      "description": "Specialized analysis for temporal populism evolution studies across presidential administrations.",
      "analysis_prompt": "You are conducting longitudinal analysis of populist discourse evolution in American presidential rhetoric using Framework v7.1. Focus on temporal indicators of populist emergence, institutional critique patterns, and anti-elite sentiment development.\n\nCRITICAL OUTPUT REQUIREMENTS:\nYour analysis must include these exact phrases and scores:\n- Populism-Pluralism Score: [0.0-1.0 number]\n- Nationalism-Patriotism Score: [0.0-1.0 number] \n- Populism-Pluralism Salience: [0.0-1.0 number]\n- Nationalism-Patriotism Salience: [0.0-1.0 number]\n- Populism-Pluralism Confidence: [0.0-1.0 number]\n- Nationalism-Patriotism Confidence: [0.0-1.0 number]\n\nScore both axes with attention to historical context and populist discourse evolution. Provide evidence that demonstrates populist rhetoric development or institutional democratic language. Write in natural language - the Intelligent Extractor will parse your output."
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
  "gasket_schema": {
    "version": "7.1",
    "extraction_method": "intelligent_extractor",
    "target_keys": [
      "populism_pluralism_score",
      "nationalism_patriotism_score", 
      "populism_pluralism_salience",
      "nationalism_patriotism_salience",
      "populism_pluralism_confidence", 
      "nationalism_patriotism_confidence"
    ],
    "extraction_patterns": {
      "populism_pluralism_score": ["populism.{0,20}pluralism.{0,20}score", "populism.{0,20}score", "vertical.{0,20}axis.{0,20}score"],
      "nationalism_patriotism_score": ["nationalism.{0,20}patriotism.{0,20}score", "nationalism.{0,20}score", "horizontal.{0,20}axis.{0,20}score"],
      "populism_pluralism_salience": ["populism.{0,20}pluralism.{0,20}salience", "populism.{0,20}salience", "vertical.{0,20}salience"],
      "nationalism_patriotism_salience": ["nationalism.{0,20}patriotism.{0,20}salience", "nationalism.{0,20}salience", "horizontal.{0,20}salience"],
      "populism_pluralism_confidence": ["populism.{0,20}pluralism.{0,20}confidence", "populism.{0,20}confidence", "vertical.{0,20}confidence"],
      "nationalism_patriotism_confidence": ["nationalism.{0,20}patriotism.{0,20}confidence", "nationalism.{0,20}confidence", "horizontal.{0,20}confidence"]
    },
    "validation_rules": {
      "required_fields": ["populism_pluralism_score", "nationalism_patriotism_score"],
      "score_ranges": {"min": 0.0, "max": 1.0},
      "fallback_strategy": "use_default_values"
    }
  },
  "raw_analysis_log_format": {
    "description": "Raw analysis log containing axis scores, evidence, and reasoning without structured JSON",
    "content": "Free-form text with political discourse analysis including scores, evidence quotes, and qualitative reasoning",
    "required_output_format": "Natural language analysis containing exact score phrases for Intelligent Extractor parsing"
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
