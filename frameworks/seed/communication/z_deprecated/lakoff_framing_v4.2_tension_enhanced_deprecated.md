# Lakoff Framing Framework v4.2 - Tension Enhanced

**Version**: v4.2 - Tension Enhanced  
**Status**: Implementation Ready  
**Enhancement Type**: Family Model Tension Pattern Analysis Integration  
**Base**: Lakoff v4.1 Salience-Enhanced + Issue #125 Tension Mathematics  

---

## Version 4.2 Enhancement: Family Model Tension Analysis

### **🚨 NEW CAPABILITY: Family Model Strategic Contradiction Index (FMSCI)**

**Version 4.2** integrates breakthrough **family model tension analysis** based on Issue #125 specifications:
- **Family Model Tension Scoring**: Quantifies moral contradictions between opposing family model dimensions
- **Family Model Strategic Contradiction Index**: Overall moral system tension measurement
- **Moral Framework Coherence**: Analysis of family model emphasis contradictions and strategic coherence

**Research Foundation**: Family model analysis now reveals whether speakers demonstrate coherent moral framework or exhibit measurable contradictions in their family model reasoning.

---

## Lakoff Framing Framework Core Analysis

*[Preserving all existing Lakoff v4.1 functionality with tension enhancement]*

### **Three Bipolar Dimensions: Family Model Architecture**

**1. Authority vs Empathy**
- **Strict Father (1.0)**: Strong leadership, moral authority, decisive action
- **Nurturant Parent (0.0)**: Understanding, inclusive dialogue, listening to voices

**2. Competition vs Cooperation**  
- **Strict Father (1.0)**: Natural hierarchy, merit-based systems, individual achievement
- **Nurturant Parent (0.0)**: Working together, shared responsibility, collaborative approaches

**3. Self-Reliance vs Interdependence**
- **Strict Father (1.0)**: Personal responsibility, self-reliance, bootstrap philosophy  
- **Nurturant Parent (0.0)**: Stronger together, mutual dependence, common good emphasis

---

## Revolutionary Family Model Tension Mathematics (v4.2 Enhancement)

### **Family Model Tension Scoring**

**Formula**: `Family Model Tension = min(Strict_Father_score, Nurturant_Parent_score) × |Strict_Father_salience - Nurturant_Parent_salience|`

**Note**: Since Lakoff dimensions are bipolar (0.0-1.0 scale where 1.0 = Strict Father, 0.0 = Nurturant Parent), tension calculation uses:
- **Strict Father Score** = Dimension score (0.0-1.0)
- **Nurturant Parent Score** = (1.0 - Dimension score) for each dimension

**Lakoff Family Model Tension Pairs**:
1. **Authority-Empathy Tension**: `min(authority_score, (1.0 - authority_score)) × |authority_salience - (1.0 - authority_salience)|`
2. **Competition-Cooperation Tension**: `min(competition_score, (1.0 - competition_score)) × |competition_salience - (1.0 - competition_salience)|`  
3. **Self-Reliance-Interdependence Tension**: `min(self_reliance_score, (1.0 - self_reliance_score)) × |self_reliance_salience - (1.0 - self_reliance_salience)|`

### **Family Model Strategic Contradiction Index (FMSCI)**

**Formula**: `FMSCI = (Sum of all Family Model Tension Scores) / Number of Dimensions`

```
FMSCI = (Authority_Empathy_Tension + Competition_Cooperation_Tension + Self_Reliance_Interdependence_Tension) / 3
```

### **Family Model Tension Pattern Classification**

**FMSCI Family Model Coherence Assessment**:
- **0.00-0.15**: **Moral Framework Coherence** - Consistent family model across all dimensions
- **0.16-0.30**: **Moral Framework Complexity** - Moderate tensions with sophisticated family model integration
- **0.31-0.45**: **Moral Framework Ambivalence** - Significant family model contradictions requiring interpretation  
- **0.46+**: **Moral Framework Contradiction** - High tension from incompatible family model elements

### **Advanced Family Model Analytics**

