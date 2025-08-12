# Entman Framing Functions Framework v7.3

**Version**: 7.3  
**Status**: Active  
**Major Change**: Enhanced Gasket Schema with Metadata Scores and Advanced Extraction Patterns

---

## Overview

The Entman Framing Functions Framework v7.3 implements Robert Entman's systematic communication analysis through four independent framing functions with enhanced metadata scoring. This framework tests whether Problem Definition, Causal Attribution, Moral Evaluation, and Treatment Recommendation operate independently as predicted by communication theory, representing systematic message construction in political discourse.

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
    ]
  }
}
```

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "entman_v7_1",
  "version": "v7.3",
  "display_name": "Entman Framing Functions Framework v7.1",
  "analysis_variants": {
    "default": {
      "description": "Sequential framing functions analysis with chain-of-thought methodology",
      "analysis_prompt": "You are an expert analyst specializing in communication framing and strategic messaging across diverse contexts. Analyze this text through focused sequential steps, examining each framing function independently before integration.\n\nSTEP 1 - PROBLEM DEFINITION ANALYSIS\nFocus ONLY on problem definition patterns (ignore other framing functions for now):\n- Look for problem identification markers: issue language ('the real issue is,' 'we face a crisis of,' 'the challenge before us,' 'the problem we must address,' 'what's really at stake') - Note: These are semantic concepts, look for how problems are conceptualized and what issues are identified as requiring attention, not just these exact phrases\n- Assess problem framing completeness and clarity\n- Score problem definition dimension (0.0-1.0) with specific textual evidence\n- Assess salience (0.0-1.0): How central is problem definition to this specific text?\n- State confidence (0.0-1.0): How certain are you in this assessment?\nShow your analytical work and evidence before proceeding.\n\nSTEP 2 - CAUSAL ATTRIBUTION ANALYSIS\nNow focus ONLY on causal attribution patterns:\n- Look for causal attribution markers: responsibility language ('X is responsible for,' 'this stems from Y's actions,' 'the fault lies with,' 'caused by,' 'accountable for,' 'the roots of this problem') - Note: These are semantic concepts, look for how responsibility is assigned and what factors are presented as causing problems, not just these exact terms\n- Assess attribution clarity and responsibility assignment\n- Score causal attribution dimension (0.0-1.0) with specific textual evidence\n- Assess salience (0.0-1.0): How central is causal attribution to the message?\n- State confidence (0.0-1.0): How certain are you in this assessment?\nShow your analytical work and evidence before proceeding.\n\nSTEP 3 - MORAL EVALUATION ANALYSIS\nNow focus ONLY on moral evaluation patterns:\n- Look for moral evaluation markers: values language ('justice demands,' 'fairness requires,' 'liberty is at stake,' 'fundamental rights,' 'moral imperative,' 'ethically unacceptable') - Note: These are semantic concepts, look for what values and moral judgments are invoked and how actions are evaluated ethically, not just these exact expressions\n- Assess moral framework clarity and ethical positioning\n- Score moral evaluation dimension (0.0-1.0) with specific textual evidence\n- Assess salience (0.0-1.0): How central are moral evaluations to the message?\n- State confidence (0.0-1.0): How certain are you in this assessment?\nShow your analytical work and evidence before proceeding.\n\nSTEP 4 - TREATMENT RECOMMENDATION ANALYSIS\nNow focus ONLY on treatment recommendation patterns:\n- Look for treatment recommendation markers: solution language ('we must immediately,' 'the answer is,' 'the only way forward,' 'solution requires,' 'necessary action,' 'concrete measures') - Note: These are semantic concepts, look for what solutions are proposed and how policy options are presented and prioritized, not just these exact recommendations\n- Assess solution clarity and policy direction\n- Score treatment recommendation dimension (0.0-1.0) with specific textual evidence\n- Assess salience (0.0-1.0): How central are treatment recommendations to the message?\n- State confidence (0.0-1.0): How certain are you in this assessment?\nShow your analytical work and evidence before proceeding.\n\nFINAL STEP - INTEGRATION AND VALIDATION\nReview your step-by-step analysis:\n- Check for scoring consistency across all framing functions\n- Validate that evidence quality meets academic standards\n- Assess systematic message construction and framing completeness\n- Confirm confidence levels are appropriately calibrated\n- Identify strategic framing patterns and communication profile\n- Apply pattern classifications based on overall framing approach\n\nProvide your final structured analysis following this format:\n\n**FRAMING FUNCTIONS ASSESSMENT**\n\n**Problem Definition**: [score] (salience: [score], confidence: [score])\n**Causal Attribution**: [score] (salience: [score], confidence: [score])\n**Moral Evaluation**: [score] (salience: [score], confidence: [score])\n**Treatment Recommendation**: [score] (salience: [score], confidence: [score])\n\n**Calculated Metrics**:\n- Message Completeness Index: [calculated score]\n- Strategic Framing Profile: [classification]\n\n**Key Insights**: [Summary of framing strategy, message construction patterns, and communication effectiveness]"
    }
  },
  "dimension_groups": {
    "framing_functions": ["problem_definition", "causal_attribution", "moral_evaluation", "treatment_recommendation"]
  },
  "calculation_spec": {
    "execution_order": [
      "message_completeness_score",
      "framing_coherence_index",
      "salience_weighted_message_completeness_score",
      "salience_weighted_framing_coherence_index"
    ],
    "formulas": {
      "message_completeness_score": "(problem_definition_score + causal_attribution_score + moral_evaluation_score + treatment_recommendation_score) / 4",
    "framing_coherence_index": "sqrt(problem_definition_score * causal_attribution_score * moral_evaluation_score * treatment_recommendation_score)",
    "salience_weighted_message_completeness_score": "(problem_definition_score * problem_definition_salience + causal_attribution_score * causal_attribution_salience + moral_evaluation_score * moral_evaluation_salience + treatment_recommendation_score * treatment_recommendation_salience) / (problem_definition_salience + causal_attribution_salience + moral_evaluation_salience + treatment_recommendation_salience + 1e-9)",
      "salience_weighted_framing_coherence_index": "pow((problem_definition_score * problem_definition_salience) * (causal_attribution_score * causal_attribution_salience) * (moral_evaluation_score * moral_evaluation_salience) * (treatment_recommendation_score * treatment_recommendation_salience), 1/4) / pow(problem_definition_salience * causal_attribution_salience * moral_evaluation_salience * treatment_recommendation_salience + 1e-9, 1/4)"
    }
  },
  "reliability_rubric": {
    "cronbachs_alpha": {
      "excellent": [0.80, 1.0],
      "good": [0.70, 0.79],
      "acceptable": [0.60, 0.69],
      "poor": [0.0, 0.59]
    },
    "notes": "Defines quality thresholds for framework reliability. The Synthesis Agent uses this for automated fit assessment."
  }
}
```

