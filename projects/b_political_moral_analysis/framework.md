# Moral Foundations Theory Framework v4.2 - Tension Enhanced

**Version**: v4.2 - Tension Enhanced  
**Status**: Implementation Ready  
**Enhancement Type**: Moral Tension Pattern Analysis Integration  
**Base**: MFT v4.1 Salience-Enhanced + Issue #125 Tension Mathematics  

---

## Version 4.2 Enhancement: Moral Foundation Tension Analysis

### **🚨 NEW CAPABILITY: Moral Strategic Contradiction Index (MSCI)**

**Version 4.2** integrates breakthrough **moral tension analysis** based on Issue #125 specifications:
- **Moral Foundation Tension Scoring**: Quantifies moral contradictions between opposing foundations
- **Moral Strategic Contradiction Index**: Overall moral tension measurement across all foundation pairs
- **Moral Priority Coherence**: Analysis of moral foundation emphasis contradictions

**Research Foundation**: Moral analysis now reveals whether speakers demonstrate coherent moral reasoning or exhibit measurable moral contradictions in their foundation priorities.

---

## Moral Foundations Theory Core Analysis

*[Preserving all existing MFT v4.1 functionality with tension enhancement]*

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

## Revolutionary Moral Tension Mathematics (v4.2 Enhancement)

### **Moral Foundation Tension Scoring**

**Formula**: `Moral Tension = min(Foundation_score, Opposition_score) × |Foundation_salience - Opposition_salience|`

**MFT Foundation Opposing Pairs**:
1. **Care-Harm Tension**: `min(care_score, harm_score) × |care_salience - harm_salience|`
2. **Fairness-Cheating Tension**: `min(fairness_score, cheating_score) × |fairness_salience - cheating_salience|`  
3. **Loyalty-Betrayal Tension**: `min(loyalty_score, betrayal_score) × |loyalty_salience - betrayal_salience|`
4. **Authority-Subversion Tension**: `min(authority_score, subversion_score) × |authority_salience - subversion_salience|`
5. **Sanctity-Degradation Tension**: `min(sanctity_score, degradation_score) × |sanctity_salience - degradation_salience|`
6. **Liberty-Oppression Tension**: `min(liberty_score, oppression_score) × |liberty_salience - oppression_salience|`

### **Moral Strategic Contradiction Index (MSCI)**

**Formula**: `MSCI = (Sum of all Moral Tension Scores) / Number of Foundation Pairs`

```
MSCI = (Care_Harm_Tension + Fairness_Cheating_Tension + Loyalty_Betrayal_Tension + 
        Authority_Subversion_Tension + Sanctity_Degradation_Tension + Liberty_Oppression_Tension) / 6
```

### **Moral Foundation Tension Pattern Classification**

**MSCI Moral Coherence Assessment**:
- **0.00-0.12**: **Moral Coherence** - Consistent moral foundation priorities across all dimensions
- **0.13-0.25**: **Moral Complexity** - Moderate moral tensions with sophisticated foundation management
- **0.26-0.38**: **Moral Ambivalence** - Significant moral contradictions requiring interpretation  
- **0.39+**: **Moral Contradiction** - High tension from competing moral foundation claims

### **Advanced Moral Analytics**

**Moral Salience Concentration**: `MSC = Standard Deviation of Moral Foundation Salience Scores`
- **Focused Moral Identity** (MSC > 0.3): Clear moral foundation priorities
- **Distributed Moral Identity** (MSC < 0.2): Broad moral engagement across foundations

**Moral Tension-Salience Interaction Effects**:
- **High Moral Focus + Low MSCI**: Authentic moral identity with clear foundation priorities
- **High Moral Focus + High MSCI**: Moral identity confusion with competing foundation emphases  
- **Low Moral Focus + Low MSCI**: Sophisticated moral complexity with coherent foundation integration
- **Low Moral Focus + High MSCI**: Inconsistent moral reasoning across different foundation contexts

