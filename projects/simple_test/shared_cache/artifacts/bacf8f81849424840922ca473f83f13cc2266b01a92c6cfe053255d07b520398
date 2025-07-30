# Populist Rhetoric Module (PRM) v5.0

**Version**: 5.0  
**Status**: Active  
**Major Change**: Embedded CSV Architecture for Synthesis Scalability

A Discernus framework is a self-contained markdown file that embodies the core principles of computational social science research. It serves as both human-readable methodology and machine-executable instructions, ensuring perfect coherence between theory and practice.

**🚀 NEW IN V5.0: Embedded CSV Output Contract**

Version 5.0 introduces the **Embedded CSV Architecture** to solve synthesis scalability bottlenecks. Frameworks must now embed standardized CSV segments directly in their LLM responses using Discernus-specific delimiters, enabling processing of 3,000-8,000 documents per synthesis run (a 60-800x improvement over current academic practice).

---

## What Is This Enhanced Temporal Module?

The Populist Rhetoric Module (PRM) v5.0 represents the **first salience-enhanced temporal module** in the Discernus framework architecture. While Core Modules provide timeless analytical foundations, this temporal module captures era-specific populist phenomena (2010s-2020s) with **salience-weighted strategic communication analysis** that reveals which populist appeals speakers emphasize most rhetorically.

**Core Purpose**: PRM v5.0 analyzes contemporary populist political communication patterns through **salience-enhanced strategic emphasis assessment**, complementing Core Module analysis with temporal specificity about current populist mobilization priorities and strategic communication patterns.

**Version 5.0 Enhancement**: **Embedded CSV Architecture** - enables massive-scale synthesis of populist rhetoric analysis.

**Key Applications**:
- **Populist Strategy Analysis**: Understanding which populist appeals speakers prioritize rhetorically
- **Contemporary Political Intelligence**: Salience-weighted analysis of current populist movements and strategic communication
- **Comparative Populism Studies**: Empirical comparison of populist emphasis patterns across contexts
- **Democratic Response Strategy**: Informed responses based on actual populist communication priorities

---

## Framework Architecture: Enhanced 6-Dimension Contemporary Populist Assessment

### **Core Populist Appeals**

#### **People vs Elite Framing (0.0-1.0)**
Politics as conflict between ordinary people and privileged elite
- **Elite Identification**: "establishment," "ruling class," "privileged few," "Washington insiders," "deep state"
- **People Identification**: "real Americans," "working families," "ordinary people," "forgotten Americans," "regular folks"
- **Conflict Framing**: "us versus them," "drain the swamp," "fight establishment," "power to people"

#### **Authentic Representation Claims (0.0-1.0)**
Assertions about representing genuine popular will
- **Authenticity Language**: "real representation," "genuine voice," "authentic leadership," "straight talk," "honest representation"
- **Opposition Illegitimacy**: "fake representation," "puppet politicians," "career politicians," "special interest representatives"

#### **Anti-System Mobilization (0.0-1.0)**
Mobilization against existing political systems
- **System Criticism**: "rigged system," "broken system," "corrupt system," "failed institutions," "establishment failure"
- **Outsider Appeals**: "political outsider," "not a politician," "outside the system," "fresh perspective"

### **Populist Mobilization Strategies**

#### **Direct Democracy Appeals (0.0-1.0)**
Direct popular sovereignty emphasis
- **Popular Sovereignty**: "people decide," "popular vote," "democratic mandate," "will of people," "majority rule"
- **Institutional Bypass**: "bypass Congress," "go directly to people," "referendum," "popular initiative"

#### **Common Sense vs Expertise (0.0-1.0)**
Popular wisdom over professional expertise
- **Common Sense Appeals**: "common sense," "practical wisdom," "real-world experience," "street smarts," "practical solutions"
- **Expert Criticism**: "out-of-touch experts," "ivory tower," "expert failure," "elite expertise," "academic theories"

#### **Cultural Authenticity Claims (0.0-1.0)**
Authentic cultural values versus cosmopolitan alternatives
- **Cultural Values**: "traditional values," "cultural heritage," "real culture," "authentic American values," "cultural roots"
- **Cultural Threat**: "cultural displacement," "foreign influence," "cultural elite," "cosmopolitan values"

