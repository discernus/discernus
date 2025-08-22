# Entman Framing Functions Framework v10.0

**Version**: v10.0  
**Status**: Active  
**Framework Type**: Communication Analysis  
**Domain**: Strategic Communication, Political Discourse, Media Studies

---

## Abstract & Raison d'Être

The Entman Framing Functions Framework v10.0 implements Robert Entman's foundational communication theory through systematic analysis of four independent framing functions. This framework tests Entman's core hypothesis that strategic communication operates through distinct, independently variable framing functions that can be deployed separately to achieve communication goals. By analyzing Problem Definition, Causal Attribution, Moral Evaluation, and Treatment Recommendation as independent dimensions, this framework reveals the systematic construction of persuasive messages and enables empirical testing of framing theory's independence hypothesis.

**Core Innovation**: Systematic communication analysis that treats framing functions as independent analytical dimensions rather than correlated message elements, enabling precise measurement of strategic communication patterns and message construction sophistication.

It is designed for political scientists, communication scholars, media analysts, and researchers studying strategic communication, framing theory, and political discourse analysis.

---

## Theoretical & Empirical Foundations

### **Entman's Framing Theory (1993, 2007)**

Robert Entman's seminal work established that framing operates through four distinct functions that can vary independently:

1. **Problem Definition**: Establishes what issues require attention and how problems are conceptualized
2. **Causal Attribution**: Assigns responsibility and explains problem origins  
3. **Moral Evaluation**: Provides ethical framework and value judgments
4. **Treatment Recommendation**: Advocates specific solutions and policy directions

### **Independence Hypothesis**

Entman's theory predicts these functions operate as independent analytical dimensions that can vary separately without necessary correlation. A communication may emphasize problem definition without moral evaluation, or propose solutions without extensive causal attribution. This independence enables strategic communication flexibility and message tailoring.

### **Academic Validation**

- **Entman, R. M. (1993).** Framing: Toward clarification of a fractured paradigm. *Journal of Communication, 43*(4), 51-58.
- **Entman, R. M. (2007).** Framing bias: Media in the distribution of power. *Journal of Communication, 57*(1), 163-173.
- **Chong, D., & Druckman, J. N. (2007).** Framing theory. *Annual Review of Political Science, 10*, 103-126.
- **Chong, D., & Druckman, J. N. (2007).** Framing public opinion in competitive democracies. *American Political Science Review, 101*(4), 637-655.

---

## Analytical Methodology

### **Four-Domain Architecture**

The framework analyzes discourse across four independent framing functions, each scored on a 0.0-1.0 scale:

1. **Problem Definition**: Issue identification, crisis framing, scope setting
2. **Causal Attribution**: Responsibility assignment, blame attribution, causal explanation  
3. **Moral Evaluation**: Value invocation, moral judgment, ethical framework
4. **Treatment Recommendation**: Solution advocacy, policy options, action imperatives

### **Dual-Track Analysis**

- **Function Intensity (0.0-1.0)**: Traditional strength measurement of each framing function
- **Salience Assessment (0.0-1.0)**: Rhetorical emphasis and strategic prominence of each function

### **Independence Testing**

The framework empirically tests Entman's independence hypothesis by measuring whether framing functions correlate or vary independently, revealing systematic vs. ad hoc message construction.

### **Strategic Pattern Recognition**

Identifies communication profiles based on which framing functions receive emphasis, enabling classification of strategic communication approaches and message construction sophistication.

### **Derived & Composite Metrics**

The framework generates five key derived metrics to quantify strategic communication patterns:

1. **Message Completeness Index**: Average coverage across all four framing functions, measuring how comprehensively the text addresses the complete framing spectrum.

2. **Framing Coherence Index**: Geometric mean of framing function scores, measuring internal consistency and balanced deployment across all functions.

3. **Salience-Weighted Message Completeness**: Message completeness weighted by strategic emphasis, revealing coverage of strategically important functions.

4. **Strategic Framing Profile**: Classification of primary communication approach (0=Problem-focused, 1=Cause-focused, 2=Values-focused, 3=Solution-focused).

5. **Framing Independence Score**: Standard deviation of framing function scores, measuring empirical independence as predicted by Entman's theory.

---

## Intended Application & Corpus Fit

