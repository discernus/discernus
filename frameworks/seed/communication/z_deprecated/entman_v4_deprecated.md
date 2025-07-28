# Entman Framing Functions Framework v4.0
**Version**: v4.0
**Status**: Active

---

## Executive Summary

The Entman Framing Functions Framework implements Robert Entman's systematic communication analysis through four independent framing functions. This framework tests whether Problem Definition, Causal Attribution, Moral Evaluation, and Treatment Recommendation operate independently as predicted by communication theory, representing systematic message construction in political discourse.

Based on Entman's foundational framing theory and communication research, this framework analyzes how strategic communications utilize distinct framing functions to construct persuasive messages through systematic problem identification, causal analysis, moral judgment, and solution advocacy.

---

## Theoretical Foundation

This framework is grounded in Robert Entman's framing theory and systematic communication analysis. The framework tests Entman's hypothesis that framing operates through four distinct, independent functions that can vary separately to achieve strategic communication goals.

### Four Framing Functions

**1. Problem Definition**: What issues are identified as requiring attention and how problems are conceptualized

**2. Causal Attribution**: What factors or actors are presented as causing problems and how responsibility is assigned

**3. Moral Evaluation**: What values and moral judgments are invoked and how actions are evaluated ethically

**4. Treatment Recommendation**: What solutions are proposed and how policy options are presented and prioritized

### Independence Hypothesis

Entman's theory predicts that these framing functions operate as independent analytical dimensions that can vary separately without necessary correlation. A communication may emphasize problem definition without moral evaluation, or propose solutions without extensive causal attribution.

### Key References

- Entman, R. M. (1993). Framing: Toward clarification of a fractured paradigm. Journal of Communication, 43(4), 51-58.
- Entman, R. M. (2007). Framing bias: Media in the distribution of power. Journal of Communication, 57(1), 163-173.
- Chong, D., & Druckman, J. N. (2007). Framing theory. Annual Review of Political Science, 10, 103-126.
- Chong, D., & Druckman, J. N. (2007). Framing public opinion in competitive democracies. American Political Science Review, 101(4), 637-655.

## Framework Dimensions

### Problem Definition

What issues are identified as requiring attention and how problems are conceptualized. This function establishes the scope and nature of issues requiring public attention.

**Key Indicators:**
- the real issue is, we face a crisis of, the challenge before us, the problem we must address
- the urgent need to, what's really at stake, the fundamental issue, the core problem
- this affects everyone, widespread implications, immediate action required, crisis demands response

### Causal Attribution

What factors or actors are presented as causing problems and how responsibility is assigned. This function establishes accountability and explanatory frameworks for identified problems.

**Key Indicators:**
- X is responsible for, this stems from Y's actions, the fault lies with, caused by
- due to, blame, accountable for, at fault, this results from broader patterns
- structural problems require, the system creates, institutional factors, the roots of this problem

### Moral Evaluation

What values and moral judgments are invoked and how actions are evaluated ethically. This function provides the ethical framework for understanding problems and solutions.

**Key Indicators:**
- justice demands, fairness requires, liberty is at stake, fundamental rights
- core values, moral imperative, ethical obligation, principle at stake
- this is fundamentally wrong, ethically unacceptable, morally justified, right thing to do

### Treatment Recommendation

What solutions are proposed and how policy options are presented and prioritized. This function advocates for specific responses and courses of action.

**Key Indicators:**
- we must immediately, the answer is, the only way forward, solution requires
- we should, necessary action, recommended approach, best path forward
- specific steps include, concrete measures, detailed implementation, policy proposal

## Analytical Methodology

This framework employs systematic communication analysis with function independence testing:

1. **Function Identification**: Identify presence and strength of each framing function independently
2. **Independence Testing**: Assess whether functions vary separately as predicted by theory
3. **Completeness Assessment**: Measure what percentage of Entman's four functions are present
4. **Sophistication Analysis**: Evaluate systematic vs ad hoc use of framing functions
5. **Evidence Collection**: Provide quotations supporting each function assessment

## Academic Validation

Framework validated through communication theory research and framing analysis literature. Enhanced communication theory implementation with systematic message construction analysis across four distinct framing functions. Tests Entman's independence hypothesis through empirical function correlation analysis and provides comprehensive framework for strategic communication assessment.

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "entman",
  "version": "v4.0",
  "display_name": "Entman Framing Functions Framework v4.0",
  "analysis_variants": {
    "default": {
      "description": "Complete implementation of the Entman Framing Functions Framework methodology",
      "analysis_prompt": "You are an expert analyst with deep knowledge of moral psychology, political discourse, and value analysis. Your task is to analyze the provided text using Entman Framing Functions Framework. The Entman Framing Functions Framework implements Robert Entman's systematic communication analysis through four independent framing functions. This framework examines the following dimensions: - **Problem Definition**: What issues are identified as requiring attention and how problems are conceptualized (look for: the real issue is, we face a crisis of, the challenge before us, the problem we must address, the urgent need to) - **Causal Attribution**: What factors or actors are presented as causing problems and how responsibility is assigned (look for: X is responsible for, this stems from Y's actions, the fault lies with, caused by, due to) - **Moral Evaluation**: What values and moral judgments are invoked and how actions are evaluated ethically (look for: justice demands, fairness requires, liberty is at stake, fundamental rights, core values) - **Treatment Recommendation**: What solutions are proposed and how policy options are presented and prioritized (look for: we must immediately, the answer is, the only way forward, solution requires, we should) For each dimension, follow this process: 1. Read the text systematically for relevant patterns and language 2. Identify specific evidence and quotations 3. Score the dimension from 0.0 to 1.0 based on strength and frequency of evidence 4. Provide approximately 2 direct quotations supporting each score 5. Assess your confidence in the scoring based on evidence clarity"
    }
  },
  "output_contract": {
    "schema": {
      "worldview": "string",
      "problem_definition_score": "number",
      "problem_definition_confidence": "number",
      "problem_definition_evidence": "array",
      "causal_attribution_score": "number",
      "causal_attribution_confidence": "number",
      "causal_attribution_evidence": "array",
      "moral_evaluation_score": "number",
      "moral_evaluation_confidence": "number",
      "moral_evaluation_evidence": "array",
      "treatment_recommendation_score": "number",
      "treatment_recommendation_confidence": "number",
      "treatment_recommendation_evidence": "array",
      "overall_analysis_confidence": "number",
      "key_patterns_observed": "string"
    },
    "instructions": "IMPORTANT: Your response MUST be a single, valid JSON object and nothing else. Do not include any text, explanations, or markdown code fences before or after the JSON object."
  },
  "calculation_spec": {
    "function_independence_score": "Statistical correlation matrix analysis - lower correlations indicate greater independence",
    "message_completeness_score": "Count of functions above presence threshold divided by four",
    "framing_sophistication_index": "Systematic coverage, function integration, and strategic emphasis measurement"
  }
}
```

</details>