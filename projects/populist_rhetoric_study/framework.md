# Cohesive Flourishing Framework v4.4 - Tension Enhanced

**Version**: v4.4 - Tension Enhanced  
**Status**: Implementation Ready  
**Enhancement Type**: Rhetorical Tension Pattern Analysis Integration  
**Base**: CFF v4.3 Salience-Weighted + Issue #125 Tension Mathematics  

---

## Version 4.4 Enhancement: Rhetorical Tension Pattern Analysis

### **🚨 NEW CAPABILITY: Strategic Contradiction Index (SCI)**

**Version 4.4** integrates breakthrough **tension pattern analysis** based on Issue #125 specifications:
- **Dimensional Tension Scoring**: Quantifies rhetorical contradictions between opposing dimensions
- **Strategic Contradiction Index**: Overall tension measurement across all opposing pairs
- **Salience-Tension Interaction**: Advanced analysis of emphasis patterns and strategic coherence

**Research Foundation**: Built on validated pilot analysis showing 4 distinct tension pattern types:
- **Harmony Strategy** (SCI = 0.07): Low tension, strategic coherence
- **Coalition Building** (SCI = 0.15): Moderate tension, balanced appeal  
- **Revolutionary Coherence** (SCI = 0.25): High intensity, aligned salience
- **Strategic Overreach** (SCI = 0.38): High tension from competing emphases

---

## Cohesive Flourishing Framework Core Analysis

*[Core framework analysis identical to v4.3 - preserving all existing functionality]*

### **Identity Axis**

**Tribal Dominance** (0.0-1.0): In-group supremacy and exclusionary identity patterns  
**Individual Dignity** (0.0-1.0): Universal human worth and inclusive dignity appeals

### **Emotional Climate**

**Fear** (0.0-1.0): Crisis mentality, threat perception, vulnerability emphasis  
**Hope** (0.0-1.0): Progress orientation, opportunity focus, optimistic vision

### **Success Orientation** 

**Envy** (0.0-1.0): Resentment toward others' success, zero-sum thinking  
**Compersion** (0.0-1.0): Celebration of others' success, abundance mindset

### **Relational Climate**

**Enmity** (0.0-1.0): Hostility, antagonism, adversarial positioning  
**Amity** (0.0-1.0): Friendship, cooperation, collaborative approach

### **Goal Orientation**

**Fragmentative Goals** (0.0-1.0): Division, separation, destructive objectives  
**Cohesive Goals** (0.0-1.0): Unity, building, integrative objectives

---

## Revolutionary Tension Mathematics (v4.4 Enhancement)

### **Dimensional Tension Scoring**

**Formula**: `Tension Score = min(Anchor_A_score, Anchor_B_score) × |Salience_A - Salience_B|`

**CFF Opposing Pairs**:
1. **Fear-Hope Tension**: `min(fear_score, hope_score) × |fear_salience - hope_salience|`
2. **Enmity-Amity Tension**: `min(enmity_score, amity_score) × |enmity_salience - amity_salience|`  
3. **Envy-Compersion Tension**: `min(envy_score, compersion_score) × |envy_salience - compersion_salience|`
4. **Dominance-Dignity Tension**: `min(tribal_dominance_score, individual_dignity_score) × |tribal_dominance_salience - individual_dignity_salience|`
5. **Fragmentative-Cohesive Tension**: `min(fragmentative_goals_score, cohesive_goals_score) × |fragmentative_goals_salience - cohesive_goals_salience|`

### **Strategic Contradiction Index (SCI)**

**Formula**: `SCI = (Sum of all Tension Scores) / Number of Opposing Pairs`

```
SCI = (Fear_Hope_Tension + Enmity_Amity_Tension + Envy_Compersion_Tension + 
       Dominance_Dignity_Tension + Fragmentative_Cohesive_Tension) / 5
```

### **Tension Pattern Classification**

**SCI Interpretation Framework**:
- **0.00-0.10**: **Harmony Strategy** - Minimal rhetorical contradictions
- **0.11-0.20**: **Coalition Building** - Moderate tension with strategic balance
- **0.21-0.30**: **Revolutionary Coherence** - High intensity with aligned emphasis
- **0.31+**: **Strategic Overreach** - High tension from competing appeals

### **Advanced Tension Analytics**

