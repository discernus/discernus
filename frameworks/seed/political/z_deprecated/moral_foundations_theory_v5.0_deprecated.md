# Moral Foundations Theory Framework v5.0

**Version**: 5.0  
**Status**: Active  
**Major Change**: Embedded CSV Architecture for Synthesis Scalability

A Discernus framework is a self-contained markdown file that embodies the core principles of computational social science research. It serves as both human-readable methodology and machine-executable instructions, ensuring perfect coherence between theory and practice.

**🚀 NEW IN V5.0: Embedded CSV Output Contract**

Version 5.0 introduces the **Embedded CSV Architecture** to solve synthesis scalability bottlenecks. Frameworks must now embed standardized CSV segments directly in their LLM responses using Discernus-specific delimiters, enabling processing of 3,000-8,000 documents per synthesis run (a 60-800x improvement over current academic practice).

---

## Moral Foundations Theory Core Analysis

### **Six Foundation Pairs: Independent Scoring with Tension Analysis**

**Individualizing Foundations (Foundation Pairs 1-2)**:
1. **Care** (0.0-1.0): Compassion, protection, suffering prevention
2. **Harm** (0.0-1.0): Cruelty concern, violence prevention, victim advocacy

3. **Fairness** (0.0-1.0): Justice, equality, proportional treatment  
4. **Cheating** (0.0-1.0): Unfairness concern, exploitation prevention, corruption focus

**Binding Foundations (Foundation Pairs 3-5)**:
5. **Loyalty** (0.0-1.0): Group cohesion, fidelity, solidarity
6. **Betrayal** (0.0-1.0): Group abandonment concern, treachery prevention

7. **Authority** (0.0-1.0): Hierarchy respect, tradition, legitimate order
8. **Subversion** (0.0-1.0): Rebellion concern, tradition undermining, hierarchy disruption

9. **Sanctity** (0.0-1.0): Sacred preservation, purity, transcendence  
10. **Degradation** (0.0-1.0): Contamination concern, profane prevention, sacred violation

**Liberty Foundation (Foundation Pair 6)**:
11. **Liberty** (0.0-1.0): Freedom, autonomy, self-determination
12. **Oppression** (0.0-1.0): Control concern, domination prevention, freedom protection

---

## Revolutionary Moral Tension Mathematics

### **Moral Foundation Tension Scoring**

**Formula**: `Moral Tension = min(Foundation_score, Opposition_score) × |Foundation_salience - Opposition_salience|`

### **Moral Strategic Contradiction Index (MSCI)**

