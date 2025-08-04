# Populist Discourse Analysis Framework (PDAF) v5.0

**Version**: 5.0
**Status**: Active
**Major Change**: Embedded CSV Architecture for Synthesis Scalability

---

## Executive Summary

The Populist Discourse Analysis Framework (PDAF) v5.0 integrates breakthrough populist strategic tension analysis to provide a multi-dimensional assessment of populist discourse. It quantifies rhetorical contradictions within a speaker's populist strategy and calculates an overall Populist Strategic Contradiction Index (PSCI). This allows for a nuanced understanding of a speaker's strategic coherence and populist messaging.

---

## Framework Dimensions

### **Primary Populist Core Anchors**
1. **Manichaean People-Elite Framing** (0.0-2.0): Pure people vs corrupt elite moral dichotomy
2. **Crisis-Restoration Temporal Narrative** (0.0-2.0): Decline-crisis-redemption temporal structuring  
3. **Popular Sovereignty Claims** (0.0-2.0): Direct people's will as ultimate political authority
4. **Anti-Pluralist Exclusion** (0.0-2.0): Rejection of legitimate opposition and institutional constraints

### **Populist Mechanism Anchors**
5. **Elite Conspiracy/Systemic Corruption** (0.0-2.0): Elite coordination against people's interests
6. **Authenticity vs. Political Class** (0.0-2.0): Genuine representation vs professional politician artifice  
7. **Homogeneous People Construction** (0.0-2.0): Unified people identity transcending internal divisions

### **Boundary Distinction Anchors**  
8. **Nationalist Exclusion** (0.0-2.0): Cultural/ethnic homogeneity and external threat emphasis
9. **Economic Populist Appeals** (0.0-2.0): Populist economic discourse regardless of ideological direction

### **Descriptive Classification Anchor**
10. **Economic Direction Indicator** (Categorical): Redistributive vs Nationalist economic orientation

---

## Populist Tension Mathematics

### **Populist Strategic Tension Scoring**

**Formula**: `Populist Tension = min(Anchor_A_score, Anchor_B_score) × |Anchor_A_salience - Anchor_B_salience|`

### **Populist Strategic Contradiction Index (PSCI)**

**Formula**: `PSCI = (Sum of all Populist Tension Scores) / Number of Tension Pairs`

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "pdaf_v5_0",
  "version": "v5.0",
  "display_name": "Populist Discourse Analysis Framework (PDAF) v5.0",
  "analysis_variants": {
    "default": {
      "description": "Complete salience-weighted populist analysis with strategic tension pattern quantification and embedded CSV output.",
      "analysis_prompt": "Phase 1: Cognitive Priming: You are an expert populist discourse analyst. Phase 2: Framework Methodology: Your task is to analyze the text using the Populist Discourse Analysis Framework (PDAF) v5.0. Phase 3: Operational Definitions: Evaluate nine populist anchors, including Manichaean People-Elite Framing, Crisis-Restoration Narrative, Popular Sovereignty Claims, and others. Also, classify the Economic Direction. Phase 4: Scoring Protocol: For each of the nine anchors, score its intensity (0.0-2.0) and salience (0.0-1.0). Provide the strongest 1-2 quotes as evidence. Calculate tension scores for three strategic pairs and the overall Populist Strategic Contradiction Index (PSCI). Phase 5: Embedded CSV Generation: CRITICAL: Your response must include two embedded CSV segments using these exact delimiters: <<<DISCERNUS_SCORES_CSV_v1>>> and <<<DISCERNUS_EVIDENCE_CSV_v1>>>. The scores CSV must have columns for each anchor's score and salience, each tension score, and the PSCI. The evidence CSV must have columns for anchor, quote, and confidence. Phase 6: Output Specification: Return a complete response containing both a comprehensive JSON analysis and the embedded CSV segments as specified in the output_contract."
    }
  },
  "dimension_groups": {
    "core_anchors": ["manichaean_people_elite_framing", "crisis_restoration_narrative", "popular_sovereignty_claims", "anti_pluralist_exclusion"],
    "mechanism_anchors": ["elite_conspiracy_systemic_corruption", "authenticity_vs_political_class", "homogeneous_people_construction"],
    "boundary_anchors": ["nationalist_exclusion", "economic_populist_appeals"]
  },
  "calculation_spec": {
    "populist_strategic_tension_mathematics": "Populist strategic tension quantification using formula: Populist Tension = min(Anchor_A_score, Anchor_B_score) × |Anchor_A_salience - Anchor_B_salience|.",
    "populist_strategic_tensions": {
      "democratic_authoritarian_tension": "min(popular_sovereignty_claims, anti_pluralist_exclusion) * abs(popular_sovereignty_claims_salience - anti_pluralist_exclusion_salience)",
      "internal_external_focus_tension": "min(homogeneous_people_construction, nationalist_exclusion) * abs(homogeneous_people_construction_salience - nationalist_exclusion_salience)",
      "crisis_elite_attribution_tension": "min(crisis_restoration_narrative, elite_conspiracy_systemic_corruption) * abs(crisis_restoration_narrative_salience - elite_conspiracy_systemic_corruption_salience)"
    },
    "populist_strategic_contradiction_index": "(democratic_authoritarian_tension + internal_external_focus_tension + crisis_elite_attribution_tension) / 3"
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
    "instructions": "IMPORTANT: Your response MUST include both a complete JSON analysis AND embedded CSV segments using the exact delimiters specified. The salience_ranking should be an ordered array of objects, each containing 'anchor', 'salience_score', and 'rank'."
  }
}
```

</details> 