### **Primary Applications**
- **Political communication analysis** - Campaign messaging, policy advocacy, public statements
- **Media framing studies** - News coverage, editorial content, public discourse
- **Strategic communication evaluation** - Corporate messaging, organizational communication
- **Academic research** - Framing theory validation, communication pattern analysis

### **Corpus Requirements**
- **Sufficient length** to assess multiple framing functions across dimensions
- **Strategic communication content** where framing functions are likely deployed
- **Clear speaker intent** to construct persuasive or explanatory messages
- **Diverse framing opportunities** to test independence hypothesis

**System Validation Note**: The Discernus platform will perform a post-hoc statistical analysis to measure the framework's fit with the chosen corpus. This framework-corpus fit score is a key indicator of the research design's validity and will be provided in the final analysis results.

### **Known Limitations & Scope**

This framework is specifically designed for strategic communication analysis and has clear boundaries of applicability. It is **unsuitable for**:
- **Non-strategic texts**: Personal correspondence, technical documentation, or purely descriptive content where framing functions are not intentionally deployed
- **Short-form content**: Brief statements, tweets, or headlines that lack sufficient length to assess multiple framing functions
- **Non-persuasive discourse**: Factual reporting, academic writing, or neutral informational content without strategic intent
- **Non-verbal communication**: Visual media, audio content, or other non-textual forms where linguistic framing markers cannot be identified

**Potential pitfalls** include over-interpreting framing patterns in texts where they are minimal or absent, and misattributing strategic intent to naturally occurring language patterns. The framework should be applied with awareness of the speaker's communicative context and intent.

---

## Machine-Readable Framework Specification

--- Start of Machine-Readable Appendix ---

