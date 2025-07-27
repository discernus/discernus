# Constitutional Health Framework (CHF) v1.1
## Constitutional System Health Assessment with Salience-Weighted Analysis

---

## Overview

CHF v1.1 analyzes how political discourse affects constitutional system health through salience-enhanced assessment. Measures discourse impact across three dimensions of constitutional health, weighted by actual rhetorical emphasis patterns.

**Purpose**: Reveals whether discourse strengthens or weakens constitutional democracy by analyzing procedural legitimacy, institutional respect, and systemic continuity.

**Innovation**: Salience-weighted analysis captures not just constitutional health/pathology but which dimensions receive the most rhetorical emphasis.

**Applications**: Constitutional health monitoring, cross-system comparison, historical analysis, early warning systems.

---

## Salience-Enhanced Analysis

**Salience**: How much rhetorical emphasis the speaker places on each constitutional dimension, regardless of raw intensity scores.

**Key Insight**: Moderate support emphasized throughout discourse (0.6 intensity, 0.8 salience) reveals greater constitutional priority than intense attacks mentioned briefly (1.0 intensity, 0.2 salience).

**Why This Matters**: Enables empirically-backed constitutional assessment based on speakers' actual priority patterns rather than predetermined assumptions.

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

## Scoring Protocol

**Three-Step Process**:
1. **Standard Scoring**: Rate all 6 dimensions (0.0-1.0 intensity)
2. **Salience Assessment**: Evaluate rhetorical emphasis (0.0-1.0 salience) 
3. **Priority Analysis**: Rank dimensions by salience to reveal constitutional strategy

**Requirements**:
- Score all dimensions for intensity and salience
- Provide 1-2 strongest quotes per dimension
- Calculate health indices (health - pathology scores)
- Rank dimensions by salience

---

## Constitutional Health Calculations

- **Procedural Health**: Procedural Legitimacy - Procedural Rejection
- **Institutional Health**: Institutional Respect - Institutional Subversion  
- **Systemic Health**: Systemic Continuity - Systemic Replacement
- **Constitutional Direction Index**: Average of three health scores
- **Salience-Weighted Assessment**: Constitutional priorities based on emphasis patterns

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "constitutional_health_framework",
  "version": "v1.1", 
  "display_name": "Constitutional Health Framework (CHF) v1.1",
  "analysis_variants": {
    "default": {
      "description": "Complete constitutional health analysis with salience weighting",
      "analysis_prompt": "You are an expert constitutional health analyst specializing in democratic system assessment. Your task is to analyze the provided text using the Constitutional Health Framework (CHF) v1.1. This framework measures constitutional health through 6 dimensions: HEALTH DIMENSIONS: Procedural Legitimacy (support for established procedures), Institutional Respect (recognition of institutional authority), Systemic Continuity (support for constitutional framework). PATHOLOGY DIMENSIONS: Procedural Rejection (circumventing procedures), Institutional Subversion (attacking institutional authority), Systemic Replacement (advocating fundamental replacement). For each dimension, assess both intensity (0.0-1.0 how strongly expressed) and salience (0.0-1.0 how central to the message). Focus on constitutional health impact rather than policy positions. Provide 1-2 strongest quotes demonstrating each score. Calculate health indices: procedural (legitimacy-rejection), institutional (respect-subversion), systemic (continuity-replacement), and overall direction index. Rank dimensions by salience to reveal constitutional strategy priorities."
    }
  },
  "calculation_spec": {
    "procedural_health_score": "(procedural_legitimacy_score - procedural_rejection_score)",
    "institutional_health_score": "(institutional_respect_score - institutional_subversion_score)", 
    "systemic_health_score": "(systemic_continuity_score - systemic_replacement_score)",
    "constitutional_direction_index": "(procedural_health_score + institutional_health_score + systemic_health_score) / 3"
  },
  "output_contract": {
    "schema": {
      "analysis_summary": "string",
      "constitutional_scores": "object",
      "evidence": "object",
      "confidence": "object", 
      "salience_ranking": "array",
      "constitutional_health_indices": "object",
      "constitutional_strategy_analysis": "string"
    },
    "instructions": "IMPORTANT: Your response MUST be a single, valid JSON object and nothing else. Do not include any text, explanations, or markdown code fences before or after the JSON object. The constitutional_scores object should contain intensity scores (0.0-1.0) for all 6 dimensions. The salience_ranking should be an ordered array of objects, each containing 'dimension' (string), 'salience_score' (0.0-1.0), and 'rank' (integer), ordered from most salient (rank 1) to least salient (rank 6). The constitutional_health_indices should contain procedural_health_score, institutional_health_score, systemic_health_score, and constitutional_direction_index calculations."
  }
}
```

</details> 