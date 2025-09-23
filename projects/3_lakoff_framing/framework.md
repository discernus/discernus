# Lakoff Framing Framework v10.0

**Version**: 10.0.0  
**Status**: Active  
**Framework Type**: Cognitive Linguistics Analysis  
**Domain**: Political Psychology, Cognitive Linguistics, Moral Politics

---

## Abstract & Raison d'Être

The Lakoff Framing Framework v10.0 implements George Lakoff's groundbreaking "Moral Politics" theory through systematic analysis of family-based moral systems in political communication. This framework tests Lakoff's core hypothesis that political worldviews stem from consistent family models that generate predictable positions across issues. By analyzing three bipolar dimensions (Authority vs Empathy, Competition vs Cooperation, Self-Reliance vs Interdependence), this framework reveals how Strict Father and Nurturant Parent moral systems manifest in political discourse and enables empirical testing of family model coherence.

**Core Innovation**: Cognitive linguistics analysis that treats family moral systems as unconscious models for political thinking, enabling precise measurement of moral framework deployment and strategic communication patterns.

It is designed for cognitive linguists, political psychologists, communication scholars, and researchers studying moral politics, family model theory, and political discourse analysis.

---

## Theoretical & Empirical Foundations

### **Lakoff's Family Model Theory (1996, 2002)**

George Lakoff's seminal work "Moral Politics" established that political worldviews stem from two fundamental family models that shape moral reasoning:

1. **Strict Father Model**: Emphasizes moral authority, competitive achievement, and individual responsibility
2. **Nurturant Parent Model**: Emphasizes empathetic care, cooperative support, and collective responsibility

### **Family Model Coherence Hypothesis**

Lakoff's theory predicts that political communications should cluster around coherent family models, with Strict Father components appearing together and competing with Nurturant Parent components. This coherence enables cross-issue prediction and reveals strategic messaging patterns.

### **Cognitive Linguistics Foundation**

Politics operates as an extension of family moral systems, where metaphorical family structures determine political positions across diverse policy domains. Family models serve as unconscious cognitive frameworks that organize moral reasoning.

### **Academic Validation**

- **Lakoff, G. (1996).** Moral Politics: How Liberals and Conservatives Think. *University of Chicago Press*.
- **Lakoff, G. (2002).** Moral Politics: How Liberals and Conservatives Think (2nd ed.). *University of Chicago Press*.
- **Lakoff, G. (2004).** Don't Think of an Elephant: Know Your Values and Frame the Debate. *Chelsea Green Publishing*.
- **Lakoff, G., & Johnson, M. (1980).** Metaphors We Live By. *University of Chicago Press*.

---

## Analytical Methodology

### **Three-Domain Bipolar Architecture**

The framework analyzes discourse across three bipolar dimensions, each scored on a 0.0-1.0 scale where 1.0 represents Strict Father orientation and 0.0 represents Nurturant Parent orientation:

1. **Authority vs Empathy**: Moral authority and hierarchical decision-making vs empathetic understanding and inclusive dialogue
2. **Competition vs Cooperation**: Natural hierarchy and merit-based competition vs egalitarian cooperation and mutual support
3. **Self-Reliance vs Interdependence**: Individual responsibility and self-determination vs collective responsibility and social connection

### **Dual-Track Analysis**

- **Family Model Intensity (0.0-1.0)**: Traditional bipolar scoring from Nurturant Parent (0.0) to Strict Father (1.0)
- **Salience Assessment (0.0-1.0)**: Rhetorical emphasis and strategic prominence of each dimension

### **Coherence Testing**

The framework empirically tests Lakoff's coherence hypothesis by measuring whether family model components cluster as predicted, revealing systematic vs. ad hoc moral framework deployment.

### **Strategic Pattern Recognition**

Identifies communication profiles based on which family model dimensions receive emphasis, enabling classification of moral political approaches and strategic messaging sophistication.

---

## Intended Application & Corpus Fit

### **Primary Applications**
- **Political communication analysis** - Campaign messaging, policy advocacy, public statements
- **Cognitive linguistics research** - Family model theory validation, moral framework analysis
- **Political psychology studies** - Moral reasoning patterns, voter response analysis
- **Strategic communication evaluation** - Message coherence assessment, audience targeting

### **Corpus Requirements**
- **Sufficient length** to assess multiple family model dimensions across moral contexts
- **Political or social discourse** where family model frameworks are likely deployed
- **Clear speaker intent** to construct persuasive or explanatory messages
- **Diverse moral contexts** to test family model coherence hypothesis

**System Validation Note**: The Discernus platform will perform a post-hoc statistical analysis to measure the framework's fit with the chosen corpus. This framework-corpus fit score is a key indicator of the research design's validity and will be provided in the final analysis results.