**Salience Concentration Index**: `SCI-S = Standard Deviation of all Salience Scores`
- **Low Concentration** (SCI-S < 0.2): Distributed emphasis across dimensions
- **High Concentration** (SCI-S > 0.3): Focused emphasis on few dimensions

**Tension-Salience Interaction Effects**:
- **High Concentration + Low SCI**: Coherent focused strategy
- **High Concentration + High SCI**: Strategic messaging overload  
- **Low Concentration + Low SCI**: Sophisticated coalition building
- **Low Concentration + High SCI**: Unfocused rhetorical strategy

---

## Enhanced World-Class Agent Integration

### **Tension-Aware Analysis Instructions**

**Critical Enhancement**: Agents now assess both traditional cohesion patterns AND rhetorical tension patterns:

1. **Standard Dimension Scoring**: Intensity (0.0-1.0) and Salience (0.0-1.0) for all 10 dimensions
2. **Tension Calculation**: Automated computation of 5 dimensional tension scores  
3. **SCI Assessment**: Strategic Contradiction Index calculation with pattern classification
4. **Interaction Analysis**: Salience concentration effects on strategic coherence

**Agent Prompt Enhancement**: *"After completing traditional CFF analysis, calculate dimensional tensions for all opposing pairs using the formula: min(score_A, score_B) × |salience_A - salience_B|. Compute the Strategic Contradiction Index as the average of all tension scores. Classify the tension pattern type based on SCI ranges."*

---

<details><summary>Machine-Readable Configuration (v4.4 Tension Enhanced)</summary>

