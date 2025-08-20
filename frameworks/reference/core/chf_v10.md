# Constitutional Health Framework (CHF) v10.0

## Abstract & Raison d'Être

The Constitutional Health Framework provides a systematic approach to evaluating how political discourse affects constitutional system health through analysis of procedural legitimacy, institutional respect, and systemic continuity patterns. Drawing on Walter Bagehot's insight that constitutions are living systems of governance rather than mere documents, this framework assesses discourse impact across three fundamental dimensions of constitutional health, weighted by actual rhetorical emphasis patterns.

Constitutional democracy depends on discourse that reinforces rather than undermines fundamental democratic institutions and processes. Political communication can either strengthen constitutional norms or contribute to democratic erosion through procedural rejection, institutional subversion, and systemic replacement rhetoric. This framework provides a rigorous methodology for assessing the constitutional implications of political discourse with salience-weighted analysis that captures not just constitutional health/pathology but which dimensions receive the most rhetorical emphasis.

This framework is intended for political scientists, constitutional scholars, journalists, policy analysts, and researchers monitoring democratic health and constitutional resilience across different political systems and historical periods.

## Theoretical & Empirical Foundations

### Bagehot's Constitutional Insight

Walter Bagehot's *The English Constitution* (1867) revealed that constitutional systems are living arrangements of institutions, procedures, and practices - not just written documents. His distinction between "dignified" and "efficient" parts of government showed that constitutional health depends on the entire system functioning together.

**Core Innovation**: Constitutional systems work through the dynamic interaction of formal rules, informal practices, institutional authority, and evolutionary adaptation.

### Fukuyama's Institutional Analysis

Francis Fukuyama's work on institutional decay demonstrates that democratic breakdown often occurs through the gradual erosion of institutional norms and practices, not sudden constitutional crises. Institutions require both formal structure and informal legitimacy to function effectively.

**Key Insight**: Constitutional health requires both institutional capacity and public trust in institutional authority.

### Rauch's Constitution of Knowledge

Jonathan Rauch's *The Constitution of Knowledge* (2021) shows how epistemic institutions - the networks of knowledge production and verification - form an unwritten but essential part of democratic constitutionalism. These institutions depend on norms of truth-seeking and intellectual integrity.

**Critical Understanding**: Constitutional systems include not just political institutions but the entire infrastructure of democratic knowledge and discourse.

### The Importance of Salience Weighting

Building on political communication research, this framework recognizes that speakers make strategic choices about which constitutional issues to emphasize. A speaker might demonstrate moderate Procedural Legitimacy support consistently throughout their discourse, while only briefly attacking Institutional Respect in one section. The Procedural Legitimacy has much higher **salience** (rhetorical prominence) than Institutional attacks despite potentially lower raw intensity.

**Academic Foundation**: Constitutional emphasis patterns reveal democratic priorities and threats, enabling more sophisticated understanding of constitutional vulnerabilities through priority-aware analysis.

## Analytical Methodology

### Three-Dimensional Constitutional Health

The framework evaluates political discourse across three bipolar axes that form the foundation of constitutional health:

#### Procedural Axis: Procedural Legitimacy ↔ Procedural Rejection
- **Procedural Legitimacy**: Support for established procedures for political change and governance, respect for constitutional processes, adherence to democratic norms
- **Procedural Rejection**: Rejecting established procedures in favor of circumvention or extra-constitutional action, emergency power claims, process bypassing

#### Institutional Axis: Institutional Respect ↔ Institutional Subversion  
- **Institutional Respect**: Recognition of institutional authority, expertise, and legitimate governance role, support for checks and balances
- **Institutional Subversion**: Attacking institutional authority, expertise, or legitimate governance role, delegitimizing democratic institutions

#### Systemic Axis: Systemic Continuity ↔ Systemic Replacement
- **Systemic Continuity**: Support for maintaining and improving existing constitutional framework, gradual reform approaches
- **Systemic Replacement**: Advocating fundamental replacement rather than reform of constitutional framework, revolutionary change rhetoric

### Salience-Weighted Constitutional Analysis

**Salience** measures how much rhetorical emphasis the speaker places on each constitutional dimension, regardless of raw health/pathology scores. This dual-track analysis captures both the impact on constitutional health AND the speaker's constitutional priorities and strategic emphasis patterns.