### **Known Limitations & Scope**

This framework is specifically designed for family model moral analysis and has clear boundaries of applicability. It is **unsuitable for**:
- **Non-moral discourse**: Technical documentation, factual reporting, or neutral informational content where moral frameworks are not deployed
- **Non-family contexts**: Professional, institutional, or abstract communication that doesn't invoke family-based moral reasoning
- **Cultural variations**: Family model expressions that differ significantly from Western nuclear family structures
- **Non-political content**: Personal correspondence, creative writing, or other forms where political moral frameworks are irrelevant

**Potential pitfalls** include over-interpreting family model patterns in texts where they are minimal or absent, and misattributing strategic intent to naturally occurring family-based language patterns. The framework should be applied with awareness of the speaker's cultural and communicative context.

---

## Machine-Readable Framework Specification

--- Start of Machine-Readable Appendix ---

```yaml
metadata:
  framework_name: "lakoff_framing_framework"
  framework_version: "10.0.0"
  spec_version: "10.0"
  author: "George Lakoff, adapted by Discernus Research Team"

analysis_variants:
  default:
    description: "Complete family model analysis with coherence testing"
    analysis_prompt: |
      You are an expert in cognitive linguistics and political psychology, specializing in George Lakoff's family model theory. Analyze this text using the Lakoff Framing Framework v10.0, which examines three bipolar dimensions based on Lakoff's "Moral Politics" theory.

      **FRAMEWORK METHODOLOGY:**
      Score each dimension independently from 0.0-1.0 based on evidence strength (0.0 = Nurturant Parent, 1.0 = Strict Father), assess salience (0.0-1.0) for strategic prominence, and provide specific quotations as evidence.

      **FAMILY MODEL DIMENSIONS:**
      1. **Authority vs Empathy** (0.0-1.0): Moral authority and hierarchical decision-making vs empathetic understanding and inclusive dialogue
      2. **Competition vs Cooperation** (0.0-1.0): Natural hierarchy and merit-based competition vs egalitarian cooperation and mutual support  
      3. **Self-Reliance vs Interdependence** (0.0-1.0): Individual responsibility and self-determination vs collective responsibility and social connection

      **EVIDENCE STANDARDS:**
      Provide specific textual quotations supporting each dimension score and salience assessment. Evaluate whether family model components cluster as predicted by Lakoff's coherence hypothesis and identify strategic moral framework deployment.

  sequential_analysis:
    description: "Step-by-step analysis of each family model dimension before integration"
    analysis_prompt: |
      You are an expert cognitive linguist specializing in family model theory. Analyze this text through focused sequential steps, examining each family model dimension independently before integration.

      **FRAMEWORK METHODOLOGY:**
      Score each dimension independently from 0.0-1.0 based on evidence strength (0.0 = Nurturant Parent, 1.0 = Strict Father), assess salience (0.0-1.0) for strategic prominence, and provide specific textual evidence.

      **SEQUENTIAL ANALYSIS APPROACH:**
      Examine authority vs empathy, competition vs cooperation, and self-reliance vs interdependence patterns sequentially. For each dimension, complete full analysis before moving to the next.

      **INTEGRATION REQUIREMENTS:**
      After individual analysis, integrate findings to assess family model coherence and strategic moral framework patterns.

  moral_framework_focus:
    description: "Analysis focused on moral framework coherence and strategic deployment"
    analysis_prompt: |
      You are an expert in moral politics and family model theory. Analyze this text using the Lakoff Framing Framework v10.0 with emphasis on moral framework coherence and strategic deployment.

      **FRAMEWORK METHODOLOGY:**
      Score each dimension independently from 0.0-1.0 based on evidence strength (0.0 = Nurturant Parent, 1.0 = Strict Father), assess salience (0.0-1.0) for strategic prominence, and provide specific textual evidence.

      **MORAL FRAMEWORK ANALYSIS FOCUS:**
      Examine which family model dimensions receive the most rhetorical investment, how the three dimensions work together or independently to construct moral frameworks, what strategic moral approach is revealed through family model deployment, and how sophisticated the moral framework construction is (coherent vs. contradictory).

      **STRATEGIC ASSESSMENT REQUIREMENTS:**
      Analyze strategic deployment patterns and identify whether the moral framework construction is coherent or contradictory.

dimensions:
  - name: "authority_vs_empathy"
    description: "Moral authority and hierarchical decision-making vs empathetic understanding and inclusive dialogue"
    markers:
      positive_examples:
        - phrase: "strong leadership"
          explanation: "Emphasizes hierarchical authority and decisive decision-making"
        - phrase: "moral authority"
          explanation: "Establishes clear moral hierarchy and authoritative guidance"
        - phrase: "decisive action"
          explanation: "Demonstrates authoritative decision-making without consultation"
        - phrase: "clear rules"
          explanation: "Establishes hierarchical structure with defined boundaries"
        - phrase: "take charge"
          explanation: "Emphasizes authoritative leadership and control"
      negative_examples:
        - phrase: "listen to voices"
          explanation: "Emphasizes inclusive dialogue and empathetic understanding"
        - phrase: "understand perspectives"
          explanation: "Demonstrates empathetic approach to diverse viewpoints"
        - phrase: "inclusive dialogue"
          explanation: "Emphasizes collaborative communication over authority"
        - phrase: "empathetic understanding"
          explanation: "Focuses on emotional connection and shared experience"
        - phrase: "consensus building"
          explanation: "Emphasizes collaborative decision-making over authority"
      boundary_cases:
        - phrase: "responsible leadership"
          explanation: "Assess whether this represents authority or balanced approach"
        - phrase: "guided discussion"
          explanation: "Evaluate if this constitutes authority or collaborative leadership"
    disambiguation:
      overlap_with_competition_cooperation: "Distinguish between authoritative decision-making (authority) and competitive achievement (competition). Authority focuses on hierarchical control, competition focuses on individual merit and achievement."
      overlap_with_self_reliance_interdependence: "Separate authoritative guidance (authority) from individual responsibility (self-reliance). Authority establishes external control, self-reliance emphasizes internal personal responsibility."
    scoring_calibration:
      high: "0.7-1.0: Strong Strict Father orientation with clear authority language and hierarchical decision-making"
      medium: "0.4-0.6: Moderate authority emphasis with some hierarchical language"
      low: "0.1-0.3: Minimal authority emphasis or balanced approach"
      absent: "0.0: Complete absence of Strict Father orientation; text exclusively uses Nurturant Parent framing (e.g., empathetic and inclusive language)"

  - name: "competition_vs_cooperation"
    description: "Natural hierarchy and merit-based competition vs egalitarian cooperation and mutual support"
    markers:
      positive_examples:
        - phrase: "natural hierarchy"
          explanation: "Emphasizes inherent competitive structure and merit-based selection"
        - phrase: "merit-based"
          explanation: "Focuses on individual achievement through competition"
        - phrase: "individual achievement"
          explanation: "Emphasizes personal success over collective effort"
        - phrase: "competitive advantage"
          explanation: "Highlights individual competitive positioning"
        - phrase: "winners and losers"
          explanation: "Frames success as competitive outcome"
      negative_examples:
        - phrase: "working together"
          explanation: "Emphasizes collaborative effort and shared responsibility"
        - phrase: "shared responsibility"
          explanation: "Focuses on collective accountability and mutual support"
        - phrase: "collective effort"
          explanation: "Emphasizes group collaboration over individual achievement"
        - phrase: "mutual support"
          explanation: "Highlights cooperative assistance and shared success"
        - phrase: "team effort"
          explanation: "Frames success as collaborative outcome"
      boundary_cases:
        - phrase: "excellence"
          explanation: "Assess whether this represents competitive achievement or collaborative standards"
        - phrase: "partnership"
          explanation: "Evaluate if this constitutes cooperation or strategic alliance"
    disambiguation:
      overlap_with_authority_empathy: "Distinguish between competitive achievement (competition) and authoritative control (authority). Competition focuses on individual merit, authority focuses on hierarchical decision-making."
      overlap_with_self_reliance_interdependence: "Separate individual achievement (competition) from personal responsibility (self-reliance). Competition emphasizes competitive positioning, self-reliance emphasizes personal accountability."
    scoring_calibration:
      high: "0.7-1.0: Strong Strict Father orientation with clear competition language and merit-based framing"
      medium: "0.4-0.6: Moderate competition emphasis with some merit-based language"
      low: "0.1-0.3: Minimal competition emphasis or balanced approach"
      absent: "0.0: Complete absence of Strict Father orientation; text exclusively uses Nurturant Parent framing (e.g., cooperative and collaborative language)"

  - name: "self_reliance_vs_interdependence"
    description: "Individual responsibility and self-determination vs collective responsibility and social connection"
    markers:
      positive_examples:
        - phrase: "personal responsibility"
          explanation: "Emphasizes individual accountability and self-determination"
        - phrase: "self-reliance"
          explanation: "Focuses on individual independence and personal agency"
        - phrase: "individual accountability"
          explanation: "Emphasizes personal responsibility over collective obligation"
        - phrase: "bootstrap"
          explanation: "Highlights individual effort and self-sufficiency"
        - phrase: "stand on own"
          explanation: "Emphasizes personal independence and self-determination"
      negative_examples:
        - phrase: "stronger together"
          explanation: "Emphasizes collective strength and mutual dependence"
        - phrase: "mutual dependence"
          explanation: "Focuses on social connection and collective responsibility"
        - phrase: "common good"
          explanation: "Emphasizes collective welfare over individual benefit"
        - phrase: "social fabric"
          explanation: "Highlights community bonds and social interdependence"
        - phrase: "community support"
          explanation: "Emphasizes collective assistance and mutual aid"
      boundary_cases:
        - phrase: "self-determination"
          explanation: "Assess whether this represents self-reliance or balanced autonomy"
        - phrase: "community involvement"
          explanation: "Evaluate if this constitutes interdependence or individual participation"
    disambiguation:
      overlap_with_authority_empathy: "Distinguish between personal responsibility (self-reliance) and authoritative guidance (authority). Self-reliance emphasizes internal control, authority emphasizes external hierarchical control."
      overlap_with_competition_cooperation: "Separate individual accountability (self-reliance) from competitive achievement (competition). Self-reliance emphasizes personal responsibility, competition emphasizes competitive positioning."
    scoring_calibration:
      high: "0.7-1.0: Strong Strict Father orientation with clear self-reliance language and individual responsibility"
      medium: "0.4-0.6: Moderate self-reliance emphasis with some individual responsibility language"
      low: "0.1-0.3: Minimal self-reliance emphasis or balanced approach"
      absent: "0.0: Complete absence of Strict Father orientation; text exclusively uses Nurturant Parent framing (e.g., interdependence and collective responsibility language)"

derived_metrics:
  - name: "strict_father_model_score"
    description: "Measures the overall Strict Father orientation across all three dimensions"
    formula: "(dimensions.authority_vs_empathy.raw_score + dimensions.competition_vs_cooperation.raw_score + dimensions.self_reliance_vs_interdependence.raw_score) / 3"

  - name: "family_model_coherence_index"
    description: "Measures the coherence of family model deployment as predicted by Lakoff's theory"
    formula: "(abs(dimensions.authority_vs_empathy.raw_score - 0.5) + abs(dimensions.competition_vs_cooperation.raw_score - 0.5) + abs(dimensions.self_reliance_vs_interdependence.raw_score - 0.5)) / 3"

  - name: "family_model_dominance"
    description: "Measures the balance between Strict Father and Nurturant Parent orientations"
    formula: "dimensions.authority_vs_empathy.raw_score + dimensions.competition_vs_cooperation.raw_score + dimensions.self_reliance_vs_interdependence.raw_score - 1.5"

  - name: "family_model_strategic_contradiction_index"
    description: "Measures strategic contradictions in family model deployment using tension analysis"
    formula: "((min(dimensions.authority_vs_empathy.raw_score, 1 - dimensions.authority_vs_empathy.raw_score) * abs(dimensions.authority_vs_empathy.salience - 0.5)) + (min(dimensions.competition_vs_cooperation.raw_score, 1 - dimensions.competition_vs_cooperation.raw_score) * abs(dimensions.competition_vs_cooperation.salience - 0.5)) + (min(dimensions.self_reliance_vs_interdependence.raw_score, 1 - dimensions.self_reliance_vs_interdependence.raw_score) * abs(dimensions.self_reliance_vs_interdependence.salience - 0.5))) / 3"

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
          description: "Family model dimension score (0.0 = Nurturant Parent, 1.0 = Strict Father)"
        salience:
          type: number
          minimum: 0.0
          maximum: 1.0
          description: "Strategic prominence of the family model dimension (0.0-1.0)"
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
      required: ["authority_vs_empathy", "competition_vs_cooperation", "self_reliance_vs_interdependence"]
      properties:
        authority_vs_empathy:
          $ref: "#/definitions/score_object"
        competition_vs_cooperation:
          $ref: "#/definitions/score_object"
        self_reliance_vs_interdependence:
          $ref: "#/definitions/score_object"
    derived_metrics:
      type: object
      required: ["strict_father_model_score", "family_model_coherence_index", "family_model_dominance", "family_model_strategic_contradiction_index"]
      properties:
        strict_father_model_score:
          type: number
          minimum: 0.0
          maximum: 1.0
          description: "Overall Strict Father orientation across all dimensions"
        family_model_coherence_index:
          type: number
          minimum: 0.0
          maximum: 0.5
          description: "Coherence of family model deployment"
        family_model_dominance:
          type: number
          minimum: -1.5
          maximum: 1.5
          description: "Balance between Strict Father and Nurturant Parent orientations"
        family_model_strategic_contradiction_index:
          type: number
          minimum: 0.0
          maximum: 0.25
          description: "Strategic contradictions in family model deployment"

--- End of Machine-Readable Appendix ---
