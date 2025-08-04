# Populism vs Pluralism Framework v7.1

**Version**: 7.1  
**Status**: Active  
**Major Change**: Enhanced Gasket Schema with Metadata Scores and Advanced Extraction Patterns

A Discernus framework is a self-contained markdown file that embodies the core principles of computational social science research. It serves as both human-readable methodology and machine-executable instructions, ensuring perfect coherence between theory and practice.

The Populism vs Pluralism Framework v7.1 analyzes the fundamental tension between populist and pluralist approaches to democratic governance through enhanced metadata analysis. This framework employs salience-weighted analysis to reveal which democratic authority sources speakers prioritize strategically, with advanced extraction patterns and validation rules for robust analysis.

**Innovation**: Metadata scoring captures not just populist/pluralist presence but which authority sources receive the most rhetorical emphasis.

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
  "name": "populism_pluralism_v7_1",
  "version": "v7.1",
  "display_name": "Populism vs Pluralism Framework v7.1",
  "analysis_variants": {
    "default": {
      "description": "Salience-enhanced populist vs pluralist democratic authority analysis with raw analysis log output.",
      "analysis_prompt": "You are an expert in democratic theory and political communication with deep understanding of populist and pluralist dynamics across diverse contexts. Your task is to analyze the provided text using the Populism vs Pluralism Framework v7.1, which measures democratic authority tensions through two key dimensions with enhanced metadata reporting and salience-weighted analysis.\n\nThe framework evaluates democratic authority across two dimensions:\n\n**Populist Authority** (0.0-1.0): Direct popular will and majoritarian sovereignty emphasis, including markers like 'will of the people,' 'popular mandate,' 'majority rule,' 'corrupt elite,' 'establishment,' 'real people,' 'ordinary citizens,' 'bypass institutions.'\n\n**Pluralist Authority** (0.0-1.0): Institutional mediation, minority rights, and procedural democracy emphasis, including markers like 'checks and balances,' 'constitutional protections,' 'rule of law,' 'protect minorities,' 'diverse voices,' 'democratic deliberation,' 'due process.'\n\nFor each dimension, provide:\n- **Score (0.0-1.0)**: Based on strength of evidence in the text\n- **Salience (0.0-1.0)**: How central is this dimension to this specific text?\n- **Confidence (0.0-1.0)**: How certain are you in this assessment?\n\nWrite a comprehensive analytical report that covers:\n- Application of the Populism vs Pluralism methodology to this specific text\n- Detailed analysis of each dimension with scores, salience, confidence, and evidence\n- Assessment of democratic authority tensions and rhetorical emphasis patterns\n- Overall authority profile with salience weighting\n- Key insights about the speaker's approach to democratic legitimacy\n\nEmbed your numerical assessments naturally within the analysis. For example: 'This text demonstrates strong populist authority (populist authority score: 0.8, salience: 0.9, confidence: 0.7) with frequent appeals to direct popular will.' Focus on rigorous intellectual analysis supported by direct textual evidence and clear reasoning for all scores and metadata."
    }
  },
  "dimension_groups": {
      "authority_sources": ["populist_authority", "pluralist_authority"]
  },
  "calculation_spec": {
    "democratic_authority_balance": "populist_authority_score - pluralist_authority_score"
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
      "populist_authority_score",
      "pluralist_authority_score",
      "populist_authority_salience",
      "pluralist_authority_salience",
      "populist_authority_confidence",
      "pluralist_authority_confidence"
    ],
    "extraction_patterns": {
      "populist_authority_score": ["populist.{0,20}authority.{0,20}score", "populist.{0,20}authority.{0,20}rating", "populist\\s*authority\\s*:\\s*[0-9]"],
      "pluralist_authority_score": ["pluralist.{0,20}authority.{0,20}score", "pluralist.{0,20}authority.{0,20}rating", "pluralist\\s*authority\\s*:\\s*[0-9]"],
      "populist_authority_salience": ["populist.{0,20}authority.{0,20}salience", "populist.{0,20}authority.{0,20}importance", "populist.{0,20}centrality"],
      "pluralist_authority_salience": ["pluralist.{0,20}authority.{0,20}salience", "pluralist.{0,20}authority.{0,20}importance", "pluralist.{0,20}centrality"],
      "populist_authority_confidence": ["populist.{0,20}authority.{0,20}confidence", "populist.{0,20}authority.{0,20}certainty", "populist.{0,20}sure"],
      "pluralist_authority_confidence": ["pluralist.{0,20}authority.{0,20}confidence", "pluralist.{0,20}authority.{0,20}certainty", "pluralist.{0,20}sure"]
    },
    "validation_rules": {
      "required_fields": [
        "populist_authority_score", "pluralist_authority_score"
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
```

</details>