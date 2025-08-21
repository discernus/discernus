# Civic Analysis Framework (CAF) v10.0

---

## Part 1: The Scholarly Document

### Section 1: Abstract & *Raison d'être*

**What is this framework?**
The Civic Analysis Framework (CAF) provides a systematic approach to evaluating the civic character of political discourse. It analyzes the moral character displayed by speakers, based on Aristotelian virtue ethics and contemporary civic republican theory. The framework evaluates what civic virtues and vices speakers demonstrate through their rhetorical choices, focusing on the fundamental tensions between competing values.

**What problem does it solve?**
Democratic governance depends on civic discourse that embodies fundamental virtues. However, political communication often involves strategic tensions where speakers simultaneously appeal to competing virtues and their pathological counterparts. This framework provides a rigorous methodology for evaluating these tensions and assessing the overall civic character of political discourse. It moves beyond simple sentiment analysis to quantify the moral coherence of a speaker's communication.

**Who is it for?**
This framework is designed for researchers, journalists, educators, and citizens who need to assess the moral fitness and integrity of political leaders. It is applicable to political speeches, debates, interviews, and other forms of public communication where a speaker's character is revealed.

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

### Section 3: Analytical Methodology

CAF evaluates political discourse across five bipolar axes that form the foundation of civic character. Each of the ten dimensions is scored independently for both intensity (raw_score) and rhetorical prominence (salience).

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

**Interpretive Guidance: Pattern Classifications**
While not calculated as formal metrics, the synthesis agent should be guided by the following interpretive patterns to assess the overall character profile. These patterns emerge from the relationships between dimensional scores and salience.
- **Authentic Virtue**: High scores and high salience for virtue dimensions, indicating a genuine commitment to civic ideals.
- **Strategic Virtue Signaling**: High scores but low salience for virtue dimensions, suggesting superficial appeals without substantive commitment.
- **Strategic Pathology**: High scores and high salience for vice dimensions, indicating a deliberate deployment of divisive or manipulative rhetoric.
- **Incoherent Messaging**: High tension scores between opposing dimensions, indicating inconsistent or contradictory value appeals.

**Derived & Composite Metrics**:

**Character Tension Indices** (0.0-1.0, higher = more contradiction):
These metrics, restored from CAF v5.0, quantify the strategic contradictions in a speaker's rhetoric. They are now salience-weighted to reflect the prominence of the competing appeals.
- **Formula**: `Tension = min(Virtue_Score, Vice_Score) * abs(Virtue_Salience - Vice_Salience)`
- **Indices**: `identity_tension`, `truth_tension`, `justice_tension`, `emotional_tension`, `reality_tension`.

**Salience-Weighted Civic Character Index** (-1.0 to +1.0, negative = vice-dominant, positive = virtue-dominant):
This is the primary summary metric, calculating the overall character orientation of the discourse. It weights each dimension by its rhetorical prominence.
- **Formula**: The sum of all (Virtue Score * Virtue Salience) minus the sum of all (Vice Score * Vice Salience), normalized by the total salience of all dimensions. This ensures that the most emphasized themes have the greatest impact on the final character assessment.

### Section 4: Intended Application & Corpus Fit

-   **Target Corpus Description**: CAF is designed for the analysis of persuasive or strategic communication where a speaker's character is a central element, such as political speeches, candidate debates, and public statements.
-   **Known Limitations & Scope**: The framework is less suited for analyzing purely informational texts, policy documents, or artistic works. It requires a text where a speaker is actively making choices that reveal their moral and civic orientation.
-   **Model Requirements**: This framework requires a highly capable LLM model (e.g., Gemini 2.5 Pro) for reliable analysis due to the nuanced distinctions between dimensions and the dual-track intensity/salience scoring.

---

