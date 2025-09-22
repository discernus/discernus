# Civic Analysis Framework (CAF) v10.0

---

## Part 1: The Scholarly Document

### Section 1: Abstract & *Raison d'être*

**What is this framework?**
The Civic Analysis Framework (CAF) is a systematic measurement methodology for quantifying civic virtue and vice patterns in political discourse. Based on Aristotelian virtue ethics and contemporary civic republican theory, this framework provides empirical data about textual patterns that theoretical frameworks associate with civic character, focusing on the tensions between competing moral appeals.

**What problem does it solve?**
Democratic governance depends on civic discourse that embodies fundamental virtues. However, systematic measurement of virtue and vice patterns in political communication has been fragmented and inconsistent. This framework provides reliable, replicable measurements of civic virtue appeals and strategic moral tensions that researchers can use to study relationships between discourse patterns and civic character.

**What it enables:**
These measurements provide empirical foundation for research examining relationships between discourse patterns and civic character assessment, moral positioning, or democratic discourse quality. Researchers integrate CAF data with virtue ethics theory, contextual knowledge, and additional sources to construct analytical arguments about civic implications.

**What it doesn't do:**
The framework measures observable textual features related to civic virtues and vices but does not assess actual speaker character, predict moral behavior, or determine fitness for office. Such assessments require moral philosophy expertise, character evidence, and domain-specific theoretical frameworks.

**Who is it for:**
This framework is designed for political philosophers, civic education researchers, and policy analysts who need reliable empirical measurements of civic virtue patterns in political discourse. It serves as methodological infrastructure for studies of civic character, moral positioning, and democratic discourse analysis.

### Section 2: Theoretical & Empirical Foundations

The CAF is grounded in a multi-disciplinary body of research from political philosophy, virtue ethics, and political communication theory.

#### **Aristotelian Virtue Ethics in a Political Context**
Drawing from Aristotle's *Nicomachean Ethics*, CAF recognizes that excellence in public life depends on the cultivation of specific virtues and the habitual avoidance of corresponding vices. Political leadership requires not merely policy competence but demonstrated moral character worthy of democratic trust. The framework operationalizes this by measuring the observable rhetorical habits of speakers.

**Core Principle**: Character is revealed through choices under pressure. How leaders communicate when facing political challenges reveals their fundamental moral orientation.

#### **Civic Republican Character Theory**
Building on contemporary scholarship by figures like Michael Sandel and Philip Pettit, CAF examines how speakers either embody the civic virtues necessary for democratic leadership or display vices that undermine their fitness for public trust.

**Key Insight**: Democratic governance depends on leaders who prioritize universal principles over narrow interests, demonstrate intellectual integrity, and maintain commitment to democratic norms even when politically costly.

#### **The Importance of Salience Weighting**
A core innovation of the v10 specification is the distinction between a dimension's **intensity** (its raw 0.0-1.0 score) and its **salience** (its rhetorical prominence or emphasis, also 0.0-1.0). This is empirically grounded in research showing that context-dependent weighting based on textual emphasis provides more accurate results than fixed weighting schemes (Laver et al., 2003). By analyzing both intensity and salience, CAF captures not just *what* is being said, but *how much emphasis* it receives, providing a more nuanced and valid assessment.

**Key Citations**:
- Aristotle. *Nicomachean Ethics*.
- Sandel, M. J. (2009). *Justice: What's the right thing to do?*. Farrar, Straus and Giroux.
- Pettit, P. (1997). *Republicanism: A theory of freedom and government*. Oxford University Press.
- Laver, M., Benoit, K., & Garry, J. (2003). Extracting policy positions from political texts using words as data. *American Political Science Review*, 97(2), 311-331.

### Section 3: Measurement Methodology

CAF quantifies political discourse across five bipolar axes that capture fundamental patterns in civic discourse. Each of the ten dimensions is scored independently for both intensity (raw_score) and rhetorical prominence (salience).

**Dimensions & Axes**:

**Identity Axis**: 
-   **Tribalism** (0.0-1.0): Group loyalty over universal principles, us-vs-them framing.
-   **Dignity** (0.0-1.0): Respect for universal human worth, emphasis on shared humanity.

**Truth Axis**:
-   **Manipulation** (0.0-1.0): Strategic distortion of information, emotional manipulation.
-   **Truth** (0.0-1.0): Commitment to factual accuracy, intellectual honesty.

**Justice Axis**:
-   **Resentment** (0.0-1.0): Exploitation of grievances, blame-focused rhetoric.
-   **Justice** (0.0-1.0): Concern for fair outcomes, procedural fairness.

**Emotional Axis**:
-   **Fear** (0.0-1.0): Anxiety-inducing rhetoric, threat-focused language.
-   **Hope** (0.0-1.0): Constructive optimism, positive vision for the future.

**Reality Axis**:
-   **Fantasy** (0.0-1.0): Unrealistic promises, magical thinking, oversimplified solutions.
-   **Pragmatism** (0.0-1.0): Realistic problem-solving, acknowledgment of constraints.

