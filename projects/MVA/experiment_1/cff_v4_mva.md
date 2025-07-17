---
# --- Discernus Configuration ---
name: CFF_MVA_Test
version: '4.0'
display_name: "Cohesive Flourishing Framework (MVA Test)"

analysis_variants:
  fully_normative:
    description: "Scores all five axes of the CFF and classifies the text's political worldview. This is the fully normative analysis."
    analysis_prompt: |
      You are an expert political discourse analyst executing a multi-part analysis using the Cohesive Flourishing Framework (CFF) v3.1.
      
      Your task is to analyze the provided text according to this framework's rigorous methodology, which requires comprehensive evidence documentation for all analytical conclusions.
      
      TEXT TO ANALYZE:
      {corpus_text}
      
      SOURCE FILE: {file_name}
      
      Step 1: Classify the political worldview of the text.
      Determine whether this text primarily expresses a "Progressive", "Conservative", "Libertarian", or "Other" worldview based on the rhetorical patterns, policy positions, and value frameworks expressed.
      
      Step 2: Score the text on all five CFF axes.
      Analyze the text carefully for each dimension using the framework's linguistic markers and theoretical foundations. For each axis, provide a score from -1.0 to +1.0:
      - identity_axis: Individual Dignity (+1.0) ↔ Tribal Dominance (-1.0)
      - fear_hope_axis: Optimistic Possibility (+1.0) ↔ Threat Perception (-1.0)
      - envy_compersion_axis: Others' Success Celebration (+1.0) ↔ Elite Resentment (-1.0)
      - enmity_amity_axis: Social Goodwill (+1.0) ↔ Interpersonal Hostility (-1.0)
      - goal_axis: Cohesive Generosity (+1.0) ↔ Fragmentative Power (-1.0)
      
      Step 3: Provide comprehensive evidence documentation.
      For each axis score, you must provide:
      - At least 3 direct quotations from the text that support your assessment
      - Confidence rating (0.0-1.0) based on evidence strength and clarity
      - Evidence type classification for each quote (lexical/semantic/rhetorical)
      - Brief reasoning explaining how the evidence supports the score
      
      Step 4: Format the output as a single JSON object.
      Return a JSON object with these top-level keys:
      - "worldview": String classification from Step 1
      - "scores": Dictionary with all five axis scores
      - "evidence": Dictionary with axis names as keys and arrays of direct quotations as values
      - "confidence": Dictionary with axis names as keys and confidence ratings as values
      - "evidence_types": Dictionary with axis names as keys and arrays of evidence type classifications as values
      - "reasoning": Dictionary with axis names as keys and explanatory text as values
      
      The output MUST be a valid JSON object that implements the framework's evidence requirements.

  motivational:
    description: "Scores the four core cohesion axes plus the Goal axis, assessing behavioral orientation."
    analysis_prompt: |
      You are an expert researcher applying the Cohesive Flourishing Framework (CFF) v3.1 with focus on motivational and behavioral dimensions.
      
      Your task is to analyze the provided text for the four core cohesion axes that drive social behavior, omitting the Identity axis for this simplified analysis.
      
      TEXT TO ANALYZE:
      {corpus_text}
      
      SOURCE FILE: {file_name}
      
      Analyze the text carefully for each dimension using the framework's linguistic markers. For each axis, provide a score from -1.0 to +1.0:
      - fear_hope_axis: Optimistic Possibility (+1.0) ↔ Threat Perception (-1.0)
      - envy_compersion_axis: Others' Success Celebration (+1.0) ↔ Elite Resentment (-1.0)
      - enmity_amity_axis: Social Goodwill (+1.0) ↔ Interpersonal Hostility (-1.0)
      - goal_axis: Cohesive Generosity (+1.0) ↔ Fragmentative Power (-1.0)
      
      For each axis score, you must provide:
      - At least 3 direct quotations from the text that support your assessment
      - Confidence rating (0.0-1.0) based on evidence strength
      - Brief reasoning connecting evidence to score
      
      Return a JSON object with:
      - "scores": Dictionary with the four axis scores
      - "evidence": Dictionary with axis names as keys and arrays of direct quotations as values
      - "confidence": Dictionary with axis names as keys and confidence ratings as values
      - "reasoning": Dictionary with axis names as keys and explanatory text as values
      
      The output MUST be a valid JSON object that maintains the framework's evidence standards.

  descriptive:
    description: "Scores only the three core emotional axes for a neutral emotional climate mapping."
    analysis_prompt: |
      You are an expert researcher applying the Cohesive Flourishing Framework (CFF) v3.1 for descriptive emotional climate analysis.
      
      Your task is to analyze the provided text for the three core emotional dimensions that characterize social climate, omitting the Identity and Goal axes for this neutral descriptive analysis.
      
      TEXT TO ANALYZE:
      {corpus_text}
      
      SOURCE FILE: {file_name}
      
      Analyze the text carefully for each emotional dimension using the framework's linguistic markers. For each axis, provide a score from -1.0 to +1.0:
      - fear_hope_axis: Optimistic Possibility (+1.0) ↔ Threat Perception (-1.0)
      - envy_compersion_axis: Others' Success Celebration (+1.0) ↔ Elite Resentment (-1.0)
      - enmity_amity_axis: Social Goodwill (+1.0) ↔ Interpersonal Hostility (-1.0)
      
      For each axis score, you must provide:
      - At least 3 direct quotations from the text that support your assessment
      - Confidence rating (0.0-1.0) based on evidence strength
      - Brief reasoning connecting evidence to score
      
      Return a JSON object with:
      - "scores": Dictionary with the three axis scores
      - "evidence": Dictionary with axis names as keys and arrays of direct quotations as values
      - "confidence": Dictionary with axis names as keys and confidence ratings as values
      - "reasoning": Dictionary with axis names as keys and explanatory text as values
      
      The output MUST be a valid JSON object that maintains the framework's evidence standards.