```json
{
  "name": "cff_v4_4_tension_enhanced",
  "version": "v4.4", 
  "display_name": "Cohesive Flourishing Framework v4.4 - Tension Enhanced",
  "analysis_variants": {
    "default": {
      "description": "Complete salience-weighted analysis with rhetorical tension pattern quantification",
      "analysis_prompt": "You are an expert discourse analyst specializing in social cohesion and democratic health assessment, with deep knowledge of affective political psychology, social identity theory, and democratic resilience. Your perspective is grounded in political psychology research and social cohesion theory. Your task is to analyze the provided text using the Cohesive Flourishing Framework v4.4 with TENSION-ENHANCED SALIENCE-WEIGHTED analysis. This framework now includes breakthrough rhetorical tension pattern analysis in addition to traditional cohesion measurement. The framework evaluates 10 dimensions across three analytical layers: IDENTITY AXIS: Tribal Dominance (0.0-1.0): In-group supremacy, exclusionary identity - look for 'us versus them', 'our people', 'real Americans', 'superior group', 'chosen people', 'group loyalty', 'tribal solidarity'. Individual Dignity (0.0-1.0): Universal human worth, inclusive dignity - look for 'human dignity', 'inherent worth', 'equal worth', 'individual dignity', 'respect for persons', 'universal rights', 'common humanity'. EMOTIONAL CLIMATE: Fear (0.0-1.0): Crisis, threat, vulnerability - look for 'crisis', 'disaster', 'emergency', 'threat', 'danger', 'vulnerable', 'under attack', 'existential risk'. Hope (0.0-1.0): Progress, opportunity, optimism - look for 'progress', 'opportunity', 'better future', 'positive change', 'breakthrough', 'advancement', 'improvement'. SUCCESS ORIENTATION: Envy (0.0-1.0): Resentment, grievance, zero-sum - look for 'unfair advantage', 'rigged system', 'privileged elite', 'didn't earn it', 'taking our share', 'wealth inequality'. Compersion (0.0-1.0): Celebration, merit, abundance - look for 'well-deserved', 'hard-earned', 'celebrate success', 'rising tide', 'shared prosperity', 'merit-based'. RELATIONAL CLIMATE: Enmity (0.0-1.0): Hostility, conflict, aggression - look for 'enemy', 'fight', 'battle', 'destroy', 'attack', 'hostile', 'aggressive', 'evil', 'corrupt'. Amity (0.0-1.0): Friendship, cooperation, unity - look for 'friend', 'ally', 'together', 'united', 'cooperation', 'partnership', 'solidarity', 'fellowship'. GOAL ORIENTATION: Fragmentative Goals (0.0-1.0): Division, separation, destruction - look for 'tear down', 'divide', 'separate', 'fragment', 'break apart', 'destroy unity'. Cohesive Goals (0.0-1.0): Unity, building, integration - look for 'bring together', 'unite', 'build', 'strengthen bonds', 'create unity', 'forge connections'. CRITICAL: After scoring all dimensions, you MUST rank them by SALIENCE - how central and prominent each dimension is to the overall discourse, regardless of score magnitude. Consider: rhetorical emphasis, repetition patterns, structural positioning, thematic centrality, and discourse prominence. SALIENCE ≠ INTENSITY. For each dimension: 1. Score intensity from 0.0 to 1.0 based on frequency, centrality, and strength 2. Assess salience from 0.0 to 1.0 based on rhetorical prominence and discourse emphasis 3. Identify at least 2 direct quotations supporting your assessment 4. Provide confidence rating from 0.0 to 1.0 based on evidence clarity. NEW v4.4 REQUIREMENT: TENSION PATTERN ANALYSIS - After completing traditional scoring, calculate rhetorical tensions for all 5 opposing pairs using the formula: Tension Score = min(Anchor_A_score, Anchor_B_score) × |Salience_A - Salience_B|. Calculate Strategic Contradiction Index (SCI) as the average of all tension scores. Classify tension pattern: Harmony Strategy (0.00-0.10), Coalition Building (0.11-0.20), Revolutionary Coherence (0.21-0.30), Strategic Overreach (0.31+)."
    },
    "descriptive_only": {
      "description": "Simplified tension-enhanced version focusing on observable patterns",
      "analysis_prompt": "You are an expert discourse analyst. Analyze the provided text using the Cohesive Flourishing Framework v4.4 with tension-enhanced salience weighting focusing on descriptive patterns. Score the 10 dimensions from 0.0 to 1.0: Tribal Dominance, Individual Dignity, Fear, Hope, Envy, Compersion, Enmity, Amity, Fragmentative Goals, Cohesive Goals. CRITICAL: Also assess salience (rhetorical prominence) for each dimension from 0.0 to 1.0. Calculate tension scores for opposing pairs and Strategic Contradiction Index. Provide basic evidence, confidence assessments, salience ranking, and tension pattern classification."
    }
  },
  "calculation_spec": {
    "salience_weighting_explanation": "CRITICAL: All indices use salience-weighted calculations instead of static weights. Salience = how prominent/emphasized each dimension is in the discourse (0.0-1.0). Higher salience dimensions get more weight in calculations because they represent what the speaker actually emphasizes.",
    "tension_mathematics_explanation": "NEW v4.4: Rhetorical tension quantification using formula: Tension Score = min(Anchor_A_score, Anchor_B_score) × |Salience_A - Salience_B|. This measures strategic contradictions where speakers simultaneously employ opposing appeals with significant intensity and different salience patterns.",
    "dimensional_tensions": {
      "fear_hope_tension": "min(fear_score, hope_score) × |fear_salience - hope_salience|",
      "enmity_amity_tension": "min(enmity_score, amity_score) × |enmity_salience - amity_salience|",
      "envy_compersion_tension": "min(envy_score, compersion_score) × |envy_salience - compersion_salience|",
      "dominance_dignity_tension": "min(tribal_dominance_score, individual_dignity_score) × |tribal_dominance_salience - individual_dignity_salience|",
      "fragmentative_cohesive_tension": "min(fragmentative_goals_score, cohesive_goals_score) × |fragmentative_goals_salience - cohesive_goals_salience|"
    },
    "strategic_contradiction_index": "(fear_hope_tension + enmity_amity_tension + envy_compersion_tension + dominance_dignity_tension + fragmentative_cohesive_tension) / 5. Measures overall rhetorical tension across all opposing dimensional pairs.",
    "tension_classification": {
      "harmony_strategy": "SCI 0.00-0.10: Minimal rhetorical contradictions, strategic coherence",
      "coalition_building": "SCI 0.11-0.20: Moderate tension with strategic balance management", 
      "revolutionary_coherence": "SCI 0.21-0.30: High intensity with aligned salience patterns",
      "strategic_overreach": "SCI 0.31+: High tension from competing high-salience appeals"
    },
    "descriptive_cohesion_index": "SALIENCE-WEIGHTED: Normalized sum of [(hope_salience × hope_score - fear_salience × fear_score) + (compersion_salience × compersion_score - envy_salience × envy_score) + (amity_salience × amity_score - enmity_salience × enmity_score)] divided by sum of all salience weights.",
    "motivational_cohesion_index": "SALIENCE-WEIGHTED: Includes goal orientation dimension in addition to descriptive elements.",
    "full_cohesion_index": "SALIENCE-WEIGHTED: Complete cohesion assessment including identity axis contributions.",
    "salience_concentration_index": "Standard deviation of all salience scores. Measures rhetorical focus: Low (<0.2) = distributed emphasis, High (>0.3) = focused emphasis.",
    "tension_salience_interaction": "Advanced analytics combining tension patterns with salience concentration for strategic communication architecture assessment."
  },
  "output_contract": {
    "schema": {
      "worldview": "string",
      "scores": "object",
      "evidence": "object", 
      "confidence": "object",
      "reasoning": "object",
      "salience_ranking": "array",
      "indices": "object",
      "tension_analysis": "object",
      "strategic_contradiction_index": "number",
      "tension_classification": "string",
      "dimensional_tensions": "object",
      "salience_concentration_index": "number"
    },
    "instructions": "IMPORTANT: Your response MUST be a single, valid JSON object and nothing else. Do not include any text, explanations, or markdown code fences before or after the JSON object. The salience_ranking should be an ordered array of objects, each containing 'dimension', 'salience_score', and 'rank'. The tension_analysis object must include all 5 dimensional tension scores, Strategic Contradiction Index (SCI), tension pattern classification, and salience concentration index. All calculations must use salience weights and tension mathematics as specified."
  }
}
```

