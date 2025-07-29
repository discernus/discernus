# Political Worldview Triad Framework v5.0

**Version**: 5.0  
**Status**: Active  
**Major Change**: Embedded CSV Architecture for Synthesis Scalability

A Discernus framework is a self-contained markdown file that embodies the core principles of computational social science research. It serves as both human-readable methodology and machine-executable instructions, ensuring perfect coherence between theory and practice.

**🚀 NEW IN V5.0: Embedded CSV Output Contract**

Version 5.0 introduces the **Embedded CSV Architecture** to solve synthesis scalability bottlenecks. Frameworks must now embed standardized CSV segments directly in their LLM responses using Discernus-specific delimiters, enabling processing of 3,000-8,000 documents per synthesis run (a 60-800x improvement over current academic practice).

---

## Executive Summary

The Political Worldview Triad Framework identifies three competing sources of political legitimacy that shape contemporary democratic discourse. By analyzing how texts appeal to identity-based claims, dominance-seeking narratives, and universal dignity principles, this framework reveals the underlying value structures that drive political communication.

---

## Framework Dimensions

### Immutable-Identity Politics

**Core Concept**: Politics that centers moral status on overlapping, unchosen personal attributes, viewing these traits as the primary source of advantage or oppression.

**Key Indicators**:
- "As Black women, we...", "Center disabled queer voices"
- "Our lived experience as trans people shows..."
- "Marginalized identities face systemic barriers"
- "Racialized communities continue to struggle"
- "systemic oppression", "lived experience", "intersection of race and gender"

### Tribal Domination

**Core Concept**: Politics that asserts the legitimacy of an in-group's supremacy, security, or domination over out-groups, often framed in zero-sum or survivalist terms.

**Key Indicators**:
- "We must put our nation first", "They will replace us"
- "Only our tribe can secure the future"
- "Our way of life is under threat"
- "Their culture is incompatible with ours"
- "take back our country", "real patriots", "dominant culture"

### Pluralist Individual Dignity

**Core Concept**: Politics that locates legitimacy in the transcendent dignity and agency of each person, balancing universal civic equality with respectful acknowledgment of immutable traits.

**Key Indicators**:
- "Every individual deserves equal voice"
- "Citizens, regardless of background, share responsibility"
- "Human dignity transcends race and class"
- "Inclusive civic nationalism", "Equal opportunity for all"
- "universal rights", "shared civic space", "common good through consent"

---
<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "political_worldview_triad_v5_0",
  "version": "v5.0",
  "display_name": "Political Worldview Triad Framework v5.0",
  "analysis_variants": {
    "default": {
      "description": "Complete triadic worldview analysis across all three political legitimacy sources with embedded CSV output.",
      "analysis_prompt": "Phase 1: Cognitive Priming: You are an expert political discourse analyst. Phase 2: Framework Methodology: Your task is to analyze the text using the Political Worldview Triad Framework v5.0. Phase 3: Operational Definitions: Evaluate three worldview dimensions: Immutable-Identity Politics (legitimacy from unchosen attributes), Tribal Domination (legitimacy from in-group supremacy), and Pluralist Individual Dignity (legitimacy from universal human worth). Phase 4: Scoring Protocol: For each worldview, score its intensity from 0.0 to 1.0 and provide the strongest 1-2 quotes as evidence. Identify the dominant worldview (highest scoring). Phase 5: Framework-Specific CSV Structure: Your scores CSV must contain exactly 5 columns in this order: aid, immutable_identity_politics, tribal_domination, pluralist_individual_dignity, dominant_worldview. Your evidence CSV must contain exactly 6 columns: aid, worldview, quote_id, quote_text, confidence_score, context_type. Phase 6: Output Specification: Return a complete response containing both a comprehensive JSON analysis AND the embedded CSV segments using the exact delimiters and column structures specified in the output_contract."
    }
  },
  "dimension_groups": {
      "worldviews": ["immutable_identity_politics", "tribal_domination", "pluralist_individual_dignity"]
  },
  "calculation_spec": {
      "dominant_worldview_calculation": "Identify the worldview with the highest score."
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
        "description": "CSV for all worldview scores and dominant worldview calculation.",
        "columns": [
          "aid",
          "immutable_identity_politics",
          "tribal_domination", 
          "pluralist_individual_dignity",
          "dominant_worldview"
        ]
      },
      "evidence_csv": {
        "delimiter_start": "<<<DISCERNUS_EVIDENCE_CSV_v1>>>",
        "delimiter_end": "<<<END_DISCERNUS_EVIDENCE_CSV_v1>>>",
        "description": "CSV for structured evidence data for audit and replication.",
        "columns": [
          "aid",
          "worldview",
          "quote_id",
          "quote_text",
          "confidence_score",
          "context_type"
        ]
      }
    },
    "instructions": "IMPORTANT: Your response MUST include both a complete JSON analysis AND embedded CSV segments using the exact delimiters specified. The scores CSV must include exactly 5 columns: aid + 3 worldview scores + dominant_worldview. The evidence CSV must include exactly 6 columns: aid + worldview + quote_id + quote_text + confidence_score + context_type."
  }
}
```

</details> 