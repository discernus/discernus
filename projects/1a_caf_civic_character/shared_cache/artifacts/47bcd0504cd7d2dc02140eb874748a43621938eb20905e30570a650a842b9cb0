# Character Assessment Framework v6.0

**Version**: 6.0
**Status**: Active
**Major Change**: JSON-First Architecture with Enhanced Synthesis Integration

---

## Executive Summary

The Character Assessment Framework (CAF) v6.0 integrates breakthrough character tension analysis to provide a multi-dimensional assessment of a speaker's moral character. It quantifies moral contradictions between opposing character traits (virtues and vices) and calculates an overall Moral Character Strategic Contradiction Index (MC-SCI). This allows for a nuanced understanding of a speaker's moral coherence and identity.

**NEW IN V6.0**: Returns to JSON-first output architecture while maintaining all analytical capabilities from v5.0, eliminating CSV parsing brittleness while preserving synthesis scalability.

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
  "name": "caf_v6_0",
  "version": "v6.0",
  "display_name": "Character Assessment Framework v6.0",
  "analysis_variants": {
    "default": {
              "description": "Complete salience-weighted character analysis with raw scoring only - mathematical calculations handled by code execution.",
      "analysis_prompt": "Phase 1: Cognitive Priming: You are an expert analyst of civic character and political ethics with deep expertise in moral psychology and character assessment. Phase 2: Framework Methodology: Your task is to analyze what the provided text reveals about the SPEAKER'S moral character using the Character Assessment Framework v6.0. This framework examines civic character through a ten-dimensional model that contrasts five civic virtues (Dignity, Truth, Justice, Hope, Pragmatism) with five opposing civic vices (Tribalism, Manipulation, Resentment, Fear, Fantasy). Phase 3: Operational Definitions: Evaluate each dimension carefully: VIRTUES - Dignity (respect for universal human worth), Truth (intellectual honesty), Justice (fairness orientation), Hope (constructive vision), Pragmatism (practical wisdom). VICES - Tribalism (group loyalty over principles), Manipulation (deceptive rhetoric), Resentment (grievance focus), Fear (anxiety appeals), Fantasy (unrealistic promises). Phase 4: Scoring Protocol: For each of the ten dimensions, provide ONLY: (1) Raw score (0.0-1.0) based on how strongly the dimension appears, (2) Salience score (0.0-1.0) based on how prominent it is in the overall message, (3) Confidence score (0.0-1.0) based on the strength of evidence, (4) The strongest 1-2 quotes as supporting evidence with context. DO NOT perform any mathematical calculations, tension computations, or derived metrics. Phase 5: JSON Structure Requirements: Your response must be a structured JSON object containing nested data for raw scores only (NO calculated metrics), evidence organized by_dimension with quote details, reasoning for each assessment, and a salience_ranking array. Phase 6: Output Specification: Return a single, valid JSON object with raw dimensional scores only - NO calculations, tensions, or derived metrics. All mathematical processing will be handled by code execution."
    }
  },
  "dimension_groups": {
    "virtues": ["dignity", "truth", "justice", "hope", "pragmatism"],
    "vices": ["tribalism", "manipulation", "resentment", "fear", "fantasy"]
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
      "tension_analysis": "object"
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
            "fantasy": "array_of_evidence_objects"
          },
          "metadata": {
            "total_quotes": "number",
            "average_confidence": "number",
            "evidence_distribution": "object"
          }
        }
      }
    },
    "instructions": "IMPORTANT: Your response MUST be a single, valid JSON object containing all required fields with the nested structures specified above. The salience_ranking should be an ordered array of objects, each containing 'dimension', 'salience_score', and 'rank'. The tension_analysis should contain qualitative reasoning about character patterns (NO mathematical calculations). All numerical scores must be between 0.0 and 1.0. DO NOT compute tensions, indices, or derived metrics."
  }
}
```

</details> 