# Cohesive Flourishing Framework (CFF) v10.4

---

## Part 1: The Scholarly Document

### Section 1: Abstract & *Raison d'Être*

**What is this framework?**
The Cohesive Flourishing Framework (CFF) is a systematic measurement methodology for quantifying rhetorical dimensions in political and social discourse. It provides computational social science researchers with empirical data about textual patterns that theoretical frameworks associate with democratic discourse quality.

**What problem does it solve?**
CFF addresses a critical gap in discourse analysis by providing a methodology that preserves complex rhetorical information. Traditional analysis often forces artificial choices (e.g., a text is "hopeful" or "fearful"), losing nuance when sophisticated communication employs competing appeals simultaneously. CFF's independent scoring of opposing dimensions (e.g., Hope vs. Fear) captures this complexity, generating reliable, replicable measurements of competing rhetorical appeals while preserving textual complexity through independent dimensional scoring and salience weighting.

**What it enables:**
These measurements may provide empirical data for investigating **potential** relationships between discourse patterns and democratic outcomes, political polarization, or rhetorical strategy, **pending validation studies and theoretical specification**. Researchers integrate CFF data with contextual knowledge, explicit theoretical frameworks, and additional sources to construct analytical arguments.

**What it doesn't do:**
The framework measures observable textual features but does not interpret their political significance, determine speaker intent, or evaluate democratic health. Such interpretations require human expertise and domain-specific theoretical knowledge.

**Who is it for?**
This framework is designed for computational social science researchers, political communication scholars, and policy researchers who need reliable empirical measurements of rhetorical patterns. It serves as methodological infrastructure for studies of political discourse, democratic health assessment, and rhetorical strategy analysis.

### Section 2: Theoretical & Empirical Foundations

**Theoretical Framework**: This framework operates within the deliberative democracy tradition (Gutmann & Thompson, 1996; Habermas, 1996), which emphasizes discourse quality as foundational to democratic legitimacy. **Alternative theoretical approaches** (competitive democratic theory, agonistic pluralism, populist democracy) would interpret these same measurements differently. Researchers should specify their theoretical framework when interpreting results.

**Cultural Validity Limitations**: This framework was developed for analysis of Western democratic discourse and may not generalize to other political systems or cultural contexts. What constitutes "healthy" political discourse varies significantly across:
- Parliamentary vs. presidential systems
- Consensus-oriented vs. majoritarian democracies  
- High-context vs. low-context communication cultures
- Collectivist vs. individualist value systems

The CFF is grounded in a multi-disciplinary body of research from social psychology, political communication, and conflict resolution theory. Its core innovation—the independent scoring of opposing conceptual anchors—is a direct response to the information loss problem observed in traditional valence-based content analysis.

#### **Social Identity Theory Foundation**

The framework's identity dimensions (Tribal Dominance vs. Individual Dignity) are grounded in Social Identity Theory (Tajfel & Turner, 1979), which demonstrates how group membership affects intergroup behavior and attitudes. Research shows that in-group favoritism and out-group derogation are fundamental processes in social categorization (Brewer, 1999). The framework's approach to measuring group supremacy rhetoric builds on work by Sidanius & Pratto (1999) on Social Dominance Theory, which explains how societies maintain group-based hierarchies.

**Key Citations**:
- Tajfel, H., & Turner, J. C. (1979). An integrative theory of intergroup conflict. In W. G. Austin & S. Worchel (Eds.), *The social psychology of intergroup relations* (pp. 33-47). Brooks/Cole.
- Brewer, M. B. (1999). The psychology of prejudice: Ingroup love and outgroup hate? *Journal of Social Issues*, 55(3), 429-444.
- Sidanius, J., & Pratto, F. (1999). *Social dominance: An intergroup theory of social hierarchy and oppression*. Cambridge University Press.

#### **Political Communication Research**

The framework's approach to emotional climate analysis (Fear vs. Hope) draws from extensive research on emotional appeals in political discourse. Brader (2006) demonstrated that emotional appeals significantly influence political behavior and decision-making. The framework's emphasis on preserving complex emotional information addresses limitations identified by Marcus et al. (2000) in their Affective Intelligence Theory.

The relational dimensions (Enmity vs. Amity) are informed by research on political polarization and democratic discourse. Jamieson & Cappella (2008) showed how media discourse patterns can increase political polarization, while Gutmann & Thompson (1996) outlined conditions for constructive democratic deliberation.

**Key Citations**:
- Brader, T. (2006). *Campaigning for hearts and minds: How emotional appeals in political ads work*. University of Chicago Press.
- Marcus, G. E., Neuman, W. R., & MacKuen, M. (2000). *Affective intelligence and political judgment*. University of Chicago Press.
- Jamieson, K. H., & Cappella, J. N. (2008). *Echo chamber: Rush Limbaugh and the conservative media establishment*. Oxford University Press.
- Gutmann, A., & Thompson, D. (1996). *Democracy and disagreement*. Harvard University Press.

#### **Discourse Analysis Methodology**

The framework's independent scoring approach addresses the "information loss problem" identified in traditional valence-based content analysis. Krippendorff (2004) emphasized the importance of preserving analytical complexity rather than forcing artificial binary classifications. The salience-weighting methodology builds on work by van Dijk (2008) on critical discourse analysis, which emphasizes the importance of rhetorical emphasis and structural positioning in meaning construction.

**Key Citations**:
- Krippendorff, K. (2004). *Content analysis: An introduction to its methodology* (2nd ed.). Sage Publications.
- van Dijk, T. A. (2008). *Discourse and power*. Palgrave Macmillan.

#### **Empirical Justification for Salience Weighting**

The use of salience-weighting is empirically grounded in research demonstrating that static, predetermined weights for analytical dimensions lack empirical support. Studies in computational linguistics (Pang & Lee, 2008) and political communication (Laver et al., 2003) have shown that context-dependent weighting based on textual emphasis patterns provides more accurate and reliable results than fixed weighting schemes.

**Key Citations**:
- Pang, B., & Lee, L. (2008). Opinion mining and sentiment analysis. *Foundations and Trends in Information Retrieval*, 2(1-2), 1-135.
- Laver, M., Benoit, K., & Garry, J. (2003). Extracting policy positions from political texts using words as data. *American Political Science Review*, 97(2), 311-331.

#### **Democratic Health and Social Cohesion**

The framework's focus on democratic health builds on Putnam's (2000) work on social capital and civic engagement, which demonstrated the relationship between discourse patterns and community cohesion. The normative layers approach draws from deliberative democracy theory (Habermas, 1996), which provides criteria for evaluating the quality of democratic discourse.

**Key Citations**:
- Putnam, R. D. (2000). *Bowling alone: The collapse and revival of American community*. Simon & Schuster.
- Habermas, J. (1996). *Between facts and norms: Contributions to a discourse theory of law and democracy*. MIT Press.

### Section 3: Measurement Methodology