**Enhanced Constitutional Intelligence**:
- **Constitutional Priorities**: Reveals which constitutional dimensions speakers prioritize in their political strategy
- **Strategic Constitutional Discourse**: Shows which constitutional issues speakers invest the most rhetorical effort in addressing
- **Authentic Constitutional Analysis**: Uses actual constitutional emphasis rather than researcher assumptions about dimension importance

### Constitutional Health Indices

The framework calculates several derived metrics to provide comprehensive constitutional health assessment:

**Axis-Level Health Indices**:
- **Procedural Health Index**: Measures overall procedural legitimacy vs. rejection, weighted by salience
- **Institutional Health Index**: Measures overall institutional respect vs. subversion, weighted by salience  
- **Systemic Health Index**: Measures overall systemic continuity vs. replacement, weighted by salience

**Summary Metrics**:
- **Constitutional Health Index**: Primary summary metric measuring overall constitutional health orientation, weighted by rhetorical prominence
- **Constitutional Pathology Index**: Measures overall constitutional threat level, weighted by salience

### Sequential Analysis Strategy

For highest fidelity analysis, it is recommended to run the three sequential analysis variants (sequential_procedural, sequential_institutional, sequential_systemic) and combine the results. This approach allows the analysis agent to focus exclusively on one axis at a time, reducing cognitive load and improving scoring accuracy.

### Concept Overlap Resolution

The framework addresses the inherent complexity of political discourse where speakers may simultaneously appeal to competing constitutional values. Each dimension includes explicit disambiguation rules to guide consistent scoring when conceptual overlap occurs:

- **Procedural Axis**: Distinguishes between legitimate process concerns and anti-constitutional bypass rhetoric
- **Institutional Axis**: Separates constructive institutional criticism from delegitimizing attacks
- **Systemic Axis**: Differentiates between reform advocacy and revolutionary replacement rhetoric

## Intended Application & Corpus Fit

### Target Corpus

This framework is designed for analysis of:
- **Political speeches and addresses**
- **Legislative debates and proceedings** 
- **Campaign communications and manifestos**
- **Policy advocacy and position papers**
- **Media commentary on constitutional issues**

### Applications

- **Constitutional Health Monitoring**: Track democratic resilience based on speakers' actual constitutional emphasis patterns
- **Cross-System Comparison**: Compare constitutional impacts using empirically-backed weighting across democratic traditions
- **Historical Analysis**: Assess constitutional threats based on rhetorical priority patterns across political eras
- **Early Warning Systems**: Detect constitutional degradation through constitutional salience pattern analysis

### Limitations

- Requires political discourse with explicit or implicit constitutional references
- Most effective with formal political communication rather than casual conversation
- Designed for democratic constitutional systems; may require adaptation for other governance models
- Salience weighting requires sufficient text length for reliable emphasis pattern detection

### System Validation Note

This framework is designed to work with the Discernus v10.0 analysis pipeline. Post-hoc statistical analysis will validate dimensional independence and internal consistency. The framework's reliability metrics are calculated automatically during analysis execution.

# --- Start of Machine-Readable Appendix ---

metadata:
  framework_name: "constitutional_health_framework"
  framework_version: "1.0.0"
  author: "Discernus Project"
  spec_version: "10.0"