```yaml
metadata:
  framework_name: "entman_framing_functions"
  framework_version: "10.0.0"
  spec_version: "10.0"
  author: "Robert Entman, adapted by Discernus Research Team"

analysis_variants:
  default:
    description: "Complete four-function framing analysis with independence testing"
    analysis_prompt: |
      You are an expert analyst specializing in communication framing and strategic messaging. Analyze this text using the Entman Framing Functions Framework v10.0, which examines four independent framing functions based on Robert Entman's foundational communication theory.

        **FRAMING FUNCTIONS TO ANALYZE:**

        1. **Problem Definition** (0.0-1.0): What issues are identified as requiring attention and how problems are conceptualized. Look for: issue identification ('the real issue is,' 'we face a crisis of,' 'the challenge before us'), crisis framing ('urgent need,' 'what's really at stake'), scope setting ('affects everyone,' 'widespread implications').

        2. **Causal Attribution** (0.0-1.0): What factors or actors are presented as causing problems and how responsibility is assigned. Look for: responsibility language ('X is responsible for,' 'this stems from Y's actions'), blame attribution ('the fault lies with,' 'caused by'), causal explanation ('due to,' 'resulted from,' 'roots of this problem').

        3. **Moral Evaluation** (0.0-1.0): What values and moral judgments are invoked and how actions are evaluated ethically. Look for: value language ('justice demands,' 'fairness requires,' 'liberty is at stake'), moral judgment ('right thing,' 'wrong approach,' 'ethical'), values framework ('core values,' 'moral foundation,' 'ethical standards').

        4. **Treatment Recommendation** (0.0-1.0): What solutions are proposed and how policy options are presented and prioritized. Look for: solution language ('we must,' 'need to,' 'the answer is'), policy options ('I propose,' 'recommend,' 'plan to'), action imperative ('take action,' 'immediate steps,' 'decisive action').

        Analyze each framing function independently, scoring from 0.0-1.0 based on evidence strength and frequency, assessing salience (0.0-1.0) for strategic prominence, and providing specific quotations as evidence. Evaluate whether functions operate independently as predicted by Entman's theory and identify strategic communication patterns.

  sequential_analysis:
    description: "Step-by-step analysis of each framing function before integration"
    analysis_prompt: |
      You are an expert communication analyst. Analyze this text through focused sequential steps, examining each framing function independently before integration.

      **ANALYSIS APPROACH:**
      Focus on each framing function sequentially, examining problem definition, causal attribution, moral evaluation, and treatment recommendation patterns independently. For each function, assess evidence strength, score from 0.0-1.0, evaluate salience (0.0-1.0) for strategic prominence, and provide specific textual evidence. After individual analysis, integrate findings to assess framing function independence and strategic communication patterns.

  strategic_focus:
    description: "Analysis focused on strategic communication patterns and message construction"
    analysis_prompt: |
      You are an expert in strategic communication and framing theory. Analyze this text using the Entman Framing Functions Framework v10.0 with emphasis on strategic communication patterns.

      **STRATEGIC ANALYSIS FOCUS:**
      Examine which framing functions receive the most rhetorical investment, how the four functions work together or independently to construct the message, what strategic communication approach is revealed through framing function deployment, and how sophisticated the message construction is (systematic vs. ad hoc).

      **FRAMING FUNCTION ASSESSMENT:**
      For each of the four functions (Problem Definition, Causal Attribution, Moral Evaluation, Treatment Recommendation), score intensity (0.0-1.0) based on evidence strength, assess salience (0.0-1.0) for strategic prominence, provide key evidence quotations, and analyze strategic deployment patterns.

dimensions:
  - name: "problem_definition"
    display_name: "Problem Definition"
    description: "What issues are identified as requiring attention and how problems are conceptualized"
    markers:
      positive_examples:
        - phrase: "the real issue is"
          explanation: "Direct problem identification with clear issue framing"
        - phrase: "we face a crisis of"
          explanation: "Crisis framing that establishes urgency and scope"
        - phrase: "the challenge before us"
          explanation: "Problem conceptualization as collective challenge"
        - phrase: "the problem we must address"
          explanation: "Explicit problem identification with action imperative"
        - phrase: "what's really at stake"
          explanation: "Stakes clarification that frames problem importance"
      negative_examples:
        - phrase: "everything is fine"
          explanation: "Denial of problems or issues requiring attention"
        - phrase: "no challenges here"
          explanation: "Explicit rejection of problem framing"
        - phrase: "business as usual"
          explanation: "Status quo framing that ignores problems"
      boundary_cases:
        - phrase: "potential issues"
          explanation: "Assess whether this represents problem identification or hedging"
        - phrase: "some concerns"
          explanation: "Evaluate if this constitutes problem definition or minimization"
    disambiguation:
      overlap_with_causal_attribution: "When both problem and cause language appear, focus on whether the text is identifying what needs attention (problem definition) vs. explaining why it happened (causal attribution). Problem definition establishes scope, causal attribution assigns responsibility."
      overlap_with_treatment_recommendation: "Distinguish between identifying what needs attention (problem definition) vs. proposing how to address it (treatment recommendation). Problem definition sets the stage, treatment recommendation provides solutions."
    scoring_calibration:
      high: "0.7-1.0: Clear problem identification with specific issue framing and scope setting"
      medium: "0.4-0.6: Moderate problem emphasis with general issue language"
      low: "0.1-0.3: Minimal problem identification or vague issue framing"
      absent: "0.0: No problem definition language or issue identification"

  - name: "causal_attribution"
    display_name: "Causal Attribution"
    description: "What factors or actors are presented as causing problems and how responsibility is assigned"
    markers:
      positive_examples:
        - phrase: "X is responsible for"
          explanation: "Direct responsibility assignment to specific actors"
        - phrase: "this stems from Y's actions"
          explanation: "Causal connection between actions and outcomes"
        - phrase: "the fault lies with"
          explanation: "Explicit blame attribution and fault assignment"
        - phrase: "caused by"
          explanation: "Direct causal relationship identification"
        - phrase: "the roots of this problem"
          explanation: "Structural or fundamental cause identification"
      negative_examples:
        - phrase: "no one is to blame"
          explanation: "Explicit rejection of responsibility assignment"
        - phrase: "accidents happen"
          explanation: "Attribution to chance rather than actors or factors"
        - phrase: "unforeseen circumstances"
          explanation: "External factors beyond human control"
      boundary_cases:
        - phrase: "may have contributed"
          explanation: "Assess whether this represents causal attribution or hedging"
        - phrase: "could be related to"
          explanation: "Evaluate if this constitutes causal explanation or speculation"
    disambiguation:
      overlap_with_problem_definition: "Distinguish between identifying what needs attention (problem definition) vs. explaining why it happened (causal attribution). Problem definition establishes scope, causal attribution assigns responsibility."
      overlap_with_moral_evaluation: "Separate causal explanation (what happened) from moral judgment (whether it was right/wrong). Causal attribution focuses on responsibility, moral evaluation focuses on ethical assessment."
    scoring_calibration:
      high: "0.7-1.0: Clear responsibility assignment with specific causal explanations and actor identification"
      medium: "0.4-0.6: Moderate causal attribution with general responsibility language"
      low: "0.1-0.3: Minimal causal explanation or vague responsibility assignment"
      absent: "0.0: No causal attribution or responsibility assignment language"

  - name: "moral_evaluation"
    display_name: "Moral Evaluation"
    description: "What values and moral judgments are invoked and how actions are evaluated ethically"
    markers:
      positive_examples:
        - phrase: "justice demands"
          explanation: "Moral imperative based on justice principles"
        - phrase: "fairness requires"
          explanation: "Ethical obligation grounded in fairness"
        - phrase: "liberty is at stake"
          explanation: "Value-based assessment of what's threatened"
        - phrase: "fundamental rights"
          explanation: "Core value identification and protection"
        - phrase: "moral imperative"
          explanation: "Explicit ethical obligation language"
      negative_examples:
        - phrase: "morally neutral"
          explanation: "Explicit rejection of moral evaluation"
        - phrase: "no ethical concerns"
          explanation: "Denial of moral dimensions"
        - phrase: "purely practical"
          explanation: "Framing as non-ethical, technical matter"
      boundary_cases:
        - phrase: "questionable practices"
          explanation: "Assess whether this represents moral evaluation or hedging"
        - phrase: "concerning behavior"
          explanation: "Evaluate if this constitutes moral judgment or observation"
    disambiguation:
      overlap_with_causal_attribution: "Separate causal explanation (what happened) from moral judgment (whether it was right/wrong). Causal attribution focuses on responsibility, moral evaluation focuses on ethical assessment."
      overlap_with_treatment_recommendation: "Distinguish between moral evaluation (what's right/wrong) and solution advocacy (what should be done). Moral evaluation provides ethical framework, treatment recommendation provides action guidance."
    scoring_calibration:
      high: "0.7-1.0: Strong moral framework with clear value judgments and ethical positioning"
      medium: "0.4-0.6: Moderate moral evaluation with general value language"
      low: "0.1-0.3: Minimal moral judgment or vague ethical language"
      absent: "0.0: No moral evaluation or value judgment language"

  - name: "treatment_recommendation"
    display_name: "Treatment Recommendation"
    description: "What solutions are proposed and how policy options are presented and prioritized"
    markers:
      positive_examples:
        - phrase: "we must immediately"
          explanation: "Strong action imperative with urgency"
        - phrase: "the answer is"
          explanation: "Direct solution identification and advocacy"
        - phrase: "the only way forward"
          explanation: "Solution presentation as necessary path"
        - phrase: "solution requires"
          explanation: "Explicit solution advocacy language"
        - phrase: "concrete measures"
          explanation: "Specific, actionable solution proposals"
      negative_examples:
        - phrase: "no easy answers"
          explanation: "Explicit rejection of solution availability"
        - phrase: "unsolvable problem"
          explanation: "Denial of solution possibility"
        - phrase: "beyond our control"
          explanation: "Framing as unsolvable external issue"
      boundary_cases:
        - phrase: "might help"
          explanation: "Assess whether this represents solution advocacy or hedging"
        - phrase: "could consider"
          explanation: "Evaluate if this constitutes treatment recommendation or suggestion"
    disambiguation:
      overlap_with_problem_definition: "Distinguish between identifying what needs attention (problem definition) vs. proposing how to address it (treatment recommendation). Problem definition sets the stage, treatment recommendation provides solutions."
      overlap_with_moral_evaluation: "Distinguish between moral evaluation (what's right/wrong) and solution advocacy (what should be done). Moral evaluation provides ethical framework, treatment recommendation provides action guidance."
    scoring_calibration:
      high: "0.7-1.0: Clear solution advocacy with specific policy proposals and action imperatives"
      medium: "0.4-0.6: Moderate treatment recommendation with general solution language"
      low: "0.1-0.3: Minimal solution advocacy or vague treatment language"
      absent: "0.0: No treatment recommendation or solution proposal language"

derived_metrics:
  - name: "message_completeness_index"
    description: "Measures how comprehensively the text covers all four framing functions"
    formula: "(dimensions.problem_definition.raw_score + dimensions.causal_attribution.raw_score + dimensions.moral_evaluation.raw_score + dimensions.treatment_recommendation.raw_score) / 4"
    interpretation: "Higher values indicate more comprehensive message construction covering all framing functions. Lower values suggest selective or incomplete framing deployment."

  - name: "framing_coherence_index"
    description: "Measures the internal consistency of framing function deployment"
    formula: "(dimensions.problem_definition.raw_score * dimensions.causal_attribution.raw_score * dimensions.moral_evaluation.raw_score * dimensions.treatment_recommendation.raw_score) ** 0.25"
    interpretation: "Higher values indicate balanced deployment across all functions. Lower values suggest uneven or lopsided framing emphasis."

  - name: "salience_weighted_message_completeness"
    description: "Message completeness weighted by the strategic prominence of each framing function"
    formula: "(dimensions.problem_definition.raw_score * dimensions.problem_definition.salience + dimensions.causal_attribution.raw_score * dimensions.causal_attribution.salience + dimensions.moral_evaluation.raw_score * dimensions.moral_evaluation.salience + dimensions.treatment_recommendation.raw_score * dimensions.treatment_recommendation.salience) / (dimensions.problem_definition.salience + dimensions.causal_attribution.salience + dimensions.moral_evaluation.salience + dimensions.treatment_recommendation.salience + 0.001)"
    interpretation: "Measures message completeness while accounting for which functions receive strategic emphasis. Higher values indicate comprehensive coverage of strategically important functions."

  - name: "strategic_framing_profile"
    description: "Classifies the strategic communication approach based on framing function emphasis patterns"
    formula: "np.argmax([dimensions.problem_definition.salience, dimensions.causal_attribution.salience, dimensions.moral_evaluation.salience, dimensions.treatment_recommendation.salience])"
    interpretation: "Identifies which framing function receives the most strategic emphasis, revealing the speaker's primary communication approach: 0=Problem-focused, 1=Cause-focused, 2=Values-focused, 3=Solution-focused."

  - name: "framing_independence_score"
    description: "Measures the empirical independence of framing functions as predicted by Entman's theory"
    formula: "np.std([dimensions.problem_definition.raw_score, dimensions.causal_attribution.raw_score, dimensions.moral_evaluation.raw_score, dimensions.treatment_recommendation.raw_score])"
    interpretation: "Higher values indicate framing functions vary independently as predicted by theory. Lower values suggest functions are deployed in correlated patterns."

output_schema:
  type: object
  required: ["dimensional_scores", "derived_metrics"]
  definitions:
    score_object:
      type: object
      required: ["raw_score", "salience", "confidence", "evidence"]
      properties:
        raw_score:
          type: number
          minimum: 0.0
          maximum: 1.0
          description: "Framing function strength (0.0-1.0)"
        salience:
          type: number
          minimum: 0.0
          maximum: 1.0
          description: "Strategic prominence of the framing function (0.0-1.0)"
        confidence:
          type: number
          minimum: 0.0
          maximum: 1.0
          description: "Analyst confidence in assessment (0.0-1.0)"
        evidence:
          type: string
          description: "Textual evidence supporting the assessment"
  properties:
    dimensional_scores:
      type: object
      required: ["problem_definition", "causal_attribution", "moral_evaluation", "treatment_recommendation"]
      properties:
        problem_definition:
          $ref: "#/definitions/score_object"
        causal_attribution:
          $ref: "#/definitions/score_object"
        moral_evaluation:
          $ref: "#/definitions/score_object"
        treatment_recommendation:
          $ref: "#/definitions/score_object"
    derived_metrics:
      type: object
      required: ["message_completeness_index", "framing_coherence_index", "salience_weighted_message_completeness", "strategic_framing_profile", "framing_independence_score"]
      properties:
        message_completeness_index:
          type: number
          minimum: 0.0
          maximum: 1.0
          description: "Average coverage across all four framing functions"
        framing_coherence_index:
          type: number
          minimum: 0.0
          maximum: 1.0
          description: "Geometric mean of framing function scores"
        salience_weighted_message_completeness:
          type: number
          minimum: 0.0
          maximum: 1.0
          description: "Message completeness weighted by strategic emphasis"
        strategic_framing_profile:
          type: integer
          minimum: 0
          maximum: 3
          description: "Primary framing function emphasis: 0=Problem, 1=Cause, 2=Values, 3=Solution"
        framing_independence_score:
          type: number
          minimum: 0.0
          maximum: 1.0
          description: "Empirical independence of framing functions"

--- End of Machine-Readable Appendix ---