**Measurement Pattern Classifications**
The framework provides data that enables researchers to identify interpretive patterns in civic discourse. These patterns emerge from the relationships between dimensional scores and salience.
- **Virtue Emphasis**: High scores and high salience for virtue dimensions, indicating textual commitment to civic ideals.
- **Surface Virtue Appeals**: High scores but low salience for virtue dimensions, suggesting brief appeals without sustained emphasis.
- **Vice Emphasis**: High scores and high salience for vice dimensions, indicating sustained deployment of divisive or manipulative rhetorical patterns.
- **Strategic Contradictions**: High tension scores between opposing dimensions, indicating inconsistent or contradictory value appeals.

**Derived & Composite Metrics**:

**Character Tension Indices** (0.0-1.0, higher = more contradiction):
These metrics, restored from CAF v5.0, quantify the strategic contradictions in a speaker's rhetoric. They are now salience-weighted to reflect the prominence of the competing appeals.
- **Formula**: `Tension = min(Virtue_Score, Vice_Score) * abs(Virtue_Salience - Vice_Salience)`
- **Indices**: `identity_tension`, `truth_tension`, `justice_tension`, `emotional_tension`, `reality_tension`.

**Salience-Weighted Civic Discourse Index** (-1.0 to +1.0, negative = vice-dominant, positive = virtue-dominant):
This is the primary summary metric, measuring the overall civic discourse orientation. It weights each dimension by its rhetorical prominence.
- **Formula**: The sum of all (Virtue Score * Virtue Salience) minus the sum of all (Vice Score * Vice Salience), normalized by the total salience of all dimensions. This ensures that the most emphasized themes have the greatest impact on the final discourse measurement.

**Sequential Measurement Strategy**:
For highest fidelity measurement, it is recommended to run the five sequential analysis variants (sequential_identity, sequential_truth, sequential_justice, sequential_emotional, sequential_reality) and combine the results. This approach allows the measurement agent to focus exclusively on one axis at a time, reducing cognitive load and improving scoring accuracy. The combined results provide a comprehensive civic discourse profile with enhanced reliability.

**Concept Overlap Resolution**:
The framework addresses the inherent complexity of political discourse where speakers may simultaneously appeal to competing values. Each dimension includes explicit disambiguation rules to guide consistent scoring when conceptual overlap occurs:

- **Identity Axis**: When statements refer to in-group dignity (e.g., "respect for our citizens"), the agent assesses whether the primary function is to create exclusionary contrast (Tribalism) or emphasize universal worth (Dignity). Both can be scored if clearly present.

- **Truth Axis**: Distinguishes between strategic deception (Manipulation) and genuine intellectual honesty (Truth). A statement can be factually correct but manipulative if framed deceptively.

- **Justice Axis**: Separates punitive blame-focus (Resentment) from restorative fairness (Justice). Both may use "fairness" language, so the agent evaluates temporal focus and intent.

- **Emotional Axis**: Allows independent scoring of Fear and Hope, recognizing that speakers can simultaneously warn of threats while offering positive vision.

- **Reality Axis**: Distinguishes between acknowledging constraints (Pragmatism) and denying complexity (Fantasy). Bold plans are Hope, not Fantasy, if grounded in plausible achievement paths.

This systematic approach ensures that the framework captures the full complexity of political rhetoric while maintaining scoring consistency and reliability.

**Machine-Readable Implementation**: The YAML appendix uses structured object formats to enhance LLM agent performance:

- **Enhanced Markers**: Each dimension's `markers` section uses `{ phrase: "...", explanation: "..." }` objects instead of simple lists. This provides context for each example, helping agents understand why specific phrases indicate particular dimensions.

- **Structured Disambiguation**: The `disambiguation` sections use nested objects with `rule`, `context_clues`, `priority`, and `co_occurrence_strategy` keys. This formal structure reduces ambiguity and ensures consistent agent interpretation of complex conceptual overlaps.

These structured formats exceed the base specification requirements but significantly improve scoring accuracy and reliability by providing explicit guidance for boundary cases and concept resolution.

### Section 4: Intended Application & Corpus Fit

-   **Target Corpus Description**: CAF is designed for the analysis of persuasive or strategic communication where a speaker's character is a central element, such as political speeches, candidate debates, and public statements.
-   **Known Limitations & Scope**: The framework is less suited for analyzing purely informational texts, policy documents, or artistic works. It requires a text where a speaker is actively making choices that reveal their moral and civic orientation.
-   **Model Requirements**: This framework requires a highly capable LLM model (e.g., Gemini 2.5 Pro) for reliable analysis due to the nuanced distinctions between dimensions and the dual-track intensity/salience scoring.
-   **System Validation Note**: Be aware that the Discernus platform will perform a post-hoc statistical analysis of your framework's fit with your chosen corpus based on the variance in the results. A low framework-corpus fit score may indicate that the framework was misapplied and could impact the interpretation of the results.

---

