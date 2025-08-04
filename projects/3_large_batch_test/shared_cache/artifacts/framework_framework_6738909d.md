# Populist Discourse Analysis Framework (PDAF) v7.1
**Version**: 7.1
**Status**: Active
**Major Change**: Enhanced Gasket Schema with Metadata Scores and Advanced Extraction Patterns

---

## Executive Summary

The Populist Discourse Analysis Framework (PDAF) v7.1 integrates breakthrough populist strategic tension analysis to provide a multi-dimensional assessment of populist discourse. It quantifies rhetorical contradictions within a speaker's populist strategy and calculates an overall Populist Strategic Contradiction Index (PSCI). This version includes enhanced gasket schema with metadata scores (salience and confidence) and advanced extraction patterns for robust populist discourse analysis.

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

## Gasket Architecture

### Raw Analysis Log Format
The analysis agent outputs a raw analysis log containing:
- Populist anchor scores for all 9 dimensions
- Salience weights for each dimension
- Evidence quotes with confidence ratings
- Qualitative reasoning about populist patterns

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "pdaf_v7_1",
  "version": "v7.1",
  "display_name": "Populist Discourse Analysis Framework (PDAF) v7.1",
  "analysis_variants": {
    "default": {
      "description": "Complete salience-weighted populist analysis with strategic tension pattern quantification and raw analysis log output.",
      "analysis_prompt": "Phase 1: Cognitive Priming: You are an expert populist discourse analyst with deep understanding of populist rhetorical strategies across different political contexts. Phase 2: Framework Methodology: Your task is to analyze the text using the Populist Discourse Analysis Framework (PDAF) v7.1, which measures populist discourse patterns through nine core anchors and strategic tension analysis. Phase 3: Operational Definitions: Evaluate nine populist anchors: Manichaean People-Elite Framing, Crisis-Restoration Narrative, Popular Sovereignty Claims, Anti-Pluralist Exclusion, Elite Conspiracy/Systemic Corruption, Authenticity vs Political Class, Homogeneous People Construction, Nationalist Exclusion, and Economic Populist Appeals. Also classify the Economic Direction Indicator. Phase 4: Scoring Protocol: For each of the nine anchors, provide ONLY: (1) intensity score (0.0-2.0), (2) salience (0.0-1.0), (3) confidence (0.0-1.0), (4) evidence quotes with justification. For Economic Direction Indicator, provide categorical classification. Phase 5: Raw Analysis Log Requirements: Your response must be a raw analysis log containing anchor scores, evidence, and reasoning - NO JSON structure or derived calculations. Phase 6: Output Specification: Return raw analysis log with dimensional scores only - NO calculation of tension scores or PSCI (these will be computed by code)."
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
  "gasket_schema": {
    "version": "7.1",
    "extraction_method": "intelligent_extractor",
    "target_keys": [
      "manichaean_people_elite_framing_score",
      "crisis_restoration_narrative_score",
      "popular_sovereignty_claims_score",
      "anti_pluralist_exclusion_score",
      "elite_conspiracy_systemic_corruption_score",
      "authenticity_vs_political_class_score",
      "homogeneous_people_construction_score",
      "nationalist_exclusion_score",
      "economic_populist_appeals_score",
      "manichaean_people_elite_framing_salience",
      "crisis_restoration_narrative_salience",
      "popular_sovereignty_claims_salience",
      "anti_pluralist_exclusion_salience",
      "elite_conspiracy_systemic_corruption_salience",
      "authenticity_vs_political_class_salience",
      "homogeneous_people_construction_salience",
      "nationalist_exclusion_salience",
      "economic_populist_appeals_salience",
      "manichaean_people_elite_framing_confidence",
      "crisis_restoration_narrative_confidence",
      "popular_sovereignty_claims_confidence",
      "anti_pluralist_exclusion_confidence",
      "elite_conspiracy_systemic_corruption_confidence",
      "authenticity_vs_political_class_confidence",
      "homogeneous_people_construction_confidence",
      "nationalist_exclusion_confidence",
      "economic_populist_appeals_confidence"
    ],
    "extraction_patterns": {
      "manichaean_people_elite_framing_score": ["manichaean.{0,20}people.{0,20}elite.{0,20}framing.{0,20}score", "manichaean.{0,20}score", "people.{0,20}elite.{0,20}score"],
      "crisis_restoration_narrative_score": ["crisis.{0,20}restoration.{0,20}narrative.{0,20}score", "crisis.{0,20}restoration.{0,20}score"],
      "popular_sovereignty_claims_score": ["popular.{0,20}sovereignty.{0,20}claims.{0,20}score", "popular.{0,20}sovereignty.{0,20}score", "sovereignty.{0,20}score"],
      "anti_pluralist_exclusion_score": ["anti.{0,20}pluralist.{0,20}exclusion.{0,20}score", "anti.{0,20}pluralist.{0,20}score", "pluralist.{0,20}exclusion.{0,20}score"],
      "elite_conspiracy_systemic_corruption_score": ["elite.{0,20}conspiracy.{0,20}systemic.{0,20}corruption.{0,20}score", "elite.{0,20}conspiracy.{0,20}score", "systemic.{0,20}corruption.{0,20}score"],
      "authenticity_vs_political_class_score": ["authenticity.{0,20}vs.{0,20}political.{0,20}class.{0,20}score", "authenticity.{0,20}political.{0,20}class.{0,20}score", "authenticity.{0,20}score"],
      "homogeneous_people_construction_score": ["homogeneous.{0,20}people.{0,20}construction.{0,20}score", "homogeneous.{0,20}people.{0,20}score"],
      "nationalist_exclusion_score": ["nationalist.{0,20}exclusion.{0,20}score", "nationalist.{0,20}score"],
      "economic_populist_appeals_score": ["economic.{0,20}populist.{0,20}appeals.{0,20}score", "economic.{0,20}populist.{0,20}score"],
      "manichaean_people_elite_framing_salience": ["manichaean.{0,20}people.{0,20}elite.{0,20}framing.{0,20}salience", "manichaean.{0,20}salience"],
      "crisis_restoration_narrative_salience": ["crisis.{0,20}restoration.{0,20}narrative.{0,20}salience", "crisis.{0,20}restoration.{0,20}salience"],
      "popular_sovereignty_claims_salience": ["popular.{0,20}sovereignty.{0,20}claims.{0,20}salience", "popular.{0,20}sovereignty.{0,20}salience"],
      "anti_pluralist_exclusion_salience": ["anti.{0,20}pluralist.{0,20}exclusion.{0,20}salience", "anti.{0,20}pluralist.{0,20}salience"],
      "elite_conspiracy_systemic_corruption_salience": ["elite.{0,20}conspiracy.{0,20}systemic.{0,20}corruption.{0,20}salience", "elite.{0,20}conspiracy.{0,20}salience"],
      "authenticity_vs_political_class_salience": ["authenticity.{0,20}vs.{0,20}political.{0,20}class.{0,20}salience", "authenticity.{0,20}salience"],
      "homogeneous_people_construction_salience": ["homogeneous.{0,20}people.{0,20}construction.{0,20}salience", "homogeneous.{0,20}people.{0,20}salience"],
      "nationalist_exclusion_salience": ["nationalist.{0,20}exclusion.{0,20}salience", "nationalist.{0,20}salience"],
      "economic_populist_appeals_salience": ["economic.{0,20}populist.{0,20}appeals.{0,20}salience", "economic.{0,20}populist.{0,20}salience"],
      "manichaean_people_elite_framing_confidence": ["manichaean.{0,20}people.{0,20}elite.{0,20}framing.{0,20}confidence", "manichaean.{0,20}confidence"],
      "crisis_restoration_narrative_confidence": ["crisis.{0,20}restoration.{0,20}narrative.{0,20}confidence", "crisis.{0,20}restoration.{0,20}confidence"],
      "popular_sovereignty_claims_confidence": ["popular.{0,20}sovereignty.{0,20}claims.{0,20}confidence", "popular.{0,20}sovereignty.{0,20}confidence"],
      "anti_pluralist_exclusion_confidence": ["anti.{0,20}pluralist.{0,20}exclusion.{0,20}confidence", "anti.{0,20}pluralist.{0,20}confidence"],
      "elite_conspiracy_systemic_corruption_confidence": ["elite.{0,20}conspiracy.{0,20}systemic.{0,20}corruption.{0,20}confidence", "elite.{0,20}conspiracy.{0,20}confidence"],
      "authenticity_vs_political_class_confidence": ["authenticity.{0,20}vs.{0,20}political.{0,20}class.{0,20}confidence", "authenticity.{0,20}confidence"],
      "homogeneous_people_construction_confidence": ["homogeneous.{0,20}people.{0,20}construction.{0,20}confidence", "homogeneous.{0,20}people.{0,20}confidence"],
      "nationalist_exclusion_confidence": ["nationalist.{0,20}exclusion.{0,20}confidence", "nationalist.{0,20}confidence"],
      "economic_populist_appeals_confidence": ["economic.{0,20}populist.{0,20}appeals.{0,20}confidence", "economic.{0,20}populist.{0,20}confidence"]
    },
    "validation_rules": {
      "required_fields": [
        "manichaean_people_elite_framing_score", "crisis_restoration_narrative_score", "popular_sovereignty_claims_score", "anti_pluralist_exclusion_score",
        "elite_conspiracy_systemic_corruption_score", "authenticity_vs_political_class_score", "homogeneous_people_construction_score", "nationalist_exclusion_score", "economic_populist_appeals_score"
      ],
      "score_ranges": {"min": 0.0, "max": 2.0},
      "metadata_ranges": {
        "salience": {"min": 0.0, "max": 1.0},
        "confidence": {"min": 0.0, "max": 1.0}
      },
      "fallback_strategy": "use_default_values"
    }
  },
  "raw_analysis_log_format": {
    "description": "Raw analysis log containing anchor scores, evidence, and reasoning without structured JSON",
    "content": "Free-form text with populist discourse analysis including scores, evidence quotes, and qualitative reasoning"
  }
}
```

</details> 