**Family Model Salience Concentration**: `FMSC = Standard Deviation of Family Model Dimension Salience Scores`
- **Focused Moral Framework** (FMSC > 0.3): Clear family model dimensional priorities
- **Distributed Moral Framework** (FMSC < 0.2): Broad engagement across family model dimensions

**Family Model Tension-Salience Interaction Effects**:
- **High Framework Focus + Low FMSCI**: Authentic moral framework with clear family model priorities
- **High Framework Focus + High FMSCI**: Moral framework confusion with competing family model emphases  
- **Low Framework Focus + Low FMSCI**: Sophisticated moral complexity with coherent family model integration
- **Low Framework Focus + High FMSCI**: Inconsistent family model reasoning across moral contexts

### **Family Model Strategic Architecture Analysis**

**Strict Father vs Nurturant Parent Coherence**:
- **Strict Father Coherence**: High authority, competition, self-reliance with low tensions
- **Nurturant Parent Coherence**: High empathy, cooperation, interdependence with low tensions
- **Mixed Framework**: Moderate tensions from balancing both family model elements

**Dimensional Priority Analysis**:
- **Authority-Empathy Priority**: Which family model element receives most rhetorical investment
- **Competition-Cooperation Balance**: Strategic choices about individual vs collective emphasis
- **Self-Reliance-Interdependence Framework**: Personal responsibility vs mutual dependence priority

---

## Enhanced Family Model Agent Integration

### **Family-Model-Tension-Aware Analysis Instructions**

**Critical Enhancement**: Agents now assess both traditional family model patterns AND moral framework contradiction patterns:

1. **Standard Family Model Scoring**: Dimension position (0.0-1.0) and salience (0.0-1.0) assessment for 3 bipolar dimensions
2. **Family Model Tension Calculation**: Automated computation of 3 family model tension scores  
3. **FMSCI Assessment**: Family Model Strategic Contradiction Index with coherence classification
4. **Moral Framework Analysis**: Salience concentration effects on family model reasoning consistency

**Agent Prompt Enhancement**: *"After completing traditional Lakoff family model analysis, calculate family model tensions for all 3 bipolar dimensions. For each dimension, use min(score, 1.0-score) × |salience_difference| to measure internal coherence tensions. Compute the Family Model Strategic Contradiction Index as the average of all tension scores. Assess whether the speaker demonstrates coherent family model reasoning or exhibits moral framework contradictions."*

---

<details><summary>Machine-Readable Configuration (v4.2 Tension Enhanced)</summary>

