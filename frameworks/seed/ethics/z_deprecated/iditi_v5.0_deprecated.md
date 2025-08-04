# Individual Dignity Identity v Tribal Identity v5.0
**Version**: 5.0
**Status**: Active
**Major Change**: Embedded CSV Architecture for Synthesis Scalability

---

## Executive Summary

The IDITI framework analyzes the fundamental tension between individual dignity and tribal identity in political discourse. This specialized framework focuses on how texts either affirm universal human worth or prioritize group-based identity and loyalty, examining the core moral question of whether human dignity is universal or conditional on group membership.

Based on Fukuyama's identity formation theory and Jung's collective psychology concepts, this framework evaluates the critical distinction between treating people as individuals with inherent worth versus defining people primarily through group membership and loyalty.

---

## Framework Dimensions

### Dignity

Affirms individual moral worth and universal rights, regardless of group identity. Emphasizes agency, pluralism, and character over affiliation. This represents the philosophical position that human dignity is inherent and universal.

**Key Indicators:**
- equal dignity, inherent worth, regardless of background, individual character
- universal rights, human agency, personal dignity, individual merit
- common humanity, respect for all, universal values, human dignity
- cross-group solidarity, individual autonomy, character-based judgment

### Tribalism

Prioritizes group dominance, loyalty, or identity over individual agency. Often frames moral worth in in-group/out-group terms. This represents the psychological tendency to condition respect and dignity on group membership.

**Key Indicators:**
- real Americans, our people, they don't belong, us vs them
- group loyalty, identity politics, blood and soil, true believers
- outsiders, not one of us, tribal unity, group supremacy
- in-group favoritism, group-based hierarchy, exclusion markers

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "iditi_v5_0",
  "version": "v5.0",
  "display_name": "Individual Dignity Identity v Tribal Identity v5.0",
  "analysis_variants": {
    "default": {
      "description": "Complete analysis of the dignity vs. tribalism axis with embedded CSV output.",
      "analysis_prompt": "Phase 1: Cognitive Priming: You are an expert analyst of political and ethical discourse. Phase 2: Framework Methodology: Your task is to analyze the text using the IDITI v5.0 framework. Phase 3: Operational Definitions: Evaluate two dimensions: Dignity (affirming universal human worth) and Tribalism (prioritizing group identity). Phase 4: Scoring Protocol: Score each dimension from 0.0 to 1.0 and provide the strongest 1-2 quotes as evidence. Calculate the identity axis score (dignity - tribalism). Phase 5: Framework-Specific CSV Structure: Your scores CSV must contain exactly 4 columns in this order: aid, dignity, tribalism, identity_axis_score. Your evidence CSV must contain exactly 6 columns: aid, dimension, quote_id, quote_text, confidence_score, context_type. Phase 6: Output Specification: Return a complete response containing both a comprehensive JSON analysis AND the embedded CSV segments using the exact delimiters and column structures specified in the output_contract."
    }
  },
  "dimension_groups": {
      "identity_axis": ["dignity", "tribalism"]
  },
  "calculation_spec": {
    "identity_axis_score": "dignity - tribalism"
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
        "description": "CSV for all dimensional scores and identity axis calculation.",
        "columns": [
          "aid",
          "dignity",
          "tribalism",
          "identity_axis_score"
        ]
      },
      "evidence_csv": {
        "delimiter_start": "<<<DISCERNUS_EVIDENCE_CSV_v1>>>",
        "delimiter_end": "<<<END_DISCERNUS_EVIDENCE_CSV_v1>>>",
        "description": "CSV for structured evidence data for audit and replication.",
        "columns": [
          "aid",
          "dimension",
          "quote_id",
          "quote_text",
          "confidence_score",
          "context_type"
        ]
      }
    },
    "instructions": "IMPORTANT: Your response MUST include both a complete JSON analysis AND embedded CSV segments using the exact delimiters specified. The scores CSV must include exactly 4 columns: aid + dignity + tribalism + identity_axis_score. The evidence CSV must include exactly 6 columns: aid + dimension + quote_id + quote_text + confidence_score + context_type."
  }
}
```

</details> 