---
<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "prm_v5_0",
  "version": "v5.0",
  "display_name": "Populist Rhetoric Module (PRM) v5.0",
  "analysis_variants": {
    "default": {
      "description": "Complete salience-enhanced contemporary populist assessment across six dimensions with embedded CSV output.",
      "analysis_prompt": "Phase 1: Cognitive Priming: You are an expert analyst specializing in contemporary populist political communication and democratic mobilization strategies. Phase 2: Framework Methodology: Your task is to analyze the provided text using the Populist Rhetoric Module (PRM) v5.0. This temporal module captures era-specific populist communication patterns (2010s-2020s) with salience weighting to reveal strategic emphasis. Phase 3: Operational Definitions: The framework evaluates 6 dimensions: People vs Elite Framing (conflict between ordinary people and a privileged elite), Authentic Representation Claims (representing genuine popular will), Anti-System Mobilization (mobilizing against existing political systems), Direct Democracy Appeals (emphasizing direct popular sovereignty), Common Sense vs Expertise (privileging popular wisdom over professional expertise), and Cultural Authenticity Claims (appealing to authentic cultural values). Phase 4: Scoring Protocol: For each dimension, score its intensity from 0.0 to 1.0. Also, assess its salience from 0.0 to 1.0, reflecting its rhetorical prominence. Provide the strongest 1-2 quotes as evidence. Calculate the three indices: core populist appeal score, populist mobilization score, and populist rhetoric index. Phase 5: Framework-Specific CSV Structure: Your scores CSV must contain exactly 16 columns in this order: aid, people_vs_elite_framing, authentic_representation_claims, anti_system_mobilization, direct_democracy_appeals, common_sense_vs_expertise, cultural_authenticity_claims, people_vs_elite_framing_salience, authentic_representation_claims_salience, anti_system_mobilization_salience, direct_democracy_appeals_salience, common_sense_vs_expertise_salience, cultural_authenticity_claims_salience, core_populist_appeal_score, populist_mobilization_score, populist_rhetoric_index. Your evidence CSV must contain exactly 6 columns: aid, dimension, quote_id, quote_text, confidence_score, context_type. Phase 6: Output Specification: Return a complete response containing both a comprehensive JSON analysis AND the embedded CSV segments using the exact delimiters and column structures specified in the output_contract."
    }
  },
  "dimension_groups": {
    "core_populist_appeals": ["people_vs_elite_framing", "authentic_representation_claims", "anti_system_mobilization"],
    "populist_mobilization_strategies": ["direct_democracy_appeals", "common_sense_vs_expertise", "cultural_authenticity_claims"]
  },
  "calculation_spec": {
    "core_populist_appeal_score": "(people_vs_elite_framing + authentic_representation_claims + anti_system_mobilization) / 3",
    "populist_mobilization_score": "(direct_democracy_appeals + common_sense_vs_expertise + cultural_authenticity_claims) / 3", 
    "populist_rhetoric_index": "(core_populist_appeal_score + populist_mobilization_score) / 2"
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
        "description": "CSV for all dimensional scores, salience scores, and calculated metrics.",
        "columns": [
          "aid",
          "people_vs_elite_framing", "authentic_representation_claims", "anti_system_mobilization",
          "direct_democracy_appeals", "common_sense_vs_expertise", "cultural_authenticity_claims",
          "people_vs_elite_framing_salience", "authentic_representation_claims_salience", "anti_system_mobilization_salience",
          "direct_democracy_appeals_salience", "common_sense_vs_expertise_salience", "cultural_authenticity_claims_salience",
          "core_populist_appeal_score", "populist_mobilization_score", "populist_rhetoric_index"
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
    "instructions": "IMPORTANT: Your response MUST include both a complete JSON analysis AND embedded CSV segments using the exact delimiters specified. The salience_ranking should be an ordered array of objects, each containing 'dimension', 'salience_score', and 'rank'. The scores CSV must include exactly 16 columns: aid + 6 dimension scores + 6 salience scores + 3 calculated indices. The evidence CSV must include exactly 6 columns: aid + dimension + quote_id + quote_text + confidence_score + context_type."
  }
}
```

</details> 