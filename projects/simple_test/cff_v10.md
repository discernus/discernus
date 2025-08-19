# Cohesive Flourishing Framework (CFF) v10.0

---

## Part 1: The Scholarly Document

### Section 1: Abstract & *Raison d'être*

**What is this framework?**
The Cohesive Flourishing Framework (CFF) is a comprehensive tool for analyzing political and social discourse to understand its impact on community cohesion and democratic health. It moves beyond simple sentiment analysis to reveal sophisticated patterns in how language builds or undermines social solidarity, trust, and constructive civic engagement.

**What problem does it solve?**
CFF addresses a critical gap in discourse analysis by providing a methodology that preserves complex rhetorical information. Traditional analysis often forces artificial choices (e.g., a text is "hopeful" or "fearful"), losing nuance when sophisticated communication employs competing appeals simultaneously. CFF's independent scoring of opposing dimensions (e.g., Hope vs. Fear) captures this complexity, enabling a more accurate and insightful analysis of rhetorical strategy.

**Who is it for?**
This framework is designed for researchers, policymakers, and civic leaders who need to understand whether discourse contributes to social flourishing or fragmentation. It is applicable to political communication, community health assessment, and media impact evaluation.

### Section 2: Theoretical & Empirical Foundations

The CFF is grounded in a multi-disciplinary body of research from social psychology, political communication, and conflict resolution theory. Its core innovation—the independent scoring of opposing conceptual anchors—is a direct response to the information loss problem observed in traditional valence-based content analysis.

-   **Social Psychology**: The framework's dimensions are informed by research on in-group/out-group dynamics, threat perception, and social identity theory.
-   **Political Communication**: The methodology leverages insights into rhetorical strategies that build or undermine democratic engagement and social capital. (See, for example, the work of K. H. Jamieson on political rhetoric).
-   **Empirical Justification for Salience**: The use of salience-weighting is empirically grounded. A meta-analysis of 10 comprehensive studies demonstrated that static, predetermined weights for analytical dimensions have zero empirical support, whereas weighting based on the speaker's actual rhetorical emphasis provides a defensible and context-aware methodology.

### Section 3: Analytical Methodology

CFF employs a multi-layered analytical approach.

-   **Dimensions**: The framework scores ten conceptual anchors independently on a 0.0 to 1.0 scale, organized into five opposing pairs:
    -   **Identity**: Tribal Dominance vs. Individual Dignity
    -   **Emotional Climate**: Fear vs. Hope
    -   **Success Orientation**: Envy vs. Compersion
    -   **Relational Climate**: Enmity vs. Amity
    -   **Goal Orientation**: Fragmentative Goals vs. Cohesive Goals

-   **Advanced Concepts**:
    -   **Salience vs. Intensity**: A critical distinction is made between a dimension's *intensity* (its raw 0.0-1.0 score) and its *salience* (its rhetorical prominence or emphasis within the text, also scored 0.0-1.0). This dual-track analysis reveals not just *what* is being said, but *how much emphasis* it receives.
    -   **Rhetorical Tension**: The framework calculates the strategic tension between opposing pairs to measure the coherence of the discourse. The formula `Tension = min(Score_A, Score_B) × |Salience_A - Salience_B|` quantifies contradictions where a speaker employs competing appeals.

-   **Derived & Composite Metrics**:
    -   **Tension Indices**: Each dimensional pair has a tension score. The average of these is the **Strategic Contradiction Index**, which measures overall rhetorical coherence.
    -   **Salience-Weighted Cohesion Index**: A comprehensive index that measures the discourse's contribution to social cohesion. It is calculated by weighting each dimension's score by its salience, providing an empirically defensible measure of the text's overall impact.

### Section 4: Intended Application & Corpus Fit

-   **Target Corpus Description**: CFF is designed for the analysis of persuasive or strategic communication, particularly in the political and social spheres. This includes political speeches, campaign materials, policy documents, and organizational communications.
-   **Known Limitations & Scope**: The framework is less suited for analyzing purely informational, conversational, or fictional texts. The complexity of the salience and tension assessments requires a text with sufficient length and rhetorical structure to be meaningful.
-   **System Validation Note**: Be aware that the Discernus platform will perform a post-hoc statistical analysis of your framework's fit with your chosen corpus based on the variance in the results. A low framework-corpus fit score may indicate that the framework was misapplied and could impact the interpretation of the results.

---

## Part 2: The Machine-Readable Appendix

