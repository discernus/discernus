# Character Assessment Framework v6.1-Factorial

**Version**: 6.1-Factorial
**Status**: Active
**Major Change**: Added Era and Ideology Classification for Factorial Experimental Designs
**Based On**: CAF v6.0 JSON-First Architecture

---

## Executive Summary

The Character Assessment Framework (CAF) v6.1-Factorial extends CAF v6.0 with contextual classification dimensions to support factorial experimental designs. It maintains all character tension analysis capabilities while adding era and ideology detection for 2×3 factorial analysis (Ideology × Era).

**NEW IN V6.1-FACTORIAL**: Adds contextual classification dimensions (era_classification, ideology_classification) to support factorial experimental designs requiring grouping variables for statistical analysis, while preserving all CAF v6.0 character assessment functionality.

---

## Character Dimensions

### **Civic Virtues** - Positive Character Traits

**1. Dignity** (0.0-1.0): Respect for universal human worth and inherent dignity  
**2. Truth** (0.0-1.0): Intellectual honesty and commitment to factual accuracy  
**3. Justice** (0.0-1.0): Fairness orientation and procedural integrity  
**4. Hope** (0.0-1.0): Constructive vision and democratic optimism  
**5. Pragmatism** (0.0-1.0): Practical wisdom and workable solutions  

### **Civic Vices** - Negative Character Traits

**1. Tribalism** (0.0-1.0): Group loyalty over universal principles  
**2. Manipulation** (0.0-1.0): Deceptive rhetoric and information distortion  
**3. Resentment** (0.0-1.0): Grievance focus and backward-looking blame  
**4. Fear** (0.0-1.0): Anxiety appeals and catastrophic thinking  
**5. Fantasy** (0.0-1.0): Unrealistic promises and magical thinking  

### **Contextual Classifications** - Factorial Design Support

**Era Classification**: Historical period classification for temporal analysis
- **Civil Rights Era** (1963-1975): Focus on fundamental rights and constitutional equality
- **Institutional Era** (1976-2007): Emphasis on institutional processes and procedural governance  
- **Populist Era** (2008-2025): Anti-establishment rhetoric and direct democratic appeals

**Ideology Classification**: Political ideological orientation for comparative analysis
- **Conservative**: Traditional values, institutional respect, incremental change
- **Progressive**: Social reform, systemic change, expanding rights and protections

---

## Character Tension Mathematics

### **Character Tension Scoring**

**Formula**: `Character Tension = min(Virtue_score, Vice_score) × |Virtue_salience - Vice_salience|`

### **Moral Character Strategic Contradiction Index (MC-SCI)**

