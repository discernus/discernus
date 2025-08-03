# Constitutional Health Framework (CHF) v7.0
**Version**: 7.0
**Status**: Active
**Major Change**: Gasket Architecture with Raw Analysis Log

---

## Overview

CHF v7.0 analyzes how political discourse affects constitutional system health through salience-enhanced assessment. Measures discourse impact across three dimensions of constitutional health, weighted by actual rhetorical emphasis patterns.

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

## Gasket Architecture

### Raw Analysis Log Format
The analysis agent outputs a raw analysis log containing:
- Constitutional health scores for all 6 dimensions
- Salience weights for each dimension
- Evidence quotes with confidence ratings
- Qualitative reasoning about constitutional patterns

### Intelligent Extractor Schema
```json
{
  "gasket_schema": {
    "target_keys": [
      "procedural_legitimacy_score",
      "procedural_rejection_score", 
      "institutional_respect_score",
      "institutional_subversion_score",
      "systemic_continuity_score",
      "systemic_replacement_score",
      "procedural_legitimacy_salience",
      "procedural_rejection_salience",
      "institutional_respect_salience",
      "institutional_subversion_salience", 
      "systemic_continuity_salience",
      "systemic_replacement_salience",
      "procedural_legitimacy_confidence",
      "procedural_rejection_confidence",
      "institutional_respect_confidence",
      "institutional_subversion_confidence",
      "systemic_continuity_confidence",
      "systemic_replacement_confidence"
    ],
    "target_dimensions": [
      "procedural_health_score",
      "institutional_health_score", 
      "systemic_health_score",
      "constitutional_direction_index"
    ]
  }
}
```

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "chf_v7_0",
  "version": "v7.0",
  "display_name": "Constitutional Health Framework (CHF) v7.0",
  "analysis_variants": {
    "default": {
      "description": "Complete constitutional health analysis with salience weighting and raw analysis log output.",
      "analysis_prompt": "Phase 1: Cognitive Priming: You are an expert constitutional health analyst with deep understanding of democratic institutional dynamics. Phase 2: Framework Methodology: Your task is to analyze the text using the Constitutional Health Framework (CHF) v7.0, which measures how political discourse affects constitutional system health through three critical axes. Phase 3: Operational Definitions: Evaluate six dimensions across three axes: Procedural (Legitimacy vs. Rejection), Institutional (Respect vs. Subversion), and Systemic (Continuity vs. Replacement). Each dimension receives a score (0.0-1.0), salience weight (0.0-1.0), and confidence rating (0.0-1.0). Phase 4: Scoring Protocol: For each dimension, provide ONLY: (1) score (0.0-1.0), (2) salience (0.0-1.0), (3) confidence (0.0-1.0), (4) evidence quotes with justification. Phase 5: Raw Analysis Log Requirements: Your response must be a raw analysis log containing dimensional scores, evidence, and reasoning - NO JSON structure or derived calculations. Phase 6: Output Specification: Return raw analysis log with dimensional scores only - NO calculations of health indices or derived metrics (these will be computed by code)."
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
  "gasket_schema": {
    "target_keys": [
      "procedural_legitimacy_score",
      "procedural_rejection_score", 
      "institutional_respect_score",
      "institutional_subversion_score",
      "systemic_continuity_score",
      "systemic_replacement_score",
      "procedural_legitimacy_salience",
      "procedural_rejection_salience",
      "institutional_respect_salience",
      "institutional_subversion_salience", 
      "systemic_continuity_salience",
      "systemic_replacement_salience",
      "procedural_legitimacy_confidence",
      "procedural_rejection_confidence",
      "institutional_respect_confidence",
      "institutional_subversion_confidence",
      "systemic_continuity_confidence",
      "systemic_replacement_confidence"
    ],
    "target_dimensions": [
      "procedural_health_score",
      "institutional_health_score", 
      "systemic_health_score",
      "constitutional_direction_index"
    ]
  },
  "raw_analysis_log_format": {
    "description": "Raw analysis log containing dimensional scores, evidence, and reasoning without structured JSON",
    "content": "Free-form text with constitutional health analysis including scores, evidence quotes, and qualitative reasoning"
  }
}
```

</details> 