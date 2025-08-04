# Constitutional Health Framework (CHF) v5.0
**Version**: 5.0
**Status**: Active
**Major Change**: Embedded CSV Architecture for Synthesis Scalability

---

## Overview

CHF v5.0 analyzes how political discourse affects constitutional system health through salience-enhanced assessment. Measures discourse impact across three dimensions of constitutional health, weighted by actual rhetorical emphasis patterns.

**Purpose**: Reveals whether discourse strengthens or weakens constitutional democracy by analyzing procedural legitimacy, institutional respect, and systemic continuity.

**Innovation**: Salience-weighted analysis captures not just constitutional health/pathology but which dimensions receive the most rhetorical emphasis.

**Applications**: Constitutional health monitoring, cross-system comparison, historical analysis, early warning systems.

---

## Constitutional Dimensions

### Health Dimensions (0.0-1.0)

#### Procedural Legitimacy
**Definition**: Support for established procedures for political change and governance.
**Key Markers**: "constitutional process," "established procedure," "due process," "proper channels"

#### Institutional Respect  
**Definition**: Recognition of institutional authority, expertise, and legitimate governance role.
**Key Markers**: "institutional authority," "expert analysis," "separation of powers," "constitutional duty"

#### Systemic Continuity
**Definition**: Support for maintaining and improving existing constitutional framework.
**Key Markers**: "constitutional stability," "democratic tradition," "institutional continuity," "gradual reform"

### Pathology Dimensions (0.0-1.0)

#### Procedural Rejection
**Definition**: Rejecting established procedures in favor of circumvention or extra-constitutional action.
**Key Markers**: "bypass the system," "emergency powers," "broken system," "people's will"

#### Institutional Subversion
**Definition**: Attacking institutional authority, expertise, or legitimate governance role.
**Key Markers**: "corrupt institutions," "illegitimate authority," "failed establishment," "biased system"

#### Systemic Replacement
**Definition**: Advocating fundamental replacement rather than reform of constitutional framework.
**Key Markers**: "new system," "radical transformation," "complete overhaul," "revolutionary change"

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "chf_v5_0",
  "version": "v5.0",
  "display_name": "Constitutional Health Framework (CHF) v5.0",
  "analysis_variants": {
    "default": {
      "description": "Complete constitutional health analysis with salience weighting and embedded CSV output.",
      "analysis_prompt": "Phase 1: Cognitive Priming: You are an expert constitutional health analyst. Phase 2: Framework Methodology: Your task is to analyze the text using the Constitutional Health Framework (CHF) v5.0. Phase 3: Operational Definitions: Evaluate six dimensions across three axes: Procedural (Legitimacy vs. Rejection), Institutional (Respect vs. Subversion), and Systemic (Continuity vs. Replacement). Phase 4: Scoring Protocol: Score each of the six dimensions from 0.0 to 1.0 for both intensity and salience. Provide the strongest 1-2 quotes as evidence. Phase 5: Embedded CSV Generation: CRITICAL: Your response must include two embedded CSV segments using these exact delimiters: <<<DISCERNUS_SCORES_CSV_v1>>> and <<<DISCERNUS_EVIDENCE_CSV_v1>>>. The scores CSV must have columns for each dimension's score and salience, plus the calculated health scores. The evidence CSV must have columns for dimension, quote, and confidence. Phase 6: Output Specification: Return a complete response containing both a comprehensive JSON analysis and the embedded CSV segments as specified in the output_contract."
    }
  },
  "dimension_groups": {
    "procedural_axis": ["procedural_legitimacy", "procedural_rejection"],
    "institutional_axis": ["institutional_respect", "institutional_subversion"],
    "systemic_axis": ["systemic_continuity", "systemic_replacement"]
  },
  "calculation_spec": {
    "procedural_health_score": "(procedural_legitimacy - procedural_rejection)",
    "institutional_health_score": "(institutional_respect - institutional_subversion)", 
    "systemic_health_score": "(systemic_continuity - systemic_replacement)",
    "constitutional_direction_index": "(procedural_health_score + institutional_health_score + systemic_health_score) / 3"
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
      "constitutional_health_indices": "object"
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