# 5.2: Analysis Variants
analysis_variants:
  default:
    description: "Complete v10.0 implementation with salience-weighted constitutional health analysis. For highest fidelity analysis, it is recommended to execute the three `sequential_*` analysis variants and combine the results."
    analysis_prompt: |
      You are an expert analyst of constitutional health and democratic governance, grounded in constitutional theory, institutional analysis, and democratic erosion studies. Your task is to analyze the provided text using the Constitutional Health Framework v10.0.

      FRAMEWORK METHODOLOGY:
      This framework evaluates how political discourse affects constitutional system health through analysis of procedural legitimacy, institutional respect, and systemic continuity. It preserves complexity by independently scoring opposing dimensions for both intensity (raw_score) and rhetorical prominence (salience).

      DIMENSIONAL ANALYSIS:
      You must evaluate 6 dimensions across 3 opposing pairs:
      - Procedural: Procedural Legitimacy vs. Procedural Rejection
      - Institutional: Institutional Respect vs. Institutional Subversion
      - Systemic: Systemic Continuity vs. Systemic Replacement

      EVIDENCE STANDARDS:
      - Provide exact quotations, not paraphrases.
      - Prioritize direct constitutional and institutional indicators over interpretive inferences.
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

  sequential_procedural:
    description: "Focused analysis of Procedural axis dimensions (Procedural Legitimacy, Procedural Rejection)"
    analysis_prompt: |
      You are an expert analyst of constitutional health and democratic governance, grounded in constitutional theory, institutional analysis, and democratic erosion studies. Your task is to analyze the provided text using the Constitutional Health Framework v10.0.
      
      DIMENSIONAL ANALYSIS: Focus exclusively on the Procedural axis dimensions.
      
      **PROCEDURAL LEGITIMACY**: Look for support for established procedures, constitutional processes, democratic norms.
      **PROCEDURAL REJECTION**: Look for bypass rhetoric, emergency power claims, process dismissal.
      
      **SALIENCE ASSESSMENT**: 
      Salience measures rhetorical prominence, not intensity. Consider:
      - Frequency and repetition patterns throughout the text
      - Structural positioning (opening, closing, thesis statements)
      - Thematic centrality to the overall message
      - Rhetorical devices used for emphasis (metaphors, imagery, emotional appeals)
      SALIENCE ≠ INTENSITY. A dimension can have moderate intensity (0.5) but high salience (0.9) if it's rhetorically central.
      
      **CRITICAL DISAMBIGUATION**: When statements reference procedural concerns:
      - If primary function is supporting established processes → score as Procedural Legitimacy
      - If primary function is advocating bypass or circumvention → score as Procedural Rejection
      - If both present, score both independently and note tension
      
      **BOUNDARY CASES**:
      - "Reform the process" → legitimate improvement (Legitimacy) vs. circumvention (Rejection)
      - "Emergency action needed" → crisis response vs. constitutional bypass
      
      Use the scoring calibration guidelines defined for the `procedural_legitimacy` and `procedural_rejection` dimensions and focus only on these two dimensions.

  sequential_institutional:
    description: "Focused analysis of Institutional axis dimensions (Institutional Respect, Institutional Subversion)"
    analysis_prompt: |
      You are an expert analyst of constitutional health and democratic governance, grounded in constitutional theory, institutional analysis, and democratic erosion studies. Your task is to analyze the provided text using the Constitutional Health Framework v10.0.
      
      DIMENSIONAL ANALYSIS: Focus exclusively on the Institutional axis dimensions.
      
      **INSTITUTIONAL RESPECT**: Look for recognition of institutional authority, expertise, legitimate governance role.
      **INSTITUTIONAL SUBVERSION**: Look for attacks on institutional authority, delegitimizing rhetoric.
      
      **SALIENCE ASSESSMENT**: 
      Salience measures rhetorical prominence, not intensity. Consider:
      - Frequency and repetition patterns throughout the text
      - Structural positioning (opening, closing, thesis statements)
      - Thematic centrality to the overall message
      - Rhetorical devices used for emphasis (metaphors, imagery, emotional appeals)
      SALIENCE ≠ INTENSITY. A dimension can have moderate intensity (0.5) but high salience (0.9) if it's rhetorically central.
      
      **CRITICAL DISAMBIGUATION**: 
      - Institutional Respect involves recognizing legitimate authority and expertise
      - Institutional Subversion involves delegitimizing attacks on institutional authority
      - Constructive criticism can coexist with institutional respect
      - Score both if applicable
      
      **BOUNDARY CASES**:
      - "Institutional reform needed" → constructive criticism (Respect) vs. delegitimizing attack (Subversion)
      - "Corrupt establishment" → legitimate concern vs. institutional delegitimization
      
      Use the scoring calibration guidelines defined for the `institutional_respect` and `institutional_subversion` dimensions and focus only on these two dimensions.

  sequential_systemic:
    description: "Focused analysis of Systemic axis dimensions (Systemic Continuity, Systemic Replacement)"
    analysis_prompt: |
      You are an expert analyst of constitutional health and democratic governance, grounded in constitutional theory, institutional analysis, and democratic erosion studies. Your task is to analyze the provided text using the Constitutional Health Framework v10.0.
      
      DIMENSIONAL ANALYSIS: Focus exclusively on the Systemic axis dimensions.
      
      **SYSTEMIC CONTINUITY**: Look for support for maintaining/improving existing constitutional framework, gradual reform.
      **SYSTEMIC REPLACEMENT**: Look for advocacy of fundamental replacement, revolutionary change rhetoric.
      
      **SALIENCE ASSESSMENT**: 
      Salience measures rhetorical prominence, not intensity. Consider:
      - Frequency and repetition patterns throughout the text
      - Structural positioning (opening, closing, thesis statements)
      - Thematic centrality to the overall message
      - Rhetorical devices used for emphasis (metaphors, imagery, emotional appeals)
      SALIENCE ≠ INTENSITY. A dimension can have moderate intensity (0.5) but high salience (0.9) if it's rhetorically central.
      
      **CRITICAL DISAMBIGUATION**: Both may use "change" language:
      - Systemic Continuity: gradual reform, improvement within existing framework
      - Systemic Replacement: fundamental replacement, revolutionary transformation
      - Scope and radicalism of proposed change are key differentiators
      
      **BOUNDARY CASES**:
      - "Major constitutional reform" → improvement (Continuity) vs. replacement (Replacement)
      - "New system needed" → reform rhetoric vs. revolutionary replacement
      
      Use the scoring calibration guidelines defined for the `systemic_continuity` and `systemic_replacement` dimensions and focus only on these two dimensions.