### **Moral Foundation Architecture Analysis**

**Individualizing vs Binding Foundation Balance**:
- **Care-Fairness Emphasis**: Liberal moral profile with low binding foundation tension
- **Loyalty-Authority-Sanctity Emphasis**: Conservative moral profile with low individualizing tension
- **Balanced Foundation Emphasis**: Complex moral reasoning across foundation categories

**Foundation-Specific Tension Patterns**:
- **Care-Harm Tension**: Compassion vs harm prevention emphasis contradictions
- **Liberty-Authority Tension**: Freedom vs order moral reasoning conflicts
- **Fairness-Loyalty Tension**: Justice vs group fidelity priority conflicts

---

## Enhanced Moral Foundation Agent Integration

### **Moral-Tension-Aware Analysis Instructions**

**Critical Enhancement**: Agents now assess both traditional moral foundation patterns AND moral contradiction patterns:

1. **Standard Foundation Scoring**: Foundation intensity (0.0-1.0) and salience (0.0-1.0) assessment for all 12 foundations
2. **Moral Tension Calculation**: Automated computation of 6 foundation pair tension scores  
3. **MSCI Assessment**: Moral Strategic Contradiction Index with moral coherence classification
4. **Moral Identity Analysis**: Salience concentration effects on moral reasoning consistency

**Agent Prompt Enhancement**: *"After completing traditional MFT moral foundation analysis, calculate moral tensions for all 6 foundation opposing pairs using the formula: min(foundation_score, opposition_score) × |foundation_salience - opposition_salience|. Compute the Moral Strategic Contradiction Index as the average of all tension scores. Assess whether the speaker demonstrates coherent moral reasoning or exhibits moral foundation contradictions."*

---

<details><summary>Machine-Readable Configuration (v4.2 Tension Enhanced)</summary>