calculation_spec:
  - metric:
      name: "cff_cohesion_index"
      formula: "(0.25 * scores.fear_hope_axis) + (0.20 * scores.envy_compersion_axis) + (0.30 * scores.enmity_amity_axis) + (0.25 * scores.goal_axis)"
---
# Cohesive Flourishing Framework (CFF) v3.1
## Advanced Hybrid Instruction Package with Integrated Cohesion Index
### For Discernus Research Agents

---

## Executive Summary

The Cohesive Flourishing Framework (CFF) v3.1 is an advanced multidimensional analysis framework designed for computational rhetoric analysis within the Discernus CARA (Conversational Academic Research Architecture) platform. Version 3.1 includes enhanced linguistic markers for improved computational detection precision.

**Core Innovation**: Five orthogonal axes enabling **graduated normative layering** with **integrated composite measurement** through the CFF Cohesion Index. This architecture provides analytical flexibility, allowing researchers to choose their level of normative engagement while generating actionable social cohesion metrics for comparative and temporal analysis.

**Key Capabilities**: 
- **Descriptive Layer**: Neutral emotional climate mapping with simplified cohesion measurement
- **Motivational Layer**: Behavioral orientation analysis with intermediate cohesion assessment
- **Fully Normative Layer**: Explicit moral evaluation with comprehensive Cohesion Index
- **Temporal Intelligence**: Systematic tracking of social cohesion evolution over time
- **Comparative Analysis**: Standardized measurement enabling cross-context assessment

**Version 3.1 Enhancement**: Enhanced linguistic markers with significantly expanded detection precision across all axes for improved computational operationalization.

---

## Part 1: Theoretical Foundation

### CFF's Dual Innovation Architecture

CFF v3.1 combines two complementary innovations that together revolutionize computational social science:

#### Innovation 1: Graduated Normative Layering
The systematic ability to scale analysis depth from neutral description to explicit moral evaluation. This architecture enables researchers to choose their level of normative engagement while maintaining methodological transparency.

#### Innovation 2: Integrated Cohesion Index  
A validated composite metric that synthesizes multidimensional analysis into actionable social cohesion measurement. The index enables temporal tracking, comparative analysis, and predictive assessment while preserving analytical sophistication.

**Theoretical Synthesis**: CFF v3.1 solves the fundamental tension between analytical objectivity and normative insight while providing practical measurement capabilities essential for democratic institutions and social research.

### Framework Architecture: Five Axes with Composite Measurement

**CFF analyzes discourse along five orthogonal dimensions while generating integrated cohesion metrics:**

1. **Identity Axis**: Individual Dignity ↔ Tribal Dominance (Foundation for Layer 3)
2. **Fear-Hope Axis**: Threat Perception ↔ Optimistic Possibility (Core Cohesion Component)
3. **Envy-Compersion Axis**: Elite Resentment ↔ Others' Success Celebration (Core Cohesion Component)
4. **Enmity-Amity Axis**: Interpersonal Hostility ↔ Social Goodwill (Core Cohesion Component)
5. **Goal Axis**: Fragmentative Power ↔ Cohesive Generosity (Core Cohesion Component)

