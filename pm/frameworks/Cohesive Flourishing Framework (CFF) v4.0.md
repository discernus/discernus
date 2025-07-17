# --- Discernus Configuration ---
name: cff_v4_0
version: '4.0'
display_name: "Cohesive Flourishing Framework v4.0"

analysis_variants:
  
  default:
    description: "Complete independent anchor scoring across all five CFF axes"
    analysis_prompt: |
      You are an expert discourse analyst with deep expertise in political communication and social psychology. Your approach is grounded in empirical research on rhetorical patterns and social cohesion dynamics.
      
      Your task is to analyze the provided text using the Cohesive Flourishing Framework v4.0. This framework examines discourse through independent anchor scoring across five conceptual axes, capturing competitive rhetorical dynamics that traditional bipolar scoring obscures.
      
      The framework evaluates 10 conceptual anchors across 5 axes:
      
      Identity Axis:
      - Tribal Dominance: Group hierarchy language, exclusion markers, in-group supremacy, out-group derogation
      - Individual Dignity: Universal respect language, equality terms, rights emphasis, inclusive recognition
      
      Fear-Hope Axis:
      - Fear: Crisis language, threat perception, urgency markers, vulnerability terms
      - Hope: Opportunity language, progress emphasis, achievement focus, possibility markers
      
      Envy-Compersion Axis:
      - Envy: Elite resentment, success dismissal, zero-sum thinking, status grievance
      - Compersion: Success celebration, merit recognition, abundance mindset, admiration language
      
      Enmity-Amity Axis:
      - Enmity: Hostility language, aggressive terms, character assassination, dehumanization
      - Amity: Friendship language, affection terms, unity expressions, respect language
      
      Goal Axis:
      - Fragmentative Goals: Dominance seeking, authority emphasis, zero-sum competition, hierarchical power
      - Cohesive Goals: Service orientation, generosity language, unity building, empowerment focus
      
      For each anchor, follow this process:
      1. Read the text systematically for linguistic markers associated with that specific anchor
      2. Consider lexical evidence (direct word matches), semantic patterns (meaning structures), and rhetorical strategies
      3. Score the anchor independently from 0.0 to 1.0 based on strength, frequency, and strategic importance of evidence
      4. Assess your confidence in the scoring based on evidence clarity and quantity
      5. Aim to provide approximately 2 direct quotations supporting each anchor score
      
      Remember: Score each anchor independently. A text can score high on both Fear and Hope, or low on both, or any combination. The goal is to capture the complete rhetorical landscape without forcing artificial bipolar relationships.
      
      Return a single JSON object with:
      {
        "tribal_dominance_score": number,
        "tribal_dominance_confidence": number,
        "tribal_dominance_evidence": ["quote1", "quote2"],
        "individual_dignity_score": number,
        "individual_dignity_confidence": number,
        "individual_dignity_evidence": ["quote1", "quote2"],
        "fear_score": number,
        "fear_confidence": number,
        "fear_evidence": ["quote1", "quote2"],
        "hope_score": number,
        "hope_confidence": number,
        "hope_evidence": ["quote1", "quote2"],
        "envy_score": number,
        "envy_confidence": number,
        "envy_evidence": ["quote1", "quote2"],
        "compersion_score": number,
        "compersion_confidence": number,
        "compersion_evidence": ["quote1", "quote2"],
        "enmity_score": number,
        "enmity_confidence": number,
        "enmity_evidence": ["quote1", "quote2"],
        "amity_score": number,
        "amity_confidence": number,
        "amity_evidence": ["quote1", "quote2"],
        "fragmentative_goal_score": number,
        "fragmentative_goal_confidence": number,
        "fragmentative_goal_evidence": ["quote1", "quote2"],
        "cohesive_goal_score": number,
        "cohesive_goal_confidence": number,
        "cohesive_goal_evidence": ["quote1", "quote2"],
        "overall_analysis_confidence": number,
        "competitive_patterns_observed": "brief description of any notable competitive dynamics"
      }

calculation_spec:
  descriptive_cohesion_index: "(0.33 * (hope_score - fear_score)) + (0.27 * (compersion_score - envy_score)) + (0.40 * (amity_score - enmity_score))"
  motivational_cohesion_index: "(0.25 * (hope_score - fear_score)) + (0.20 * (compersion_score - envy_score)) + (0.30 * (amity_score - enmity_score)) + (0.25 * (cohesive_goal_score - fragmentative_goal_score))"
  full_cohesion_index: "(0.25 * (hope_score - fear_score)) + (0.20 * (compersion_score - envy_score)) + (0.30 * (amity_score - enmity_score)) + (0.25 * (cohesive_goal_score - fragmentative_goal_score))"

---

# Cohesive Flourishing Framework (CFF) v4.0
## Independent Anchor Scoring for Comprehensive Discourse Analysis

