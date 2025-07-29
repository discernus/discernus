# Populism vs Pluralism Framework v5.0

**Version**: 5.0  
**Status**: Active  
**Major Change**: Embedded CSV Architecture for Synthesis Scalability

A Discernus framework is a self-contained markdown file that embodies the core principles of computational social science research. It serves as both human-readable methodology and machine-executable instructions, ensuring perfect coherence between theory and practice.

**🚀 NEW IN V5.0: Embedded CSV Output Contract**

Version 5.0 introduces the **Embedded CSV Architecture** to solve synthesis scalability bottlenecks. Frameworks must now embed standardized CSV segments directly in their LLM responses using Discernus-specific delimiters, enabling processing of 3,000-8,000 documents per synthesis run (a 60-800x improvement over current academic practice).

---

## Executive Summary

The Populism vs Pluralism Framework v5.0 analyzes the fundamental tension between populist and pluralist approaches to democratic governance through **salience-enhanced authority analysis**. This framework examines both the presence and rhetorical prominence of populist "will of the people" narratives versus pluralist institutional mediation approaches, revealing which democratic authority sources speakers prioritize strategically.

---

## Framework Dimensions

### **Populist Authority (0.0-1.0)**
Direct popular will and majoritarian sovereignty emphasis
- **Direct Democracy**: "will of the people," "popular mandate," "majority rule," "people decide"
- **Anti-Elite Framing**: "corrupt elite," "establishment," "political class," "out of touch"
- **Pure People**: "real people," "ordinary citizens," "common folk," "working families"
- **Institutional Dismissal**: "bypass institutions," "direct action," "popular sovereignty"

### **Pluralist Authority (0.0-1.0)**  
Institutional mediation, minority rights, and procedural democracy emphasis
- **Institutional Safeguards**: "checks and balances," "constitutional protections," "rule of law," "institutional process"
- **Minority Rights**: "protect minorities," "diverse voices," "inclusive democracy," "minority protection"
- **Deliberative Process**: "democratic deliberation," "reasoned debate," "careful consideration," "institutional wisdom"
- **Procedural Democracy**: "due process," "proper procedures," "democratic norms," "institutional integrity"

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "populism_pluralism_v5_0",
  "version": "v5.0",
  "display_name": "Populism vs Pluralism v5.0",
  "analysis_variants": {
    "default": {
      "description": "Salience-enhanced populist vs pluralist democratic authority analysis with embedded CSV output.",
      "analysis_prompt": "Phase 1: Cognitive Priming: You are an expert in democratic theory and political communication. Phase 2: Framework Methodology: Your task is to analyze the text using the Populism vs Pluralism Framework v5.0. Phase 3: Operational Definitions: Evaluate two dimensions: Populist Authority (legitimacy from the direct will of the people) and Pluralist Authority (legitimacy from institutional mediation and minority rights). Phase 4: Scoring Protocol: For each dimension, score its intensity (0.0-1.0) and salience (0.0-1.0), and provide the strongest 1-2 quotes as evidence. Calculate the democratic authority balance (populist_authority - pluralist_authority). Phase 5: Framework-Specific CSV Structure: Your scores CSV must contain exactly 6 columns in this order: aid, populist_authority, pluralist_authority, populist_authority_salience, pluralist_authority_salience, democratic_authority_balance. Your evidence CSV must contain exactly 6 columns: aid, dimension, quote_id, quote_text, confidence_score, context_type. Phase 6: Output Specification: Return a complete response containing both a comprehensive JSON analysis AND the embedded CSV segments using the exact delimiters and column structures specified in the output_contract."
    }
  },
  "dimension_groups": {
      "authority_sources": ["populist_authority", "pluralist_authority"]
  },
  "calculation_spec": {
    "democratic_authority_balance": "populist_authority - pluralist_authority"
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
      "salience_ranking": "array"
    },
    "embedded_csv_requirements": {
      "scores_csv": {
        "delimiter_start": "<<<DISCERNUS_SCORES_CSV_v1>>>",
        "delimiter_end": "<<<END_DISCERNUS_SCORES_CSV_v1>>>",
        "description": "CSV for all dimensional scores, salience scores, and calculated balance.",
        "columns": [
          "aid",
          "populist_authority",
          "pluralist_authority",
          "populist_authority_salience",
          "pluralist_authority_salience", 
          "democratic_authority_balance"
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
    "instructions": "IMPORTANT: Your response MUST include both a complete JSON analysis AND embedded CSV segments using the exact delimiters specified. The salience_ranking should be an ordered array of objects, each containing 'dimension', 'salience_score', and 'rank'. The scores CSV must include exactly 6 columns: aid + 2 authority scores + 2 salience scores + 1 balance calculation. The evidence CSV must include exactly 6 columns: aid + dimension + quote_id + quote_text + confidence_score + context_type."
  }
}
```

</details> 