**Measurement Integration**: The four core cohesion axes (Fear-Hope, Envy-Compersion, Enmity-Amity, Goal) are systematically combined using validated weights to generate the CFF Cohesion Index alongside traditional axis scores.

---

## Part 2: The CFF Cohesion Index - Integrated Core Component

### Mathematical Specification

```
CFF_Cohesion_Index = w₁(Hope - Fear) + w₂(Compersion - Envy) + w₃(Amity - Enmity) + w₄(Cohesive_Goal - Fragmentative_Goal)
```

**Empirically Validated Weights**:
- **w₁ (Hope-Fear): 0.25** - Temporal orientation toward collective future
- **w₂ (Compersion-Envy): 0.20** - Social comparison and economic dynamics  
- **w₃ (Amity-Enmity): 0.30** - Interpersonal relations (highest weight - fundamental social bonds)
- **w₄ (Goal Orientation): 0.25** - Collective objectives toward unity or division

### Interpretive Scale (-1.0 to +1.0)

**+0.7 to +1.0: High Cohesion**
- Characteristics: Sustained hope, celebrated success, interpersonal goodwill, unity goals
- Social Implications: Strong solidarity potential, robust democratic discourse

**+0.3 to +0.7: Moderate Cohesion**  
- Characteristics: Cautious optimism, conditional cooperation, manageable divisions
- Social Implications: Stable social bonds with some tensions

**-0.3 to +0.3: Neutral/Contested**
- Characteristics: Emotional volatility, strategic positioning, uncertain direction  
- Social Implications: Outcomes depend on external factors and leadership

**-0.7 to -0.3: Moderate Fragmentation**
- Characteristics: Sustained pessimism, competitive resentment, group tensions
- Social Implications: Risk of social division and conflict escalation

**-1.0 to -0.7: High Fragmentation Risk**
- Characteristics: Catastrophic thinking, elite hatred, interpersonal hostility
- Social Implications: Significant potential for social breakdown

---

## Part 3: Analysis Protocol

### Scoring Methodology

**Scale Definition**: Each axis uses a bipolar scale from -1.0 to +1.0
- **-1.0**: Maximum presence of negative pole (Fear, Envy, Enmity, etc.)
- **0.0**: Neutral or balanced presence of both poles
- **+1.0**: Maximum presence of positive pole (Hope, Compersion, Amity, etc.)

**Evidence Requirements**: 
- Minimum 3 pieces of textual evidence per score
- Evidence must include direct quotations from source text
- Evidence types: lexical, semantic, rhetorical patterns
- Confidence assessment required for each score

**Scoring Process**:
1. **Text Reading**: Complete reading for overall themes
2. **Evidence Collection**: Systematic gathering of linguistic markers
3. **Axis Scoring**: Independent scoring of each dimension
4. **Cohesion Calculation**: Mathematical integration using validated weights
5. **Confidence Assessment**: Evaluation of evidence strength and certainty

---

## Part 4: Linguistic Markers and Evidence Types

### Identity Axis: Individual Dignity ↔ Tribal Dominance

**Individual Dignity Markers**:
- Universal respect language: "every person," "all humans," "inherent dignity"
- Equality terms: "equal treatment," "same standards," "level playing field"
- Inclusive pronouns: "all of us," "every American," "each citizen"
- Rights language: "constitutional rights," "civil liberties," "individual freedoms"

**Tribal Dominance Markers**:
- Group hierarchy terms: "better people," "superior values," "real Americans"
- Exclusion language: "not our kind," "doesn't belong," "them vs us"
- In-group supremacy: "chosen people," "natural rulers," "superior civilization"
- Out-group derogation: dehumanizing terms, moral disqualification

### Fear-Hope Axis: Threat Perception ↔ Optimistic Possibility

**Fear Markers**:
- Crisis terms: "emergency," "catastrophe," "disaster," "collapse"
- Danger language: "under attack," "existential threat," "mortal danger"
- Urgency markers: "running out of time," "last chance," "point of no return"
- Vulnerability terms: "defenseless," "exposed," "helpless," "at risk"

**Hope Markers**:
- Opportunity terms: "bright future," "golden age," "breakthrough"
- Progress language: "moving forward," "advancement," "improvement"
- Achievement terms: "success," "victory," "accomplishment," "milestone"
- Possibility markers: "potential," "opportunity," "chance," "opening"

### Envy-Compersion Axis: Elite Resentment ↔ Others' Success Celebration

**Envy Markers**:
- Elite resentment: "privileged elite," "out of touch," "rigged system"
- Success dismissal: "lucky breaks," "didn't earn it," "handed everything"
- Zero-sum thinking: "taking our share," "stealing from us," "unfair advantage"
- Status resentment: "don't deserve credit," "overrated," "artificially promoted"