```json
{
  "name": "mft_v4_2_tension_enhanced",
  "version": "v4.2", 
  "display_name": "Moral Foundations Theory Framework v4.2 - Tension Enhanced",
  "analysis_variants": {
    "default": {
      "description": "Complete salience-weighted moral foundation analysis with moral tension pattern quantification",
      "analysis_prompt": "You are an expert moral psychology analyst with deep knowledge of Moral Foundations Theory, moral reasoning, and cross-cultural moral research. Your perspective is grounded in moral psychology research, cognitive moral development theory, and empirical moral foundation studies. Your task is to analyze the provided text using the Moral Foundations Theory Framework v4.2 with TENSION-ENHANCED SALIENCE-WEIGHTED analysis. This framework now includes breakthrough moral tension pattern analysis in addition to traditional moral foundation assessment. The framework evaluates moral reasoning through 6 foundation pairs (12 total foundations) plus moral contradiction analysis. Focus on moral reasoning patterns and foundation priorities demonstrated in discourse. MORAL FOUNDATIONS (score 0.0-1.0): Care Foundation: Compassion, protection, suffering prevention - look for 'protect', 'care', 'compassion', 'sympathy', 'kindness', 'help', 'support', 'vulnerable', protection language. Harm Foundation: Cruelty concern, violence prevention - look for 'harm', 'hurt', 'violence', 'cruelty', 'abuse', 'suffering', 'victim', 'innocent', harm prevention. Fairness Foundation: Justice, equality, proportionality - look for 'fair', 'just', 'equal', 'rights', 'deserve', 'justice', 'equality', 'proportional', fairness appeals. Cheating Foundation: Unfairness concern, exploitation prevention - look for 'unfair', 'cheat', 'exploit', 'corrupt', 'fraud', 'discriminate', 'bias', unfairness concern. Loyalty Foundation: Group cohesion, fidelity - look for 'loyalty', 'solidarity', 'unity', 'team', 'group', 'allegiance', 'bond', 'commitment', group fidelity. Betrayal Foundation: Group abandonment concern - look for 'betray', 'abandon', 'desert', 'turncoat', 'traitor', 'disloyal', 'treachery', betrayal prevention. Authority Foundation: Hierarchy respect, tradition - look for 'authority', 'respect', 'order', 'tradition', 'hierarchy', 'leadership', 'legitimate', respect for authority. Subversion Foundation: Rebellion concern, hierarchy disruption - look for 'rebel', 'subvert', 'undermine', 'disrespect', 'chaos', 'disorder', 'illegitimate', subversion concern. Sanctity Foundation: Sacred preservation, purity - look for 'sacred', 'holy', 'pure', 'sanctity', 'divine', 'transcendent', 'blessed', 'spiritual', sacred language. Degradation Foundation: Contamination concern, profane prevention - look for 'degrade', 'contaminate', 'profane', 'pollute', 'corrupt', 'impure', 'desecrate', degradation concern. Liberty Foundation: Freedom, autonomy - look for 'freedom', 'liberty', 'autonomy', 'independence', 'choice', 'self-determination', 'free', freedom appeals. Oppression Foundation: Control concern, domination prevention - look for 'oppress', 'control', 'dominate', 'coerce', 'force', 'suppress', 'tyranny', oppression concern. CRITICAL: After scoring all foundations, you MUST rank them by SALIENCE - how central and prominent each moral foundation is to the overall moral reasoning, regardless of score magnitude. Consider: rhetorical emphasis, repetition patterns, structural positioning, thematic centrality, and discourse prominence in moral appeals. SALIENCE ≠ INTENSITY. For each foundation: 1. Score moral intensity from 0.0 to 1.0 based on frequency, centrality, and strength 2. Assess salience from 0.0 to 1.0 based on rhetorical prominence and emphasis in moral reasoning 3. Identify at least 2 direct quotations supporting moral assessment 4. Provide confidence rating from 0.0 to 1.0 based on evidence clarity. NEW v4.2 REQUIREMENT: MORAL TENSION ANALYSIS - After completing traditional foundation scoring, calculate moral tensions for all 6 foundation opposing pairs: Care-Harm, Fairness-Cheating, Loyalty-Betrayal, Authority-Subversion, Sanctity-Degradation, Liberty-Oppression. Calculate Moral Strategic Contradiction Index (MSCI) as the average of all tension scores. Classify moral pattern: Moral Coherence (0.00-0.12), Moral Complexity (0.13-0.25), Moral Ambivalence (0.26-0.38), Moral Contradiction (0.39+)."
    },
    "political_analysis": {
      "description": "Specialized moral foundation analysis for political discourse with tension analysis",
      "analysis_prompt": "You are conducting political moral foundation analysis using MFT v4.2 with tension enhancement. Focus on moral foundations most relevant to political discourse and moral reasoning in democratic contexts. Score all 12 moral foundations for both intensity and salience, with particular attention to how moral priorities create or avoid contradictions. Calculate moral tensions and assess moral coherence for political moral reasoning evaluation. Focus on moral foundation patterns that reveal political moral identity and reasoning consistency."
    }
  },
  "calculation_spec": {
    "salience_weighting_explanation": "CRITICAL: All moral calculations use salience-weighted analysis instead of static weights. Salience = how prominent/emphasized each moral foundation is in moral reasoning (0.0-1.0). Higher salience foundations reveal speaker's actual moral priorities and reasoning patterns.",
    "moral_tension_mathematics": "NEW v4.2: Moral tension quantification using formula: Moral Tension = min(Foundation_score, Opposition_score) × |Foundation_salience - Opposition_salience|. This measures moral contradictions where speakers simultaneously emphasize opposing moral foundations with different priority patterns.",
    "moral_foundation_tensions": {
      "care_harm_tension": "min(care_score, harm_score) × |care_salience - harm_salience|",
      "fairness_cheating_tension": "min(fairness_score, cheating_score) × |fairness_salience - cheating_salience|",
      "loyalty_betrayal_tension": "min(loyalty_score, betrayal_score) × |loyalty_salience - betrayal_salience|",
      "authority_subversion_tension": "min(authority_score, subversion_score) × |authority_salience - subversion_salience|",
      "sanctity_degradation_tension": "min(sanctity_score, degradation_score) × |sanctity_salience - degradation_salience|",
      "liberty_oppression_tension": "min(liberty_score, oppression_score) × |liberty_salience - oppression_salience|"
    },
    "moral_strategic_contradiction_index": "(care_harm_tension + fairness_cheating_tension + loyalty_betrayal_tension + authority_subversion_tension + sanctity_degradation_tension + liberty_oppression_tension) / 6. Measures overall moral contradiction patterns across all foundation pairs.",
    "moral_tension_classification": {
      "moral_coherence": "MSCI 0.00-0.12: Consistent moral foundation priorities across all dimensions",
      "moral_complexity": "MSCI 0.13-0.25: Moderate moral tensions with sophisticated foundation management", 
      "moral_ambivalence": "MSCI 0.26-0.38: Significant moral contradictions requiring interpretation",
      "moral_contradiction": "MSCI 0.39+: High tension from competing moral foundation claims"
    },
    "individualizing_foundations_index": "SALIENCE-WEIGHTED: Normalized sum of [(care_salience × care_score) + (fairness_salience × fairness_score)] minus [(harm_salience × harm_score) + (cheating_salience × cheating_score)] divided by relevant salience weights.",
    "binding_foundations_index": "SALIENCE-WEIGHTED: Normalized sum of [(loyalty_salience × loyalty_score) + (authority_salience × authority_score) + (sanctity_salience × sanctity_score)] minus [(betrayal_salience × betrayal_score) + (subversion_salience × subversion_score) + (degradation_salience × degradation_score)] divided by relevant salience weights.",
    "liberty_foundation_index": "SALIENCE-WEIGHTED: [(liberty_salience × liberty_score) - (oppression_salience × oppression_score)] divided by (liberty_salience + oppression_salience).",
    "moral_salience_concentration": "Standard deviation of all moral foundation salience scores. Measures moral reasoning focus: Low (<0.2) = distributed moral engagement, High (>0.3) = focused moral priorities."
  },
  "output_contract": {
    "schema": {
      "worldview": "string",
      "scores": "object",
      "evidence": "object",
      "confidence": "object",
      "reasoning": "object",
      "salience_ranking": "array",
      "foundation_indices": "object",
      "moral_profile": "string",
      "tension_analysis": "object",
      "moral_strategic_contradiction_index": "number",
      "moral_tension_classification": "string",
      "moral_foundation_tensions": "object",
      "moral_salience_concentration": "number"
    },
    "instructions": "IMPORTANT: Your response MUST be a single, valid JSON object and nothing else. Do not include any text, explanations, or markdown code fences before or after the JSON object. The salience_ranking should be an ordered array of objects for all 12 foundations, each containing 'foundation' (string), 'salience_score' (0.0-1.0), and 'rank' (integer), ordered from most salient (rank 1) to least salient (rank 12). The foundation_indices object should contain calculated individualizing_foundations_index, binding_foundations_index, and liberty_foundation_index using salience-weighted formulas. The tension_analysis must include all 6 moral foundation tension scores, Moral Strategic Contradiction Index (MSCI), moral pattern classification, and moral salience concentration index."
  }
}
```