**Formula**: `MC-SCI = (Sum of all Character Tension Scores) / Number of Opposing Pairs`

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "caf_v6_1_factorial",
  "version": "v6.1-factorial",
  "display_name": "Character Assessment Framework v6.1-Factorial",
  "analysis_variants": {
    "default": {
      "description": "Complete salience-weighted character analysis with era/ideology classification for factorial designs - mathematical calculations handled by code execution.",
      "analysis_prompt": "Phase 1: Cognitive Priming: You are an expert analyst of civic character and political ethics with deep expertise in moral psychology, character assessment, and American political history. Phase 2: Framework Methodology: Your task is to analyze what the provided text reveals about the SPEAKER'S moral character using the Character Assessment Framework v6.1-Factorial. This framework examines civic character through a twelve-dimensional model: ten character dimensions (five civic virtues vs. five civic vices) plus two contextual classifications (era and ideology) for factorial experimental analysis. Phase 3: Operational Definitions: VIRTUES - Dignity (respect for universal human worth), Truth (intellectual honesty), Justice (fairness orientation), Hope (constructive vision), Pragmatism (practical wisdom). VICES - Tribalism (group loyalty over principles), Manipulation (deceptive rhetoric), Resentment (grievance focus), Fear (anxiety appeals), Fantasy (unrealistic promises). CONTEXTUAL CLASSIFICATIONS - Era Classification: Civil Rights Era (1963-1975, fundamental rights focus), Institutional Era (1976-2007, procedural governance), Populist Era (2008-2025, anti-establishment appeals). Ideology Classification: Conservative (traditional values, institutional respect, incremental change) vs. Progressive (social reform, systemic change, expanding rights). Phase 4: Scoring Protocol: For each of the ten CHARACTER dimensions, provide: (1) Raw score (0.0-1.0) based on strength, (2) Salience score (0.0-1.0) based on prominence, (3) Confidence score (0.0-1.0) based on evidence strength, (4) Strongest 1-2 quotes with context. For the two CLASSIFICATION dimensions, provide: (1) Classification category (string), (2) Confidence score (0.0-1.0) based on evidence strength, (3) Justification explaining the classification. DO NOT perform mathematical calculations, tension computations, or derived metrics. Phase 5: JSON Structure Requirements: Your response must be a structured JSON object containing nested data for all twelve dimensions (10 character + 2 contextual), evidence organized by dimension, reasoning for each assessment, and salience_ranking array. Phase 6: Output Specification: Return a single, valid JSON object with raw dimensional scores and contextual classifications - NO calculations, tensions, or derived metrics. All mathematical processing will be handled by code execution."
    }
  },
  "dimension_groups": {
    "virtues": ["dignity", "truth", "justice", "hope", "pragmatism"],
    "vices": ["tribalism", "manipulation", "resentment", "fear", "fantasy"],
    "contextual": ["era_classification", "ideology_classification"]
  },
  "calculation_spec": {
    "character_tension_mathematics": "Character tension quantification using formula: Character Tension = min(Virtue_score, Vice_score) × |Virtue_salience - Vice_salience|.",
    "character_tensions": {
      "dignity_tribalism_tension": "min(dignity, tribalism) * abs(dignity_salience - tribalism_salience)",
      "truth_manipulation_tension": "min(truth, manipulation) * abs(truth_salience - manipulation_salience)",
      "justice_resentment_tension": "min(justice, resentment) * abs(justice_salience - resentment_salience)",
      "hope_fear_tension": "min(hope, fear) * abs(hope_salience - fear_salience)",
      "pragmatism_fantasy_tension": "min(pragmatism, fantasy) * abs(pragmatism_salience - fantasy_salience)"
    },
    "moral_character_sci": "(dignity_tribalism_tension + truth_manipulation_tension + justice_resentment_tension + hope_fear_tension + pragmatism_fantasy_tension) / 5"
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
      "salience_ranking": "array",
      "tension_analysis": "object",
      "contextual_classification": "object",
      "factorial_grouping": "object"
    },
    "structured_data_requirements": {
      "scores": {
        "description": "Nested object containing all dimensional scores and calculated metrics",
        "structure": {
          "dimensions": {
            "dignity": {
              "score": "number (0.0-1.0)",
              "salience": "number (0.0-1.0)",
              "confidence": "number (0.0-1.0)"
            },
            "truth": {
              "score": "number (0.0-1.0)",
              "salience": "number (0.0-1.0)",
              "confidence": "number (0.0-1.0)"
            },
            "justice": {
              "score": "number (0.0-1.0)",
              "salience": "number (0.0-1.0)",
              "confidence": "number (0.0-1.0)"
            },
            "hope": {
              "score": "number (0.0-1.0)",
              "salience": "number (0.0-1.0)",
              "confidence": "number (0.0-1.0)"
            },
            "pragmatism": {
              "score": "number (0.0-1.0)",
              "salience": "number (0.0-1.0)",
              "confidence": "number (0.0-1.0)"
            },
            "tribalism": {
              "score": "number (0.0-1.0)",
              "salience": "number (0.0-1.0)",
              "confidence": "number (0.0-1.0)"
            },
            "manipulation": {
              "score": "number (0.0-1.0)",
              "salience": "number (0.0-1.0)",
              "confidence": "number (0.0-1.0)"
            },
            "resentment": {
              "score": "number (0.0-1.0)",
              "salience": "number (0.0-1.0)",
              "confidence": "number (0.0-1.0)"
            },
            "fear": {
              "score": "number (0.0-1.0)",
              "salience": "number (0.0-1.0)",
              "confidence": "number (0.0-1.0)"
            },
            "fantasy": {
              "score": "number (0.0-1.0)",
              "salience": "number (0.0-1.0)",
              "confidence": "number (0.0-1.0)"
            }
          },
          "contextual": {
            "era_classification": {
              "classification": "string (Civil Rights Era|Institutional Era|Populist Era)",
              "confidence": "number (0.0-1.0)"
            },
            "ideology_classification": {
              "classification": "string (Conservative|Progressive)",
              "confidence": "number (0.0-1.0)"
            }
          },
          "factorial_grouping": {
            "era": "string (Civil Rights Era|Institutional Era|Populist Era)",
            "ideology": "string (Conservative|Progressive)"
          },
          "metadata": {
            "total_dimensions": "number",
            "analysis_completeness": "number (0.0-1.0)",
            "virtue_dominance": "number",
            "vice_dominance": "number"
          }
        }
      },
      "evidence": {
        "description": "Nested object containing structured evidence data for audit and replication",
        "structure": {
          "by_dimension": {
            "dignity": [
              {
                "quote_id": "string",
                "quote_text": "string", 
                "confidence": "number (0.0-1.0)",
                "context_type": "string",
                "salience_justification": "string"
              }
            ],
            "truth": "array_of_evidence_objects",
            "justice": "array_of_evidence_objects",
            "hope": "array_of_evidence_objects",
            "pragmatism": "array_of_evidence_objects",
            "tribalism": "array_of_evidence_objects",
            "manipulation": "array_of_evidence_objects",
            "resentment": "array_of_evidence_objects",
            "fear": "array_of_evidence_objects",
            "fantasy": "array_of_evidence_objects",
            "era_classification": [
              {
                "evidence_text": "string",
                "justification": "string",
                "confidence": "number (0.0-1.0)"
              }
            ],
            "ideology_classification": [
              {
                "evidence_text": "string",
                "justification": "string", 
                "confidence": "number (0.0-1.0)"
              }
            ]
          },
          "metadata": {
            "total_quotes": "number",
            "average_confidence": "number",
            "evidence_distribution": "object"
          }
        }
      },
      "contextual_classification": {
        "description": "Classification results for factorial experimental design",
        "structure": {
          "era": "string (Civil Rights Era|Institutional Era|Populist Era)",
          "ideology": "string (Conservative|Progressive)",
          "era_confidence": "number (0.0-1.0)",
          "ideology_confidence": "number (0.0-1.0)",
          "classification_rationale": {
            "era_justification": "string",
            "ideology_justification": "string"
          }
        }
      },
      "factorial_grouping": {
        "description": "Direct string values for factorial statistical analysis",
        "structure": {
          "era": "string (Civil Rights Era|Institutional Era|Populist Era)",
          "ideology": "string (Conservative|Progressive)"
        }
      }
    },
    "instructions": "IMPORTANT: Your response MUST be a single, valid JSON object containing all required fields with the nested structures specified above. Include both character dimensions (10) and contextual classifications (2). CRITICAL: You must include BOTH the contextual_classification section AND a factorial_grouping section with direct era and ideology string values for statistical analysis. The factorial_grouping section must contain: 'era': 'Civil Rights Era'|'Institutional Era'|'Populist Era' and 'ideology': 'Conservative'|'Progressive'. The salience_ranking should be an ordered array of objects for character dimensions only. All numerical scores must be between 0.0 and 1.0. DO NOT compute tensions, indices, or derived metrics."
  }
}
```

</details>