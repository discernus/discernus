# Constitutional Health Framework (CHF) v7.1
**Version**: 7.1
**Status**: Active
**Major Change**: Enhanced Gasket Schema with Metadata Scores and Advanced Extraction Patterns

---

## Overview

CHF v7.1 analyzes how political discourse affects constitutional system health through enhanced metadata analysis. Measures discourse impact across three dimensions of constitutional health, with advanced extraction patterns and validation rules for robust analysis.

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
    ]
  }
}
```

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "chf_v7_1",
  "version": "v7.1",
  "display_name": "Constitutional Health Framework (CHF) v7.1",
  "analysis_variants": {
    "default": {
      "description": "Complete constitutional health analysis with salience weighting and raw analysis log output.",
      "analysis_prompt": "You are an expert constitutional health analyst with deep understanding of democratic institutional dynamics. Your task is to analyze the provided text using the Constitutional Health Framework (CHF) v7.1, which measures how political discourse affects constitutional system health through three critical axes with enhanced metadata reporting.\n\nThe framework evaluates discourse across three constitutional axes:\n\n**Procedural Axis**: Procedural Legitimacy (0.0-1.0) - support for established procedures for political change and governance vs. Procedural Rejection (0.0-1.0) - rejecting established procedures in favor of circumvention or extra-constitutional action.\n\n**Institutional Axis**: Institutional Respect (0.0-1.0) - recognition of institutional authority, expertise, and legitimate governance role vs. Institutional Subversion (0.0-1.0) - attacking institutional authority, expertise, or legitimate governance role.\n\n**Systemic Axis**: Systemic Continuity (0.0-1.0) - support for maintaining and improving existing constitutional framework vs. Systemic Replacement (0.0-1.0) - advocating fundamental replacement rather than reform of constitutional framework.\n\nFor each dimension, provide:\n- **Score (0.0-1.0)**: Based on strength of evidence in the text\n- **Salience (0.0-1.0)**: How central is this dimension to this specific text?\n- **Confidence (0.0-1.0)**: How certain are you in this assessment?\n\nWrite a comprehensive analytical report that covers:\n- Application of the CHF methodology to this specific text\n- Detailed analysis of each relevant dimension with scores, salience, confidence, and evidence\n- Assessment of constitutional health vs. pathology patterns\n- Overall constitutional direction profile with salience weighting\n- Key insights about the speaker's constitutional approach\n\nEmbed your numerical assessments naturally within the analysis. For example: 'This text demonstrates strong procedural legitimacy (procedural legitimacy score: 0.8, salience: 0.9, confidence: 0.7) with frequent references to constitutional processes.' Focus on rigorous intellectual analysis supported by direct textual evidence and clear reasoning for all scores and metadata."
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
    "version": "7.1",
    "extraction_method": "intelligent_extractor",
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
    "extraction_patterns": {
      "procedural_legitimacy_score": ["procedural.{0,20}legitimacy.{0,20}score", "procedural.{0,20}legitimacy.{0,20}rating", "legitimacy\\s*:\\s*[0-9]"],
      "procedural_rejection_score": ["procedural.{0,20}rejection.{0,20}score", "procedural.{0,20}rejection.{0,20}rating", "rejection\\s*:\\s*[0-9]"],
      "institutional_respect_score": ["institutional.{0,20}respect.{0,20}score", "institutional.{0,20}respect.{0,20}rating", "respect\\s*:\\s*[0-9]"],
      "institutional_subversion_score": ["institutional.{0,20}subversion.{0,20}score", "institutional.{0,20}subversion.{0,20}rating", "subversion\\s*:\\s*[0-9]"],
      "systemic_continuity_score": ["systemic.{0,20}continuity.{0,20}score", "systemic.{0,20}continuity.{0,20}rating", "continuity\\s*:\\s*[0-9]"],
      "systemic_replacement_score": ["systemic.{0,20}replacement.{0,20}score", "systemic.{0,20}replacement.{0,20}rating", "replacement\\s*:\\s*[0-9]"],
      "procedural_legitimacy_salience": ["procedural.{0,20}legitimacy.{0,20}salience", "legitimacy.{0,20}importance", "legitimacy.{0,20}centrality"],
      "procedural_rejection_salience": ["procedural.{0,20}rejection.{0,20}salience", "rejection.{0,20}importance", "rejection.{0,20}centrality"],
      "institutional_respect_salience": ["institutional.{0,20}respect.{0,20}salience", "respect.{0,20}importance", "respect.{0,20}centrality"],
      "institutional_subversion_salience": ["institutional.{0,20}subversion.{0,20}salience", "subversion.{0,20}importance", "subversion.{0,20}centrality"],
      "systemic_continuity_salience": ["systemic.{0,20}continuity.{0,20}salience", "continuity.{0,20}importance", "continuity.{0,20}centrality"],
      "systemic_replacement_salience": ["systemic.{0,20}replacement.{0,20}salience", "replacement.{0,20}importance", "replacement.{0,20}centrality"],
      "procedural_legitimacy_confidence": ["procedural.{0,20}legitimacy.{0,20}confidence", "legitimacy.{0,20}certainty", "legitimacy.{0,20}sure"],
      "procedural_rejection_confidence": ["procedural.{0,20}rejection.{0,20}confidence", "rejection.{0,20}certainty", "rejection.{0,20}sure"],
      "institutional_respect_confidence": ["institutional.{0,20}respect.{0,20}confidence", "respect.{0,20}certainty", "respect.{0,20}sure"],
      "institutional_subversion_confidence": ["institutional.{0,20}subversion.{0,20}confidence", "subversion.{0,20}certainty", "subversion.{0,20}sure"],
      "systemic_continuity_confidence": ["systemic.{0,20}continuity.{0,20}confidence", "continuity.{0,20}certainty", "continuity.{0,20}sure"],
      "systemic_replacement_confidence": ["systemic.{0,20}replacement.{0,20}confidence", "replacement.{0,20}certainty", "replacement.{0,20}sure"]
    },
    "validation_rules": {
      "required_fields": [
        "procedural_legitimacy_score", "procedural_rejection_score", "institutional_respect_score",
        "institutional_subversion_score", "systemic_continuity_score", "systemic_replacement_score"
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