```json
{
  "name": "lakoff_framing_v4_2_tension_enhanced",
  "version": "v4.2", 
  "display_name": "Lakoff Framing Framework v4.2 - Tension Enhanced",
  "analysis_variants": {
    "default": {
      "description": "Complete salience-weighted family model analysis with moral framework tension pattern quantification",
      "analysis_prompt": "You are an expert in cognitive linguistics and political psychology, specializing in Lakoff's family model theory and moral framework analysis. Your perspective is grounded in cognitive linguistics research, family metaphor theory, and political psychology. Your task is to analyze the provided text using the Lakoff Framing Framework v4.2 with TENSION-ENHANCED SALIENCE-WEIGHTED analysis. This framework now includes breakthrough family model tension pattern analysis in addition to traditional family model assessment. The framework evaluates moral reasoning through 3 bipolar dimensions plus moral framework contradiction analysis. Focus on family model reasoning patterns and moral framework priorities demonstrated in discourse. FAMILY MODEL DIMENSIONS (score 0.0-1.0, where 1.0 = Strict Father, 0.0 = Nurturant Parent): Authority vs Empathy: Strict Father (1.0) - 'strong leadership', 'moral authority', 'decisive action', 'firm discipline', 'clear hierarchy', 'authoritative guidance'; Nurturant Parent (0.0) - 'listen to voices', 'understand perspectives', 'inclusive dialogue', 'empathetic response', 'collaborative decision', 'shared input'. Competition vs Cooperation: Strict Father (1.0) - 'natural hierarchy', 'merit-based', 'individual achievement', 'competitive advantage', 'personal success', 'winners and losers'; Nurturant Parent (0.0) - 'working together', 'shared responsibility', 'collaboration', 'mutual support', 'collective success', 'everyone benefits'. Self-Reliance vs Interdependence: Strict Father (1.0) - 'personal responsibility', 'self-reliance', 'bootstrap', 'individual accountability', 'stand on own', 'self-sufficient'; Nurturant Parent (0.0) - 'stronger together', 'mutual dependence', 'common good', 'interconnected', 'shared resources', 'community support'. CRITICAL: After scoring all dimensions, you MUST rank them by SALIENCE - how central and prominent each family model dimension is to the overall moral reasoning, regardless of score magnitude. Consider: rhetorical emphasis, repetition patterns, structural positioning, thematic centrality, and discourse prominence in moral framework appeals. SALIENCE ≠ INTENSITY. For each dimension: 1. Score family model position from 0.0 to 1.0 (Strict Father to Nurturant Parent continuum) 2. Assess salience from 0.0 to 1.0 based on rhetorical prominence and emphasis in moral framework 3. Identify at least 2 direct quotations supporting family model assessment 4. Provide confidence rating from 0.0 to 1.0 based on evidence clarity. NEW v4.2 REQUIREMENT: FAMILY MODEL TENSION ANALYSIS - After completing traditional family model scoring, calculate family model tensions for all 3 bipolar dimensions. For each dimension, calculate tension using: min(dimension_score, 1.0 - dimension_score) × salience_concentration_effect. Calculate Family Model Strategic Contradiction Index (FMSCI) as the average of all tension scores. Classify family model pattern: Moral Framework Coherence (0.00-0.15), Moral Framework Complexity (0.16-0.30), Moral Framework Ambivalence (0.31-0.45), Moral Framework Contradiction (0.46+)."
    },
    "political_communication": {
      "description": "Specialized family model analysis for political discourse with tension analysis",
      "analysis_prompt": "You are conducting political family model analysis using Lakoff v4.2 with tension enhancement. Focus on family model elements most relevant to political discourse and moral framework reasoning in democratic contexts. Score all 3 bipolar dimensions for both position and salience, with particular attention to how family model priorities create or avoid contradictions. Calculate family model tensions and assess moral framework coherence for political communication evaluation. Focus on family model patterns that reveal political moral framework identity and reasoning consistency."
    }
  },
  "calculation_spec": {
    "salience_weighting_explanation": "CRITICAL: All family model calculations use salience-weighted analysis instead of static weights. Salience = how prominent/emphasized each family model dimension is in moral reasoning (0.0-1.0). Higher salience dimensions reveal speaker's actual moral framework priorities and reasoning patterns.",
    "family_model_tension_mathematics": "NEW v4.2: Family model tension quantification for bipolar dimensions using formula: Family Model Tension = min(dimension_score, 1.0 - dimension_score) × |salience_effect|. This measures moral framework contradictions where speakers demonstrate internal tensions within family model dimensions.",
    "family_model_tensions": {
      "authority_empathy_tension": "min(authority_score, (1.0 - authority_score)) × salience_concentration_factor. Measures internal tension between strict father and nurturant parent authority approaches.",
      "competition_cooperation_tension": "min(competition_score, (1.0 - competition_score)) × salience_concentration_factor. Measures internal tension between competitive and cooperative moral frameworks.",
      "self_reliance_interdependence_tension": "min(self_reliance_score, (1.0 - self_reliance_score)) × salience_concentration_factor. Measures internal tension between individual and collective responsibility frameworks."
    },
    "family_model_strategic_contradiction_index": "(authority_empathy_tension + competition_cooperation_tension + self_reliance_interdependence_tension) / 3. Measures overall family model contradiction patterns across all bipolar dimensions.",
    "family_model_tension_classification": {
      "moral_framework_coherence": "FMSCI 0.00-0.15: Consistent family model across all dimensions",
      "moral_framework_complexity": "FMSCI 0.16-0.30: Moderate tensions with sophisticated family model integration", 
      "moral_framework_ambivalence": "FMSCI 0.31-0.45: Significant family model contradictions requiring interpretation",
      "moral_framework_contradiction": "FMSCI 0.46+: High tension from incompatible family model elements"
    },
    "strict_father_model_score": "SALIENCE-WEIGHTED: [(authority_salience × authority_score) + (competition_salience × competition_score) + (self_reliance_salience × self_reliance_score)] / (authority_salience + competition_salience + self_reliance_salience).",
    "nurturant_parent_model_score": "SALIENCE-WEIGHTED: [(authority_salience × (1.0 - authority_score)) + (competition_salience × (1.0 - competition_score)) + (self_reliance_salience × (1.0 - self_reliance_score))] / (authority_salience + competition_salience + self_reliance_salience).",
    "family_model_coherence_index": "Math.abs(strict_father_model_score - nurturant_parent_model_score) using salience-weighted calculations. Measures consistency of family model direction across dimensions.",
    "family_model_salience_concentration": "Standard deviation of family model dimension salience scores. Measures moral framework focus: Low (<0.2) = distributed family model engagement, High (>0.3) = focused family model priorities."
  },
  "output_contract": {
    "schema": {
      "family_model_analysis": "string",
      "dimension_scores": "object",
      "salience_ranking": "array",
      "coherence_assessment": "string",
      "moral_strategy_analysis": "string",
      "tension_analysis": "object",
      "family_model_strategic_contradiction_index": "number",
      "family_model_tension_classification": "string",
      "family_model_tensions": "object",
      "family_model_salience_concentration": "number"
    },
    "instructions": "IMPORTANT: Your response MUST be a single, valid JSON object and nothing else. Do not include any text, explanations, or markdown code fences before or after the JSON object. The salience_ranking should be an ordered array of objects for all 3 dimensions, each containing 'dimension' (string), 'salience_score' (0.0-1.0), and 'rank' (integer), ordered from most salient (rank 1) to least salient (rank 3). The tension_analysis must include all 3 family model tension scores, Family Model Strategic Contradiction Index (FMSCI), family model pattern classification, and family model salience concentration index."
  }
}
```

