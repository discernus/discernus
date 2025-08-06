# Populism vs Pluralism Framework v7.3

**Version**: 7.1  
**Status**: Active  
**Major Change**: Enhanced Gasket Schema with Metadata Scores and Advanced Extraction Patterns

A Discernus framework is a self-contained markdown file that embodies the core principles of computational social science research. It serves as both human-readable methodology and machine-executable instructions, ensuring perfect coherence between theory and practice.

The Populism vs Pluralism Framework v7.3 analyzes the fundamental tension between populist and pluralist approaches to democratic governance through enhanced metadata analysis. This framework employs salience-weighted analysis to reveal which democratic authority sources speakers prioritize strategically, with advanced extraction patterns and validation rules for robust analysis.

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
  "version": "v7.3",
  "display_name": "Populism vs Pluralism Framework v7.3",
  "analysis_variants": {
    "default": {
      "description": "Sequential populist vs pluralist democratic authority analysis with chain-of-thought methodology",
      "analysis_prompt": "You are an expert in democratic theory and political communication with deep understanding of populist and pluralist dynamics across diverse contexts. Analyze this text through focused sequential steps, examining each democratic authority source independently before integration.\n\nSTEP 1 - POPULIST AUTHORITY ANALYSIS\nFocus ONLY on populist authority patterns (ignore pluralist authority for now):\n- Look for populist authority patterns: direct popular will ('will of the people,' 'popular mandate,' 'majority rule'), anti-elite sentiment ('corrupt elite,' 'establishment,' 'out of touch'), people emphasis ('real people,' 'ordinary citizens,' 'common folk'), institutional bypass ('bypass institutions,' 'go directly to people,' 'around the system') - Note: These are semantic concepts, look for direct popular will and majoritarian sovereignty emphasis, not just these exact phrases\n- Assess populist legitimacy claims and majoritarian appeals\n- Score populist authority dimension (0.0-1.0) with specific textual evidence\n- Assess salience (0.0-1.0): How central are populist authority appeals to the overall message?\n- State confidence (0.0-1.0): How certain are you in this assessment?\nShow your analytical work and evidence before proceeding.\n\nSTEP 2 - PLURALIST AUTHORITY ANALYSIS\nNow focus ONLY on pluralist authority patterns:\n- Look for pluralist authority patterns: institutional mediation ('checks and balances,' 'constitutional protections,' 'institutional process'), minority rights ('rule of law,' 'protect minorities,' 'minority rights'), procedural democracy ('diverse voices,' 'democratic deliberation,' 'due process'), constitutional framework ('constitutional protections,' 'separation of powers,' 'judicial review') - Note: These are semantic concepts, look for institutional mediation, minority rights, and procedural democracy emphasis, not just these exact terms\n- Assess pluralist legitimacy claims and institutional respect\n- Score pluralist authority dimension (0.0-1.0) with specific textual evidence\n- Assess salience (0.0-1.0): How central are pluralist authority appeals to the message?\n- State confidence (0.0-1.0): How certain are you in this assessment?\nShow your analytical work and evidence before proceeding.\n\nFINAL STEP - INTEGRATION AND VALIDATION\nReview your step-by-step analysis:\n- Check for scoring consistency between populist and pluralist dimensions\n- Validate that evidence quality meets academic standards\n- Assess democratic authority tensions and rhetorical emphasis patterns\n- Confirm confidence levels are appropriately calibrated\n- Calculate democratic authority balance and overall profile\n- Apply pattern classifications based on authority source combinations\n\nProvide your final structured analysis following this format:\n\n**DEMOCRATIC AUTHORITY ASSESSMENT**\n\n**Populist Authority**: [score] (salience: [score], confidence: [score])\n**Pluralist Authority**: [score] (salience: [score], confidence: [score])\n\n**Calculated Metrics**:\n- Democratic Authority Balance: [calculated score]\n- Authority Profile: [populist/pluralist orientation]\n\n**Key Insights**: [Summary of democratic authority approach, legitimacy claims, and rhetorical emphasis patterns]"
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