---

## Executive Summary

The Cohesive Flourishing Framework (CFF) v4.0 introduces **independent anchor scoring** to solve the fundamental information loss problem in discourse analysis. By scoring each conceptual pole separately (0.0 to 1.0) rather than forcing bipolar relationships, CFF v4.0 captures sophisticated rhetorical patterns including competitive tension, strategic balance, and dialectical complexity.

**Core Innovation**: Complete preservation of competitive dynamics through independent measurement, enabling detection of rhetorical sophistication that traditional scoring methods systematically obscure.

**Key Capabilities**:
- **Information Preservation**: No loss of competitive dynamics through forced averaging
- **Pattern Recognition**: Detection of pure directional, competitive tension, disengaged, and strategic balance patterns
- **Rich Evidence Base**: Two quotations per anchor with confidence ratings
- **Flexible Post-Processing**: Raw data supports multiple analytical approaches and normative layers
- **Scalable Collection**: Optimized for large-scale LLM analysis

---

## Part 1: Theoretical Foundation

### The Information Loss Problem

**Traditional Bipolar Scoring Limitation**:
- High Fear + High Hope = 0.0 (sophisticated tension management)
- No Fear + No Hope = 0.0 (emotional absence)  
- Moderate Fear + No Hope = -0.4 (pure negativity)

**CFF v4.0 Independent Anchor Solution**:
- High Fear (0.8) + High Hope (0.7) = Competitive Tension Pattern
- Low Fear (0.1) + Low Hope (0.1) = Disengaged Pattern
- Moderate Fear (0.4) + Low Hope (0.0) = Pure Directional Pattern

### Framework Architecture

**Five Conceptual Axes with Ten Independent Anchors**:

1. **Identity Axis**: Tribal Dominance ↔ Individual Dignity
2. **Fear-Hope Axis**: Fear ↔ Hope
3. **Envy-Compersion Axis**: Envy ↔ Compersion  
4. **Enmity-Amity Axis**: Enmity ↔ Amity
5. **Goal Axis**: Fragmentative Goals ↔ Cohesive Goals

**Post-Processing Flexibility**: Raw anchor data enables multiple analytical layers including descriptive emotional climate, motivational behavioral orientation, and comprehensive social health assessment.

---

## Part 2: Independent Anchor Methodology

### Anchor Scoring Protocol

**Scale Definition**: Each anchor scored independently from 0.0 to 1.0
- **0.0-0.2**: Minimal to no evidence
- **0.3-0.4**: Weak presence with limited evidence
- **0.5-0.6**: Moderate presence with clear evidence
- **0.7-0.8**: Strong presence with substantial evidence
- **0.9-1.0**: Dominant presence with overwhelming evidence

**Evidence Requirements**:
- **Goal**: Approximately 2 direct quotations per anchor
- **Flexibility**: Adjust based on text content and evidence availability
- **Quality Focus**: Strong evidence preferred over quotation quantity
- **Confidence Rating**: 0.0-1.0 based on evidence clarity and interpretive certainty

### Competitive Pattern Recognition

**Four Primary Patterns**:

**Pure Directional**: High score on one anchor, low on opposing anchor
- Indicates unified, confident strategic positioning
- Example: Hope=0.8, Fear=0.1

**Competitive Tension**: High scores on both opposing anchors
- Indicates sophisticated rhetorical management or audience segmentation
- Example: Hope=0.7, Fear=0.8

**Disengaged**: Low scores on both anchors
- Indicates minimal engagement with this conceptual axis
- Example: Hope=0.2, Fear=0.1

**Strategic Balance**: Moderate scores with clear directional preference
- Indicates measured positioning and strategic restraint
- Example: Hope=0.5, Fear=0.2

---

## Part 3: Linguistic Markers Reference

### Identity Axis

**Tribal Dominance Markers**:
- Group hierarchy: "better people," "superior values," "real Americans," "chosen people"
- Exclusion language: "not our kind," "doesn't belong," "them vs us," "foreign influence"  
- In-group supremacy: "natural rulers," "rightful place," "pure heritage," "true believers"
- Out-group derogation: dehumanizing terms, moral disqualification, capability denial

**Individual Dignity Markers**:
- Universal respect: "every person," "all humans," "inherent dignity," "common humanity"
- Equality language: "equal treatment," "same standards," "level playing field," "fair chance"
- Rights emphasis: "constitutional rights," "civil liberties," "individual freedoms," "personal autonomy"
- Inclusive recognition: "all of us," "every American," "each citizen," "everyone belongs"

### Fear-Hope Axis

