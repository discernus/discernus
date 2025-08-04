# Emotional Climate Framework (ECF) v5.0
**Version**: 5.0
**Status**: Active
**Major Change**: Embedded CSV Architecture for Synthesis Scalability

---

## Overview

ECF analyzes emotional atmosphere in political discourse through six dimensions, independent of rhetorical strategy, speaker character, or institutional effects. Measures psychological environment that discourse generates.

**Purpose**: Objective measurement of emotional climate for audience response prediction and message optimization.

**Applications**: Emotional impact assessment, cross-platform analysis, longitudinal tracking, message optimization.

---

## Dimensions

#### Fear (Crisis/Threat Climate) (0.0-1.0)
**Definition**: Language emphasizing danger, threat, vulnerability, crisis, or existential risk.
**Key Markers**: "emergency," "crisis," "under attack," "running out of time," "defenseless"

#### Hope (Opportunity/Progress Climate) (0.0-1.0)  
**Definition**: Language emphasizing positive possibilities, progress, improvement, or achievement potential.
**Key Markers**: "opportunity," "breakthrough," "bright future," "great potential," "optimistic"

#### Enmity (Hostility/Conflict Climate) (0.0-1.0)
**Definition**: Language creating antagonistic atmosphere toward opponents, enemies, or opposing groups.
**Key Markers**: "enemy," "betrayal," "fight against," "destroy," "combat"

#### Amity (Friendship/Unity Climate) (0.0-1.0)
**Definition**: Language fostering positive relationships, cooperation, solidarity, or shared purpose.
**Key Markers**: "together," "unity," "partnership," "cooperation," "shared values"

#### Envy (Resentment/Grievance Climate) (0.0-1.0)
**Definition**: Language expressing resentment toward others' advantages, success, or privileged positions.
**Key Markers**: "unfair advantage," "privileged elite," "deserve better," "left behind," "rigged system"

#### Compersion (Celebration/Merit Climate) (0.0-1.0)
**Definition**: Language celebrating others' success, merit, achievement, or positive developments.
**Key Markers**: "congratulations," "well-deserved," "earned success," "inspiring achievement," "celebration"

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "ecf_v5_0",
  "version": "v5.0",
  "display_name": "Emotional Climate Framework (ECF) v5.0",
  "analysis_variants": {
    "default": {
      "description": "Complete emotional climate analysis across six dimensions with embedded CSV output.",
      "analysis_prompt": "Phase 1: Cognitive Priming: You are an expert emotional climate analyst. Phase 2: Framework Methodology: Your task is to analyze the text using the Emotional Climate Framework (ECF) v5.0. Phase 3: Operational Definitions: Evaluate six dimensions of emotional climate: Fear, Hope, Enmity, Amity, Envy, and Compersion. Phase 4: Scoring Protocol: Score each dimension from 0.0 to 1.0 for both intensity and salience. Provide the strongest 1-2 quotes as evidence. Phase 5: Embedded CSV Generation: CRITICAL: Your response must include two embedded CSV segments using these exact delimiters: <<<DISCERNUS_SCORES_CSV_v1>>> and <<<DISCERNUS_EVIDENCE_CSV_v1>>>. The scores CSV must have columns for each dimension's score and salience. The evidence CSV must have columns for dimension, quote, and confidence. Phase 6: Output Specification: Return a complete response containing both a comprehensive JSON analysis and the embedded CSV segments as specified in the output_contract."
    }
  },
  "dimension_groups": {
      "emotional_axes": ["fear", "hope", "enmity", "amity", "envy", "compersion"]
  },
  "calculation_spec": {
    "affective_climate_index": "(hope - fear)",
    "relational_climate_index": "(amity - enmity)", 
    "success_climate_index": "(compersion - envy)",
    "overall_emotional_intensity": "(fear + hope + enmity + amity + envy + compersion) / 6",
    "emotional_balance_score": "(affective_climate_index + relational_climate_index + success_climate_index) / 3"
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
      "salience_ranking": "array"
    },
    "embedded_csv_requirements": {
      "scores_csv": {
        "delimiter_start": "<<<DISCERNUS_SCORES_CSV_v1>>>",
        "delimiter_end": "<<<END_DISCERNUS_SCORES_CSV_v1>>>",
        "description": "CSV for all dimensional scores, salience scores, and calculated indices."
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