CFF employs a multi-layered measurement approach that generates empirical data with transparent normative layering for researcher interpretation.

**Dimensions**: The framework scores ten conceptual anchors independently on a 0.0 to 1.0 scale, organized into five opposing pairs:

**Identity Axis**: 
-   **Tribal Dominance** (0.0-1.0): In-group supremacy, exclusionary identity patterns, "us versus them" rhetoric
-   **Individual Dignity** (0.0-1.0): Universal human worth, inclusive recognition, equal treatment emphasis

**Emotional Climate**:
-   **Fear** (0.0-1.0): Crisis mentality, existential threat perception, vulnerability emphasis
-   **Hope** (0.0-1.0): Progress orientation, optimistic collective vision, opportunity language

**Success Orientation**:
-   **Envy** (0.0-1.0): Resentment toward others' success, zero-sum thinking, grievance rhetoric
-   **Mudita** (0.0-1.0): Joy from others' success, abundance mindset, merit celebration

**Relational Climate**:
-   **Enmity** (0.0-1.0): Hostility, adversarial positioning, conflict emphasis
-   **Amity** (0.0-1.0): Friendship appeals, cooperative framing, unity language

**Goal Orientation**:
-   **Fragmentative Goals** (0.0-1.0): Divisive zero-sum objectives, separation emphasis
-   **Cohesive Goals** (0.0-1.0): Integrative positive-sum objectives, building emphasis

**Advanced Concepts**:
-   **Salience vs. Intensity**: A critical distinction is made between a dimension's *intensity* (its raw 0.0-1.0 score) and its *salience* (its rhetorical prominence or emphasis within the text, also scored 0.0-1.0). This dual-track analysis reveals not just *what* is being said, but *how much emphasis* it receives.
-   **Rhetorical Tension**: The framework calculates the strategic tension between opposing pairs to measure the coherence of the discourse. The formula `Tension = min(Score_A, Score_B) × |Salience_A - Salience_B|` quantifies contradictions where a speaker employs competing appeals.

**Three Measurement Layers with Normative Transparency**:

| Layer | Type | Focus | Key Questions | Normative Load | Applications |
|-------|------|-------|---------------|----------------|--------------|
| **1 - Empirical Measurement** | **Descriptive** | Rhetorical patterns | What rhetorical patterns are present? How prominent are they? | **None** - Pure pattern recognition | Academic research, content analysis, baseline measurement |
| **2 - Behavioral Prediction** | **Analytical** | Audience responses | What audience responses might these patterns elicit? | **Minimal** - Based on communication research | Strategic communication, audience analysis, campaign evaluation |
| **3 - Democratic Health Evaluation** | **Normative** | Democratic impact | How do these patterns relate to democratic discourse ideals? | **High** - Requires explicit theoretical framework | Policy evaluation, intervention design, community health monitoring |

Each layer builds on the previous one, providing increasingly contextualized empirical measurements while maintaining transparency about normative assumptions. This transparency enables researchers to select appropriate measurement depth for their analytical purposes while maintaining methodological rigor.

**Derived & Composite Metrics**:

**Tension Indices** (0.0-1.0, higher = more contradiction):
-   **Identity Tension**: Measures contradiction between tribal dominance and individual dignity appeals
  - **Formula**: `min(tribal_dominance_score, individual_dignity_score) × |tribal_dominance_salience - individual_dignity_salience|`
-   **Emotional Tension**: Measures contradiction between fear and hope messaging
  - **Formula**: `min(fear_score, hope_score) × |fear_salience - hope_salience|`
-   **Success Tension**: Measures contradiction between envy and mudita rhetoric
  - **Formula**: `min(envy_score, mudita_score) × |envy_salience - mudita_salience|`
-   **Relational Tension**: Measures contradiction between enmity and amity positioning
  - **Formula**: `min(enmity_score, amity_score) × |enmity_salience - amity_salience|`
-   **Goal Tension**: Measures contradiction between fragmentative and cohesive objectives
  - **Formula**: `min(fragmentative_goals_score, cohesive_goals_score) × |fragmentative_goals_salience - cohesive_goals_salience|`

**Strategic Contradiction Index** (0.0-1.0, higher = more incoherent):
-   **Average of all tension indices** measuring overall rhetorical coherence
-   **Formula**: `(identity_tension + emotional_tension + success_tension + relational_tension + goal_tension) / 5`
-   **Low values** indicate consistent, coherent messaging
-   **High values** indicate strategic contradictions and mixed appeals

**Salience-Weighted Cohesion Indices** (-1.0 to +1.0, negative = fragmentative, positive = cohesive):

**Descriptive Cohesion Index**: Measures immediate emotional and relational climate using salience weighting. **Positive values** indicate hope, mudita, and amity emphasis; **negative values** indicate fear, envy, and enmity emphasis.

**Formula**: `(hope_score × hope_salience - fear_score × fear_salience) + (mudita_score × mudita_salience - envy_score × envy_salience) + (amity_score × amity_salience - enmity_score × enmity_salience)` divided by the sum of all salience weights for these dimensions plus epsilon (0.001) to prevent division by zero.

**Motivational Cohesion Index**: Assesses likely behavioral consequences with salience-adjusted emphasis. **Positive values** suggest cooperative, abundance-oriented behaviors; **negative values** suggest competitive, zero-sum behaviors.

**Formula**: `(hope_score × hope_salience - fear_score × fear_salience) + (mudita_score × mudita_salience - envy_score × envy_salience) + (amity_score × amity_salience - enmity_score × enmity_salience) + (cohesive_goals_score × cohesive_goals_salience - fragmentative_goals_score × fragmentative_goals_salience)` divided by the sum of all salience weights for these dimensions plus epsilon (0.001) to prevent division by zero.

**Full Cohesion Index**: Comprehensive evaluation of democratic health and social cohesion. **Positive values** indicate discourse supporting democratic institutions and social solidarity; **negative values** indicate discourse undermining democratic health and promoting fragmentation.

**Formula**: `(individual_dignity_score × individual_dignity_salience - tribal_dominance_score × tribal_dominance_salience) + (hope_score × hope_salience - fear_score × fear_salience) + (mudita_score × mudita_salience - envy_score × envy_salience) + (amity_score × amity_salience - enmity_score × enmity_salience) + (cohesive_goals_score × cohesive_goals_salience - fragmentative_goals_score × fragmentative_goals_salience)` divided by the sum of all salience weights for these dimensions plus epsilon (0.001) to prevent division by zero.

**Calculation Method**: All indices use salience-weighted calculations where each dimension's score is multiplied by its rhetorical prominence (salience), ensuring that what speakers actually emphasize receives appropriate influence on the final measurement. The normalization by total salience weights ensures indices remain within the -1.0 to +1.0 range while reflecting the relative emphasis patterns in the discourse.

### Section 3.5: Alternative Interpretive Frameworks

**Measurement-Interpretation Distinction**: The CFF generates empirical measurements that can be interpreted through multiple theoretical lenses. Researchers should explicitly specify their interpretive framework:

**Democratic Health Framework** (Deliberative Democracy Tradition):
- **Theory Base**: Habermas (1996), Gutmann & Thompson (1996)
- **Positive Indicators**: Individual dignity, hope, amity, cohesive goals
- **Concerns**: Tribal dominance, fear, enmity, fragmentative goals
- **Application**: Evaluating discourse quality for democratic legitimacy

**Competitive Politics Framework** (Competitive Democratic Theory):
- **Theory Base**: Schumpeter (1942), Przeworski (1999)
- **Interpretation**: Strong position-taking and differentiation may indicate healthy democratic competition
- **Concerns**: Low energy or unclear choices may suggest weak democratic contestation
- **Application**: Assessing electoral and policy competition dynamics

**Social Movement Framework** (Social Movement Theory):
- **Theory Base**: McAdam, Tarrow & Tilly (2001)
- **Interpretation**: Boundary-setting and grievance articulation may be necessary for social change
- **Concerns**: Excessive accommodation may perpetuate systemic injustices
- **Application**: Analyzing advocacy strategies and institutional change efforts

**Agonistic Democracy Framework** (Agonistic Pluralism):
- **Theory Base**: Mouffe (2000), Connolly (1991)  
- **Interpretation**: Productive conflict and passion may be essential to democratic vitality
- **Concerns**: Excessive consensus may mask power relations and suppress legitimate dissent
- **Application**: Evaluating democratic authenticity and institutional responsiveness

**Research Application Guidance**: This framework functions as a measurement tool for generating testable hypotheses about discourse-democracy relationships. It does not:
- Definitively establish causal relationships
- Provide universal standards for discourse evaluation  
- Replace domain expertise in political communication
- Account for context-specific factors affecting interpretation

### Section 4: Intended Application & Corpus Fit

-   **Target Corpus Description**: CFF is designed for the analysis of persuasive or strategic communication, particularly in the political and social spheres. This includes political speeches, campaign materials, policy documents, and organizational communications.
-   **Known Limitations & Scope**: The framework is less suited for analyzing purely informational, conversational, or fictional texts. The complexity of the salience and tension assessments requires a text with sufficient length and rhetorical structure to be meaningful.
-   **Model Requirements**: This framework requires a highly capable LLM model (e.g., Gemini 2.5 Pro, Claude 3 Opus, GPT-4) for reliable analysis. The sophisticated dual-track analysis (intensity + salience), complex concept distinctions, and mathematical framework exceed the capabilities of basic or lightweight models.
-   **System Validation Note**: Be aware that the Discernus platform will perform a post-hoc statistical analysis of your framework's fit with your chosen corpus based on the variance in the results. A low framework-corpus fit score may indicate that the framework was misapplied and could impact the interpretation of the results.

---

## Part 2: The Machine-Readable Appendix

