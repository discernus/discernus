# Entman Framing Functions Framework v5.0
**Version**: 5.0
**Status**: Active
**Major Change**: Embedded CSV Architecture for Synthesis Scalability

---

## Executive Summary

The Entman Framing Functions Framework implements Robert Entman's systematic communication analysis through four independent framing functions. This framework tests whether Problem Definition, Causal Attribution, Moral Evaluation, and Treatment Recommendation operate independently as predicted by communication theory, representing systematic message construction in political discourse.

Based on Entman's foundational framing theory and communication research, this framework analyzes how strategic communications utilize distinct framing functions to construct persuasive messages through systematic problem identification, causal analysis, moral judgment, and solution advocacy.

---

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

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "entman_v5_0",
  "version": "v5.0",
  "display_name": "Entman Framing Functions Framework v5.0",
  "analysis_variants": {
    "default": {
      "description": "Complete four-function framing analysis with embedded CSV output.",
      "analysis_prompt": "Phase 1: Cognitive Priming: You are an expert analyst of communication and framing. Phase 2: Framework Methodology: Your task is to analyze the text using the Entman Framing Functions Framework v5.0. Phase 3: Operational Definitions: Evaluate four independent framing functions: Problem Definition, Causal Attribution, Moral Evaluation, and Treatment Recommendation. Phase 4: Scoring Protocol: Score each function from 0.0 to 1.0 and provide the strongest 1-2 quotes as evidence. Calculate the message completeness score as the average of all four functions. Phase 5: Framework-Specific CSV Structure: Your scores CSV must contain exactly 6 columns in this order: aid, problem_definition, causal_attribution, moral_evaluation, treatment_recommendation, message_completeness_score. Your evidence CSV must contain exactly 6 columns: aid, function, quote_id, quote_text, confidence_score, context_type. Phase 6: Output Specification: Return a complete response containing both a comprehensive JSON analysis AND the embedded CSV segments using the exact delimiters and column structures specified in the output_contract."
    }
  },
  "dimension_groups": {
    "framing_functions": ["problem_definition", "causal_attribution", "moral_evaluation", "treatment_recommendation"]
  },
  "calculation_spec": {
    "message_completeness_score": "(problem_definition + causal_attribution + moral_evaluation + treatment_recommendation) / 4"
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
      "reasoning": "object"
    },
    "embedded_csv_requirements": {
      "scores_csv": {
        "delimiter_start": "<<<DISCERNUS_SCORES_CSV_v1>>>",
        "delimiter_end": "<<<END_DISCERNUS_SCORES_CSV_v1>>>",
        "description": "CSV for all dimensional scores and calculated metrics.",
        "columns": [
          "aid",
          "problem_definition",
          "causal_attribution", 
          "moral_evaluation",
          "treatment_recommendation",
          "message_completeness_score"
        ]
      },
      "evidence_csv": {
        "delimiter_start": "<<<DISCERNUS_EVIDENCE_CSV_v1>>>",
        "delimiter_end": "<<<END_DISCERNUS_EVIDENCE_CSV_v1>>>",
        "description": "CSV for structured evidence data for audit and replication.",
        "columns": [
          "aid",
          "function",
          "quote_id",
          "quote_text", 
          "confidence_score",
          "context_type"
        ]
      }
    },
    "instructions": "IMPORTANT: Your response MUST include both a complete JSON analysis AND embedded CSV segments using the exact delimiters specified. The scores CSV must include exactly 6 columns: aid + 4 function scores + 1 message completeness score. The evidence CSV must include exactly 6 columns: aid + function + quote_id + quote_text + confidence_score + context_type."
  }
}
```

</details> 