# Populism vs Pluralism Framework v6.0

**Version**: 6.0  
**Status**: Active  
**Major Change**: JSON-First Architecture with Enhanced Synthesis Integration

A Discernus framework is a self-contained markdown file that embodies the core principles of computational social science research. It serves as both human-readable methodology and machine-executable instructions, ensuring perfect coherence between theory and practice.

**🚀 NEW IN V6.0: Enhanced JSON Output Contract**

Version 6.0 returns to the JSON-first architecture while retaining all analytical capabilities from v5.0, eliminating CSV parsing brittleness while preserving synthesis scalability.

---

## Executive Summary

The Populism vs Pluralism Framework v6.0 analyzes the fundamental tension between populist and pluralist approaches to democratic governance through **salience-enhanced authority analysis**. This framework examines both the presence and rhetorical prominence of populist "will of the people" narratives versus pluralist institutional mediation approaches, revealing which democratic authority sources speakers prioritize strategically.

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
  "name": "populism_pluralism_v6_0",
  "version": "v6.0",
  "display_name": "Populism vs Pluralism v6.0",
  "analysis_variants": {
    "default": {
      "description": "Salience-enhanced populist vs pluralist democratic authority analysis with JSON output - mathematical calculations handled by code execution.",
      "analysis_prompt": "Phase 1: Cognitive Priming: You are an expert in democratic theory and political communication. Phase 2: Framework Methodology: Your task is to analyze the text using the Populism vs Pluralism Framework v6.0. Phase 3: Operational Definitions: Evaluate two dimensions: Populist Authority (legitimacy from the direct will of the people) and Pluralist Authority (legitimacy from institutional mediation and minority rights). Phase 4: Scoring Protocol: For each dimension, provide ONLY: (1) Raw score (0.0-1.0) based on intensity, (2) Salience score (0.0-1.0) based on prominence, (3) Confidence score (0.0-1.0) based on evidence strength, (4) Supporting quotes with contextual analysis. DO NOT perform any mathematical calculations such as democratic authority balance - this will be handled by code execution. Phase 5: JSON Structure Requirements: Your response must be a structured JSON object with nested data for raw scores only (NO calculated metrics), evidence organized by dimension, and reasoning for each assessment. Phase 6: Output Specification: Return a single, valid JSON object with raw dimensional scores only - NO calculations or derived metrics. All mathematical processing will be handled by code execution."
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
    "structured_data_requirements": {
      "scores": {
        "description": "Nested object containing ONLY raw dimensional scores (NO calculated metrics)",
        "structure": {
          "dimensions": {
            "populist_authority": {
              "score": "number (0.0-1.0)",
              "salience": "number (0.0-1.0)",
              "confidence": "number (0.0-1.0)"
            },
            "pluralist_authority": {
              "score": "number (0.0-1.0)",
              "salience": "number (0.0-1.0)",
              "confidence": "number (0.0-1.0)"
            }
          },
          "metadata": {
            "total_dimensions": "number",
            "analysis_completeness": "number (0.0-1.0)"
          }
        }
      },
      "evidence": {
        "description": "Nested object containing structured evidence data for audit and replication",
        "structure": {
          "by_dimension": {
            "populist_authority": [
              {
                "quote_id": "string",
                "quote_text": "string", 
                "confidence": "number (0.0-1.0)",
                "context_type": "string",
                "salience_justification": "string"
              }
            ],
            "pluralist_authority": "array_of_evidence_objects"
          },
          "metadata": {
            "total_quotes": "number",
            "average_confidence": "number"
          }
        }
      }
    },
    "instructions": "IMPORTANT: Your response MUST be a single, valid JSON object containing all required fields with the nested structures specified above. The salience_ranking should be an ordered array of objects, each containing 'dimension', 'salience_score', and 'rank'. All numerical scores must be between 0.0 and 1.0. DO NOT perform any mathematical calculations such as democratic_authority_balance - provide ONLY raw dimensional scores, salience, confidence, and evidence."
  }
}
```

</details>