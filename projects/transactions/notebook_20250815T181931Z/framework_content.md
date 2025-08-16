# Cohesive Flourishing Framework v8.0

## Research Purpose
Measure how political discourse impacts social cohesion through five dimensions of human social psychology.

## Analysis Requirements
- **Score Range**: All dimensions scored 0.0-1.0
- **Evidence Required**: Supporting textual quotes for each dimension score
- **Salience Weighting**: Score prominence based on textual frequency and emphasis
- **Confidence Assessment**: Analyst certainty for each dimensional score (0.0-1.0)

## Dimensions

### **Tribal Dominance** (0.0-1.0)
In-group supremacy and exclusionary identity patterns
- **Linguistic Markers**: "us vs them", "real Americans", "our people", exclusionary language
- **Evidence**: Direct quotes showing in-group preference or out-group rejection
- **Salience**: Weight by frequency and rhetorical emphasis

### **Individual Dignity** (0.0-1.0)
Universal human worth and inclusive recognition
- **Linguistic Markers**: "all people", "human dignity", "equal rights", inclusive language
- **Evidence**: Quotes affirming universal human worth
- **Salience**: Weight by centrality to argument

### **Fear** (0.0-1.0)
Crisis mentality and existential threat perception
- **Linguistic Markers**: "crisis", "threat", "danger", "destruction", catastrophic language
- **Evidence**: Statements framing situations as existential threats
- **Salience**: Weight by urgency and repetition

### **Hope** (0.0-1.0)
Progress orientation and optimistic collective vision
- **Linguistic Markers**: "future", "progress", "opportunity", "better tomorrow", aspirational language
- **Evidence**: Forward-looking positive statements
- **Salience**: Weight by vision prominence

### **Envy** (0.0-1.0)
Resentment toward others' success, zero-sum thinking
- **Linguistic Markers**: "unfair advantage", "rigged system", "they don't deserve", resentment language
- **Evidence**: Statements expressing resentment of others' success
- **Salience**: Weight by emotional intensity

### **Compersion** (0.0-1.0)
Celebration of others' success, abundance mindset
- **Linguistic Markers**: "celebrate success", "rising tide", "abundance", positive-sum language
- **Evidence**: Statements celebrating others' achievements
- **Salience**: Weight by genuine enthusiasm

### **Enmity** (0.0-1.0)
Hostility and adversarial positioning
- **Linguistic Markers**: "enemy", "fight", "battle", "defeat", combative language
- **Evidence**: Statements positioning others as adversaries
- **Salience**: Weight by hostility intensity

### **Amity** (0.0-1.0)
Friendship appeals and cooperative framing
- **Linguistic Markers**: "together", "unity", "cooperation", "partnership", collaborative language
- **Evidence**: Statements promoting cooperation
- **Salience**: Weight by collaboration emphasis

### **Fragmentative Goals** (0.0-1.0)
Divisive zero-sum objectives
- **Linguistic Markers**: "win/lose", "defeat them", "take back", zero-sum framing
- **Evidence**: Goals that require others to lose
- **Salience**: Weight by strategic prominence

### **Cohesive Goals** (0.0-1.0)
Integrative positive-sum objectives
- **Linguistic Markers**: "win-win", "mutual benefit", "shared prosperity", positive-sum framing
- **Evidence**: Goals that benefit multiple groups
- **Salience**: Weight by inclusivity scope

## Calculations

### **Derived Metrics**
- **Identity Tension**: `tribal_dominance_score - individual_dignity_score`
  - Measures conflict between exclusionary and inclusive identity framing
  - Range: -1.0 (dignity dominant) to +1.0 (tribal dominant)

- **Emotional Balance**: `hope_score - fear_score` 
  - Measures optimistic vs pessimistic emotional climate
  - Range: -1.0 (fear dominant) to +1.0 (hope dominant)

- **Success Climate**: `compersion_score - envy_score`
  - Measures abundance vs scarcity mindset toward others' success
  - Range: -1.0 (envy dominant) to +1.0 (compersion dominant)

- **Relational Climate**: `amity_score - enmity_score`
  - Measures cooperative vs adversarial positioning
  - Range: -1.0 (enmity dominant) to +1.0 (amity dominant)

- **Goal Orientation**: `cohesive_goals_score - fragmentative_goals_score`
  - Measures integrative vs divisive objective framing
  - Range: -1.0 (fragmentative dominant) to +1.0 (cohesive dominant)

### **Composite Indices**
- **Overall Cohesion Index**: `(individual_dignity + hope + compersion + amity + cohesive_goals) / 5 - (tribal_dominance + fear + envy + enmity + fragmentative_goals) / 5`
  - Comprehensive measure of discourse cohesiveness
  - Range: -1.0 (maximally fragmentative) to +1.0 (maximally cohesive)