```yaml
# --- Start of Machine-Readable Appendix ---

# 5.1: Metadata
metadata:
  framework_name: "cohesive_flourishing_framework"
  framework_version: "10.4.0"
  author: "Discernus Project"
  spec_version: "10.0"

# 5.2: Analysis Variants
analysis_variants:
  default:
    description: "Complete v10.4 implementation with salience and tension analysis."
    analysis_prompt: |
      You are an expert discourse analyst specializing in social cohesion and democratic health, grounded in political psychology and social identity theory. Your task is to generate empirical measurements of the provided text using the Cohesive Flourishing Framework v10.4.

      FRAMEWORK METHODOLOGY:
      This framework generates empirical measurements of rhetorical dimensions in discourse through independent scoring of opposing conceptual anchors. It preserves complex rhetorical information by avoiding forced binary choices, providing reliable quantitative data about strategic communication that employs competing appeals simultaneously.

      DIMENSIONAL ANALYSIS:
      You must evaluate 10 dimensions across 5 opposing pairs:
      - Identity: Tribal Dominance vs. Individual Dignity
      - Emotional Climate: Fear vs. Hope  
      - Success Orientation: Envy vs. Mudita
      - Relational Climate: Enmity vs. Amity
      - Goal Orientation: Fragmentative Goals vs. Cohesive Goals

      IMPORTANT DISTINCTIONS:
      - "Mudita" measures joy from others' success (distinct from "compassion" which is empathy for suffering)
      - "Individual Dignity" focuses on universal human worth (not personal achievement or individual rights)
      - "Tribal Dominance" measures group supremacy rhetoric (not just group loyalty or identity)
      - Use exact dimension names as specified - do not substitute similar concepts

      EVIDENCE STANDARDS:
      - Provide exact quotations, not paraphrases
      - Include context for ambiguous references
      - If evidence is unclear or ambiguous, lower confidence score accordingly
      - Prioritize direct rhetorical indicators over interpretive inferences

      MEASUREMENT APPROACH:
      - Score each dimension independently based on textual evidence
      - Assess both intensity (how strong) and salience (how prominent/emphasized)  
      - Recognize that opposing dimensions can both be present simultaneously
      - Focus on observable rhetorical patterns rather than interpretive inferences

      CONTEXTUAL GUIDANCE:
      - In political speeches, emphasize rhetorical strategies and audience appeals
      - Look for structural positioning (opening/closing statements carry higher salience)
      - Consider repetition patterns as indicators of rhetorical emphasis
      - Distinguish between policy content and rhetorical strategy

      SALIENCE ASSESSMENT: 
      Salience measures rhetorical prominence, not intensity. Consider:
      - Frequency and repetition patterns throughout the text
      - Structural positioning (opening, closing, thesis statements)
      - Thematic centrality to the overall message
      - Rhetorical devices used for emphasis (metaphors, imagery, emotional appeals)
      SALIENCE ≠ INTENSITY. A dimension can have moderate intensity (0.5) but high salience (0.9) if it's rhetorically central.

      MANDATORY OUTPUT REQUIREMENTS:
      You must provide both dimensional_scores AND derived_metrics in your response. The derived_metrics are calculated automatically based on your dimensional scores, but you must include both sections in your JSON output.

  # Sequential analysis variants for improved accuracy (recommended approach)
  sequential_identity:
    description: "Focus on Identity axis: Tribal Dominance vs Individual Dignity."
    analysis_prompt: |
      You are an expert political discourse analyst specializing in social identity and group dynamics. Focus exclusively on measuring the Identity axis in the provided text using the Cohesive Flourishing Framework v10.4.

      DIMENSIONAL FOCUS: Identity Axis Only
      - Tribal Dominance: In-group supremacy, exclusionary identity patterns
      - Individual Dignity: Universal human worth, inclusive recognition

      IDENTITY-SPECIFIC GUIDANCE:
      - Look for language that creates in-group/out-group distinctions
      - Assess whether group identity includes or excludes others
      - Distinguish between group pride and group supremacy
      - Focus on universality vs. selectivity in human worth language

      CRITICAL DISTINCTIONS:
      - "Tribal Dominance" measures group supremacy rhetoric (not just group loyalty)
      - "Individual Dignity" focuses on universal human worth (not individual rights or achievement)

      Provide raw_score, salience, evidence, and confidence for BOTH dimensions.

  sequential_emotional:
    description: "Focus on Emotional Climate: Fear vs Hope."
    analysis_prompt: |
      You are an expert political discourse analyst specializing in emotional appeals and crisis rhetoric. Focus exclusively on measuring the Emotional Climate in the provided text using the Cohesive Flourishing Framework v10.4.

      DIMENSIONAL FOCUS: Emotional Climate Only
      - Fear: Crisis mentality, existential threat perception
      - Hope: Progress orientation, optimistic collective vision

      EMOTIONAL-SPECIFIC GUIDANCE:
      - Look for temporal framing (crisis vs. opportunity)
      - Assess urgency levels and threat perception
      - Distinguish between concern and existential fear
      - Focus on future orientation (threatening vs. promising)

      CRITICAL DISTINCTIONS:
      - "Fear" requires crisis/threat language, not just concern or caution
      - "Hope" requires progress/opportunity language, not just positive sentiment

      Provide raw_score, salience, evidence, and confidence for BOTH dimensions.

  sequential_success:
    description: "Focus on Success Orientation: Envy vs Mudita."
    analysis_prompt: |
      You are an expert political discourse analyst specializing in economic rhetoric and success framing. Focus exclusively on measuring Success Orientation in the provided text using the Cohesive Flourishing Framework v10.4.

      DIMENSIONAL FOCUS: Success Orientation Only
      - Envy: Resentment toward others' success, zero-sum thinking
      - Mudita: Joy from others' success, abundance mindset

      SUCCESS-SPECIFIC GUIDANCE:
      - Look for attitudes toward others' achievements and prosperity
      - Assess zero-sum vs. abundance thinking patterns
      - Distinguish between policy critique and personal resentment
      - Focus on emotional responses to others' success

      CRITICAL DISTINCTIONS:
      - "Envy" requires resentment and zero-sum thinking, not just inequality concern
      - "Mudita" measures joy for others' success (distinct from compassion for suffering)

      Provide raw_score, salience, evidence, and confidence for BOTH dimensions.

  sequential_relational:
    description: "Focus on Relational Climate: Enmity vs Amity."
    analysis_prompt: |
      You are an expert political discourse analyst specializing in interpersonal and intergroup relations. Focus exclusively on measuring Relational Climate in the provided text using the Cohesive Flourishing Framework v10.4.

      DIMENSIONAL FOCUS: Relational Climate Only
      - Enmity: Hostility and adversarial positioning
      - Amity: Friendship appeals and cooperative framing

      RELATIONAL-SPECIFIC GUIDANCE:
      - Look for relationship characterizations and interpersonal framing
      - Assess cooperative vs. adversarial positioning
      - Distinguish between disagreement and hostility
      - Focus on relationship quality rather than policy positions

      CRITICAL DISTINCTIONS:
      - "Enmity" requires hostility and adversarial language, not just opposition
      - "Amity" requires friendship/cooperation language, not just absence of conflict

      Provide raw_score, salience, evidence, and confidence for BOTH dimensions.

  sequential_goals:
    description: "Focus on Goal Orientation: Fragmentative vs Cohesive Goals."
    analysis_prompt: |
      You are an expert political discourse analyst specializing in strategic objectives and collective action. Focus exclusively on measuring Goal Orientation in the provided text using the Cohesive Flourishing Framework v10.4.

      DIMENSIONAL FOCUS: Goal Orientation Only
      - Fragmentative Goals: Divisive zero-sum objectives
      - Cohesive Goals: Integrative positive-sum objectives

      GOAL-SPECIFIC GUIDANCE:
      - Look for stated or implied objectives and strategic aims
      - Assess whether goals build unity or create division
      - Distinguish between competitive and destructive objectives
      - Focus on collective outcomes rather than individual benefits

      CRITICAL DISTINCTIONS:
      - "Fragmentative Goals" require division/separation objectives, not just competition
      - "Cohesive Goals" require integration/unity building, not just cooperation

      Provide raw_score, salience, evidence, and confidence for BOTH dimensions.

# 5.3: Dimensions
dimensions:
  - name: "tribal_dominance"
    description: "In-group supremacy and exclusionary identity patterns."
    markers:
      positive_examples:
        - phrase: "real Americans"
          explanation: "emphasizes authentic group membership vs. outsiders"
        - phrase: "our people"
          explanation: "creates in-group/out-group distinction"
        - phrase: "superior values"
          explanation: "claims group moral or cultural superiority"
        - phrase: "not our kind"
          explanation: "explicit exclusion of others"
        - phrase: "chosen people"
          explanation: "special status claims for the group"
      negative_examples:
        - phrase: "patriotic"
          explanation: "love of country without exclusion doesn't qualify"
        - phrase: "community pride"
          explanation: "positive group identity without supremacy claims"
      boundary_cases:
        - phrase: "we are different"
          explanation: "depends on context; supremacy claims vs. simple distinction"
    scoring_calibration:
      high: "0.7-1.0: Explicit supremacy claims, strong us-vs-them rhetoric, exclusionary language"
      medium: "0.4-0.6: Moderate in-group preference, subtle exclusion, implied superiority"
      low: "0.1-0.3: Mild group preference, weak exclusionary hints"
      absent: "0.0: No group supremacy, exclusion, or superiority claims"
    disambiguation:
      overlap_with_individual_dignity: "Both dimensions can be present simultaneously; score each independently based on textual evidence"

  - name: "individual_dignity"
    description: "Universal human worth and inclusive recognition."
    markers:
      positive_examples:
        - phrase: "every person"
          explanation: "universal scope of human worth"
        - phrase: "inherent dignity"
          explanation: "intrinsic value regardless of group membership"
        - phrase: "common humanity"
          explanation: "shared human experience transcending divisions"
        - phrase: "equal treatment"
          explanation: "procedural fairness across groups"
        - phrase: "everyone belongs"
          explanation: "inclusive community vision"
      negative_examples:
        - phrase: "individual rights"
          explanation: "legal/political concept, not dignity focus"
        - phrase: "personal achievement"
          explanation: "individual success, not universal worth"
      boundary_cases:
        - phrase: "respect for persons"
          explanation: "depends on universality vs. selective respect"
    scoring_calibration:
      high: "0.7-1.0: Strong universal worth language, explicit inclusion, dignity emphasis"
      medium: "0.4-0.6: Moderate inclusivity, some universal recognition"
      low: "0.1-0.3: Weak inclusive hints, minimal dignity language"
      absent: "0.0: No universal worth, inclusion, or dignity themes"

  - name: "fear"
    description: "Crisis mentality and existential threat perception."
    markers:
      positive_examples:
        - phrase: "existential threat"
          explanation: "survival-level danger"
        - phrase: "catastrophe"
          explanation: "disaster language and crisis framing"
        - phrase: "under attack"
          explanation: "active threat perception"
        - phrase: "running out of time"
          explanation: "urgency and deadline pressure"
        - phrase: "emergency"
          explanation: "crisis requiring immediate action"
      negative_examples:
        - phrase: "challenge"
          explanation: "difficulty without crisis implication"
        - phrase: "concern"
          explanation: "worry without existential threat"
      boundary_cases:
        - phrase: "serious problem"
          explanation: "depends on urgency and threat level"
    scoring_calibration:
      high: "0.7-1.0: Existential crisis, survival threats, imminent catastrophe"
      medium: "0.4-0.6: Serious concerns, significant risks, urgent problems"
      low: "0.1-0.3: Minor worries, potential problems, mild anxiety"
      absent: "0.0: No threat language, crisis indicators, or fear appeals"

  - name: "hope"
    description: "Progress orientation and optimistic collective vision."
    markers:
      positive_examples:
        - phrase: "bright future"
          explanation: "optimistic forward vision"
        - phrase: "breakthrough"
          explanation: "significant positive progress"
        - phrase: "moving forward"
          explanation: "progress and advancement"
        - phrase: "opportunity"
          explanation: "positive potential and possibility"
        - phrase: "success"
          explanation: "achievement and accomplishment focus"
      negative_examples:
        - phrase: "stability"
          explanation: "maintaining status quo, not progress"
        - phrase: "recovery"
          explanation: "returning to previous state, not advancement"
      boundary_cases:
        - phrase: "better days ahead"
          explanation: "depends on progress vs. simple improvement"
    scoring_calibration:
      high: "0.7-1.0: Strong optimism, clear progress vision, breakthrough language"
      medium: "0.4-0.6: Moderate optimism, some progress indicators"
      low: "0.1-0.3: Mild optimism, weak progress hints"
      absent: "0.0: No optimism, progress language, or positive vision"

  - name: "envy"
    description: "Resentment toward others' success, zero-sum thinking."
    markers:
      positive_examples:
        - phrase: "privileged elite"
          explanation: "resentment toward successful groups"
        - phrase: "didn't earn it"
          explanation: "questioning legitimacy of others' success"
        - phrase: "rigged system"
          explanation: "systemic unfairness claims"
        - phrase: "taking our share"
          explanation: "zero-sum resource thinking"
        - phrase: "unfair advantage"
          explanation: "resentment over others' benefits"
      negative_examples:
        - phrase: "inequality"
          explanation: "factual disparity without resentment"
        - phrase: "fairness"
          explanation: "justice concern without envy"
      boundary_cases:
        - phrase: "they have too much"
          explanation: "depends on resentment vs. policy concern"
    scoring_calibration:
      high: "0.7-1.0: Strong resentment, clear zero-sum thinking, success delegitimization"
      medium: "0.4-0.6: Moderate resentment, some zero-sum indicators"
      low: "0.1-0.3: Mild resentment hints, weak zero-sum thinking"
      absent: "0.0: No resentment, zero-sum thinking, or success delegitimization"

  - name: "mudita"
    description: "Joy from others' success, abundance mindset, merit celebration."
    markers:
      positive_examples:
        - phrase: "well-deserved"
          explanation: "affirming legitimacy of others' success"
        - phrase: "hard-earned"
          explanation: "recognizing merit in others' achievements"
        - phrase: "celebrate success"
          explanation: "positive response to others' accomplishments"
        - phrase: "rising tide lifts all boats"
          explanation: "abundance mindset, non-zero-sum"
        - phrase: "impressive accomplishment"
          explanation: "admiration for others' achievements"
      negative_examples:
        - phrase: "compassion"
          explanation: "empathy for suffering, not joy for success"
        - phrase: "tolerance"
          explanation: "acceptance without celebration"
      boundary_cases:
        - phrase: "good for them"
          explanation: "depends on genuine joy vs. dismissive tone"
    scoring_calibration:
      high: "0.7-1.0: Clear joy for others' success, strong abundance mindset"
      medium: "0.4-0.6: Moderate appreciation, some merit recognition"
      low: "0.1-0.3: Weak appreciation hints, minimal success celebration"
      absent: "0.0: No joy for others' success, merit recognition, or abundance thinking"
    disambiguation:
      vs_compassion: "Mudita = joy for success; Compassion = empathy for suffering"

  - name: "enmity"
    description: "Language that frames relationships in terms of hostility, adversarial conflict, or dehumanization. Focuses on identifying and attacking an enemy."
    markers:
      positive_examples:
        - phrase: "enemy"
          explanation: "explicit adversarial designation"
        - phrase: "destroy"
          explanation: "aggressive action language against a group"
        - phrase: "evil"
          explanation: "moral condemnation and dehumanization"
        - phrase: "they are a threat"
          explanation: "casting a group as an existential danger"
        - phrase: "traitors"
          explanation: "character assassination and accusation of betrayal"
      negative_examples:
        - phrase: "disagree with their policies"
          explanation: "opposition to ideas, not people"
        - phrase: "we must correct this injustice"
          explanation: "criticism of a system, not a hostile attack on a group"
      boundary_cases:
        - phrase: "fight against injustice"
          explanation: "Scores low unless the 'fight' is framed as hostility toward a specific group of people."
    scoring_calibration:
      high: "0.7-1.0: Clear hostility, enemy designation, dehumanizing language"
      medium: "0.4-0.6: Moderate adversarial positioning, some hostile language, blame attribution"
      low: "0.1-0.3: Mild adversarial hints, criticism of groups without overt hostility"
      absent: "0.0: No hostility, enemy language, or adversarial positioning toward people"
    disambiguation:
      vs_amity: "A text can have high Enmity (criticizing an opponent) AND high Amity (calling for future brotherhood). Score each independently. Enmity applies to the description of the present conflict."
      enmity_vs_criticism: "Enmity requires hostility toward PEOPLE or GROUPS. Strong criticism of IDEAS, SYSTEMS, or ACTIONS without personal hostility should not score high on Enmity."

  - name: "amity"
    description: "Language that frames relationships in terms of friendship, cooperation, shared identity, and potential for reconciliation. Focuses on building or affirming positive social bonds."
    markers:
      positive_examples:
        - phrase: "my friends"
          explanation: "explicit positive relationship designation"
        - phrase: "our shared future"
          explanation: "emphasizes a common in-group or goal"
        - phrase: "work together"
          explanation: "explicit call for cooperation"
        - phrase: "brotherhood"
          explanation: "appeal to familial, non-transactional bonds"
        - phrase: "let us sit down together"
          explanation: "call for dialogue and reconciliation"
      negative_examples:
        - phrase: "a necessary evil"
          explanation: "reluctant acceptance, not positive relationship"
        - phrase: "our opponents"
          explanation: "acknowledges disagreement without implying a positive bond"
      boundary_cases:
        - phrase: "our fellow citizens"
          explanation: "Can be a simple statement of fact, or a genuine appeal to shared identity. Score based on warmth and context."
    scoring_calibration:
      high: "0.7-1.0: Strong appeals to friendship, brotherhood, reconciliation, and shared identity."
      medium: "0.4-0.6: Moderate calls for cooperation, dialogue, or finding common ground."
      low: "0.1-0.3: Weak hints of potential cooperation or shared identity."
      absent: "0.0: No language of friendship, cooperation, or reconciliation."
    disambiguation:
      vs_enmity: "A text can describe a present state of Enmity while calling for a future state of Amity. Score both based on the evidence. Amity often relates to the speaker's proposed solution or ideal future."

  - name: "fragmentative_goals"
    description: "Divisive zero-sum objectives."
    markers:
      positive_examples:
        - phrase: "divide and conquer"
          explanation: "explicit fragmentation strategy"
        - phrase: "tear down"
          explanation: "destruction of existing structures"
        - phrase: "separate"
          explanation: "division and isolation emphasis"
        - phrase: "break apart"
          explanation: "fragmentation of unity"
        - phrase: "defeat them"
          explanation: "zero-sum victory objectives"
      negative_examples:
        - phrase: "reform"
          explanation: "change without destruction"
        - phrase: "replace"
          explanation: "substitution without fragmentation"
      boundary_cases:
        - phrase: "restructure"
          explanation: "depends on destruction vs. reorganization"
    scoring_calibration:
      high: "0.7-1.0: Clear fragmentation objectives, strong divisive language"
      medium: "0.4-0.6: Moderate division emphasis, some zero-sum objectives"
      low: "0.1-0.3: Weak divisive hints, minimal fragmentation"
      absent: "0.0: No fragmentation, division, or zero-sum objectives"

  - name: "cohesive_goals"
    description: "Integrative positive-sum objectives."
    markers:
      positive_examples:
        - phrase: "bring together"
          explanation: "explicit unification objectives"
        - phrase: "unite"
          explanation: "solidarity and integration emphasis"
        - phrase: "build bridges"
          explanation: "connection and relationship building"
        - phrase: "strengthen bonds"
          explanation: "relationship enhancement"
        - phrase: "common ground"
          explanation: "shared foundation emphasis"
      negative_examples:
        - phrase: "maintain"
          explanation: "preservation without building"
        - phrase: "manage"
          explanation: "administration without integration"
      boundary_cases:
        - phrase: "work together"
          explanation: "depends on integration vs. temporary cooperation"
    scoring_calibration:
      high: "0.7-1.0: Strong integration objectives, clear unity building"
      medium: "0.4-0.6: Moderate unification, some building language"
      low: "0.1-0.3: Weak integration hints, minimal unity emphasis"
      absent: "0.0: No integration, unity building, or positive-sum objectives"

# 5.4: Required Calculations
# All implementations MUST calculate these derived metrics
required_calculations:
  # Step 1: Calculate tension indices (measure rhetorical contradictions)
  tension_indices:
    identity_tension:
      description: "Measures contradiction between tribal dominance and individual dignity appeals"
      calculation_steps:
        1: "Take minimum of tribal_dominance.raw_score and individual_dignity.raw_score"
        2: "Calculate absolute difference between tribal_dominance.salience and individual_dignity.salience"
        3: "Multiply step 1 result by step 2 result"
      formula: "min(tribal_dominance.raw_score, individual_dignity.raw_score) * abs(tribal_dominance.salience - individual_dignity.salience)"
      inputs: ["tribal_dominance.raw_score", "tribal_dominance.salience", "individual_dignity.raw_score", "individual_dignity.salience"]
      output_range: [0.0, 1.0]
      output_type: "float"

    emotional_tension:
      description: "Measures contradiction between fear and hope messaging"
      calculation_steps:
        1: "Take minimum of fear.raw_score and hope.raw_score"
        2: "Calculate absolute difference between fear.salience and hope.salience"
        3: "Multiply step 1 result by step 2 result"
      formula: "min(fear.raw_score, hope.raw_score) * abs(fear.salience - hope.salience)"
      inputs: ["fear.raw_score", "fear.salience", "hope.raw_score", "hope.salience"]
      output_range: [0.0, 1.0]
      output_type: "float"

    success_tension:
      description: "Measures contradiction between envy and mudita rhetoric"
      calculation_steps:
        1: "Take minimum of envy.raw_score and mudita.raw_score"
        2: "Calculate absolute difference between envy.salience and mudita.salience"
        3: "Multiply step 1 result by step 2 result"
      formula: "min(envy.raw_score, mudita.raw_score) * abs(envy.salience - mudita.salience)"
      inputs: ["envy.raw_score", "envy.salience", "mudita.raw_score", "mudita.salience"]
      output_range: [0.0, 1.0]
      output_type: "float"

    relational_tension:
      description: "Measures contradiction between enmity and amity positioning"
      calculation_steps:
        1: "Take minimum of enmity.raw_score and amity.raw_score"
        2: "Calculate absolute difference between enmity.salience and amity.salience"
        3: "Multiply step 1 result by step 2 result"
      formula: "min(enmity.raw_score, amity.raw_score) * abs(enmity.salience - amity.salience)"
      inputs: ["enmity.raw_score", "enmity.salience", "amity.raw_score", "amity.salience"]
      output_range: [0.0, 1.0]
      output_type: "float"

    goal_tension:
      description: "Measures contradiction between fragmentative and cohesive objectives"
      calculation_steps:
        1: "Take minimum of fragmentative_goals.raw_score and cohesive_goals.raw_score"
        2: "Calculate absolute difference between fragmentative_goals.salience and cohesive_goals.salience"
        3: "Multiply step 1 result by step 2 result"
      formula: "min(fragmentative_goals.raw_score, cohesive_goals.raw_score) * abs(fragmentative_goals.salience - cohesive_goals.salience)"
      inputs: ["fragmentative_goals.raw_score", "fragmentative_goals.salience", "cohesive_goals.raw_score", "cohesive_goals.salience"]
      output_range: [0.0, 1.0]
      output_type: "float"

  # Step 2: Calculate strategic contradiction index
  strategic_coherence:
    strategic_contradiction_index:
      description: "Average of all tension indices measuring overall rhetorical coherence"
      calculation_steps:
        1: "Sum identity_tension + emotional_tension + success_tension + relational_tension + goal_tension"
        2: "Divide sum by 5"
      formula: "(identity_tension + emotional_tension + success_tension + relational_tension + goal_tension) / 5"
      inputs: ["identity_tension", "emotional_tension", "success_tension", "relational_tension", "goal_tension"]
      output_range: [0.0, 1.0]
      output_type: "float"
      interpretation:
        low_values: "0.0-0.3: Consistent, coherent messaging"
        medium_values: "0.3-0.6: Moderate contradictions"
        high_values: "0.6-1.0: Strategic contradictions and mixed appeals"

  # Step 3: Calculate cohesion components (intermediate calculations)
  cohesion_components:
    emotional_cohesion_component:
      description: "Emotional climate contribution to cohesion"
      calculation_steps:
        1: "Multiply hope.raw_score by hope.salience"
        2: "Multiply fear.raw_score by fear.salience"
        3: "Subtract step 2 result from step 1 result"
      formula: "(hope.raw_score * hope.salience) - (fear.raw_score * fear.salience)"
      inputs: ["hope.raw_score", "hope.salience", "fear.raw_score", "fear.salience"]
      output_type: "float"

    success_cohesion_component:
      description: "Success orientation contribution to cohesion"
      calculation_steps:
        1: "Multiply mudita.raw_score by mudita.salience"
        2: "Multiply envy.raw_score by envy.salience"
        3: "Subtract step 2 result from step 1 result"
      formula: "(mudita.raw_score * mudita.salience) - (envy.raw_score * envy.salience)"
      inputs: ["mudita.raw_score", "mudita.salience", "envy.raw_score", "envy.salience"]
      output_type: "float"

    relational_cohesion_component:
      description: "Relational climate contribution to cohesion"
      calculation_steps:
        1: "Multiply amity.raw_score by amity.salience"
        2: "Multiply enmity.raw_score by enmity.salience"
        3: "Subtract step 2 result from step 1 result"
      formula: "(amity.raw_score * amity.salience) - (enmity.raw_score * enmity.salience)"
      inputs: ["amity.raw_score", "amity.salience", "enmity.raw_score", "enmity.salience"]
      output_type: "float"

    goal_cohesion_component:
      description: "Goal orientation contribution to cohesion"
      calculation_steps:
        1: "Multiply cohesive_goals.raw_score by cohesive_goals.salience"
        2: "Multiply fragmentative_goals.raw_score by fragmentative_goals.salience"
        3: "Subtract step 2 result from step 1 result"
      formula: "(cohesive_goals.raw_score * cohesive_goals.salience) - (fragmentative_goals.raw_score * fragmentative_goals.salience)"
      inputs: ["cohesive_goals.raw_score", "cohesive_goals.salience", "fragmentative_goals.raw_score", "fragmentative_goals.salience"]
      output_type: "float"

    identity_cohesion_component:
      description: "Identity axis contribution to cohesion"
      calculation_steps:
        1: "Multiply individual_dignity.raw_score by individual_dignity.salience"
        2: "Multiply tribal_dominance.raw_score by tribal_dominance.salience"
        3: "Subtract step 2 result from step 1 result"
      formula: "(individual_dignity.raw_score * individual_dignity.salience) - (tribal_dominance.raw_score * tribal_dominance.salience)"
      inputs: ["individual_dignity.raw_score", "individual_dignity.salience", "tribal_dominance.raw_score", "tribal_dominance.salience"]
      output_type: "float"

  # Step 4: Calculate salience totals (for normalization)
  salience_totals:
    descriptive_salience_total:
      description: "Sum of salience weights for descriptive cohesion index"
      calculation_steps:
        1: "Sum hope.salience + fear.salience + mudita.salience + envy.salience + amity.salience + enmity.salience"
      formula: "hope.salience + fear.salience + mudita.salience + envy.salience + amity.salience + enmity.salience"
      inputs: ["hope.salience", "fear.salience", "mudita.salience", "envy.salience", "amity.salience", "enmity.salience"]
      output_type: "float"

    motivational_salience_total:
      description: "Sum of salience weights for motivational cohesion index"
      calculation_steps:
        1: "Use descriptive_salience_total"
        2: "Add cohesive_goals.salience + fragmentative_goals.salience"
      formula: "descriptive_salience_total + cohesive_goals.salience + fragmentative_goals.salience"
      inputs: ["descriptive_salience_total", "cohesive_goals.salience", "fragmentative_goals.salience"]
      output_type: "float"

    full_salience_total:
      description: "Sum of salience weights for full cohesion index"
      calculation_steps:
        1: "Use motivational_salience_total"
        2: "Add individual_dignity.salience + tribal_dominance.salience"
      formula: "motivational_salience_total + individual_dignity.salience + tribal_dominance.salience"
      inputs: ["motivational_salience_total", "individual_dignity.salience", "tribal_dominance.salience"]
      output_type: "float"

  # Step 5: Calculate final cohesion indices
  final_indices:
    descriptive_cohesion_index:
      description: "Measures immediate emotional and relational climate using salience weighting"
      calculation_steps:
        1: "Sum emotional_cohesion_component + success_cohesion_component + relational_cohesion_component"
        2: "Add 0.001 to descriptive_salience_total to prevent division by zero"
        3: "Divide step 1 result by step 2 result"
      formula: "(emotional_cohesion_component + success_cohesion_component + relational_cohesion_component) / (descriptive_salience_total + 0.001)"
      inputs: ["emotional_cohesion_component", "success_cohesion_component", "relational_cohesion_component", "descriptive_salience_total"]
      output_range: [-1.0, 1.0]
      output_type: "float"
      interpretation:
        positive_values: "Hope, mudita, and amity emphasis"
        negative_values: "Fear, envy, and enmity emphasis"

    motivational_cohesion_index:
      description: "Assesses likely behavioral consequences with salience-adjusted emphasis"
      calculation_steps:
        1: "Sum emotional_cohesion_component + success_cohesion_component + relational_cohesion_component + goal_cohesion_component"
        2: "Add 0.001 to motivational_salience_total to prevent division by zero"
        3: "Divide step 1 result by step 2 result"
      formula: "(emotional_cohesion_component + success_cohesion_component + relational_cohesion_component + goal_cohesion_component) / (motivational_salience_total + 0.001)"
      inputs: ["emotional_cohesion_component", "success_cohesion_component", "relational_cohesion_component", "goal_cohesion_component", "motivational_salience_total"]
      output_range: [-1.0, 1.0]
      output_type: "float"
      interpretation:
        positive_values: "Cooperative, abundance-oriented behaviors likely"
        negative_values: "Competitive, zero-sum behaviors likely"

    full_cohesion_index:
      description: "Comprehensive evaluation of democratic health and social cohesion"
      calculation_steps:
        1: "Sum identity_cohesion_component + emotional_cohesion_component + success_cohesion_component + relational_cohesion_component + goal_cohesion_component"
        2: "Add 0.001 to full_salience_total to prevent division by zero"
        3: "Divide step 1 result by step 2 result"
      formula: "(identity_cohesion_component + emotional_cohesion_component + success_cohesion_component + relational_cohesion_component + goal_cohesion_component) / (full_salience_total + 0.001)"
      inputs: ["identity_cohesion_component", "emotional_cohesion_component", "success_cohesion_component", "relational_cohesion_component", "goal_cohesion_component", "full_salience_total"]
      output_range: [-1.0, 1.0]
      output_type: "float"
      interpretation:
        positive_values: "Discourse supporting democratic institutions and social solidarity"
        negative_values: "Discourse undermining democratic health and promoting fragmentation"

# 5.5: Enhanced Output Schema
# Both dimensional_scores AND derived_metrics are REQUIRED
# calculation_audit is OPTIONAL for computational transparency
output_schema:
  type: object
  properties:
    dimensional_scores:
      type: object
      properties:
        tribal_dominance: { $ref: "#/definitions/score_object" }
        individual_dignity: { $ref: "#/definitions/score_object" }
        fear: { $ref: "#/definitions/score_object" }
        hope: { $ref: "#/definitions/score_object" }
        envy: { $ref: "#/definitions/score_object" }
        mudita: { $ref: "#/definitions/score_object" }
        enmity: { $ref: "#/definitions/score_object" }
        amity: { $ref: "#/definitions/score_object" }
        fragmentative_goals: { $ref: "#/definitions/score_object" }
        cohesive_goals: { $ref: "#/definitions/score_object" }
      required: ["tribal_dominance", "individual_dignity", "fear", "hope", "envy", "mudita", "enmity", "amity", "fragmentative_goals", "cohesive_goals"]
    
    derived_metrics:
      type: object
      properties:
        # Tension indices
        identity_tension: { type: number, minimum: 0.0, maximum: 1.0 }
        emotional_tension: { type: number, minimum: 0.0, maximum: 1.0 }
        success_tension: { type: number, minimum: 0.0, maximum: 1.0 }
        relational_tension: { type: number, minimum: 0.0, maximum: 1.0 }
        goal_tension: { type: number, minimum: 0.0, maximum: 1.0 }
        
        # Strategic coherence
        strategic_contradiction_index: { type: number, minimum: 0.0, maximum: 1.0 }
        
        # Cohesion components (intermediate calculations)
        emotional_cohesion_component: { type: number }
        success_cohesion_component: { type: number }
        relational_cohesion_component: { type: number }
        goal_cohesion_component: { type: number }
        identity_cohesion_component: { type: number }
        
        # Salience totals
        descriptive_salience_total: { type: number, minimum: 0.0 }
        motivational_salience_total: { type: number, minimum: 0.0 }
        full_salience_total: { type: number, minimum: 0.0 }
        
        # Final cohesion indices
        descriptive_cohesion_index: { type: number, minimum: -1.0, maximum: 1.0 }
        motivational_cohesion_index: { type: number, minimum: -1.0, maximum: 1.0 }
        full_cohesion_index: { type: number, minimum: -1.0, maximum: 1.0 }
      
      required: ["identity_tension", "emotional_tension", "success_tension", "relational_tension", "goal_tension", "strategic_contradiction_index", "emotional_cohesion_component", "success_cohesion_component", "relational_cohesion_component", "goal_cohesion_component", "identity_cohesion_component", "descriptive_salience_total", "motivational_salience_total", "full_salience_total", "descriptive_cohesion_index", "motivational_cohesion_index", "full_cohesion_index"]
    
    calculation_audit:
      type: object
      properties:
        computation_code: 
          type: string
          description: "Executable code showing step-by-step derived metric calculations for independent verification"
        framework_version: 
          type: string
          description: "Framework version used for calculations"
        calculation_timestamp: 
          type: string
          format: date-time
          description: "ISO timestamp of when calculations were performed"
        verification_hash: 
          type: string
          description: "Hash of input values for verification purposes"
        calculation_notes:
          type: string
          description: "Any notes about calculation implementation or edge cases handled"
      required: ["computation_code", "framework_version"]
  
  required: ["dimensional_scores", "derived_metrics"]
  
  definitions:
    score_object:
      type: object
      properties:
        raw_score: { type: number, minimum: 0.0, maximum: 1.0 }
        salience: { type: number, minimum: 0.0, maximum: 1.0 }
        confidence: { type: number, minimum: 0.0, maximum: 1.0 }
        evidence: { type: string }
      required: ["raw_score", "salience", "confidence", "evidence"]

# 5.6: Alternative Interpretive Frameworks
interpretive_frameworks:
  democratic_health:
    theory_base: "Deliberative democracy (Habermas, Gutmann & Thompson)"
    positive_indicators: ["individual_dignity", "hope", "amity", "cohesive_goals"]
    concern_indicators: ["tribal_dominance", "fear", "enmity", "fragmentative_goals"]
    application: "Evaluating discourse quality for democratic legitimacy"
    
  competitive_politics:
    theory_base: "Competitive democratic theory (Schumpeter, Przeworski)"
    interpretation: "Strong position-taking and differentiation may indicate healthy democratic competition"
    concern_indicators: ["low_energy", "unclear_choices"]
    application: "Assessing electoral and policy competition dynamics"
    
  social_movement:
    theory_base: "Social movement theory (McAdam, Tarrow, Tilly)"
    interpretation: "Boundary-setting and grievance articulation may be necessary for social change"
    concern_indicators: ["excessive_accommodation"]
    application: "Analyzing advocacy strategies and institutional change efforts"
    
  agonistic_democracy:
    theory_base: "Agonistic pluralism (Mouffe, Connolly)"
    interpretation: "Productive conflict and passion may be essential to democratic vitality"
    concern_indicators: ["excessive_consensus", "suppressed_dissent"]
    application: "Evaluating democratic authenticity and institutional responsiveness"

# 5.7: Cultural and Contextual Limitations
contextual_limitations:
  cultural_scope: "Developed for Western democratic discourse analysis"
  generalizability_concerns:
    - "Parliamentary vs. presidential systems"
    - "Consensus-oriented vs. majoritarian democracies"
    - "High-context vs. low-context communication cultures"  
    - "Collectivist vs. individualist value systems"
  validation_requirements: "Cross-cultural validation studies required before application in non-Western contexts"

# 5.8: Research Application Guidelines
research_guidelines:
  appropriate_uses:
    - "Generating testable hypotheses about discourse-democracy relationships"
    - "Measuring rhetorical patterns for comparative analysis"
    - "Providing empirical data for theory testing"
    - "Supporting mixed-methods research designs"
  
  inappropriate_uses:
    - "Definitively establishing causal relationships"
    - "Providing universal standards for discourse evaluation"
    - "Replacing domain expertise in political communication"
    - "Ignoring context-specific interpretation factors"
  
  theoretical_specification_required: "Researchers must explicitly specify their interpretive framework when reporting results"

# 5.9: Implementation Notes
implementation_notes:
  calculation_order: "Follow the required_calculations sequence: tension_indices → strategic_coherence → cohesion_components → salience_totals → final_indices"
  error_prevention: "Add epsilon (0.001) to all denominators to prevent division by zero"
  precision: "Round final results to 3 decimal places for consistency"
  validation: "Verify all cohesion indices fall within [-1.0, 1.0] range"
  debugging: "If calculations fail, check that all dimensional scores are properly assigned before computing derived metrics"

# --- End of Machine-Readable Appendix ---
```