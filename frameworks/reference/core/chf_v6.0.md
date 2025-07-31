# Constitutional Health Framework (CHF) v6.0
**Version**: 6.0
**Status**: Active
**Major Change**: JSON-First Architecture with Enhanced Synthesis Integration

---

## Overview

CHF v6.0 analyzes how political discourse affects constitutional system health through salience-enhanced assessment. Measures discourse impact across three dimensions of constitutional health, weighted by actual rhetorical emphasis patterns.

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
  "name": "chf_v6_0",
  "version": "v6.0",
  "display_name": "Constitutional Health Framework (CHF) v6.0",
  "analysis_variants": {
    "default": {
      "description": "Complete constitutional health analysis with salience weighting and JSON-first output.",
      "analysis_prompt": "Phase 1: Cognitive Priming: You are an expert constitutional health analyst with deep understanding of democratic institutional dynamics. Phase 2: Framework Methodology: Your task is to analyze the text using the Constitutional Health Framework (CHF) v6.0, which measures how political discourse affects constitutional system health through three critical axes. Phase 3: Operational Definitions: Evaluate six dimensions across three axes: Procedural (Legitimacy vs. Rejection), Institutional (Respect vs. Subversion), and Systemic (Continuity vs. Replacement). Each dimension receives a score (0.0-1.0), salience weight (0.0-1.0), and confidence rating (0.0-1.0). Phase 4: Scoring Protocol: For each dimension, provide ONLY: (1) score (0.0-1.0), (2) salience (0.0-1.0), (3) confidence (0.0-1.0), (4) evidence quotes with justification. Phase 5: JSON Structure Requirements: Your response must be a single, valid JSON object with nested structures for scores, evidence, reasoning, and salience ranking as specified in the output contract. Phase 6: Output Specification: Return structured JSON with raw dimensional scores only - NO calculations of health indices or derived metrics (these will be computed by code)."
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
      "constitutional_health_patterns": "object"
    },
    "structured_data_requirements": {
      "scores": {
        "description": "Nested object containing ONLY raw dimensional scores (NO calculated health indices)",
        "structure": {
          "dimensions": {
            "procedural_legitimacy": {
              "score": "number (0.0-1.0)",
              "salience": "number (0.0-1.0)",
              "confidence": "number (0.0-1.0)"
            },
            "procedural_rejection": {
              "score": "number (0.0-1.0)",
              "salience": "number (0.0-1.0)",
              "confidence": "number (0.0-1.0)"
            },
            "institutional_respect": {
              "score": "number (0.0-1.0)",
              "salience": "number (0.0-1.0)",
              "confidence": "number (0.0-1.0)"
            },
            "institutional_subversion": {
              "score": "number (0.0-1.0)",
              "salience": "number (0.0-1.0)",
              "confidence": "number (0.0-1.0)"
            },
            "systemic_continuity": {
              "score": "number (0.0-1.0)",
              "salience": "number (0.0-1.0)",
              "confidence": "number (0.0-1.0)"
            },
            "systemic_replacement": {
              "score": "number (0.0-1.0)",
              "salience": "number (0.0-1.0)",
              "confidence": "number (0.0-1.0)"
            }
          },
          "metadata": {
            "total_dimensions": "number",
            "analysis_completeness": "number (0.0-1.0)",
            "health_dominance": "number",
            "pathology_dominance": "number"
          }
        }
      },
      "evidence": {
        "description": "Nested object containing structured evidence data for audit and replication",
        "structure": {
          "by_dimension": {
            "procedural_legitimacy": [
              {
                "quote_id": "string",
                "quote_text": "string", 
                "confidence": "number (0.0-1.0)",
                "context_type": "string",
                "salience_justification": "string"
              }
            ],
            "procedural_rejection": "array_of_evidence_objects",
            "institutional_respect": "array_of_evidence_objects",
            "institutional_subversion": "array_of_evidence_objects",
            "systemic_continuity": "array_of_evidence_objects",
            "systemic_replacement": "array_of_evidence_objects"
          },
          "metadata": {
            "total_quotes": "number",
            "average_confidence": "number",
            "evidence_distribution": "object"
          }
        }
      }
    },
    "instructions": "IMPORTANT: Your response MUST be a single, valid JSON object containing all required fields with the nested structures specified above. The salience_ranking should be an ordered array of objects, each containing 'dimension', 'salience_score', and 'rank'. The constitutional_health_patterns should contain qualitative reasoning about health/pathology patterns (NO mathematical calculations). All numerical scores must be between 0.0 and 1.0. DO NOT compute health indices or derived metrics."
  }
}
```

</details>