```yaml
# --- Start of Machine-Readable Appendix ---

# 5.1: Metadata
metadata:
  framework_name: "cohesive_flourishing_framework"
  framework_version: "10.0.0"
  author: "Discernus Project"
  spec_version: "10.0"

# 5.2: Analysis Variants
analysis_variants:
  default:
    description: "Complete v10.0 implementation with salience and tension analysis."
    analysis_prompt: |
      You are an expert discourse analyst specializing in social cohesion and democratic health, grounded in political psychology. Your task is to analyze the provided text using the Cohesive Flourishing Framework v10.0.

      You must evaluate 10 dimensions across 5 opposing pairs:
      - Identity: Tribal Dominance vs. Individual Dignity
      - Emotional Climate: Fear vs. Hope
      - Success Orientation: Envy vs. Compersion
      - Relational Climate: Enmity vs. Amity
      - Goal Orientation: Fragmentative Goals vs. Cohesive Goals

      CRITICAL: For EACH of the 10 dimensions, you must provide:
      1.  A `raw_score` (0.0-1.0) for its intensity.
      2.  A `salience` score (0.0-1.0) for its rhetorical prominence and emphasis. REMEMBER: Salience is NOT the same as intensity.
      3.  A direct quote as `evidence`.

      IMPORTANT DISTINCTION: "Compersion" measures joy from others' success (distinct from "compassion" which is empathy for suffering). Use the exact dimension names as specified - do not substitute similar concepts.
      4.  Your `confidence` in the assessment (0.0-1.0).

# 5.3: Dimensions
dimensions:
  - { name: "tribal_dominance", description: "In-group supremacy and exclusionary identity patterns." }
  - { name: "individual_dignity", description: "Universal human worth and inclusive recognition." }
  - { name: "fear", description: "Crisis mentality and existential threat perception." }
  - { name: "hope", description: "Progress orientation and optimistic collective vision." }
  - { name: "envy", description: "Resentment toward others' success, zero-sum thinking." }
  - { name: "compersion", description: "Compersion: the joy derived from others' success and achievements. This is distinct from compassion (empathy for suffering) - compersion specifically measures positive emotional responses to others' prosperity, accomplishments, and good fortune. Reflects abundance mindset and non-zero-sum thinking." }
  - { name: "enmity", description: "Hostility and adversarial positioning." }
  - { name: "amity", description: "Friendship appeals and cooperative framing." }
  - { name: "fragmentative_goals", description: "Divisive zero-sum objectives." }
  - { name: "cohesive_goals", description: "Integrative positive-sum objectives." }

# 5.4: Derived Metrics
derived_metrics:
  - name: "identity_tension"
    formula: "min(dimensional_scores.tribal_dominance.raw_score, dimensional_scores.individual_dignity.raw_score) * abs(dimensional_scores.tribal_dominance.salience - dimensional_scores.individual_dignity.salience)"
  - name: "emotional_tension"
    formula: "min(dimensional_scores.fear.raw_score, dimensional_scores.hope.raw_score) * abs(dimensional_scores.fear.salience - dimensional_scores.hope.salience)"
  - name: "success_tension"
    formula: "min(dimensional_scores.envy.raw_score, dimensional_scores.compersion.raw_score) * abs(dimensional_scores.envy.salience - dimensional_scores.compersion.salience)"
  - name: "relational_tension"
    formula: "min(dimensional_scores.enmity.raw_score, dimensional_scores.amity.raw_score) * abs(dimensional_scores.enmity.salience - dimensional_scores.amity.salience)"
  - name: "goal_tension"
    formula: "min(dimensional_scores.fragmentative_goals.raw_score, dimensional_scores.cohesive_goals.raw_score) * abs(dimensional_scores.fragmentative_goals.salience - dimensional_scores.cohesive_goals.salience)"
  - name: "strategic_contradiction_index"
    formula: "(derived_metrics.identity_tension + derived_metrics.emotional_tension + derived_metrics.success_tension + derived_metrics.relational_tension + derived_metrics.goal_tension) / 5"

# 5.5: Output Schema
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
        compersion: { $ref: "#/definitions/score_object" }
        enmity: { $ref: "#/definitions/score_object" }
        amity: { $ref: "#/definitions/score_object" }
        fragmentative_goals: { $ref: "#/definitions/score_object" }
        cohesive_goals: { $ref: "#/definitions/score_object" }
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
```