**Compersion Markers**:
- Success celebration: "well-deserved," "hard-earned," "impressive accomplishment"
- Merit acknowledgment: "earned through effort," "demonstrated excellence"
- Abundance mindset: "rising tide lifts all boats," "everyone can win"
- Admiration language: "talented individual," "inspiring example," "role model"

### Enmity-Amity Axis: Interpersonal Hostility ↔ Social Goodwill

**Enmity Markers**:
- Hostility terms: "enemy," "adversary," "threat," "menace"
- Aggressive language: "attack," "destroy," "eliminate," "crush"
- Character assassination: "evil," "corrupt," "criminal," "degenerate"
- Dehumanization: animal comparisons, object references, disease metaphors

**Amity Markers**:
- Friendship terms: "friend," "ally," "partner," "colleague"
- Affection language: "love," "care," "cherish," "value"
- Unity expressions: "together," "united," "connected," "joined"
- Respect language: "honor," "esteem," "dignity," "worth"

### Goal Axis: Fragmentative Power ↔ Cohesive Generosity

**Fragmentative Power Markers**:
- Dominance terms: "control," "dominate," "rule," "command"
- Authority language: "obey," "submit," "comply," "bow down"
- Zero-sum competition: "beat," "defeat," "outperform," "victory"
- Hierarchical power: "superior," "above," "elite," "privileged"

**Cohesive Generosity Markers**:
- Service terms: "serve," "help," "assist," "support"
- Generosity language: "give," "share," "donate," "contribute"
- Unity building: "bring together," "connect," "join," "include"
- Empowerment terms: "empower," "enable," "strengthen," "uplift"

---

## Part 5: Output Requirements

### Quantitative Components
- **Axis Scores**: Five numerical scores (-1.0 to +1.0) for each dimension
- **Cohesion Index**: Single composite score (-1.0 to +1.0) representing overall cohesion
- **Confidence Ratings**: Certainty assessment for each score (0.0 to 1.0)
- **Evidence Count**: Number of supporting textual examples per axis

### Qualitative Components
- **Evidence Citations**: Direct quotations supporting each axis score
- **Interpretive Analysis**: Explanation of scoring rationale and patterns
- **Contextual Notes**: Relevant background affecting interpretation
- **Uncertainty Documentation**: Areas of ambiguity or competing interpretations

### Synthesis Requirements
- **Pattern Identification**: Key rhetorical strategies and themes
- **Temporal Comparison**: Changes over time if applicable
- **Cohesion Assessment**: Social implications of measured dimensions
- **Strategic Intelligence**: Actionable insights for stakeholders

---

## Part 6: Quality Control and Validation

### Confidence Calibration
- **High Confidence (0.8-1.0)**: Clear, unambiguous evidence with multiple supporting examples
- **Medium Confidence (0.5-0.7)**: Moderate evidence with some interpretive judgment required
- **Low Confidence (0.0-0.4)**: Weak or ambiguous evidence requiring additional analysis

### Evidence Standards
- **Lexical Evidence**: Direct word and phrase matches with framework markers
- **Semantic Evidence**: Meaning-based patterns requiring interpretive analysis
- **Rhetorical Evidence**: Structural and stylistic elements supporting dimensional assessment
- **Contextual Evidence**: Background factors affecting interpretation and scoring

### Validation Protocols
- **Inter-rater Reliability**: Multiple analysts should achieve >80% agreement on major patterns
- **Evidence Documentation**: All scores must be traceable to specific textual evidence
- **Methodological Transparency**: Complete documentation of scoring decisions and rationale
- **Replication Standards**: Analysis should be reproducible by other researchers using same framework

---

## Conclusion

CFF v3.1 provides a comprehensive, validated framework for analyzing discourse along multiple dimensions of social cohesion. The framework's dual innovation of graduated normative layering and integrated cohesion measurement enables both descriptive analysis and normative assessment while maintaining methodological rigor.

**Key Strengths**:
1. **Theoretical Grounding**: Based on established social psychology research
2. **Empirical Validation**: Weights derived from large-scale political rhetoric analysis
3. **Analytical Flexibility**: Multiple layers of analysis depth
4. **Practical Application**: Actionable insights for democratic institutions
5. **Computational Optimization**: Enhanced linguistic markers for LLM analysis

The framework serves as a powerful tool for understanding how political discourse affects social cohesion, providing both academic insights and practical intelligence for maintaining democratic stability. 