</details>

---

## Conclusion

The Lakoff Framing Framework v4.2 represents a breakthrough in family model analysis by combining established moral framework assessment with pioneering family model tension pattern quantification. This enhancement enables systematic analysis of moral framework coherence - revealing whether speakers demonstrate consistent family model reasoning or exhibit measurable contradictions in their moral framework priorities.

**Key Innovation**: Lakoff v4.2 transforms family model analysis from measuring **which family model speakers prefer** to measuring **how coherently they apply family model reasoning**, providing unprecedented insight into moral framework authenticity and reasoning consistency.

**Research Foundation**: Built on validated tension mathematics from Issue #125, providing empirical foundation for cognitive linguistics research and moral framework assessment.

**Political Applications**: Enables systematic evaluation of moral framework coherence in political discourse, revealing authentic family model identity vs tactical moral positioning.

---

**Family Model Tension Discovery**:
- **Authority vs Empathy**: Leadership approach vs understanding emphasis tensions
- **Competition vs Cooperation**: Individual achievement vs collective responsibility balance  
- **Self-Reliance vs Interdependence**: Personal responsibility vs mutual dependence framework

**Research Applications Enabled**:
- Family model coherence studies across political contexts
- Cross-cultural moral framework tension pattern analysis  
- Cognitive consistency evaluation for political communication
- Moral framework authenticity vs tactical positioning research

**Bipolar Dimension Innovation**: 
First framework to apply tension mathematics to bipolar dimensions, measuring internal coherence tensions within single dimensions rather than between separate opposing dimensions.

---

**Version History**:
- **v4.1**: Salience-weighted family model analysis based on meta-analysis research
- **v4.2**: Added family model tension pattern analysis and Family Model Strategic Contradiction Index

**Next Enhancements**: Integration with other frameworks for cross-framework moral-political-family model correlation analysis.