## Analysis Methodology

**Sequential Chain-of-Thought Analysis**: Examine each dimension group independently before integration to improve analytical consistency and evidence quality.

### **Step-by-Step Process**
1. **Identity Axis**: Focus ONLY on tribal dominance vs. individual dignity patterns
2. **Emotional Climate**: Focus ONLY on fear vs. hope patterns  
3. **Success Orientation**: Focus ONLY on envy vs. compersion patterns
4. **Relational Climate**: Focus ONLY on enmity vs. amity patterns
5. **Goal Orientation**: Focus ONLY on fragmentative vs. cohesive goals patterns
6. **Integration**: Calculate derived metrics and assess strategic patterns

### **For Each Step**
- **Score** the dimension (0.0-1.0) with specific textual evidence
- **Assess salience** (0.0-1.0): How central is this appeal to the overall discourse?
- **State confidence** (0.0-1.0): How certain are you of this assessment?
- **Show your work**: Explain reasoning and provide supporting quotes

## Advanced Metrics

### **Tension Mathematics**
**Tension Score Formula**: `min(Dimension_A_score, Dimension_B_score) × |Salience_A - Salience_B|`

- **Identity Tension**: `min(tribal_dominance_score, individual_dignity_score) × |tribal_dominance_salience - individual_dignity_salience|`
- **Emotional Tension**: `min(fear_score, hope_score) × |fear_salience - hope_salience|`
- **Success Tension**: `min(envy_score, compersion_score) × |envy_salience - compersion_salience|`
- **Relational Tension**: `min(enmity_score, amity_score) × |enmity_salience - amity_salience|`
- **Goal Tension**: `min(fragmentative_goals_score, cohesive_goals_score) × |fragmentative_goals_salience - cohesive_goals_salience|`

### **Strategic Indices**
- **Strategic Contradiction Index**: `(identity_tension + emotional_tension + success_tension + relational_tension + goal_tension) / 5`
- **Salience-Weighted Cohesive Index**: `(individual_dignity_score × individual_dignity_salience + hope_score × hope_salience + compersion_score × compersion_salience + amity_score × amity_salience + cohesive_goals_score × cohesive_goals_salience) / (individual_dignity_salience + hope_salience + compersion_salience + amity_salience + cohesive_goals_salience)`
- **Salience-Weighted Fragmentative Index**: `(tribal_dominance_score × tribal_dominance_salience + fear_score × fear_salience + envy_score × envy_salience + enmity_score × enmity_salience + fragmentative_goals_score × fragmentative_goals_salience) / (tribal_dominance_salience + fear_salience + envy_salience + enmity_salience + fragmentative_goals_salience)`

## Expected Output Structure
```yaml
analysis_metadata:
  framework_name: cohesive_flourishing_framework
  framework_version: v8.0
  analyst_confidence: 0.95
  analysis_notes: "Sequential chain-of-thought analysis with salience weighting"

document_analyses:
  - document_id: "unique_identifier"
    document_name: "filename.txt"
    dimensional_scores:
      tribal_dominance_score:
        raw_score: 0.8
        salience: 0.9
        confidence: 0.85
      individual_dignity_score:
        raw_score: 0.6
        salience: 0.7
        confidence: 0.80
      fear_score:
        raw_score: 0.3
        salience: 0.4
        confidence: 0.90
      hope_score:
        raw_score: 0.7
        salience: 0.8
        confidence: 0.85
      envy_score:
        raw_score: 0.2
        salience: 0.3
        confidence: 0.75
      compersion_score:
        raw_score: 0.6
        salience: 0.5
        confidence: 0.70
      enmity_score:
        raw_score: 0.4
        salience: 0.6
        confidence: 0.80
      amity_score:
        raw_score: 0.7
        salience: 0.8
        confidence: 0.85
      fragmentative_goals_score:
        raw_score: 0.3
        salience: 0.4
        confidence: 0.75
      cohesive_goals_score:
        raw_score: 0.8
        salience: 0.9
        confidence: 0.90
    evidence:
      - dimension: "tribal_dominance_score"
        quote_text: "We must put our people first, ahead of all others"
        confidence: 0.85
        context_type: "direct_statement"
      - dimension: "individual_dignity_score"
        quote_text: "Every person deserves respect regardless of background"
        confidence: 0.80
        context_type: "direct_statement"
      - dimension: "hope_score"
        quote_text: "Together we can build a better future for all"
        confidence: 0.85
        context_type: "aspirational_statement"
```