# 5.3: Dimensions
dimensions:
  - name: "procedural_legitimacy"
    description: "Support for established procedures for political change and governance, respect for constitutional processes, adherence to democratic norms."
    markers:
      positive_examples:
        - { phrase: "constitutional process", explanation: "explicit support for established constitutional procedures" }
        - { phrase: "due process", explanation: "commitment to procedural fairness and legal norms" }
        - { phrase: "proper channels", explanation: "advocacy for working within established systems" }
        - { phrase: "electoral mandate", explanation: "recognition of democratic legitimacy through elections" }
        - { phrase: "legislative process", explanation: "support for formal lawmaking procedures" }
      negative_examples:
        - { phrase: "individual rights", explanation: "legal concept, not procedural legitimacy focus" }
        - { phrase: "policy outcomes", explanation: "substantive results, not procedural concerns" }
        - { phrase: "political strategy", explanation: "tactical considerations, not constitutional process" }
      boundary_cases:
        - { phrase: "reform the process", explanation: "could be procedural improvement or circumvention attempt" }
        - { phrase: "constitutional convention", explanation: "legitimate process vs. system replacement" }
    disambiguation:
      overlap_with_procedural_rejection:
        rule: "Procedural Legitimacy supports established processes; Procedural Rejection advocates circumvention."
        context_clues: "Support for working within system vs. bypass rhetoric"
        priority: "Intent and proposed method are key differentiators"
        co_occurrence_strategy: "Both may reference same procedures; assess whether supporting or circumventing"
    scoring_calibration:
      high: "0.7-1.0: Strong support for constitutional processes and democratic norms."
      medium: "0.4-0.6: Moderate procedural adherence, some process respect"
      low: "0.1-0.3: Weak procedural support, minimal process recognition"
      absent: "0.0: No support for established procedures"

  - name: "procedural_rejection"
    description: "Rejecting established procedures in favor of circumvention or extra-constitutional action, emergency power claims, process bypassing."
    markers:
      positive_examples:
        - { phrase: "bypass the system", explanation: "explicit advocacy for circumventing established procedures" }
        - { phrase: "emergency powers", explanation: "claims for extra-constitutional authority" }
        - { phrase: "broken system", explanation: "delegitimizing established procedures" }
        - { phrase: "people's will", explanation: "appeal to direct democracy over constitutional process" }
        - { phrase: "extraordinary measures", explanation: "advocacy for non-standard procedures" }
      negative_examples:
        - { phrase: "process improvement", explanation: "reform within system, not rejection" }
        - { phrase: "constitutional amendment", explanation: "formal change process, not bypass" }
        - { phrase: "legal challenge", explanation: "working within judicial system" }
      boundary_cases:
        - { phrase: "crisis requires action", explanation: "legitimate emergency response vs. constitutional bypass" }
        - { phrase: "people deserve better", explanation: "reform advocacy vs. system rejection" }
    disambiguation:
      overlap_with_procedural_legitimacy:
        rule: "Procedural Rejection advocates circumvention; Procedural Legitimacy supports established processes."
        context_clues: "Bypass rhetoric vs. working within system"
        priority: "Method and intent are key differentiators"
        co_occurrence_strategy: "Distinguish between reform (legitimacy) and circumvention (rejection)"
    scoring_calibration:
      high: "0.7-1.0: Strong advocacy for bypassing constitutional processes."
      medium: "0.4-0.6: Moderate process criticism, some bypass rhetoric"
      low: "0.1-0.3: Weak process rejection, minimal bypass language"
      absent: "0.0: No rejection of established procedures"

  - name: "institutional_respect"
    description: "Recognition of institutional authority, expertise, and legitimate governance role, support for checks and balances."
    markers:
      positive_examples:
        - { phrase: "institutional authority", explanation: "recognition of legitimate governance role" }
        - { phrase: "expert analysis", explanation: "deference to institutional expertise" }
        - { phrase: "separation of powers", explanation: "support for constitutional checks and balances" }
        - { phrase: "constitutional duty", explanation: "recognition of institutional obligations" }
        - { phrase: "judicial review", explanation: "support for institutional oversight" }
      negative_examples:
        - { phrase: "political opinion", explanation: "personal views, not institutional recognition" }
        - { phrase: "policy preference", explanation: "substantive positions, not institutional respect" }
        - { phrase: "partisan politics", explanation: "political competition, not institutional authority" }
      boundary_cases:
        - { phrase: "institutional reform", explanation: "improvement within system vs. delegitimization" }
        - { phrase: "accountability measures", explanation: "oversight vs. institutional attack" }
    disambiguation:
      overlap_with_institutional_subversion:
        rule: "Institutional Respect recognizes legitimate authority; Institutional Subversion delegitimizes institutions."
        context_clues: "Recognition of authority vs. delegitimizing attacks"
        priority: "Constructive criticism can coexist with institutional respect"
        co_occurrence_strategy: "Distinguish between reform (respect) and delegitimization (subversion)"
    scoring_calibration:
      high: "0.7-1.0: Strong recognition of institutional authority and expertise."
      medium: "0.4-0.6: Moderate institutional recognition, some deference"
      low: "0.1-0.3: Weak institutional respect, minimal authority recognition"
      absent: "0.0: No recognition of institutional authority"

  - name: "institutional_subversion"
    description: "Attacking institutional authority, expertise, or legitimate governance role, delegitimizing democratic institutions."
    markers:
      positive_examples:
        - { phrase: "corrupt institutions", explanation: "delegitimizing attack on institutional integrity" }
        - { phrase: "illegitimate authority", explanation: "rejection of institutional governance role" }
        - { phrase: "failed establishment", explanation: "wholesale delegitimization of institutions" }
        - { phrase: "biased system", explanation: "attack on institutional neutrality and expertise" }
        - { phrase: "deep state", explanation: "conspiracy rhetoric delegitimizing institutions" }
      negative_examples:
        - { phrase: "policy disagreement", explanation: "substantive differences, not institutional attack" }
        - { phrase: "constructive criticism", explanation: "reform-oriented feedback, not delegitimization" }
        - { phrase: "oversight concerns", explanation: "accountability measures, not subversion" }
      boundary_cases:
        - { phrase: "institutional capture", explanation: "legitimate concern vs. delegitimizing attack" }
        - { phrase: "reform needed", explanation: "improvement advocacy vs. institutional delegitimization" }
    disambiguation:
      overlap_with_institutional_respect:
        rule: "Institutional Subversion delegitimizes institutions; Institutional Respect recognizes legitimate authority."
        context_clues: "Delegitimizing attacks vs. recognition of authority"
        priority: "Intent to undermine vs. improve institutions"
        co_occurrence_strategy: "Distinguish between criticism (respect) and delegitimization (subversion)"
    scoring_calibration:
      high: "0.7-1.0: Strong attacks on institutional authority and legitimacy."
      medium: "0.4-0.6: Moderate institutional criticism, some delegitimization"
      low: "0.1-0.3: Weak institutional attacks, minimal delegitimization"
      absent: "0.0: No attacks on institutional authority"

  - name: "systemic_continuity"
    description: "Support for maintaining and improving existing constitutional framework, gradual reform approaches."
    markers:
      positive_examples:
        - { phrase: "constitutional stability", explanation: "support for maintaining constitutional framework" }
        - { phrase: "democratic tradition", explanation: "respect for established democratic practices" }
        - { phrase: "institutional continuity", explanation: "support for maintaining institutional structures" }
        - { phrase: "gradual reform", explanation: "advocacy for incremental improvement" }
        - { phrase: "constitutional amendment", explanation: "formal process for constitutional change" }
      negative_examples:
        - { phrase: "status quo", explanation: "general resistance to change, not constitutional focus" }
        - { phrase: "conservative policy", explanation: "policy positions, not constitutional continuity" }
        - { phrase: "traditional values", explanation: "cultural preferences, not constitutional framework" }
      boundary_cases:
        - { phrase: "major reform", explanation: "significant improvement vs. system replacement" }
        - { phrase: "constitutional change", explanation: "formal amendment vs. revolutionary replacement" }
    disambiguation:
      overlap_with_systemic_replacement:
        rule: "Systemic Continuity supports maintaining/improving existing framework; Systemic Replacement advocates fundamental replacement."
        context_clues: "Gradual improvement vs. revolutionary transformation"
        priority: "Scope and radicalism of proposed change are key"
        co_occurrence_strategy: "Distinguish between reform (continuity) and replacement (replacement)"
    scoring_calibration:
      high: "0.7-1.0: Strong support for maintaining and improving constitutional framework."
      medium: "0.4-0.6: Moderate continuity support, some framework respect"
      low: "0.1-0.3: Weak continuity support, minimal framework maintenance"
      absent: "0.0: No support for constitutional continuity"

  - name: "systemic_replacement"
    description: "Advocating fundamental replacement rather than reform of constitutional framework, revolutionary change rhetoric."
    markers:
      positive_examples:
        - { phrase: "new system", explanation: "advocacy for fundamental replacement of existing framework" }
        - { phrase: "radical transformation", explanation: "revolutionary change rather than reform" }
        - { phrase: "complete overhaul", explanation: "wholesale replacement of constitutional system" }
        - { phrase: "revolutionary change", explanation: "fundamental transformation of governance" }
        - { phrase: "new constitution", explanation: "replacement rather than amendment of constitutional framework" }
      negative_examples:
        - { phrase: "policy reform", explanation: "substantive changes, not constitutional replacement" }
        - { phrase: "institutional improvement", explanation: "reform within system, not replacement" }
        - { phrase: "constitutional amendment", explanation: "formal change process, not replacement" }
      boundary_cases:
        - { phrase: "fundamental change", explanation: "major reform vs. system replacement" }
        - { phrase: "new approach", explanation: "policy innovation vs. constitutional replacement" }
    disambiguation:
      overlap_with_systemic_continuity:
        rule: "Systemic Replacement advocates fundamental replacement; Systemic Continuity supports maintaining/improving existing framework."
        context_clues: "Revolutionary transformation vs. gradual improvement"
        priority: "Scope and radicalism of proposed change"
        co_occurrence_strategy: "Distinguish between replacement (replacement) and reform (continuity)"
    scoring_calibration:
      high: "0.7-1.0: Strong advocacy for fundamental constitutional replacement."
      medium: "0.4-0.6: Moderate replacement rhetoric, some revolutionary language"
      low: "0.1-0.3: Weak replacement advocacy, minimal revolutionary rhetoric"
      absent: "0.0: No advocacy for constitutional replacement"