## Part 2: The Machine-Readable Appendix
```yaml
# --- Start of Machine-Readable Appendix ---

# 5.1: Metadata
metadata:
  framework_name: "civic_analysis_framework"
  framework_version: "10.0.0"
  author: "Discernus Project"
  spec_version: "10.0"

# 5.2: Analysis Variants
analysis_variants:
  default:
    description: "Complete v10.0 implementation with salience and tension analysis."
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
      Salience measures rhetorical prominence. Consider frequency, structural positioning (openings/closings), and thematic centrality. SALIENCE is not the same as INTENSITY.

  sequential_identity:
    description: "Focus on Identity axis: Tribalism vs Dignity."
    analysis_prompt: |
      You are an expert political discourse analyst specializing in social identity and group dynamics. Focus exclusively on evaluating the Identity axis in the provided text using the Civic Analysis Framework v10.0.
      DIMENSIONAL FOCUS: Identity Axis Only - Tribalism vs. Dignity.
      Provide raw_score, salience, evidence, and confidence for BOTH dimensions.

  sequential_truth:
    description: "Focus on Truth axis: Manipulation vs Truth."
    analysis_prompt: |
      You are an expert political discourse analyst specializing in deceptive rhetoric and intellectual honesty. Focus exclusively on evaluating the Truth axis in the provided text using the Civic Analysis Framework v10.0.
      DIMENSIONAL FOCUS: Truth Axis Only - Manipulation vs. Truth.
      Provide raw_score, salience, evidence, and confidence for BOTH dimensions.

  sequential_justice:
    description: "Focus on Justice axis: Resentment vs Justice."
    analysis_prompt: |
      You are an expert political discourse analyst specializing in grievance politics and fairness rhetoric. Focus exclusively on evaluating the Justice axis in the provided text using the Civic Analysis Framework v10.0.
      DIMENSIONAL FOCUS: Justice Axis Only - Resentment vs. Justice.
      Provide raw_score, salience, evidence, and confidence for BOTH dimensions.

  sequential_emotional:
    description: "Focus on Emotional axis: Fear vs Hope."
    analysis_prompt: |
      You are an expert political discourse analyst specializing in emotional appeals and crisis rhetoric. Focus exclusively on evaluating the Emotional axis in the provided text using the Civic Analysis Framework v10.0.
      DIMENSIONAL FOCUS: Emotional Axis Only - Fear vs. Hope.
      Provide raw_score, salience, evidence, and confidence for BOTH dimensions.

  sequential_reality:
    description: "Focus on Reality axis: Fantasy vs Pragmatism."
    analysis_prompt: |
      You are an expert political discourse analyst specializing in policy realism and utopian promises. Focus exclusively on evaluating the Reality axis in the provided text using the Civic Analysis Framework v10.0.
      DIMENSIONAL FOCUS: Reality Axis Only - Fantasy vs. Pragmatism.
      Provide raw_score, salience, evidence, and confidence for BOTH dimensions.

# 5.3: Dimensions
dimensions:
  - name: "tribalism"
    description: "Group loyalty over universal principles, us-vs-them framing."
    markers:
      positive_examples:
        - { phrase: "our people", explanation: "creates in-group/out-group distinction" }
        - { phrase: "real Americans", explanation: "emphasizes authentic group membership vs. outsiders" }
      negative_examples:
        - { phrase: "patriotism", explanation: "love of country without exclusion doesn't qualify" }
    scoring_calibration:
      high: "0.7-1.0: Explicit supremacy claims, strong us-vs-them rhetoric, exclusionary language"
      medium: "0.4-0.6: Moderate in-group preference, subtle exclusion"
      low: "0.1-0.3: Mild group preference"
      absent: "0.0: No group supremacy or exclusion"

  - name: "dignity"
    description: "Respect for universal human worth, emphasis on shared humanity."
    markers:
      positive_examples:
        - { phrase: "every person", explanation: "universal scope of human worth" }
        - { phrase: "common humanity", explanation: "shared human experience transcending divisions" }
      negative_examples:
        - { phrase: "individual rights", explanation: "legal/political concept, not dignity focus" }
    scoring_calibration:
      high: "0.7-1.0: Strong universal worth language, explicit inclusion"
      medium: "0.4-0.6: Moderate inclusivity, some universal recognition"
      low: "0.1-0.3: Weak inclusive hints"
      absent: "0.0: No universal worth themes"

  - name: "manipulation"
    description: "Strategic distortion of information, emotional manipulation."
    markers:
      positive_examples:
        - { phrase: "they're hiding the truth", explanation: "conspiratorial framing" }
        - { phrase: "don't be fooled", explanation: "implies hidden deceptions" }
      negative_examples:
        - { phrase: "let's look at the facts", explanation: "evidence-based appeal without distortion" }
    scoring_calibration:
      high: "0.7-1.0: Clear use of deceptive rhetoric, emotional exploitation"
      medium: "0.4-0.6: Some misleading framing or spin"
      low: "0.1-0.3: Minor rhetorical exaggeration"
      absent: "0.0: No deceptive or manipulative rhetoric"

  - name: "truth"
    description: "Commitment to factual accuracy, intellectual honesty."
    markers:
      positive_examples:
        - { phrase: "the evidence shows", explanation: "appeal to verifiable facts" }
        - { phrase: "it's a complex issue", explanation: "acknowledgment of nuance" }
      negative_examples:
        - { phrase: "believe me", explanation: "appeal to authority, not evidence" }
    scoring_calibration:
      high: "0.7-1.0: Strong commitment to facts, acknowledges complexity and uncertainty"
      medium: "0.4-0.6: Generally factual, but may omit inconvenient details"
      low: "0.1-0.3: Some appeal to facts, but weak"
      absent: "0.0: No commitment to factual accuracy"

  - name: "resentment"
    description: "Exploitation of grievances, blame-focused rhetoric."
    markers:
      positive_examples:
        - { phrase: "the system is rigged", explanation: "grievance and systemic blame" }
        - { phrase: "it's their fault", explanation: "direct blame attribution" }
      negative_examples:
        - { phrase: "we need reform", explanation: "focus on solutions, not blame" }
    scoring_calibration:
      high: "0.7-1.0: Strong grievance focus, clear blame assignment"
      medium: "0.4-0.6: Moderate grievance framing"
      low: "0.1-0.3: Minor hints of blame or grievance"
      absent: "0.0: No grievance or blame rhetoric"

  - name: "justice"
    description: "Concern for fair outcomes, procedural fairness."
    markers:
      positive_examples:
        - { phrase: "equal treatment for all", explanation: "appeal to procedural fairness" }
        - { phrase: "a level playing field", explanation: "metaphor for fair opportunity" }
      negative_examples:
        - { phrase: "we must win at all costs", explanation: "focus on outcomes over process" }
    scoring_calibration:
      high: "0.7-1.0: Strong focus on fairness, due process, and equity"
      medium: "0.4-0.6: Moderate concern for fairness"
      low: "0.1-0.3: Weak appeals to fairness"
      absent: "0.0: No concern for fairness or justice"

  - name: "fear"
    description: "Anxiety-inducing rhetoric, threat-focused language."
    markers:
      positive_examples:
        - { phrase: "existential threat", explanation: "survival-level danger" }
        - { phrase: "our way of life is under attack", explanation: "active threat perception" }
      negative_examples:
        - { phrase: "we face challenges", explanation: "difficulty without crisis implication" }
    scoring_calibration:
      high: "0.7-1.0: Existential crisis, survival threats, imminent catastrophe"
      medium: "0.4-0.6: Serious concerns, significant risks"
      low: "0.1-0.3: Minor worries, potential problems"
      absent: "0.0: No threat language or fear appeals"

  - name: "hope"
    description: "Constructive optimism, positive vision for the future."
    markers:
      positive_examples:
        - { phrase: "a brighter future is possible", explanation: "optimistic forward vision" }
        - { phrase: "we can build a better world", explanation: "empowerment and positive action" }
      negative_examples:
        - { phrase: "we must protect what we have", explanation: "maintaining status quo, not progress" }
    scoring_calibration:
      high: "0.7-1.0: Strong optimism, clear progress vision"
      medium: "0.4-0.6: Moderate optimism, some progress indicators"
      low: "0.1-0.3: Mild optimism"
      absent: "0.0: No optimistic or progress-oriented language"

  - name: "fantasy"
    description: "Unrealistic promises, magical thinking, oversimplified solutions."
    markers:
      positive_examples:
        - { phrase: "we can solve this overnight", explanation: "unrealistic timeline" }
        - { phrase: "a simple solution", explanation: "denial of complexity" }
      negative_examples:
        - { phrase: "it will be difficult, but...", explanation: "acknowledgment of reality and constraints" }
    scoring_calibration:
      high: "0.7-1.0: Promises impossible outcomes, clear denial of complexity"
      medium: "0.4-0.6: Some oversimplification or unrealistic expectations"
      low: "0.1-0.3: Mildly unrealistic"
      absent: "0.0: No magical thinking or complexity denial"

  - name: "pragmatism"
    description: "Realistic problem-solving, acknowledgment of constraints."
    markers:
      positive_examples:
        - { phrase: "there are no easy answers", explanation: "acknowledgment of complexity" }
        - { phrase: "we must make tough choices", explanation: "recognition of trade-offs" }
      negative_examples:
        - { phrase: "we can have it all", explanation: "denial of constraints" }
    scoring_calibration:
      high: "0.7-1.0: Strong focus on realistic solutions, acknowledges trade-offs"
      medium: "0.4-0.6: Some practical considerations"
      low: "0.1-0.3: Weakly pragmatic"
      absent: "0.0: No focus on practical constraints"

# 5.4: Derived Metrics
derived_metrics:
  # Character Tension Indices (from v5.0)
  - name: "identity_tension"
    formula: "min(dimensional_scores.dignity.raw_score, dimensional_scores.tribalism.raw_score) * abs(dimensional_scores.dignity.salience - dimensional_scores.tribalism.salience)"
  - name: "truth_tension"
    formula: "min(dimensional_scores.truth.raw_score, dimensional_scores.manipulation.raw_score) * abs(dimensional_scores.truth.salience - dimensional_scores.manipulation.salience)"
  - name: "justice_tension"
    formula: "min(dimensional_scores.justice.raw_score, dimensional_scores.resentment.raw_score) * abs(dimensional_scores.justice.salience - dimensional_scores.resentment.salience)"
  - name: "emotional_tension"
    formula: "min(dimensional_scores.hope.raw_score, dimensional_scores.fear.raw_score) * abs(dimensional_scores.hope.salience - dimensional_scores.fear.salience)"
  - name: "reality_tension"
    formula: "min(dimensional_scores.pragmatism.raw_score, dimensional_scores.fantasy.raw_score) * abs(dimensional_scores.pragmatism.salience - dimensional_scores.fantasy.salience)"
  
  # Intermediate calculations for Salience-Weighted Civic Character Index
  - name: "virtue_salience_total"
    formula: "(dimensional_scores.dignity.salience + dimensional_scores.truth.salience + dimensional_scores.justice.salience + dimensional_scores.hope.salience + dimensional_scores.pragmatism.salience)"
  - name: "vice_salience_total"
    formula: "(dimensional_scores.tribalism.salience + dimensional_scores.manipulation.salience + dimensional_scores.resentment.salience + dimensional_scores.fear.salience + dimensional_scores.fantasy.salience)"
  - name: "combined_salience_total"
    formula: "(derived_metrics.virtue_salience_total + derived_metrics.vice_salience_total)"
    
  - name: "weighted_virtue_score"
    formula: "((dimensional_scores.dignity.raw_score * dimensional_scores.dignity.salience) + (dimensional_scores.truth.raw_score * dimensional_scores.truth.salience) + (dimensional_scores.justice.raw_score * dimensional_scores.justice.salience) + (dimensional_scores.hope.raw_score * dimensional_scores.hope.salience) + (dimensional_scores.pragmatism.raw_score * dimensional_scores.pragmatism.salience))"
  - name: "weighted_vice_score"
    formula: "((dimensional_scores.tribalism.raw_score * dimensional_scores.tribalism.salience) + (dimensional_scores.manipulation.raw_score * dimensional_scores.manipulation.salience) + (dimensional_scores.resentment.raw_score * dimensional_scores.resentment.salience) + (dimensional_scores.fear.raw_score * dimensional_scores.fear.salience) + (dimensional_scores.fantasy.raw_score * dimensional_scores.fantasy.salience))"
  
  # Final Salience-Weighted Civic Character Index
  - name: "civic_character_index"
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