</details>

---

## Conclusion

The Cohesive Flourishing Framework v4.4 represents a breakthrough in rhetorical analysis by combining established cohesion measurement with pioneering tension pattern quantification. This enhancement enables systematic analysis of strategic communication architecture - revealing whether speakers employ coherent messaging strategies or create measurable rhetorical contradictions.

**Key Innovation**: CFF v4.4 transforms discourse analysis from measuring **what speakers emphasize** to measuring **how coherently they emphasize it**, providing unprecedented insight into strategic communication effectiveness and rhetorical authenticity.

**Research Foundation**: Built on validated tension pattern classification from pilot studies, providing empirical foundation for strategic communication research and practical messaging optimization.

**Status**: Ready for implementation across the framework ecosystem following Issue #125 specifications.

---

**Version History**:
- **v4.3**: Salience-weighted analysis based on meta-analysis research
- **v4.4**: Added rhetorical tension pattern analysis and Strategic Contradiction Index

**Next Enhancements**: Integration with other frameworks (CAF, MFT, Lakoff) for ecosystem-wide tension analysis capabilities.

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "cohesive_flourishing_framework_v4_4_tension_enhanced",
  "version": "v4.4", 
  "display_name": "Cohesive Flourishing Framework v4.4 - Tension Enhanced",
  "analysis_variants": {
    "default": {
      "description": "Complete implementation of CFF v4.4 with tension analysis and Strategic Contradiction Index",
      "analysis_prompt": "You are an expert political discourse analyst with deep knowledge of rhetorical strategies and social cohesion theory. Your task is to analyze the provided text for cohesive flourishing patterns using the CFF v4.4 Tension Enhanced framework.\n\nThis framework examines discourse across multiple dimensions:\n\n**Cohesion Dimensions**:\n1. **Unifying/Divisive** (0.0-1.0): Language that brings people together vs. creates divisions\n2. **Individual/Collective** (0.0-1.0): Focus on individual agency vs. collective action\n3. **Crisis/Opportunity** (0.0-1.0): Framing challenges as threats vs. possibilities\n4. **Past/Future** (0.0-1.0): Orientation toward tradition vs. innovation\n5. **Internal/External** (0.0-1.0): Focus on domestic vs. international concerns\n\nFor each dimension, analyze the text for:\n- Direct rhetorical appeals\n- Implicit framing patterns\n- Emotional language and imagery\n- Policy arguments and solutions\n\nCalculate the **Strategic Contradiction Index (SCI)** by measuring tension between opposing dimensional emphases. Higher SCI indicates strategic overreach or contradictory messaging.\n\nProvide evidence from the text for each score, confidence assessments, salience analysis showing which dimensions receive the most rhetorical emphasis, and detailed reasoning explaining your analysis."
    }
  },
  "calculation_spec": {
    "sci_score": "sqrt(sum((dimension_positive - dimension_negative)^2 for all dimension pairs)) / 5"
  },
  "output_contract": {
    "schema": {
      "cohesion_dimensions": "object",
      "sci_score": "number", 
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