# 5.4: Derived Metrics
derived_metrics:
  # Intermediate calculations for salience weighting
  - name: "procedural_health_salience_total"
    description: "Combined salience of procedural dimensions for weighting calculations."
    formula: "dimensions.procedural_legitimacy.salience + dimensions.procedural_rejection.salience + 0.001"

  - name: "institutional_health_salience_total"
    description: "Combined salience of institutional dimensions for weighting calculations."
    formula: "dimensions.institutional_respect.salience + dimensions.institutional_subversion.salience + 0.001"

  - name: "systemic_health_salience_total"
    description: "Combined salience of systemic dimensions for weighting calculations."
    formula: "dimensions.systemic_continuity.salience + dimensions.systemic_replacement.salience + 0.001"

  - name: "total_constitutional_salience"
    description: "Total salience across all constitutional dimensions for overall weighting."
    formula: "derived_metrics.procedural_health_salience_total + derived_metrics.institutional_health_salience_total + derived_metrics.systemic_health_salience_total"

  # Axis-level health indices
  - name: "procedural_health_index"
    description: "Salience-weighted procedural health score measuring legitimacy vs. rejection."
    formula: "((dimensions.procedural_legitimacy.raw_score * dimensions.procedural_legitimacy.salience) - (dimensions.procedural_rejection.raw_score * dimensions.procedural_rejection.salience)) / derived_metrics.procedural_health_salience_total"

  - name: "institutional_health_index"
    description: "Salience-weighted institutional health score measuring respect vs. subversion."
    formula: "((dimensions.institutional_respect.raw_score * dimensions.institutional_respect.salience) - (dimensions.institutional_subversion.raw_score * dimensions.institutional_subversion.salience)) / derived_metrics.institutional_health_salience_total"

  - name: "systemic_health_index"
    description: "Salience-weighted systemic health score measuring continuity vs. replacement."
    formula: "((dimensions.systemic_continuity.raw_score * dimensions.systemic_continuity.salience) - (dimensions.systemic_replacement.raw_score * dimensions.systemic_replacement.salience)) / derived_metrics.systemic_health_salience_total"

  # Summary metrics
  - name: "constitutional_health_index"
    description: "Primary summary metric measuring overall constitutional health orientation, weighted by rhetorical prominence."
    formula: "((derived_metrics.procedural_health_index * derived_metrics.procedural_health_salience_total) + (derived_metrics.institutional_health_index * derived_metrics.institutional_health_salience_total) + (derived_metrics.systemic_health_index * derived_metrics.systemic_health_salience_total)) / derived_metrics.total_constitutional_salience"

  - name: "constitutional_pathology_index"
    description: "Measures overall constitutional threat level, weighted by salience."
    formula: "((dimensions.procedural_rejection.raw_score * dimensions.procedural_rejection.salience) + (dimensions.institutional_subversion.raw_score * dimensions.institutional_subversion.salience) + (dimensions.systemic_replacement.raw_score * dimensions.systemic_replacement.salience)) / derived_metrics.total_constitutional_salience"