## Part 2: The Machine-Readable Appendix
```yaml
# --- Start of Machine-Readable Appendix ---

# 5.1: Metadata
metadata:
  framework_name: "civic_analysis_framework"
  framework_version: "1.0.0"
  author: "Discernus Project"
  spec_version: "10.0"

# 5.2: Analysis Variants
analysis_variants:
  default:
    description: "Complete v10.0 implementation with salience and tension analysis. For highest fidelity analysis, it is recommended to execute the five `sequential_*` analysis variants and combine the results."
    analysis_prompt: |
      You are an expert analyst of civic character and political ethics, grounded in Aristotelian virtue ethics and civic republican theory. Your task is to analyze the provided text using the Civic Analysis Framework v10.0.

      FRAMEWORK METHODOLOGY:
      This framework evaluates civic virtues and vices speakers demonstrate through rhetorical choices. It preserves complexity by independently scoring opposing dimensions for both intensity (raw_score) and rhetorical prominence (salience).

      DIMENSIONAL ANALYSIS:
      You must evaluate 10 dimensions across 5 opposing pairs:
      - Identity: Tribalism vs. Dignity
      - Truth: Manipulation vs. Truth
      - Justice: Resentment vs. Justice
      - Emotional: Fear vs. Hope
      - Reality: Fantasy vs. Pragmatism

      EVIDENCE STANDARDS:
      - Provide exact quotations, not paraphrases.
      - Prioritize direct rhetorical indicators over interpretive inferences.
      - If evidence is ambiguous, lower the confidence score.

      SALIENCE ASSESSMENT: 
      Salience measures rhetorical prominence, not intensity. Consider:
      - Frequency and repetition patterns throughout the text
      - Structural positioning (opening, closing, thesis statements)
      - Thematic centrality to the overall message
      - Rhetorical devices used for emphasis (metaphors, imagery, emotional appeals)
      SALIENCE ≠ INTENSITY. A dimension can have moderate intensity (0.5) but high salience (0.9) if it's rhetorically central.

      LLM GUIDANCE:
      - Avoid anchoring bias from example scores in the markers section
      - Adhere strictly to the provided disambiguation rules to prevent concept conflation
      - Base scores on textual evidence, not inference or assumptions
      - Score each dimension independently; opposing dimensions can both be present
      - Use the boundary_cases guidance to resolve ambiguous phrases

  sequential_identity:
    description: "Focused analysis of Identity axis dimensions (Tribalism, Dignity)"
    analysis_prompt: |
      DIMENSIONAL ANALYSIS: Focus exclusively on the Identity axis dimensions.
      
      **TRIBALISM**: Look for in-group supremacy claims, exclusionary language, "us vs. them" dynamics.
      **DIGNITY**: Look for universal worth language, shared humanity emphasis, inclusive recognition.
      
      **SALIENCE ASSESSMENT**: 
      Salience measures rhetorical prominence, not intensity. Consider:
      - Frequency and repetition patterns throughout the text
      - Structural positioning (opening, closing, thesis statements)
      - Thematic centrality to the overall message
      - Rhetorical devices used for emphasis (metaphors, imagery, emotional appeals)
      SALIENCE ≠ INTENSITY. A dimension can have moderate intensity (0.5) but high salience (0.9) if it's rhetorically central.
      
      **CRITICAL DISAMBIGUATION**: When statements refer to "our people" or "our citizens":
      - If primary function is creating exclusionary contrast → score as Tribalism
      - If primary function is emphasizing inherent worth → score as Dignity  
      - If both present, score both independently and note tension
      
      **BOUNDARY CASES**:
      - "We are a special people" → assess context for superiority vs. pride
      - "Respect for our citizens" → assess for exclusionary vs. universal worth emphasis
      
      Use the scoring calibration guidelines defined for the `tribalism` and `dignity` dimensions and focus only on these two dimensions.

  sequential_truth:
    description: "Focused analysis of Truth axis dimensions (Manipulation, Truth)"
    analysis_prompt: |
      DIMENSIONAL ANALYSIS: Focus exclusively on the Truth axis dimensions.
      
      **MANIPULATION**: Look for strategic deception, emotional exploitation, misleading framing.
      **TRUTH**: Look for factual commitment, intellectual honesty, complexity acknowledgment.
      
      **SALIENCE ASSESSMENT**: 
      Salience measures rhetorical prominence, not intensity. Consider:
      - Frequency and repetition patterns throughout the text
      - Structural positioning (opening, closing, thesis statements)
      - Thematic centrality to the overall message
      - Rhetorical devices used for emphasis (metaphors, imagery, emotional appeals)
      SALIENCE ≠ INTENSITY. A dimension can have moderate intensity (0.5) but high salience (0.9) if it's rhetorically central.
      
      **CRITICAL DISAMBIGUATION**: 
      - Manipulation involves INTENT to mislead (strategic deception)
      - Truth is about adherence to evidence (intellectual honesty)
      - A statement can be factually correct but manipulative if framed deceptively
      - Score both if applicable
      
      **BOUNDARY CASES**:
      - "A biased media" → legitimate critique (Truth) vs. manipulative deflection (Manipulation)
      - "An inconvenient truth" → genuine honesty vs. rhetorical framing device
      
      Use the scoring calibration guidelines defined for the `manipulation` and `truth` dimensions and focus only on these two dimensions.

  sequential_justice:
    description: "Focused analysis of Justice axis dimensions (Resentment, Justice)"
    analysis_prompt: |
      DIMENSIONAL ANALYSIS: Focus exclusively on the Justice axis dimensions.
      
      **RESENTMENT**: Look for grievance exploitation, blame-focused rhetoric, past wrongs emphasis.
      **JUSTICE**: Look for fair outcomes, procedural fairness, systemic solutions.
      
      **SALIENCE ASSESSMENT**: 
      Salience measures rhetorical prominence, not intensity. Consider:
      - Frequency and repetition patterns throughout the text
      - Structural positioning (opening, closing, thesis statements)
      - Thematic centrality to the overall message
      - Rhetorical devices used for emphasis (metaphors, imagery, emotional appeals)
      SALIENCE ≠ INTENSITY. A dimension can have moderate intensity (0.5) but high salience (0.9) if it's rhetorically central.
      
      **CRITICAL DISAMBIGUATION**: Both may use "fairness" language:
      - Resentment: backward-looking, punitive focus on blame
      - Justice: forward-looking, restorative focus on systems
      - Temporal orientation and intent are key differentiators
      
      **BOUNDARY CASES**:
      - "They must be held accountable" → punitive blame (Resentment) vs. restorative fairness (Justice)
      - "Restoring order" → legitimate goal (Justice) vs. pretext for suppression
      
      Use the scoring calibration guidelines defined for the `resentment` and `justice` dimensions and focus only on these two dimensions.

  sequential_emotional:
    description: "Focused analysis of Emotional axis dimensions (Fear, Hope)"
    analysis_prompt: |
      DIMENSIONAL ANALYSIS: Focus exclusively on the Emotional axis dimensions.
      
      **FEAR**: Look for anxiety-inducing rhetoric, threat-focused language, survival concerns.
      **HOPE**: Look for constructive optimism, positive vision, proactive language.
      
      **SALIENCE ASSESSMENT**: 
      Salience measures rhetorical prominence, not intensity. Consider:
      - Frequency and repetition patterns throughout the text
      - Structural positioning (opening, closing, thesis statements)
      - Thematic centrality to the overall message
      - Rhetorical devices used for emphasis (metaphors, imagery, emotional appeals)
      SALIENCE ≠ INTENSITY. A dimension can have moderate intensity (0.5) but high salience (0.9) if it's rhetorically central.
      
      **CRITICAL DISAMBIGUATION**: 
      - Fear focuses on preventing negative future (threat prevention)
      - Hope focuses on achieving positive future (positive vision)
      - A statement can contain both aspects; score independently
      - Hope requires proactive, possibility-focused language (not just fear reduction)
      
      **BOUNDARY CASES**:
      - "A dangerous path" → legitimate warning (Pragmatism) vs. fear appeal
      - "A new American dream" → genuine hope vs. simple reassurance (fear reduction without positive vision)
      
      Use the scoring calibration guidelines defined for the `fear` and `hope` dimensions and focus only on these two dimensions.

  sequential_reality:
    description: "Focused analysis of Reality axis dimensions (Fantasy, Pragmatism)"
    analysis_prompt: |
      DIMENSIONAL ANALYSIS: Focus exclusively on the Reality axis dimensions.
      
      **FANTASY**: Look for unrealistic promises, magical thinking, complexity denial.
      **PRAGMATISM**: Look for realistic problem-solving, constraint acknowledgment, trade-offs.
      
      **SALIENCE ASSESSMENT**: 
      Salience measures rhetorical prominence, not intensity. Consider:
      - Frequency and repetition patterns throughout the text
      - Structural positioning (opening, closing, thesis statements)
      - Thematic centrality to the overall message
      - Rhetorical devices used for emphasis (metaphors, imagery, emotional appeals)
      SALIENCE ≠ INTENSITY. A dimension can have moderate intensity (0.5) but high salience (0.9) if it's rhetorically central.
      
      **CRITICAL DISAMBIGUATION**: 
      - Fantasy denies constraints (impossible outcomes)
      - Pragmatism acknowledges constraints (realistic solutions)
      - Bold, ambitious plans are Hope (not Fantasy) if grounded in plausible achievement paths
      - Pragmatism ≠ pessimism; can still be hopeful
      
      **BOUNDARY CASES**:
      - "A chicken in every pot" → folksy promise (Hope) vs. unrealistic fantasy
      - "A bold new plan" → pragmatic strategy vs. complete fantasy
      
      Use the scoring calibration guidelines defined for the `fantasy` and `pragmatism` dimensions and focus only on these two dimensions.

# 5.3: Dimensions
dimensions:
  - name: "tribalism"
    description: "Group loyalty over universal principles, us-vs-them framing."
    markers:
      positive_examples:
        - { phrase: "our people", explanation: "creates in-group/out-group distinction" }
        - { phrase: "real Americans", explanation: "emphasizes authentic group membership vs. outsiders" }
        - { phrase: "better people", explanation: "claims group moral or cultural superiority" }
        - { phrase: "not our kind", explanation: "explicit exclusion of others" }
        - { phrase: "chosen people", explanation: "special status claims for the group" }
      negative_examples:
        - { phrase: "patriotism", explanation: "love of country without exclusion doesn't qualify" }
        - { phrase: "community pride", explanation: "positive group identity without supremacy claims" }
        - { phrase: "we are different", explanation: "simple distinction without superiority claims" }
      boundary_cases:
        - { phrase: "we are a special people", explanation: "depends on context; could be simple pride or imply superiority." }
    disambiguation:
      overlap_with_dignity:
        rule: "When a statement expresses respect for an in-group ('our people'), assess the context."
        context_clues: "Look for 'us vs. them' dynamic or implied superiority vs. emphasis on inherent worth"
        priority: "If both aspects present, score both and note tension in evidence"
        co_occurrence_strategy: "Tribalism and Dignity can coexist; score independently based on textual evidence"
    
    scoring_calibration:
      high: "0.7-1.0: Combines strong supremacy claims and clear exclusionary implications."
      medium: "0.4-0.6: Moderate in-group preference, subtle exclusion"
      low: "0.1-0.3: Mild group preference, weak exclusionary hints"
      absent: "0.0: No group supremacy or exclusion"

  - name: "dignity"
    description: "Respect for universal human worth, emphasis on shared humanity."
    markers:
      positive_examples:
        - { phrase: "every person", explanation: "universal scope of human worth" }
        - { phrase: "common humanity", explanation: "shared human experience transcending divisions" }
        - { phrase: "inherent dignity", explanation: "intrinsic value regardless of group membership" }
        - { phrase: "equal treatment", explanation: "procedural fairness across groups" }
        - { phrase: "everyone belongs", explanation: "inclusive community vision" }
      negative_examples:
        - { phrase: "individual rights", explanation: "legal/political concept, not dignity focus" }
        - { phrase: "personal achievement", explanation: "individual success, not universal worth" }
        - { phrase: "respect for persons", explanation: "depends on universality vs. selective respect" }
      boundary_cases:
        - { phrase: "respect for our citizens", explanation: "depends on whether 'our' is descriptive or exclusionary." }
    disambiguation:
      overlap_with_tribalism:
        rule: "When a statement refers to 'our citizens' or similar in-group language, assess whether it emphasizes universal worth or creates exclusionary contrast."
        context_clues: "Universal worth emphasis vs. 'us vs. them' dynamic"
        priority: "If both aspects present, score both independently"
        co_occurrence_strategy: "Dignity and Tribalism can coexist; score based on textual evidence"
    scoring_calibration:
      high: "0.7-1.0: Combines strong universal worth language and explicit inclusion."
      medium: "0.4-0.6: Moderate inclusivity, some universal recognition"
      low: "0.1-0.3: Weak inclusive hints, minimal dignity language"
      absent: "0.0: No universal worth themes"

  - name: "manipulation"
    description: "Strategic distortion of information, emotional manipulation."
    markers:
      positive_examples:
        - { phrase: "they're hiding the truth", explanation: "conspiratorial framing" }
        - { phrase: "don't be fooled", explanation: "implies hidden deceptions" }
        - { phrase: "misleading information", explanation: "false claims or deceptive statements" }
        - { phrase: "propaganda", explanation: "information warfare or message control" }
        - { phrase: "emotional manipulation", explanation: "feeling exploitation for rhetorical gain" }
      negative_examples:
        - { phrase: "let's look at the facts", explanation: "evidence-based appeal without distortion" }
        - { phrase: "the evidence shows", explanation: "appeal to verifiable facts" }
        - { phrase: "it's a complex issue", explanation: "acknowledgment of nuance" }
      boundary_cases:
        - { phrase: "a biased media", explanation: "could be a legitimate critique (Truth) or a manipulative deflection (Manipulation)." }
    scoring_calibration:
      high: "0.7-1.0: Combines clear deceptive rhetoric and emotional exploitation."
      medium: "0.4-0.6: Some misleading framing or spin"
      low: "0.1-0.3: Minor rhetorical exaggeration"
      absent: "0.0: No deceptive or manipulative rhetoric"
    disambiguation:
      overlap_with_truth:
        rule: "Manipulation involves intent to mislead."
        context_clues: "Look for strategic deception vs. good faith errors"
        priority: "Intent is the key differentiator"
        co_occurrence_strategy: "A statement can be factually correct but manipulative if framed deceptively"

  - name: "truth"
    description: "Commitment to factual accuracy, intellectual honesty."
    markers:
      positive_examples:
        - { phrase: "the evidence shows", explanation: "appeal to verifiable facts" }
        - { phrase: "it's a complex issue", explanation: "acknowledgment of nuance" }
        - { phrase: "factual accuracy", explanation: "empirical evidence and verifiable data" }
        - { phrase: "intellectual honesty", explanation: "honest assessment and candid evaluation" }
        - { phrase: "acknowledge uncertainty", explanation: "admit mistakes and correct errors" }
      negative_examples:
        - { phrase: "believe me", explanation: "appeal to authority, not evidence" }
        - { phrase: "trust me", explanation: "appeal to personal credibility over facts" }
        - { phrase: "everyone knows", explanation: "appeal to common knowledge without evidence" }
      boundary_cases:
        - { phrase: "an inconvenient truth", explanation: "could be genuine intellectual honesty or a rhetorical framing device." }
    scoring_calibration:
      high: "0.7-1.0: Combines strong factual commitment and complexity acknowledgment."
      medium: "0.4-0.6: Generally factual, but may omit inconvenient details"
      low: "0.1-0.3: Some appeal to facts, but weak"
      absent: "0.0: No commitment to factual accuracy"
    disambiguation:
      overlap_with_manipulation:
        rule: "Truth is about adherence to evidence and intellectual honesty."
        context_clues: "Factual accuracy vs. deceptive framing"
        priority: "Score both if applicable"
        co_occurrence_strategy: "A statement can be factually correct but still manipulative if framed deceptively"

  - name: "resentment"
    description: "Exploitation of grievances, blame-focused rhetoric."
    markers:
      positive_examples:
        - { phrase: "the system is rigged", explanation: "grievance and systemic blame" }
        - { phrase: "it's their fault", explanation: "direct blame attribution" }
        - { phrase: "grievance", explanation: "complaint and injustice suffered" }
        - { phrase: "victimization", explanation: "persecution and discrimination claims" }
        - { phrase: "historical wrong", explanation: "past injustice and inherited grievance" }
      negative_examples:
        - { phrase: "we need reform", explanation: "focus on solutions, not blame" }
        - { phrase: "let's fix this", explanation: "constructive problem-solving approach" }
        - { phrase: "moving forward", explanation: "future-oriented rather than backward-looking" }
      boundary_cases:
        - { phrase: "they must be held accountable", explanation: "could be a call for Justice or a simple expression of Resentment." }
    scoring_calibration:
      high: "0.7-1.0: Combines strong grievance focus and clear blame assignment."
      medium: "0.4-0.6: Moderate grievance framing"
      low: "0.1-0.3: Minor hints of blame or grievance"
      absent: "0.0: No grievance or blame rhetoric"
    disambiguation:
      overlap_with_justice:
        rule: "Resentment focuses on blame for past wrongs. Justice focuses on solutions for future fairness."
        context_clues: "Punitive focus vs. restorative focus"
        priority: "Temporal focus and intent are key"
        co_occurrence_strategy: "Both may use 'fairness' language; distinguish between backward-looking grievance and forward-looking systemic focus"

  - name: "justice"
    description: "Concern for fair outcomes, procedural fairness."
    markers:
      positive_examples:
        - { phrase: "equal treatment for all", explanation: "appeal to procedural fairness" }
        - { phrase: "a level playing field", explanation: "metaphor for fair opportunity" }
        - { phrase: "due process", explanation: "procedural fairness and established process" }
        - { phrase: "proportional response", explanation: "appropriate measure and fitting consequence" }
        - { phrase: "fair consideration", explanation: "balanced approach and impartial treatment" }
      negative_examples:
        - { phrase: "we must win at all costs", explanation: "focus on outcomes over process" }
        - { phrase: "ends justify means", explanation: "outcome focus over procedural fairness" }
        - { phrase: "whatever it takes", explanation: "goal orientation over fair process" }
      boundary_cases:
        - { phrase: "restoring order", explanation: "could be a legitimate goal of Justice or a pretext for suppressing dissent." }
    scoring_calibration:
      high: "0.7-1.0: Combines strong fairness focus and procedural emphasis."
      medium: "0.4-0.6: Moderate concern for fairness"
      low: "0.1-0.3: Weak appeals to fairness"
      absent: "0.0: No concern for fairness or justice"
    disambiguation:
      overlap_with_resentment:
        rule: "Justice seeks fair systems and procedures. Resentment seeks retribution for perceived slights."
        context_clues: "Forward-looking systemic focus vs. backward-looking grievance focus"
        priority: "Temporal orientation is key"
        co_occurrence_strategy: "Both may use 'fairness' language; distinguish between restorative systems and punitive blame"

  - name: "fear"
    description: "Anxiety-inducing rhetoric, threat-focused language."
    markers:
      positive_examples:
        - { phrase: "existential threat", explanation: "survival-level danger" }
        - { phrase: "our way of life is under attack", explanation: "active threat perception" }
        - { phrase: "catastrophe", explanation: "disaster language and crisis framing" }
        - { phrase: "running out of time", explanation: "urgency and deadline pressure" }
        - { phrase: "emergency", explanation: "crisis requiring immediate action" }
      negative_examples:
        - { phrase: "we face challenges", explanation: "difficulty without crisis implication" }
        - { phrase: "serious problem", explanation: "significant issue without existential threat" }
        - { phrase: "concern", explanation: "worry without crisis implication" }
      boundary_cases:
        - { phrase: "a dangerous path", explanation: "could be a legitimate warning (Pragmatism) or an appeal to Fear." }
    scoring_calibration:
      high: "0.7-1.0: Combines existential crisis and survival threats."
      medium: "0.4-0.6: Serious concerns, significant risks"
      low: "0.1-0.3: Minor worries, potential problems"
      absent: "0.0: No threat language or fear appeals"
    disambiguation:
      overlap_with_hope:
        rule: "Fear focuses on preventing a negative future. Hope focuses on achieving a positive one."
        context_clues: "Threat prevention vs. positive vision"
        priority: "Score both independently if present"
        co_occurrence_strategy: "A statement can contain both (e.g., 'We must act now to avoid disaster and build a better world')"

  - name: "hope"
    description: "Constructive optimism, positive vision for the future."
    markers:
      positive_examples:
        - { phrase: "a brighter future is possible", explanation: "optimistic forward vision" }
        - { phrase: "we can build a better world", explanation: "empowerment and positive action" }
        - { phrase: "breakthrough", explanation: "significant positive progress" }
        - { phrase: "moving forward", explanation: "progress and advancement" }
        - { phrase: "opportunity", explanation: "positive potential and possibility" }
      negative_examples:
        - { phrase: "we must protect what we have", explanation: "maintaining status quo, not progress" }
        - { phrase: "stability", explanation: "maintaining current state, not advancement" }
        - { phrase: "recovery", explanation: "returning to previous state, not advancement" }
      boundary_cases:
        - { phrase: "a new American dream", explanation: "could be genuine Hope or a form of political Fantasy." }
    scoring_calibration:
      high: "0.7-1.0: Combines strong optimism and clear progress vision."
      medium: "0.4-0.6: Moderate optimism, some progress indicators"
      low: "0.1-0.3: Mild optimism"
      absent: "0.0: No optimistic or progress-oriented language"
    disambiguation:
      overlap_with_fear:
        rule: "Hope is not merely the absence of fear."
        context_clues: "Proactive, possibility-focused language vs. fear reduction"
        priority: "Look for positive, constructive vision"
        co_occurrence_strategy: "A speaker can reduce fear without inspiring hope; require proactive language"

  - name: "fantasy"
    description: "Unrealistic promises, magical thinking, oversimplified solutions."
    markers:
      positive_examples:
        - { phrase: "we can solve this overnight", explanation: "unrealistic timeline" }
        - { phrase: "a simple solution", explanation: "denial of complexity" }
        - { phrase: "magical thinking", explanation: "wishful thinking and fantasy solutions" }
        - { phrase: "perfect world", explanation: "ideal society without flaws" }
        - { phrase: "effortless solutions", explanation: "painless change and cost-free benefits" }
      negative_examples:
        - { phrase: "it will be difficult, but...", explanation: "acknowledgment of reality and constraints" }
        - { phrase: "complex challenges", explanation: "recognition of difficulty" }
        - { phrase: "trade-offs", explanation: "acknowledgment of constraints" }
      boundary_cases:
        - { phrase: "a chicken in every pot", explanation: "could be a folksy promise (Hope) or an unrealistic Fantasy." }
    scoring_calibration:
      high: "0.7-1.0: Combines impossible outcomes and complexity denial."
      medium: "0.4-0.6: Some oversimplification or unrealistic expectations"
      low: "0.1-0.3: Mildly unrealistic"
      absent: "0.0: No magical thinking or complexity denial"
    disambiguation:
      overlap_with_pragmatism:
        rule: "Fantasy denies constraints, while Pragmatism acknowledges them."
        context_clues: "Constraint denial vs. constraint acknowledgment"
        priority: "Bold plans can be Hope if grounded in plausible achievement paths"
        co_occurrence_strategy: "Distinguish between unrealistic promises and ambitious but achievable goals"

  - name: "pragmatism"
    description: "Realistic problem-solving, acknowledgment of constraints."
    markers:
      positive_examples:
        - { phrase: "there are no easy answers", explanation: "acknowledgment of complexity" }
        - { phrase: "we must make tough choices", explanation: "recognition of trade-offs" }
        - { phrase: "practical solutions", explanation: "workable approach and feasible plan" }
        - { phrase: "implementation strategy", explanation: "execution plan and delivery mechanism" }
        - { phrase: "results-oriented", explanation: "outcome-focused and achievement-directed" }
      negative_examples:
        - { phrase: "we can have it all", explanation: "denial of constraints" }
        - { phrase: "perfect solution", explanation: "unrealistic expectations" }
        - { phrase: "no trade-offs", explanation: "denial of complexity" }
      boundary_cases:
        - { phrase: "a bold new plan", explanation: "could be a pragmatic, ambitious strategy or a complete fantasy." }
    scoring_calibration:
      high: "0.7-1.0: Combines strong practical focus and constraint recognition."
      medium: "0.4-0.6: Some practical considerations"
      low: "0.1-0.3: Weakly pragmatic"
      absent: "0.0: No focus on practical constraints"
    disambiguation:
      overlap_with_fantasy:
        rule: "Pragmatism is the opposite of Fantasy."
        context_clues: "Constraint acknowledgment vs. constraint denial"
        priority: "Acknowledging constraints and trade-offs"
        co_occurrence_strategy: "Distinguish from pessimism; pragmatic approach can still be hopeful"

# 5.4: Derived Metrics
derived_metrics:
  # Character Tension Indices (from v5.0)
  - name: "identity_tension"
    description: "Measures the strategic contradiction between Dignity and Tribalism appeals, weighted by salience."
    formula: "min(dimensions.dignity.raw_score, dimensions.tribalism.raw_score) * abs(dimensions.dignity.salience - dimensions.tribalism.salience)"
  - name: "truth_tension"
    description: "Measures the strategic contradiction between Truth and Manipulation appeals, weighted by salience."
    formula: "min(dimensions.truth.raw_score, dimensions.manipulation.raw_score) * abs(dimensions.truth.salience - dimensions.manipulation.salience)"
  - name: "justice_tension"
    description: "Measures the strategic contradiction between Justice and Resentment appeals, weighted by salience."
    formula: "min(dimensions.justice.raw_score, dimensions.resentment.raw_score) * abs(dimensions.justice.salience - dimensions.resentment.salience)"
  - name: "emotional_tension"
    description: "Measures the strategic contradiction between Hope and Fear appeals, weighted by salience."
    formula: "min(dimensions.hope.raw_score, dimensions.fear.raw_score) * abs(dimensions.hope.salience - dimensions.fear.salience)"
  - name: "reality_tension"
    description: "Measures the strategic contradiction between Pragmatism and Fantasy appeals, weighted by salience."
    formula: "min(dimensions.pragmatism.raw_score, dimensions.fantasy.raw_score) * abs(dimensions.pragmatism.salience - dimensions.fantasy.salience)"
  
  # Intermediate calculations for Salience-Weighted Civic Character Index
  - name: "virtue_salience_total"
    description: "Sum of all virtue dimension salience weights for normalization."
    formula: "(dimensions.dignity.salience + dimensions.truth.salience + dimensions.justice.salience + dimensions.hope.salience + dimensions.pragmatism.salience)"
  - name: "vice_salience_total"
    description: "Sum of all vice dimension salience weights for normalization."
    formula: "(dimensions.tribalism.salience + dimensions.manipulation.salience + dimensions.resentment.salience + dimensions.fear.salience + dimensions.fantasy.salience)"
  - name: "combined_salience_total"
    description: "Total salience across all dimensions for normalization."
    formula: "(dimensions.dignity.salience + dimensions.truth.salience + dimensions.justice.salience + dimensions.hope.salience + dimensions.pragmatism.salience + dimensions.tribalism.salience + dimensions.manipulation.salience + dimensions.resentment.salience + dimensions.fear.salience + dimensions.fantasy.salience)"
    
  - name: "weighted_virtue_score"
    description: "Sum of all virtue scores multiplied by their respective salience weights."
    formula: "((dimensions.dignity.raw_score * dimensions.dignity.salience) + (dimensions.truth.raw_score * dimensions.truth.salience) + (dimensions.justice.raw_score * dimensions.justice.salience) + (dimensions.hope.raw_score * dimensions.hope.salience) + (dimensions.pragmatism.raw_score * dimensions.pragmatism.salience))"
  - name: "weighted_vice_score"
    description: "Sum of all vice scores multiplied by their respective salience weights."
    formula: "((dimensions.tribalism.raw_score * dimensions.tribalism.salience) + (dimensions.manipulation.raw_score * dimensions.manipulation.salience) + (dimensions.resentment.raw_score * dimensions.resentment.salience) + (dimensions.fear.raw_score * dimensions.fear.salience) + (dimensions.fantasy.raw_score * dimensions.fantasy.salience))"
  
  # Final Salience-Weighted Civic Character Index
  - name: "civic_character_index"
    description: "Primary summary metric measuring overall character orientation, weighted by rhetorical prominence."
    formula: "(derived_metrics.weighted_virtue_score - derived_metrics.weighted_vice_score) / (derived_metrics.combined_salience_total + 0.001)"

# 5.5: Output Schema
output_schema:
  type: object
  properties:
    dimensional_scores:
      type: object
      properties:
        tribalism: { $ref: "#/definitions/score_object" }
        dignity: { $ref: "#/definitions/score_object" }
        manipulation: { $ref: "#/definitions/score_object" }
        truth: { $ref: "#/definitions/score_object" }
        resentment: { $ref: "#/definitions/score_object" }
        justice: { $ref: "#/definitions/score_object" }
        fear: { $ref: "#/definitions/score_object" }
        hope: { $ref: "#/definitions/score_object" }
        fantasy: { $ref: "#/definitions/score_object" }
        pragmatism: { $ref: "#/definitions/score_object" }
  required: [ "dimensional_scores" ]
  definitions:
    score_object:
      type: object
      properties:
        raw_score: { type: number, minimum: 0.0, maximum: 1.0 }
        salience: { type: number, minimum: 0.0, maximum: 1.0 }
        confidence: { type: number, minimum: 0.0, maximum: 1.0 }
        evidence: { type: string }
      required: [ "raw_score", "salience", "confidence", "evidence" ]

# --- End of Machine-Readable Appendix ---