</details>

---

## Conclusion

The Moral Foundations Theory Framework v4.2 represents a breakthrough in moral psychology analysis by combining established foundation assessment with pioneering moral tension pattern quantification. This enhancement enables systematic analysis of moral reasoning coherence - revealing whether speakers demonstrate consistent moral priorities or exhibit measurable moral contradictions in their foundation emphasis.

**Key Innovation**: MFT v4.2 transforms moral analysis from measuring **what moral foundations speakers prioritize** to measuring **how coherently they prioritize them**, providing unprecedented insight into moral reasoning authenticity and ethical consistency.

**Research Foundation**: Built on validated tension mathematics from Issue #125, providing empirical foundation for moral psychology research and ethical reasoning assessment.

**Political Applications**: Enables systematic evaluation of moral reasoning coherence in political discourse, revealing authentic moral identity vs tactical moral positioning.

---

**Moral Foundation Tension Discovery**:
- **Care vs Harm**: Compassion emphasis vs cruelty prevention priority
- **Fairness vs Cheating**: Justice appeals vs unfairness concern balance  
- **Loyalty vs Betrayal**: Group fidelity vs abandonment prevention
- **Authority vs Subversion**: Hierarchy respect vs rebellion concern
- **Sanctity vs Degradation**: Sacred preservation vs contamination prevention
- **Liberty vs Oppression**: Freedom emphasis vs control concern

