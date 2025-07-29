# Political Discourse Two-Axis Analysis v5.0

**Version**: 5.0
**Status**: Active
**Major Change**: Embedded CSV Architecture for Synthesis Scalability

---

## Executive Summary

Revolutionary two-axis framework for political discourse analysis that resolves the fundamental conceptual overlap problems in traditional competitive models. Uses orthogonal axes to capture the core tensions in democratic political discourse without crowding-out effects.

This framework implements two independent dimensions: Populism ↔ Pluralism (vertical axis examining people vs institutions) and Patriotism ↔ Nationalism (horizontal axis examining civic vs ethnic identity). The orthogonal architecture eliminates the "Bolsonaro Problem" where traditional frameworks failed to accurately capture high populism and high nationalism simultaneously.

---

## Framework Dimensions

### Populism (Vertical Axis - High)

Direct popular sovereignty, anti-elite sentiment, Manichaean worldview. This represents appeals to "the people" against corrupt institutions and elite interests.

**Key Indicators:**
- the people, corrupt elite, establishment, will of the people
- us versus them, drain the swamp, real Americans/citizens, ordinary people

### Pluralism (Vertical Axis - Low)

Institutional mediation, diverse representation, expert knowledge. This represents respect for democratic institutions, procedural norms, and diverse stakeholder input.

**Key Indicators:**
- institutions, experts, diverse perspectives, democratic process
- checks and balances, constitutional principles, stakeholder input, evidence-based

### Nationalism (Horizontal Axis - High)

Ethnic/cultural identity emphasis, national supremacy claims. This represents appeals to cultural heritage, traditional values, and ethnic/cultural superiority.

**Key Indicators:**
- our people, national greatness, cultural heritage, traditional values
- foreign influence, national identity, cultural purity, ancestral homeland

### Patriotism (Horizontal Axis - Low)

Civic attachment to political institutions and constitutional values. This represents pride in democratic institutions, constitutional principles, and civic participation.

**Key Indicators:**
- constitution, democratic values, rule of law, civic duty
- constitutional rights, democratic institutions, equal justice, civic participation

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "political_discourse_two_axis_v5_0",
  "version": "v5.0",
  "display_name": "Political Discourse Two-Axis Analysis v5.0",
  "analysis_variants": {
    "default": {
      "description": "Complete two-axis analysis with embedded CSV output.",
      "analysis_prompt": "Phase 1: Cognitive Priming: You are an expert analyst of political discourse. Phase 2: Framework Methodology: Your task is to analyze the text using the Political Discourse Two-Axis Analysis v5.0. Phase 3: Operational Definitions: Evaluate two orthogonal axes: Populism vs. Pluralism (vertical) and Nationalism vs. Patriotism (horizontal). Phase 4: Scoring Protocol: Score each axis from 0.0 to 1.0. For the vertical axis, 1.0 is pure populism and 0.0 is pure pluralism. For the horizontal axis, 1.0 is pure nationalism and 0.0 is pure patriotism. Provide the strongest 1-2 quotes as evidence for each axis. Determine the quadrant classification based on the axis intersection. Phase 5: Framework-Specific CSV Structure: Your scores CSV must contain exactly 4 columns in this order: aid, vertical_axis_score, horizontal_axis_score, quadrant_classification. Your evidence CSV must contain exactly 6 columns: aid, axis, quote_id, quote_text, confidence_score, context_type. Phase 6: Output Specification: Return a complete response containing both a comprehensive JSON analysis AND the embedded CSV segments using the exact delimiters and column structures specified in the output_contract."
    }
  },
  "dimension_groups": {
      "axes": ["vertical_axis", "horizontal_axis"]
  },
  "calculation_spec": {
    "vertical_axis_score": "Single-pass analysis of vertical dimension indicators (0.0 = Pure Pluralism, 1.0 = Pure Populism)",
    "horizontal_axis_score": "Single-pass analysis of horizontal dimension indicators (0.0 = Pure Patriotism, 1.0 = Pure Nationalism)",
    "quadrant_classification": "Four-quadrant classification based on axis intersection"
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
        "description": "CSV for axis scores and quadrant classification.",
        "columns": [
          "aid",
          "vertical_axis_score",
          "horizontal_axis_score", 
          "quadrant_classification"
        ]
      },
      "evidence_csv": {
        "delimiter_start": "<<<DISCERNUS_EVIDENCE_CSV_v1>>>",
        "delimiter_end": "<<<END_DISCERNUS_EVIDENCE_CSV_v1>>>",
        "description": "CSV for structured evidence data for audit and replication.",
        "columns": [
          "aid",
          "axis",
          "quote_id",
          "quote_text",
          "confidence_score",
          "context_type"
        ]
      }
    },
    "instructions": "IMPORTANT: Your response MUST include both a complete JSON analysis AND embedded CSV segments using the exact delimiters specified. The scores CSV must include exactly 4 columns: aid + vertical_axis_score + horizontal_axis_score + quadrant_classification. The evidence CSV must include exactly 6 columns: aid + axis + quote_id + quote_text + confidence_score + context_type."
  }
}
```

</details> 