**Fear Markers**:
- Crisis language: "emergency," "catastrophe," "disaster," "collapse," "breakdown"
- Threat perception: "under attack," "existential threat," "mortal danger," "life or death"
- Urgency markers: "running out of time," "last chance," "point of no return," "critical moment"
- Vulnerability terms: "defenseless," "exposed," "helpless," "at risk," "in jeopardy"

**Hope Markers**:
- Opportunity language: "bright future," "golden age," "breakthrough," "transformation"
- Progress emphasis: "moving forward," "advancement," "improvement," "development"
- Achievement focus: "success," "victory," "accomplishment," "milestone," "triumph"
- Possibility markers: "potential," "opportunity," "chance," "opening," "pathway"

### Envy-Compersion Axis

**Envy Markers**:
- Elite resentment: "privileged elite," "out of touch," "ivory tower," "rigged system"
- Success dismissal: "lucky breaks," "didn't earn it," "handed everything," "connections"
- Zero-sum thinking: "taking our share," "stealing from us," "unfair advantage," "hoarding wealth"
- Status grievance: "don't deserve credit," "overrated," "artificially promoted," "media darling"

**Compersion Markers**:
- Success celebration: "well-deserved," "hard-earned," "impressive accomplishment," "outstanding achievement"
- Merit recognition: "earned through effort," "demonstrated excellence," "proved themselves," "worked hard"
- Abundance mindset: "rising tide lifts all boats," "everyone can win," "plenty of opportunity," "shared success"
- Admiration language: "talented individual," "inspiring example," "role model," "lights the way"

### Enmity-Amity Axis

**Enmity Markers**:
- Hostility language: "enemy," "adversary," "threat," "menace," "danger," "foe"
- Aggressive terms: "attack," "destroy," "eliminate," "crush," "defeat," "annihilate"
- Character assassination: "evil," "corrupt," "criminal," "degenerate," "immoral," "perverted"
- Dehumanization: animal comparisons, object references, disease metaphors, vermin language

**Amity Markers**:
- Friendship language: "friend," "ally," "partner," "colleague," "teammate," "supporter"
- Affection terms: "love," "care," "cherish," "value," "appreciate," "treasure"
- Unity expressions: "together," "united," "connected," "joined," "linked," "unified"
- Respect language: "honor," "esteem," "dignity," "worth," "respect," "regard"

### Goal Axis

**Fragmentative Goal Markers**:
- Dominance seeking: "control," "dominate," "rule," "command," "master," "dictate"
- Authority emphasis: "obey," "submit," "comply," "bow down," "surrender," "yield"
- Zero-sum competition: "beat," "defeat," "outperform," "victory," "win," "triumph over"
- Hierarchical power: "superior," "above," "elite," "privileged," "special," "chosen"

**Cohesive Goal Markers**:
- Service orientation: "serve," "help," "assist," "support," "aid," "contribute"
- Generosity language: "give," "share," "donate," "contribute," "offer," "provide"
- Unity building: "bring together," "connect," "join," "include," "unite," "integrate"
- Empowerment focus: "empower," "enable," "strengthen," "uplift," "inspire," "elevate"

---

## Part 4: Quality Standards and Applications

### Quality Assurance

**Evidence Standards**:
- Direct quotations must clearly relate to specific anchor concepts
- Confidence ratings reflect evidence strength and interpretive certainty
- Overall analysis confidence represents systematic assessment quality

**Validation Approach**:
- Independent anchor scoring enables cross-validation through pattern consistency
- Rich evidence base supports inter-rater reliability testing
- Competitive pattern recognition provides analytical triangulation

### Research Applications

**Large-Scale Analysis**: Framework optimized for computational deployment across extensive text corpora
**Temporal Studies**: Independent anchor data enables sophisticated longitudinal analysis  
**Comparative Research**: Consistent methodology across contexts, cultures, and time periods
**Pattern Discovery**: Rich data supports machine learning and statistical pattern recognition

### Post-Processing Flexibility

**Normative Layering**: Apply different analytical depth based on research requirements
**Visualization Options**: Support multiple visualization approaches from simple charts to complex geometric analysis
**Statistical Analysis**: Raw anchor data enables advanced statistical modeling and correlation analysis
**Cohesion Measurement**: Multiple cohesion index formulations for different analytical purposes

---

## Conclusion

CFF v4.0 transforms discourse analysis from categorical assessment to nuanced pattern recognition through independent anchor scoring. By preserving complete competitive information, the framework enables detection of sophisticated rhetorical strategies while maintaining analytical rigor and computational scalability.

The framework serves as a comprehensive data collection engine, providing rich, structured datasets that support diverse analytical approaches and visualization strategies while avoiding the mathematical pitfalls that plague high-dimensional analysis systems.

**Key Innovation**: CFF v4.0 solves the fundamental information loss problem in discourse analysis, enabling researchers to capture and analyze the full complexity of rhetorical dynamics in democratic discourse.