</details>

<GASKET_SCHEMA_START>
{
  "gasket_schema": {
    "version": "v7.3",
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
      "problem_definition_score": ["problem.{0,20}definition.{0,20}score", "problem.{0,20}definition.{0,20}rating", "problem\\s*definition\\s*:\\s*[0-9]"],
      "causal_attribution_score": ["causal.{0,20}attribution.{0,20}score", "causal.{0,20}attribution.{0,20}rating", "causal\\s*attribution\\s*:\\s*[0-9]"],
      "moral_evaluation_score": ["moral.{0,20}evaluation.{0,20}score", "moral.{0,20}evaluation.{0,20}rating", "moral\\s*evaluation\\s*:\\s*[0-9]"],
      "treatment_recommendation_score": ["treatment.{0,20}recommendation.{0,20}score", "treatment.{0,20}recommendation.{0,20}rating", "treatment\\s*recommendation\\s*:\\s*[0-9]"],
      "problem_definition_salience": ["problem.{0,20}definition.{0,20}salience", "problem.{0,20}definition.{0,20}importance", "problem.{0,20}definition.{0,20}centrality"],
      "causal_attribution_salience": ["causal.{0,20}attribution.{0,20}salience", "causal.{0,20}attribution.{0,20}importance", "causal.{0,20}attribution.{0,20}centrality"],
      "moral_evaluation_salience": ["moral.{0,20}evaluation.{0,20}salience", "moral.{0,20}evaluation.{0,20}importance", "moral.{0,20}evaluation.{0,20}centrality"],
      "treatment_recommendation_salience": ["treatment.{0,20}recommendation.{0,20}salience", "treatment.{0,20}recommendation.{0,20}importance", "treatment.{0,20}recommendation.{0,20}centrality"],
      "problem_definition_confidence": ["problem.{0,20}definition.{0,20}confidence", "problem.{0,20}definition.{0,20}certainty", "problem.{0,20}definition.{0,20}sure"],
      "causal_attribution_confidence": ["causal.{0,20}attribution.{0,20}confidence", "causal.{0,20}attribution.{0,20}certainty", "causal.{0,20}attribution.{0,20}sure"],
      "moral_evaluation_confidence": ["moral.{0,20}evaluation.{0,20}confidence", "moral.{0,20}evaluation.{0,20}certainty", "moral.{0,20}evaluation.{0,20}sure"],
      "treatment_recommendation_confidence": ["treatment.{0,20}recommendation.{0,20}confidence", "treatment.{0,20}recommendation.{0,20}certainty", "treatment.{0,20}recommendation.{0,20}sure"]
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
  }
}
<GASKET_SCHEMA_END>