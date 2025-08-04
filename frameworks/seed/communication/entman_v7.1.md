# Entman Framing Functions Framework v7.1

**Version**: 7.1  
**Status**: Active  
**Major Change**: Enhanced Gasket Schema with Metadata Scores and Advanced Extraction Patterns

---

## Overview

The Entman Framing Functions Framework v7.1 implements Robert Entman's systematic communication analysis through four independent framing functions with enhanced metadata scoring. This framework tests whether Problem Definition, Causal Attribution, Moral Evaluation, and Treatment Recommendation operate independently as predicted by communication theory, representing systematic message construction in political discourse.

**Purpose**: Analyzes strategic communication through four independent framing functions with enhanced extraction patterns and validation rules for comprehensive message analysis.

**Innovation**: Systematic communication analysis based on Entman's foundational framing theory examining message construction through distinct framing functions.

**Applications**: Communication analysis, framing studies, political message assessment, strategic communication evaluation.

---

## Framework Dimensions

### **Communication Framing Functions**

#### Problem Definition (0.0-1.0)
**Definition**: What issues are identified as requiring attention and how problems are conceptualized.
**Key Markers**: "the real issue is," "we face a crisis of," "the challenge before us," "the problem we must address," "the urgent need to," "what's really at stake," "the fundamental issue," "the core problem," "immediate action required," "crisis demands response"

#### Causal Attribution (0.0-1.0)
**Definition**: What factors or actors are presented as causing problems and how responsibility is assigned.
**Key Markers**: "X is responsible for," "this stems from Y's actions," "the fault lies with," "caused by," "due to," "blame," "accountable for," "at fault," "structural problems require," "the system creates," "institutional factors," "the roots of this problem"

#### Moral Evaluation (0.0-1.0)
**Definition**: What values and moral judgments are invoked and how actions are evaluated ethically.
**Key Markers**: "justice demands," "fairness requires," "liberty is at stake," "fundamental rights," "core values," "moral imperative," "ethical obligation," "principle at stake," "this is fundamentally wrong," "ethically unacceptable," "morally justified," "right thing to do"

#### Treatment Recommendation (0.0-1.0)
**Definition**: What solutions are proposed and how policy options are presented and prioritized.  
**Key Markers**: "we must immediately," "the answer is," "the only way forward," "solution requires," "we should," "necessary action," "recommended approach," "best path forward," "specific steps include," "concrete measures," "detailed implementation," "policy proposal"

---

## Gasket Architecture

### Raw Analysis Log Format
The analysis agent outputs a raw analysis log containing:
- Framing function scores for all 4 functions
- Salience weights for each function
- Evidence quotes with confidence ratings
- Qualitative reasoning about framing patterns

### Intelligent Extractor Schema
```json
{
  "gasket_schema": {
    "target_keys": [
      "problem_definition_score",
      "causal_attribution_score",
      "moral_evaluation_score",
      "treatment_recommendation_score",
      "problem_definition_salience",
      "causal_attribution_salience",
      "moral_evaluation_salience",
      "treatment_recommendation_salience",
      "problem_definition_confidence",
      "causal_attribution_confidence",
      "moral_evaluation_confidence",
      "treatment_recommendation_confidence"
    ],
    "target_dimensions": [
      "message_completeness_score",
      "framing_coherence_index"
    ]
  }
}
```

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "entman_v7_1",
  "version": "v7.1",
  "display_name": "Entman Framing Functions Framework v7.1",
  "analysis_variants": {
    "default": {
      "description": "Complete four-function framing analysis with raw analysis log output.",
      "analysis_prompt": "Phase 1: Cognitive Priming: You are an expert analyst specializing in communication framing and strategic messaging across diverse contexts. Phase 2: Framework Methodology: Your task is to analyze the provided text using the Entman Framing Functions Framework v7.1, which captures communication patterns through four independent framing functions with enhanced metadata scoring. Phase 3: Operational Definitions: Evaluate 4 framing functions: Problem Definition, Causal Attribution, Moral Evaluation, and Treatment Recommendation. Each function receives a score (0.0-1.0), salience weight (0.0-1.0), and confidence rating (0.0-1.0). Phase 4: Scoring Protocol: For each function, provide ONLY: (1) score (0.0-1.0), (2) salience (0.0-1.0), (3) confidence (0.0-1.0), (4) evidence quotes with justification. Phase 5: Raw Analysis Log Requirements: Your response must be a raw analysis log containing function scores, evidence, and reasoning - NO JSON structure or derived calculations. Phase 6: Output Specification: Return raw analysis log with function scores only - NO calculations of message indices or derived metrics (these will be computed by code)."
    }
  },
  "dimension_groups": {
    "framing_functions": ["problem_definition", "causal_attribution", "moral_evaluation", "treatment_recommendation"]
  },
  "calculation_spec": {
    "message_completeness_score": "(problem_definition_score + causal_attribution_score + moral_evaluation_score + treatment_recommendation_score) / 4",
    "framing_coherence_index": "sqrt(problem_definition_score * causal_attribution_score * moral_evaluation_score * treatment_recommendation_score)"
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
      "problem_definition_score",
      "causal_attribution_score",
      "moral_evaluation_score",
      "treatment_recommendation_score",
      "problem_definition_salience",
      "causal_attribution_salience",
      "moral_evaluation_salience",
      "treatment_recommendation_salience",
      "problem_definition_confidence",
      "causal_attribution_confidence",
      "moral_evaluation_confidence",
      "treatment_recommendation_confidence"
    ],
    "extraction_patterns": {
      "problem_definition_score": ["problem.{0,20}definition.{0,20}score"],
      "causal_attribution_score": ["causal.{0,20}attribution.{0,20}score"],
      "moral_evaluation_score": ["moral.{0,20}evaluation.{0,20}score"],
      "treatment_recommendation_score": ["treatment.{0,20}recommendation.{0,20}score"],
      "problem_definition_salience": ["problem.{0,20}definition.{0,20}salience"],
      "causal_attribution_salience": ["causal.{0,20}attribution.{0,20}salience"],
      "moral_evaluation_salience": ["moral.{0,20}evaluation.{0,20}salience"],
      "treatment_recommendation_salience": ["treatment.{0,20}recommendation.{0,20}salience"],
      "problem_definition_confidence": ["problem.{0,20}definition.{0,20}confidence"],
      "causal_attribution_confidence": ["causal.{0,20}attribution.{0,20}confidence"],
      "moral_evaluation_confidence": ["moral.{0,20}evaluation.{0,20}confidence"],
      "treatment_recommendation_confidence": ["treatment.{0,20}recommendation.{0,20}confidence"]
    },
    "validation_rules": {
      "required_fields": [
        "problem_definition_score", "causal_attribution_score", "moral_evaluation_score", "treatment_recommendation_score"
      ],
      "score_ranges": {"min": 0.0, "max": 1.0},
      "metadata_ranges": {
        "salience": {"min": 0.0, "max": 1.0},
        "confidence": {"min": 0.0, "max": 1.0}
      },
      "fallback_strategy": "use_default_values"
    }
  },
  "raw_analysis_log_format": {
    "description": "Raw analysis log containing framing function scores, evidence, and reasoning without structured JSON",
    "content": "Free-form text with communication framing analysis including scores, evidence quotes, and qualitative reasoning"
  }
}
```

</details>