**Research Applications Enabled**:
- Moral reasoning coherence studies across political contexts
- Cross-cultural moral foundation tension pattern analysis  
- Ethical consistency evaluation for leadership assessment
- Moral identity authenticity vs tactical positioning research

---

**Version History**:
- **v4.1**: Salience-weighted moral foundation analysis based on meta-analysis research
- **v4.2**: Added moral tension pattern analysis and Moral Strategic Contradiction Index

**Next Enhancements**: Integration with other frameworks for cross-framework moral-political correlation analysis.

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "moral_foundations_theory_v4_2_tension_enhanced",
  "version": "v4.2",
  "display_name": "Moral Foundations Theory v4.2 - Tension Enhanced",
  "analysis_variants": {
    "default": {
      "description": "Complete implementation of MFT v4.2 with tension analysis and salience weighting",
      "analysis_prompt": "You are an expert moral psychologist with deep knowledge of Moral Foundations Theory and political discourse analysis. Your task is to analyze the provided text for moral foundation patterns using the MFT v4.2 Tension Enhanced framework.\n\nThis framework examines moral reasoning through six foundation pairs:\n\n1. **Care/Harm** (0.0-1.0): Compassion, empathy, protection of vulnerable individuals from suffering\n2. **Fairness/Cheating** (0.0-1.0): Justice, equality, proportionality, and rights-based reasoning\n3. **Loyalty/Betrayal** (0.0-1.0): Group solidarity, patriotism, team loyalty, and self-sacrifice for the group\n4. **Authority/Subversion** (0.0-1.0): Respect for hierarchy, tradition, leadership, and legitimate institutions\n5. **Sanctity/Degradation** (0.0-1.0): Purity, divinity, sacredness, and avoidance of contamination\n6. **Liberty/Oppression** (0.0-1.0): Freedom from oppression, resistance to domination, and personal autonomy\n\nFor each foundation, analyze the text for:\n- Direct appeals to the foundation\n- Implicit moral reasoning patterns\n- Emotional language that activates the foundation\n- Policy arguments grounded in the foundation\n\nCalculate the **Moral Strategic Contradiction Index (MSCI)** by measuring tension between opposing moral emphases. Higher MSCI indicates more contradictory moral framing.\n\nProvide evidence from the text for each score, confidence assessments, and detailed reasoning explaining your analysis."
    }
  },
  "calculation_spec": {
    "msci_score": "sqrt(sum((foundation_i - foundation_j)^2 for all opposing pairs)) / 6"
  },
  "output_contract": {
    "schema": {
      "moral_foundations": "object",
      "msci_score": "number",
      "salience_analysis": "object",
      "evidence": "object",
      "confidence": "object",
      "reasoning": "object"
    },
    "instructions": "IMPORTANT: Your response MUST be a single, valid JSON object and nothing else. Do not include any text, explanations, or markdown code fences before or after the JSON object."
  }
}
```

</details>