**Formula**: `MSCI = (Sum of all Moral Tension Scores) / Number of Foundation Pairs`

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "mft_v5_0",
  "version": "v5.0",
  "display_name": "Moral Foundations Theory Framework v5.0",
  "analysis_variants": {
    "default": {
      "description": "Complete salience-weighted moral foundation analysis with moral tension pattern quantification and embedded CSV output.",
      "analysis_prompt": "Phase 1: Cognitive Priming: You are an expert moral psychology analyst with deep knowledge of Moral Foundations Theory. Phase 2: Framework Methodology: Your task is to analyze the text using the Moral Foundations Theory Framework v5.0, which includes tension-enhanced salience-weighted analysis. Phase 3: Operational Definitions: The framework evaluates 6 foundation pairs (12 total foundations): Care/Harm, Fairness/Cheating, Loyalty/Betrayal, Authority/Subversion, Sanctity/Degradation, and Liberty/Oppression. Phase 4: Scoring Protocol: For each of the 12 foundations, score its intensity (0.0-1.0) and salience (0.0-1.0). Provide the strongest 1-2 quotes as evidence. Then, calculate the moral tension for each of the 6 pairs and the overall Moral Strategic Contradiction Index (MSCI). Phase 5: Framework-Specific CSV Structure: Your scores CSV must contain exactly 27 columns in this order: aid, care, harm, fairness, cheating, loyalty, betrayal, authority, subversion, sanctity, degradation, liberty, oppression, care_salience, harm_salience, fairness_salience, cheating_salience, loyalty_salience, betrayal_salience, authority_salience, subversion_salience, sanctity_salience, degradation_salience, liberty_salience, oppression_salience, care_harm_tension, fairness_cheating_tension, loyalty_betrayal_tension, authority_subversion_tension, sanctity_degradation_tension, liberty_oppression_tension, moral_strategic_contradiction_index. Your evidence CSV must contain exactly 6 columns: aid, foundation, quote_id, quote_text, confidence_score, context_type. Phase 6: Output Specification: Return a complete response containing both a comprehensive JSON analysis AND the embedded CSV segments using the exact delimiters and column structures specified in the output_contract."
    }
  },
  "dimension_groups": {
    "individualizing_foundations": ["care", "harm", "fairness", "cheating"],
    "binding_foundations": ["loyalty", "betrayal", "authority", "subversion", "sanctity", "degradation"],
    "liberty_foundation": ["liberty", "oppression"]
  },
  "calculation_spec": {
    "moral_tension_mathematics": "Moral tension quantification using formula: Moral Tension = min(Foundation_score, Opposition_score) × |Foundation_salience - Opposition_salience|.",
    "moral_foundation_tensions": {
      "care_harm_tension": "min(care, harm) × abs(care_salience - harm_salience)",
      "fairness_cheating_tension": "min(fairness, cheating) × abs(fairness_salience - cheating_salience)",
      "loyalty_betrayal_tension": "min(loyalty, betrayal) × abs(loyalty_salience - betrayal_salience)",
      "authority_subversion_tension": "min(authority, subversion) × abs(authority_salience - subversion_salience)",
      "sanctity_degradation_tension": "min(sanctity, degradation) × abs(sanctity_salience - degradation_salience)",
      "liberty_oppression_tension": "min(liberty, oppression) × abs(liberty_salience - oppression_salience)"
    },
    "moral_strategic_contradiction_index": "(care_harm_tension + fairness_cheating_tension + loyalty_betrayal_tension + authority_subversion_tension + sanctity_degradation_tension + liberty_oppression_tension) / 6"
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
      "salience_ranking": "array",
      "tension_analysis": "object"
    },
    "embedded_csv_requirements": {
      "scores_csv": {
        "delimiter_start": "<<<DISCERNUS_SCORES_CSV_v1>>>",
        "delimiter_end": "<<<END_DISCERNUS_SCORES_CSV_v1>>>",
        "description": "CSV for all dimensional scores, salience scores, tension scores, and calculated metrics.",
        "columns": [
          "aid",
          "care", "harm", "fairness", "cheating", "loyalty", "betrayal", 
          "authority", "subversion", "sanctity", "degradation", "liberty", "oppression",
          "care_salience", "harm_salience", "fairness_salience", "cheating_salience", 
          "loyalty_salience", "betrayal_salience", "authority_salience", "subversion_salience", 
          "sanctity_salience", "degradation_salience", "liberty_salience", "oppression_salience",
          "care_harm_tension", "fairness_cheating_tension", "loyalty_betrayal_tension",
          "authority_subversion_tension", "sanctity_degradation_tension", "liberty_oppression_tension",
          "moral_strategic_contradiction_index"
        ]
      },
      "evidence_csv": {
        "delimiter_start": "<<<DISCERNUS_EVIDENCE_CSV_v1>>>",
        "delimiter_end": "<<<END_DISCERNUS_EVIDENCE_CSV_v1>>>",
        "description": "CSV for structured evidence data for audit and replication.",
        "columns": [
          "aid",
          "foundation",
          "quote_id", 
          "quote_text",
          "confidence_score",
          "context_type"
        ]
      }
    },
    "instructions": "IMPORTANT: Your response MUST include both a complete JSON analysis AND embedded CSV segments using the exact delimiters specified. The salience_ranking should be an ordered array of objects, each containing 'foundation', 'salience_score', and 'rank'. The scores CSV must include exactly 27 columns: aid + 12 foundation scores + 12 salience scores + 6 tension scores + 1 MSCI score. The evidence CSV must include exactly 6 columns: aid + foundation + quote_id + quote_text + confidence_score + context_type."
  }
}
```

</details> 