# 5.5: Output Schema
output_schema:
  type: object
  properties:
    dimensional_scores:
      type: object
      properties:
        procedural_legitimacy:
          $ref: "#/definitions/score_object"
        procedural_rejection:
          $ref: "#/definitions/score_object"
        institutional_respect:
          $ref: "#/definitions/score_object"
        institutional_subversion:
          $ref: "#/definitions/score_object"
        systemic_continuity:
          $ref: "#/definitions/score_object"
        systemic_replacement:
          $ref: "#/definitions/score_object"
      required: ["procedural_legitimacy", "procedural_rejection", "institutional_respect", "institutional_subversion", "systemic_continuity", "systemic_replacement"]
    derived_metrics:
      type: object
      properties:
        procedural_health_salience_total:
          type: number
          minimum: 0.001
        institutional_health_salience_total:
          type: number
          minimum: 0.001
        systemic_health_salience_total:
          type: number
          minimum: 0.001
        total_constitutional_salience:
          type: number
          minimum: 0.003
        procedural_health_index:
          type: number
          minimum: -1.0
          maximum: 1.0
        institutional_health_index:
          type: number
          minimum: -1.0
          maximum: 1.0
        systemic_health_index:
          type: number
          minimum: -1.0
          maximum: 1.0
        constitutional_health_index:
          type: number
          minimum: -1.0
          maximum: 1.0
        constitutional_pathology_index:
          type: number
          minimum: 0.0
          maximum: 1.0
  required: ["dimensional_scores", "derived_metrics"]
  definitions:
    score_object:
      type: object
      properties:
        raw_score:
          type: number
          minimum: 0.0
          maximum: 1.0
        salience:
          type: number
          minimum: 0.0
          maximum: 1.0
        evidence:
          type: string
        confidence:
          type: number
          minimum: 0.0
          maximum: 1.0
      required: ["raw_score", "salience", "evidence", "confidence"]

# --- End of Machine-Readable Appendix ---
