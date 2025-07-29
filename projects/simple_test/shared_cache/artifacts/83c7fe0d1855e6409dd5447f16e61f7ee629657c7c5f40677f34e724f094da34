# Character Assessment Framework v5.0

**Version**: 5.0
**Status**: Active
**Major Change**: Embedded CSV Architecture for Synthesis Scalability

---

## Executive Summary

The Character Assessment Framework (CAF) v5.0 integrates breakthrough character tension analysis to provide a multi-dimensional assessment of a speaker's moral character. It quantifies moral contradictions between opposing character traits (virtues and vices) and calculates an overall Moral Character Strategic Contradiction Index (MC-SCI). This allows for a nuanced understanding of a speaker's moral coherence and identity.

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
  "name": "caf_v5_0",
  "version": "v5.0",
  "display_name": "Character Assessment Framework v5.0",
  "analysis_variants": {
    "default": {
      "description": "Complete salience-weighted character analysis with moral tension pattern quantification and embedded CSV output.",
      "analysis_prompt": "Phase 1: Cognitive Priming: You are an expert analyst of civic character and political ethics. Phase 2: Framework Methodology: Your task is to analyze what the provided text reveals about the SPEAKER'S moral character using the Character Assessment Framework v5.0. Phase 3: Operational Definitions: Evaluate five civic virtues (Dignity, Truth, Justice, Hope, Pragmatism) and five opposing civic vices (Tribalism, Manipulation, Resentment, Fear, Fantasy). Phase 4: Scoring Protocol: For each of the ten dimensions, score its intensity (0.0-1.0) and salience (0.0-1.0). Provide the strongest 1-2 quotes as evidence. Calculate the tension score for each virtue-vice pair and the overall Moral Character Strategic Contradiction Index (MC-SCI). Phase 5: Embedded CSV Generation: CRITICAL: Your response must include two embedded CSV segments using these exact delimiters: <<<DISCERNUS_SCORES_CSV_v1>>> and <<<DISCERNUS_EVIDENCE_CSV_v1>>>. The scores CSV must have columns for each dimension's score and salience, each tension score, and the MC-SCI. The evidence CSV must have columns for dimension, quote, and confidence. Phase 6: Output Specification: Return a complete response containing both a comprehensive JSON analysis and the embedded CSV segments as specified in the output_contract."
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
    "embedded_csv_requirements": {
      "scores_csv": {
        "delimiter_start": "<<<DISCERNUS_SCORES_CSV_v1>>>",
        "delimiter_end": "<<<END_DISCERNUS_SCORES_CSV_v1>>>",
        "description": "CSV for all dimensional scores, salience scores, tension scores, and calculated metrics."
      },
      "evidence_csv": {
        "delimiter_start": "<<<DISCERNUS_EVIDENCE_CSV_v1>>>",
        "delimiter_end": "<<<END_DISCERNUS_EVIDENCE_CSV_v1>>>",
        "description": "CSV for structured evidence data for audit and replication."
      }
    },
    "instructions": "IMPORTANT: Your response MUST include both a complete JSON analysis AND embedded CSV segments using the exact delimiters specified. The salience_ranking should be an ordered array of objects, each containing 'dimension', 'salience_score', and 'rank'."
  }
}
```

</details> 